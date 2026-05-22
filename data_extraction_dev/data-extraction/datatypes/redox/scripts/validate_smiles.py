#!/usr/bin/env python3
"""
validate_smiles.py — check that SMILES strings in a CSV parse to valid molecules.

Uses RDKit if available, otherwise falls back to bracket-balance + character-set heuristics.
The RDKit path is strict (catches all malformed SMILES); the heuristic catches obvious garbage.

Usage:
    python validate_smiles.py <input_csv> [--smiles-col compound_name] [--notes-col notes]
    python validate_smiles.py /path/to/redox_mediators.csv

Looks for SMILES in two places:
  1. The named smiles-col directly (default: compound_name)
  2. A "SMILES=..." substring inside the named notes-col (default: notes)

Output:
  Prints rows whose SMILES fails validation.
  Exit code 0 if all valid, 1 if any invalid.
"""
import sys
import csv
import re
import argparse


_RDKIT = None


def get_rdkit():
    global _RDKIT
    if _RDKIT is None:
        try:
            from rdkit import Chem  # noqa
            from rdkit import RDLogger
            RDLogger.DisableLog("rdApp.*")
            _RDKIT = Chem
        except ImportError:
            _RDKIT = False
    return _RDKIT


def heuristic_check(smi):
    """Catch obviously malformed SMILES without RDKit."""
    if not smi or len(smi) < 2:
        return False, "empty or too short"
    # Bracket balance
    if smi.count("(") != smi.count(")"):
        return False, "unbalanced parentheses"
    if smi.count("[") != smi.count("]"):
        return False, "unbalanced square brackets"
    # 4 carbonyls on a single ring is impossible
    # Aromatic carbonyl notation `c(=O)` is non-standard; valid SMILES uses uppercase C(=O) for ketones
    if re.search(r"c1c\(=O\)c\(=O\)c\(=O\)c\(=O\)", smi):
        return False, "four aromatic carbonyls in a row (chemically impossible)"
    # Lowercase aromatic with =O ester/ketone is suspicious
    n_aromatic_carbonyl = len(re.findall(r"c\(=O\)|c=O", smi))
    if n_aromatic_carbonyl >= 3:
        return False, f"{n_aromatic_carbonyl} aromatic-carbonyl patterns (likely parsing error)"
    # Character set
    if not re.match(r"^[A-Za-z0-9@+\-\[\]\(\)=#$/\\.%,:*\s]+$", smi):
        return False, "invalid characters"
    return True, "passes heuristic checks"


def chemistry_plausibility(mol):
    """Catch chemically-implausible structures that RDKit's loose parser accepts.

    RDKit's MolFromSmiles can return a Mol object even when the structure violates
    real-world chemistry (e.g., aromatic ring with 4 carbonyl substituents). These
    checks reject the most common "syntactically valid, chemically impossible" cases.
    """
    from rdkit import Chem
    # Check 1: aromatic rings with too many carbonyls
    # In an aromatic 6-ring, at most 2 C=O substituents are tolerated chemically (quinone)
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) != 6:
            continue
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(a.GetIsAromatic() for a in ring_atoms):
            continue
        # Count exocyclic =O attached to ring atoms
        carbonyl_count = 0
        for ai in ring:
            atom = mol.GetAtomWithIdx(ai)
            for bond in atom.GetBonds():
                other = bond.GetOtherAtom(atom)
                if (other.GetSymbol() == "O" and bond.GetBondType() == Chem.BondType.DOUBLE
                        and other.GetIdx() not in ring):
                    carbonyl_count += 1
        if carbonyl_count > 2:
            return False, f"aromatic 6-ring has {carbonyl_count} exocyclic carbonyls (>2 is chemically impossible)"
    # Check 2: any carbon with too many bonds (RDKit Sanitize already catches most, but be safe)
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == "C" and atom.GetTotalDegree() > 4:
            return False, f"carbon atom has total degree {atom.GetTotalDegree()} (>4)"
    return True, "passes chemistry plausibility"


def validate(smi):
    """Return (valid: bool, msg: str)."""
    if not smi:
        return None, "no SMILES"
    Chem = get_rdkit()
    if Chem:
        try:
            # Use sanitize=True (default) so valence errors are caught
            mol = Chem.MolFromSmiles(smi, sanitize=True)
            if mol is None:
                return False, "RDKit could not parse (sanitize failed)"
            # Additional chemistry plausibility check
            ok, msg = chemistry_plausibility(mol)
            if not ok:
                return False, msg
            return True, f"valid compound_name (n_atoms={mol.GetNumAtoms()})"
        except Exception as e:
            return False, f"RDKit error: {e}"
    return heuristic_check(smi)


def extract_smiles(row, smiles_col, notes_col):
    """Pull SMILES from row, checking column directly and notes field.

    A field is treated as SMILES if it contains no spaces, contains at least one
    SMILES-indicative character (=, #, parens, brackets, ring digits), and starts
    with a recognizable element symbol or aromatic/atom-bracket character.
    """
    direct = (row.get(smiles_col) or "").strip()
    notes = (row.get(notes_col) or "").strip()
    if direct and " " not in direct and len(direct) >= 3:
        # Must contain at least one SMILES-typical character
        has_smiles_char = any(c in direct for c in "=#()[]")
        # Must start with an element-symbol-like character: any organic-subset letter or [
        starts_ok = direct[0] in "BCNOPSFIbcnopsfi[" or (direct[0].isalpha() and direct[0].isupper())
        if has_smiles_char and starts_ok:
            return direct
    m = re.search(r"SMILES=([^;]+)", notes)
    if m:
        return m.group(1).strip()
    return None


def main():
    ap = argparse.ArgumentParser(description="Validate SMILES strings in a CSV.")
    ap.add_argument("input_csv")
    ap.add_argument("--smiles-col", default="compound_name")
    ap.add_argument("--notes-col", default="notes")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--max-output", type=int, default=50)
    args = ap.parse_args()

    Chem = get_rdkit()
    if Chem:
        print(f"# Using RDKit for SMILES validation", file=sys.stderr)
    else:
        print(f"# RDKit not available; using heuristic checks (less strict)", file=sys.stderr)

    fail = 0
    total_with_smiles = 0
    with open(args.input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            smi = extract_smiles(row, args.smiles_col, args.notes_col)
            if not smi:
                continue
            total_with_smiles += 1
            valid, msg = validate(smi)
            if valid is False:
                fail += 1
                if fail <= args.max_output:
                    rid = row.get(args.id_col, row.get("#", "?"))
                    mol = (row.get(args.smiles_col) or "")[:40]
                    print(f"#{rid}  INVALID: {msg}")
                    print(f"   compound_name: {mol}")
                    print(f"   SMILES:   {smi[:80]}")

    print(f"\n# Total rows with SMILES: {total_with_smiles}", file=sys.stderr)
    print(f"# Invalid SMILES: {fail}", file=sys.stderr)
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()

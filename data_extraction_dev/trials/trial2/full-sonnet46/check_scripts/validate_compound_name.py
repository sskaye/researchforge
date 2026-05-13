#!/usr/bin/env python3
"""
validate_compound_name.py — validate compound names and (when present) SMILES.

Two kinds of checks:

  (a) Compound name shape: flag bare paper-local codes ("compound 3",
      "complex 9a", "4b"), truncated names ending in a substituent
      prefix without a parent scaffold ("...hydroxy", "...iodo"), and
      empty / whitespace-only names. These are common parsing artifacts.

  (b) When `compound_smiles` is populated: RDKit validity + chemistry
      plausibility (reject impossible structures like 4 carbonyls on one
      aromatic ring). Falls back to a syntactic check if RDKit isn't
      installed.

Usage:
    python3 validate_compound_name.py <input_csv>

Output:
    row <id>: <reason>
Exit 0 if clean; 1 if any flagged.
"""
import sys
import csv
import re
import argparse


# Patterns that fail the compound-name shape check
_BARE_CODE = re.compile(
    r"^(?:compound|complex|cpd|molecule|product|cmpd)\s+\d+[a-z]?$",
    re.IGNORECASE)
_BARE_NUMBER = re.compile(r"^\d+[a-z]?$")
_TRUNCATED_SUFFIXES = (
    "hydroxy", "iodo", "bromo", "chloro", "fluoro", "amino", "nitro",
    "phenyl", "methyl", "ethyl", "propyl", "butyl", "oxy", "thio",
    "sulfanyl", "yl",
)


# Truncated-locant-prefix patterns. Real IUPAC names rarely start with a
# bare capital letter + dash; the letter is almost always preceded by a
# locant digit ("7H-Indeno...", "1H-Pyrrolo...", "5-Bromo...", etc.).
# When the digit is missing, the name has been truncated. Specifically
# call out the indicated-hydrogen "<letter>H-" form because it's the
# most common truncation pattern observed.
_TRUNCATED_LOCANT_PREFIX = re.compile(
    r"^("
    r"[A-Z]H-[A-Z]"        # "H-Indeno...", "H-Pyrrolo..."
    r"|"
    r"H-(?:Pyrrolo|Indeno|Pyrazolo|Quinolino|Imidazo|Indolo|Benzo|"
    r"Pyrido|Pyrimid|Triazol|Thiadiaz|Oxadiaz|Carbazo|Phenazin)"
    r")"
)


def check_name_shape(name: str) -> str | None:
    if not name or not name.strip():
        return "compound_name is empty"
    n = name.strip()
    if _BARE_CODE.match(n):
        return f"compound_name is a bare paper-local code: {n!r}"
    if _BARE_NUMBER.match(n):
        return f"compound_name is just a number/letter code: {n!r}"
    # Truncated indicated-hydrogen locant: "H-Indeno..." where "7H-Indeno..."
    # is the real name; the leading digit got dropped during PDF wrap.
    if _TRUNCATED_LOCANT_PREFIX.match(n):
        return (f"compound_name appears truncated at an indicated-hydrogen "
                f"locant; expected leading digit before the H- "
                f"(name starts with {n[:30]!r})")
    # Truncated substituent prefix: name ends in "-<suffix>" or "<suffix>"
    # where suffix is in the truncated set AND the name has no recognizable
    # parent scaffold (no -ane, -ene, -ine, -one, -ole, etc. heteroatom hint).
    nl = n.lower().rstrip(".,; ")
    for suf in _TRUNCATED_SUFFIXES:
        if nl.endswith("-" + suf) or nl.endswith(suf):
            # Allow if the name also contains a parent indicator
            if re.search(
                r"(?:ane|ene|yne|ol|one|ene|ine|ole|enone|amine|amide|"
                r"acid|ester|nitrile|aldehyde|imide|indole|"
                r"pyridine|pyrimidine|quinoline|quinazoline|phenol|"
                r"benzene|anthracene|naphthalene|furan|thiophene|"
                r"morpholine|piperidine|piperazine|imidazole|triazole|"
                r"oxazole|thiazole|carbazole|chromenone|chromene)\b",
                    nl):
                continue
            return (f"compound_name appears truncated at substituent "
                    f"prefix {suf!r}; parent scaffold missing")
    return None


def check_smiles(smiles: str) -> str | None:
    """Validate SMILES; returns error string or None."""
    if not smiles or not smiles.strip():
        return None
    s = smiles.strip()
    try:
        from rdkit import Chem  # type: ignore
        from rdkit import RDLogger  # type: ignore
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        return _smiles_syntactic_check(s)

    mol = Chem.MolFromSmiles(s)
    if mol is None:
        return f"SMILES does not parse: {s!r}"
    # Chemistry plausibility: count carbonyls per aromatic ring
    n_atoms = mol.GetNumAtoms()
    if n_atoms < 2:
        return f"SMILES has <2 heavy atoms: {s!r}"
    # Specific: 4+ exocyclic carbonyls on a single 6-ring is implausible
    # for typical drug / mp-bp compounds (kekulé form has only 3 double bonds)
    from collections import defaultdict
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) == 6 and all(mol.GetAtomWithIdx(i).GetIsAromatic()
                                    for i in ring):
            n_carbonyl = 0
            for i in ring:
                atom = mol.GetAtomWithIdx(i)
                for nbr in atom.GetNeighbors():
                    if (nbr.GetSymbol() == "O" and
                            mol.GetBondBetweenAtoms(i, nbr.GetIdx())
                            .GetBondTypeAsDouble() == 2.0):
                        n_carbonyl += 1
            if n_carbonyl >= 4:
                return (f"SMILES has {n_carbonyl} carbonyls on one "
                        f"aromatic ring (implausible): {s!r}")
    return None


def _smiles_syntactic_check(s: str) -> str | None:
    """Minimal syntactic check when RDKit is absent."""
    if not re.fullmatch(r"[A-Za-z0-9@+\-\[\]()=#/\\.%*$]+", s):
        return f"SMILES contains invalid characters: {s!r}"
    # Brackets balanced
    if s.count("(") != s.count(")"):
        return f"SMILES parenthesis imbalance: {s!r}"
    if s.count("[") != s.count("]"):
        return f"SMILES square-bracket imbalance: {s!r}"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    args = ap.parse_args()
    flagged = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = row.get("id", "?")
            msg = check_name_shape(row.get("compound_name", ""))
            if msg:
                print(f"row {rid}: {msg}")
                flagged += 1
                continue
            smiles_msg = check_smiles(row.get("compound_smiles", ""))
            if smiles_msg:
                print(f"row {rid}: {smiles_msg}")
                flagged += 1
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

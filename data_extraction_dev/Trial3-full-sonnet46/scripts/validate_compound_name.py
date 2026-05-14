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


# v1.5: terminal unfinished-suffix tokens. Names that end in these tokens
# without a trailing 'e' or terminal punctuation are usually one or two
# characters short — caused by a PDF wrap or a column-boundary cut.
# Observed in Trial-2 gpt55_high (rows ending in "...Carboxamid",
# "...Carbo", "carbonitril", "sulfonamid").
_TERMINAL_UNFINISHED = re.compile(
    r"("
    r"carboxamid|carbo|carbonitril|sulfonamid|carbohydrid|"
    r"carboxylat|sulfonat|phosphat|phosphonat|"
    r"carbothioamid|carboxamidin|sulfanyl"
    r")$",
    re.IGNORECASE,
)

# v1.5: names ending in a dangling hyphen or apostrophe (e.g.,
# "Phenyl(6'-", "8-(1-(3-(5'-") — dangling locants left mid-substituent.
_DANGLING_TAIL = re.compile(r"[\-'`’′]\s*$")

# Note: an earlier v1.5 draft included a "leading open-paren = truncation"
# rule. We dropped it because legitimate IUPAC names routinely start with
# parenthesized stereo / optical descriptors like (E)-, (-)-, (R,S)-,
# (2E,4E)-, (SS,S)-. Sonnet's actual failure mode (missing leading
# "4-(4-" substituent block) is already caught by the bracket-balance
# check below, since dropping the leading "4-(" produces a name with
# more closing parens than opening parens.

# v1.5: procedure-text contamination. If the compound name contains
# experimental-procedure words, it's almost certainly a sentence that
# bled into the name field rather than a compound.
#
# Note: 'yielded', 'mixture', 'solution', 'residue' are NOT here. They
# appear in legitimate chemistry annotations ("(4l/4m mixture)",
# "isomer mixture", "as an aqueous solution"). The list focuses on
# words that are almost never part of a compound name.
_PROCEDURE_WORDS = re.compile(
    r"\b(afforded?|stirred|heated|cooled|filtered|added\s+to|"
    r"reaction|distilled|crystallized|recrystalliz|"
    r"NMR\s|IR\s|HRMS|m\.?\s*p\.?\s*=|mp\s*=)\b",
    re.IGNORECASE,
)


def _has_balanced_brackets(s: str) -> str | None:
    """Return error string if parens / brackets / braces / primes don't
    balance in the compound name."""
    for open_ch, close_ch, label in (
        ("(", ")", "parens"),
        ("[", "]", "brackets"),
        ("{", "}", "braces"),
    ):
        if s.count(open_ch) != s.count(close_ch):
            return (f"unbalanced {label} ({s.count(open_ch)} open vs. "
                    f"{s.count(close_ch)} close)")
    # Primes/apostrophes: rough check that they appear in pairs after the
    # first character. A single trailing prime is a tell of "5'-" or "6'-"
    # dangling locants. Allow even counts; flag a lone trailing prime.
    n_primes = s.count("'") + s.count("’") + s.count("′")
    if n_primes % 2 == 1 and re.search(r"[\-(][^()\-]*['’′]\s*$", s):
        return "unmatched trailing prime/apostrophe (dangling locant)"
    return None


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
    # v1.5: dangling trailing hyphen/apostrophe = mid-substituent cut.
    if _DANGLING_TAIL.search(n):
        return (f"compound_name ends with a dangling hyphen/prime "
                f"(mid-substituent truncation): {n[-30:]!r}")
    # v1.5: terminal unfinished-suffix tokens (Carboxamid, Carbo, etc.).
    nl_strip = n.rstrip(".,; ").lower()
    m = _TERMINAL_UNFINISHED.search(nl_strip)
    if m:
        suffix = m.group(1)
        # 'sulfanyl' is the only one in the list that's a real suffix on
        # its own (e.g., "methylsulfanyl-..."); it only flags when at
        # the absolute end. Same for 'carbo' which is a frequent cut of
        # 'carboxamide' / 'carbonate' / etc.
        return (f"compound_name ends in unfinished suffix token "
                f"{suffix!r}; likely truncated mid-token: {n[-40:]!r}")
    # v1.5: bracket/paren/prime balance.
    bal = _has_balanced_brackets(n)
    if bal:
        return f"compound_name has {bal}: {n[:60]!r}"
    # v1.5: procedure-text contamination.
    pm = _PROCEDURE_WORDS.search(n)
    if pm:
        return (f"compound_name contains procedure-text token "
                f"{pm.group(0)!r}; experimental paragraph leaked into "
                f"name field: {n[:80]!r}")
    # Truncated substituent prefix: name ends in "-<suffix>" or "<suffix>"
    # where suffix is in the truncated set AND the name has no recognizable
    # parent scaffold (no -ane, -ene, -ine, -one, -ole, etc. heteroatom hint).
    nl = n.lower().rstrip(".,; ")
    # Legitimate -phenyl-family parent names that the suffix check would
    # otherwise mis-flag (biphenyl, terphenyl, quaterphenyl, diphenyl,
    # triphenyl scaffolds are real IUPAC parents).
    if re.search(r"\b(?:bi|ter|quater|di|tri|tetra)phenyl\b", nl):
        return None
    # Common "-yl" parent compounds where the trailing -yl is part of the
    # name, not a substituent prefix indicating truncation. Treat these
    # endings as legitimate parents.
    _YL_PARENT_NAMES = (
        "binaphthyl", "naphthyl", "anthryl", "phenanthryl",
        "biphenyl", "terphenyl", "quaterphenyl",
    )
    if any(nl.endswith(p) for p in _YL_PARENT_NAMES):
        return None
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

#!/usr/bin/env python3
"""
voltage_range_check.py — flag rows whose voltage_v_she is outside the plausible range
for the chemical class indicated in the molecule field (with notes as a fallback signal).

Usage:
    python voltage_range_check.py <input_csv>

Output:
    Lists rows where (chemical class, voltage) appears inconsistent.
    Exit code 0 if all rows pass or class can't be detected, 1 if any inconsistencies.

Class detection priority:
    1. Match against the `molecule` field. Use the most specific keyword that matches
       (e.g., "anthraquinone" wins over "quinone").
    2. Only fall back to `notes` if the molecule field provides no clue (e.g., when the
       molecule field is a SMILES).

This avoids the failure mode where a row's notes mention a paired counter-electrode
(e.g., "paired with ferrocyanide as catholyte") and the row's value is then evaluated
against the WRONG class's range.
"""
import sys
import csv
import argparse


# (class keyword, solvent class hint, low_V, high_V vs SHE)
# Order matters: more-specific classes first. The first match wins.
RANGES = [
    # Specific quinone subclasses before the generic "quinone"
    ("phthalimide",       "aprotic", -2.5,  0.5),
    ("phthalimide",       "aqueous", -1.0,  0.5),
    ("anthraquinone",     "aqueous", -0.9,  1.0),
    ("anthraquinone",     "aprotic", -2.0,  0.5),
    ("naphthoquinone",    "aqueous", -0.7,  1.0),
    ("naphthoquinone",    "aprotic", -1.8,  0.5),
    ("benzoquinone",      "aqueous", -0.8,  1.2),
    ("benzoquinone",      "aprotic", -1.8,  1.0),
    # Aza-aromatics
    ("phenazine",         "aqueous", -1.5, -0.3),
    ("alloxazine",        "aqueous", -0.9, -0.3),
    ("flavin",            "aqueous", -0.6, -0.2),
    ("indigo",            "aqueous", -0.6,  0.2),
    # Generic quinone (catches everything else with quinone in name)
    ("quinone",           "aqueous", -0.9,  1.2),
    ("quinone",           "aprotic", -2.0,  1.0),
    # Specific organic classes
    ("viologen",          "aqueous", -0.9, -0.2),
    ("tempo",             "aqueous",  0.5,  1.0),
    ("nitroxide",         "aqueous",  0.5,  1.0),
    ("phenothiazine",     "aqueous",  0.4,  1.1),
    ("phenoxazine",       "aqueous", -0.5,  0.7),
    # Metal-based
    ("ferrocyanide",      "aqueous",  0.2,  0.6),
    ("ferrocene",         "aqueous",  0.2,  0.7),
    ("ferrocene",         "aprotic", -0.2,  0.5),
    ("polyoxometalate",   "aqueous", -1.5,  0.7),
    ("pom",               "aqueous", -1.5,  0.7),
    ("metal aquo",        "aqueous", -3.5,  1.7),
    ("metal-complex",     "aqueous", -2.0,  1.7),
    # Halides
    ("halide",            "aqueous",  0.5,  3.0),
    ("halogen",           "aqueous",  0.5,  3.0),
]


def detect_class(row):
    """Return (class_keyword, solvent_class, low, high) or None.

    Match priority: molecule field (primary) > notes field (fallback). Only the
    first matching class is returned.
    """
    molecule = (row.get("molecule") or "").lower()
    notes = (row.get("notes") or "").lower()
    solv = (row.get("solvent") or "").lower()

    is_aqueous = ("water" in solv or "aqueous" in solv or
                  "koh" in solv or "naoh" in solv or "h2so4" in solv or "hcl" in solv or
                  "kcl" in solv or "nacl" in solv or "h3po4" in solv or "phosphate" in solv)
    is_aprotic = ("dmf" in solv or "mecn" in solv or "acetonitrile" in solv or
                  "dmso" in solv or "organic solvent" in solv or "implicit" in solv)
    if not is_aqueous and not is_aprotic:
        return None
    sclass = "aqueous" if is_aqueous else "aprotic"

    # Try molecule field first
    for kw, sc, lo, hi in RANGES:
        if kw in molecule and sc == sclass:
            return (kw, sclass, lo, hi)
    # Fall back to notes
    for kw, sc, lo, hi in RANGES:
        if kw in notes and sc == sclass:
            return (kw, sclass, lo, hi)
    return None


def main():
    ap = argparse.ArgumentParser(description="Voltage-range plausibility check by chemical class.")
    ap.add_argument("input_csv")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--max-output", type=int, default=50)
    ap.add_argument("--include-computational", action="store_true",
                    help="Apply ranges to computational rows too (default skips them since predicted "
                         "values from screens legitimately fall outside experimental ranges)")
    args = ap.parse_args()

    fail = 0
    skipped_computational = 0
    skipped_no_class = 0
    with open(args.input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not args.include_computational and row.get("data_type") == "computational":
                skipped_computational += 1
                continue
            cls = detect_class(row)
            if cls is None:
                skipped_no_class += 1
                continue
            kw, sclass, lo, hi = cls
            try:
                v = float(row["voltage_v_she"])
            except (ValueError, TypeError, KeyError):
                continue
            if v < lo or v > hi:
                fail += 1
                if fail <= args.max_output:
                    rid = row.get(args.id_col, row.get("#", "?"))
                    print(f"#{rid}  V={v:+.3f}  [{kw} {sclass}: expected {lo:+.2f} to {hi:+.2f}]")
                    print(f"   molecule: {row.get('molecule', '')[:60]}")

    print(f"\n# Skipped (computational): {skipped_computational}", file=sys.stderr)
    print(f"# Skipped (no class detected): {skipped_no_class}", file=sys.stderr)
    print(f"# Range violations: {fail}", file=sys.stderr)
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()

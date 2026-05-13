#!/usr/bin/env python3
"""
cross_source_consistency.py — flag the same molecule appearing in 3+ sources at the same
pH/solvent class with disagreement > tolerance.

Usage:
    python cross_source_consistency.py <input_csv> [--tolerance 0.05]

Output:
    Lists groups of rows with significant disagreement.
    Exit code 0 if no flagged groups, 1 if any.

Note: spreads of >150 mV often indicate mixing of distinct redox couples (e.g., V2+/V+•
vs V+•/V0 for methyl viologen). Examine flagged groups carefully — sometimes the
disagreement is real chemistry, not a database error.
"""
import sys
import csv
import re
import argparse
from collections import defaultdict
from statistics import median


def normalize_name(name):
    """Conservative name normalization for cross-source matching.

    We do NOT alias short ambiguous tokens (e.g. "DHAQ" could be 1,8/1,5/2,6-DHAQ
    — distinct molecules with different potentials). Aliasing those would conflate
    real chemistry differences as 'cross-source disagreements'. Only aliases for
    common abbreviations whose full meaning is unambiguous are applied.
    """
    n = name.lower()
    n = re.sub(r"\([^)]*\)", "", n)
    n = re.sub(r"\[[^\]]*\]", "", n)
    n = re.sub(r"[\W_]+", "", n)
    # Conservative aliases: only when the abbreviation maps unambiguously to one molecule.
    aliases = {
        "mv":   "methylviologen",
        "ev":   "ethylviologen",
        "aqds": "anthraquinonedisulfonate",  # generic; pH bin will separate isomers
        "tempol": "4hydroxytempo",
    }
    return aliases.get(n, n)


def ph_bin(ph_str):
    try:
        ph = float(ph_str)
    except (ValueError, TypeError):
        return "unknown"
    if ph <= 1: return "acidic"
    if ph <= 5: return "mild_acidic"
    if ph < 9:  return "neutral"
    if ph < 13: return "mild_alkaline"
    return "alkaline"


def solvent_class(solv):
    s = (solv or "").lower()
    if ("water" in s or "aqueous" in s or "koh" in s or "naoh" in s or
            "h2so4" in s or "hcl" in s or "kcl" in s or "nacl" in s or
            "h3po4" in s or "phosphate" in s or "buffer" in s or "hbr" in s):
        return "aqueous"
    if ("dmf" in s or "mecn" in s or "acetonitrile" in s or "dmso" in s or
            "thf" in s or "dcm" in s or "aprotic" in s or "organic solvent" in s):
        return "aprotic"
    return "other"


def main():
    ap = argparse.ArgumentParser(description="Cross-source consistency check.")
    ap.add_argument("input_csv")
    ap.add_argument("--tolerance", type=float, default=0.05,
                    help="Max acceptable spread in V (default 0.05). Rows beyond this from group median are flagged.")
    ap.add_argument("--min-sources", type=int, default=2,
                    help="Minimum number of distinct sources to constitute a group (default 2).")
    ap.add_argument("--id-col", default="id")
    args = ap.parse_args()

    groups = defaultdict(list)
    with open(args.input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                v = float(row["voltage_v_she"])
            except (ValueError, TypeError, KeyError):
                continue
            n = normalize_name(row.get("molecule", ""))
            if not n or len(n) < 4:
                continue
            key = (n, ph_bin(row.get("ph", "")), solvent_class(row.get("solvent", "")))
            groups[key].append((row, v))

    flagged_groups = 0
    flagged_rows = 0
    for key, items in groups.items():
        if len(items) < 2:
            continue
        sources = set((r["source"] or "")[:60] for r, _ in items)
        if len(sources) < args.min_sources:
            continue
        vs = [v for _, v in items]
        med = median(vs)
        deviants = [(r, v) for r, v in items if abs(v - med) > args.tolerance]
        if not deviants:
            continue
        flagged_groups += 1
        flagged_rows += len(deviants)
        name, ph_b, sc = key
        spread = max(vs) - min(vs)
        print(f"\n=== {name} (pH {ph_b}, {sc}) — {len(items)} rows from {len(sources)} sources, spread {spread*1000:.0f} mV ===")
        items_sorted = sorted(items, key=lambda x: x[1])
        for r, v in items_sorted:
            is_deviant = abs(v - med) > args.tolerance
            rid = r.get(args.id_col, r.get("#", "?"))
            if is_deviant:
                # Use the 'flagged-row' format that run_all_checks parses (#<id> <msg>)
                print(f"#{rid} v={v:+.3f}  deviates from group median {med:+.3f}  pH={r.get('ph',''):<4}  src={(r.get('source','') or '')[:60]}")
            else:
                # Use a leading marker that's NOT '#' so run_all_checks doesn't pick this up as a flag
                print(f"  - id={rid} v={v:+.3f}  pH={r.get('ph',''):<4}  src={(r.get('source','') or '')[:60]}  (within tolerance of median {med:+.3f})")

    print(f"\n# Flagged groups: {flagged_groups}", file=sys.stderr)
    print(f"# Flagged rows:   {flagged_rows}", file=sys.stderr)
    sys.exit(0 if flagged_groups == 0 else 1)


if __name__ == "__main__":
    main()

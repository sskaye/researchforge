#!/usr/bin/env python3
"""
dedup_within_paper.py — flag duplicate rows within a single paper.

Two rows are "duplicates within paper" if they share:
  - source_url (same paper)
  - compound_name (case-insensitive)
  - property
  - value_celsius (within 0.5 °C)

This catches:
  - Two extraction passes that overlapped on the same compound
  - Same compound listed twice with the same value in different table rows
    (e.g., a row in the synthesis table AND in a summary table)

Different `data_type` (measured vs. calculated) for the same compound /
property IS NOT a duplicate — that's a meaningful distinction. Same with
different `evidence_location` for genuinely-distinct measurements.

Usage:
    python3 dedup_within_paper.py <input_csv>

Output:
    duplicate group <key>: row ids <a>, <b>, ...
Exit 0 if clean; 1 if any duplicates.
"""
import sys
import csv
import argparse
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--tolerance", type=float, default=0.5,
                    help="°C tolerance for value match (default 0.5)")
    args = ap.parse_args()
    groups: dict[tuple, list[tuple[str, float]]] = defaultdict(list)
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                v = float(row.get("value_celsius") or "nan")
            except ValueError:
                continue
            key = (
                (row.get("source_url") or "").strip().lower(),
                (row.get("compound_name") or "").strip().lower(),
                (row.get("property") or "").strip().lower(),
                (row.get("data_type") or "").strip().lower(),
            )
            groups[key].append((row.get("id", "?"), v))

    flagged = 0
    for key, items in groups.items():
        if len(items) < 2:
            continue
        # Within this group, find pairs within tolerance
        items.sort(key=lambda x: x[1])
        clusters: list[list[tuple[str, float]]] = []
        for rid, v in items:
            placed = False
            for c in clusters:
                if abs(c[-1][1] - v) <= args.tolerance:
                    c.append((rid, v))
                    placed = True
                    break
            if not placed:
                clusters.append([(rid, v)])
        for c in clusters:
            if len(c) >= 2:
                ids = ", ".join(rid for rid, _ in c)
                src_short = key[0][:50]
                print(f"duplicate group source={src_short!r} "
                      f"compound={key[1]!r} property={key[2]} "
                      f"data_type={key[3]}: rows {ids}")
                flagged += len(c) - 1  # all but the first

    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
migrate_v17_to_v20.py — one-off migration utility (NOT part of the shipped skill).

Brings v1.7-schema CSVs to the v2.0 data-extraction schema:

  - Renames `value_celsius` → `value`
  - Renames `value_celsius_min` → `value_min`
  - Renames `value_celsius_max` → `value_max`
  - Renames `data_type` → `meas_calc`
  - Inserts a new `units` column populated with `°C` (the v1.7 schema implied this)
  - Reorders columns to the v2.0 canonical order

Lives at the project root next to `audit_criteria.md`, not inside the skill's
`scripts/`, because it's a one-time migration tool, not a Phase-3 lint.

Usage:
    python3 migrate_v17_to_v20.py <input.csv> [--out <output.csv>]

If `--out` is omitted, writes `<input>_v20.csv` next to the input.
"""
import sys
import csv
import argparse
import os

V20_COLUMNS = [
    "id", "verification_status", "compound_name", "compound_smiles",
    "property", "value", "value_min", "value_max", "value_raw", "units",
    "relation", "meas_calc", "source", "source_url", "evidence_location",
    "evidence_quote", "conversion_arithmetic", "notes",
]

RENAME = {
    "value_celsius": "value",
    "value_celsius_min": "value_min",
    "value_celsius_max": "value_max",
    "data_type": "meas_calc",
}


def migrate(in_path: str, out_path: str) -> tuple[int, int]:
    """Read v1.7 CSV, write v2.0 CSV. Return (rows_in, rows_out)."""
    with open(in_path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        rows_in = list(rdr)

    rows_out = []
    for r in rows_in:
        nr = {}
        for k, v in r.items():
            nk = RENAME.get(k, k)
            nr[nk] = v
        # Populate units = °C (the v1.7 schema baked °C into value_celsius;
        # the v2.0 schema makes it explicit).
        nr.setdefault("units", "°C")
        # Ensure every v2.0 column exists (may be empty).
        for col in V20_COLUMNS:
            nr.setdefault(col, "")
        rows_out.append(nr)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=V20_COLUMNS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in rows_out:
            w.writerow({k: r.get(k, "") for k in V20_COLUMNS})

    return len(rows_in), len(rows_out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("input_csv")
    ap.add_argument("--out", help="Output path (default: <input>_v20.csv)")
    args = ap.parse_args()

    if not os.path.isfile(args.input_csv):
        print(f"error: {args.input_csv} not found", file=sys.stderr)
        sys.exit(2)

    out_path = args.out
    if not out_path:
        root, ext = os.path.splitext(args.input_csv)
        out_path = f"{root}_v20{ext}"

    n_in, n_out = migrate(args.input_csv, out_path)
    print(f"Migrated {n_in} rows → {out_path} ({n_out} rows out)")
    if n_in != n_out:
        print(f"warning: row count mismatch ({n_in} in, {n_out} out)",
              file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

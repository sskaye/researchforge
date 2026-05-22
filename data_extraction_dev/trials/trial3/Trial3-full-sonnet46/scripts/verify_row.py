#!/usr/bin/env python3
"""
verify_row.py — run all programmatic Phase-3 checks against a single row.

Note: this script does NOT verify the evidence_quote against the actual
paper file (use verify_evidence_quote.py for that) and does NOT replace
the Phase 4 independent-agent verification. It's a fast deterministic
sanity check for one row.

Usage:
    python3 verify_row.py <csv_path> <row_id>
"""
import sys
import csv
import argparse
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from value_range_check import check_row as range_check  # noqa: E402
from unit_conversion_arithmetic import check_row as arith_check  # noqa: E402
from validate_compound_name import (  # noqa: E402
    check_name_shape, check_smiles,
)


REQUIRED_FIELDS = (
    "compound_name", "property", "value_celsius", "value_raw",
    "data_type", "source", "source_url", "evidence_location",
    "evidence_quote",
)


def required_fields(row: dict) -> list[str]:
    out = []
    for k in REQUIRED_FIELDS:
        v = (row.get(k) or "").strip()
        if not v:
            out.append(f"required field {k} is empty")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("row_id")
    args = ap.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if str(row.get("id", "")) != str(args.row_id):
                continue
            findings = []
            findings += required_fields(row)
            shape = check_name_shape(row.get("compound_name", ""))
            if shape:
                findings.append(shape)
            sm = check_smiles(row.get("compound_smiles", ""))
            if sm:
                findings.append(sm)
            rng = range_check(row)
            if rng:
                findings.append(rng)
            arith = arith_check(row)
            if arith:
                findings.append(arith)
            print(f"row {args.row_id}:")
            if not findings:
                print("  ✓ all programmatic checks passed")
            else:
                for f in findings:
                    print(f"  ✗ {f}")
            sys.exit(0 if not findings else 1)
    print(f"row_id {args.row_id} not found in {args.csv_path}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()

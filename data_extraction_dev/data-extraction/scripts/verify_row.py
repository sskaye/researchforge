#!/usr/bin/env python3
"""
verify_row.py — run all programmatic Phase-3 checks against a single row.

Note: this script does NOT verify the evidence_quote against the actual
paper file (use verify_evidence_quote.py for that) and does NOT replace
the Phase 4 independent-agent verification. It's a fast deterministic
sanity check for one row.

Usage:
    python3 verify_row.py --datatype <name> <csv_path> <row_id>

The --datatype flag is REQUIRED. The skill is data-type-agnostic at its
core but every row verification must specify which overlay's value-range /
unit-conversion checks to apply. If the named overlay folder doesn't
exist, the script halts with the list of installed data types.
"""
import sys
import csv
import argparse
import importlib.util
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from validate_compound_name import (  # noqa: E402
    check_name_shape, check_smiles,
)


REQUIRED_FIELDS = (
    "compound_name", "property", "value", "value_raw", "units",
    "meas_calc", "source", "source_url", "evidence_location",
    "evidence_quote",
)


def _available_datatypes() -> list[str]:
    base = os.path.join(SKILL_ROOT, "datatypes")
    if not os.path.isdir(base):
        return []
    return sorted(
        d for d in os.listdir(base)
        if os.path.isdir(os.path.join(base, d)) and not d.startswith("_")
    )


def required_fields(row: dict) -> list[str]:
    out = []
    for k in REQUIRED_FIELDS:
        v = (row.get(k) or "").strip()
        if not v:
            if k == "units":
                # Allow empty units for categorical-valued properties.
                val = (row.get("value") or "").strip()
                try:
                    float(val)
                except ValueError:
                    continue
            out.append(f"required field {k} is empty")
    return out


def _load_overlay_check_row(datatype: str):
    """Yield `check_row` callables found in any datatypes/<datatype>/scripts/*.py
    that exposes one. Scripts without a `check_row` function are skipped
    silently — they may be e.g. CSV-level lints that don't operate per row."""
    pattern = os.path.join(SKILL_ROOT, "datatypes", datatype, "scripts", "*.py")
    for sp in sorted(glob.glob(pattern)):
        modname = f"_overlay_{os.path.basename(sp)[:-3]}"
        spec = importlib.util.spec_from_file_location(modname, sp)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"  (skipping {sp}: {e})", file=sys.stderr)
            continue
        fn = getattr(mod, "check_row", None)
        if callable(fn):
            yield os.path.basename(sp), fn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("row_id")
    ap.add_argument("--datatype", required=False,
                    help="REQUIRED. Name of the data-type overlay under "
                         "datatypes/ (e.g., mp_bp, redox).")
    args = ap.parse_args()

    available = _available_datatypes()
    if not args.datatype:
        print("error: --datatype is required.", file=sys.stderr)
        if available:
            print(f"available data types: {', '.join(available)}",
                  file=sys.stderr)
        sys.exit(2)
    if args.datatype not in available:
        print(f"error: unknown data type {args.datatype!r}.", file=sys.stderr)
        if available:
            print(f"available data types: {', '.join(available)}",
                  file=sys.stderr)
        sys.exit(2)

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
            # Overlay scripts that expose a check_row()
            for name, fn in _load_overlay_check_row(args.datatype):
                try:
                    msg = fn(row)
                except Exception as e:
                    findings.append(f"{name} raised: {e}")
                    continue
                if msg:
                    findings.append(f"[{name}] {msg}")
            print(f"row {args.row_id}:")
            if not findings:
                print("  ✓ all programmatic checks passed")
            else:
                for fnd in findings:
                    print(f"  ✗ {fnd}")
            sys.exit(0 if not findings else 1)
    print(f"row_id {args.row_id} not found in {args.csv_path}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()

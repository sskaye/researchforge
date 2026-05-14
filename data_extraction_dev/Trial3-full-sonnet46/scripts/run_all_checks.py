#!/usr/bin/env python3
"""
run_all_checks.py — run every Phase-3 sanity check on a CSV and emit a
flags report.

Bundles:
  - Required-field check
  - validate_compound_name.py (name shape + SMILES if present)
  - value_range_check.py
  - unit_conversion_arithmetic.py
  - verify_doi.py (only if --paper-root provided)
  - verify_evidence_quote.py (only if --paper-root provided)
  - dedup_within_paper.py
  - Placeholder-citation detection
  - Truncated-compound-name pattern

Usage:
    python3 run_all_checks.py <input_csv> [--paper-root <dir>] [--out flags.csv]
"""
import sys
import csv
import os
import re
import argparse
import subprocess
from collections import defaultdict


HERE = os.path.dirname(os.path.abspath(__file__))


def _run(cmd: list[str]) -> tuple[int, str]:
    """Run a subprocess and return (returncode, stdout). Both stderr and
    stdout pass through to the umbrella's stderr/stdout so the user sees
    each sub-script's findings."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stderr.write(r.stderr)
    if r.stdout:
        sys.stdout.write(r.stdout)
    return r.returncode, r.stdout


def required_fields_check(rows: list[dict]) -> dict[str, list[str]]:
    flags: dict[str, list[str]] = defaultdict(list)
    REQUIRED = ("compound_name", "property", "value_celsius", "value_raw",
                "data_type", "source", "source_url", "evidence_location",
                "evidence_quote")
    for r in rows:
        rid = r.get("id", "?")
        for k in REQUIRED:
            v = (r.get(k) or "").strip()
            if not v:
                flags[rid].append(f"missing {k}")
    return flags


def placeholder_citation_check(rows: list[dict]) -> dict[str, list[str]]:
    flags: dict[str, list[str]] = defaultdict(list)
    PLACEHOLDERS = (
        r"\bauthor\s+et\s+al", r"\bxxx\b",
        r"\bplaceholder\b", r"\bunknown\s+source\b",
        r"\bdoi:?\s*$",  # source_url ending in "doi:" with nothing else
    )
    rx = re.compile("|".join(PLACEHOLDERS), re.IGNORECASE)
    for r in rows:
        rid = r.get("id", "?")
        src = (r.get("source") or "") + " " + (r.get("source_url") or "")
        if rx.search(src):
            flags[rid].append(f"placeholder citation: {src[:80]!r}")
    return flags


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path")
    ap.add_argument("--paper-root",
                    help="Directory containing one subdir per paper. "
                         "Required for verify_doi and verify_evidence_quote.")
    ap.add_argument("--out", default="flags.csv",
                    help="Output CSV of flagged rows (default flags.csv).")
    args = ap.parse_args()

    if not os.path.isfile(args.csv_path):
        print(f"error: {args.csv_path} not found", file=sys.stderr)
        sys.exit(2)

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} rows from {args.csv_path}")

    aggregated: dict[str, list[str]] = defaultdict(list)
    any_subscript_failed = False

    # 1. Required fields
    rf_flags = required_fields_check(rows)
    for rid, msgs in rf_flags.items():
        aggregated[rid].extend(msgs)
        for msg in msgs:
            print(f"row {rid}: {msg}")
    print(f"  required-field check: {len(rf_flags)} flagged")

    # 1b. csv_quote_lint — verify the CSV is well-quoted per RFC 4180
    rc, _ = _run(["python3", os.path.join(HERE, "csv_quote_lint.py"),
                   args.csv_path])
    print(f"  csv_quote_lint.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 1c. quote_template_lint — flag constructed/templated evidence_quote
    rc, _ = _run(["python3", os.path.join(HERE, "quote_template_lint.py"),
                   args.csv_path])
    print(f"  quote_template_lint.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 1d. quote_support_lint — verify evidence_quote actually carries the
    # numeric value and the compound name (or its label)
    rc, _ = _run(["python3", os.path.join(HERE, "quote_support_lint.py"),
                   args.csv_path])
    print(f"  quote_support_lint.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 2. validate_compound_name
    rc, _ = _run(["python3", os.path.join(HERE, "validate_compound_name.py"),
                   args.csv_path])
    print(f"  validate_compound_name.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 3. value_range_check
    rc, _ = _run(["python3", os.path.join(HERE, "value_range_check.py"),
                   args.csv_path])
    print(f"  value_range_check.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 4. unit_conversion_arithmetic
    rc, _ = _run(["python3", os.path.join(HERE, "unit_conversion_arithmetic.py"),
                   args.csv_path])
    print(f"  unit_conversion_arithmetic.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 5/6. verify_doi + verify_evidence_quote (need paper-root)
    if args.paper_root:
        rc, _ = _run(["python3", os.path.join(HERE, "verify_doi.py"),
                       args.csv_path, "--paper-root", args.paper_root])
        print(f"  verify_doi.py: exit={rc}")
        any_subscript_failed |= (rc != 0)
        rc, _ = _run(["python3", os.path.join(HERE,
                       "verify_evidence_quote.py"),
                       args.csv_path, "--paper-root", args.paper_root])
        print(f"  verify_evidence_quote.py: exit={rc}")
        any_subscript_failed |= (rc != 0)
    else:
        print("  verify_doi.py: SKIPPED (no --paper-root)")
        print("  verify_evidence_quote.py: SKIPPED (no --paper-root)")

    # 7. dedup_within_paper
    rc, _ = _run(["python3", os.path.join(HERE, "dedup_within_paper.py"),
                   args.csv_path])
    print(f"  dedup_within_paper.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 8. placeholder citations
    pc_flags = placeholder_citation_check(rows)
    for rid, msgs in pc_flags.items():
        aggregated[rid].extend(msgs)
        for msg in msgs:
            print(f"row {rid}: {msg}")
    print(f"  placeholder-citation check: {len(pc_flags)} flagged")

    # Emit flags.csv with the required-field + placeholder findings
    # (the script-level findings printed to stdout above)
    if aggregated and args.out:
        if rows:
            cols = list(rows[0].keys()) + ["_flag_reasons"]
            id_to_row = {r.get("id", "?"): r for r in rows}
            with open(args.out, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cols,
                                   quoting=csv.QUOTE_ALL,
                                   extrasaction="ignore")
                w.writeheader()
                for rid, msgs in sorted(aggregated.items()):
                    r = dict(id_to_row.get(rid, {"id": rid}))
                    r["_flag_reasons"] = "; ".join(msgs)
                    w.writerow(r)
            print(f"\nWrote {len(aggregated)} flagged rows to {args.out}")

    # Phase 4 readiness warning — flag if most rows are still pending_verification.
    # Without Phase 4 (independent agent re-audit), the run has unmeasured
    # audit quality. The Phase 3 scripts only catch deterministic issues;
    # semantic errors (compound mis-binding, NMR shift as mp, etc.) require
    # an independent agent reading the source.
    n_total = len(rows)
    n_pending = sum(1 for r in rows
                    if (r.get("verification_status") or "").strip()
                    == "pending_verification")
    if n_total and n_pending / n_total > 0.9:
        print()
        print("⚠️  WARNING: Phase 4 independent verification has not been run.")
        print(f"    {n_pending}/{n_total} rows are still 'pending_verification'.")
        print("    Phase 3 deterministic checks alone do NOT measure audit quality.")
        print("    Per SKILL.md, Phase 4 (fresh-context agent re-audit) is MANDATORY")
        print("    before declaring the output ready. Reports should not claim")
        print("    audit pass rates without Phase 4 evidence.")
        print()

    if aggregated or any_subscript_failed:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

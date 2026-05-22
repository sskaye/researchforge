#!/usr/bin/env python3
"""
run_all_checks.py — run every Phase-3 sanity check on a CSV and emit a
flags report.

Bundles:
  Generic (run for every data type):
    - Required-field check
    - csv_quote_lint.py
    - quote_support_lint.py (advisory)
    - validate_compound_name.py (name shape + SMILES if present)
    - conversion_arithmetic_lint.py (syntax shape of conversion_arithmetic)
    - verify_doi.py (only if --paper-root provided)
    - verify_evidence_quote.py (only if --paper-root provided)
    - dedup_within_paper.py
    - Placeholder-citation detection

  Data-type-specific (auto-discovered):
    - Every Python script in datatypes/<datatype>/scripts/ is invoked
      with <csv_path> as its first arg. Example for mp_bp:
        - datatypes/mp_bp/scripts/value_range_check.py
        - datatypes/mp_bp/scripts/unit_conversion_arithmetic.py

Usage:
    python3 run_all_checks.py --datatype <name> <input_csv> \\
        [--paper-root <dir>] [--out flags.csv]

The --datatype flag is REQUIRED. The skill is data-type-agnostic at its
core but every run must specify which overlay's value-range / unit-
conversion / property-enum checks to apply. If the named overlay folder
doesn't exist, the script halts with the list of installed data types.
"""
import sys
import csv
import os
import re
import glob
import argparse
import subprocess
from collections import defaultdict


HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)


def _available_datatypes() -> list[str]:
    """Return sorted list of overlay names with a datatypes/<X>/ folder."""
    base = os.path.join(SKILL_ROOT, "datatypes")
    if not os.path.isdir(base):
        return []
    return sorted(
        d for d in os.listdir(base)
        if os.path.isdir(os.path.join(base, d)) and not d.startswith("_")
    )


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
    REQUIRED = ("compound_name", "property", "value", "value_raw", "units",
                "meas_calc", "source", "source_url", "evidence_location",
                "evidence_quote")
    for r in rows:
        rid = r.get("id", "?")
        for k in REQUIRED:
            v = (r.get(k) or "").strip()
            if not v:
                # `units` is allowed to be empty for categorical-valued
                # properties (see SKILL.md empty-when-not-applicable). For
                # mp_bp it is always populated, so the check still fires
                # for mp_bp rows missing it.
                if k == "units":
                    # Only flag if value is numeric (i.e., not categorical)
                    val = (r.get("value") or "").strip()
                    try:
                        float(val)
                    except ValueError:
                        continue  # categorical, units may be empty
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
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[1],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("csv_path")
    ap.add_argument("--datatype", required=False,
                    help="REQUIRED. Name of the data-type overlay under "
                         "datatypes/ (e.g., mp_bp, redox).")
    ap.add_argument("--paper-root",
                    help="Directory containing one subdir per paper. "
                         "Required for verify_doi and verify_evidence_quote.")
    ap.add_argument("--out", default="flags.csv",
                    help="Output CSV of flagged rows (default flags.csv).")
    args = ap.parse_args()

    # Halt if --datatype is missing. Per the v2.0 skill rule, every run
    # must specify which overlay to apply — there is no implicit "generic
    # only" mode.
    available = _available_datatypes()
    if not args.datatype:
        print("error: --datatype is required.", file=sys.stderr)
        if available:
            print(f"available data types: {', '.join(available)}",
                  file=sys.stderr)
        else:
            print("no data types installed under datatypes/", file=sys.stderr)
        sys.exit(2)
    if args.datatype not in available:
        print(f"error: unknown data type {args.datatype!r}.", file=sys.stderr)
        if available:
            print(f"available data types: {', '.join(available)}",
                  file=sys.stderr)
        sys.exit(2)

    if not os.path.isfile(args.csv_path):
        print(f"error: {args.csv_path} not found", file=sys.stderr)
        sys.exit(2)

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} rows from {args.csv_path}")
    print(f"data type: {args.datatype}")

    aggregated: dict[str, list[str]] = defaultdict(list)
    any_subscript_failed = False

    # 1. Required fields
    rf_flags = required_fields_check(rows)
    for rid, msgs in rf_flags.items():
        aggregated[rid].extend(msgs)
        for msg in msgs:
            print(f"row {rid}: {msg}")
    print(f"  required-field check: {len(rf_flags)} flagged")

    # 1b. csv_quote_lint — verify the CSV is well-quoted per RFC 4180.
    rc, _ = _run(["python3", os.path.join(HERE, "csv_quote_lint.py"),
                   args.csv_path])
    print(f"  csv_quote_lint.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 1c. quote_support_lint — verify evidence_quote actually carries the
    # numeric value (advisory; warning, not auto-fail).
    rc, _ = _run(["python3", os.path.join(HERE, "quote_support_lint.py"),
                   args.csv_path])
    print(f"  quote_support_lint.py: exit={rc}  (advisory)")
    # Advisory only — do NOT propagate failure to overall exit code.
    # Quote-fidelity issues are Tier-2 verifiability flags, not Tier-1
    # correctness failures (see audit_criteria.md).

    # 2. validate_compound_name (generic)
    rc, _ = _run(["python3", os.path.join(HERE, "validate_compound_name.py"),
                   args.csv_path])
    print(f"  validate_compound_name.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 2b. conversion_arithmetic_lint — verify syntax shape of the
    # conversion_arithmetic column (v2.0 standardized syntax).
    cal_path = os.path.join(HERE, "conversion_arithmetic_lint.py")
    if os.path.isfile(cal_path):
        rc, _ = _run(["python3", cal_path, args.csv_path])
        print(f"  conversion_arithmetic_lint.py: exit={rc}")
        any_subscript_failed |= (rc != 0)

    # 3. verify_doi + verify_evidence_quote (need paper-root)
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

    # 4. dedup_within_paper
    rc, _ = _run(["python3", os.path.join(HERE, "dedup_within_paper.py"),
                   args.csv_path])
    print(f"  dedup_within_paper.py: exit={rc}")
    any_subscript_failed |= (rc != 0)

    # 5. placeholder citations (inline)
    pc_flags = placeholder_citation_check(rows)
    for rid, msgs in pc_flags.items():
        aggregated[rid].extend(msgs)
        for msg in msgs:
            print(f"row {rid}: {msg}")
    print(f"  placeholder-citation check: {len(pc_flags)} flagged")

    # 6. Data-type-specific scripts (auto-discovered).
    overlay_scripts = sorted(glob.glob(os.path.join(
        SKILL_ROOT, "datatypes", args.datatype, "scripts", "*.py")))
    print(f"  datatypes/{args.datatype}/scripts/: "
          f"{len(overlay_scripts)} script(s)")
    for sp in overlay_scripts:
        rc, _ = _run(["python3", sp, args.csv_path])
        print(f"    {os.path.basename(sp)}: exit={rc}")
        any_subscript_failed |= (rc != 0)

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

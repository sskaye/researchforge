#!/usr/bin/env python3
"""
run_all_checks.py — run every Phase-3 sanity check on a CSV and produce a flags report.

Bundles:
  - SMILES validity (validate_smiles.py)
  - Voltage-range plausibility by class (voltage_range_check.py)
  - Conversion arithmetic verification (conversion_arithmetic.py)
  - Cross-source consistency (cross_source_consistency.py)
  - Required-field check (molecule, voltage_v_she, source non-empty; voltage_v_she parseable)
  - Reference-electrode + electrolyte consistency

Usage:
    python run_all_checks.py <input_csv> [--out flags.csv]

Output:
    Per-check summary on stdout.
    flags.csv listing every flagged row with the failed check(s).
    Exit code 0 if zero flags, 1 if any flags.
"""
import sys
import csv
import re
import argparse
import subprocess
import os
from collections import defaultdict


HERE = os.path.dirname(os.path.abspath(__file__))


def _row_id(r, id_col):
    """Get id from primary id_col, fall back to '#' for legacy CSVs."""
    return r.get(id_col) or r.get("#") or "?"


def required_fields_check(rows, id_col="id"):
    flags = defaultdict(list)
    for r in rows:
        rid = _row_id(r, id_col)
        if not (r.get("molecule") or "").strip():
            flags[rid].append("missing molecule")
        v = (r.get("voltage_v_she") or "").strip()
        if not v:
            flags[rid].append("missing voltage_v_she")
        else:
            try:
                float(v)
            except ValueError:
                flags[rid].append(f"voltage_v_she not numeric ({v!r})")
        if not (r.get("source") or "").strip():
            flags[rid].append("missing source")
    return flags


def reference_consistency_check(rows, id_col="id"):
    """Hg/HgO requires alkaline; Hg/Hg2SO4 requires sulfate; Fc/Fc+ rare in water."""
    flags = defaultdict(list)
    for r in rows:
        rid = _row_id(r, id_col)
        ref = (r.get("reference_electrode") or "").lower()
        solv = (r.get("solvent") or "").lower()
        ph_str = (r.get("ph") or "").strip()
        try:
            ph = float(ph_str)
        except (ValueError, TypeError):
            ph = None

        is_alkaline = ("koh" in solv or "naoh" in solv or "alkaline" in solv or
                       "lioh" in solv or "csoh" in solv or (ph is not None and ph >= 9))
        if "hg/hgo" in ref or "hg-hgo" in ref:
            if not is_alkaline:
                flags[rid].append("Hg/HgO requires alkaline electrolyte; this row's solvent is not alkaline")
        if "hg/hg2so4" in ref or "hg2so4" in ref:
            if "so4" not in solv and "sulfate" not in solv:
                flags[rid].append("Hg/Hg2SO4 requires sulfate electrolyte")
        if ("fc/fc" in ref or "ferrocene/ferrocenium" in ref):
            if "water" in solv or "aqueous" in solv:
                flags[rid].append("Fc/Fc+ used in aqueous (rare; verify)")
    return flags


def placeholder_citation_check(rows, id_col="id"):
    flags = defaultdict(list)
    for r in rows:
        rid = _row_id(r, id_col)
        s = (r.get("source") or "").lower()
        if "author et al" in s:
            flags[rid].append("source contains 'Author et al.' placeholder")
        if "(related" in s and "cited in" in s:
            flags[rid].append("source contains '(related ... cited in ...)' placeholder")
    return flags


def truncated_name_check(rows, id_col="id"):
    flags = defaultdict(list)
    suspect_endings = ("hydroxy", "amino", "methyl", "methoxy", "sulfo", "phospho",
                       "iodo", "chloro", "bromo", "fluoro", "ethoxy", "carboxy", "nitro")
    parent_scaffolds = ("anthraquinone", "naphthoquinone", "benzoquinone", "phenazine",
                        "phthalimide", "alloxazine", "indigo", "tempo", "ferrocene",
                        "viologen", "quinone", "phenothiazine")
    for r in rows:
        rid = _row_id(r, id_col)
        mol = (r.get("molecule") or "").strip().lower()
        if not mol:
            continue
        if mol.endswith(suspect_endings) and not any(p in mol for p in parent_scaffolds):
            flags[rid].append(f"molecule name appears truncated (ends with substituent prefix; missing parent scaffold)")
    return flags


def doi_title_check(rows, id_col="id"):
    """Network check: resolve each unique DOI via CrossRef, flag those whose title
    contains no chemistry/molecule keywords. Slow — only run when --check-dois is set.

    Skips rows whose source_url indicates a textbook (e.g. starts with 'textbook:')
    or has no DOI at all. CrossRef-down errors are treated as 'unable to verify'
    rather than 'DOI bad' (see crossref_lookup.crossref())."""
    import re as _re
    sys.path.insert(0, HERE)
    from crossref_lookup import crossref, title_keyword_check

    chem_kws = ["redox", "voltammetry", "voltammetric", "electrochemistry", "electrochemical",
                "flow battery", "flow batteries", "potential", "reduction", "oxidation",
                "anolyte", "catholyte", "negolyte", "posolyte", "quinone", "viologen",
                "phenazine", "alloxazine", "ferrocene", "ferrocyanide", "tempo",
                "phthalimide", "halide", "halogen", "metal complex", "polyoxometalate",
                "POM", "indigo", "phenothiazine", "iron", "chromium", "vanadium",
                "battery", "electrolyte", "cyclic", "couple"]

    flags = defaultdict(list)
    seen = {}
    for r in rows:
        rid = _row_id(r, id_col)
        url = r.get("source_url") or ""
        src = r.get("source") or ""
        # Skip textbook entries — they have no DOI by design
        if url.lower().startswith("textbook:") or "handbook" in src.lower() or "textbook" in src.lower():
            continue
        m = _re.search(r"10\.\d{4,9}/[\w\.\-/;()<>:]+", url) or _re.search(r"10\.\d{4,9}/[\w\.\-/;()<>:]+", src)
        if not m:
            continue
        doi = m.group(0).rstrip(".,;)")
        if doi in seen:
            verdict = seen[doi]
        else:
            md = crossref(doi)
            if md is None:
                verdict = ("unresolvable", None)
            elif md.get("title") and title_keyword_check(md["title"], chem_kws):
                verdict = ("ok", md.get("title"))
            else:
                verdict = ("off-topic", md.get("title"))
            seen[doi] = verdict
        kind, title = verdict
        if kind == "unresolvable":
            flags[rid].append(f"DOI {doi} unresolvable on CrossRef")
        elif kind == "off-topic":
            flags[rid].append(f"DOI {doi} resolves to a paper unrelated to redox chemistry: '{(title or '')[:80]}'")
    return flags


def main():
    ap = argparse.ArgumentParser(description="Run all sanity checks on a redox CSV.")
    ap.add_argument("input_csv")
    ap.add_argument("--out", default="flags.csv", help="Output flags CSV path")
    ap.add_argument("--id-col", default="id", help="Name of the row-identifier column")
    ap.add_argument("--skip-smiles", action="store_true")
    ap.add_argument("--skip-range", action="store_true")
    ap.add_argument("--skip-arithmetic", action="store_true")
    ap.add_argument("--skip-cross", action="store_true")
    ap.add_argument("--check-dois", action="store_true",
                    help="Also resolve every DOI via CrossRef and check the title is "
                         "redox-related (slow — makes one HTTP call per unique DOI).")
    ap.add_argument("--include-computational", action="store_true",
                    help="Apply voltage_range_check to computational rows too.")
    args = ap.parse_args()

    # Load rows once for the in-process checks
    with open(args.input_csv, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Loaded {len(rows)} rows from {args.input_csv}", file=sys.stderr)

    all_flags = defaultdict(list)

    # In-process checks (fast)
    print("\n## Required fields", file=sys.stderr)
    for k, vs in required_fields_check(rows, args.id_col).items():
        all_flags[k].extend(vs)

    print("## Reference-electrode consistency", file=sys.stderr)
    for k, vs in reference_consistency_check(rows, args.id_col).items():
        all_flags[k].extend(vs)

    print("## Placeholder citations", file=sys.stderr)
    for k, vs in placeholder_citation_check(rows, args.id_col).items():
        all_flags[k].extend(vs)

    print("## Truncated names", file=sys.stderr)
    for k, vs in truncated_name_check(rows, args.id_col).items():
        all_flags[k].extend(vs)

    if args.check_dois:
        print("## DOI title relevance (CrossRef lookups, slow)", file=sys.stderr)
        for k, vs in doi_title_check(rows, args.id_col).items():
            all_flags[k].extend(vs)

    # External script checks
    def run_script(script, label, skip, extra_args=()):
        if skip:
            return
        path = os.path.join(HERE, script)
        cmd = [sys.executable, path, args.input_csv, "--id-col", args.id_col]
        cmd.extend(extra_args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        # External scripts print row hits to stdout; parse them
        for line in result.stdout.splitlines():
            m = re.match(r"#(\S+)\s+(.*)", line.strip())
            if m:
                row_id = m.group(1).rstrip(":")
                msg = m.group(2)
                all_flags[row_id].append(f"{label}: {msg[:120]}")
        # Print summary line from stderr
        for line in result.stderr.splitlines():
            if line.startswith("#"):
                print(f"## {label}: {line.lstrip('# ')}", file=sys.stderr)

    range_args = ["--include-computational"] if args.include_computational else []
    run_script("validate_smiles.py",          "smiles_invalid",  args.skip_smiles)
    run_script("voltage_range_check.py",      "voltage_oor",     args.skip_range, range_args)
    run_script("conversion_arithmetic.py",    "arithmetic_err",  args.skip_arithmetic)
    run_script("cross_source_consistency.py", "cross_source",    args.skip_cross)

    # Write flags CSV
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([args.id_col, "n_flags", "flag_messages"])
        for rid, msgs in sorted(all_flags.items(), key=lambda x: x[0]):
            w.writerow([rid, len(msgs), " | ".join(msgs)])

    print(f"\n# Total rows flagged: {len(all_flags)}", file=sys.stderr)
    print(f"# Flags report: {args.out}", file=sys.stderr)
    sys.exit(0 if not all_flags else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
verify_row.py — independently verify a single evidence-locked row.

Given a CSV with the standard provenance columns, this script:
  1. Resolves the DOI via CrossRef and prints the actual paper metadata
  2. Tries to find an open-access source for the paper
  3. Re-runs the conversion arithmetic and compares to voltage_v_she
  4. Reports a verdict for the row

This script does *not* fetch the source PDF and grep for the evidence quote — that step
requires a verifying agent with web access. This script does the parts that can be done
purely programmatically: metadata resolution, arithmetic, format checks.

Usage:
    python verify_row.py <input_csv> <row_id>
    python verify_row.py redox_mediators.csv 4119

Exit code 0 if all programmatic checks pass, 1 if any fail.
"""
import sys
import csv
import re
import json
import argparse
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from crossref_lookup import crossref, title_keyword_check
from conversion_arithmetic import verify as verify_arith
from validate_smiles import extract_smiles, validate as validate_smi
from find_open_access import find_open_access


def extract_doi(source_url, source):
    """Pull DOI from URL or source string."""
    for text in (source_url, source):
        if not text:
            continue
        m = re.search(r"10\.\d{4,9}/[\w\.\-/;()<>:]+", text)
        if m:
            return m.group(0).rstrip(".,;)")
    return None


def keyword_terms(row):
    """Build a list of keywords to verify in the paper title."""
    kws = []
    mol = (row.get("molecule") or "").strip()
    notes = (row.get("notes") or "").strip()
    if mol:
        # Use the first significant token from the molecule name
        bits = re.findall(r"[A-Za-z][A-Za-z0-9-]+", mol)
        for b in bits[:3]:
            if len(b) >= 4:
                kws.append(b)
    # Always include a chemistry keyword
    chemistry_kws = ["redox", "voltammetry", "electrochemistry", "flow battery",
                     "potential", "reduction", "oxidation", "anolyte", "catholyte",
                     "quinone", "viologen", "phenazine", "ferrocene", "TEMPO"]
    return kws, chemistry_kws


def main():
    ap = argparse.ArgumentParser(description="Verify a single row's programmatic provenance.")
    ap.add_argument("input_csv")
    ap.add_argument("row_id", help="Value of the id (or #) column to verify")
    ap.add_argument("--id-col", default="id", help="Name of the row-identifier column (default 'id'; falls back to '#').")
    ap.add_argument("--unpaywall-email", default="", help="Email for Unpaywall API (improves OA discovery)")
    args = ap.parse_args()

    row = None
    with open(args.input_csv, newline="") as f:
        for r in csv.DictReader(f):
            # Try id-col first, then fall back to '#' for legacy CSVs
            if r.get(args.id_col, "") == args.row_id or r.get("#", "") == args.row_id:
                row = r
                break

    if row is None:
        print(f"Row {args.row_id} not found in {args.input_csv}", file=sys.stderr)
        sys.exit(2)

    print(f"=== Row {args.row_id} ===")
    print(f"  molecule: {row.get('molecule', '')[:80]}")
    print(f"  voltage_v_she: {row.get('voltage_v_she')}")
    print(f"  voltage_raw: {row.get('voltage_raw', '')[:80]}")
    print(f"  reference_electrode: {row.get('reference_electrode')}")
    print(f"  solvent: {row.get('solvent')}, pH={row.get('ph')}")
    print(f"  source: {row.get('source', '')[:100]}")
    print(f"  source_url: {row.get('source_url', '')[:100]}")
    print(f"  evidence_location: {row.get('evidence_location', '')[:80]}")
    print(f"  evidence_quote: {(row.get('evidence_quote') or '')[:120]}")
    print(f"  conversion_arithmetic: {row.get('conversion_arithmetic', '')[:100]}")

    fails = []
    is_textbook = (row.get("source_url", "").lower().startswith("textbook:") or
                   "handbook" in row.get("source", "").lower() or
                   "textbook" in row.get("source", "").lower())

    # 1. DOI resolution + title keyword check (skipped for textbook entries)
    doi = extract_doi(row.get("source_url", ""), row.get("source", ""))
    if is_textbook:
        print(f"\n  Textbook entry: skipping DOI/CrossRef checks (no DOI required for textbook references)")
    elif not doi:
        fails.append("no DOI parseable from source_url or source")
    else:
        md = crossref(doi)
        if md is None:
            fails.append(f"DOI {doi} unresolvable on CrossRef")
        else:
            print(f"\n  CrossRef title: {md.get('title', '')[:120]}")
            print(f"  Journal/Year:   {md.get('journal')} ({md.get('year')})")
            print(f"  Vol/Page:       {md.get('volume')}, {md.get('page')}")
            mol_kws, chem_kws = keyword_terms(row)
            ok_chem = title_keyword_check(md.get("title", ""), chem_kws)
            ok_mol = mol_kws and title_keyword_check(md.get("title", ""), mol_kws)
            if not ok_chem and not ok_mol:
                fails.append(f"DOI title contains no chemistry/molecule keywords: '{md.get('title','')[:60]}'")

    # 2. Conversion arithmetic
    arith = (row.get("conversion_arithmetic") or "").strip()
    if arith:
        ok, msg = verify_arith(arith, row.get("voltage_v_she"))
        print(f"\n  Arithmetic: {msg}")
        if ok is False:
            fails.append(f"conversion arithmetic: {msg}")
    else:
        # Conversion may be a no-op (already vs SHE); that's OK as long as reference matches
        ref = (row.get("reference_electrode") or "").lower()
        if ref and "she" not in ref and "nhe" not in ref:
            fails.append(f"reference_electrode '{ref}' is not SHE but no conversion_arithmetic provided")

    # 3. SMILES validity (if any)
    smi = extract_smiles(row, "molecule", "notes")
    if smi:
        valid, msg = validate_smi(smi)
        print(f"\n  SMILES: {msg}")
        if valid is False:
            fails.append(f"invalid SMILES: {msg}")

    # 4. Open-access discovery (skipped for textbook entries)
    if doi and not is_textbook:
        cands = find_open_access(doi, email=args.unpaywall_email)
        url_cands = [c for c in cands if c.get("url")]
        if url_cands:
            print(f"\n  Open-access candidates ({len(url_cands)}):")
            for c in url_cands[:3]:
                print(f"    [{c['source']}] {c['url']}")
        else:
            print(f"\n  Open-access candidates: none found")

    # Verdict
    print(f"\n=== Verdict ===")
    if not fails:
        print("PASS — all programmatic checks succeeded.")
        print("Note: this does not verify the evidence_quote is actually present in the source.")
        print("That check requires fetching the source and string-searching for the quote.")
        sys.exit(0)
    else:
        print(f"FAIL — {len(fails)} programmatic check(s) failed:")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()

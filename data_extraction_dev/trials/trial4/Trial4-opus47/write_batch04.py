#!/usr/bin/env python3
"""Writer helper - takes pre-extracted rows (read by the LLM) and writes them as CSV with QUOTE_ALL.
This is NOT a regex extractor; the agent reads each paper and supplies rows as Python literals."""
import csv
import sys

HEADER = [
    "id","verification_status","compound_name","compound_smiles","property",
    "value_celsius","value_celsius_min","value_celsius_max","value_raw",
    "relation","data_type","source","source_url","evidence_location",
    "evidence_quote","conversion_arithmetic","notes"
]

def write_rows(rows, out_path):
    """rows: list of dicts with HEADER keys"""
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for i, r in enumerate(rows, start=1):
            row = {k: "" for k in HEADER}
            row.update(r)
            row["id"] = str(i)
            w.writerow(row)

if __name__ == "__main__":
    print("import this module and call write_rows(rows, out_path)")

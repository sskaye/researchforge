#!/usr/bin/env python3
"""
csv_quote_lint.py — verify that a CSV is well-quoted per RFC 4180.

Detects rows where a field containing a comma, double quote, or newline
was emitted without proper quoting, which causes columns to shift when
Python's `csv.DictReader` parses the file.

How it detects shifts:
  - Parse the file with `csv.reader`.
  - Every row should have the same number of columns as the header.
  - If a row has more columns than the header, an unquoted comma in some
    field caused a column-split.

Also catches the specific symptom that bit Trial-1-full: the `data_type`
column (which should be `measured` or `calculated`) carrying a value-raw
or relation string. This is a robustness check even when column counts
happen to line up by accident.

Usage:
    python3 csv_quote_lint.py <input_csv>

Output:
    row <id>: <reason>
Exit 0 if clean; 1 if any rows malformed.
"""
import sys
import csv
import argparse


_ALLOWED_DATA_TYPES = {"measured", "calculated", ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    args = ap.parse_args()

    flagged = 0
    with open(args.csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        print("csv is empty")
        sys.exit(1)
    header = rows[0]
    n_expected = len(header)
    print(f"# header has {n_expected} columns: {header}", file=sys.stderr)

    # Find the data_type column index
    try:
        dt_idx = header.index("data_type")
    except ValueError:
        dt_idx = None

    try:
        id_idx = header.index("id")
    except ValueError:
        id_idx = 0

    for li, row in enumerate(rows[1:], start=2):
        rid = row[id_idx] if id_idx < len(row) else f"line {li}"
        # Check column count
        if len(row) != n_expected:
            print(f"row {rid}: column count {len(row)} != expected {n_expected} "
                  f"(unquoted comma in some field?)")
            flagged += 1
            continue
        # Check data_type sanity (if header has it)
        if dt_idx is not None:
            dt = (row[dt_idx] or "").strip()
            if dt not in _ALLOWED_DATA_TYPES:
                print(f"row {rid}: data_type={dt!r} not in "
                      f"{sorted(_ALLOWED_DATA_TYPES)} — likely column shift "
                      "from unquoted comma in an earlier field")
                flagged += 1
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

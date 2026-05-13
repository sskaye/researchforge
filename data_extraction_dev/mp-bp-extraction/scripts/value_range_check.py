#!/usr/bin/env python3
"""
value_range_check.py — flag values outside plausible mp/bp ranges.

The ranges are intentionally generous, covering:
  - mp: helium (~ -272 °C at high pressure) up through the highest-melting
    refractory carbides / borides (~ 4200 °C; tantalum hafnium carbide is
    sometimes cited near 4215 °C, leaving headroom). We use [-275, 4500].
  - bp: helium (~ -269 °C) up through rhenium (~ 5596 °C), tungsten
    (~ 5555 °C). We use [-275, 6500].
  - DSC_onset / DSC_peak: same range as mp.
  - decomposition / sublimation: very wide; -275 to 6500 is safe.

A value outside this range is almost certainly a parsing artifact —
PDF sign-loss ("277.9" actually "−77.9"), wrong-unit not-yet-converted
(K stored as °C), or a non-property number captured by mistake.

Usage:
    python3 value_range_check.py <input_csv> [--out flags.csv]

Output:
    Lines like:
      row 42: value_celsius=4823.0 °C exceeds mp upper bound 4500
    Exit code 0 if all rows pass; 1 if any flagged.
"""
import sys
import csv
import argparse


# (property, low_C, high_C)
RANGES = {
    "melting_point":   (-275.0, 4500.0),
    "boiling_point":   (-275.0, 6500.0),
    "DSC_onset":       (-275.0, 4500.0),
    "DSC_peak":        (-275.0, 4500.0),
    "decomposition":   (-275.0, 6500.0),
    "sublimation":     (-275.0, 6500.0),
}


def check_row(row: dict) -> str | None:
    prop = (row.get("property") or "").strip()
    rng = RANGES.get(prop)
    if rng is None:
        return None  # unknown property; skip
    v = (row.get("value_celsius") or "").strip()
    if not v:
        return None
    try:
        val = float(v)
    except ValueError:
        return f"value_celsius={v!r} is not a number"
    lo, hi = rng
    if val < lo:
        return (f"value_celsius={val} °C below {prop} lower bound {lo} — "
                "check for PDF sign-loss artifact")
    if val > hi:
        return (f"value_celsius={val} °C exceeds {prop} upper bound {hi} — "
                "check for wrong-unit (K stored as °C) or wrong-cell extraction")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path")
    ap.add_argument("--out", help="Optional CSV path to write flagged rows.")
    args = ap.parse_args()

    flagged = []
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        msg = check_row(r)
        if msg:
            rid = r.get("id", "?")
            print(f"row {rid}: {msg}")
            flagged.append({**r, "_flag": msg})

    if args.out and flagged:
        cols = list(rows[0].keys()) + ["_flag"] if rows else ["_flag"]
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL,
                               extrasaction="ignore")
            w.writeheader()
            for r in flagged:
                w.writerow(r)
        print(f"\nWrote {len(flagged)} flagged rows to {args.out}")

    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

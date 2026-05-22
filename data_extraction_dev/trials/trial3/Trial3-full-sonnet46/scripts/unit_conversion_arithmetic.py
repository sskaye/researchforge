#!/usr/bin/env python3
"""
unit_conversion_arithmetic.py — verify the K/°F → °C conversion in each row.

Rules:
  - If `value_raw` is in K, expect `conversion_arithmetic` of the form
    `<X> K - 273.15 = <Y> °C` and confirm Y ≈ X − 273.15 (±0.5 °C tolerance).
  - If `value_raw` is in °F, expect `(<X> °F - 32) * 5/9 = <Y> °C` and
    confirm Y ≈ (X − 32) × 5/9.
  - If `value_raw` is already in °C, `conversion_arithmetic` must be empty.
  - In every case, the row's `value_celsius` field must match the computed
    Y to within tolerance.

Usage:
    python3 unit_conversion_arithmetic.py <input_csv>

Output:
    row <id>: <reason>
    Exit code 0 if clean; 1 if any flagged.
"""
import sys
import csv
import re
import argparse


TOLERANCE_C = 0.5  # °C allowed slack on rounding


def detect_unit(value_raw: str) -> str | None:
    """Return 'C', 'K', or 'F' based on what's in value_raw, or None if unclear."""
    if not value_raw:
        return None
    txt = value_raw.strip()
    if re.search(r"°\s*C\b|\bdeg\s*C\b", txt) or txt.endswith(" C"):
        return "C"
    if re.search(r"°\s*F\b", txt) or txt.endswith(" F"):
        return "F"
    if re.search(r"\bK\b", txt):
        return "K"
    # Fallback: bare number → assume °C
    if re.fullmatch(r"\s*-?\d+(?:\.\d+)?\s*(?:[-–]\s*-?\d+(?:\.\d+)?)?\s*", txt):
        return "C"
    return None


def parse_numbers(s: str) -> list[float]:
    """All numbers in s. Treats '-' between two digits as a range
    separator (not a sign): '188-190' → [188, 190]. Standalone '-X'
    (after whitespace or at start) remains a negative sign: '-77.9' → [-77.9].
    Handles unicode minus/en-dash/em-dash."""
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    # Replace digit-hyphen-digit with digit-space-digit so the hyphen
    # is not consumed as a sign on the right-hand number.
    s = re.sub(r"(\d)\s*-\s*(\d)", r"\1 \2", s)
    return [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", s)]


def check_row(row: dict) -> str | None:
    raw = (row.get("value_raw") or "").strip()
    arith = (row.get("conversion_arithmetic") or "").strip()
    canon = (row.get("value_celsius") or "").strip()
    unit = detect_unit(raw)
    if unit is None:
        return f"could not detect unit in value_raw={raw!r}"
    try:
        canon_val = float(canon) if canon else None
    except ValueError:
        return f"value_celsius={canon!r} is not a number"

    # Numbers in raw — first is the raw value (or low end of range)
    raw_nums = parse_numbers(raw)
    if not raw_nums:
        return f"no numeric value in value_raw={raw!r}"
    raw_lo = raw_nums[0]
    raw_hi = raw_nums[1] if len(raw_nums) >= 2 else raw_lo

    # Expected °C midpoint
    if unit == "C":
        if arith:
            return (f"conversion_arithmetic={arith!r} present but "
                    "value_raw is already in °C")
        expected = (raw_lo + raw_hi) / 2.0
    elif unit == "K":
        if not arith:
            return f"value_raw is in K but conversion_arithmetic is empty"
        # Validate the arithmetic statement: "X K - 273.15 = Y °C"
        m = re.search(r"(-?\d+(?:\.\d+)?)\s*K\s*[-−]\s*273\.15\s*=\s*"
                      r"(-?\d+(?:\.\d+)?)\s*°?\s*C", arith)
        if not m:
            return (f"conversion_arithmetic does not match "
                    "'<X> K - 273.15 = <Y> °C': {arith!r}")
        x, y = float(m.group(1)), float(m.group(2))
        if abs(y - (x - 273.15)) > TOLERANCE_C:
            return (f"arithmetic error: {x} K − 273.15 = "
                    f"{x - 273.15:.3f} °C, but stated {y}")
        expected = (raw_lo + raw_hi) / 2.0 - 273.15
    elif unit == "F":
        if not arith:
            return f"value_raw is in °F but conversion_arithmetic is empty"
        m = re.search(r"\(\s*(-?\d+(?:\.\d+)?)\s*°?\s*F\s*[-−]\s*32\s*\)\s*"
                      r"\*\s*5\s*/\s*9\s*=\s*(-?\d+(?:\.\d+)?)\s*°?\s*C", arith)
        if not m:
            return (f"conversion_arithmetic does not match "
                    "'(<X> °F - 32) * 5/9 = <Y> °C': {arith!r}")
        x, y = float(m.group(1)), float(m.group(2))
        if abs(y - (x - 32) * 5.0 / 9.0) > TOLERANCE_C:
            return (f"arithmetic error: ({x} − 32) × 5/9 = "
                    f"{(x - 32) * 5.0 / 9.0:.3f} °C, but stated {y}")
        expected = ((raw_lo + raw_hi) / 2.0 - 32) * 5.0 / 9.0
    else:
        return None

    if canon_val is None:
        return f"value_celsius is empty but value_raw is {raw!r}"
    if abs(canon_val - expected) > TOLERANCE_C:
        return (f"value_celsius={canon_val} disagrees with expected "
                f"{expected:.3f} (from {raw!r} as {unit})")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    args = ap.parse_args()
    flagged = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            msg = check_row(row)
            if msg:
                print(f"row {row.get('id','?')}: {msg}")
                flagged += 1
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

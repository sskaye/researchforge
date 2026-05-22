#!/usr/bin/env python3
"""
conversion_arithmetic_lint.py — verify the SHAPE of the conversion_arithmetic
column per the v2.0 standardized syntax.

The v2.0 standardized syntax (see SKILL.md) is:

    <input_value_with_units> <operator> <constant> = <output_value_with_units>

Examples:

  - mp/bp K → °C:           `300 K − 273.15 = 26.85 °C`
  - mp/bp °F → °C:          `(300 °F − 32) × 5/9 = 148.89 °C`
  - redox SCE → SHE:        `+0.40 V vs SCE + 0.241 = +0.641 V vs SHE`
  - (empty)                 row has no conversion applied

This lint only checks the shape — that the column is either empty or
matches the input-operator-constant-equals-output pattern with units
attached. Numeric correctness is checked by each overlay's own
conversion script (`datatypes/<X>/scripts/unit_conversion_arithmetic.py`
or similar) using the data-type's specific math.

Usage:
    python3 conversion_arithmetic_lint.py <input_csv>

Output:
    row <id>: <reason>
Exit code 0 if all rows have well-shaped or empty conversion_arithmetic;
1 if any row's conversion_arithmetic violates the syntax.
"""
import sys
import csv
import re
import argparse


# Generic v2.0 syntax matcher.
#
# - Input is `<number_with_optional_sign_and_decimal>[whitespace]<units>` or
#   the parenthesized form `(<number> <units> <op> <const>)` for two-step
#   conversions like °F → °C.
# - Operator is one of `−`, `-` (minus), `+` (plus), `×`, `*` (times),
#   `/` (divide).
# - Constant can include a units suffix and may itself include `/` (for
#   composite expressions like `× 5/9`).
# - Output is `<number_with_optional_sign_and_decimal>[whitespace]<units>`.
#
# We don't constrain the units strings beyond a non-comma, non-equals,
# non-newline regex — overlays use a wide variety (°C, K, V vs SHE, Pa·s,
# etc.).
_NUMBER = r"[+\-−]?\d+(?:\.\d+)?"
_UNITS = r"[^,=\n]+?"
_OP = r"[\-−+×*/]"
_INPUT_SIMPLE = rf"{_NUMBER}\s+{_UNITS}"
_INPUT_PARENS = rf"\(\s*{_NUMBER}\s+{_UNITS}\s+{_OP}\s+\S+?\s*\)"
_CONVERSION_SHAPE = re.compile(
    rf"^\s*"
    rf"(?:{_INPUT_PARENS}|{_INPUT_SIMPLE})"
    rf"\s+{_OP}\s+\S[^=]*?"
    rf"=\s*{_NUMBER}\s+{_UNITS}"
    rf"\s*$"
)


def check_row(row: dict) -> str | None:
    """Return error message if the row's conversion_arithmetic is malformed;
    None if it's empty or well-shaped."""
    arith = (row.get("conversion_arithmetic") or "").strip()
    if not arith:
        return None  # empty is fine (no conversion needed)
    if not _CONVERSION_SHAPE.match(arith):
        return (f"conversion_arithmetic does not match v2.0 syntax "
                f"`<input value+units> <op> <constant> = <output value+units>`: "
                f"{arith!r}")
    if "=" not in arith:
        return (f"conversion_arithmetic missing `=` separator: {arith!r}")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
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

#!/usr/bin/env python3
"""
v2.0 eval helper: unit tests for scripts/conversion_arithmetic_lint.py.

Verifies the lint accepts the three valid example shapes from SKILL.md
(K→°C, °F→°C, redox SCE→SHE) plus their ASCII-operator equivalents, and
rejects four malformed shapes (missing =, missing operator, missing
units, missing input number).

Used by the 'v20-conversion-arithmetic-lint-shapes' eval.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from conversion_arithmetic_lint import check_row  # noqa: E402


VALID = [
    "",                                                # empty — no conversion
    "300 K − 273.15 = 26.85 °C",                       # K → °C unicode minus
    "300 K - 273.15 = 26.85 °C",                       # K → °C ASCII minus
    "(300 °F − 32) × 5/9 = 148.89 °C",                 # °F → °C unicode
    "(300 °F - 32) * 5/9 = 148.89 °C",                 # °F → °C ASCII
    "+0.40 V vs SCE + 0.241 = +0.641 V vs SHE",        # redox SCE → SHE
]

INVALID = [
    "300 K - 273.15 26.85 °C",      # missing =
    "300 K 26.85 °C",                # missing operator + constant + =
    "300 - 273.15 = 26.85",          # missing units
    "K - 273.15 = 26.85 °C",         # missing input number
]


errs = 0
for s in VALID:
    msg = check_row({"id": "_", "conversion_arithmetic": s})
    if msg is not None:
        print(f"UNEXPECTED FAIL on valid {s!r}: {msg}")
        errs += 1

for s in INVALID:
    msg = check_row({"id": "_", "conversion_arithmetic": s})
    if msg is None:
        print(f"UNEXPECTED PASS on invalid {s!r}")
        errs += 1

if errs:
    print(f"UNEXPECTED FAILURES: {errs}")
    sys.exit(1)
print("UNEXPECTED FAILURES: NONE")
sys.exit(0)

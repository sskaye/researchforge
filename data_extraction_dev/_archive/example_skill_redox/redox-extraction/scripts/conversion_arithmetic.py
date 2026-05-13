#!/usr/bin/env python3
"""
conversion_arithmetic.py — verify that any reference-electrode conversion shown in a row
arithmetically agrees with voltage_v_she.

The skill requires rows to record the conversion from the source's native reference electrode
to vs SHE. Two formats are accepted:

1. Add-form (most references):
   "-0.47 V vs Ag/AgCl(3M KCl) + 0.210 = -0.26 V vs SHE"

2. Subtract-form (for absolute-scale / vacuum-referenced storage):
   "4.42 - 5.50 = -1.08 V vs SHE"   (E_SHE = constant - raw)

This script parses such strings and verifies:
  1. The arithmetic is correct.
  2. The offset/constant matches a known reference-electrode conversion (within tolerance).
  3. The result equals voltage_v_she.

Usage:
    python conversion_arithmetic.py <input_csv>

Exit code 0 if all rows pass, 1 if any fail.
"""
import sys
import csv
import re
import argparse


# Add-form: known offsets (V) added to native reference to get SHE.
# Source: see references/REFERENCE_ELECTRODES.md (kept in sync).
KNOWN_OFFSETS = {
    "she": 0.000, "nhe": 0.000,
    "sce": 0.241, "saturated calomel": 0.241,
    "sce 1 m kcl": 0.283, "sce normal": 0.283,
    "ag/agcl sat": 0.197, "ag/agcl saturated": 0.197,
    "ag/agcl 3 m kcl": 0.210,
    "ag/agcl 3 m nacl": 0.209,
    "ag/agcl 1 m kcl": 0.236,
    "ag/agcl 0.1 m kcl": 0.288,
    "hg/hgo 1 m naoh": 0.098,
    "hg/hgo 1 m koh": 0.098,
    "hg/hgo 0.1 m naoh": 0.165,
    "hg/hg2so4 sat. k2so4": 0.640, "hg/hg2so4": 0.640,
    "fc/fc+ in mecn": 0.400, "fc/fc+ mecn": 0.400, "ferrocene/ferrocenium mecn": 0.400,
    "fc/fc+ in dmf": 0.450, "fc/fc+ dmf": 0.450,
    "fc/fc+ in dmso": 0.450, "fc/fc+ dmso": 0.450,
    "fc/fc+ in thf": 0.560,
    "fc/fc+ in dcm": 0.460,
    "ag/ag+ mecn": 0.550,
    "rhe at ph 7": -0.4137, "rhe ph 7": -0.4137,
    "rhe at ph 14": -0.8274, "rhe ph 14": -0.8274,
}

# Subtract-form: known constants used in absolute-scale conversions.
# 4.42 V is the commonly used absolute SHE potential; some conventions use 4.44 V.
KNOWN_SUBTRACT_CONSTANTS = {
    4.42: "absolute-scale convention (E_SHE = 4.42 - raw)",
    4.44: "absolute SHE potential (alternate convention, 4.44 V)",
}


def parse_add_form(text):
    """Match 'X V vs Y +/- Z = W V vs SHE'. Returns (raw, ref, offset, result) or None."""
    m = re.search(
        r"(-?\d+\.?\d*)\s*V?\s*vs\s+([^+\-=]+?)\s*([+\-])\s*(\d+\.?\d*)\s*V?\s*=\s*(-?\d+\.?\d*)",
        text, re.IGNORECASE
    )
    if not m:
        return None
    raw = float(m.group(1))
    ref = m.group(2).strip().lower()
    sign = m.group(3)
    offset_abs = float(m.group(4))
    offset = offset_abs * (1 if sign == "+" else -1)
    result = float(m.group(5))
    return raw, ref, offset, result


def parse_subtract_form(text):
    """Match 'C - X = W V vs SHE' (absolute-scale form). Returns (constant, raw, result) or None."""
    m = re.search(
        r"(\d+\.?\d*)\s*[-−–]\s*(-?\d+\.?\d*)\s*=\s*(-?\d+\.?\d*)\s*V?\s*(?:vs\s+SHE)?",
        text, re.IGNORECASE
    )
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def normalize_ref(ref):
    """Lower-case and squash whitespace/punctuation for matching against KNOWN_OFFSETS keys."""
    n = re.sub(r"[(),]", " ", ref.lower())
    n = re.sub(r"\s+", " ", n).strip()
    return n


def offset_matches_known(offset, ref_text):
    """Return key of matching known reference, or None."""
    ref_n = normalize_ref(ref_text)
    for key, off in KNOWN_OFFSETS.items():
        # Match if all words of the key appear in ref_n
        key_words = key.split()
        if all(w in ref_n for w in key_words) and abs(off - offset) < 0.015:
            return key
    return None


def verify(arith_text, voltage_v_she):
    """Verify arithmetic. Returns (ok: bool|None, message: str)."""
    if not arith_text:
        return None, "no parseable arithmetic"
    text = arith_text.replace("−", "-").replace("–", "-").replace("—", "-")

    # Try add-form first (most common)
    parsed = parse_add_form(text)
    if parsed is not None:
        raw, ref, offset, result = parsed
        expected = round(raw + offset, 4)
        if abs(expected - result) > 0.005:
            return False, f"arithmetic error: {raw} + {offset} = {expected:.3f}, claimed {result}"
        try:
            v_she = float(voltage_v_she)
        except (ValueError, TypeError):
            return False, "voltage_v_she not numeric"
        if abs(result - v_she) > 0.005:
            return False, f"result {result} doesn't match voltage_v_she {v_she}"
        matched = offset_matches_known(offset, ref)
        if matched is None:
            return False, f"offset {offset:+.3f} doesn't match any known reference (ref text: '{ref[:40]}')"
        return True, f"verified add-form ({matched}, offset {offset:+.3f})"

    # Try subtract-form (absolute-scale)
    parsed = parse_subtract_form(text)
    if parsed is not None:
        constant, raw, result = parsed
        expected = round(constant - raw, 4)
        if abs(expected - result) > 0.005:
            return False, f"arithmetic error: {constant} - {raw} = {expected:.3f}, claimed {result}"
        try:
            v_she = float(voltage_v_she)
        except (ValueError, TypeError):
            return False, "voltage_v_she not numeric"
        if abs(result - v_she) > 0.005:
            return False, f"result {result} doesn't match voltage_v_she {v_she}"
        matched_const = None
        for c, name in KNOWN_SUBTRACT_CONSTANTS.items():
            if abs(c - constant) < 0.05:
                matched_const = name
                break
        if matched_const is None:
            return False, f"constant {constant:+.3f} doesn't match any known absolute-scale convention"
        return True, f"verified subtract-form ({matched_const})"

    return None, "no parseable arithmetic"


def main():
    ap = argparse.ArgumentParser(description="Verify conversion arithmetic in CSV rows.")
    ap.add_argument("input_csv")
    ap.add_argument("--arith-col", default="conversion_arithmetic")
    ap.add_argument("--voltage-col", default="voltage_v_she")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--max-output", type=int, default=50)
    args = ap.parse_args()

    fail = 0
    total = 0
    no_arith = 0
    with open(args.input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arith = (row.get(args.arith_col) or "").strip()
            if not arith:
                no_arith += 1
                continue
            total += 1
            ok, msg = verify(arith, row.get(args.voltage_col))
            if ok is False:
                fail += 1
                if fail <= args.max_output:
                    rid = row.get(args.id_col, row.get("#", "?"))
                    print(f"#{rid}  FAIL: {msg}")
                    print(f"   arithmetic: {arith[:80]}")
                    print(f"   v_she: {row.get(args.voltage_col)}")

    print(f"\n# Rows with arithmetic: {total}", file=sys.stderr)
    print(f"# Rows without arithmetic field (skipped): {no_arith}", file=sys.stderr)
    print(f"# Arithmetic violations: {fail}", file=sys.stderr)
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()

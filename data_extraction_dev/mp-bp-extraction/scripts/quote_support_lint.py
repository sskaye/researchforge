#!/usr/bin/env python3
"""
quote_support_lint.py — verify that each row's evidence_quote actually
contains the recorded value.

This catches a failure mode the v1.2 quote re-confirmation step left open:
the quote is present verbatim in the paper, but does NOT contain the
value. Examples observed in Trial-2:

  - Opus row 80: quote = "Dark red solid;" — verbatim in the paper, but
    the m.p. 168-170 °C is on the next physical line in column 2. The
    quote ended at the leading clause and never reached the value.
  - GPT-5.5 masthead rows: quote = the paper's journal masthead text —
    verbatim in the paper, contains no mp/bp value, supports no row.

The hard check is **value must be in quote**:

  - The numeric portion of `value_raw` must appear in `evidence_quote`.

This is the only structural rule that doesn't false-positive on
legitimate quotes. Most synthesis papers print compound names in a
**section heading** immediately above the m.p. line, so the agent's
quote often contains the value + characterization clause but not the
compound name itself — Phase 4 confirms the (section-header, value)
binding semantically.

A separate, advisory check (warn-only, exit 0 by itself) looks for the
compound name / serial code in the quote and surfaces rows where
neither is present. Those need a Phase 4 look but aren't an
automatic-fail because of the synthesis-paragraph pattern above.

Usage:
    python3 quote_support_lint.py <input_csv> [--strict-compound]

Output:
    row <id>: <reason>
Exit 0 if no value-containment failures (default).
Exit 0 if --strict-compound is set and only compound-token advisories fire.
Exit 1 if any value-containment failure (the hard check) is found.
"""
import sys
import csv
import re
import argparse
import unicodedata


# Whitespace-collapse + NFC normalization, matching the project's
# verbatim-quote convention.
def _norm(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Hyphen-fold: − – — → -
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    return s.lower()


_NUMBER_RE = re.compile(r"-?\d+(?:[.,]\d+)?")


def numeric_tokens(value_raw: str) -> list[str]:
    """Pull every numeric run out of `value_raw`, plus integer-only
    variants so '27.0' matches a paper that prints just '27'.

    "188-190 °C" → ["188", "190"]
    "492.478 K"  → ["492.478", "492"]
    "−77.9 °C"   → ["-77.9", "-77"]
    "27.0 °C"    → ["27.0", "27"]

    The check passes if ANY of these tokens is present in the normalized
    quote.
    """
    if not value_raw:
        return []
    s = _norm(value_raw)
    toks = []
    for m in re.finditer(r"-?\d+(?:[.,]\d+)?", s):
        tok = m.group(0)
        toks.append(tok)
        # Also yield integer part (handles "27.0" vs paper's "27")
        if "." in tok or "," in tok:
            int_part = re.split(r"[.,]", tok, 1)[0]
            if int_part and int_part not in toks:
                toks.append(int_part)
    return toks


def value_in_quote(value_raw: str, quote: str) -> bool:
    """True iff at least one numeric token from value_raw appears in quote."""
    qn = _norm(quote)
    toks = numeric_tokens(value_raw)
    if not toks:
        # Row's value_raw is non-numeric (shouldn't happen for mp/bp);
        # skip the check rather than false-flag.
        return True
    for t in toks:
        if t in qn:
            return True
    return False


# Tokens commonly used as series-codes / compound labels in synthesis
# papers. We try to extract one from compound_name as a fallback when the
# IUPAC name itself isn't substring-present in the quote.
_CODE_RE = re.compile(
    r"\b("
    r"(?:compound|complex|cpd|molecule|product|cmpd)\s+\d+[a-z]?'?"
    r"|"
    r"\d{1,3}[a-z]'?"        # bare codes like "4f", "11h", "2g'"
    r")\b",
    re.IGNORECASE,
)


def candidate_compound_tokens(compound_name: str) -> list[str]:
    """Return a list of substrings any one of which should appear in the quote.

    Strategy:
      1. The whole normalized name (in case the quote contains the full
         IUPAC name).
      2. The longest hyphen-delimited "informative" chunk (e.g.,
         "ethan-1-ol" from "(4-nitrophenyl)ethan-1-ol").
      3. Any parenthesized serial code (e.g., "(4f)", "(AL1)").
      4. Any bare serial-code-shaped token (e.g., "4f", "11h", "compound 5").
      5. Each space-separated word ≥4 chars after dropping stop tokens.

    The lint passes if ANY of these tokens appears in the normalized quote.
    """
    if not compound_name:
        return []
    name = _norm(compound_name)
    out: list[str] = []
    out.append(name)
    # Hyphen-delimited longest informative chunk
    parts = sorted(re.split(r"[\s,;()]+", name), key=len, reverse=True)
    for p in parts[:5]:
        if len(p) >= 5 and re.search(r"[a-z]{4,}", p):
            out.append(p)
    # Parenthesized serial codes
    for m in re.finditer(r"\(([^)]{1,8})\)", compound_name):
        out.append(_norm(m.group(1)))
    # Bare-code-shaped tokens
    for m in _CODE_RE.finditer(compound_name):
        out.append(_norm(m.group(1)))
    # Word tokens ≥4 chars
    for w in re.findall(r"[A-Za-z][A-Za-z\-]{3,}", compound_name):
        out.append(_norm(w))
    # De-dup while preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for t in out:
        if t and t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


_GENERIC_STOPWORDS = {
    "and", "the", "with", "for", "from", "compound", "complex", "product",
    "molecule", "synthesis", "yield", "solid", "powder", "crystal",
    "afford", "afforded", "stirred", "heated", "cooled",
}


def compound_in_quote(compound_name: str, quote: str) -> tuple[bool, str | None]:
    """True iff some recognizable compound token from compound_name appears
    in quote. Returns (passed, matched_token_or_None)."""
    if not compound_name:
        return False, None
    qn = _norm(quote)
    for tok in candidate_compound_tokens(compound_name):
        # Skip generic stopwords as the only match
        if tok in _GENERIC_STOPWORDS:
            continue
        if len(tok) < 3:
            continue
        if tok in qn:
            return True, tok
    return False, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path")
    ap.add_argument("--strict-compound", action="store_true",
                    help="Also fail when compound_name / serial code is "
                         "absent from evidence_quote (default: advisory "
                         "warning, exit 0).")
    args = ap.parse_args()

    hard_fail = 0
    advisory = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = row.get("id", "?")
            value_raw = row.get("value_raw", "")
            quote = row.get("evidence_quote", "")
            name = row.get("compound_name", "")

            if not quote.strip():
                # required-fields check will catch this
                continue

            # Hard check: value must be in quote.
            if not value_in_quote(value_raw, quote):
                toks = numeric_tokens(value_raw)
                print(f"row {rid}: evidence_quote does not contain any "
                      f"numeric token from value_raw={value_raw!r} "
                      f"(expected one of {toks}); quote begins with "
                      f"{quote[:60]!r}")
                hard_fail += 1
                continue

            # Advisory: compound name / serial code in quote. Synthesis
            # papers often print the compound name in the section header
            # above the m.p. line and the agent quotes only the value
            # clause — this is a legitimate pattern that Phase 4
            # confirms semantically. We log these rows as advisory so
            # the maintainer can spot-check, but don't auto-fail.
            ok, _matched = compound_in_quote(name, quote)
            if not ok:
                tag = "FAIL" if args.strict_compound else "advisory"
                print(f"row {rid}: [{tag}] evidence_quote does not "
                      f"contain a recognizable token from "
                      f"compound_name={name[:60]!r}; quote begins with "
                      f"{quote[:80]!r}")
                advisory += 1

    if hard_fail or (args.strict_compound and advisory):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

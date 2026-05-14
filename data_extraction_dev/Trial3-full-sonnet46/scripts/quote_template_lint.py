#!/usr/bin/env python3
"""
quote_template_lint.py — flag evidence_quote strings that look templated /
constructed rather than copied verbatim from a paper.

Motivated by Trial-2 Sonnet 4.6, where 770 rows from 20 large reference-
table PDFs had quotes built by a Python data-entry script:

    f"Table III: {nm} BP {bp} MP {mp}"
    f"Table 1: {nm} Melting point (deg C) {mp}"
    f"{nm} ... Expt. {mp}"

The underlying compound + value were typically correct, but the quote
strings are paraphrases — none of them appears verbatim in the source
files. ~22 of the 45 audit failures (~half) trace to these patterns.

The patterns flagged here are intentionally specific so the lint doesn't
fire on legitimate verbatim quotes that happen to start with "Table".
A real paper sentence like "Table 1 shows the m.p. of 188-190 °C for 2a"
will not match these patterns; a templated `"Table 1: 2a MP 188"` will.

Usage:
    python3 quote_template_lint.py <input_csv>

Output:
    row <id>: <reason>
Exit 0 if clean; 1 if any rows flagged.
"""
import sys
import csv
import re
import argparse


# A quote that is just "Table <N>:" or "Table <N>." followed by a single
# word and then numbers is overwhelmingly a constructed string. Real
# paper sentences with "Table N" embedded almost always have additional
# prose ("Table 1 shows...", "As reported in Table 1, ...", "see Table 1").
_TABLE_PREFIX_TEMPLATE = re.compile(
    r"^\s*Table\s+[IVX0-9]+\s*[:.,]\s*\S",
    re.IGNORECASE,
)

# Inline f-string templates that pair an MP and BP value with no separating
# paper prose. Real paper text saying "MP 188 BP 286" without sentence
# structure does not occur — papers use prose like "m.p. 188 °C; b.p. 286 °C"
# or tables with cells.
_INLINE_MP_BP = re.compile(
    r"\bMP\s+\d{1,4}(?:[.\-–]\d{1,4})?\b.{0,40}\bBP\s+\d{2,4}",
    re.IGNORECASE,
)

# Column-header strings used as field separators inside a quote are tells
# that the quote was assembled from table-cell content rather than copied
# as a contiguous span.
_COLUMN_HEADER_TOKENS = re.compile(
    r"\b(Melting point\s*\(deg\s*C\)|Boiling point\s*\(deg\s*C\)|"
    r"Mp\s*\(°C\)|Bp\s*\(°C\)|Tm\s*\(K\))\b",
    re.IGNORECASE,
)

# Literal ellipsis used to elide non-adjacent text. ASCII `...` and the
# Unicode ellipsis `…`. Three-dot ellipsis in a paper sentence (e.g.,
# "compound X is novel..., melts at 188 °C") is rare; the typical use
# we see in failures is `"compound ... value"` joining two table cells.
# We flag any literal `...` in the quote and let manual review confirm.
_ELLIPSIS = re.compile(r"(\.{3,}|…)")

# Trailing-ellipsis-plus-value pattern: "...  Expt.  158.3" or " ... 188"
# at end of quote — common in Sonnet 4.6's f-string output.
_TRAILING_ELLIPSIS_VALUE = re.compile(
    r"\.{3,}\s*(?:Expt\.|Exp\.)?\s*-?\d{2,4}(?:\.\d+)?\s*$",
    re.IGNORECASE,
)


def check_quote(quote: str) -> str | None:
    if not quote or not quote.strip():
        return None
    q = quote.strip()
    if _ELLIPSIS.search(q):
        # Literal ellipsis in the quote string is forbidden — a contiguous
        # substring of paper text would not need an authorial elision.
        return ("evidence_quote contains literal ellipsis ('...' or '…') — "
                "constructed quotes joining non-adjacent spans are "
                f"forbidden; quote begins {q[:80]!r}")
    if _TABLE_PREFIX_TEMPLATE.match(q):
        # The "Table N: X" leading pattern is almost always templated.
        # Real paper prose embeds Table references in sentences, not as
        # standalone leading clauses with a colon-separator.
        return ("evidence_quote starts with a 'Table N:' template prefix — "
                "looks templated rather than copied verbatim from paper "
                f"text; quote begins {q[:80]!r}")
    if _INLINE_MP_BP.search(q):
        return ("evidence_quote contains an inline 'MP X BP Y' pattern — "
                "looks like f-string template output rather than a paper "
                f"sentence; quote begins {q[:80]!r}")
    m = _COLUMN_HEADER_TOKENS.search(q)
    if m:
        return ("evidence_quote contains a column-header token "
                f"({m.group(0)!r}) used as a field separator — quote "
                "appears assembled from table cells rather than copied; "
                f"begins {q[:80]!r}")
    if _TRAILING_ELLIPSIS_VALUE.search(q):
        return ("evidence_quote ends with an ellipsis+value pattern — "
                f"looks templated; quote ends {q[-60:]!r}")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path")
    args = ap.parse_args()

    flagged = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = row.get("id", "?")
            msg = check_quote(row.get("evidence_quote", ""))
            if msg:
                print(f"row {rid}: {msg}")
                flagged += 1
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

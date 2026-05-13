"""Gate C — Evidence substring check.

Per § 7b of merged_skill_proposal.md.

`evidence_text` must be a verifiable substring of the article text
after Unicode NFC normalization, whitespace collapse, and
PDF-hyphen-line-break dehyphenation.

Only two evidence_type values reach this gate:
  - "verbatim_text" → must be a substring of the article's normalized text
  - "structured_coordinates" → must resolve to a real table coordinate
Any other type was rejected upstream (paraphrase_evidence_not_allowed).
"""

from __future__ import annotations

import re
import unicodedata


def normalize_for_substring_match(text: str) -> str:
    """NFC Unicode, dehyphenate PDF line breaks, collapse whitespace."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    # Dehyphenate line breaks: "hydroxy-\nnaphthalen" → "hydroxynaphthalen"
    text = re.sub(r"-\s*\n\s*", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def evidence_is_in_article(
    evidence_text: str,
    evidence_type: str,
    article_full_text: str,
    article_table_lookup=None,
) -> bool:
    """Return True iff the evidence is verifiably in the article.

    `article_table_lookup` is an optional callable that takes a
    structured-coordinate string (e.g., 'table: Table 1; row#2; col#3')
    and returns True iff it resolves to a real cell. Phase 4 keeps the
    lookup permissive — it parses the evidence_location structure but
    doesn't yet verify against the article's table objects in full.
    """
    if evidence_type == "verbatim_text":
        e = normalize_for_substring_match(evidence_text)
        if not e:
            return False
        a = normalize_for_substring_match(article_full_text)
        return e in a

    if evidence_type == "structured_coordinates":
        if article_table_lookup is None:
            # Minimal check: structured coordinates must mention a table
            # label (e.g., "Table 1") and a row index.
            return ("table" in evidence_text.lower()
                    and re.search(r"row#?\d+|row\s+\d+", evidence_text,
                                  re.IGNORECASE) is not None)
        return article_table_lookup(evidence_text)

    # No other types are allowed in v1; structured_summary was rejected
    # earlier in the pipeline.
    return False


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--evidence", required=True)
    p.add_argument("--type", default="verbatim_text")
    p.add_argument("--article", required=True,
                   help="path to article full text")
    args = p.parse_args()
    with open(args.article, "r", encoding="utf-8") as f:
        article_text = f.read()
    print(evidence_is_in_article(args.evidence, args.type, article_text))

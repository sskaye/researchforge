"""Phase 5 — Per-paper coverage check.

Per § 5 step 9 of merged_skill_proposal.md. Runs BEFORE verification so
coverage warnings can expand the stratified audit pool.

Three warning conditions per paper:
  1. The paper's abstract contains property keywords AND the paper
     emitted 0 rows AND skipped 0 candidates → silent miss.
  2. A table whose headers match property-keyword triggers contributed
     0 candidates to the index.
  3. The article's abstract claim "N compounds were synthesized" is
     more than 50 % above the emitted+skipped count.
"""

from __future__ import annotations

import os
import re
import sys
from typing import Iterable

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


_PROPERTY_KEYWORDS_DEFAULT = [
    r"\bmelting\s+point",
    r"\bm\.?p\.?\b",
    r"\bmp\s*=",
    r"\bboiling\s+point",
    r"\bb\.?p\.?\b",
    r"\btm\b",
    r"\btb\b",
    r"\btfus\b",
]


def coverage_check(per_article_stats: dict,
                   articles_by_id: dict,
                   property_keywords: Iterable[str] | None = None,
                   ) -> list[dict]:
    """Return a list of coverage warnings.

    Each warning is a dict with keys: article_id, warning, details.

    Inputs:
      per_article_stats[article_id] = {
          "candidates_enumerated": int,
          "kept": int,
          "skipped": int,
      }
      articles_by_id[article_id] = Article object (from ingest_article)
    """
    keywords = list(property_keywords or _PROPERTY_KEYWORDS_DEFAULT)
    kw_re = re.compile("|".join(keywords), re.IGNORECASE)

    warnings: list[dict] = []

    for article_id, stats in per_article_stats.items():
        article = articles_by_id.get(article_id)
        if article is None:
            continue

        emitted = int(stats.get("kept", 0))
        skipped = int(stats.get("skipped", 0))
        candidates = int(stats.get("candidates_enumerated", 0))

        # --- Warning 1: silent miss ---
        # Abstract or full text mentions property keywords but pipeline
        # produced 0 candidates AND 0 emitted/skipped.
        abstract_text = _extract_abstract(article)
        if (kw_re.search(abstract_text)
                and emitted == 0 and skipped == 0 and candidates == 0):
            warnings.append({
                "article_id": article_id,
                "warning": "silent_miss_abstract_mentions_property",
                "details": "Abstract mentions property keywords but no "
                           "candidates were enumerated. Check ingestion "
                           "and find_candidates.",
            })

        # --- Warning 2: property-keyword table with 0 candidates ---
        for t in getattr(article, "tables", []):
            header_text = " ".join(t.headers).lower()
            caption_text = (t.caption or "").lower()
            if kw_re.search(header_text + " " + caption_text):
                # Does this table contribute to candidates? We don't have
                # per-table breakdown easily; approximate by checking if
                # the table label appears in any candidate's
                # evidence_location. (Coverage check is run upstream of
                # emit so we rely on the stats dict alone.)
                # Best we can do: if total candidates == 0, this table
                # contributed nothing.
                if candidates == 0:
                    warnings.append({
                        "article_id": article_id,
                        "warning": "property_table_zero_candidates",
                        "details": f"Table {t.label!r} headers/caption "
                                   "mention property keywords but no "
                                   "candidates were enumerated for the "
                                   "paper.",
                    })
                    break  # one warning per paper for this category

        # --- Warning 3: abstract claim vs row count ---
        # Look for "<N> compounds" / "<N> derivatives" / "<N> new compounds"
        m = re.search(
            r"(\d+)\s+(?:new\s+)?(?:compounds?|derivatives?|analogues?|"
            r"products?|series\s+of)\b",
            abstract_text, re.IGNORECASE,
        )
        if m:
            claimed = int(m.group(1))
            actual = emitted + skipped
            if claimed > 0 and actual < claimed * 0.5:
                warnings.append({
                    "article_id": article_id,
                    "warning": "abstract_claim_far_above_actual",
                    "details": f"Abstract claims {claimed} compounds but "
                               f"emitted+skipped = {actual} "
                               f"({100*actual/claimed:.0f} % of claim).",
                })

    return warnings


def _extract_abstract(article) -> str:
    """Return the article's abstract text if available, else first
    paragraph(s)."""
    # Look for a section whose deepest heading is "Abstract" or "Summary"
    sections = getattr(article, "sections", []) or []
    for sec in sections:
        if sec.heading_path:
            heading = sec.heading_path[-1].lower()
            if heading in ("abstract", "summary", "synopsis"):
                return " ".join(sec.paragraphs)
    # Fallback: first non-empty paragraph(s) of the first section
    if sections and sections[0].paragraphs:
        return " ".join(sections[0].paragraphs)
    # Fallback to first 2000 chars of full_text
    return (article.full_text or "")[:2000]

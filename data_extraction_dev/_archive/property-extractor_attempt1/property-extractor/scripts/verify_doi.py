"""Phase 1: DOI cross-source verification.

Per § 5 step 2 of merged_skill_proposal.md.

Inputs the list of DOICandidate objects from ingest_article.py and
returns a verified DOI, doi_evidence (which source won), and
doi_verified flag. Implements the precedence + decision logic
spelled out in the proposal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# Source precedence (highest to lowest authority)
SOURCE_PRECEDENCE = [
    "nxml_front_matter",      # 1. NXML <front> article-id pub-id-type="doi"
    "pdf_metadata",           # 2. PDF /Doc metadata field
    "pdf_text_first_2_pages", # 3. DOI regex in first 2 pages
    "publisher_lookup",       # 4. Publisher metadata lookup (if configured)
    "user_metadata",          # 5. User-provided metadata file
]


@dataclass
class DOIVerificationResult:
    doi: str                # the DOI to record on rows (may be empty)
    doi_evidence: str       # source that won (one of SOURCE_PRECEDENCE, or "")
    doi_verified: bool      # True if 2+ sources agreed on the same DOI
    warnings: list[str]     # human-readable notes for audit_log

    def __init__(self) -> None:
        self.doi = ""
        self.doi_evidence = ""
        self.doi_verified = False
        self.warnings = []


def _normalize_doi(doi: str) -> str:
    """Trim trailing punctuation, lowercase the doi.org host portion only,
    but preserve case for the registrant/suffix.

    DOIs are case-insensitive per the DOI spec; we lower for comparison
    but preserve the printed form for display.
    """
    return doi.strip().rstrip(".,;)>]").strip()


def _doi_equal(a: str, b: str) -> bool:
    """Case-insensitive DOI equality."""
    return _normalize_doi(a).lower() == _normalize_doi(b).lower()


def verify_doi(candidates: list) -> DOIVerificationResult:
    """Cross-validate DOI candidates.

    Candidates is a list of objects with .doi and .source attributes
    (matches ingest_article.DOICandidate).

    Returns DOIVerificationResult with the chosen DOI, the winning
    source, and verification status.
    """
    result = DOIVerificationResult()

    if not candidates:
        result.warnings.append("doi_no_sources")
        return result

    # Group candidates by normalized doi (case-insensitive). For each group,
    # record which sources contributed and the most-authoritative printed form.
    groups: dict[str, dict] = {}
    for c in candidates:
        norm = _normalize_doi(c.doi).lower()
        if not norm:
            continue
        g = groups.setdefault(norm, {
            "sources": [],
            "display_doi": _normalize_doi(c.doi),
        })
        g["sources"].append(c.source)
        # Use the highest-precedence source's printed form for display
        if (_precedence_rank(c.source)
                < _precedence_rank_of_sources(g["sources"][:-1])):
            g["display_doi"] = _normalize_doi(c.doi)

    if not groups:
        result.warnings.append("doi_no_valid_candidates")
        return result

    # If multiple distinct DOIs appear (genuine conflict), pick the one
    # whose highest-precedence source is best.
    if len(groups) == 1:
        norm, g = next(iter(groups.items()))
        # Only one DOI seen across all sources
        sources = g["sources"]
        # Verified if 2+ DISTINCT sources agree (e.g., NXML + PDF metadata)
        distinct_sources = set(sources)
        if len(distinct_sources) >= 2:
            result.doi = g["display_doi"]
            result.doi_verified = True
            best = _best_source(sources)
            result.doi_evidence = best
            result.warnings.append(
                f"doi_verified_across_{len(distinct_sources)}_sources")
        else:
            result.doi = g["display_doi"]
            result.doi_verified = False
            result.doi_evidence = sources[0]
            result.warnings.append("doi_single_source_only")
        return result

    # Multiple distinct DOIs → conflict
    result.warnings.append(f"doi_conflict_{len(groups)}_distinct_dois")

    # Among the conflicting groups, pick the one whose BEST source has the
    # highest precedence.
    def group_best_rank(item: tuple[str, dict]) -> int:
        return _precedence_rank_of_sources(item[1]["sources"])

    winner = min(groups.items(), key=group_best_rank)
    norm, g = winner
    result.doi = g["display_doi"]
    result.doi_verified = False
    result.doi_evidence = _best_source(g["sources"])
    # Record the conflicting DOIs for the audit log
    other_dois = [v["display_doi"] for k, v in groups.items() if k != norm]
    result.warnings.append(
        f"doi_winning_source={result.doi_evidence}; "
        f"rejected_dois={other_dois}"
    )
    return result


def _precedence_rank(source: str) -> int:
    """Lower rank = higher authority. Returns len(SOURCE_PRECEDENCE)
    for unknown sources (lowest authority)."""
    if source in SOURCE_PRECEDENCE:
        return SOURCE_PRECEDENCE.index(source)
    return len(SOURCE_PRECEDENCE)


def _precedence_rank_of_sources(sources: list[str]) -> int:
    """Best (lowest) rank among sources. Empty list → infinity."""
    if not sources:
        return len(SOURCE_PRECEDENCE) + 1
    return min(_precedence_rank(s) for s in sources)


def _best_source(sources: list[str]) -> str:
    """Return the highest-precedence source from a list."""
    if not sources:
        return ""
    return min(sources, key=_precedence_rank)


# ---------------------------------------------------------------------------
# CLI for diagnostic
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    import sys
    # Reuse the ingester
    sys.path.insert(0, ".")
    from ingest_article import ingest_article  # type: ignore

    p = argparse.ArgumentParser(description="Verify DOI for one article")
    p.add_argument("article_dir")
    args = p.parse_args()

    art = ingest_article(args.article_dir)
    result = verify_doi(art.doi_candidates)

    print(json.dumps({
        "article_id": art.article_id,
        "candidates": [
            {"doi": c.doi, "source": c.source}
            for c in art.doi_candidates
        ],
        "verified_doi": result.doi,
        "doi_evidence": result.doi_evidence,
        "doi_verified": result.doi_verified,
        "warnings": result.warnings,
    }, indent=2, ensure_ascii=False))

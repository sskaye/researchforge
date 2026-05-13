"""Build a candidate index per article using the chosen property adapter.

Phase 2 (§ 5 step 3 of merged_skill_proposal.md): enumerate every property-
relevant mention BEFORE any filtering. Candidate-first design is the fix
for failure mode F5 (silent table miss).
"""

from __future__ import annotations

import csv
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ingest_article import ingest_article          # noqa: E402
from adapter_loader import load_adapter            # noqa: E402


CSV_COLUMNS = [
    "candidate_id", "article_id", "source_type",
    "property_trigger", "raw_value_text", "unit_text", "relation_hint",
    "nearby_compound_handle", "compound_handle_position",
    "evidence_location",
]


def build_index_for_article(article_dir: str, adapter_name: str) -> list[dict]:
    """Run ingestion + candidate enumeration for one article.

    Returns the candidate list. Each candidate has the standard adapter
    contract keys plus article_id (added here for the index CSV).
    """
    article = ingest_article(article_dir)
    adapter = load_adapter(adapter_name)
    cands = adapter.find_candidates(article)
    # Add article_id to every candidate row
    for c in cands:
        c["article_id"] = article.article_id
    return cands


def write_index_csv(candidates: list[dict], out_path: str) -> None:
    """Write a candidate list to a CSV at out_path."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True) if os.path.dirname(out_path) else None
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, quoting=csv.QUOTE_ALL,
                           extrasaction="ignore")
        w.writeheader()
        for c in candidates:
            w.writerow(c)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("article_dir")
    p.add_argument("--adapter", default="mp_bp")
    p.add_argument("--out", default=None,
                   help="output CSV path; default = stdout summary")
    args = p.parse_args()
    cands = build_index_for_article(args.article_dir, args.adapter)
    if args.out:
        write_index_csv(cands, args.out)
        print(f"wrote {len(cands)} candidates to {args.out}")
    else:
        # Summary
        from collections import Counter
        by_source = Counter(c["source_type"] for c in cands)
        by_trigger = Counter(c["property_trigger"] for c in cands)
        print(f"Article: {cands[0]['article_id'] if cands else '?'}")
        print(f"Total candidates: {len(cands)}")
        print(f"By source: {dict(by_source)}")
        print(f"By trigger (top 10): {by_trigger.most_common(10)}")

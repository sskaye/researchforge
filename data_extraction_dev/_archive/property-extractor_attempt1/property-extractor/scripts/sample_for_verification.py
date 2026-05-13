"""Phase 5 — Random + stratified verification sampler.

Per § 9b of merged_skill_proposal.md.

  random sample: 15 % of emitted rows
  stratified pool: 100 % of rows flagged high-risk by validate_row
  minimum total audit pool: 30 (top up with random if below)

Sampling is reproducible: a fixed seed yields the same row→verifier
assignment.
"""

from __future__ import annotations

import random
from typing import Iterable, Sequence


_DEFAULT_RANDOM_FRAC = 0.15
_DEFAULT_MIN_POOL = 30


def build_verification_pool(
    rows: Sequence[dict],
    seed: int,
    random_frac: float = _DEFAULT_RANDOM_FRAC,
    min_pool: int = _DEFAULT_MIN_POOL,
    coverage_warned_articles: set[str] | None = None,
) -> tuple[list[dict], dict]:
    """Return (audit_pool, sampling_report).

    audit_pool: deduplicated list of rows to audit. Each row keeps all its
                original keys plus a sampling_strata field that lists
                which strata caused it to be sampled.

    sampling_report: dict with totals (random_count, stratified_count,
                     audit_pool_size, top_up_count, seed).

    Rules:
      * Stratified rows = those whose validate_row soft_flags is non-empty
        OR which appear in `coverage_warned_articles`.
      * Random rows = a `random_frac` fraction of ALL rows (drawn from
        rows NOT already in the stratified pool).
      * If the union of stratified + random has fewer than min_pool
        members, draw additional random rows up to min_pool. The
        top-up draw is reproducible under the same seed.
      * Overlap between random and stratified is counted once.
    """
    coverage_warned_articles = coverage_warned_articles or set()
    rng = random.Random(seed)

    # Stratified subset
    stratified_ids: set[str] = set()
    stratified: list[dict] = []
    for r in rows:
        strata = []
        if r.get("soft_flags"):
            strata.extend(r["soft_flags"])
        if r.get("article_id") in coverage_warned_articles:
            strata.append("article_coverage_warned")
        if strata:
            r2 = dict(r)
            r2["sampling_strata"] = strata
            stratified.append(r2)
            stratified_ids.add(_row_id(r))

    # Random sample (over rows NOT already in stratified)
    pool = [r for r in rows if _row_id(r) not in stratified_ids]
    n_random = int(round(random_frac * len(rows)))
    rng.shuffle(pool)
    random_sample = pool[:n_random]
    for r in random_sample:
        r["sampling_strata"] = ["random"]

    audit_pool = list(stratified) + list(random_sample)
    top_up_count = 0
    if len(audit_pool) < min_pool:
        # Top up with more random rows from the remaining pool
        already = stratified_ids | {_row_id(r) for r in random_sample}
        remaining = [r for r in rows if _row_id(r) not in already]
        rng.shuffle(remaining)
        needed = min_pool - len(audit_pool)
        top_up_rows = remaining[:needed]
        for r in top_up_rows:
            r["sampling_strata"] = ["random_top_up"]
        audit_pool.extend(top_up_rows)
        top_up_count = len(top_up_rows)

    sampling_report = {
        "seed": seed,
        "random_frac": random_frac,
        "min_pool": min_pool,
        "total_rows": len(rows),
        "stratified_count": len(stratified),
        "random_count": len(random_sample),
        "top_up_count": top_up_count,
        "audit_pool_size": len(audit_pool),
        "coverage_warned_article_count": len(coverage_warned_articles),
    }
    return audit_pool, sampling_report


def _row_id(row: dict) -> str:
    """Stable per-row identity for de-duplication during sampling."""
    return (row.get("candidate_id") or
            f"{row.get('article_id', '?')}::{row.get('compound_name', '?')[:80]}"
            f"::{row.get('value_canonical', '?')}")


if __name__ == "__main__":
    import argparse
    import csv
    import json

    p = argparse.ArgumentParser()
    p.add_argument("rows_csv")
    p.add_argument("--seed", type=int, default=20260511)
    p.add_argument("--random-frac", type=float, default=_DEFAULT_RANDOM_FRAC)
    p.add_argument("--min-pool", type=int, default=_DEFAULT_MIN_POOL)
    p.add_argument("--out", default=None,
                   help="write audit pool to this CSV (one row per audited)")
    args = p.parse_args()
    rows = list(csv.DictReader(open(args.rows_csv)))
    pool, report = build_verification_pool(
        rows, seed=args.seed, random_frac=args.random_frac,
        min_pool=args.min_pool)
    print(json.dumps(report, indent=2))
    if args.out:
        # Each row in the pool has the original schema plus sampling_strata
        fieldnames = list(rows[0].keys()) + ["sampling_strata"] if rows else []
        with open(args.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames,
                               quoting=csv.QUOTE_ALL, extrasaction="ignore")
            w.writeheader()
            for r in pool:
                r2 = dict(r)
                r2["sampling_strata"] = ";".join(r2.get("sampling_strata", []))
                w.writerow(r2)
        print(f"wrote audit pool to {args.out}")

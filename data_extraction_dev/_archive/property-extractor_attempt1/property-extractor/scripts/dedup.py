"""Gate F — Strong-key deduplication.

Per § 5 step 7 of merged_skill_proposal.md.

Dedup key:
  (article_id, normalized_name, property_name, property_subtype,
   value_canonical ± adapter.DEDUP_VALUE_TOLERANCE,
   relation, data_origin, instrument)

Within-paper duplicates (e.g., same compound in table + inline
characterization) collapse to one row. Different `instrument` or
`relation` keep rows distinct on purpose.
"""

from __future__ import annotations

import re
from typing import Iterable


def _normalize_name(name: str) -> str:
    """Lowercase, collapse whitespace, strip trailing local codes
    like '(2a)' or ', 2a'. Used as the dedup key for compound identity."""
    s = (name or "").lower()
    # Drop trailing parenthesized code
    s = re.sub(r"\s*\(\s*\d+[a-z]?\s*\)\s*$", "", s)
    s = re.sub(r"\s*\(\s*compound\s+\d+[a-z]?\s*\)\s*$", "", s)
    s = re.sub(r"\s*,\s*\d+[a-z]?\s*$", "", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _bucket_value(value: float | None, tolerance: float) -> int | None:
    """Bucket a value to within `tolerance` for dedup key equality.

    Rounds to the nearest multiple of `tolerance` so values within
    `tolerance` collapse to the same bucket. Returns None when value
    is None (preserves NULLs as a distinct key).
    """
    if value is None:
        return None
    if tolerance <= 0:
        return value  # type: ignore[return-value]
    return round(value / tolerance)


def dedup_key(row: dict, tolerance: float) -> tuple:
    """Build the dedup key tuple for a row.

    A row that didn't pass earlier gates may still come through to
    dedup; dedup uses only fields it expects to be present in any
    schema-valid row.
    """
    return (
        row.get("article_id", ""),
        _normalize_name(row.get("compound_name", "")),
        row.get("property_name", ""),
        row.get("property_subtype", ""),
        _bucket_value(row.get("value_canonical"), tolerance),
        row.get("relation", "="),
        row.get("data_origin", ""),
        row.get("instrument", ""),
    )


def dedup(rows: Iterable[dict], tolerance: float = 0.5
          ) -> tuple[list[dict], list[dict]]:
    """De-duplicate rows under the strong dedup key.

    Returns (kept_rows, dropped_rows).
    """
    seen: dict[tuple, dict] = {}
    dropped: list[dict] = []
    for r in rows:
        key = dedup_key(r, tolerance)
        if key in seen:
            # Record the dropped row with a skip_reason
            r2 = dict(r)
            r2["skip_reason"] = (
                "deduplicate:collapsed_with="
                + seen[key].get("candidate_id", "<unknown>")
            )
            dropped.append(r2)
            continue
        seen[key] = r
    return list(seen.values()), dropped


if __name__ == "__main__":
    import argparse
    import json
    import csv

    p = argparse.ArgumentParser()
    p.add_argument("rows_csv")
    p.add_argument("--tolerance", type=float, default=0.5)
    args = p.parse_args()

    with open(args.rows_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    # Coerce numeric fields back to floats where present
    for r in rows:
        if r.get("value_canonical"):
            try:
                r["value_canonical"] = float(r["value_canonical"])
            except ValueError:
                pass
    kept, dropped = dedup(rows, tolerance=args.tolerance)
    print(json.dumps({
        "total_in": len(rows),
        "kept": len(kept),
        "dropped": len(dropped),
    }, indent=2))

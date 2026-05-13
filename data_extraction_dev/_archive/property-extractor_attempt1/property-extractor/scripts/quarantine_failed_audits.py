"""Phase 5 — Quarantine audit failures and recompute pass rate.

Per § 5 step 11–12 and § 9c of merged_skill_proposal.md.

Inputs:
  - The current output_draft.csv (post-Gates A–F)
  - The audit results from audit_verifier.run_verification
Outputs:
  - A reduced output CSV with audit-failed rows removed
  - An updated skipped CSV with the quarantined rows added
  - A pass_rate computed AFTER quarantine

The acceptance gate (98 %) is applied to the post-quarantine pass rate,
not the pre-quarantine emission. If the audit sample is empty (no rows
reached emission OR all sampled rows were quarantined), the run is
flagged for human review rather than auto-accepted.
"""

from __future__ import annotations

from typing import Iterable


def quarantine(
    emitted_rows: list[dict],
    audit_results: dict,
    skipped_rows: list[dict] | None = None,
) -> dict:
    """Apply audit verdicts: move failed rows from emitted → skipped,
    recompute the pass rate over the audit sample only.

    Returns:
      {
        "delivered_rows":  list of rows that survived quarantine,
        "skipped_rows":    list of rows skipped (existing + newly
                           quarantined),
        "audit_sample_size": int,
        "pass_count":        int (passed audit),
        "fail_count":        int (failed audit → quarantined),
        "error_count":       int (verifier errored),
        "pass_rate":         float in [0, 1] or None for empty sample,
        "status":            "accepted" | "verification_failed" |
                             "no_emission" | "verifier_unreliable",
      }
    """
    skipped_rows = list(skipped_rows or [])

    if audit_results.get("aborted"):
        return {
            "delivered_rows": [],
            "skipped_rows": skipped_rows,
            "audit_sample_size": 0,
            "pass_count": 0,
            "fail_count": 0,
            "error_count": 0,
            "pass_rate": None,
            "status": "verifier_unreliable",
            "abort_reason": audit_results.get("abort_reason"),
        }

    results = audit_results.get("results", [])
    pass_n = audit_results.get("pass_count", 0)
    fail_n = audit_results.get("fail_count", 0)
    err_n = audit_results.get("error_count", 0)
    sample_size = len(results)

    # Build a set of (row_id) for failed/errored rows
    failed_ids: set[str] = set()
    for r in results:
        if r["verdict"] in ("fail", "error"):
            failed_ids.add(r["row_id"])

    # Quarantine: move from emitted to skipped
    delivered: list[dict] = []
    quarantined_count = 0
    for row in emitted_rows:
        row_id = (row.get("candidate_id") or
                  f"{row.get('article_id','?')}::"
                  f"{row.get('compound_name','?')[:60]}")
        if row_id in failed_ids:
            row2 = dict(row)
            # Find the matching audit result for the skip_reason
            audit_match = next((r for r in results if r["row_id"] == row_id),
                                None)
            reason_tag = (audit_match["reason"] if audit_match else
                          "failed_independent_audit")
            row2["skip_reason"] = f"failed_independent_audit:{reason_tag}"
            skipped_rows.append(row2)
            quarantined_count += 1
        else:
            delivered.append(row)

    # Empty-sample edge case (no rows reached audit OR all failed)
    if sample_size == 0:
        return {
            "delivered_rows": delivered,
            "skipped_rows": skipped_rows,
            "audit_sample_size": 0,
            "pass_count": 0,
            "fail_count": 0,
            "error_count": 0,
            "pass_rate": None,
            "status": "no_emission",
        }

    pass_rate = pass_n / sample_size
    status = "accepted" if pass_rate >= 0.98 else "verification_failed"

    return {
        "delivered_rows": delivered,
        "skipped_rows": skipped_rows,
        "audit_sample_size": sample_size,
        "pass_count": pass_n,
        "fail_count": fail_n,
        "error_count": err_n,
        "pass_rate": pass_rate,
        "quarantined_count": quarantined_count,
        "status": status,
    }

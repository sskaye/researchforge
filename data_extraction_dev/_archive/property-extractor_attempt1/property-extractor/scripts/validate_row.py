"""Phase 5 — Deterministic row validator.

Per § 9a of merged_skill_proposal.md.

Runs after rows have passed Gates A–F in emit_outputs. Confirms each row
satisfies every schema-level invariant. Splits results into:
  - hard failures (row goes to skipped.csv with skip_reason)
  - soft flags (row stays, but is added to the stratified-audit pool)
"""

from __future__ import annotations

import os
import re
import sys
from typing import Iterable

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_name import validate_standalone_name


_DOI_RE = re.compile(r"^10\.\d{4,9}/.+$")
_ALLOWED_RELATIONS = {"=", ">", "<", "≥", "≤", "~", "≈"}
_ALLOWED_VALUE_TYPES = {"numeric", "qualitative", "boolean"}
_ALLOWED_EVIDENCE_TYPES = {"verbatim_text", "structured_coordinates"}
_ALLOWED_NAME_RESOLUTION = {
    "exact_text", "code_lookup", "template_resolution",
    "scheme_mapping", "reviewer_approved_inference",
}
_CONFIDENCE_RANK = {"high": 0, "medium": 1, "low": 2}


def validate_row(row: dict,
                 article_full_text: str = "",
                 adapter_extras: dict | None = None,
                 ) -> tuple[list[str], list[str]]:
    """Run hard-fail and soft-flag checks against a single emitted row.

    Returns (hard_failures, soft_flags) — both are lists of short strings
    describing each problem. An empty hard_failures list means the row
    is valid for delivery.
    """
    adapter_extras = adapter_extras or {}
    hard: list[str] = []
    soft: list[str] = []

    # ---- Hard-fail checks ----

    doi = (row.get("doi") or "").strip()
    if not doi:
        hard.append("doi_empty")
    elif not _DOI_RE.match(doi):
        hard.append("doi_malformed")

    # compound_name passes Gate A
    name = row.get("compound_name", "")
    ok, reason = validate_standalone_name(
        name,
        extra_exempt=adapter_extras.get("EXTRA_EXEMPT_NAMES", []),
        extra_reject=adapter_extras.get("EXTRA_REJECT_PATTERNS", []),
        extra_require=adapter_extras.get("EXTRA_REQUIRE_PATTERNS", []),
    )
    if not ok:
        hard.append(f"compound_name_invalid:{reason}")

    # evidence_type sanity
    compound_evidence_type = row.get("compound_evidence_type", "")
    property_evidence_type = row.get("property_evidence_type", "")
    if compound_evidence_type not in _ALLOWED_EVIDENCE_TYPES:
        hard.append(f"compound_evidence_type_invalid:{compound_evidence_type}")
    if property_evidence_type not in _ALLOWED_EVIDENCE_TYPES:
        hard.append(f"property_evidence_type_invalid:{property_evidence_type}")

    # Evidence in article (verbatim only — structured_coordinates is checked
    # by Gate C upstream)
    if article_full_text:
        ce = row.get("compound_evidence_text", "")
        if compound_evidence_type == "verbatim_text" and ce:
            if not _substring_present(ce, article_full_text):
                hard.append("compound_evidence_not_in_article")
        pe = row.get("property_evidence_text", "")
        if property_evidence_type == "verbatim_text" and pe:
            if not _substring_present(pe, article_full_text):
                hard.append("property_evidence_not_in_article")

    # value_type vs value_canonical/value_text consistency
    vtype = row.get("value_type", "")
    if vtype not in _ALLOWED_VALUE_TYPES:
        hard.append(f"value_type_invalid:{vtype}")
    else:
        v_canon = row.get("value_canonical")
        v_text = row.get("value_text")
        # Empty strings/None coerce to None for the check
        is_canon_set = (v_canon not in (None, "", "None"))
        is_text_set = (v_text not in (None, "", "None"))
        if vtype == "numeric":
            if not is_canon_set:
                hard.append("numeric_value_canonical_missing")
            if is_text_set:
                hard.append("numeric_value_text_present")
        elif vtype == "qualitative":
            if is_canon_set:
                hard.append("qualitative_value_canonical_present")
            if not is_text_set:
                hard.append("qualitative_value_text_missing")
        # boolean rows are emitted by other adapters; we don't enforce here

    # value_original appears in property_evidence_text. This check applies
    # to verbatim-text evidence only — for structured-coordinate rows,
    # the value lives implicitly at the cell coordinates and is not in
    # the evidence string.
    v_orig = (row.get("value_original") or "").strip()
    pe = row.get("property_evidence_text", "")
    if (v_orig and pe
            and property_evidence_type == "verbatim_text"):
        v_norm = (v_orig.replace("–", "-").replace("−", "-")
                          .replace("—", "-"))
        p_norm = (pe.replace("–", "-").replace("−", "-")
                     .replace("—", "-"))
        if v_norm not in p_norm:
            half = v_norm.split("-")[0]
            if half and half not in p_norm:
                hard.append("value_original_not_in_property_evidence")

    # relation in allowed set
    rel = row.get("relation", "=")
    if rel not in _ALLOWED_RELATIONS:
        hard.append(f"relation_invalid:{rel}")

    # data_origin classified (non-empty)
    if not (row.get("data_origin") or "").strip():
        hard.append("data_origin_empty")

    # name_resolution_method in allowed set
    nrm = row.get("name_resolution_method", "")
    if nrm and nrm not in _ALLOWED_NAME_RESOLUTION:
        hard.append(f"name_resolution_method_invalid:{nrm}")

    # extraction_confidence ≤ name_resolution_confidence
    ext_c = row.get("extraction_confidence", "")
    name_c = row.get("name_resolution_confidence", "")
    if ext_c in _CONFIDENCE_RANK and name_c in _CONFIDENCE_RANK:
        if _CONFIDENCE_RANK[ext_c] < _CONFIDENCE_RANK[name_c]:
            hard.append(
                f"confidence_inversion:extraction={ext_c}>name={name_c}")

    # ---- Soft-flag checks (row kept, added to audit pool) ----

    if nrm in ("template_resolution", "scheme_mapping",
                "reviewer_approved_inference"):
        soft.append(f"high_risk_name_resolution_method:{nrm}")

    doi_verified = row.get("doi_verified")
    if doi_verified in (False, "False", "false"):
        soft.append("doi_unverified")

    unit_o = (row.get("unit_original") or "").strip()
    canonical_unit = (row.get("canonical_unit") or "").strip()
    if unit_o and canonical_unit and unit_o != canonical_unit:
        soft.append(f"unit_conversion:{unit_o}->{canonical_unit}")

    data_origin = row.get("data_origin", "")
    if data_origin.startswith("predicted_"):
        soft.append("data_origin_predicted")

    if ext_c in ("medium", "low"):
        soft.append(f"extraction_confidence_{ext_c}")

    return hard, soft


def _substring_present(needle: str, haystack: str) -> bool:
    """Whitespace-collapsing substring check."""
    if not needle or not haystack:
        return False
    n = re.sub(r"\s+", " ", needle).strip()
    h = re.sub(r"\s+", " ", haystack)
    if n in h:
        return True
    # Try a longest-30-char window from the start of the needle as a fallback
    return n[:80] in h


def validate_rows(rows: Iterable[dict],
                  article_full_text_by_id: dict[str, str] | None = None,
                  adapter_extras: dict | None = None,
                  ) -> tuple[list[dict], list[dict]]:
    """Validate a batch of rows.

    Returns (kept_rows, dropped_rows). Each dropped row has a 'skip_reason'
    key with the joined hard failures. Each kept row may have a
    'soft_flags' key listing soft-flag reasons (empty list when no flags).
    """
    article_full_text_by_id = article_full_text_by_id or {}
    kept: list[dict] = []
    dropped: list[dict] = []
    for r in rows:
        article_id = r.get("article_id", "")
        full_text = article_full_text_by_id.get(article_id, "")
        hard, soft = validate_row(r, full_text, adapter_extras)
        r_out = dict(r)
        if hard:
            r_out["skip_reason"] = "validate_row:" + ";".join(hard)
            dropped.append(r_out)
        else:
            r_out["soft_flags"] = soft
            kept.append(r_out)
    return kept, dropped

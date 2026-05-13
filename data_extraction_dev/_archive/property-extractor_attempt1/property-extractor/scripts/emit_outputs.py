"""Drive the full extraction pipeline and emit the deliverable artifacts.

Per § 5 step 8 of merged_skill_proposal.md.

Inputs:
  - input_path: a folder containing per-article subdirectories
  - adapter_name: which property adapter to load
  - output_csv path, skipped_csv path, audit_log path, notes_md path

Procedure (Phase 4 scope — Phase 5 will add the verification gate):
  1. For each article: ingest, build label dict, build template dict,
     find candidates, resolve names, classify origin/subtype/instrument,
     normalize values, run Gates A–F, emit/skip.
  2. Run dedup across all kept rows for the article (Gate F).
  3. Write output_draft.csv, skipped.csv, audit_log.json, extraction_notes.md.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ingest_article import ingest_article                       # noqa: E402
from verify_doi import verify_doi                                # noqa: E402
from adapter_loader import load_adapter                          # noqa: E402
from build_label_dictionary import build_label_dictionary        # noqa: E402
from resolve_template_variables import resolve_template_variables  # noqa: E402
from resolve_compound_name import resolve_compound_name          # noqa: E402
from validate_name import validate_standalone_name               # noqa: E402
from identity_token_check import identity_token_consistency      # noqa: E402
from verify_substring import evidence_is_in_article              # noqa: E402
from dedup import dedup                                          # noqa: E402


# Output CSV columns — matches § 3 schema (Phase 5 will add the
# audit-stratification fields if any are still missing)
OUTPUT_COLUMNS = [
    "compound_name", "compound_label",
    "compound_evidence_text", "compound_evidence_type",
    "name_resolution_method", "name_resolution_confidence",
    "property_name", "property_subtype",
    "value_type", "value_canonical",
    "value_canonical_min", "value_canonical_max",
    "canonical_unit", "value_text",
    "value_original", "unit_original", "relation",
    "property_evidence_text", "property_evidence_type",
    "evidence_location",
    "data_origin", "instrument",
    "source_section",
    "doi", "doi_evidence", "doi_verified",
    "article_id",
    "extraction_confidence",
    "candidate_id",
]

SKIPPED_COLUMNS = [
    "candidate_id", "article_id", "skip_reason",
    "raw_value_text", "unit_text", "relation_hint",
    "nearby_compound_handle", "property_trigger",
    "source_type", "evidence_location",
]


def _confidence_min(a: str, b: str) -> str:
    """Return the lesser of two confidence values."""
    rank = {"high": 0, "medium": 1, "low": 2}
    if rank.get(a, 9) <= rank.get(b, 9):
        return a
    return b


def _process_article(article_dir: str, adapter_name: str,
                     adapter, audit_log: dict) -> tuple[list[dict], list[dict]]:
    """Process one article through the full pipeline.

    Returns (kept_rows, skipped_rows) for this article.
    """
    art = ingest_article(article_dir)
    doi_result = verify_doi(art.doi_candidates)

    label_dict = build_label_dictionary(art)
    template_dict = resolve_template_variables(art)

    extras = {
        "EXTRA_EXEMPT_NAMES": adapter.EXTRA_EXEMPT_NAMES,
        "EXTRA_REJECT_PATTERNS": adapter.EXTRA_REJECT_PATTERNS,
        "EXTRA_REQUIRE_PATTERNS": adapter.EXTRA_REQUIRE_PATTERNS,
    }

    candidates = adapter.find_candidates(art)
    audit_log["per_article"][art.article_id] = {
        "candidates_enumerated": len(candidates),
        "doi": doi_result.doi,
        "doi_verified": doi_result.doi_verified,
        "doi_warnings": doi_result.warnings,
        "ingestion_warnings": list(art.warnings),
        "kept": 0,
        "skipped": 0,
        "by_gate": {},
    }

    kept: list[dict] = []
    skipped: list[dict] = []
    by_gate: dict[str, int] = {}

    article_context = {
        "full_text": art.full_text,
        "doi": doi_result.doi,
        "doi_evidence": doi_result.doi_evidence,
        "doi_verified": doi_result.doi_verified,
        "sections": art.sections,
    }

    for c in candidates:
        skip_reason = None

        # ---- Resolve compound name ----
        res = resolve_compound_name(c, label_dict, template_dict,
                                    adapter_extras=extras)
        if "skip_reason" in res:
            skip_reason = res["skip_reason"]
        else:
            compound_name = res["compound_name"]
            compound_label = res.get("compound_label", "")
            compound_evidence_text = res.get("compound_evidence_text", "")
            name_resolution_method = res["name_resolution_method"]
            name_resolution_confidence = res["name_resolution_confidence"]

            # ---- Gate A: standalone-name validator (already inside
            # resolve_compound_name, but rerun in case of template path)
            ok, reason = validate_standalone_name(
                compound_name,
                extra_exempt=extras["EXTRA_EXEMPT_NAMES"],
                extra_reject=extras["EXTRA_REJECT_PATTERNS"],
                extra_require=extras["EXTRA_REQUIRE_PATTERNS"])
            if not ok:
                skip_reason = reason

        if skip_reason:
            _record_skip(c, art.article_id, skip_reason, skipped, by_gate)
            continue

        # ---- Gate D (value): adapter.parse_value ----
        try:
            value_struct = adapter.parse_value(
                c["raw_value_text"], c.get("unit_text"))
        except ValueError as e:
            _record_skip(c, art.article_id,
                         f"value_unparseable:{e}",
                         skipped, by_gate)
            continue

        # ---- Gate E (data_origin + property_subtype + instrument) ----
        data_origin, property_subtype, instrument = adapter.classify(
            c, article_context)

        # ---- Build the prospective row ----
        property_evidence_text = c.get("evidence_location") or \
                                 c.get("raw_value_text", "")
        # For paragraph candidates, get a small window of the article around
        # the value for property_evidence_text
        if c["source_type"].startswith("paragraph") or c["source_type"] == "pdf_paragraph":
            # The evidence_location says e.g. "section: ... ; para#N"; we
            # already validated via Gate B/C so a simple window from the
            # article around the trigger is the verifiable substring.
            property_evidence_text = _build_property_evidence(c, art)
        property_evidence_type = "structured_coordinates" if c["source_type"] in {
            "table", "table_first_col_trigger", "pdf_table"
        } else "verbatim_text"

        compound_evidence_type = "structured_coordinates" if c["source_type"] in {
            "table", "table_first_col_trigger", "pdf_table"
        } else "verbatim_text"

        # ---- Gate B: identity-token consistency ----
        # For table candidates, the compound_evidence_text comes from
        # res; the position-in-evidence we compute by string search.
        name_position = (
            (compound_evidence_text or "").find(compound_name)
            if compound_name else -1
        )
        gate_b_ok, gate_b_report = identity_token_consistency(
            compound_name=compound_name,
            compound_evidence_text=compound_evidence_text,
            property_evidence_text=property_evidence_text,
            name_position_in_compound_evidence=
                name_position if name_position >= 0 else None,
        )
        if not gate_b_ok:
            _record_skip(c, art.article_id,
                         f"identity_token_mismatch:{gate_b_report}",
                         skipped, by_gate)
            continue

        # ---- Gate C: evidence-substring check ----
        if compound_evidence_type == "verbatim_text":
            if not evidence_is_in_article(compound_evidence_text,
                                           "verbatim_text",
                                           art.full_text):
                _record_skip(c, art.article_id,
                             "evidence_not_in_article:compound_evidence_text",
                             skipped, by_gate)
                continue
        if property_evidence_type == "verbatim_text":
            if not evidence_is_in_article(property_evidence_text,
                                           "verbatim_text",
                                           art.full_text):
                _record_skip(c, art.article_id,
                             "evidence_not_in_article:property_evidence_text",
                             skipped, by_gate)
                continue
        # structured_coordinates: minimal check (Phase 4 keeps lookup permissive)

        # ---- extraction_confidence (cap at doi/name confidence) ----
        extraction_confidence = name_resolution_confidence
        if not article_context["doi_verified"]:
            extraction_confidence = _confidence_min(extraction_confidence,
                                                    "medium")

        # ---- Assemble the row ----
        row = {
            "compound_name": compound_name,
            "compound_label": compound_label,
            "compound_evidence_text": compound_evidence_text,
            "compound_evidence_type": compound_evidence_type,
            "name_resolution_method": name_resolution_method,
            "name_resolution_confidence": name_resolution_confidence,
            "property_name":
                "boiling_point" if property_subtype == "boil"
                else "melting_point",
            "property_subtype": property_subtype,
            "value_type": value_struct["value_type"],
            "value_canonical": value_struct["value_canonical"],
            "value_canonical_min": value_struct["value_canonical_min"],
            "value_canonical_max": value_struct["value_canonical_max"],
            "canonical_unit": adapter.CANONICAL_UNIT,
            "value_text": value_struct.get("value_text"),
            "value_original": value_struct["value_original"],
            "unit_original": value_struct["unit_original"],
            "relation": value_struct["relation"],
            "property_evidence_text": property_evidence_text,
            "property_evidence_type": property_evidence_type,
            "evidence_location": c.get("evidence_location", ""),
            "data_origin": data_origin,
            "instrument": instrument,
            "source_section": _section_from_location(c.get("evidence_location", "")),
            "doi": article_context["doi"],
            "doi_evidence": article_context["doi_evidence"],
            "doi_verified": article_context["doi_verified"],
            "article_id": art.article_id,
            "extraction_confidence": extraction_confidence,
            "candidate_id": c["candidate_id"],
        }
        kept.append(row)

    # ---- Gate F: deduplicate within this article ----
    kept, dropped = dedup(kept, tolerance=adapter.DEDUP_VALUE_TOLERANCE)
    for d in dropped:
        skipped.append({
            "candidate_id": d.get("candidate_id", ""),
            "article_id": art.article_id,
            "skip_reason": d.get("skip_reason",
                                  "deduplicate:collapsed"),
            "raw_value_text": d.get("value_original", ""),
            "unit_text": d.get("unit_original", ""),
            "relation_hint": d.get("relation", "="),
            "nearby_compound_handle": d.get("compound_name", ""),
            "property_trigger": "",
            "source_type": "dedup",
            "evidence_location": d.get("evidence_location", ""),
        })
        by_gate["F_dedup"] = by_gate.get("F_dedup", 0) + 1

    audit_log["per_article"][art.article_id]["kept"] = len(kept)
    audit_log["per_article"][art.article_id]["skipped"] = len(skipped)
    audit_log["per_article"][art.article_id]["by_gate"] = by_gate
    return kept, skipped


def _record_skip(c: dict, article_id: str, reason: str,
                 skipped: list, by_gate: dict) -> None:
    skipped.append({
        "candidate_id": c.get("candidate_id", ""),
        "article_id": article_id,
        "skip_reason": reason,
        "raw_value_text": c.get("raw_value_text", ""),
        "unit_text": c.get("unit_text", ""),
        "relation_hint": c.get("relation_hint", "="),
        "nearby_compound_handle": c.get("nearby_compound_handle", ""),
        "property_trigger": c.get("property_trigger", ""),
        "source_type": c.get("source_type", ""),
        "evidence_location": c.get("evidence_location", ""),
    })
    # Tag by the first-level gate name for the audit summary
    gate_tag = (reason.split(":")[0] if reason else "unknown")
    by_gate[gate_tag] = by_gate.get(gate_tag, 0) + 1


def _build_property_evidence(c: dict, art) -> str:
    """Construct a small property_evidence_text window around the
    candidate's value for paragraph-source candidates.

    Heuristic: scan the article's full text for the property_trigger
    near the raw_value_text, and return a 200-char window.
    """
    value = c.get("raw_value_text", "")
    if not value:
        return c.get("evidence_location", "")
    # Look for an exact occurrence of the value text in the article
    idx = art.full_text.find(value)
    if idx < 0:
        return c.get("evidence_location", "")
    lo = max(0, idx - 120)
    hi = min(len(art.full_text), idx + len(value) + 80)
    return art.full_text[lo:hi]


def _section_from_location(loc: str) -> str:
    """Extract the section path from an evidence_location string."""
    if "section:" in loc:
        return loc.split("section:", 1)[1].split(";")[0].strip()
    if "table:" in loc:
        return loc.split("table:", 1)[1].split(";")[0].strip()
    return loc[:80]


# ---------------------------------------------------------------------------
# Pipeline driver
# ---------------------------------------------------------------------------

def run_pipeline(input_path: str, adapter_name: str,
                 output_csv: str, skipped_csv: str,
                 audit_log: str, notes_md: str | None = None) -> dict:
    """Process every article subdirectory under `input_path`."""
    adapter = load_adapter(adapter_name)
    audit: dict[str, Any] = {
        "run_metadata": {
            "started_at": int(time.time()),
            "input_path": input_path,
            "adapter": adapter_name,
        },
        "per_article": {},
        "totals": {"kept": 0, "skipped": 0, "papers": 0},
    }

    all_kept: list[dict] = []
    all_skipped: list[dict] = []

    article_dirs = sorted(
        os.path.join(input_path, d) for d in os.listdir(input_path)
        if os.path.isdir(os.path.join(input_path, d))
        and not d.startswith(".")
    )
    audit["totals"]["papers"] = len(article_dirs)

    for ad in article_dirs:
        try:
            kept, skipped = _process_article(ad, adapter_name, adapter, audit)
        except Exception as e:
            audit["per_article"][os.path.basename(ad)] = {
                "error": f"{type(e).__name__}: {e}",
            }
            continue
        all_kept.extend(kept)
        all_skipped.extend(skipped)

    audit["totals"]["kept"] = len(all_kept)
    audit["totals"]["skipped"] = len(all_skipped)
    audit["totals"]["finished_at"] = int(time.time())

    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS,
                           quoting=csv.QUOTE_ALL, extrasaction="ignore")
        w.writeheader()
        for r in all_kept:
            w.writerow(r)

    with open(skipped_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SKIPPED_COLUMNS,
                           quoting=csv.QUOTE_ALL, extrasaction="ignore")
        w.writeheader()
        for r in all_skipped:
            w.writerow(r)

    with open(audit_log, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    if notes_md:
        _write_notes_md(notes_md, audit, all_kept, all_skipped)

    return audit


def _write_notes_md(path: str, audit: dict,
                    kept: list[dict], skipped: list[dict]) -> None:
    """Write a human-readable extraction_notes.md summary."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Extraction notes\n\n")
        f.write(f"- Started at: {audit['run_metadata']['started_at']}\n")
        f.write(f"- Adapter: {audit['run_metadata']['adapter']}\n")
        f.write(f"- Articles: {audit['totals']['papers']}\n")
        f.write(f"- Rows kept: {audit['totals']['kept']}\n")
        f.write(f"- Rows skipped: {audit['totals']['skipped']}\n\n")
        f.write("## Per-article summary\n\n")
        f.write("| Article | Candidates | Kept | Skipped |\n")
        f.write("|---|---:|---:|---:|\n")
        for art_id, info in audit["per_article"].items():
            if "error" in info:
                f.write(f"| {art_id[:60]} | ERR | - | - |\n")
            else:
                f.write(f"| {art_id[:60]} | {info['candidates_enumerated']} "
                        f"| {info['kept']} | {info['skipped']} |\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("input_path")
    p.add_argument("--adapter", default="mp_bp")
    p.add_argument("--out", default="output_draft.csv")
    p.add_argument("--skipped", default="skipped.csv")
    p.add_argument("--audit-log", default="audit_log.json")
    p.add_argument("--notes", default="extraction_notes.md")
    args = p.parse_args()
    audit = run_pipeline(args.input_path, args.adapter,
                          args.out, args.skipped,
                          args.audit_log, args.notes)
    print(f"Done. Kept: {audit['totals']['kept']}, "
          f"Skipped: {audit['totals']['skipped']}")

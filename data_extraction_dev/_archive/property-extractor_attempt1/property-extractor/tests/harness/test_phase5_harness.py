"""Phase 5 — Verification-harness self-tests.

Per § 12.8 of merged_skill_proposal.md.
"""

import os
import sys
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from validate_row import validate_row, validate_rows
from sample_for_verification import build_verification_pool
from audit_verifier import (
    load_frozen_prompt, load_sanity_set, normalize_verdict,
    run_verification, mock_verifier_factory,
)
from quarantine_failed_audits import quarantine


# ---------------------------------------------------------------------------
# validate_row tests
# ---------------------------------------------------------------------------

def _good_row():
    return {
        "compound_name": "5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one",
        "compound_label": "2a",
        "compound_evidence_text": "5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one, 2a",
        "compound_evidence_type": "verbatim_text",
        "name_resolution_method": "exact_text",
        "name_resolution_confidence": "high",
        "property_name": "melting_point",
        "property_subtype": "melt",
        "value_type": "numeric",
        "value_canonical": 188.0,
        "value_canonical_min": 187.0,
        "value_canonical_max": 189.0,
        "canonical_unit": "°C",
        "value_text": "",
        "value_original": "187-189",
        "unit_original": "°C",
        "relation": "=",
        "property_evidence_text": "Yield = 43%; mp = 187–189 °C (EtOH)",
        "property_evidence_type": "verbatim_text",
        "evidence_location": "section: 3.1.2 ...; para#0",
        "data_origin": "measured_by_article",
        "instrument": "unk",
        "source_section": "Chemistry",
        "doi": "10.3390/molecules31040699",
        "doi_evidence": "nxml_front_matter",
        "doi_verified": True,
        "article_id": "011_PMC12943719",
        "extraction_confidence": "high",
        "candidate_id": "011__c0001",
    }


def test_validate_row_good_row_no_failures():
    article_text = (
        "5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one, 2a "
        "Yield = 43%; mp = 187–189 °C (EtOH)"
    )
    hard, soft = validate_row(_good_row(), article_text)
    assert hard == [], f"unexpected hard failures: {hard}"


def test_validate_row_empty_doi_hard_fail():
    r = _good_row(); r["doi"] = ""
    hard, _ = validate_row(r, "")
    assert "doi_empty" in hard


def test_validate_row_malformed_doi_hard_fail():
    r = _good_row(); r["doi"] = "not-a-doi"
    hard, _ = validate_row(r, "")
    assert any("doi_malformed" in h for h in hard)


def test_validate_row_bad_relation_hard_fail():
    r = _good_row(); r["relation"] = "!!"
    hard, _ = validate_row(r, "")
    assert any("relation_invalid" in h for h in hard)


def test_validate_row_section_title_name_hard_fail():
    r = _good_row(); r["compound_name"] = "Result and discussion"
    hard, _ = validate_row(r, "")
    assert any("compound_name_invalid" in h for h in hard)


def test_validate_row_value_canonical_missing_for_numeric():
    r = _good_row(); r["value_canonical"] = None
    hard, _ = validate_row(r, "")
    assert "numeric_value_canonical_missing" in hard


def test_validate_row_confidence_inversion():
    r = _good_row()
    r["name_resolution_confidence"] = "low"
    r["extraction_confidence"] = "high"
    hard, _ = validate_row(r, "")
    assert any("confidence_inversion" in h for h in hard)


def test_validate_row_template_resolution_is_soft_flag():
    r = _good_row(); r["name_resolution_method"] = "template_resolution"
    _, soft = validate_row(r, "")
    assert any("template_resolution" in s for s in soft)


def test_validate_row_doi_unverified_is_soft_flag():
    r = _good_row(); r["doi_verified"] = False
    _, soft = validate_row(r, "")
    assert "doi_unverified" in soft


def test_validate_row_unit_conversion_is_soft_flag():
    r = _good_row(); r["unit_original"] = "K"; r["canonical_unit"] = "°C"
    _, soft = validate_row(r, "")
    assert any("unit_conversion" in s for s in soft)


# ---------------------------------------------------------------------------
# sample_for_verification tests
# ---------------------------------------------------------------------------

def _row_n(i, soft_flags=None, article_id="A1"):
    return {"candidate_id": f"r{i:04d}", "article_id": article_id,
            "compound_name": f"compound_{i}", "value_canonical": float(i),
            "soft_flags": soft_flags or []}


def test_sampler_seed_reproducibility():
    rows = [_row_n(i) for i in range(100)]
    p1, _ = build_verification_pool(rows, seed=42, min_pool=30)
    p2, _ = build_verification_pool(rows, seed=42, min_pool=30)
    ids1 = sorted(r["candidate_id"] for r in p1)
    ids2 = sorted(r["candidate_id"] for r in p2)
    assert ids1 == ids2, "same seed must yield same sample"


def test_sampler_random_15pct():
    rows = [_row_n(i) for i in range(100)]
    pool, report = build_verification_pool(rows, seed=1, min_pool=0)
    # 15% of 100 = 15
    assert report["random_count"] == 15
    assert report["stratified_count"] == 0


def test_sampler_stratified_includes_all_flagged():
    rows = ([_row_n(i, soft_flags=["template_resolution"])
             for i in range(5)]
            + [_row_n(i + 100) for i in range(50)])
    pool, report = build_verification_pool(rows, seed=2, min_pool=0)
    assert report["stratified_count"] == 5
    strat_ids = {r["candidate_id"] for r in pool
                  if "template_resolution" in (r.get("sampling_strata") or [])}
    # All 5 flagged rows are in the pool
    flagged_ids = {f"r{i:04d}" for i in range(5)}
    assert flagged_ids.issubset(strat_ids)


def test_sampler_min_pool_enforced():
    rows = [_row_n(i) for i in range(20)]  # tiny corpus
    pool, report = build_verification_pool(
        rows, seed=3, min_pool=30, random_frac=0.0)
    # Should top up to the min_pool (capped at all rows since corpus = 20)
    assert report["audit_pool_size"] == 20  # can't exceed total rows
    assert report["top_up_count"] == 20  # all rows became top-up sample


def test_sampler_coverage_warned_articles_pulled_in():
    rows = [_row_n(i, article_id="A1" if i < 5 else "A2") for i in range(20)]
    pool, report = build_verification_pool(
        rows, seed=4, random_frac=0.0, min_pool=0,
        coverage_warned_articles={"A1"})
    # All A1 rows should be in the pool
    a1_in_pool = {r["candidate_id"] for r in pool
                  if r["article_id"] == "A1"}
    assert len(a1_in_pool) == 5


# ---------------------------------------------------------------------------
# audit_verifier tests
# ---------------------------------------------------------------------------

def test_frozen_prompt_loads_and_hashes_consistently():
    text, h1 = load_frozen_prompt()
    _, h2 = load_frozen_prompt()
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex
    assert "Prompt version: v1" in text


def test_sanity_set_loads():
    s = load_sanity_set()
    assert "rows" in s
    assert len(s["rows"]) == 20
    # 10 correct + 10 wrong
    correct = [r for r in s["rows"] if r["expected_verdict"] == "pass"]
    wrong = [r for r in s["rows"] if r["expected_verdict"] == "fail"]
    assert len(correct) == 10
    assert len(wrong) == 10


def test_normalize_verdict_all_yes_passes():
    raw = {f"q{i}": "Yes" for i in range(1, 7)}
    v, s = normalize_verdict(raw)
    assert v == "pass"


def test_normalize_verdict_one_no_fails():
    raw = {f"q{i}": "Yes" for i in range(1, 7)}
    raw["q3"] = "No"
    v, s = normalize_verdict(raw)
    assert v == "fail"
    assert "q3" in s


def test_normalize_verdict_cannot_determine_fails():
    raw = {f"q{i}": "Yes" for i in range(1, 7)}
    raw["q5"] = "Cannot-determine"
    v, _ = normalize_verdict(raw)
    assert v == "fail"


def test_normalize_verdict_invalid_answer_errors():
    raw = {f"q{i}": "Yes" for i in range(1, 7)}
    raw["q2"] = "Maybe"
    v, _ = normalize_verdict(raw)
    assert v == "error"


def test_mock_verifier_sanity_aware_correctly_flags_known_wrong():
    v = mock_verifier_factory("sanity_aware")
    # Simulate the sanity_article_text for a known-wrong row
    article = ("source_paper=011\nrationale=mock\n"
                "hint:expected_to_fail=q3")
    raw = v({}, article, "prompt")
    assert raw["q3"] == "No"
    assert raw["verdict"] == "fail"


def test_run_verification_with_mock_passes_sanity():
    pool = [{"candidate_id": "p1", "article_id": "X",
             "compound_name": "acetone"}]
    text_provider = lambda art_id: "synthetic article text"
    out = run_verification(pool, text_provider,
                            mock_verifier_factory("sanity_aware"))
    assert not out["aborted"]
    assert out["sanity_rate"] == 1.0
    assert out["audited_count"] == 1
    assert out["pass_count"] == 1


def test_run_verification_always_fail_aborts_sanity():
    pool = [{"candidate_id": "p1", "article_id": "X",
             "compound_name": "acetone"}]
    text_provider = lambda art_id: ""
    out = run_verification(pool, text_provider,
                            mock_verifier_factory("always_fail"))
    assert out["aborted"], "always-fail verifier should fail sanity"
    assert out["abort_reason"] == "verifier_unreliable"


# ---------------------------------------------------------------------------
# quarantine_failed_audits tests
# ---------------------------------------------------------------------------

def test_quarantine_moves_failed_rows():
    emitted = [
        {"candidate_id": "r1", "article_id": "A", "compound_name": "ok_1"},
        {"candidate_id": "r2", "article_id": "A", "compound_name": "ok_2"},
        {"candidate_id": "r3", "article_id": "A", "compound_name": "bad"},
    ]
    audit = {
        "aborted": False,
        "results": [
            {"row_id": "r1", "verdict": "pass", "reason": "ok"},
            {"row_id": "r2", "verdict": "pass", "reason": "ok"},
            {"row_id": "r3", "verdict": "fail", "reason": "q1:No"},
        ],
        "pass_count": 2, "fail_count": 1, "error_count": 0,
    }
    out = quarantine(emitted, audit, skipped_rows=[])
    assert len(out["delivered_rows"]) == 2
    assert len(out["skipped_rows"]) == 1
    assert out["pass_rate"] == 2/3
    assert out["status"] == "verification_failed"  # 67% < 98%


def test_quarantine_pass_rate_above_threshold_accepts():
    # 50 pass, 1 fail → 50/51 ≈ 98.04% — accepted
    emitted = [{"candidate_id": f"r{i}", "article_id": "A",
                "compound_name": f"c{i}"} for i in range(51)]
    results = [{"row_id": f"r{i}", "verdict": "pass", "reason": "ok"}
               for i in range(50)]
    results.append({"row_id": "r50", "verdict": "fail", "reason": "q1:No"})
    audit = {"aborted": False, "results": results,
             "pass_count": 50, "fail_count": 1, "error_count": 0}
    out = quarantine(emitted, audit)
    assert out["status"] == "accepted"


def test_quarantine_empty_sample_flags_for_review():
    out = quarantine([], {"aborted": False, "results": [],
                          "pass_count": 0, "fail_count": 0,
                          "error_count": 0})
    assert out["status"] == "no_emission"
    assert out["pass_rate"] is None


def test_quarantine_aborted_verifier_status():
    out = quarantine([], {"aborted": True,
                          "abort_reason": "verifier_unreliable"})
    assert out["status"] == "verifier_unreliable"


# ---------------------------------------------------------------------------
# Frozen-prompt tamper detection
# ---------------------------------------------------------------------------

def test_prompt_hash_changes_on_mutation():
    text, h1 = load_frozen_prompt()
    mutated = text + "\nINJECTED\n"
    h2 = hashlib.sha256(mutated.encode("utf-8")).hexdigest()
    assert h1 != h2


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import inspect
    here = sys.modules[__name__]
    failures = []
    passed = 0
    for name, fn in inspect.getmembers(here, inspect.isfunction):
        if not name.startswith("test_"):
            continue
        try:
            fn()
            passed += 1
            print(f"PASS  {name}")
        except AssertionError as e:
            failures.append((name, str(e)))
            print(f"FAIL  {name}: {e}")
        except Exception as e:
            failures.append((name, f"{type(e).__name__}: {e}"))
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {len(failures)} failed")
    if failures:
        sys.exit(1)

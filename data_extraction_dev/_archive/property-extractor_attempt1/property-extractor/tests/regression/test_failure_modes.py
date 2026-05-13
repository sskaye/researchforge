"""Regression tests for the eight failure modes (F1–F8) from § 1 and § 12.3
of merged_skill_proposal.md.

Each test is based on the actual case that bit Claude or GPT in the
prior audit. If the gate catches the bad input, the test passes.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
sys.path.insert(0, os.path.join(SKILL_ROOT, "properties", "mp_bp"))

from validate_name import validate_standalone_name
from identity_token_check import identity_token_consistency
from dedup import dedup
import adapter as mp_bp_adapter
from ingest_article import ingest_article
from build_candidate_index import build_index_for_article
from resolve_compound_name import resolve_compound_name
from build_label_dictionary import build_label_dictionary
from resolve_template_variables import resolve_template_variables


DEV_ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"


def find_paper(prefix):
    for d in os.listdir(DEV_ROOT):
        if d.startswith(prefix):
            return os.path.join(DEV_ROOT, d)
    raise FileNotFoundError(prefix)


# ---------------------------------------------------------------------------
# F1 — Wrong-functional-group transcription (Claude paper 011 #5d)
# ---------------------------------------------------------------------------

def test_F1_5d_benzonitrile_caught_by_gate_b():
    """Claude recorded compound 5d as 'benzonitrile' when the paper says
    'benzoic Acid'. Gate B forward identity-token check must reject."""
    bad_name = "4-[(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)-methyl]benzonitrile"
    # The actual paper evidence says 'benzoic Acid'
    correct_evidence = (
        "...]benzoic Acid, 5d Yield = 52%; mp = 193–195 °C (EtOH); "
        "1H-NMR (400 MHz, CDCl3) δ 1.41 (t, 3H, CH2CH3, J = 7.2 Hz)..."
    )
    name_pos = correct_evidence.find("]benzoic")
    ok, report = identity_token_consistency(
        compound_name=bad_name,
        compound_evidence_text=correct_evidence,
        property_evidence_text=correct_evidence,
        name_position_in_compound_evidence=name_pos,
    )
    assert not ok, "Gate B should reject benzonitrile vs benzoic Acid"
    # The forward gap should mention "nitrile"
    fg_forward = report.get("forward", {}).get("fg", [])
    assert "nitrile" in fg_forward, \
        f"Expected 'nitrile' in forward fg gap; got {fg_forward}"


# ---------------------------------------------------------------------------
# F2 — Section title used as compound name
# ---------------------------------------------------------------------------

def test_F2_section_title_rejected_by_gate_a():
    """GPT used 'Result and discussion' as a compound name. Gate A rejects."""
    for n in ["Result and discussion", "Results and Discussion",
              "Halogen-Release Biocides", "Methods"]:
        ok, reason = validate_standalone_name(n)
        assert not ok, f"Gate A should reject section title: {n}"


# ---------------------------------------------------------------------------
# F3 — Local-label-only names (resolver should pick them up via dict)
# ---------------------------------------------------------------------------

def test_F3_paper_020_compound_3_resolved():
    """Paper 020 compound 3: handle='compound 3' resolves via label dict
    to '2-(3-Methoxybenzyloxy)isoindolin-1,3-dione'."""
    art = ingest_article(find_paper("020_PMC11206691"))
    ld = build_label_dictionary(art)
    td = resolve_template_variables(art)
    cand = {"nearby_compound_handle": "compound 3"}
    out = resolve_compound_name(cand, ld, td)
    assert "compound_name" in out, f"resolution failed: {out}"
    assert "Methoxybenzyloxy" in out["compound_name"] or \
        "isoindolin" in out["compound_name"].lower()
    assert out["name_resolution_method"] == "code_lookup"


# ---------------------------------------------------------------------------
# F4 — Template-format names (paper 050 (X=Cl, R=4-CH3))
# ---------------------------------------------------------------------------

def test_F4_paper_050_template_resolved():
    """Paper 050 (X=Cl, R=4-CH3) → '6-chloro-2-methyl-3-(4-methylphenyl)
    quinazoline-4(3H)-thione' via template_resolution."""
    art = ingest_article(find_paper("050_PMC6146942"))
    ld = build_label_dictionary(art)
    td = resolve_template_variables(art)
    cand = {"nearby_compound_handle":
            "2e - 2-methyl-3-phenylquinazoline-4(3H)-thione (X=Cl, R=4-CH3)"}
    out = resolve_compound_name(cand, ld, td)
    assert "compound_name" in out, f"resolution failed: {out}"
    name = out["compound_name"]
    assert "6-chloro" in name.lower()
    assert "methylphenyl" in name


# ---------------------------------------------------------------------------
# F5 — Whole-table miss (Dearden table 2)
# ---------------------------------------------------------------------------

def test_F5_dearden_candidate_enumeration():
    """The candidate index for Dearden must contain ≥196 candidates,
    proving candidate-first enumeration catches the table that GPT
    silently missed."""
    cands = build_index_for_article(find_paper("2009_Dearden"), "mp_bp")
    assert len(cands) >= 196, f"Expected ≥196 candidates, got {len(cands)}"


# ---------------------------------------------------------------------------
# F6 — Duplicate rows from inline + table appearances
# ---------------------------------------------------------------------------

def test_F6_duplicate_inline_and_table_collapses():
    """The same compound + value reported in both an inline characterization
    paragraph and a summary table collapses to one row under dedup."""
    rows = [
        {"article_id": "PAPER1",
         "compound_name": "5-methyl-1,3,4-oxadiazole-2(3H)-thione",
         "property_name": "melting_point", "property_subtype": "melt",
         "value_canonical": 68.0, "relation": "=",
         "data_origin": "measured_by_article", "instrument": "unk",
         "candidate_id": "c1"},
        {"article_id": "PAPER1",
         "compound_name": "5-methyl-1,3,4-oxadiazole-2(3H)-thione (4)",
         "property_name": "melting_point", "property_subtype": "melt",
         "value_canonical": 68.0, "relation": "=",
         "data_origin": "measured_by_article", "instrument": "unk",
         "candidate_id": "c2"},
    ]
    kept, dropped = dedup(rows, tolerance=0.5)
    assert len(kept) == 1
    assert len(dropped) == 1


def test_F6b_distinct_measurement_methods_kept():
    """Same compound + value but different instrument stays distinct."""
    rows = [
        {"article_id": "P", "compound_name": "X",
         "property_name": "melting_point", "property_subtype": "melt",
         "value_canonical": 100.0, "relation": "=",
         "data_origin": "measured_by_article", "instrument": "DSC",
         "candidate_id": "c1"},
        {"article_id": "P", "compound_name": "X",
         "property_name": "melting_point", "property_subtype": "melt",
         "value_canonical": 100.0, "relation": "=",
         "data_origin": "measured_by_article", "instrument": "capillary",
         "candidate_id": "c2"},
    ]
    kept, dropped = dedup(rows, tolerance=0.5)
    assert len(kept) == 2, "Different instruments should keep rows distinct"


# ---------------------------------------------------------------------------
# F7 — Open-bound values are EMITTED with relation, not skipped
# ---------------------------------------------------------------------------

def test_F7_open_bound_emitted_with_relation():
    """A '>300 °C' value should parse with value_canonical=300, relation=>."""
    v = mp_bp_adapter.parse_value(">300", "°C")
    assert v["value_canonical"] == 300.0
    assert v["relation"] == ">"
    assert v["value_canonical_min"] is None  # not a range
    assert v["value_canonical_max"] is None


def test_F7_approximate_relation():
    """An '≈100 °C' value normalizes to relation='~'."""
    v = mp_bp_adapter.parse_value("≈100", "°C")
    assert v["value_canonical"] == 100.0
    assert v["relation"] == "~"


def test_F7_range_value_midpoint():
    """A '109-112' range parses as canonical=110.5, min=109, max=112."""
    v = mp_bp_adapter.parse_value("109-112", "°C")
    assert v["value_canonical"] == 110.5
    assert v["value_canonical_min"] == 109.0
    assert v["value_canonical_max"] == 112.0
    assert v["relation"] == "="


def test_F7_kelvin_to_celsius_conversion():
    """A K value converts to °C via -273.15."""
    v = mp_bp_adapter.parse_value("487.15", "K")
    assert abs(v["value_canonical"] - 214.0) < 0.001
    assert v["unit_original"] == "K"


# ---------------------------------------------------------------------------
# F8 — Paper-jargon parentheticals in compound name
# ---------------------------------------------------------------------------

def test_F8_jargon_with_common_name_via_exempt():
    """Common names like 'acetone' alone pass Gate A. The 'pure guest AC'
    parenthetical should be stripped during name building (Phase 5 audit
    will surface any leakage); for now confirm Gate A's behavior."""
    ok, _ = validate_standalone_name("acetone")
    assert ok
    # And the jargon prefix variant: the validator rejects the whole
    # string because the parenthetical is not a chemistry signal.
    ok, _ = validate_standalone_name("Result and discussion (acetone)")
    assert not ok


# ---------------------------------------------------------------------------
# Run all tests
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

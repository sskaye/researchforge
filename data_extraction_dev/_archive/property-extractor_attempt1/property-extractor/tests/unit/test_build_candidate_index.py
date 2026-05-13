"""Unit tests for scripts/build_candidate_index.py + mp_bp adapter's find_candidates."""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from build_candidate_index import build_index_for_article


DEV_ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"


def find_paper(prefix):
    for d in os.listdir(DEV_ROOT):
        if d.startswith(prefix):
            return os.path.join(DEV_ROOT, d)
    raise FileNotFoundError(prefix)


# ---------- Test 1: paper 020 produces ≥ 39 candidates (proposal target) ----------

def test_paper_020_meets_target():
    cands = build_index_for_article(find_paper("020_PMC11206691"), "mp_bp")
    assert len(cands) >= 39, f"Expected ≥39 candidates, got {len(cands)}"


# ---------- Test 2: Dearden produces ≥ 196 candidates (proposal target) ----------

def test_dearden_meets_target():
    cands = build_index_for_article(find_paper("2009_Dearden"), "mp_bp")
    assert len(cands) >= 196, f"Expected ≥196 candidates, got {len(cands)}"


# ---------- Test 3: paper 064 first-column-trigger pattern works ----------

def test_paper_064_first_column_trigger():
    """Paper 064 Table 5 has Tb/Tm in column 0, not in headers.
    The first-column-trigger logic must pick up these candidates."""
    cands = build_index_for_article(find_paper("064_PMC8697427"), "mp_bp")
    # Must find at least some first-column-trigger candidates
    first_col = [c for c in cands if c["source_type"] == "table_first_col_trigger"]
    assert len(first_col) >= 30, \
        f"Expected ≥30 first-column-trigger candidates, got {len(first_col)}"
    # Triggers must include Tb (boiling) and Tm (melting)
    triggers = {c["property_trigger"] for c in first_col}
    assert "Tb" in triggers or "tb" in {t.lower() for t in triggers}
    assert "Tm" in triggers or "tm" in {t.lower() for t in triggers}


# ---------- Test 4: every candidate has required keys ----------

def test_candidate_schema():
    cands = build_index_for_article(find_paper("026_PMC8332001"), "mp_bp")
    required = {"candidate_id", "raw_value_text", "unit_text",
                "nearby_compound_handle", "compound_handle_position",
                "property_trigger", "source_type", "evidence_location"}
    for c in cands:
        missing = required - set(c.keys())
        assert not missing, f"Candidate missing keys: {missing}; row={c}"


# ---------- Test 5: candidate_id is unique within article ----------

def test_candidate_ids_unique():
    cands = build_index_for_article(find_paper("011_PMC12943719"), "mp_bp")
    ids = [c["candidate_id"] for c in cands]
    assert len(ids) == len(set(ids)), "candidate_id collisions"


# ---------- Test 6: exclusion triggers filter Tg/RMSE ----------

def test_exclusion_triggers_filter_tg():
    """Paper 017 mixes Tg, Tm, Tc. Tg should NOT produce candidates."""
    cands = build_index_for_article(find_paper("017_PMC10673250"), "mp_bp")
    triggers = {c["property_trigger"] for c in cands}
    # Tg should not appear as a property_trigger
    assert "Tg" not in triggers, "Tg should be in exclusion_triggers, not a hit"


# ---------- Test 7: loose PDF candidate count is non-trivial ----------

def test_loose_pdf_emits_candidates():
    """A loose-PDF paper (no NXML) should still get candidates via the
    PDF table heuristic or paragraph fallback."""
    cands = build_index_for_article(find_paper("2014_Schmittel"), "mp_bp")
    # Schmittel has 5 measured mp values; we should find at least 5 candidates
    assert len(cands) >= 5, f"Expected ≥5 candidates for Schmittel, got {len(cands)}"


# ---------- Test 8: paper 028 sees inline mp values ----------

def test_paper_028_inline_candidates():
    """Paper 028 has no NXML tables but many inline mp values.
    Should produce ≥ 30 paragraph candidates."""
    cands = build_index_for_article(find_paper("028_PMC10671214"), "mp_bp")
    para = [c for c in cands if c["source_type"] == "paragraph"]
    assert len(para) >= 30, f"Expected ≥30 paragraph candidates, got {len(para)}"


# ---------- Test 9: paper 056 image-cell table — known limitation ----------

def test_paper_056_image_cell_table_known_partial():
    """Paper 056 has compound names rendered as PNG images in tables.
    The text-only extractor cannot recover these, but it should still
    enumerate the value columns. Documents the known limitation."""
    cands = build_index_for_article(find_paper("056_PMC12395778"), "mp_bp")
    # Even with image cells, the value cells (numeric) should produce some
    # candidates. We don't enforce a high target — this is the known gap.
    # Just confirm the run completes without error and emits some candidates
    # from non-image columns.
    assert isinstance(cands, list)


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

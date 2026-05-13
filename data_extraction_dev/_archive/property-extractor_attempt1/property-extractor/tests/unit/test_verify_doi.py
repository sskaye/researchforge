"""Unit tests for scripts/verify_doi.py.

Per § 12.1 of merged_skill_proposal.md.
Tests the cross-source verification decision logic.
"""
import os
import sys
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from verify_doi import verify_doi, _normalize_doi, _doi_equal


@dataclass
class FakeCandidate:
    doi: str
    source: str


# ---------- Test 1: two sources agree → verified ----------

def test_two_sources_agree():
    candidates = [
        FakeCandidate(doi="10.1234/abc", source="nxml_front_matter"),
        FakeCandidate(doi="10.1234/abc", source="pdf_metadata"),
    ]
    result = verify_doi(candidates)
    assert result.doi == "10.1234/abc"
    assert result.doi_verified is True
    assert result.doi_evidence == "nxml_front_matter"


def test_three_sources_agree():
    candidates = [
        FakeCandidate(doi="10.1234/abc", source="nxml_front_matter"),
        FakeCandidate(doi="10.1234/abc", source="pdf_metadata"),
        FakeCandidate(doi="10.1234/abc", source="pdf_text_first_2_pages"),
    ]
    result = verify_doi(candidates)
    assert result.doi_verified is True
    assert result.doi_evidence == "nxml_front_matter"


# ---------- Test 2: only one source → not verified, capped confidence ----------

def test_one_source_only():
    candidates = [
        FakeCandidate(doi="10.1234/abc", source="pdf_text_first_2_pages"),
    ]
    result = verify_doi(candidates)
    assert result.doi == "10.1234/abc"
    assert result.doi_verified is False
    assert result.doi_evidence == "pdf_text_first_2_pages"
    assert any("single_source" in w for w in result.warnings)


# ---------- Test 3: sources conflict → highest-precedence wins ----------

def test_conflict_nxml_wins_over_pdf_text():
    candidates = [
        FakeCandidate(doi="10.1234/abc", source="nxml_front_matter"),
        FakeCandidate(doi="10.5678/xyz", source="pdf_text_first_2_pages"),
    ]
    result = verify_doi(candidates)
    assert result.doi == "10.1234/abc"  # nxml wins
    assert result.doi_verified is False
    assert result.doi_evidence == "nxml_front_matter"
    # The audit log should record the conflict
    assert any("conflict" in w for w in result.warnings)


def test_conflict_pdf_metadata_wins_over_user_metadata():
    candidates = [
        FakeCandidate(doi="10.1234/abc", source="pdf_metadata"),
        FakeCandidate(doi="10.5678/xyz", source="user_metadata"),
    ]
    result = verify_doi(candidates)
    assert result.doi == "10.1234/abc"
    assert result.doi_evidence == "pdf_metadata"


# ---------- Test 4: zero candidates ----------

def test_no_candidates():
    result = verify_doi([])
    assert result.doi == ""
    assert result.doi_verified is False
    assert any("no_sources" in w for w in result.warnings)


# ---------- Test 5: DOI case-insensitive matching ----------

def test_doi_equality_case_insensitive():
    candidates = [
        FakeCandidate(doi="10.1234/AbCd", source="nxml_front_matter"),
        FakeCandidate(doi="10.1234/abcd", source="pdf_metadata"),
    ]
    result = verify_doi(candidates)
    assert result.doi_verified is True


# ---------- Test 6: DOI normalization trims punctuation ----------

def test_normalize_doi_trims():
    assert _normalize_doi("10.1234/abc.") == "10.1234/abc"
    assert _normalize_doi("10.1234/abc,") == "10.1234/abc"
    assert _normalize_doi("10.1234/abc;)") == "10.1234/abc"
    assert _normalize_doi("  10.1234/abc  ") == "10.1234/abc"


def test_doi_equal_helper():
    assert _doi_equal("10.1234/abc", "10.1234/ABC") is True
    assert _doi_equal("10.1234/abc.", "10.1234/abc") is True
    assert _doi_equal("10.1234/abc", "10.1234/xyz") is False


# ---------- Test 7: integration with real paper 026 ----------

def test_integration_paper_026():
    sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
    from ingest_article import ingest_article
    dev_root = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"
    paper_dir = None
    for d in os.listdir(dev_root):
        if d.startswith("026_PMC8332001"):
            paper_dir = os.path.join(dev_root, d)
            break
    assert paper_dir is not None
    art = ingest_article(paper_dir)
    result = verify_doi(art.doi_candidates)
    assert result.doi == "10.1007/s13738-021-02358-x"
    assert result.doi_verified is True


def test_integration_paper_157_no_doi():
    """Paper 157 has no DOI in NXML or PDF — verify_doi handles gracefully."""
    sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
    from ingest_article import ingest_article
    dev_root = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"
    paper_dir = None
    for d in os.listdir(dev_root):
        if d.startswith("157_PMC3716435"):
            paper_dir = os.path.join(dev_root, d)
            break
    assert paper_dir is not None
    art = ingest_article(paper_dir)
    result = verify_doi(art.doi_candidates)
    assert result.doi == ""
    assert result.doi_verified is False


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

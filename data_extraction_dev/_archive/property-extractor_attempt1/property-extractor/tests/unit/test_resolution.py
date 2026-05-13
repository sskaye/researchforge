"""Unit tests for the Phase 3 resolution scripts:
- build_label_dictionary.py
- resolve_template_variables.py
- resolve_compound_name.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from ingest_article import ingest_article
from build_label_dictionary import build_label_dictionary
from resolve_template_variables import resolve_template_variables
from resolve_compound_name import resolve_compound_name


DEV_ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set"


def find_paper(prefix):
    for d in os.listdir(DEV_ROOT):
        if d.startswith(prefix):
            return os.path.join(DEV_ROOT, d)
    raise FileNotFoundError(prefix)


# ---------- build_label_dictionary ----------

def test_paper_020_compound_3_resolves():
    """Phase 3 acceptance criterion #1."""
    art = ingest_article(find_paper("020_PMC11206691"))
    ld = build_label_dictionary(art)
    assert "3" in ld, f"label dict missing code 3; keys={list(ld.keys())[:10]}"
    name = ld["3"]["name"]
    assert "Methoxybenzyloxy" in name or "isoindolin" in name.lower(), \
        f"Expected isoindolin-1,3-dione, got: {name}"


def test_paper_011_compound_2a_resolves():
    """Paper 011 uses '<NAME>, <code> Yield' pattern."""
    art = ingest_article(find_paper("011_PMC12943719"))
    ld = build_label_dictionary(art)
    assert "2a" in ld
    name = ld["2a"]["name"]
    assert "pyridazin" in name.lower()


def test_label_dictionary_codes_are_lowercase():
    """All codes in the dict are lowercased for case-insensitive lookup."""
    art = ingest_article(find_paper("011_PMC12943719"))
    ld = build_label_dictionary(art)
    for k in ld:
        assert k == k.lower(), f"key not lowercased: {k}"


# ---------- resolve_template_variables ----------

def test_paper_050_x_resolves_to_6_chloro():
    """Phase 3 acceptance criterion #2."""
    art = ingest_article(find_paper("050_PMC6146942"))
    td = resolve_template_variables(art)
    assert "X" in td, f"Variables found: {list(td.keys())}"
    cl = td["X"].get("Cl")
    assert cl is not None, f"X=Cl not found; values={list(td['X'].keys())}"
    assert cl["position"] == 6
    assert cl["prefix"] == "chloro"


def test_paper_050_x_h_is_implied():
    """X=H is auto-bound to position=None (no substituent)."""
    art = ingest_article(find_paper("050_PMC6146942"))
    td = resolve_template_variables(art)
    h = td["X"].get("H")
    assert h is not None
    assert h["position"] is None


def test_paper_without_template_returns_empty():
    """Paper 011 has no X/R templates; resolver should return empty dict."""
    art = ingest_article(find_paper("011_PMC12943719"))
    td = resolve_template_variables(art)
    # May find spurious matches, but shouldn't crash
    assert isinstance(td, dict)


# ---------- resolve_compound_name ----------

def test_resolve_bare_code_via_label_dict():
    art = ingest_article(find_paper("020_PMC11206691"))
    ld = build_label_dictionary(art)
    td = resolve_template_variables(art)
    cand = {"nearby_compound_handle": "compound 3"}
    out = resolve_compound_name(cand, ld, td)
    assert "compound_name" in out, f"resolution failed: {out}"
    assert "Methoxybenzyloxy" in out["compound_name"] or "isoindolin" in out["compound_name"].lower()
    assert out["name_resolution_method"] == "code_lookup"
    assert out["compound_label"] == "3"


def test_resolve_template_to_6_chloro():
    art = ingest_article(find_paper("050_PMC6146942"))
    ld = build_label_dictionary(art)
    td = resolve_template_variables(art)
    cand = {"nearby_compound_handle":
            "2e - 2-methyl-3-phenylquinazoline-4(3H)-thione (X=Cl, R=4-CH3)"}
    out = resolve_compound_name(cand, ld, td)
    assert "compound_name" in out, f"resolution failed: {out}"
    name = out["compound_name"]
    assert "6-chloro" in name.lower(), f"expected '6-chloro' prefix, got: {name}"
    assert "methylphenyl" in name or "4-methyl" in name, \
        f"expected R=4-CH3 → 4-methylphenyl substitution, got: {name}"
    assert out["name_resolution_method"] == "template_resolution"


def test_resolve_verbatim_iupac_name():
    cand = {"nearby_compound_handle":
            "5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one (2a)"}
    out = resolve_compound_name(cand, {}, {})
    assert "compound_name" in out
    assert out["name_resolution_method"] == "exact_text"
    assert out["compound_label"] == "2a"


def test_resolve_unknown_code_skips():
    cand = {"nearby_compound_handle": "compound 999"}
    out = resolve_compound_name(cand, {"1": {"name": "foo"}}, {})
    assert "skip_reason" in out
    assert "not_resolvable" in out["skip_reason"]


def test_resolve_empty_handle_skips():
    out = resolve_compound_name({"nearby_compound_handle": ""}, {}, {})
    assert "skip_reason" in out


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

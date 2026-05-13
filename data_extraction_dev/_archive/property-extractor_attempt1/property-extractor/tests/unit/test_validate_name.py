"""Unit tests for scripts/validate_name.py (Gate A)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from validate_name import validate_standalone_name


# ---------- Test 1: REJECT patterns each catch their canonical case ----------

def test_reject_section_titles():
    for n in ["Result and discussion", "Results and Discussion",
              "Introduction", "Experimental", "Methods"]:
        ok, reason = validate_standalone_name(n)
        assert not ok, f"Should reject section title: {n}"
        assert "name_not_standalone" in reason

def test_reject_bare_codes():
    for n in ["compound 3", "Compound 3", "complex 9", "4a", "1G"]:
        ok, reason = validate_standalone_name(n)
        assert not ok, f"Should reject bare code: {n}"

def test_reject_generic_derivative():
    for n in ["benzoxanthenone derivative 4b",
              "benzoxanthenone derivative",
              "pyridazinone derivative"]:
        ok, reason = validate_standalone_name(n)
        assert not ok, f"Should reject generic derivative: {n}"

def test_reject_complex_of_compound():
    ok, reason = validate_standalone_name("Pb(II) complex of compound 4")
    assert not ok

def test_reject_template_variables():
    for n in ["2,2-dimethyl-3-phenyl-quinazoline (X=Cl, R=4-CH3)",
              "X = H",
              "name with (R=4-Cl) inside"]:
        ok, reason = validate_standalone_name(n)
        assert not ok, f"Should reject template: {n}"

def test_reject_range_labels():
    for n in ["compounds 33-50", "Oximes 33-50"]:
        ok, reason = validate_standalone_name(n)
        assert not ok

def test_reject_empty():
    for n in ["", "   "]:
        ok, reason = validate_standalone_name(n)
        assert not ok


# ---------- Test 2: REQUIRE patterns admit real chemistry ----------

def test_accept_full_iupac_name():
    n = "5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one"
    ok, reason = validate_standalone_name(n)
    assert ok, f"Should accept: {n} (reason: {reason})"

def test_accept_il_shorthand():
    for n in ["[BMIm][NTf2]", "[N1,1,1,4][BF4]", "[C6MIm][NTf2]"]:
        ok, reason = validate_standalone_name(n)
        assert ok, f"Should accept IL: {n} (reason: {reason})"

def test_accept_inorganic():
    for n in ["sodium chloride", "copper(II) sulfate pentahydrate"]:
        ok, reason = validate_standalone_name(n)
        assert ok, f"Should accept inorganic: {n} (reason: {reason})"


# ---------- Test 3: EXEMPT_NAMES bypass require pattern ----------

def test_accept_exempt_names():
    for n in ["acetone", "Acetone", "DDT", "TNT", "glutaraldehyde"]:
        ok, reason = validate_standalone_name(n)
        assert ok, f"Should accept exempt: {n} (reason: {reason})"


# ---------- Test 4: case-insensitive matching ----------

def test_case_insensitivity():
    # Lowercase version of a REJECT pattern still rejects
    for n in ["RESULT AND DISCUSSION", "result and discussion",
              "COMPOUND 3", "compound 3", "Compound 3"]:
        ok, _ = validate_standalone_name(n)
        assert not ok, f"Should reject regardless of case: {n}"


# ---------- Test 5: adapter extras (extra_exempt / reject / require) ----------

def test_extra_exempt_admits_otherwise_rejected():
    # A name that would NOT pass the core REQUIRE patterns
    n = "MyCompoundXYZ123"
    ok_default, _ = validate_standalone_name(n)
    assert not ok_default, "Should reject by default"
    # With an adapter exempt, it admits
    ok_with, _ = validate_standalone_name(n, extra_exempt={"mycompoundxyz123"})
    assert ok_with

def test_extra_reject_blocks_otherwise_accepted():
    n = "5-Acetyl-...-pyridazinone"
    ok_default, _ = validate_standalone_name(n)
    assert ok_default
    ok_with, _ = validate_standalone_name(n, extra_reject=[r"pyridazinone"])
    assert not ok_with


# ---------- Test 6: short abbreviation case (was risky before fix) ----------

def test_short_abbreviations_not_blanket_rejected():
    """Old rule '^.{1,3}$' would have blocked these. Confirm the rule
    is gone and EXEMPT_NAMES admits them."""
    for n in ["TNT", "DDT", "MBT", "BHA"]:
        ok, _ = validate_standalone_name(n)
        assert ok, f"Short abbr should be admitted via EXEMPT_NAMES: {n}"


# ---------- Test 7: chemical diversity (§ 12.10) ----------

def test_chemical_diversity():
    # Small organic molecules
    for n in ["acetonitrile", "methanol", "benzene", "toluene"]:
        ok, _ = validate_standalone_name(n)
        assert ok, n
    # Names with stereodescriptors
    ok, _ = validate_standalone_name("(R)-mandelic acid")
    assert ok
    ok, _ = validate_standalone_name("(2E,4E)-N-Isobutyl-5-phenylpenta-2,4-dienamide")
    assert ok


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

"""Unit tests for scripts/adapter_loader.py."""
import os
import sys
import tempfile
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from adapter_loader import load_adapter, AdapterContractError


# ---------- Test 1: mp_bp adapter loads cleanly ----------

def test_load_mp_bp_adapter():
    m = load_adapter("mp_bp")
    assert m.PROPERTY_NAMES == ["melting_point", "boiling_point"]
    assert m.CANONICAL_UNIT == "°C"
    assert callable(m.find_candidates)


# ---------- Test 2: nonexistent adapter raises ----------

def test_missing_adapter_dir_raises():
    try:
        load_adapter("nonexistent_property_xyz")
    except AdapterContractError as e:
        assert "not found" in str(e).lower() or "missing" in str(e).lower()
        return
    raise AssertionError("Expected AdapterContractError for missing adapter")


# ---------- Test 3: adapter missing a required function raises ----------

def test_adapter_missing_function():
    with tempfile.TemporaryDirectory() as tmp:
        adapter_dir = os.path.join(tmp, "broken")
        os.makedirs(adapter_dir)
        with open(os.path.join(adapter_dir, "adapter.py"), "w") as f:
            f.write(textwrap.dedent("""
                PROPERTY_NAMES = ["x"]
                CANONICAL_UNIT = "X"
                PROPERTY_SUBTYPES = []
                DATA_ORIGINS = []
                EXTRA_EXEMPT_NAMES = set()
                EXTRA_REJECT_PATTERNS = []
                EXTRA_REQUIRE_PATTERNS = []
                DEDUP_VALUE_TOLERANCE = 0.5
                # missing find_candidates, parse_value, classify
            """))
        try:
            load_adapter("broken", properties_root=tmp)
        except AdapterContractError as e:
            assert "find_candidates" in str(e) or "missing functions" in str(e)
            return
        raise AssertionError("Expected AdapterContractError for missing function")


# ---------- Test 4: adapter missing a required constant raises ----------

def test_adapter_missing_constant():
    with tempfile.TemporaryDirectory() as tmp:
        adapter_dir = os.path.join(tmp, "broken")
        os.makedirs(adapter_dir)
        with open(os.path.join(adapter_dir, "adapter.py"), "w") as f:
            f.write(textwrap.dedent("""
                def find_candidates(article): return []
                def parse_value(v, u, c=None): return {}
                def classify(c, ctx): return ("", "", "")
                # PROPERTY_NAMES missing
                CANONICAL_UNIT = "X"
                PROPERTY_SUBTYPES = []
                DATA_ORIGINS = []
                EXTRA_EXEMPT_NAMES = set()
                EXTRA_REJECT_PATTERNS = []
                EXTRA_REQUIRE_PATTERNS = []
                DEDUP_VALUE_TOLERANCE = 0.5
            """))
        try:
            load_adapter("broken", properties_root=tmp)
        except AdapterContractError as e:
            assert "PROPERTY_NAMES" in str(e)
            return
        raise AssertionError("Expected AdapterContractError")


# ---------- Test 5: adapter that raises on import is caught ----------

def test_adapter_import_error():
    with tempfile.TemporaryDirectory() as tmp:
        adapter_dir = os.path.join(tmp, "broken")
        os.makedirs(adapter_dir)
        with open(os.path.join(adapter_dir, "adapter.py"), "w") as f:
            f.write("raise RuntimeError('boom')\n")
        try:
            load_adapter("broken", properties_root=tmp)
        except AdapterContractError as e:
            assert "raised on import" in str(e).lower()
            return
        raise AssertionError("Expected AdapterContractError")


# ---------- Test 6: type-check fails for non-set EXTRA_EXEMPT_NAMES ----------

def test_adapter_wrong_type_extra_exempt_names():
    with tempfile.TemporaryDirectory() as tmp:
        adapter_dir = os.path.join(tmp, "broken")
        os.makedirs(adapter_dir)
        with open(os.path.join(adapter_dir, "adapter.py"), "w") as f:
            f.write(textwrap.dedent("""
                def find_candidates(article): return []
                def parse_value(v, u, c=None): return {}
                def classify(c, ctx): return ("", "", "")
                PROPERTY_NAMES = ["x"]
                CANONICAL_UNIT = "X"
                PROPERTY_SUBTYPES = []
                DATA_ORIGINS = []
                EXTRA_EXEMPT_NAMES = ["should_be_set_not_list"]
                EXTRA_REJECT_PATTERNS = []
                EXTRA_REQUIRE_PATTERNS = []
                DEDUP_VALUE_TOLERANCE = 0.5
            """))
        try:
            load_adapter("broken", properties_root=tmp)
        except AdapterContractError as e:
            assert "EXTRA_EXEMPT_NAMES" in str(e)
            return
        raise AssertionError("Expected AdapterContractError for wrong type")


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

"""Adapter loader.

Per § 5 step 1 of merged_skill_proposal.md. Loads a property adapter from
properties/<name>/, validates the contract, and returns the imported module.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from typing import Any

REQUIRED_FUNCTIONS = ("find_candidates", "parse_value", "classify")
REQUIRED_CONSTANTS = ("PROPERTY_NAMES", "CANONICAL_UNIT",
                      "PROPERTY_SUBTYPES", "DATA_ORIGINS",
                      "DEDUP_VALUE_TOLERANCE")
REQUIRED_LEXICON = ("EXTRA_EXEMPT_NAMES", "EXTRA_REJECT_PATTERNS",
                    "EXTRA_REQUIRE_PATTERNS")


class AdapterContractError(Exception):
    """Raised when an adapter doesn't expose the required contract."""


def load_adapter(adapter_name: str, properties_root: str | None = None) -> Any:
    """Load and validate the adapter at properties/<adapter_name>/adapter.py.

    Returns the imported module. Raises AdapterContractError if any
    required attribute is missing.
    """
    if properties_root is None:
        # Default: properties/ next to scripts/
        here = os.path.dirname(os.path.abspath(__file__))
        properties_root = os.path.abspath(os.path.join(here, "..", "properties"))

    adapter_dir = os.path.join(properties_root, adapter_name)
    if not os.path.isdir(adapter_dir):
        raise AdapterContractError(
            f"Adapter directory not found: {adapter_dir}")

    adapter_py = os.path.join(adapter_dir, "adapter.py")
    if not os.path.isfile(adapter_py):
        raise AdapterContractError(
            f"adapter.py missing in {adapter_dir}")

    # Import the module under a unique name so multiple adapters can coexist
    mod_name = f"property_adapter_{adapter_name}"
    spec = importlib.util.spec_from_file_location(mod_name, adapter_py)
    if spec is None or spec.loader is None:
        raise AdapterContractError(
            f"Cannot create import spec for {adapter_py}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise AdapterContractError(
            f"Adapter {adapter_name} raised on import: {type(e).__name__}: {e}"
        ) from e

    _validate_adapter(module, adapter_name)
    return module


def _validate_adapter(module: Any, name: str) -> None:
    missing_fns = [f for f in REQUIRED_FUNCTIONS if not callable(getattr(module, f, None))]
    if missing_fns:
        raise AdapterContractError(
            f"Adapter {name}: missing functions {missing_fns}")
    missing_consts = [c for c in REQUIRED_CONSTANTS if not hasattr(module, c)]
    if missing_consts:
        raise AdapterContractError(
            f"Adapter {name}: missing constants {missing_consts}")
    missing_lex = [c for c in REQUIRED_LEXICON if not hasattr(module, c)]
    if missing_lex:
        raise AdapterContractError(
            f"Adapter {name}: missing lexicon attrs {missing_lex}")

    # Type checks
    if not isinstance(module.PROPERTY_NAMES, list) or not module.PROPERTY_NAMES:
        raise AdapterContractError(
            f"Adapter {name}: PROPERTY_NAMES must be a non-empty list")
    if not isinstance(module.PROPERTY_SUBTYPES, list):
        raise AdapterContractError(
            f"Adapter {name}: PROPERTY_SUBTYPES must be a list")
    if not isinstance(module.DATA_ORIGINS, list):
        raise AdapterContractError(
            f"Adapter {name}: DATA_ORIGINS must be a list")
    if not isinstance(module.EXTRA_EXEMPT_NAMES, set):
        raise AdapterContractError(
            f"Adapter {name}: EXTRA_EXEMPT_NAMES must be a set")
    if not isinstance(module.DEDUP_VALUE_TOLERANCE, (int, float)):
        raise AdapterContractError(
            f"Adapter {name}: DEDUP_VALUE_TOLERANCE must be numeric")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("adapter_name")
    args = p.parse_args()
    m = load_adapter(args.adapter_name)
    print(f"Loaded adapter {args.adapter_name}")
    print(f"  PROPERTY_NAMES: {m.PROPERTY_NAMES}")
    print(f"  CANONICAL_UNIT: {m.CANONICAL_UNIT}")
    print(f"  PROPERTY_SUBTYPES: {m.PROPERTY_SUBTYPES}")
    print(f"  DEDUP_VALUE_TOLERANCE: {m.DEDUP_VALUE_TOLERANCE}")

"""Gate A — standalone compound-name validator.

Per § 6 of merged_skill_proposal.md.

A name is REJECTED if any REJECT_PATTERN matches OR an adapter's
EXTRA_REJECT_PATTERN matches.

A name passes only if it ALSO matches at least one REQUIRE_PATTERN, OR is
in EXEMPT_NAMES ∪ adapter.EXTRA_EXEMPT_NAMES.

All matching is case-insensitive.
"""

from __future__ import annotations

import re
from typing import Iterable, Optional


_FLAGS = re.IGNORECASE


# Core REJECT patterns (§ 6)
_CORE_REJECT_PATTERNS: list[str] = [
    # --- Section titles / prose fragments ---
    r"^(?:results?\s+and\s+discussion|introduction|experimental|methods?)$",
    r"^(?:synthesis|preparation|general\s+procedure)\b",
    r"^the\s+(?:precursors?|compound|product|minor|main)",
    r"^(?:halogen|aldehyde|amine|phenol)-release\s+biocides?",
    r"^(?:characterization|spectral\s+data|analytical\s+data)",

    # --- Bare codes / local labels ---
    r"^compound\s+\d+[a-z]?$",
    r"^complex\s+\d+[a-z]?$",
    r"^\d+[a-z]?$",

    # --- Generic derivative labels ---
    r"\bderivative\s*\d*[a-z]?\s*$",
    r"\bcomplex\s+of\s+compound\s+\d",

    # --- Unresolved template variables ---
    r"\bX\s*=\s*[A-Za-z0-9]",
    r"\(\s*X\s*=",
    r"\bR\s*=\s*[A-Za-z0-9]",
    r"\(\s*R\s*=",
    r"R\d+\s*=",

    # --- Range labels / plural series ---
    r"\bcompounds?\s+\d+\s*[-–]\s*\d+",
    r"^[A-Z]\w+s\s+\d+[-–]\d+",

    # --- Empty ---
    r"^\s*$",

    # --- Procedural / experimental prose fragments ---
    # If the candidate name contains these words it is procedural prose,
    # not a compound name.
    r"\b(?:mmol|mol|mL|mg|g/mol|mol/L|atm|h\.?\s*\d|min\.?\s*\d)\b",
    r"\b(?:was|were|is|are)\s+(?:added|synthes(?:ized|ised)|prepared|"
    r"obtained|extracted|dissolved|filtered|stirred|cooled|heated|"
    r"refluxed|treated|washed|dried|isolated|purified|evaporated|"
    r"removed)\b",
    r"\b(?:until|then|and\s+then|after\s+which|gave|afforded|yielded)\b",
    r"^\d+\s+(?:mmol|mol|mL|mg|g)\b",

    # Names with a leading numeric weight/volume/amount also indicate
    # procedural prose: "001 mmol of tetrakis ..."
    r"^\d{2,}\s",

    # --- Spectroscopic / mass-spec notation fragments ---
    # These look chemistry-shaped but are NMR/MS context, not compound names.
    r"\bm/z\b",                         # m/z 244
    r"\[\s*M\s*[+\-]\s*[A-Za-z0-9]+\s*\]", # [M+H]+, [M+Na]+, [M-H]-
    r"^MS\s*[\(:]",                     # "MS (ESI):"
    r"\bESI[\-+\s]+MS\b",
    r"\bHRMS\b",
    r"\b1\s*H\s*-?\s*NMR\b",
    r"\b13\s*C\s*-?\s*NMR\b",
    r"\bIR\s*\(",                       # "IR (KBr)" context
    r"\bUV\s*\(",
    r"^calcd\b|^found\b|^anal\.?\s+calcd",
]

# Core REQUIRE patterns (§ 6)
_CORE_REQUIRE_PATTERNS: list[str] = [
    # Chemistry-bearing tokens (organic)
    r"(?:yl|oxy|amine|amino|acid|ester|amide|nitrile|thione|thiol|"
    r"alcohol|phenol|phenyl|methyl|ethyl|hydroxy|naphthal|benzo|"
    r"pyrid|pyrim|thiadiazol|oxadiazol|triazol|imid|sulfanyl|"
    r"sulfonyl|sulfonate|sulfate|phosphate|nitrate|carbox|carbonyl|"
    r"piperidin|piperazin|morpholin|oxazol|furan|thiophen|indol|"
    r"quinolin|xanthen|chromen)",

    # IL / salt shorthand: [...][...]
    r"\[[^\]]+\]\[[^\]]+\]",

    # IUPAC stereodescriptors
    r"\b(?:rac|cis|trans|R|S|E|Z|α|β)-",

    # Inorganic / coordination compound patterns
    r"(?:hydrate|hydrochloride|chloride|bromide|iodide|fluoride|"
    r"oxide|sulfide|nitride|carbonate)\b",
    r"\b[A-Z][a-z]?(?:O|S|N|Cl|Br|I|F)\d*\b",

    # Polymer / material patterns
    r"\b(?:poly|co-poly|block-poly)\w+",
]

# Common-name lexicon
_CORE_EXEMPT_NAMES: set[str] = {
    # Organic small molecules
    "acetone", "acetonitrile", "methanol", "ethanol", "isopropanol",
    "water", "benzene", "toluene", "xylene", "chloroform", "ether",
    "tetrahydrofuran", "thf", "dmf", "dmso", "nmp", "dichloromethane",
    "dcm", "ethyl acetate", "hexane", "heptane", "pentane",
    # APIs / drugs from the audit corpus
    "chloroquine", "hydroxychloroquine", "dexamethasone", "thalidomide",
    "favipiravir", "fingolimod", "umifenovir", "baricitinib", "camostat",
    "ibuprofen", "acetylsalicylic acid", "aspirin",
    # Industrial / biocide / preservative names
    "glutaraldehyde", "bronopol", "dazomet", "tcmtb", "bhap", "mbt",
    "bcdmh", "dbnpa",
    # Common food/pharma additive abbreviations
    "bha", "bht", "bdo", "edta",
    # Halocarbons (common short names)
    "ddt", "ddd", "pcb", "tnt", "rdx", "hmx",
    # Natural products
    "dehydrocholic acid", "tyrindoleninone", "tyrindolinone",
}


def _norm(s: str) -> str:
    return s.strip().lower()


def validate_standalone_name(
    name: str,
    extra_exempt: Optional[Iterable[str]] = None,
    extra_reject: Optional[Iterable[str]] = None,
    extra_require: Optional[Iterable[str]] = None,
) -> tuple[bool, str | None]:
    """Validate a compound name against Gate A rules.

    Returns (ok, reason).
      ok=True, reason=None  → name passes
      ok=False, reason='name_not_standalone:<which_rule>' → rejected

    `extra_*` parameters come from the property adapter.
    """
    extra_exempt = set(map(_norm, extra_exempt or []))
    extra_reject_patterns = list(extra_reject or [])
    extra_require_patterns = list(extra_require or [])

    if not name or not isinstance(name, str):
        return False, "name_not_standalone:empty"

    cleaned = name.strip()
    if not cleaned:
        return False, "name_not_standalone:empty"

    # 1. REJECT patterns
    all_reject = _CORE_REJECT_PATTERNS + extra_reject_patterns
    for pat in all_reject:
        if re.search(pat, cleaned, _FLAGS):
            return False, f"name_not_standalone:reject_pattern:{pat[:50]}"

    # 2. Check EXEMPT lexicon
    norm = _norm(cleaned)
    if norm in _CORE_EXEMPT_NAMES or norm in extra_exempt:
        return True, None

    # 3. REQUIRE patterns
    all_require = _CORE_REQUIRE_PATTERNS + extra_require_patterns
    for pat in all_require:
        if re.search(pat, cleaned, _FLAGS):
            return True, None

    # Neither exempt nor required-pattern-matching → reject
    return False, "name_not_standalone:no_chemistry_signal"


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("name", nargs="+")
    args = p.parse_args()
    name = " ".join(args.name)
    ok, reason = validate_standalone_name(name)
    print(f"name: {name}")
    print(f"  ok={ok}  reason={reason}")

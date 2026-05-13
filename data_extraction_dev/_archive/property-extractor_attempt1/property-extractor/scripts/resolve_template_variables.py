"""Resolve table template variables (X, R, Y, Z, etc.) to their
substituent identity AND position on the parent scaffold.

Per § 5 step 5 of merged_skill_proposal.md.

Output:
  per-article dict of {variable_name: {value: {position: int|None,
                                                 evidence_text: str,
                                                 evidence_source: str}}}

For paper 050, the article prose explicitly says:
  "6-Chloro-...-quinazoline-..."
  "6-chloro derivatives (X = Cl)"
Result: X → {"Cl": {"position": 6, ...}, "H": {"position": None, ...}}

A position of None means "the no-substituent case" (value = H) or
"position not bound from prose" (logged as uncertain).
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


# A small dictionary of substituent atomic / radical names → preferred IUPAC
# prefix form. Used when reconstructing "6-Cl" as "6-chloro" in an expanded
# name.
_SUBST_PREFIX = {
    "h": "",                # H means no substituent — drop locant
    "f": "fluoro",
    "cl": "chloro",
    "br": "bromo",
    "i": "iodo",
    "no2": "nitro",
    "oh": "hydroxy",
    "och3": "methoxy",
    "ome": "methoxy",
    "och2ch3": "ethoxy",
    "oet": "ethoxy",
    "cn": "cyano",
    "ch3": "methyl",
    "me": "methyl",
    "c2h5": "ethyl",
    "et": "ethyl",
    "cf3": "trifluoromethyl",
    "nh2": "amino",
}


# ----------------------------------------------------------------------
# Patterns for (locant, substituent) ↔ (variable, value) pairings in prose
# ----------------------------------------------------------------------

# Pattern 1: "the <locant>-<subst> derivatives (X = <val>)"
# e.g., "the 6-chloro derivatives (X = Cl)"
_PAT_LOCANT_DERIVATIVE = re.compile(
    r"""
    (?P<locant>\d+)
    -
    (?P<subst>chloro|fluoro|bromo|iodo|nitro|hydroxy|methoxy|ethoxy|
              cyano|methyl|ethyl|trifluoromethyl|amino|carboxy)
    \s+(?:derivatives?|analog(?:ue|s)?|compounds?)
    [^.()]{0,80}?
    \(\s*(?P<var>[A-Z])\s*=\s*(?P<val>[A-Za-z0-9_-]{1,12})\s*\)
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Pattern 2: "(X = <val>) at (the )?<locant>-position"
_PAT_VAR_AT_POSITION = re.compile(
    r"""
    \(\s*(?P<var>[A-Z])\s*=\s*(?P<val>[A-Za-z0-9_-]{1,12})\s*\)
    [^.]{0,80}?
    at\s+(?:the\s+)?(?:position\s+)?
    (?P<locant>\d+)(?:[\s-]?position)?
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Pattern 3: "<var> = <val> at (the )?<locant>(-position)?"
_PAT_VAR_EQ_AT = re.compile(
    r"""
    \b(?P<var>[A-Z])\s*=\s*(?P<val>[A-Za-z0-9_-]{1,12})\b
    [^.]{0,40}?
    at\s+(?:the\s+)?(?:position\s+)?(?P<locant>\d+)
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Pattern 4: A paper-wide IUPAC name like
#   "6-Chloro-2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione"
# pairs the locant + substituent with the parent scaffold. We harvest
# (locant, subst) pairs from prose and check against the table's variable
# columns to infer the binding.
_PAT_IUPAC_LOCANT = re.compile(
    r"""
    \b(?P<locant>\d+)
    -
    (?P<subst>chloro|fluoro|bromo|iodo|nitro|hydroxy|methoxy|ethoxy|
              cyano|methyl|ethyl|trifluoromethyl|amino|carboxy)
    -
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _norm_subst(s: str) -> str:
    """Normalize a substituent token. 'Cl' → 'chloro', 'F' → 'fluoro', etc.
    For prefix-form inputs (e.g., 'chloro') just lowercase."""
    s_low = s.lower()
    if s_low in _SUBST_PREFIX:
        canonical = _SUBST_PREFIX[s_low]
        if canonical:
            return canonical
        return "h"   # H = no substituent
    # Already in prefix form?
    if s_low in _SUBST_PREFIX.values():
        return s_low
    return s_low


def _scan_text(text: str, source_label: str,
               out: dict[str, dict[str, dict[str, Any]]]) -> None:
    """Scan one chunk of text and merge findings into `out`."""
    # Pattern 1: "<locant>-<subst> derivatives (X = <val>)"
    for m in _PAT_LOCANT_DERIVATIVE.finditer(text):
        locant = m.group("locant")
        subst_prose = _norm_subst(m.group("subst"))
        var = m.group("var").upper()
        val = m.group("val")
        # The (X = Cl) tells us that VARIABLE = VAL, and the prose
        # locant+substituent tells us the resulting locant+substituent
        # form. We pair: out[X]['Cl'] = {position: 6, prefix: 'chloro'}
        out.setdefault(var, {})
        out[var][val] = {
            "position": int(locant),
            "prefix": subst_prose,
            "evidence_text": m.group(0),
            "evidence_source": source_label,
            "pattern": "locant_derivative",
        }

    # Pattern 2: "(X = Cl) at position 6"
    for m in _PAT_VAR_AT_POSITION.finditer(text):
        var = m.group("var").upper()
        val = m.group("val")
        locant = m.group("locant")
        out.setdefault(var, {})
        if val not in out[var]:
            out[var][val] = {
                "position": int(locant),
                "prefix": _norm_subst(val),
                "evidence_text": m.group(0),
                "evidence_source": source_label,
                "pattern": "var_at_position",
            }

    # Pattern 3: "X = Cl at the 6-position"
    for m in _PAT_VAR_EQ_AT.finditer(text):
        var = m.group("var").upper()
        val = m.group("val")
        locant = m.group("locant")
        # Only accept single-letter variables to avoid false positives
        if len(var) != 1:
            continue
        out.setdefault(var, {})
        if val not in out[var]:
            out[var][val] = {
                "position": int(locant),
                "prefix": _norm_subst(val),
                "evidence_text": m.group(0),
                "evidence_source": source_label,
                "pattern": "var_eq_at",
            }


def resolve_template_variables(article) -> dict[str, dict[str, dict[str, Any]]]:
    """Walk the article and emit {variable: {value: {position, prefix,
    evidence_text, evidence_source}}}.

    Empty dict if no template variables are bound.
    """
    out: dict[str, dict[str, dict[str, Any]]] = {}

    sources: list[tuple[str, str]] = []
    for sec_i, sec in enumerate(article.sections):
        path = " > ".join(sec.heading_path) or "(root)"
        for p_i, para in enumerate(sec.paragraphs):
            sources.append((f"section[{sec_i}].p[{p_i}]: {path}", para))
    if article.full_text:
        sources.append(("article.full_text", article.full_text))

    for label, text in sources:
        _scan_text(text, label, out)

    # Always bind <var> = H to the "no-substituent" form (position None,
    # empty prefix) so that downstream resolution doesn't fail on H rows.
    for var in list(out.keys()):
        if "H" not in out[var] and "h" not in out[var]:
            out[var]["H"] = {
                "position": None,
                "prefix": "",
                "evidence_text": "(implied: H means no substituent)",
                "evidence_source": "implied",
                "pattern": "implied_h",
            }
    return out


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    sys.path.insert(0, HERE)
    from ingest_article import ingest_article  # type: ignore

    p = argparse.ArgumentParser()
    p.add_argument("article_dir")
    args = p.parse_args()
    art = ingest_article(args.article_dir)
    d = resolve_template_variables(art)
    print(f"Article: {art.article_id}")
    print(f"Variables resolved: {list(d.keys())}")
    for var, vals in d.items():
        print(f"\n  {var}:")
        for val, info in vals.items():
            print(f"    {val}: position={info['position']}, prefix={info['prefix']!r}, pattern={info['pattern']}")
            print(f"       evidence: {info['evidence_text'][:100]}")

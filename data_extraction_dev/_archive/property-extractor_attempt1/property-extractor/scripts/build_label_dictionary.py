"""Build an article-wide {code: standalone_name} dictionary.

Per § 5 step 4 of merged_skill_proposal.md.

Walks the whole article looking for code-to-name introductions like:
  "<IUPAC name> ( <code> )"
  "The compound <NAME> (<code>) was synthesized"
  "<NAME>, <code> Yield"
  "Synthesis of <NAME>, <code>"
  "<code>: <NAME>"
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_name import validate_standalone_name


# Pattern building helpers
# ------------------------------------------------------------------
# A "candidate name" is a chunk of text that:
#  - starts with a capital letter or digit (chemistry names can start "5-Acetyl...")
#  - is 10-400 chars long
#  - does NOT cross a sentence boundary (period + space) or paragraph break
#  - does NOT contain section-heading words

_NAME_STOP = r"(?:\bThe compound\b|\bSynthesis of\b|\bResults?\b|"  \
             r"\bExperimental\b|\bGeneral [Pp]rocedure\b|" \
             r"\bSpectral data\b|\bAnalytical data\b)"


def _looks_like_chemistry_name(text: str) -> bool:
    """Quick chemistry-name shape check. Used to filter false positives."""
    if not text or len(text) < 4:
        return False
    # Validator says yes? Use that as the source of truth.
    ok, _ = validate_standalone_name(text)
    return ok


# ------------------------------------------------------------------
# Pattern A: "The compound <NAME> ( <code> ) was synthesized"
# ------------------------------------------------------------------
_PAT_TC = re.compile(
    r"""
    \bThe\s+compound\s+
    (?P<name>[A-Z0-9\[\(][^.;]{8,400}?)       # name
    \s*\(\s*(?P<code>\d+[a-z]?|[A-Z])\s*\)    # code
    \s*(?:was\s+synthesized|was\s+prepared|was\s+obtained)
    """,
    re.VERBOSE | re.IGNORECASE,
)

# ------------------------------------------------------------------
# Pattern B: "<NAME>, <code> Yield"  (synthesis paragraph heading style)
# Used in papers 011, 013, 010, 020, 028.
# ------------------------------------------------------------------
_PAT_NCY = re.compile(
    r"""
    (?P<lead>[.\n]\s+)                          # sentence/section break
    (?P<name>[A-Z0-9\[\(][^.;\n]{8,400}?)       # the chemistry name
    ,\s*(?P<code>\d+[a-z]?|[A-Z])\s+
    (?:Yield|yield)
    """,
    re.VERBOSE,
)

# ------------------------------------------------------------------
# Pattern C: "Synthesis of <NAME>, <code>"  (section header)
# ------------------------------------------------------------------
_PAT_SOF = re.compile(
    r"""
    \bSynthesis\s+of\s+(?:Compound\s+)?
    (?P<name>[A-Z0-9\[\(][^.;\n]{8,400}?)
    ,\s*(?P<code>\d+[a-z]?|[A-Z])\b
    """,
    re.VERBOSE | re.IGNORECASE,
)

# ------------------------------------------------------------------
# Pattern D: "<NAME> ( <code> )"  (generic; lower confidence)
# Anchored to a sentence break to keep the name boundaries sane.
# ------------------------------------------------------------------
_PAT_NPAR = re.compile(
    r"""
    (?P<lead>[.\n]\s+|^\s*)
    (?P<name>[A-Z0-9\[\(][^.;\n]{8,400}?)
    \s*\(\s*(?P<code>\d+[a-z]?|[A-Z])\s*\)
    (?:\s+was\s+|\s+yielded|\s+afforded|\s*\.|\s*,|\s*:)
    """,
    re.VERBOSE,
)

# ------------------------------------------------------------------
# Pattern E: "<code>: <NAME>"  (rare, but seen in some papers)
# ------------------------------------------------------------------
_PAT_CN = re.compile(
    r"""
    (?:^|\n|\.\s+)
    (?P<code>\d+[a-z]?|[A-Z])\s*[:\.]\s+
    (?P<name>[A-Z0-9\[\(][^.;\n]{8,400}?)
    (?=\.\s|\n|$)
    """,
    re.VERBOSE,
)

# Order matters: most-specific patterns first so the best evidence wins
_PATTERNS = [
    ("the_compound_was", _PAT_TC,   "high"),
    ("name_code_yield",   _PAT_NCY,  "high"),
    ("synthesis_of",      _PAT_SOF,  "high"),
    ("name_paren_code",   _PAT_NPAR, "medium"),
    ("code_colon_name",   _PAT_CN,   "medium"),
]


def _clean_name(name: str) -> str:
    """Trim leading/trailing junk and normalize whitespace."""
    s = re.sub(r"\s+", " ", name).strip()
    # Drop a leading single capital letter + period (e.g., "X. ") that
    # sometimes leaks from list numbering.
    s = re.sub(r"^[A-Z]\.\s+", "", s)
    # Drop a trailing word that looks like a section/word boundary.
    return s.strip(" ,;:")


def build_label_dictionary(article) -> dict[str, dict[str, Any]]:
    """Walk the article and emit {code: {name, evidence_text, source,
    confidence}}.

    Code keys are lowercase to make later lookups case-insensitive
    (chemistry codes like "2a" vs "2A" are the same compound).
    """
    out: dict[str, dict[str, Any]] = {}

    # Build the source text to scan: section paragraphs + table cells
    # + full PDF text. (The label dictionary lives at article scope.)
    sources: list[tuple[str, str]] = []  # (source_label, text)
    for sec_i, sec in enumerate(article.sections):
        path = " > ".join(sec.heading_path) or "(root)"
        for p_i, para in enumerate(sec.paragraphs):
            sources.append((f"section[{sec_i}].p[{p_i}]: {path}", para))
    # PDF / plain text: scan article.full_text once
    if article.full_text:
        sources.append(("article.full_text", article.full_text))

    for source_label, text in sources:
        for pattern_name, pat, conf in _PATTERNS:
            for m in pat.finditer(text):
                name_raw = m.group("name")
                code = m.group("code").lower()
                name = _clean_name(name_raw)
                if not _looks_like_chemistry_name(name):
                    continue
                # Build evidence_text from a window around the match
                start = max(0, m.start() - 20)
                end = min(len(text), m.end() + 20)
                evidence = text[start:end]
                # If a higher-confidence entry already exists for this code,
                # keep it (high beats medium).
                existing = out.get(code)
                if existing is not None and existing["confidence_rank"] <= _RANK[conf]:
                    continue
                out[code] = {
                    "name": name,
                    "evidence_text": evidence,
                    "evidence_source": source_label,
                    "evidence_start_in_source": m.start(),
                    "name_start_in_evidence": evidence.find(name),
                    "confidence": conf,
                    "confidence_rank": _RANK[conf],
                    "pattern_name": pattern_name,
                }
    # Strip internal confidence_rank from output for callers
    for v in out.values():
        v.pop("confidence_rank", None)
    return out


_RANK = {"high": 0, "medium": 1, "low": 2}


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    sys.path.insert(0, HERE)
    from ingest_article import ingest_article

    p = argparse.ArgumentParser()
    p.add_argument("article_dir")
    p.add_argument("--code", default=None, help="show only entry for this code")
    args = p.parse_args()
    art = ingest_article(args.article_dir)
    d = build_label_dictionary(art)
    if args.code:
        key = args.code.lower()
        print(json.dumps(d.get(key, {}), indent=2, ensure_ascii=False))
    else:
        print(f"Article: {art.article_id}")
        print(f"Code → name entries: {len(d)}")
        # Show a few examples
        for k in sorted(d.keys())[:15]:
            entry = d[k]
            print(f"  {k}: {entry['name'][:80]}  [{entry['pattern_name']}, {entry['confidence']}]")

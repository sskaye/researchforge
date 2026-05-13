"""Resolve a candidate's compound handle to a standalone compound name.

Per § 5 step 6 of merged_skill_proposal.md.

Precedence (first hit wins):
  (a) The handle already contains a verbatim IUPAC-like name        → exact_text
  (b) The handle is a bare code; look up in label dictionary        → code_lookup
  (c) The handle is a template like "(X=Cl, R=4-CH3)"; expand
      using the template-variable dictionary and a scaffold name    → template_resolution
  (d) Reviewer-approved inference (out of scope for v1)

Output: a dict with
  compound_name, compound_label, compound_evidence_text,
  name_resolution_method, name_resolution_confidence
OR None plus a skip_reason.
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_name import validate_standalone_name


# Code shape: bare like "1", "2a", "4h", "(10b)", "A", "B";
# or labeled like "compound 3", "complex 9", "complex 10", "Complex A".
_CODE_RE = re.compile(
    r"""
    ^\s*
    (?:compound\s+|complex\s+|cpd\s+)?           # optional "compound"/"complex" prefix
    \(?\s*(?P<code>\d{1,3}[a-z]?|[A-Z])\s*\)?
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Pattern that recognizes a template-format handle like:
#   "1a - 2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thiones (1) (X=H, R=4-CH3)"
# or
#   "1a (X=H, R=4-CH3)"
# Returns the parent scaffold (without the (X=, R=) trailing chunk) and
# the X/R key=value pairs.
_TEMPLATE_RE = re.compile(
    r"""
    ^
    (?:(?P<code>\d{1,3}[a-z]?)\s*[-:]\s+)?       # optional leading code
    (?P<scaffold>[^()]+?(?:\([^()]*\))*[^()]*?)  # the scaffold prose
    \s*
    \(\s*
        (?P<vars>
            [A-Z]\s*=\s*[A-Za-z0-9_-]+
            (?:\s*,\s*[A-Z]\s*=\s*[A-Za-z0-9_-]+)*
        )
    \s*\)\s*$
    """,
    re.VERBOSE,
)


def _looks_like_full_iupac_name(text: str) -> bool:
    """Predicate: handle is likely a full chemistry name already."""
    if not text:
        return False
    text = text.strip()
    # Cheap shape check
    if len(text) < 6:
        return False
    # Has at least one chemistry-bearing token
    ok, _ = validate_standalone_name(text)
    return ok


def _extract_code_from_handle(handle: str) -> Optional[str]:
    """If the handle is a bare/parenthesized code, return the code in
    lowercase. Otherwise None."""
    if not handle:
        return None
    m = _CODE_RE.match(handle)
    if m:
        return m.group("code").lower()
    # Or the handle has a trailing "(code)"
    m = re.search(r"\(\s*(\d{1,3}[a-z]?|[A-Z])\s*\)\s*$", handle)
    if m:
        return m.group(1).lower()
    return None


def _extract_template(handle: str) -> Optional[dict[str, str]]:
    """Pull X=, R= pairs out of a template-style handle.
    Returns {"X": "Cl", "R": "4-CH3"} or None if not a template."""
    m = _TEMPLATE_RE.match(handle.strip())
    if not m:
        return None
    pairs = {}
    for kv in re.split(r"\s*,\s*", m.group("vars")):
        k, v = kv.split("=", 1)
        pairs[k.strip().upper()] = v.strip()
    return pairs


def _scaffold_from_template_handle(handle: str) -> str:
    """Extract the scaffold prose from a template handle, dropping the
    trailing (X=…, R=…) parenthetical."""
    s = re.sub(r"\s*\(\s*[A-Z]\s*=\s*[^)]+\)\s*$", "", handle).strip()
    # Drop a leading "<code> -" or "<code> :"
    s = re.sub(r"^\s*\d{1,3}[a-z]?\s*[-:]\s+", "", s)
    return s


def _apply_locant_substituent(
        scaffold: str, locant: int, prefix: str) -> str:
    """Prepend "<locant>-<prefix>-" to scaffold. If prefix is empty
    (H case, no substituent), return scaffold unchanged."""
    if not prefix:
        return scaffold
    # Use lowercase prefix per IUPAC convention
    pre = f"{locant}-{prefix.lower()}-"
    return pre + scaffold[0].lower() + scaffold[1:]


def _apply_phenyl_R(scaffold: str, r_value: str) -> str:
    """Replace "3-phenyl" with "3-(R-phenyl)" — i.e., put the R substituent
    on the phenyl ring. r_value is e.g. "4-CH3" (4-methylphenyl)."""
    if not r_value or r_value == "H":
        return scaffold
    # Common substituent-shorthand → IUPAC-prefix mapping. Keys are the
    # element/group symbol as it appears in the paper's R column.
    mapping = {
        "ch3": "methyl", "c2h5": "ethyl", "c3h7": "propyl",
        "isoc3h7": "isopropyl", "ic3h7": "isopropyl",
        "c4h9": "butyl", "tc4h9": "tert-butyl",
        "ocf3": "trifluoromethoxy", "och3": "methoxy", "oet": "ethoxy",
        "oc2h5": "ethoxy", "ome": "methoxy",
        "cl": "chloro", "br": "bromo", "f": "fluoro", "i": "iodo",
        "no2": "nitro", "cn": "cyano", "oh": "hydroxy", "nh2": "amino",
        "cf3": "trifluoromethyl",
    }
    # Plural pattern first: "3,4-Cl2", "2,4,6-Cl3"
    m = re.match(r"^(?P<loc>\d+(?:,\d+)+)-(?P<token>[A-Za-z][A-Za-z0-9]*?)"
                 r"(?P<count>[2-9])$", r_value)
    if m:
        loc = m.group("loc")
        token = m.group("token").lower()
        count = int(m.group("count"))
        prefix = mapping.get(token, token)
        multipliers = {2: "di", 3: "tri", 4: "tetra"}
        prefix = multipliers.get(count, "") + prefix
        new_phenyl = f"{loc}-{prefix}phenyl"
        # Match "3-phenyl" as a substituent prefix. We use a forward
        # boundary that allows the next char to be either a non-word OR
        # a continuation of the IUPAC name (e.g., "3-phenylquinazoline").
        return re.sub(r"\b3-phenyl(?=[a-z\-]|\b)", f"3-({new_phenyl})",
                      scaffold, count=1)
    # Single pattern: "4-CH3", "4-Br", "4-isoC3H7"
    m = re.match(r"^(?P<loc>\d+)-(?P<token>[A-Za-z][A-Za-z0-9]*)$", r_value)
    if m:
        loc = m.group("loc")
        token = m.group("token").lower()
        prefix = mapping.get(token, token)
        new_phenyl = f"{loc}-{prefix}phenyl"
        # Match "3-phenyl" as a substituent prefix. We use a forward
        # boundary that allows the next char to be either a non-word OR
        # a continuation of the IUPAC name (e.g., "3-phenylquinazoline").
        return re.sub(r"\b3-phenyl(?=[a-z\-]|\b)", f"3-({new_phenyl})",
                      scaffold, count=1)
    # Unrecognized R format — leave scaffold unchanged
    return scaffold


def resolve_compound_name(
    candidate: dict,
    label_dict: dict[str, dict[str, Any]],
    template_dict: dict[str, dict[str, dict[str, Any]]],
    adapter_extras: Optional[dict] = None,
) -> dict[str, Any]:
    """Resolve `candidate["nearby_compound_handle"]` to a standalone name.

    Returns a dict with one of two shapes:
      Success:
        {
          "compound_name": "...",
          "compound_label": "...",  # the paper-local code if any
          "compound_evidence_text": "...",
          "name_resolution_method": "...",
          "name_resolution_confidence": "high" | "medium" | "low",
        }
      Failure:
        {"skip_reason": "compound_identity_not_resolvable_from_paper:<details>"}
    """
    handle = (candidate.get("nearby_compound_handle") or "").strip()
    adapter_extras = adapter_extras or {}
    extra_exempt = adapter_extras.get("EXTRA_EXEMPT_NAMES", set())
    extra_reject = adapter_extras.get("EXTRA_REJECT_PATTERNS", [])
    extra_require = adapter_extras.get("EXTRA_REQUIRE_PATTERNS", [])

    if not handle:
        return {"skip_reason": "compound_identity_not_resolvable_from_paper:no_handle"}

    # (a) Handle already a full IUPAC name
    if _looks_like_full_iupac_name(handle):
        # If the handle has a trailing "(<code>)", split it off into label
        code_m = re.search(r"\(\s*(\d{1,3}[a-z]?|[A-Z])\s*\)\s*$", handle)
        compound_label = code_m.group(1).lower() if code_m else ""
        name = handle
        if code_m:
            name = handle[:code_m.start()].strip().rstrip(",")
        # Validate
        ok, reason = validate_standalone_name(
            name, extra_exempt=extra_exempt,
            extra_reject=extra_reject, extra_require=extra_require)
        if ok:
            return {
                "compound_name": name,
                "compound_label": compound_label,
                "compound_evidence_text": handle,
                "name_resolution_method": "exact_text",
                "name_resolution_confidence": "high",
            }
        # else fall through to other strategies

    # (b) Bare code lookup
    code = _extract_code_from_handle(handle)
    if code and code in label_dict:
        entry = label_dict[code]
        ok, _ = validate_standalone_name(
            entry["name"], extra_exempt=extra_exempt,
            extra_reject=extra_reject, extra_require=extra_require)
        if ok:
            return {
                "compound_name": entry["name"],
                "compound_label": code,
                "compound_evidence_text": entry["evidence_text"],
                "name_resolution_method": "code_lookup",
                "name_resolution_confidence": entry.get("confidence", "high"),
            }

    # (c) Template expansion: (X=H, R=4-CH3) style
    template = _extract_template(handle)
    if template and template_dict:
        scaffold = _scaffold_from_template_handle(handle)
        expanded = scaffold
        # Apply X first if present
        if "X" in template and "X" in template_dict:
            val = template["X"]
            binding = template_dict["X"].get(val)
            if binding is None:
                # Try case-insensitive lookup
                binding = template_dict["X"].get(val.upper()) or template_dict["X"].get(val.lower())
            if binding:
                if binding["position"] is None:
                    pass  # H — no change
                else:
                    expanded = _apply_locant_substituent(
                        expanded, binding["position"], binding["prefix"])
        # Apply R if present
        if "R" in template:
            expanded = _apply_phenyl_R(expanded, template["R"])
        # Validate the expanded name
        ok, _ = validate_standalone_name(
            expanded, extra_exempt=extra_exempt,
            extra_reject=extra_reject, extra_require=extra_require)
        if ok and expanded != handle:
            # Extract compound label (the leading code, if any)
            lbl_m = re.match(r"^\s*(\d{1,3}[a-z]?)\s*[-:]\s+", handle)
            compound_label = lbl_m.group(1).lower() if lbl_m else ""
            return {
                "compound_name": expanded,
                "compound_label": compound_label,
                "compound_evidence_text": handle,
                "name_resolution_method": "template_resolution",
                "name_resolution_confidence": "medium",
            }
        # Template not fully resolvable
        return {"skip_reason":
                f"compound_identity_not_resolvable_from_paper:template_var_unresolved"}

    return {"skip_reason":
            f"compound_identity_not_resolvable_from_paper:handle='{handle[:60]}'"}


# ------------------------------------------------------------------
# CLI helper
# ------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    sys.path.insert(0, HERE)
    from ingest_article import ingest_article  # type: ignore
    from build_label_dictionary import build_label_dictionary  # type: ignore
    from resolve_template_variables import resolve_template_variables  # type: ignore

    p = argparse.ArgumentParser()
    p.add_argument("article_dir")
    p.add_argument("--handle", required=True, help="the nearby_compound_handle to resolve")
    args = p.parse_args()
    art = ingest_article(args.article_dir)
    ld = build_label_dictionary(art)
    td = resolve_template_variables(art)
    cand = {"nearby_compound_handle": args.handle}
    out = resolve_compound_name(cand, ld, td)
    print(json.dumps(out, indent=2, ensure_ascii=False))

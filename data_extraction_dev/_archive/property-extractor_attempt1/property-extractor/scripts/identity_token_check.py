"""Gate B — Identity-token consistency check.

Per § 7a of merged_skill_proposal.md.

The check is BIDIRECTIONAL and POSITION-AWARE:
  * Forward: every category token in compound_name must appear in the
    UNION of compound_evidence_text + property_evidence_text.
  * Reverse: every category token in compound_evidence_text within
    ±60 chars of the compound-name occurrence must also appear in
    compound_name.
  * Locants: paired (locant, token) tuples must agree between name
    and the local evidence window.

Catches the Claude paper 011 #5d benzonitrile/benzoic-acid error
and rows where the resolver omitted a substituent that the evidence
clearly shows.
"""

from __future__ import annotations

import re
from typing import Optional


# Substituent abbreviation → IUPAC-prefix mapping. Used during the forward
# token check to accept abbreviated forms in evidence: if the compound_name
# says "chloro" but the evidence says "Cl", they refer to the same
# substituent. This stops Gate B from rejecting rows whose template
# expansion normalized "Cl" → "chloro".
SUBST_ABBREVIATIONS: dict[str, list[str]] = {
    "chloro": ["cl"],
    "bromo": ["br"],
    "fluoro": ["f"],
    "iodo": ["i"],
    "methoxy": ["och3", "ome"],
    "ethoxy": ["oet", "oc2h5"],
    "methyl": ["ch3", "me"],
    "ethyl": ["c2h5", "et"],
    "amino": ["nh2"],
    "hydroxy": ["oh"],
    "nitro": ["no2"],
    "cyano": ["cn"],
    "trifluoromethyl": ["cf3"],
    "phenyl": ["ph"],
    "acetyl": ["ac"],
}


def _token_present_in_evidence(token: str, evid_text: str) -> bool:
    """Check if `token` (or any of its known abbreviations) is in evid_text.
    Case-insensitive."""
    if token in evid_text:
        return True
    abbrevs = SUBST_ABBREVIATIONS.get(token, [])
    for abbr in abbrevs:
        # Look for the abbreviation with non-word context on at least one side
        # so we don't false-match inside another token.
        if re.search(r"(?<![a-z0-9])" + re.escape(abbr) + r"(?![a-z])",
                     evid_text):
            return True
    return False


# Identity-bearing substring tokens, organized by category. Locants are
# NOT in this dict; they are handled by a separate regex-based function.
IDENTITY_TOKENS: dict[str, list[str]] = {
    # Functional-group suffixes
    "fg": ["nitrile", "acid", "ester", "amide", "amine", "alcohol",
           "ether", "ketone", "aldehyde", "phenol", "sulfonate",
           "sulfanyl", "sulfonyl", "sulfide", "thione", "thiol",
           "oxide", "imine", "imide", "carboxyl", "carboxamide",
           "carbamate", "carbonyl"],

    # Substituent prefixes (identity-changing)
    "subst": ["fluoro", "chloro", "bromo", "iodo", "nitro", "methoxy",
              "ethoxy", "hydroxy", "amino", "cyano", "trifluoromethyl",
              "phenoxy", "methylthio", "acetyl", "carboxy",
              "methylenedioxy"],

    # Heterocycle stems
    "het": ["pyridazin", "pyrimidin", "thiadiazol", "oxadiazol",
            "triazol", "imidazol", "thiazol", "pyrrol", "furan",
            "thiophen", "naphthalen", "indol", "quinolin",
            "isoquinolin", "xanthen", "chromen", "piperidin",
            "piperazin", "morpholin", "oxazol"],

    # Salt / hydrate / coordination descriptors
    "form": ["hydrate", "hydrochloride", "sulfate", "acetate",
             "nitrate", "phosphate", "methanesulfonate", "tosylate",
             "chloride", "bromide", "iodide", "fluoride", "oxide",
             "carbonate"],

    # Stoichiometric / counterion identifiers
    "stoich": ["bis", "tris", "tetra", "penta", "hexa", "di", "tri",
               "tetrakis"],
}


# Locant + substituent pattern: "<locant>(,locant)*-<substituent token>"
# Examples: "6-chloro", "3,5-dimethyl", "2-amino".
_LOCANT_TOKEN_RE = re.compile(
    r"\b(?P<locant>\d+(?:,\d+)*)-(?P<token>[a-z]+)",
    re.IGNORECASE,
)


def _extract_locant_pairs(text: str) -> set[tuple[str, str]]:
    """Return (locant, token) tuples found in text. Token is lowercased."""
    pairs: set[tuple[str, str]] = set()
    for m in _LOCANT_TOKEN_RE.finditer(text):
        locant = m.group("locant")
        token = m.group("token").lower()
        pairs.add((locant, token))
    return pairs


def _locant_consistency(compound_name: str,
                        local_evidence_text: str
                        ) -> tuple[bool, list[tuple[str, str, str]]]:
    """For every (locant, token) pair in compound_name, the same pair must
    appear in the local evidence. If the SAME token appears with a
    DIFFERENT locant, that's a disagreement.

    Returns (ok, list of (direction, locant, token) mismatches).
    """
    name_pairs = _extract_locant_pairs(compound_name)
    evid_pairs = _extract_locant_pairs(local_evidence_text)

    all_identity_tokens = {t for cat in IDENTITY_TOKENS.values() for t in cat}

    mismatches: list[tuple[str, str, str]] = []

    # Forward: every locant pair in name must be in evidence OR the token
    # isn't in evidence at all (handled by main forward check).
    for locant, token in name_pairs:
        if (locant, token) not in evid_pairs:
            other_locants = [p[0] for p in evid_pairs if p[1] == token]
            if other_locants:
                # Same token, different locant → disagreement
                mismatches.append(("forward_locant_disagrees", locant, token))

    # Reverse: identity tokens in evidence with locants must match name
    for locant, token in evid_pairs:
        if token in all_identity_tokens and (locant, token) not in name_pairs:
            other_in_name = [p[0] for p in name_pairs if p[1] == token]
            if other_in_name:
                mismatches.append(("reverse_locant_disagrees", locant, token))

    return (len(mismatches) == 0, mismatches)


def identity_token_consistency(
    compound_name: str,
    compound_evidence_text: str,
    property_evidence_text: str,
    name_position_in_compound_evidence: Optional[int] = None,
    local_window: int = 60,
) -> tuple[bool, dict]:
    """Bidirectional + position-aware identity-token check.

    Returns (ok, report). Report has keys:
      - forward: dict of category → missing tokens
      - reverse: dict of category → missing tokens
      - locants: list of (direction, locant, token) mismatches

    If `name_position_in_compound_evidence` is None, the whole
    compound_evidence_text is used as the local window (fallback).
    The reverse check is only as good as the position information.
    """
    name = compound_name.lower()
    evid_full = (compound_evidence_text + " " + property_evidence_text).lower()

    if (name_position_in_compound_evidence is not None
            and name_position_in_compound_evidence >= 0):
        start = max(0, name_position_in_compound_evidence - local_window)
        end = (name_position_in_compound_evidence
               + len(compound_name) + local_window)
        local_evid = compound_evidence_text[start:end].lower()
    else:
        local_evid = compound_evidence_text.lower()

    forward_missing: dict[str, list[str]] = {}
    reverse_missing: dict[str, list[str]] = {}
    for category, tokens in IDENTITY_TOKENS.items():
        name_tokens = {t for t in tokens if t in name}
        evid_tokens = {t for t in tokens if t in evid_full}
        local_evid_tokens = {t for t in tokens if t in local_evid}
        # Forward gap: tokens in name that aren't in evidence — but also
        # accept known abbreviations of those tokens in the evidence.
        forward_gap = set()
        for t in name_tokens:
            if t not in evid_tokens and not _token_present_in_evidence(
                    t, evid_full):
                forward_gap.add(t)
        if forward_gap:
            forward_missing[category] = sorted(forward_gap)
        # Reverse gap: tokens in local evidence that aren't in name.
        # Also accept abbreviation: if evidence has "Cl" near the name AND
        # name has "chloro", that's consistent.
        reverse_gap = set()
        for t in local_evid_tokens:
            if t not in name_tokens:
                # Check if the name uses the abbreviated form
                abbrevs = SUBST_ABBREVIATIONS.get(t, [])
                if not any(a in name for a in abbrevs):
                    reverse_gap.add(t)
        if reverse_gap:
            reverse_missing[category] = sorted(reverse_gap)

    locant_ok, locant_mismatches = _locant_consistency(
        compound_name, local_evid)

    ok = (not forward_missing
          and not reverse_missing
          and locant_ok)
    return ok, {
        "forward": forward_missing,
        "reverse": reverse_missing,
        "locants": locant_mismatches,
    }


if __name__ == "__main__":
    import argparse
    import json
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--compound-evidence", required=True)
    p.add_argument("--property-evidence", default="")
    p.add_argument("--name-pos", type=int, default=None)
    args = p.parse_args()
    ok, report = identity_token_consistency(
        args.name, args.compound_evidence, args.property_evidence,
        args.name_pos)
    print(f"ok={ok}")
    print(json.dumps(report, indent=2, ensure_ascii=False))

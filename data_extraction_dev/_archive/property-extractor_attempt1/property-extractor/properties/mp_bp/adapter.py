"""mp_bp property adapter — Phase 2: find_candidates only.

parse_value() and classify() are Phase 4 stubs that raise NotImplementedError
so any premature call is loud.

Per §§ 5, 8a of merged_skill_proposal.md.
"""

from __future__ import annotations

import os
import re
import yaml
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Adapter contract constants (§ 8a)
# ---------------------------------------------------------------------------

PROPERTY_NAMES = ["melting_point", "boiling_point"]
CANONICAL_UNIT = "°C"
PROPERTY_SUBTYPES = ["melt", "decomp", "melt_or_decomp", "boil",
                     "DSC_onset", "DSC_peak", "sublimation"]
DATA_ORIGINS = ["measured_by_article", "literature_cited"]  # + predicted_<method>
EXTRA_EXEMPT_NAMES: set[str] = {
    "glutaraldehyde", "dehydrocholic acid",
    "tyrindoleninone", "tyrindolinone",
}
EXTRA_REJECT_PATTERNS: list[str] = []
EXTRA_REQUIRE_PATTERNS: list[str] = []
DEDUP_VALUE_TOLERANCE = 0.5  # °C

_HERE = os.path.dirname(os.path.abspath(__file__))
_TRIGGERS_PATH = os.path.join(_HERE, "triggers.yaml")


@dataclass
class _Triggers:
    paragraph: list[str]
    table_headers: list[str]
    exclusion: list[str]
    relation: dict[str, list[str]]
    instruments: list[str]


def _load_triggers() -> _Triggers:
    with open(_TRIGGERS_PATH, "r") as f:
        data = yaml.safe_load(f)
    return _Triggers(
        paragraph=data["property_triggers"]["paragraph"],
        table_headers=data["property_triggers"]["table_headers"],
        exclusion=data.get("exclusion_triggers", []),
        relation=data.get("relation_triggers", {}),
        instruments=data.get("instruments", []),
    )


_TRIGGERS: _Triggers | None = None
def triggers() -> _Triggers:
    global _TRIGGERS
    if _TRIGGERS is None:
        _TRIGGERS = _load_triggers()
    return _TRIGGERS


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# A temperature value: optional sign, digits, optional decimal, optional range
_VALUE_RE = re.compile(
    r"""
    (?P<rel>[><≥≤~≈]|[<>=]\s*=)?       # optional relation symbol
    \s*
    (?P<num>
      [-−]?\d+(?:\.\d+)?
      (?:\s*[-–−]\s*[-−]?\d+(?:\.\d+)?)?
    )
    \s*
    (?P<unit>°\s*C|°\s*F|\bK\b|\bC\b|\bF\b)?
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _compile_trigger_regex(triggers_list: list[str], boundary: bool = True) -> re.Pattern:
    """Compile a list of trigger strings into a single alternation regex,
    longest-first to prefer 'melting point' over 'mp', and with appropriate
    word-boundary handling.

    For triggers containing only word characters (e.g., 'mp', 'Mp', 'Tm',
    'Tfus'), wrap with \b boundaries.
    For triggers containing non-word characters (e.g., 'm.p.', 'B.P.',
    'melting point'), use lookahead/behind to ensure non-word boundary
    on the alphanumeric edges.
    """
    parts = []
    # Sort by length descending so longer matches are tried first
    for t in sorted(set(triggers_list), key=len, reverse=True):
        escaped = re.escape(t)
        # Detect if the trigger starts/ends with a word char
        starts_word = bool(re.match(r"\w", t))
        ends_word = bool(re.search(r"\w$", t))
        pre = r"(?<!\w)" if starts_word else ""
        post = r"(?!\w)" if ends_word else ""
        parts.append(pre + escaped + post)
    pattern = "|".join(parts)
    return re.compile(pattern, re.IGNORECASE)


def _is_excluded(text: str, match_start: int, match_end: int,
                 exclusion_pattern: re.Pattern, window: int = 80) -> bool:
    """Return True if an exclusion trigger appears within `window` chars
    on either side of the match. This catches Tg, RMSE, etc. near an mp."""
    lo = max(0, match_start - window)
    hi = min(len(text), match_end + window)
    return bool(exclusion_pattern.search(text, lo, hi))


def _find_compound_handle(text: str, trigger_pos: int) -> tuple[str, int]:
    """Look backwards from trigger_pos for a likely compound handle.

    Strategies (first hit wins):
      1. The pattern `<NAME>, <code>` immediately preceding a Yield/yield word.
         This is the canonical synthesis-paragraph format.
      2. A standalone "<NAME> (<code>)" where the code is a real compound
         code shape (digit+letter or 2-3 digit number, NOT bare 0/1
         which often refer to scheme labels).
      3. The most recent parenthesized compound code "(NN)" alone.

    Returns (handle_text, position_in_text). If no good handle found, returns
    ("", -1).

    Any captured handle is sanity-checked: it must NOT obviously be prose
    (no "was synthesized", "mmol", etc.). When the captured handle looks
    procedural, we fall through to subsequent strategies.
    """
    # Search the preceding 500 chars
    window_start = max(0, trigger_pos - 500)
    pre = text[window_start:trigger_pos]

    # Helper: is `name` plausibly a chemistry name? Cheap shape check.
    def _plausible_name(name: str) -> bool:
        n = name.strip()
        if not n or len(n) < 4:
            return False
        # Reject obvious procedural prose
        if re.search(
            r"\b(?:was|were|is|are)\s+"
            r"(?:added|synthes(?:ized|ised)|prepared|obtained|extracted|"
            r"dissolved|filtered|stirred|cooled|heated|refluxed|treated|"
            r"washed|dried|isolated|purified|evaporated|removed)\b",
            n, re.IGNORECASE,
        ):
            return False
        if re.search(r"\b(?:mmol|mol|mL|mg|g/mol|mol/L)\b", n, re.IGNORECASE):
            return False
        if re.search(r"\b(?:until|and\s+then|after\s+which|gave|afforded|yielded)\b",
                     n, re.IGNORECASE):
            return False
        # Real chemistry names rarely start with a multi-digit number that
        # represents an amount (e.g. "001 mmol").
        if re.match(r"^\d{2,}\s", n):
            return False
        return True

    # Pattern 1: "<NAME>, <code> Yield" — high-precision synthesis heading.
    # The name may be preceded by a sentence boundary (". "), a paragraph
    # boundary, or be at the very start of the search window.
    m = None
    for cand in re.finditer(
        r"(?:^|\.\s+|\n\s*)"
        r"(?P<name>[A-Z0-9][^.;\n]{15,400}?),\s*(?P<code>\d+[a-z]?)\s+(?:Yield|yield)",
        pre,
    ):
        if _plausible_name(cand.group("name")):
            m = cand
    if m:
        return m.group(0).strip(), window_start + m.start()

    # Pattern 2: "<NAME> (<code>)" — restrict code to compound-code shape:
    #   - digit + letter (e.g., 2a, 4h)
    #   - OR 2-3 digit number (e.g., 10, 99)
    #   - OR single uppercase letter (A, B)
    # This excludes bare "0" / "1" which often refer to scheme labels.
    m2 = None
    for cand in re.finditer(
        r"(?P<name>[A-Z0-9\[][^.;]{10,300}?)\s*\(\s*"
        r"(?P<code>\d+[a-z]|\d{2,3}|[A-Z])\s*\)",
        pre,
    ):
        if _plausible_name(cand.group("name")):
            m2 = cand
    if m2:
        return m2.group(0).strip(), window_start + m2.start()

    # Pattern 3: most-recent "(<code>)" alone (only digit+letter or letter)
    m3 = None
    for cand in re.finditer(r"\(\s*(\d+[a-z]|[A-Z])\s*\)", pre):
        m3 = cand
    if m3:
        return m3.group(0).strip(), window_start + m3.start()

    # Pattern 4: a capitalized chemistry-shape name in the LAST 100 chars
    # before the trigger. Targets prose like
    #   "Tyrindoleninone, red needles, mp 109.5 °C"
    # The name MUST pass the full Gate A validator — this is stricter than
    # _plausible_name and stops false positives like "Yield" or "After".
    # Validation runs locally via lazy import to avoid module-level cycles.
    try:
        from validate_name import validate_standalone_name  # type: ignore
    except ImportError:
        import sys as _sys
        import os as _os
        _scripts_dir = _os.path.join(_os.path.dirname(__file__),
                                      "..", "..", "scripts")
        _sys.path.insert(0, _os.path.abspath(_scripts_dir))
        from validate_name import validate_standalone_name  # type: ignore

    short_pre = pre[-150:]
    m4 = None
    for cand in re.finditer(
        r"\b(?P<name>[A-Z][a-zA-Z0-9\[\]\-,']{4,60})",
        short_pre,
    ):
        candidate_text = cand.group("name")
        if not _plausible_name(candidate_text):
            continue
        ok, _ = validate_standalone_name(candidate_text)
        if ok:
            m4 = cand
    if m4:
        offset = window_start + len(pre) - len(short_pre) + m4.start()
        return m4.group("name").strip(), offset

    return "", -1


def _next_value_after(text: str, start: int, window: int = 60) -> tuple[str, str | None, str, int]:
    """Look for a temperature value within `window` chars after start.

    Returns (raw_value_text, unit_text_or_None, relation_str, abs_position).
    Returns ("", None, "=", -1) if no value found.
    """
    end = min(len(text), start + window)
    chunk = text[start:end]
    m = _VALUE_RE.search(chunk)
    if not m:
        return "", None, "=", -1
    num = m.group("num").strip()
    unit_raw = m.group("unit")
    unit = unit_raw.replace(" ", "") if unit_raw else None
    rel = (m.group("rel") or "=").strip()
    # Normalize approximate symbol
    if rel == "≈":
        rel = "~"
    # Default relation if rel is empty
    if not rel:
        rel = "="
    return num, unit, rel, start + m.start()


# ---------------------------------------------------------------------------
# Helpers for table-template handles (paper-050-style tables)
# ---------------------------------------------------------------------------

def _parse_caption_scaffolds(caption: str) -> dict[str, str]:
    """Parse a table caption that lists series scaffolds.

    Patterns supported:
      "<scaffold> (1) and <scaffold> (2)" → {"1": s1, "2": s2}
      "<scaffold> (1)"                     → {"1": s1}

    Scaffold names may contain nested parentheses like "(3H)" or "(4-Cl)";
    the regex allows one level of nesting via "[^()] | \([^()]*\)".

    Returns an empty dict when no series-scaffold pattern is found.
    """
    if not caption:
        return {}
    # Allow one level of nested parens in the scaffold name
    s_body = r"(?:[^()]|\([^()]*\))"
    # Pattern A: "<scaffold1> (1) and <scaffold2> (2)"
    m = re.search(
        r"(?P<s1>[A-Z0-9](?:" + s_body + r"){15,200}?)\s*\(\s*1\s*\)"
        r"\s+(?:and|&)\s+"
        r"(?P<s2>[A-Z0-9](?:" + s_body + r"){15,200}?)\s*\(\s*2\s*\)",
        caption,
    )
    if m:
        return {
            "1": _clean_scaffold(m.group("s1")),
            "2": _clean_scaffold(m.group("s2")),
        }
    # Pattern B: "<scaffold> (1)"
    m = re.search(
        r"(?P<s>[A-Z0-9](?:" + s_body + r"){15,200}?)\s*\(\s*1\s*\)",
        caption,
    )
    if m:
        return {"1": _clean_scaffold(m.group("s"))}
    return {}


def _clean_scaffold(text: str) -> str:
    """Strip caption-prose prefix words and trailing plural 's' from a
    scaffold name extracted from a table caption.

    "Analytical data of 2,2-dimethyl-...thiones" → "2,2-dimethyl-...thione"
    """
    s = text.strip().rstrip(",;: ")
    # Common caption prefixes we strip
    prefix_words = (
        r"^(?:"
        r"analytical\s+data\s+of\s+|"
        r"data\s+(?:for|of)\s+|"
        r"properties\s+of\s+|"
        r"physical\s+properties\s+of\s+|"
        r"results?\s+for\s+|"
        r"summary\s+of\s+|"
        r"the\s+compounds?\s+"
        r")"
    )
    s = re.sub(prefix_words, "", s, flags=re.IGNORECASE).strip()
    # Singularize plural IUPAC chemical-name endings: "thiones" → "thione"
    s = re.sub(r"(ones|ines|ones|olines|oles|amines|amides|"
               r"acids|esters|alcohols|thiones|ethers|ketones)\b",
               lambda m: m.group(1)[:-1],   # drop the trailing "s"
               s, flags=re.IGNORECASE)
    return s


def _sanity_check_range(value_text: str) -> str:
    """If `value_text` is a range like '238-24182' where hi has too many
    digits, truncate hi to match the lo's digit count. Returns the
    sanity-checked value text (or the original if no truncation needed).

    Reason: NXML cells in some papers concatenate mp range + yield with
    no separator, e.g., '238-241' + '82' → '238-24182'. The true range
    is 238-241; the trailing 82 is the yield.
    """
    m = re.match(r"^(-?\d+(?:\.\d+)?)-(-?\d+(?:\.\d+)?)$", value_text)
    if not m:
        return value_text
    lo_str, hi_str = m.group(1), m.group(2)
    try:
        lo = float(lo_str)
        hi = float(hi_str)
    except ValueError:
        return value_text
    # Plausible mp/bp range: hi within 100 °C of lo
    if abs(hi - lo) <= 100:
        return value_text
    # Truncate hi to first len(lo_str) digits and retry
    if len(hi_str) > len(lo_str):
        truncated_hi = hi_str[:len(lo_str)]
        try:
            new_hi = float(truncated_hi)
            if abs(new_hi - lo) <= 100:
                return f"{lo_str}-{truncated_hi}"
        except ValueError:
            pass
    # Otherwise return as-is and let downstream validation flag it
    return value_text


def _build_template_handle(code_cell: str, row, template_cols: dict[str, int],
                            series_scaffolds: dict[str, str]) -> str:
    """Synthesize a template-style handle from a table row's X/R values
    and the matching series scaffold.

    Returns an empty string when no template can be built (no template cols,
    or no series scaffold matches the row's code).
    """
    if not template_cols or not series_scaffolds:
        return ""
    code = code_cell.strip()
    # The compound code typically starts with the series digit
    # (e.g., "1a" → series "1", "2e" → series "2").
    m = re.match(r"^(\d{1,3})([a-z]?)$", code)
    if not m:
        return ""
    series = m.group(1)
    scaffold = series_scaffolds.get(series)
    if scaffold is None:
        return ""
    # Pull each template variable's value from its row cell.
    pairs = []
    for var, ci in sorted(template_cols.items()):
        if ci < len(row):
            v = row[ci].text.strip()
            if v:
                pairs.append(f"{var}={v}")
    if not pairs:
        return ""
    vars_str = ", ".join(pairs)
    # Drop the trailing "(1)" or "(2)" from the scaffold name (it's redundant
    # with the code) but keep the chemistry parts.
    scaffold_clean = re.sub(r"\s*\(\s*\d+\s*\)\s*$", "", scaffold)
    return f"{code} - {scaffold_clean} ({vars_str})"


# ---------------------------------------------------------------------------
# find_candidates
# ---------------------------------------------------------------------------

def find_candidates(article) -> list[dict]:
    """Enumerate every property-relevant mention in the article.

    Returns a list of candidate dicts per § 8a contract.
    """
    tr = triggers()
    para_re = _compile_trigger_regex(tr.paragraph)
    excl_re = _compile_trigger_regex(tr.exclusion)

    candidates: list[dict] = []
    next_id = 0

    def make_id() -> str:
        nonlocal next_id
        cid = f"{article.article_id}__c{next_id:05d}"
        next_id += 1
        return cid

    # ------- 1. Section-paragraph scan (NXML) -------
    for sec in article.sections:
        section_path = " > ".join(sec.heading_path) or "(root)"
        # The deepest section heading often contains the compound name
        # itself (e.g., NXML structures each compound as its own <sec>
        # whose <title> is the compound name). Use this as a fallback
        # handle when the paragraph text doesn't include the name.
        deepest_heading = sec.heading_path[-1] if sec.heading_path else ""
        for p_idx, para in enumerate(sec.paragraphs):
            for m in para_re.finditer(para):
                trigger_text = m.group(0)
                if _is_excluded(para, m.start(), m.end(), excl_re):
                    continue
                value_text, unit, rel, val_pos = _next_value_after(
                    para, m.end(), window=80)
                if not value_text:
                    continue
                if unit is None:
                    continue
                # Try paragraph-local handle first; if empty, fall back
                # to the deepest section heading.
                handle_text, handle_pos = _find_compound_handle(
                    para, m.start())
                source_type = "paragraph"
                if not handle_text and deepest_heading:
                    handle_text = deepest_heading
                    handle_pos = 0
                    source_type = "paragraph_section_heading"
                candidates.append({
                    "candidate_id": make_id(),
                    "raw_value_text": value_text,
                    "unit_text": unit,
                    "relation_hint": rel,
                    "nearby_compound_handle": handle_text,
                    "compound_handle_position": handle_pos,
                    "property_trigger": trigger_text,
                    "source_type": source_type,
                    "evidence_location": f"section: {section_path}; para#{p_idx}",
                })

    # ------- 2. NXML table scan -------
    # Two layouts are handled:
    #   Pattern A: property trigger lives in a COLUMN HEADER (e.g., "Mp (°C)").
    #              For each row, the cell in that column is a candidate.
    #   Pattern B: property trigger lives in the FIRST COLUMN of a ROW
    #              (e.g., row 0 = "Tb" "K" "794.469" ...). The remaining
    #              cells in that row are candidates.
    # Compile a word-bounded header-trigger regex once. Substring matching
    # on header text was too loose ('Comp.' falsely matched 'mp').
    _header_trigger_re = _compile_trigger_regex(tr.table_headers)

    for t in article.tables:
        # ---- Pattern A: header-column trigger ----
        trigger_cols: dict[int, str] = {}  # col_index -> trigger matched
        for ci, hdr in enumerate(t.headers):
            if excl_re.search(hdr):
                continue
            tm = _header_trigger_re.search(hdr)
            if tm:
                trigger_cols[ci] = tm.group(0)

        if trigger_cols:
            # Detect template-variable columns (X, R, etc.) in this table.
            # Convention: a column header that is exactly "X" or "R" (or a
            # short variable token) identifies a substituent column whose
            # value varies per row.
            template_cols: dict[str, int] = {}
            for ci, hdr in enumerate(t.headers):
                core = hdr.strip()
                if re.fullmatch(r"[A-Z]\d?", core) and core not in {"H", "S", "N", "C", "O", "P", "F", "Cl", "Br", "I"}:
                    # Single uppercase letter that isn't an element/atom symbol
                    template_cols[core] = ci
            # Parse the table caption for scaffold names like "X (1) and Y (2)"
            series_scaffolds = _parse_caption_scaffolds(t.caption)
            for r_idx, row in enumerate(t.rows):
                if not row:
                    continue
                handle_cell = row[0].text if row else ""
                # If template cols exist, build a richer handle with the
                # row's X/R values + the matched series scaffold.
                rich_handle = _build_template_handle(
                    handle_cell, row, template_cols, series_scaffolds)
                effective_handle = rich_handle or handle_cell
                for col_idx, hint in trigger_cols.items():
                    if col_idx >= len(row):
                        continue
                    cell_text = row[col_idx].text
                    if not cell_text:
                        continue
                    stripped = cell_text.strip().strip("-—–").strip()
                    if not stripped or stripped.lower() in {"na", "n/a", "—", "–", "-"}:
                        continue
                    vm = _VALUE_RE.search(cell_text)
                    if not vm:
                        continue
                    value_text = _sanity_check_range(vm.group("num").strip())
                    unit_raw = vm.group("unit")
                    unit = unit_raw.replace(" ", "") if unit_raw else None
                    rel = (vm.group("rel") or "=").strip()
                    if rel == "≈": rel = "~"
                    if not rel: rel = "="
                    if unit is None:
                        hdr = t.headers[col_idx] if col_idx < len(t.headers) else ""
                        hum = re.search(r"°\s*C|°\s*F|\bK\b|\bC\b|\bF\b", hdr)
                        if hum:
                            unit = hum.group(0).replace(" ", "")
                    candidates.append({
                        "candidate_id": make_id(),
                        "raw_value_text": value_text,
                        "unit_text": unit,
                        "relation_hint": rel,
                        "nearby_compound_handle": effective_handle,
                        "compound_handle_position": 0,
                        "property_trigger": hint,
                        "source_type": "table",
                        "evidence_location": (
                            f"table: {t.label}; row#{r_idx}; "
                            f"col#{col_idx} ({t.headers[col_idx]}); "
                            f"row_handle='{handle_cell}'"
                        ),
                    })

        # ---- Pattern B: first-column property trigger ----
        # Compile per-row trigger regex once
        first_col_trigger_re = _compile_trigger_regex(tr.table_headers)
        for r_idx, row in enumerate(t.rows):
            if not row:
                continue
            first_cell = row[0].text
            if not first_cell:
                continue
            # Trigger must match the first cell directly
            tm = first_col_trigger_re.search(first_cell)
            if not tm:
                continue
            # Exclude rows where exclusion triggers also appear (e.g., 'Tg')
            if excl_re.search(first_cell):
                continue
            hint = tm.group(0)
            # The remaining cells are candidate values. The "compound
            # handle" is the table's header row text at that column
            # (typically the compound name when tables are method-vs-compound
            # matrices). If no compound name found in headers, fall back to
            # the table label.
            for col_idx in range(1, len(row)):
                cell_text = row[col_idx].text
                if not cell_text:
                    continue
                stripped = cell_text.strip().strip("-—–").strip()
                if not stripped or stripped.lower() in {"na", "n/a", "—", "–", "-"}:
                    continue
                # Skip cells that are pure unit annotations like "[K]"
                if re.fullmatch(r"\[?\s*[A-Za-z°]+\s*\]?", stripped):
                    continue
                vm = _VALUE_RE.search(cell_text)
                if not vm:
                    continue
                value_text = vm.group("num").strip()
                # Check this is a number, not a column index or order
                try:
                    float(value_text.split("-")[0].replace("−", "-"))
                except ValueError:
                    continue
                unit_raw = vm.group("unit")
                unit = unit_raw.replace(" ", "") if unit_raw else None
                rel = (vm.group("rel") or "=").strip()
                if rel == "≈": rel = "~"
                if not rel: rel = "="
                # The unit hint may come from a unit cell in the same row
                # (cell at col_idx-1 or col_idx+1 may be "[K]" etc.)
                if unit is None:
                    for adj_col in (col_idx - 1, col_idx + 1):
                        if 0 <= adj_col < len(row):
                            adj_text = row[adj_col].text
                            um = re.search(r"°\s*C|°\s*F|\bK\b", adj_text)
                            if um:
                                unit = um.group(0).replace(" ", "")
                                break
                # Compound handle: try to use the table column header at col_idx
                # (e.g., "Baricitinib", "Camostat"); fall back to table label
                handle = (t.headers[col_idx]
                          if col_idx < len(t.headers) else "") or t.label
                candidates.append({
                    "candidate_id": make_id(),
                    "raw_value_text": value_text,
                    "unit_text": unit,
                    "relation_hint": rel,
                    "nearby_compound_handle": handle,
                    "compound_handle_position": 0,
                    "property_trigger": hint,
                    "source_type": "table_first_col_trigger",
                    "evidence_location": (
                        f"table: {t.label}; row#{r_idx}; col#{col_idx}; "
                        f"first_col='{first_cell[:40]}'; col_header='{handle[:40]}'"
                    ),
                })

    # ------- 3. PDF table scan (column-aligned text from -layout mode) -------
    # For loose PDFs where NXML is absent, scan the full text looking for
    # header lines that contain property triggers and align data lines
    # below by character column.
    if not article.tables and article.full_text:
        candidates.extend(_pdf_table_candidates(article, para_re, excl_re, tr,
                                                 starting_id=next_id))
        # Re-sync next_id after pdf table scan
        next_id += sum(1 for c in candidates
                       if c["source_type"] in ("pdf_table", "pdf_paragraph"))

    # ------- 4. Full-text paragraph fallback -------
    # Runs when (a) loose-PDF (no NXML sections), OR (b) NXML sections
    # are sparse / didn't yield many candidates relative to the article's
    # textual length. Catches inline mp values that live in article_text.txt
    # but weren't structured into NXML <sec><p> elements (paper 138).
    nxml_para_candidates = sum(
        1 for c in candidates if c["source_type"] in
        ("paragraph", "paragraph_section_heading"))
    article_text_length = len(article.full_text or "")
    needs_fulltext_fallback = (
        (not article.sections and article.full_text and not article.tables)
        # Heuristic: NXML produced very few paragraph candidates for an
        # article with substantial text (≥40k chars) — likely article_text
        # has content the NXML doesn't structure.
        or (article_text_length >= 40_000 and nxml_para_candidates < 5)
    )
    if needs_fulltext_fallback and article.full_text:
        already_seen_pos: set[int] = set()
        # Avoid re-emitting candidates we already found via PDF table scan
        for c in candidates:
            if c["source_type"] == "pdf_table":
                # Record approximate position to skip duplicates
                # The evidence_location for pdf_table includes the data line
                # but not the position; skip dedup for now
                pass
        for m in para_re.finditer(article.full_text):
            trigger_text = m.group(0)
            if _is_excluded(article.full_text, m.start(), m.end(), excl_re):
                continue
            value_text, unit, rel, val_pos = _next_value_after(
                article.full_text, m.end(), window=80)
            if not value_text or unit is None:
                continue
            handle_text, handle_pos = _find_compound_handle(
                article.full_text, m.start())
            candidates.append({
                "candidate_id": make_id(),
                "raw_value_text": value_text,
                "unit_text": unit,
                "relation_hint": rel,
                "nearby_compound_handle": handle_text,
                "compound_handle_position": handle_pos,
                "property_trigger": trigger_text,
                "source_type": "pdf_paragraph",
                "evidence_location": (
                    f"pdf_text_offset: {m.start()}"
                ),
            })

    return candidates


# ---------------------------------------------------------------------------
# PDF table candidates (column-aligned heuristic)
# ---------------------------------------------------------------------------

def _pdf_table_candidates(article, para_re: re.Pattern,
                          excl_re: re.Pattern, tr: _Triggers,
                          starting_id: int) -> list[dict]:
    """Detect column-aligned tables in PDF -layout text.

    Heuristic:
      1. Find lines that contain >=2 property trigger occurrences.
         Treat them as header lines.
      2. Record column positions of each trigger in the header.
      3. For lines following the header (until a blank line cluster),
         check if numeric tokens align with header columns.
      4. Emit a candidate for each (row, trigger-column) pair.
    """
    next_id = starting_id
    candidates: list[dict] = []
    full_text = article.full_text
    lines = full_text.splitlines()

    # Mark header lines: those with >=2 trigger occurrences AND containing
    # a property-keyword like "exp." or "(exp" or "experimental"
    headers: list[tuple[int, dict[int, str]]] = []  # (line_idx, col_pos->trigger)
    for li, line in enumerate(lines):
        # Quick reject: must be non-trivial length
        if len(line) < 20:
            continue
        # Find all trigger occurrences in the line and record col positions
        trigger_cols: dict[int, str] = {}
        for m in para_re.finditer(line):
            trigger_cols[m.start()] = m.group(0)
        if len(trigger_cols) >= 2:
            headers.append((li, trigger_cols))

    # For each header, walk down through following lines collecting data rows
    for hdr_idx, (hi, hdr_cols) in enumerate(headers):
        # Stop at next header or after 200 lines
        next_hdr = headers[hdr_idx + 1][0] if hdr_idx + 1 < len(headers) else len(lines)
        max_end = min(hi + 500, next_hdr)
        blank_streak = 0
        for li in range(hi + 1, max_end):
            line = lines[li]
            if not line.strip():
                blank_streak += 1
                if blank_streak >= 3:
                    break
                continue
            blank_streak = 0
            # Find numeric tokens with their column positions
            num_iter = re.finditer(
                r"(?<!\w)([-−]?\d+(?:\.\d+)?(?:\s*[-–−]\s*[-−]?\d+(?:\.\d+)?)?)\b",
                line
            )
            row_numbers = [(nm.start(), nm.group(1).strip()) for nm in num_iter]
            if len(row_numbers) < 2:
                continue
            # First non-numeric tokens at start of line as compound handle
            # Take the text up to the first numeric token
            first_num_start = row_numbers[0][0]
            handle_text = line[:first_num_start].strip()
            if not handle_text:
                continue
            # For each header trigger column, find the closest number
            for col_pos, hint in hdr_cols.items():
                # Find nearest numeric token by col position (within ±10 chars)
                nearest = None
                for npos, ntext in row_numbers:
                    if abs(npos - col_pos) <= 12:
                        if nearest is None or abs(npos - col_pos) < abs(nearest[0] - col_pos):
                            nearest = (npos, ntext)
                if not nearest:
                    continue
                npos, ntext = nearest
                # Try to find a unit token near the number; otherwise assume
                # unit lives in header (e.g., "(°C)" or "(K)")
                unit = None
                after = line[npos + len(ntext): npos + len(ntext) + 6]
                um = re.search(r"°\s*C|°\s*F|\bK\b", after)
                if um:
                    unit = um.group(0).replace(" ", "")
                # If still no unit, check header context around col_pos
                if unit is None:
                    hdr_line = lines[hi]
                    around = hdr_line[max(0, col_pos - 10): col_pos + 40]
                    hm = re.search(r"°\s*C|°\s*F|\bK\b", around)
                    if hm:
                        unit = hm.group(0).replace(" ", "")
                # If still no unit, default to °C for the mp_bp adapter
                # (most papers in this domain default to Celsius). The
                # data_origin/classification gate can re-flag if wrong.
                if unit is None:
                    unit = "°C"
                cid = f"{article.article_id}__c{next_id:05d}"
                next_id += 1
                candidates.append({
                    "candidate_id": cid,
                    "raw_value_text": ntext,
                    "unit_text": unit,
                    "relation_hint": "=",
                    "nearby_compound_handle": handle_text,
                    "compound_handle_position": 0,
                    "property_trigger": hint,
                    "source_type": "pdf_table",
                    "evidence_location": (
                        f"pdf_table; header_line={hi}; "
                        f"data_line={li}; col_pos={col_pos}; "
                        f"row_handle='{handle_text[:60]}'"
                    ),
                })

    return candidates


# ---------------------------------------------------------------------------
# Phase 4 — parse_value (Gate D)
# ---------------------------------------------------------------------------

# Accepted units → normalization form (without the degree-symbol space)
_UNIT_NORM = {
    "°C": "°C", "°c": "°C", "C": "°C",
    "K": "K", "k": "K",
    "°F": "°F", "°f": "°F", "F": "°F",
}


def _convert_to_canonical(value: float, unit: str) -> float:
    """Convert (value, unit) to °C (the adapter's canonical_unit)."""
    if unit == "K":
        return value - 273.15
    if unit == "°F":
        return (value - 32) * 5.0 / 9.0
    return value  # °C or empty


def parse_value(raw_value_text: str, unit_text: str | None,
                adapter_context: dict | None = None) -> dict:
    """Convert a raw printed value + unit into the structured value fields.

    Returns:
      {
        "value_type":            "numeric",
        "value_canonical":       float (°C, midpoint of range, boundary for >X),
        "value_canonical_min":   float | None,
        "value_canonical_max":   float | None,
        "value_text":            None (numeric properties don't use this),
        "value_original":        the original printed text (cleaned),
        "unit_original":         the printed unit, normalized to "°C"/"K"/"°F"
        "relation":              "=", ">", "<", "~", etc.
        "parse_warnings":        list of strings
      }

    Raises ValueError if the text cannot be parsed as a numeric value.
    """
    if raw_value_text is None or raw_value_text == "":
        raise ValueError("empty value text")

    warnings: list[str] = []
    txt = unicodedata_safe_strip(raw_value_text)

    # Identify the relation prefix, if any
    relation = "="
    rel_m = re.match(r"^\s*([<>=≥≤~≈]|[<>=]\s*=)\s*", txt)
    if rel_m:
        rel_char = rel_m.group(1).strip()
        # Normalize approximate symbols to "~"
        if rel_char in ("≈", "~"):
            relation = "~"
        elif rel_char == "≥":
            relation = "≥"
        elif rel_char == "≤":
            relation = "≤"
        elif rel_char in (">", ">="):
            relation = ">"
        elif rel_char in ("<", "<="):
            relation = "<"
        txt = txt[rel_m.end():].strip()

    # Normalize Unicode minus to ASCII minus and en-dash to hyphen in numbers
    txt_norm = txt.replace("−", "-").replace("–", "-").replace("—", "-")

    # Try range pattern first: "123-125" or "-94.3-(-90.0)"
    # Accept two numbers separated by a hyphen with optional spaces; the
    # first number may be negative.
    rng_m = re.match(
        r"^(?P<lo>-?\d+(?:\.\d+)?)\s*-\s*(?P<hi>-?\d+(?:\.\d+)?)\s*$",
        txt_norm
    )
    if rng_m:
        lo = float(rng_m.group("lo"))
        hi = float(rng_m.group("hi"))
        if lo > hi:
            warnings.append(f"range_reversed: {lo} > {hi}; swapping")
            lo, hi = hi, lo
        unit_norm = _normalize_unit(unit_text, warnings)
        lo_c = _convert_to_canonical(lo, unit_norm)
        hi_c = _convert_to_canonical(hi, unit_norm)
        return {
            "value_type": "numeric",
            "value_canonical": (lo_c + hi_c) / 2,
            "value_canonical_min": lo_c,
            "value_canonical_max": hi_c,
            "value_text": None,
            "value_original": raw_value_text.strip(),
            "unit_original": unit_norm if unit_norm else "",
            "relation": relation,
            "parse_warnings": warnings,
        }

    # Single value
    single_m = re.match(r"^(?P<n>-?\d+(?:\.\d+)?)\s*$", txt_norm)
    if not single_m:
        raise ValueError(f"unparseable value: {raw_value_text!r}")
    n = float(single_m.group("n"))
    unit_norm = _normalize_unit(unit_text, warnings)
    v_c = _convert_to_canonical(n, unit_norm)
    return {
        "value_type": "numeric",
        "value_canonical": v_c,
        "value_canonical_min": None,
        "value_canonical_max": None,
        "value_text": None,
        "value_original": raw_value_text.strip(),
        "unit_original": unit_norm if unit_norm else "",
        "relation": relation,
        "parse_warnings": warnings,
    }


def unicodedata_safe_strip(s: str) -> str:
    """Strip leading/trailing whitespace, also Unicode forms thereof."""
    return s.strip(" \t\n\r     　")


def _normalize_unit(unit_text: str | None, warnings: list) -> str:
    """Normalize a printed unit to "°C", "K", or "°F". Returns "" if
    not recognized and adds a warning."""
    if not unit_text:
        warnings.append("unit_missing")
        return ""
    u = unit_text.strip().replace(" ", "")
    if u in _UNIT_NORM:
        return _UNIT_NORM[u]
    warnings.append(f"unit_not_recognized:{unit_text!r}")
    return ""


# ---------------------------------------------------------------------------
# Phase 4 — classify (Gate E)
# ---------------------------------------------------------------------------

def classify(candidate: dict, article_context: dict | None = None
             ) -> tuple[str, str, str]:
    """Classify a candidate into (data_origin, property_subtype, instrument).

    `candidate` has the keys produced by find_candidates plus any context
    added during resolution. `article_context` may contain
    `full_text` for nearby-window inspection.
    """
    article_ctx = article_context or {}
    article_text = article_ctx.get("full_text", "") or ""

    # Reload triggers each time would be wasteful — reuse cached load
    tr = triggers()

    # Build a small window of nearby text around the candidate's value
    nearby = _candidate_neighborhood(candidate, article_text)

    # Data origin: order matters — predicted > literature_cited > measured
    data_origin = _classify_origin(candidate, nearby)

    # Property subtype: mp default vs decomp, boil, DSC variants
    subtype = _classify_subtype(candidate, nearby)

    # Instrument: scan for a known instrument string in nearby text
    instrument = _classify_instrument(nearby, tr.instruments)

    return data_origin, subtype, instrument


def _candidate_neighborhood(candidate: dict, article_text: str,
                            window: int = 200) -> str:
    """Return a snippet of text around the candidate's value, used for
    contextual classification. Falls back to evidence_location-derived
    text if no positional anchor is available."""
    # Look for compound_handle_position if it's a real article-text offset
    pos = candidate.get("compound_handle_position", 0)
    if isinstance(pos, int) and pos > 0 and pos < len(article_text):
        start = max(0, pos - window)
        end = min(len(article_text), pos + window)
        return article_text[start:end]
    # Fallback: evidence_location text, if present
    return (candidate.get("evidence_location") or "") + " " + \
           (candidate.get("raw_value_text") or "")


def _classify_origin(candidate: dict, nearby: str) -> str:
    """Decide data_origin = measured_by_article | literature_cited |
    predicted_<method>."""
    nearby_low = nearby.lower()
    trigger = (candidate.get("property_trigger") or "").lower()

    # Check predicted-calculated patterns first (most specific)
    predicted_methods = [
        "strm", "sirm", "asnn", "qspr", "calculated", "predicted",
        "estimated"
    ]
    for method in predicted_methods:
        if method in nearby_low:
            return f"predicted_{method.upper()}"
    # Literature-cited: a citation marker or lit. abbreviation near the value
    if re.search(r"\blit\.?\b|literature\s+value|\bref(?:erence)?\b", nearby_low):
        return "literature_cited"
    if re.search(r"\[\s*\d+\s*\]", nearby):
        return "literature_cited"
    # Default: paper measured it
    return "measured_by_article"


def _classify_subtype(candidate: dict, nearby: str) -> str:
    """Map a candidate to its property_subtype.

    For mp/bp:
      - "(dec)", "(dec.)", "decomp" near a mp → melt_or_decomp
      - "Tb", "boiling" → boil
      - "DSC" + "onset" → DSC_onset; "DSC" + "peak" → DSC_peak
      - Default mp trigger → melt; default bp trigger → boil
    """
    nearby_low = nearby.lower()
    trigger = (candidate.get("property_trigger") or "").lower()

    # Boiling-point family
    if trigger in {"bp", "b.p.", "b.p", "bp.", "boiling point", "tb", "t_b"} \
            or "boiling" in trigger:
        return "boil"

    # Melting-point family default
    # Check for decomposition annotation in the nearby window
    if re.search(r"\(dec\.?\)|\bdecomp(?:osition|osed)?\b", nearby_low):
        return "melt_or_decomp"

    # DSC peak / onset
    if "dsc" in nearby_low:
        if "onset" in nearby_low or "te" in trigger.lower():
            return "DSC_onset"
        if "peak" in nearby_low:
            return "DSC_peak"

    # Sublimation
    if "sublim" in nearby_low:
        return "sublimation"

    return "melt"


def _classify_instrument(nearby: str, instruments: list[str]) -> str:
    """Scan nearby for any known instrument name. Falls back to 'unk'."""
    for inst in instruments:
        if inst.lower() in nearby.lower():
            # Special-case: "DSC" alone is preferred when present
            if inst.lower() == "dsc":
                return "DSC"
            return inst
    return "unk"

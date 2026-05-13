#!/usr/bin/env python3
"""Evidence-locked mp/bp extraction for the local mp_bp_full_set corpus.

The script intentionally reads only INPUT_ROOT and writes only OUTPUT_DIR.
It favors exact source snippets over broad recall: every emitted row has a
source_file and an evidence_quote copied from text actually read from disk.
"""

from __future__ import annotations

import csv
import html
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from lxml import etree, html as lxml_html
except Exception:  # pragma: no cover - fallback for system python
    etree = None
    lxml_html = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


WORKSPACE = Path("/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev")
INPUT_ROOT = WORKSPACE / "mp_bp_full_set"
OUTPUT_DIR = WORKSPACE / "Trial1-full-gpt55_high"
OUT_CSV = OUTPUT_DIR / "mp_bp_extracted.csv"
SKIPPED_CSV = OUTPUT_DIR / "skipped_sources.csv"

COLUMNS = [
    "id",
    "verification_status",
    "compound_name",
    "compound_smiles",
    "property",
    "value_celsius",
    "value_celsius_min",
    "value_celsius_max",
    "value_raw",
    "relation",
    "data_type",
    "source",
    "source_url",
    "evidence_location",
    "evidence_quote",
    "conversion_arithmetic",
    "notes",
    "source_file",
]

PROPERTY_RE = re.compile(
    r"(?P<label>"
    r"\b(?:m\.?\s*p\.?|mp|melting\s+points?|melting\s+range|melting\s+temperature|mpt)\b"
    r"|\b(?:b\.?\s*p\.?|bp|boiling\s+points?|boiling\s+temperature)\b"
    r"|\b(?:decomp(?:osition)?|dec\.)\b"
    r"|\b(?:sublim(?:ation|ed)?)\b"
    r"|\b(?:DSC\s+onset|DSC\s+peak)\b"
    r")"
    r"\s*(?:\([^)]{0,40}\))?\s*(?:[:=]|was|is|at|of)?\s*"
    r"(?P<rel>[<>~≈]?)\s*"
    r"(?P<val>[−-]?\d+(?:\.\d+)?(?:\s*(?:-|–|—|to)\s*[−-]?\d+(?:\.\d+)?)?)"
    r"\s*(?P<unit>°\s*C|º\s*C|℃|o\s*C|deg\.?\s*C|degrees?\s*C|C\b|K\b|°\s*F|º\s*F|F\b)?",
    re.IGNORECASE,
)

TABLE_HEADER_RE = re.compile(
    r"(?:M\.?\s*p\.?|m\.?\s*p\.?|mp|melting\s+point)\s*\(?\s*(?:°|o)?\s*C\s*\)?",
    re.IGNORECASE,
)

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
PMC_RE = re.compile(r"\bPMC\d{4,9}\b", re.IGNORECASE)
PMID_RE = re.compile(r"\bPMID:?\s*(\d{5,10})\b", re.IGNORECASE)
ARTICLE_DOI_RE = re.compile(
    r"<article-id[^>]+pub-id-type=[\"']doi[\"'][^>]*>\s*([^<\s]+)",
    re.IGNORECASE,
)

BAD_CONTEXT = re.compile(
    r"(reaction|reflux|incubat|storage|room temperature|temperature should|"
    r"solvent|column|concentration|assay|growth|culture|crystal data|"
    r"reflections|scan type|bioassay|activity|inhibition|IC\s*50|MIC|"
    r"MP-500D|Downloaded from|Wiley Online Library|\bBP\s+17\b)",
    re.IGNORECASE,
)

GOOD_CONTEXT = re.compile(
    r"(yield|solid|powder|crystal|oil|needles|m\.?\s*p\.?|mp:|melting|"
    r"boiling|IR|NMR|MS|Anal\.|Calcd|Found|recrystall|DSC|TGA|decomp)",
    re.IGNORECASE,
)

NAME_STOP = re.compile(
    r"\b(?:IR|FTIR|NMR|MS|Anal|Calculated|Calcd|found|yield|white|yellow|"
    r"green|brown|orange|red|colorless|solid|powder|crystal|oil)\b",
    re.IGNORECASE,
)

GENERIC_NAMES = {
    "resulting",
    "obtained",
    "measured",
    "literature",
    "observed",
    "physical state",
    "characteristic",
    "with the",
    "as for the",
    "one of the first reported dess was a mixture of choline chloride",
    "title co",
    "it has a",
    "predicted versus observed",
    "cns drugs",
    "when β = 5 k min −1, the mass change measured at the closure of the",
    "melting point (",
    "separated crystals were filtered off, washed with cold water, dried and crystallized from acoh",
}


@dataclass
class SourceDoc:
    key: str
    source_file: Path
    text: str
    metadata: dict
    standard_layout: bool


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def clean_text(s: str) -> str:
    s = html.unescape(s or "")
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\u00a0", " ")
    s = s.replace("° C", "°C").replace("º C", "°C")
    s = re.sub(r"[\t\r\n]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}


def html_to_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if lxml_html is None:
        return clean_text(re.sub(r"<[^>]+>", " ", raw))
    doc = lxml_html.fromstring(raw)
    etree.strip_elements(doc, "script", "style", with_tail=False)
    return clean_text(doc.text_content())


def nxml_to_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if etree is None:
        return clean_text(re.sub(r"<[^>]+>", " ", raw))
    parser = etree.XMLParser(recover=True, huge_tree=True)
    root = etree.fromstring(raw.encode("utf-8", errors="replace"), parser=parser)
    return clean_text(" ".join(root.itertext()))


def pdf_to_text(path: Path) -> str:
    if PdfReader is not None:
        try:
            reader = PdfReader(str(path))
            parts = []
            for page in reader.pages:
                try:
                    parts.append(page.extract_text() or "")
                except Exception:
                    parts.append("")
            text = clean_text(" ".join(parts))
            if len(text) > 200:
                return text
        except Exception:
            pass
    try:
        out = subprocess.run(
            ["strings", str(path)], capture_output=True, text=True, timeout=60
        )
        if out.returncode == 0:
            return clean_text(out.stdout)
    except Exception:
        pass
    return ""


def source_docs() -> Iterable[SourceDoc]:
    for child in sorted(INPUT_ROOT.iterdir()):
        if child.name.startswith("."):
            continue
        if child.is_dir() and (child / "article_text.txt").exists():
            meta = read_json(child / "metadata.json")
            text = (child / "article_text.txt").read_text(
                encoding="utf-8", errors="replace"
            )
            yield SourceDoc(child.name, child / "article_text.txt", clean_text(text), meta, True)
        elif child.is_dir():
            for f in sorted(child.iterdir()):
                if f.name.startswith(".") or f.name == "_meta.csv":
                    continue
                if f.suffix.lower() == ".html":
                    yield SourceDoc(f"{child.name}/{f.name}", f, html_to_text(f), {}, False)
                elif f.suffix.lower() == ".pdf":
                    yield SourceDoc(f"{child.name}/{f.name}", f, pdf_to_text(f), {}, False)
                elif f.suffix.lower() in {".txt", ".nxml", ".xml"}:
                    text = nxml_to_text(f) if f.suffix.lower() in {".nxml", ".xml"} else f.read_text(encoding="utf-8", errors="replace")
                    yield SourceDoc(f"{child.name}/{f.name}", f, clean_text(text), {}, False)
        elif child.suffix.lower() == ".pdf":
            yield SourceDoc(child.name, child, pdf_to_text(child), {}, False)
        elif child.suffix.lower() == ".html":
            yield SourceDoc(child.name, child, html_to_text(child), {}, False)


def citation(doc: SourceDoc) -> tuple[str, str]:
    meta = doc.metadata
    text = doc.text[:5000]
    doi = (meta.get("doi") or "").strip()
    if not doi:
        nxml = doc.source_file.parent / "article.nxml"
        if doc.standard_layout and nxml.exists():
            raw = nxml.read_text(encoding="utf-8", errors="replace")[:20000]
            am = ARTICLE_DOI_RE.search(raw)
            if am:
                doi = html.unescape(am.group(1)).rstrip(".,);")
        if not doi:
            # Skip journal-level DOI identifiers such as 10.1002/(ISSN)...
            for m in DOI_RE.finditer(text):
                candidate = m.group(0).rstrip(".,);")
                if "(ISSN)" not in candidate.upper() and "/B978-" not in candidate.upper():
                    doi = candidate
                    break
    if doi and doc.standard_layout:
        source_url = f"https://doi.org/{doi}"
    elif doc.standard_layout and (meta.get("pmcid") or PMC_RE.search(text)):
        pmc = meta.get("pmcid") or PMC_RE.search(text).group(0).upper()
        source_url = f"pmc:{pmc}"
    elif doc.standard_layout and (meta.get("pmid") or PMID_RE.search(text)):
        pmid = meta.get("pmid") or PMID_RE.search(text).group(1)
        source_url = f"pmid:{pmid}"
    else:
        source_url = "legacy:" + doc.source_file.relative_to(INPUT_ROOT).as_posix()

    src = (meta.get("citation") or "").strip()
    if not src:
        title = (meta.get("title") or "").strip()
        if not title:
            title = doc.source_file.stem
            title = re.sub(r"^\d{4}[_ -]+", "", title)
            title = re.sub(r"^[A-Z][A-Za-z]+[_ -]+", "", title)
            title = title.replace("_", " ")
        year = meta.get("pub_year") or ""
        src = f"{title} {year}".strip()
    return src, source_url


def property_from_label(label: str) -> str:
    l = label.lower()
    if "boil" in l or re.match(r"b\.?\s*p\.?|bp", l):
        return "boiling_point"
    if "dsc onset" in l:
        return "DSC_onset"
    if "dsc peak" in l:
        return "DSC_peak"
    if "decomp" in l or l.startswith("dec"):
        return "decomposition"
    if "sublim" in l:
        return "sublimation"
    return "melting_point"


def value_parts(raw_num: str, unit: str) -> tuple[float, str, str, str, str]:
    unit_clean = normalize(unit or "°C").replace(" ", "")
    s = normalize(raw_num)
    nums: list[float] = []
    display_num = s
    rm = re.match(
        r"^\s*([+-]?\d+(?:\.\d+)?)\s*(?:-|to)\s*([+-]?\d+(?:\.\d+)?)\s*$",
        s,
        re.IGNORECASE,
    )
    if rm:
        lo0 = float(rm.group(1))
        hi0 = float(rm.group(2))
        # Abbreviated ranges like 175-6 mean 175-176, not 175 to 6.
        if hi0 >= 0 and lo0 >= 100 and hi0 < lo0 and hi0 < 100:
            hi_digits = len(str(int(hi0)))
            scale = 10 ** hi_digits
            hi0 = math.floor(lo0 / scale) * scale + hi0
            if hi0 < lo0:
                hi0 += scale
            display_num = f"{lo0:g}-{hi0:g}"
        nums = [lo0, hi0]
    else:
        nums = [float(x) for x in re.findall(r"[+-]?\d+(?:\.\d+)?", s)]
    if not nums:
        raise ValueError(raw_num)
    lo = hi = nums[0]
    if len(nums) >= 2:
        lo, hi = nums[0], nums[1]
    mid = (lo + hi) / 2.0
    conversion = ""
    if unit_clean.upper() == "K":
        conversion = f"{mid:g} K - 273.15 = {mid - 273.15:.2f} °C"
        lo_c = lo - 273.15
        hi_c = hi - 273.15
    elif unit_clean.upper() in {"°F", "ºF", "F"}:
        conversion = f"({mid:g} °F - 32) * 5/9 = {(mid - 32) * 5 / 9:.2f} °C"
        lo_c = (lo - 32) * 5 / 9
        hi_c = (hi - 32) * 5 / 9
    else:
        lo_c, hi_c = lo, hi
    value_c = (lo_c + hi_c) / 2.0
    if len(nums) >= 2:
        return value_c, f"{lo_c:.2f}".rstrip("0").rstrip("."), f"{hi_c:.2f}".rstrip("0").rstrip("."), conversion, display_num
    return value_c, "", "", conversion, display_num


def evidence_snippet(text: str, start: int, end: int) -> str:
    left = max(0, start - 360)
    right = min(len(text), end + 520)
    snippet = text[left:right]
    # Trim to a useful semicolon- or sentence-like boundary while preserving exact text.
    before = max(snippet.rfind(". ", 0, start - left), snippet.rfind("; ", 0, start - left))
    if before > 80:
        snippet = snippet[before + 2 :]
        left += before + 2
    after_candidates = [p for p in (snippet.find("; ", end - left), snippet.find(". ", end - left)) if p != -1]
    if after_candidates:
        cut = min(after_candidates)
        if cut > 60:
            snippet = snippet[: cut + 1]
    return clean_text(snippet)


def extract_name_from_context(context: str, prop_start: int) -> str:
    lead = context.strip(" ;,.")
    lead_match = re.match(
        r"^(?:\d+(?:\.\d+)*\s+)?(?P<name>[A-Z0-9][^.;:]{8,260}?\([A-Za-z]?\d+[A-Za-z]?\))\s+"
        r"(?:The general procedure|General procedure|A mixture|A solution|Using|Reacting|"
        r"White|Yellow|Pale|Brown|Orange|Red|Colorless|Yield|was|were|prepared|obtained)",
        lead,
        re.IGNORECASE,
    )
    if lead_match:
        return normalize_name(lead_match.group("name"))

    prefix = context[:prop_start].strip(" ;,.")
    prefix = re.sub(r"^(?:\d+(?:\.\d+)*\s+)+", "", prefix)
    prefix = re.split(
        r"\b(?:The general procedure|General procedure|A mixture|A solution|Reacting)\b",
        prefix,
        flags=re.IGNORECASE,
    )[0].strip(" ;,.") or prefix
    # Prefer a name followed by a compound code immediately before the property.
    code_match = list(re.finditer(r"([A-Z0-9][^.;:]{8,260}?)\s*\(([A-Za-z]?\d+[A-Za-z]?)\)\s*(?:[,;:]?\s*(?:as\s+)?(?:a\s+)?)?$", prefix))
    if code_match:
        name = code_match[-1].group(1).strip()
        code = code_match[-1].group(2)
        name = NAME_STOP.split(name)[0].strip(" ;,.")
        if code.lower() not in name.lower():
            name = f"{name} ({code})"
        return normalize_name(name)
    # Otherwise take the phrase after the previous sentence boundary.
    tail = re.split(r"(?:\.\s+|;|\bExperimental\b|\bGeneral procedure\b)", prefix)[-1]
    tail = NAME_STOP.split(tail)[0]
    return normalize_name(tail)


def normalize_name(name: str) -> str:
    name = clean_text(name)
    name = re.sub(r"^S\d+\s+", "", name)
    name = re.sub(r"^\d+(?:\.\d+)*\s+", "", name)
    name = re.sub(r"^(?:and|the|compound|compounds?|synthesis of|preparation of)\s+", "", name, flags=re.I)
    name = re.split(
        r"\b(?:The general procedure|General procedure|A mixture|A solution|Reacting|Using|Title compound|According to)\b",
        name,
        flags=re.IGNORECASE,
    )[0]
    name = re.split(r"\s+C\d+\s*H\d+", name, flags=re.IGNORECASE)[0]
    name = re.sub(r"(\([A-Za-z]?\d+[A-Za-z]?\))\s*\d+(?:,\d+)?$", r"\1", name)
    name = name.strip(" ,;:.")
    name = re.sub(r"\s+", " ", name)
    return name


def plausible_name(name: str) -> bool:
    low = name.lower().strip(" :;,.")
    if low in GENERIC_NAMES:
        return False
    if low.startswith((
        "resulting ",
        "obtained ",
        "measured ",
        "observed ",
        "literature ",
        "using a ",
        "it has a ",
        "predicted versus observed",
        "as a result",
        "when the nve simulation",
        "when β",
        "cns drugs",
        "after ",
        "flash chromatography",
        "usual work-up",
        "raw product",
        "crude product",
        "organic layer",
        "mixture was concentrated",
        "this residue",
        "residue ",
        "solvent was then removed",
        "after cooling",
        "second polymorph",
        "a sharp endotherm",
        "gw-1 polymorph",
        "regarding gw-3",
        "elbelghiti",
        "oulay slimane",
        "touzani",
        "f sciences",
        "[142]",
        "abra-",
        "then, hc",
    )):
        return False
    if len(name) < 8 or len(name) > 320:
        return False
    if re.fullmatch(r"(?:compound|complex|derivative)?\s*[A-Za-z]?\d+[A-Za-z]?", name, re.I):
        return False
    if re.search(r"\b(?:yield|nmr|ir|ms|calcd|found|table|figure|scheme|reaction|procedure)\b", name, re.I):
        return False
    if len(re.findall(r"[A-Za-z]", name)) < 6:
        return False
    return True


def extract_inline_rows(doc: SourceDoc) -> list[dict]:
    rows = []
    source, source_url = citation(doc)
    text = doc.text
    for m in PROPERTY_RE.finditer(text):
        label = m.group("label")
        prop = property_from_label(label)
        snippet = evidence_snippet(text, m.start(), m.end())
        if not GOOD_CONTEXT.search(snippet):
            continue
        if BAD_CONTEXT.search(snippet) and not re.search(r"\b(m\.?\s*p\.?|mp:|melting point|boiling point)\b", snippet, re.I):
            continue
        prop_start_in_snippet = max(0, normalize(snippet[: max(0, m.start() - (m.start() - doc.text.find(snippet[:50])))]).find(normalize(label)))
        prop_pos = snippet.lower().find(label.lower().split()[0].replace("\\", ""))
        name = extract_name_from_context(snippet, prop_pos if prop_pos >= 0 else len(snippet) // 2)
        if not plausible_name(name):
            continue
        unit = m.group("unit") or "°C"
        raw_num = normalize(m.group("rel") + m.group("val")).strip()
        try:
            value_c, vmin, vmax, conv, display_num = value_parts(m.group("val"), unit)
        except ValueError:
            continue
        display_unit = "°C" if re.search(r"(?:°|º|o|deg|degree)?\s*C\b|℃", unit, re.I) else unit
        value_raw = f"{m.group('rel') or ''}{display_num} {display_unit}".strip()
        note = ""
        if display_num != raw_num:
            note = f"source prints abbreviated range as {raw_num} {unit}".strip()
        if not math.isfinite(value_c):
            continue
        relation = m.group("rel") or "="
        rows.append(
            {
                "verification_status": "pending_verification",
                "compound_name": name,
                "compound_smiles": "",
                "property": prop,
                "value_celsius": f"{value_c:.2f}".rstrip("0").rstrip("."),
                "value_celsius_min": vmin,
                "value_celsius_max": vmax,
                "value_raw": value_raw,
                "relation": relation,
                "data_type": "calculated" if re.search(r"\b(predicted|calculated|QSPR|model)\b", snippet, re.I) else "measured",
                "source": source,
                "source_url": source_url,
                "evidence_location": f"{doc.source_file.relative_to(INPUT_ROOT).as_posix()} char {m.start()}",
                "evidence_quote": snippet,
                "conversion_arithmetic": conv,
                "notes": note,
                "source_file": doc.source_file.as_posix(),
            }
        )
    return rows


def dedup(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for r in rows:
        key = (
            r["source_file"],
            normalize(r["compound_name"]).lower(),
            r["property"],
            r["value_raw"],
            normalize(r["evidence_quote"])[:180],
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def verify_quotes(rows: list[dict], docs_by_file: dict[str, SourceDoc]) -> tuple[list[dict], list[dict]]:
    good = []
    bad = []
    for r in rows:
        doc = docs_by_file.get(r["source_file"])
        if not doc:
            r["verification_status"] = "flagged_review"
            r["notes"] = "flagged_evidence_quote_not_found: source_file unavailable"
            bad.append(r)
            continue
        if normalize(r["evidence_quote"]) not in normalize(doc.text):
            r["verification_status"] = "flagged_review"
            r["notes"] = "flagged_evidence_quote_not_found: quote not found in extracted source text"
            bad.append(r)
            continue
        good.append(r)
    return good, bad


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    docs = list(source_docs())
    docs_by_file = {d.source_file.as_posix(): d for d in docs}
    all_rows = []
    skipped = []
    for doc in docs:
        if len(doc.text) < 200:
            skipped.append(
                {
                    "source_file": doc.source_file.as_posix(),
                    "reason": "flagged_paper_unreadable: no readable text extracted",
                    "bytes_or_chars": len(doc.text),
                }
            )
            continue
        rows = extract_inline_rows(doc)
        if not rows:
            skipped.append(
                {
                    "source_file": doc.source_file.as_posix(),
                    "reason": "no inline mp/bp/decomposition/sublimation values matched conservative extractor",
                    "bytes_or_chars": len(doc.text),
                }
            )
        all_rows.extend(rows)
    all_rows = dedup(all_rows)
    good_rows, bad_rows = verify_quotes(all_rows, docs_by_file)
    final_rows = good_rows + bad_rows
    for i, row in enumerate(final_rows, start=1):
        row["id"] = i
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(final_rows)
    with SKIPPED_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source_file", "reason", "bytes_or_chars"], quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(skipped)
    print(f"read_sources={len(docs)} rows={len(final_rows)} skipped={len(skipped)} out={OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

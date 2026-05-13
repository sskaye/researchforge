"""Phase 1: source ingestion.

Reads a paper's available source files (NXML, plain text, PDF) and returns
a uniform Article object containing:
- sections (with hierarchical headings + paragraph text)
- tables (with column/row headers + structured cells)
- figure / scheme / table captions
- DOI candidates from each available source (returned for verify_doi.py)
- article_id
- full plain text (concatenation of all available sources)

Per § 5 step 2 of merged_skill_proposal.md.

NEVER modifies article files. All reads are read-only.
"""

from __future__ import annotations

import os
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Data classes for the Article object
# ---------------------------------------------------------------------------

@dataclass
class TableCell:
    """A single cell in a table, with row/col indices and the cell text."""
    row: int
    col: int
    text: str


@dataclass
class Table:
    """A parsed table.

    headers_row: list of header strings, one per column (best effort).
    rows: list of lists of TableCell. rows[i][j] is row i, column j.
    """
    table_id: str               # e.g. "Table 1" or "t1-ijms-08-00662"
    label: str                  # e.g. "Table 1"
    caption: str
    headers: list[str] = field(default_factory=list)
    rows: list[list[TableCell]] = field(default_factory=list)


@dataclass
class Section:
    """A section in the article with hierarchical heading path."""
    section_id: str             # XML id or auto-generated
    heading_path: list[str]     # e.g. ["Experimental", "Synthesis", "Compound 4"]
    paragraphs: list[str] = field(default_factory=list)


@dataclass
class DOICandidate:
    """A DOI candidate from one of the precedence sources."""
    doi: str
    source: str                 # one of:
                                # "nxml_front_matter", "pdf_metadata",
                                # "pdf_text_first_2_pages",
                                # "publisher_lookup", "user_metadata"


@dataclass
class Article:
    """A uniform article object produced by ingest_article."""
    article_id: str
    source_kind: str            # "pmc_nxml" | "loose_pdf" | "text_only" | "mixed"
    available_sources: list[str]
    sections: list[Section] = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    captions: list[str] = field(default_factory=list)
    doi_candidates: list[DOICandidate] = field(default_factory=list)
    full_text: str = ""         # whole-article plain text used for substring checks
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def _normalize_text(s: str) -> str:
    """NFC unicode normalization + whitespace collapse.

    Does NOT dehyphenate line breaks — that lives in verify_substring.py
    where it's applied at substring-check time. We preserve raw newlines
    here so that PDF column/page boundaries remain visible to downstream
    consumers if they want them.
    """
    if not s:
        return ""
    s = unicodedata.normalize("NFC", s)
    return s


def _element_text(el: ET.Element) -> str:
    """Concatenate the text of an element and all its descendants, preserving
    significant whitespace.
    """
    parts: list[str] = []
    if el.text:
        parts.append(el.text)
    for child in el:
        parts.append(_element_text(child))
        if child.tail:
            parts.append(child.tail)
    return _normalize_text(re.sub(r"\s+", " ", "".join(parts)).strip())


# ---------------------------------------------------------------------------
# NXML parsing
# ---------------------------------------------------------------------------

def _parse_nxml_doi(root: ET.Element) -> list[DOICandidate]:
    """Find DOI candidates in NXML front matter only.

    Citation-list DOIs (under <back><ref-list>) are explicitly EXCLUDED,
    per § 5 step 2 of the proposal — those are reference DOIs, not THE
    paper's DOI.
    """
    cands: list[DOICandidate] = []
    front = root.find("front")
    if front is None:
        return cands
    for aid in front.iter("article-id"):
        if aid.attrib.get("pub-id-type") == "doi" and aid.text:
            cands.append(DOICandidate(doi=aid.text.strip(),
                                      source="nxml_front_matter"))
    return cands


def _parse_nxml_sections(root: ET.Element) -> list[Section]:
    body = root.find("body")
    sections: list[Section] = []
    if body is None:
        return sections

    def walk(sec: ET.Element, parent_path: list[str]):
        title_el = sec.find("title")
        title = _element_text(title_el) if title_el is not None else ""
        path = parent_path + [title] if title else list(parent_path)
        paragraphs = [_element_text(p) for p in sec.findall("p")]
        if paragraphs or path:
            sections.append(Section(
                section_id=sec.attrib.get("id", "") or f"sec_{len(sections)}",
                heading_path=path,
                paragraphs=paragraphs,
            ))
        # Recurse into nested sections
        for sub in sec.findall("sec"):
            walk(sub, path)

    for sec in body.findall("sec"):
        walk(sec, [])
    return sections


def _expand_thead_to_grid(thead_el: ET.Element) -> list[list[str]]:
    """Expand a <thead> with colspan/rowspan into a 2D grid of cell text.

    Each row of the result is one thead <tr>, with colspans expanded by
    repeating the cell text and rowspans propagating downward.
    """
    raw_rows: list[list[tuple[str, int, int]]] = []
    for tr in thead_el.iter("tr"):
        row: list[tuple[str, int, int]] = []
        for c in tr:
            if c.tag in ("td", "th"):
                text = _element_text(c)
                cs = int(c.attrib.get("colspan", "1"))
                rs = int(c.attrib.get("rowspan", "1"))
                row.append((text, cs, rs))
        raw_rows.append(row)

    grid: list[list[str]] = []
    pending: dict[int, tuple[str, int]] = {}
    for raw in raw_rows:
        out_row: list[str] = []
        ci = 0
        src_i = 0
        while src_i < len(raw) or pending:
            if ci in pending:
                text, remain = pending[ci]
                out_row.append(text)
                if remain - 1 <= 0:
                    del pending[ci]
                else:
                    pending[ci] = (text, remain - 1)
                ci += 1
                continue
            if src_i >= len(raw):
                break
            text, cs, rs = raw[src_i]
            for _ in range(cs):
                out_row.append(text)
                if rs > 1:
                    pending[ci] = (text, rs - 1)
                ci += 1
            src_i += 1
        grid.append(out_row)
    return grid


def _parse_nxml_tables(root: ET.Element) -> list[Table]:
    """Parse <table-wrap> elements into Table objects with structured cells.

    Handles colspan / rowspan minimally: a colspan=N cell occupies N columns
    of its row (we duplicate the cell text into each). Rowspan support is
    similar — replicate downward across that many rows.
    """
    tables: list[Table] = []
    for tw in root.iter("table-wrap"):
        tw_id = tw.attrib.get("id", f"tw_{len(tables)}")
        label_el = tw.find("label")
        cap_el = tw.find("caption")
        label = _element_text(label_el) if label_el is not None else ""
        caption = _element_text(cap_el) if cap_el is not None else ""

        table_el = tw.find("table")
        if table_el is None:
            tables.append(Table(table_id=tw_id, label=label, caption=caption))
            continue

        # First pass: gather raw cells with span info. Track which rows
        # came from <thead> so we can skip them when building data rows.
        raw_rows: list[list[tuple[str, int, int]]] = []
        thead_row_indices: set[int] = set()

        thead_el = table_el.find("thead")
        if thead_el is not None:
            for tr in thead_el.iter("tr"):
                row: list[tuple[str, int, int]] = []
                for c in tr:
                    if c.tag in ("td", "th"):
                        text = _element_text(c)
                        cs = int(c.attrib.get("colspan", "1"))
                        rs = int(c.attrib.get("rowspan", "1"))
                        row.append((text, cs, rs))
                thead_row_indices.add(len(raw_rows))
                raw_rows.append(row)

        # tbody and any direct <tr> children of <table> become data rows
        for parent in [table_el] + table_el.findall("tbody"):
            for tr in parent.findall("tr"):
                row = []
                for c in tr:
                    if c.tag in ("td", "th"):
                        text = _element_text(c)
                        cs = int(c.attrib.get("colspan", "1"))
                        rs = int(c.attrib.get("rowspan", "1"))
                        row.append((text, cs, rs))
                raw_rows.append(row)

        # Second pass: build a 2D grid expanding spans
        grid: list[list[str]] = []
        # pending_rowspans[col] = (text, remaining_rows)
        pending: dict[int, tuple[str, int]] = {}
        for raw in raw_rows:
            out_row: list[str] = []
            ci = 0
            src_i = 0
            while src_i < len(raw) or pending:
                # If a previous row span is still occupying this column, fill it
                if ci in pending:
                    text, remain = pending[ci]
                    out_row.append(text)
                    if remain - 1 <= 0:
                        del pending[ci]
                    else:
                        pending[ci] = (text, remain - 1)
                    ci += 1
                    continue
                if src_i >= len(raw):
                    break
                text, cs, rs = raw[src_i]
                for _ in range(cs):
                    out_row.append(text)
                    if rs > 1:
                        pending[ci] = (text, rs - 1)
                    ci += 1
                src_i += 1
            # If pending occupies trailing columns after raw is exhausted
            while pending and max(pending.keys()) >= len(out_row):
                col = len(out_row)
                if col in pending:
                    text, remain = pending[col]
                    out_row.append(text)
                    if remain - 1 <= 0:
                        del pending[col]
                    else:
                        pending[col] = (text, remain - 1)
                else:
                    break
            grid.append(out_row)

        # Identify headers. Multi-row thead is common in chemistry tables:
        # row 1 may say "Elemental analysis (colspan=4)" and row 2 splits
        # that into "C | H | N | S". We expand each thead row into a column
        # grid (using colspan/rowspan), then merge column-by-column: the
        # combined header for column J is the join of each thead row's
        # cell at column J. Empty cells are skipped during merge so a
        # column header like "M.p. (°C)" that only appears in row 1 isn't
        # blanked out by an empty row-2 cell.
        headers: list[str] = []
        if thead_el is not None:
            thead_grid = _expand_thead_to_grid(thead_el)
            if thead_grid:
                ncols = max(len(r) for r in thead_grid)
                merged = []
                for col in range(ncols):
                    parts = []
                    for r in thead_grid:
                        if col < len(r):
                            cell = r[col].strip()
                            if cell and (not parts or cell != parts[-1]):
                                # Drop duplicate column-spanning cells:
                                # "Elemental analysis" appearing 4× via
                                # colspan should not repeat in the merged
                                # header string.
                                parts.append(cell)
                    merged.append(" | ".join(parts))
                headers = merged
        if not headers and grid:
            headers = grid[0]

        # Build Table.rows, skipping any rows that came from <thead>
        # (those have already been used to populate `headers`). If there
        # was no <thead> but we used grid[0] as the headers, skip that
        # row from data.
        data_rows: list[list[TableCell]] = []
        for i, row in enumerate(grid):
            if i in thead_row_indices:
                continue
            if thead_el is None and i == 0 and headers == row:
                continue
            row_cells = [TableCell(row=i, col=j, text=row[j])
                         for j in range(len(row))]
            data_rows.append(row_cells)

        tables.append(Table(
            table_id=tw_id, label=label, caption=caption,
            headers=headers, rows=data_rows,
        ))
    return tables


def _parse_nxml_captions(root: ET.Element) -> list[str]:
    out: list[str] = []
    for fig in root.iter("fig"):
        cap = fig.find("caption")
        if cap is not None:
            out.append(_element_text(cap))
    for tw in root.iter("table-wrap"):
        cap = tw.find("caption")
        if cap is not None:
            out.append(_element_text(cap))
    return out


def _parse_nxml(path: str) -> dict[str, Any]:
    """Returns (root, sections, tables, captions, doi_cands) or raises."""
    tree = ET.parse(path)
    root = tree.getroot()
    return {
        "root": root,
        "sections": _parse_nxml_sections(root),
        "tables": _parse_nxml_tables(root),
        "captions": _parse_nxml_captions(root),
        "doi_candidates": _parse_nxml_doi(root),
    }


# ---------------------------------------------------------------------------
# PDF parsing
# ---------------------------------------------------------------------------

_PDFTOTEXT_BIN = "pdftotext"


def _pdftotext(path: str, mode: str) -> str:
    """Run pdftotext with the given mode flag and return stdout text."""
    if not os.path.exists(path):
        return ""
    cmd = [_PDFTOTEXT_BIN]
    if mode == "layout":
        cmd.append("-layout")
    elif mode == "raw":
        cmd.append("-raw")
    cmd.extend([path, "-"])
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                              check=False)
        return proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def _pdftotext_first_pages(path: str, num_pages: int = 2) -> str:
    """Return text from only the first N pages of the PDF (for DOI scanning).
    Falls back to full-document text if pdftotext doesn't support page args.
    """
    if not os.path.exists(path):
        return ""
    cmd = [_PDFTOTEXT_BIN, "-layout", "-l", str(num_pages), path, "-"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                              check=False)
        if proc.returncode == 0:
            return proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return ""


_DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s)>\]'\" ]+", re.IGNORECASE)


def _scan_pdf_text_for_doi(text: str) -> list[str]:
    """Find DOI-like strings in PDF text. Returns a deduped list preserving
    order of first occurrence.
    """
    seen = []
    for m in _DOI_RE.finditer(text):
        d = m.group(0).rstrip(".,;")
        if d not in seen:
            seen.append(d)
    return seen


def _pdf_metadata_doi(path: str) -> str:
    """Try to read DOI from PDF /Info metadata via pdfinfo if available."""
    if not os.path.exists(path):
        return ""
    try:
        proc = subprocess.run(["pdfinfo", path], capture_output=True,
                              text=True, timeout=15, check=False)
        out = proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""
    # pdfinfo prints "Subject: 10.xxx/..." or "Keywords: doi:10.xxx/..." etc.
    for line in out.splitlines():
        m = _DOI_RE.search(line)
        if m:
            return m.group(0).rstrip(".,;")
    return ""


# ---------------------------------------------------------------------------
# Top-level ingestion
# ---------------------------------------------------------------------------

def ingest_article(article_dir: str,
                   article_id: str | None = None,
                   user_doi: str | None = None) -> Article:
    """Ingest a single article directory.

    Looks for these files (any subset may exist):
      - article.nxml
      - article_text.txt
      - article.pdf
      - metadata.json

    Returns an Article with all available sources merged.
    """
    if not os.path.isdir(article_dir):
        raise FileNotFoundError(f"Not a directory: {article_dir}")

    if article_id is None:
        article_id = os.path.basename(os.path.normpath(article_dir))

    nxml_path = os.path.join(article_dir, "article.nxml")
    text_path = os.path.join(article_dir, "article_text.txt")
    pdf_path = os.path.join(article_dir, "article.pdf")

    available: list[str] = []
    if os.path.exists(nxml_path):
        available.append("nxml")
    if os.path.exists(text_path):
        available.append("text")
    if os.path.exists(pdf_path):
        available.append("pdf")

    article = Article(
        article_id=article_id,
        source_kind=_classify_source_kind(available),
        available_sources=available,
    )

    text_parts: list[str] = []

    # NXML (preferred for sections + tables + DOI front matter)
    if "nxml" in available:
        try:
            parsed = _parse_nxml(nxml_path)
            article.sections = parsed["sections"]
            article.tables = parsed["tables"]
            article.captions = parsed["captions"]
            article.doi_candidates.extend(parsed["doi_candidates"])
        except ET.ParseError as e:
            article.warnings.append(f"nxml_parse_error: {e}")

    # Plain text (fallback / supplement)
    if "text" in available:
        try:
            with open(text_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()
            text_parts.append(_normalize_text(text_content))
        except OSError as e:
            article.warnings.append(f"text_read_error: {e}")

    # PDF (additional source, also used for DOI scanning)
    if "pdf" in available:
        # pdftotext -layout (good for tables)
        layout_text = _pdftotext(pdf_path, "layout")
        # pdftotext -raw (good for sign reconstruction and column flow)
        raw_text = _pdftotext(pdf_path, "raw")
        if layout_text:
            text_parts.append(_normalize_text(layout_text))
        if raw_text:
            text_parts.append(_normalize_text(raw_text))

        # DOI candidates from PDF metadata
        meta_doi = _pdf_metadata_doi(pdf_path)
        if meta_doi:
            article.doi_candidates.append(
                DOICandidate(doi=meta_doi, source="pdf_metadata"))

        # DOI candidates from first 2 pages of PDF text
        first_pages = _pdftotext_first_pages(pdf_path, num_pages=2)
        if first_pages:
            for d in _scan_pdf_text_for_doi(first_pages):
                article.doi_candidates.append(
                    DOICandidate(doi=d, source="pdf_text_first_2_pages"))

    # User-provided metadata override (highest-numbered precedence; lowest)
    if user_doi:
        article.doi_candidates.append(
            DOICandidate(doi=user_doi, source="user_metadata"))

    # Dedup doi_candidates while preserving order (first occurrence wins
    # for ties within the same source)
    seen_keys = set()
    deduped: list[DOICandidate] = []
    for c in article.doi_candidates:
        key = (c.doi, c.source)
        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(c)
    article.doi_candidates = deduped

    # Build full_text by joining all sources with double newlines
    if "nxml" in available:
        # Also flatten sections into prose for full_text. We include
        # section headings as their own lines so that compound names
        # used as section titles (a common NXML pattern in chemistry
        # papers — each compound gets its own <sec>) are recoverable
        # via the substring check in Gate C.
        nxml_prose_parts: list[str] = []
        for sec in article.sections:
            for h in sec.heading_path:
                if h:
                    nxml_prose_parts.append(h)
            for p in sec.paragraphs:
                nxml_prose_parts.append(p)
        # Tables: include caption + headers + row cells as flat text so the
        # substring check can find table-cell values.
        for t in article.tables:
            nxml_prose_parts.append(t.label + " " + t.caption)
            if t.headers:
                nxml_prose_parts.append(" | ".join(t.headers))
            for row in t.rows:
                nxml_prose_parts.append(" | ".join(c.text for c in row))
        if nxml_prose_parts:
            text_parts.insert(0, "\n\n".join(nxml_prose_parts))

    article.full_text = "\n\n".join(p for p in text_parts if p).strip()
    return article


def _classify_source_kind(available: list[str]) -> str:
    if "nxml" in available:
        return "pmc_nxml"
    if "pdf" in available and "text" not in available:
        return "loose_pdf"
    if "text" in available and "pdf" not in available:
        return "text_only"
    return "mixed"


# ---------------------------------------------------------------------------
# CLI for diagnostic dump (Phase 1 acceptance: produce a diagnostic per paper)
# ---------------------------------------------------------------------------

def diagnostic_dump(article: Article) -> dict[str, Any]:
    """Phase 1 acceptance produces a per-paper diagnostic for manual review."""
    return {
        "article_id": article.article_id,
        "source_kind": article.source_kind,
        "available_sources": article.available_sources,
        "section_count": len(article.sections),
        "section_first_3_headings": [
            " > ".join(s.heading_path) for s in article.sections[:3]
        ],
        "table_count": len(article.tables),
        "table_labels": [t.label for t in article.tables],
        "table_header_examples": [
            t.headers for t in article.tables[:3] if t.headers
        ],
        "caption_count": len(article.captions),
        "doi_candidate_count": len(article.doi_candidates),
        "doi_candidates": [
            {"doi": c.doi, "source": c.source}
            for c in article.doi_candidates
        ],
        "full_text_length": len(article.full_text),
        "warnings": article.warnings,
    }


if __name__ == "__main__":
    import argparse
    import json
    p = argparse.ArgumentParser(description="Ingest one article directory")
    p.add_argument("article_dir")
    p.add_argument("--article-id", default=None)
    args = p.parse_args()
    art = ingest_article(args.article_dir, article_id=args.article_id)
    print(json.dumps(diagnostic_dump(art), indent=2, ensure_ascii=False))

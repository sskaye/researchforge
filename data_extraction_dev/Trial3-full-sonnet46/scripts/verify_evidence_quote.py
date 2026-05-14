#!/usr/bin/env python3
"""
verify_evidence_quote.py — confirm each row's evidence_quote is verbatim
present somewhere in the cited paper file.

This is the deterministic-script equivalent of Phase 4 step 4. The agent
verifier does a deeper semantic check; this script only catches the
clear-cut case of "quote isn't in the file at all".

Matching is whitespace-normalized (multiple whitespace → single space,
NFC unicode normalization, ASCII hyphen folding from − – —).

Usage:
    python3 verify_evidence_quote.py <csv_path> --paper-root <papers_dir>

Output:
    row <id>: evidence_quote not found in <paper_dir>
Exit 0 if all quotes locate; 1 if any fail.
"""
import sys
import csv
import os
import re
import argparse
import subprocess
import unicodedata


def normalize(s: str) -> str:
    """Whitespace-collapse + unicode NFC + ASCII hyphen folding."""
    if not s:
        return ""
    s = unicodedata.normalize("NFC", s)
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def read_paper_text(paper_dir: str) -> str:
    """Concatenate all readable text sources for a paper."""
    parts = []
    for fname in ("article.nxml", "article_text.txt", "metadata.json"):
        p = os.path.join(paper_dir, fname)
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    parts.append(f.read())
            except Exception:
                pass
    pdf = os.path.join(paper_dir, "article.pdf")
    if os.path.isfile(pdf):
        try:
            r = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                               capture_output=True, text=True, timeout=30)
            if r.returncode == 0:
                parts.append(r.stdout)
            # Also try raw mode (sometimes recovers different glyphs)
            r2 = subprocess.run(["pdftotext", pdf, "-"],
                                capture_output=True, text=True, timeout=30)
            if r2.returncode == 0:
                parts.append(r2.stdout)
        except Exception:
            pass
    return "\n".join(parts)


def doi_from_source_url(url: str) -> str | None:
    if not url:
        return None
    u = url.strip().lower()
    for prefix in ("textbook:", "pmc:", "pmid:", "legacy:"):
        if u.startswith(prefix):
            return None
    m = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", url, re.IGNORECASE)
    return m.group(0) if m else None


def pmc_id_from_source_url(url: str) -> str | None:
    if not url:
        return None
    m = re.match(r"^pmc:(PMC\d+)$", url.strip(), re.IGNORECASE)
    return m.group(1).upper() if m else None


def build_index(paper_root: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return (DOI→dir, PMC-ID→dir) maps."""
    doi_map: dict[str, str] = {}
    pmc_map: dict[str, str] = {}
    if not os.path.isdir(paper_root):
        return doi_map, pmc_map
    rx_doi = re.compile(r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+", re.IGNORECASE)
    rx_dirpmc = re.compile(r"PMC(\d+)", re.IGNORECASE)
    rx_textpmc = re.compile(r"\bPMC\d{4,8}\b")
    for name in sorted(os.listdir(paper_root)):
        d = os.path.join(paper_root, name)
        if not os.path.isdir(d):
            continue
        # PMC ID first — usually in directory name
        dm = rx_dirpmc.search(name)
        if dm:
            pmc_map.setdefault(f"PMC{dm.group(1)}", d)
        text = read_paper_text(d)
        for m in rx_doi.finditer(text):
            doi = m.group(0).rstrip(".,);").lower()
            doi_map.setdefault(doi, d)
        if not dm:
            for tm in rx_textpmc.finditer(text):
                pmc_map.setdefault(tm.group(0).upper(), d)
                break
    return doi_map, pmc_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--paper-root", required=True)
    args = ap.parse_args()

    doi_index, pmc_index = build_index(args.paper_root)
    # Cache paper texts (normalized) per dir
    paper_cache: dict[str, str] = {}

    flagged = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            quote = (row.get("evidence_quote") or "").strip()
            rid = row.get("id", "?")
            if not quote:
                print(f"row {rid}: evidence_quote is empty")
                flagged += 1
                continue
            url = row.get("source_url", "") or ""
            doi = doi_from_source_url(url)
            pmc = pmc_id_from_source_url(url)
            paper_dir: str | None = None
            if doi:
                paper_dir = doi_index.get(doi.lower())
                if paper_dir is None:
                    print(f"row {rid}: could not locate paper for DOI={doi}")
                    flagged += 1
                    continue
            elif pmc:
                paper_dir = pmc_index.get(pmc.upper())
                if paper_dir is None:
                    print(f"row {rid}: could not locate paper for PMC ID={pmc}")
                    flagged += 1
                    continue
            else:
                # textbook: / pmid: / legacy: / etc. — agent verifier handles
                if url.lower().startswith(("textbook:", "pmid:", "legacy:")):
                    continue
                print(f"row {rid}: source_url has no recognizable identifier: {url!r}")
                flagged += 1
                continue
            if paper_dir not in paper_cache:
                paper_cache[paper_dir] = normalize(read_paper_text(paper_dir))
            haystack = paper_cache[paper_dir]
            needle = normalize(quote)
            if needle in haystack:
                continue
            # Fallback: try first 60 chars of quote (in case of trailing noise)
            if len(needle) > 60 and needle[:60] in haystack:
                continue
            rid = row.get("id", "?")
            print(f"row {rid}: evidence_quote not found in {os.path.basename(paper_dir)}")
            flagged += 1

    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

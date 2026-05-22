#!/usr/bin/env python3
"""
verify_doi.py — confirm a row's DOI actually appears in the cited paper file.

A row's source_url (DOI) is the canonical citation. If the DOI string isn't
present anywhere in the actual paper file's text, the citation is broken —
either the extractor invented the DOI or pointed at the wrong paper.

Usage:
    python3 verify_doi.py <csv_path> --paper-root <papers_dir>

`papers_dir` is the directory containing one subdirectory per paper.
The row's paper file is found by matching the row's `notes` field
or by a `paper_dir` column (if present), or by scanning paper
subdirectories for the matching DOI.

Output:
    row <id>: DOI=<...> not found in any provided paper file
Exit 0 if all DOIs locate; 1 if any fail.
"""
import sys
import csv
import os
import re
import argparse
import subprocess


def extract_doi(text: str) -> set[str]:
    """All DOI strings found in `text`. Case-insensitive."""
    if not text:
        return set()
    rx = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+",
                    re.IGNORECASE)
    return {m.group(0).rstrip(".,);").lower() for m in rx.finditer(text)}


def doi_from_source_url(url: str) -> str | None:
    """Return the DOI in source_url, or None if source_url uses a
    non-DOI form (textbook:, pmc:, pmid:, legacy:, etc.) or has no DOI."""
    if not url:
        return None
    u = url.strip().lower()
    for prefix in ("textbook:", "pmc:", "pmid:", "legacy:"):
        if u.startswith(prefix):
            return None
    m = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", url, re.IGNORECASE)
    return m.group(0) if m else None


def pmc_id_from_source_url(url: str) -> str | None:
    """Return the PMC ID (e.g. 'PMC3716435') if source_url is a pmc: form."""
    if not url:
        return None
    u = url.strip()
    m = re.match(r"^pmc:(PMC\d+)$", u, re.IGNORECASE)
    return m.group(1).upper() if m else None


def pmid_from_source_url(url: str) -> str | None:
    if not url:
        return None
    u = url.strip()
    m = re.match(r"^pmid:(\d+)$", u, re.IGNORECASE)
    return m.group(1) if m else None


def read_paper_text(paper_dir: str) -> str:
    """Return the best text representation of the paper at paper_dir."""
    candidates = ["article.nxml", "article_text.txt", "metadata.json"]
    parts = []
    for fname in candidates:
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
            txt = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                                 capture_output=True, text=True, timeout=30)
            if txt.returncode == 0:
                parts.append(txt.stdout)
        except Exception:
            pass
    return "\n".join(parts)


def find_paper_for_row(row: dict, paper_root: str,
                        index: dict[str, str]) -> str | None:
    """Return the paper directory matching the row's DOI, or None."""
    doi = doi_from_source_url(row.get("source_url", ""))
    if not doi:
        return None
    # If we have a precomputed DOI→dir index, use it
    return index.get(doi.lower())


def build_index(paper_root: str) -> dict[str, str]:
    """Scan paper_root subdirectories and build a DOI → dir map."""
    out: dict[str, str] = {}
    if not os.path.isdir(paper_root):
        return out
    for name in sorted(os.listdir(paper_root)):
        d = os.path.join(paper_root, name)
        if not os.path.isdir(d):
            continue
        text = read_paper_text(d)
        for doi in extract_doi(text):
            out.setdefault(doi.lower(), d)
    return out


def build_pmc_index(paper_root: str) -> dict[str, str]:
    """Scan paper_root subdirectories and build a PMC-ID → dir map.
    PMC IDs come from either the directory name (e.g. '157_PMC3716435_...')
    or from the paper text."""
    out: dict[str, str] = {}
    if not os.path.isdir(paper_root):
        return out
    rx_dirname = re.compile(r"PMC(\d+)", re.IGNORECASE)
    rx_text = re.compile(r"\bPMC\d{4,8}\b")
    for name in sorted(os.listdir(paper_root)):
        d = os.path.join(paper_root, name)
        if not os.path.isdir(d):
            continue
        # Prefer the directory name (cheaper) — most PMC papers have it
        m = rx_dirname.search(name)
        if m:
            out.setdefault(f"PMC{m.group(1)}", d)
            continue
        # Fall back to scanning the paper text
        text = read_paper_text(d)
        for tm in rx_text.finditer(text):
            out.setdefault(tm.group(0).upper(), d)
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--paper-root", required=True,
                    help="Directory containing one subdir per paper.")
    args = ap.parse_args()
    doi_index = build_index(args.paper_root)
    pmc_index = build_pmc_index(args.paper_root)
    print(f"# Indexed {len(doi_index)} DOIs and {len(pmc_index)} PMC IDs "
          f"across {len(os.listdir(args.paper_root))} paper subdirs",
          file=sys.stderr)
    flagged = 0
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url = row.get("source_url", "")
            rid = row.get("id", "?")
            doi = doi_from_source_url(url)
            pmc = pmc_id_from_source_url(url)
            pmid = pmid_from_source_url(url)
            if doi is not None:
                if doi.lower() not in doi_index:
                    print(f"row {rid}: DOI={doi} not found in any "
                          "provided paper file")
                    flagged += 1
            elif pmc is not None:
                if pmc.upper() not in pmc_index:
                    print(f"row {rid}: PMC ID={pmc} not found in any "
                          "provided paper file")
                    flagged += 1
            elif pmid is not None:
                # No deterministic index for PMIDs (rare); skip check.
                # Verifier-agent will check manually.
                continue
            else:
                # textbook: / legacy: / unknown — script can't verify;
                # leave it to the agent verifier.
                continue
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()

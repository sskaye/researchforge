#!/usr/bin/env python3
"""Corpus-aware DOI verifier for this trial's layout."""
import csv, os, re, subprocess, sys

PAPERS = "/sessions/wizardly-beautiful-tesla/mnt/opus47_papers/Papers"

def extract_dois(text):
    rx = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
    return {m.group(0).rstrip(".,);").lower() for m in rx.finditer(text or "")}

def read_pdf(p):
    try:
        r = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, timeout=15)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""

def read_subdir(d):
    parts = []
    for f in ("article.nxml", "article_text.txt", "metadata.json"):
        p = os.path.join(d, f)
        if os.path.isfile(p):
            try:
                with open(p, errors="replace") as fh:
                    parts.append(fh.read())
            except: pass
    pdf = os.path.join(d, "article.pdf")
    if os.path.isfile(pdf):
        parts.append(read_pdf(pdf))
    return "\n".join(parts)

print("Building DOI index ...", file=sys.stderr)
doi_index = {}
pmc_index = {}

# 1. PMC dirs at top level
for name in sorted(os.listdir(PAPERS)):
    p = os.path.join(PAPERS, name)
    if not os.path.isdir(p) or name in ("materials_inorganic","measurement_prediction","organic_synthesis","pharma_cocrystals"):
        continue
    txt = read_subdir(p)
    for d in extract_dois(txt):
        doi_index.setdefault(d, p)
    m = re.search(r"PMC(\d+)", name)
    if m: pmc_index.setdefault(f"PMC{m.group(1)}", p)

# 2. standalone PDFs
for f in sorted(os.listdir(PAPERS)):
    p = os.path.join(PAPERS, f)
    if f.endswith(".pdf") and os.path.isfile(p):
        txt = read_pdf(p)
        for d in extract_dois(txt):
            doi_index.setdefault(d, p)

# 3. category PDFs
for cat in ("materials_inorganic","measurement_prediction","organic_synthesis","pharma_cocrystals"):
    for f in sorted(os.listdir(os.path.join(PAPERS, cat))):
        if f.endswith(".pdf"):
            p = os.path.join(PAPERS, cat, f)
            txt = read_pdf(p)
            for d in extract_dois(txt):
                doi_index.setdefault(d, p)

print(f"# Indexed {len(doi_index)} DOIs, {len(pmc_index)} PMC IDs", file=sys.stderr)

with open("doi_index.txt", "w") as fh:
    for d, p in sorted(doi_index.items()):
        fh.write(f"{d}\t{p}\n")

# Verify each row
flagged = 0
total = 0
with open(sys.argv[1], encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total += 1
        url = row.get("source_url", "").strip()
        rid = row.get("id", "?")
        if url.startswith(("textbook:", "legacy:")):
            continue
        m_doi = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", url, re.IGNORECASE)
        if m_doi:
            d = m_doi.group(0).lower()
            if d not in doi_index:
                print(f"row {rid}: DOI={d} not found in any provided paper file")
                flagged += 1
        elif url.lower().startswith("pmc:"):
            pmc = url[4:].strip().upper()
            if pmc not in pmc_index:
                print(f"row {rid}: PMC={pmc} not indexed")
                flagged += 1
print(f"\nTotal rows: {total}; DOI/PMC mismatches: {flagged}")
sys.exit(0)

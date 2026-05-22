#!/usr/bin/env python3
import csv, os, re, subprocess, sys, html, unicodedata

PAPERS = "/sessions/wizardly-beautiful-tesla/mnt/opus47_papers/Papers"

def read_pdf(p):
    try:
        r = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, timeout=20)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""

def read_subdir(d):
    parts = []
    for f in ("article.nxml", "article_text.txt"):
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

def normalize(s):
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    s = unicodedata.normalize("NFKD", s)
    # Fold various Unicode variants to ASCII equivalents
    replacements = {
        "−": "-", "–": "-", "—": "-", "‐": "-", "‑": "-",
        "′": "'", "‵": "'", "‛": "'", "´": "'", "ʹ": "'", "ʼ": "'",
        "″": "\"", "“": "\"", "”": "\"", "‟": "\"",
        "·": ".", "•": ".",
        " ": " ", "​": "", " ": " ",
        "◦": "°",  # degree-looking ring
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    # remove combining marks
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

print("Building paper-text index ...", file=sys.stderr)
text_by_doi, text_by_pmc, text_by_legacy = {}, {}, {}
rx_doi = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)

for name in sorted(os.listdir(PAPERS)):
    p = os.path.join(PAPERS, name)
    if not os.path.isdir(p) or name in ("materials_inorganic","measurement_prediction","organic_synthesis","pharma_cocrystals"):
        continue
    txt = read_subdir(p)
    if not txt: continue
    ntxt = normalize(txt)
    for m in rx_doi.finditer(txt):
        text_by_doi.setdefault(m.group(0).rstrip(".,);").lower(), ntxt)
    m = re.search(r"PMC(\d+)", name)
    if m: text_by_pmc.setdefault(f"PMC{m.group(1)}", ntxt)

for f in sorted(os.listdir(PAPERS)):
    p = os.path.join(PAPERS, f)
    if f.endswith(".pdf") and os.path.isfile(p):
        txt = read_pdf(p)
        ntxt = normalize(txt)
        stem = f.rsplit(".pdf",1)[0]
        text_by_legacy["legacy:"+stem.lower().replace(" ","_")] = ntxt
        for m in rx_doi.finditer(txt):
            text_by_doi.setdefault(m.group(0).rstrip(".,);").lower(), ntxt)

for cat in ("materials_inorganic","measurement_prediction","organic_synthesis","pharma_cocrystals"):
    for f in sorted(os.listdir(os.path.join(PAPERS, cat))):
        if f.endswith(".pdf"):
            p = os.path.join(PAPERS, cat, f)
            txt = read_pdf(p)
            ntxt = normalize(txt)
            stem = f.rsplit(".pdf",1)[0]
            text_by_legacy.setdefault("legacy:"+stem.lower(), ntxt)
            for m in rx_doi.finditer(txt):
                text_by_doi.setdefault(m.group(0).rstrip(".,);").lower(), ntxt)

print(f"# Indexed DOI={len(text_by_doi)} PMC={len(text_by_pmc)} legacy={len(text_by_legacy)}", file=sys.stderr)

def get_paper(url):
    u = url.strip().lower()
    if u.startswith("textbook:"): return "textbook"  # skip flagging
    if u.startswith("legacy:"): return text_by_legacy.get(u)
    if u.startswith("pmc:"):
        return text_by_pmc.get(url[4:].upper().strip())
    m = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", url, re.IGNORECASE)
    if m: return text_by_doi.get(m.group(0).lower())
    return None

flagged_quote = 0
flagged_value = 0
no_paper = 0
total = 0
flagged_ids = []
with open(sys.argv[1], encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total += 1
        q = (row.get("evidence_quote") or "").strip()
        if not q: continue
        paper = get_paper(row.get("source_url", ""))
        if paper is None:
            no_paper += 1
            continue
        if paper == "textbook":
            continue
        nq = normalize(q)
        if nq and nq in paper:
            continue
        # Try shorter chunks: split on first whitespace, find longest single substring
        # The full quote may have agent-introduced whitespace differences; try just the numeric portion + a nearby word
        # Try also stripped of leading "Synthesis of " preamble
        nq2 = re.sub(r"^synthesis (of |)", "", nq)
        if nq2 in paper:
            continue
        # Try a 40-char window
        if len(nq) > 40:
            mid = nq[len(nq)//2 - 20: len(nq)//2 + 20]
            if mid in paper:
                continue
        flagged_quote += 1
        flagged_ids.append(row["id"])

print(f"\nTotal rows: {total}; no_paper_indexed: {no_paper}; quote-not-found: {flagged_quote}")
# Save flagged IDs
with open("quote_advisory_flags.txt", "w") as f:
    for rid in flagged_ids:
        f.write(rid + "\n")

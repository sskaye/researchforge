import unicodedata, re, sys, os, json, csv, glob

def norm(s):
    if not s: return ""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[‐‑‒–—―−]", "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def load_paper(folder):
    for fname in ["article_text.txt", "article.nxml"]:
        path = os.path.join(folder, fname)
        if os.path.exists(path):
            with open(path, errors="replace") as f:
                return f.read(), path
    for p in sorted(glob.glob(os.path.join(folder, "*.html"))):
        with open(p, errors="replace") as f:
            return f.read(), p
    for p in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
        return load_file(p)
    return "", None

def load_file(path):
    if path.endswith(".pdf"):
        import subprocess
        try:
            r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, timeout=60)
            return r.stdout, path
        except Exception as e:
            return f"PDF_ERROR:{e}", path
    with open(path, errors="replace") as f:
        return f.read(), path

def map_path(p):
    return p.replace("/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/", "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/")

def check(row):
    notes = row["notes"]
    m = re.search(r"paper_path=([^;]+)", notes)
    if not m:
        return {"error": "no paper_path"}
    pp = map_path(m.group(1).strip())
    if os.path.isdir(pp):
        txt, used = load_paper(pp)
    elif os.path.isfile(pp):
        txt, used = load_file(pp)
    else:
        return {"error": f"path not found: {pp}"}
    ntxt = norm(txt)
    quote = row["evidence_quote"]
    nq = norm(quote)
    doi_url = row["source_url"]
    doi = ""
    if "doi.org/" in doi_url:
        doi = doi_url.split("doi.org/")[-1]
    elif "pmc:" in doi_url.lower():
        doi = doi_url.split(":")[-1]

    res = {
        "path_used": used,
        "doi_substring": doi,
        "doi_in_text": doi.lower() in ntxt.lower() if doi else None,
        "quote_in_text": nq in ntxt,
        "value_raw": row["value_raw"],
        "value_in_quote": norm(row["value_raw"]) in nq,
        "has_ellipsis": "..." in quote or "…" in quote,
        "compound_name": row["compound_name"],
        "data_type": row["data_type"],
        "ntxt_len": len(ntxt),
    }
    if nq in ntxt:
        i = ntxt.find(nq)
        res["ctx_before"] = ntxt[max(0,i-200):i][-200:]
        res["ctx_after"] = ntxt[i+len(nq):i+len(nq)+200]
    else:
        nv = norm(row["value_raw"])
        if nv and nv in ntxt:
            i = ntxt.find(nv)
            res["value_ctx"] = ntxt[max(0,i-400):i+len(nv)+200]
        else:
            # show occurrences of compound name
            cn = norm(row["compound_name"])[:60]
            if cn and cn in ntxt:
                i = ntxt.find(cn)
                res["compound_ctx"] = ntxt[max(0,i-200):i+len(cn)+400]
    return res

# Read CSV
rows = []
with open("/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/Trial3-full-gpt55_high/_my_audit_batch_2.csv") as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

ids = sys.argv[1:] if len(sys.argv) > 1 else [r["id"] for r in rows]
out = {}
for row in rows:
    if row["id"] in ids:
        out[row["id"]] = check(row)
print(json.dumps(out, indent=2, ensure_ascii=False))

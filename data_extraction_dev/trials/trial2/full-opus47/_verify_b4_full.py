#!/usr/bin/env python3
"""Comprehensive verifier for batch 4 - extracts contexts for all 25 rows."""
import json, csv, os, unicodedata, re, sys, subprocess

ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev"
csv_path = f"{ROOT}/trials/trial2/full-opus47/_my_audit_extra_batch_4.csv"
map_path = f"{ROOT}/trials/trial2/full-opus47/url_to_folder_built.json"

with open(map_path) as f:
    URLMAP = json.load(f)

def fold(s):
    if not s: return ""
    s = unicodedata.normalize("NFKC", s)
    for ch in ["‐","‑","‒","–","—","―","−","⁃","­","˗","－"]:
        s = s.replace(ch, "-")
    s = re.sub(r"\s+", " ", s)
    return s

def strip_xml(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"').replace("&apos;","'").replace("&nbsp;"," ")
    s = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1),16)), s)
    s = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), s)
    return s

def get_files_for_doi(folder, doi_keys):
    full = os.path.join(ROOT, folder)
    meta_path = os.path.join(full, "_meta.csv")
    matched_base = None
    if os.path.isfile(meta_path):
        with open(meta_path, errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                doi = (r.get("doi","") or "").strip()
                for key in doi_keys:
                    if doi and doi.lower() == key.lower():
                        matched_base = r.get("filename_base","")
                        break
                if matched_base: break
    files = []
    if matched_base and os.path.isdir(full):
        for fn in os.listdir(full):
            if fn.startswith(matched_base):
                p = os.path.join(full, fn)
                if os.path.isfile(p):
                    files.append(p)
    return files, matched_base

def load_text_for(folder, doi_keys, url):
    full = os.path.join(ROOT, folder)
    # PDF as folder path
    if folder.endswith(".pdf"):
        if os.path.isfile(full):
            try:
                r = subprocess.run(["pdftotext","-layout", full, "-"], capture_output=True, text=True, timeout=60)
                return r.stdout, "pdf"
            except: return "", "err"
    # Single-paper folder: corpora/full_168 (a leaf placeholder)
    if folder == "corpora/full_168":
        # search for matching file
        for fn in os.listdir(os.path.join(ROOT, folder)):
            full2 = os.path.join(ROOT, folder, fn)
            if os.path.isdir(full2): continue
            # match doi in filename or content?
        return "", "no_paper"
    # multi-paper folder
    if os.path.isdir(full) and os.path.isfile(os.path.join(full,"_meta.csv")):
        files, base = get_files_for_doi(folder, doi_keys)
        for p in files:
            if p.endswith(".html"):
                with open(p, errors="replace") as f:
                    return f.read(), "html:"+base
        for p in files:
            if p.endswith(".pdf"):
                try:
                    r = subprocess.run(["pdftotext","-layout", p, "-"], capture_output=True, text=True, timeout=60)
                    return r.stdout, "pdf:"+base
                except: pass
        return "", "no_match"
    # single-paper folder
    if os.path.isdir(full):
        for fn in ["article.nxml","article_text.txt"]:
            p = os.path.join(full, fn)
            if os.path.isfile(p):
                with open(p, errors="replace") as f:
                    return f.read(), fn
        p = os.path.join(full, "article.pdf")
        if os.path.isfile(p):
            try:
                r = subprocess.run(["pdftotext","-layout", p, "-"], capture_output=True, text=True, timeout=60)
                return r.stdout, "pdf"
            except: pass
    return "", "none"

def context_around(text, needle, before=80, after=120):
    """Return up to 3 contexts around occurrences of needle in text."""
    if not needle or not text: return []
    needle_short = needle[:60]  # first 60 chars
    out = []
    idx = 0
    while idx < len(text) and len(out) < 3:
        i = text.find(needle_short, idx)
        if i == -1: break
        s = max(0, i-before)
        e = min(len(text), i+len(needle_short)+after)
        ctx = text[s:e]
        ctx = re.sub(r"\s+", " ", ctx)
        out.append(ctx)
        idx = i+len(needle_short)
    return out

rows = list(csv.DictReader(open(csv_path)))

out = []
for row in rows:
    rid = row["id"]
    url = row["source_url"]
    quote = row["evidence_quote"]
    val_raw = row["value_raw"]
    compound = row["compound_name"]
    folder = URLMAP.get(url, "")
    data_type = row.get("data_type","")
    prop = row.get("property","")
    val_c = row.get("value_celsius","")
    notes = row.get("notes","")
    info = {
        "id": rid, "compound": compound, "url": url, "folder": folder,
        "value_raw": val_raw, "value_celsius": val_c, "property": prop,
        "data_type": data_type, "evidence_quote": quote, "notes": notes,
    }
    doi_keys = []
    if url.startswith("https://doi.org/"):
        doi_keys.append(url.replace("https://doi.org/",""))
    if url.startswith("pmc:"):
        doi_keys.append(url[4:])
    if url.startswith("legacy:"):
        doi_keys.append(url[7:])
    info["doi_keys"] = doi_keys
    text, src = load_text_for(folder, doi_keys, url)
    info["src"] = src
    info["plen"] = len(text)
    # NFC fold checks
    text_fold = fold(text)
    text_stripped_fold = fold(strip_xml(text))
    quote_fold = fold(quote)
    info["quote_in_raw"] = quote_fold in text_fold
    info["quote_in_stripped"] = quote_fold in text_stripped_fold
    # ellipsis check
    info["quote_has_ellipsis"] = "..." in quote or "…" in quote
    # doi check (also try in stripped)
    info["doi_in_paper"] = any(k.lower() in text.lower() for k in doi_keys) if doi_keys else None
    # value digits in quote
    digits = re.findall(r"-?\d+\.?\d*", val_raw or "")
    info["digits_val"] = digits
    info["digits_in_quote"] = all(d in quote for d in digits) if digits else None
    # get context around quote in paper (use stripped text)
    ctx_q = context_around(text_stripped_fold, quote_fold[:40] if len(quote_fold)>40 else quote_fold, 60, 200)
    info["ctx_quote"] = ctx_q
    # value_celsius unit conversion check
    info["value_celsius_check"] = None
    out.append(info)

with open("/tmp/results_b4.json","w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"wrote {len(out)} entries to /tmp/results_b4.json")

#!/usr/bin/env python3
"""Comprehensive verifier for batch 4."""
import json, csv, os, unicodedata, re, sys, subprocess, glob

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

OVERRIDES = {
    # id -> (folder, filename_base) - manual overrides for missing mappings
    "1646": ("corpora/full_168/pharma_cocrystals", "dichi_2025_polyphenols_thermal"),
    "31": ("corpora/full_168", None),  # need to find file
}

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

def pdf_text(path):
    out_file = "/tmp/_pdftext_tmp.txt"
    try:
        subprocess.run(["pdftotext","-layout", path, out_file], timeout=60, capture_output=True)
        if os.path.isfile(out_file):
            with open(out_file, errors="replace") as f:
                return f.read()
    except Exception:
        return ""
    return ""

def load_text_for(folder, doi_keys, url, rid=None):
    if rid in OVERRIDES:
        f2, base = OVERRIDES[rid]
        if base:
            files = []
            full = os.path.join(ROOT, f2)
            for fn in os.listdir(full):
                if fn.startswith(base):
                    files.append(os.path.join(full,fn))
            for p in files:
                if p.endswith(".pdf"):
                    t = pdf_text(p)
                    if t: return t, "pdf:"+base
            for p in files:
                if p.endswith(".html"):
                    return open(p, errors="replace").read(), "html:"+base
    full = os.path.join(ROOT, folder)
    if folder.endswith(".pdf"):
        if os.path.isfile(full):
            return pdf_text(full), "pdf"
    if os.path.isdir(full) and os.path.isfile(os.path.join(full,"_meta.csv")):
        files, base = get_files_for_doi(folder, doi_keys)
        for p in files:
            if p.endswith(".pdf"):
                t = pdf_text(p)
                if t: return t, "pdf:"+base
        for p in files:
            if p.endswith(".html"):
                return open(p, errors="replace").read(), "html:"+base
        return "", "no_match"
    if os.path.isdir(full):
        for fn in ["article.nxml","article_text.txt"]:
            p = os.path.join(full, fn)
            if os.path.isfile(p):
                return open(p, errors="replace").read(), fn
        p = os.path.join(full, "article.pdf")
        if os.path.isfile(p):
            return pdf_text(p), "pdf"
    return "", "none"

def find_value_in_quote(quote, val_raw):
    """Check if value_raw's key digits/range are in the quote (allowing hyphen fold)."""
    if not quote or not val_raw: return False
    q = fold(quote)
    v = fold(val_raw)
    # Try direct
    if v in q: return True
    # try without units
    v_strip = re.sub(r"\s*°\s*C|\s*°C|\s*deg\s*C|\s*\(.*?\)", "", v).strip()
    if v_strip and v_strip in q: return True
    # try just the range
    m = re.search(r"(-?\d+\.?\d*)\s*-\s*(-?\d+\.?\d*)", v_strip)
    if m:
        rng = f"{m.group(1)}-{m.group(2)}"
        if rng in q: return True
    return False

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
    text, src = load_text_for(folder, doi_keys, url, rid)
    info["src"] = src
    info["plen"] = len(text)
    text_fold = fold(text)
    text_stripped_fold = fold(strip_xml(text))
    quote_fold = fold(quote)
    info["q_raw"] = quote_fold in text_fold
    info["q_strip"] = quote_fold in text_stripped_fold
    info["q_has_ellipsis"] = "..." in quote or "…" in quote
    info["doi_in"] = any(k.lower() in text.lower() for k in doi_keys) if doi_keys else None
    digits = re.findall(r"-?\d+\.?\d*", val_raw or "")
    info["digits_val"] = digits
    info["digits_in_quote"] = all(d in quote for d in digits) if digits else None
    info["val_in_quote"] = find_value_in_quote(quote, val_raw)
    # context
    needle = quote_fold[:50] if len(quote_fold)>50 else quote_fold
    idx = text_stripped_fold.find(needle)
    if idx >= 0:
        info["ctx"] = text_stripped_fold[max(0,idx-50):idx+len(needle)+200]
    else:
        info["ctx"] = None
    out.append(info)

with open("/tmp/results_b4.json","w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
for d in out:
    print(f"id={d['id']} src={d['src']} plen={d['plen']} q_raw={d['q_raw']} q_strip={d['q_strip']} doi={d['doi_in']} dig={d['digits_in_quote']} val_in={d['val_in_quote']}")

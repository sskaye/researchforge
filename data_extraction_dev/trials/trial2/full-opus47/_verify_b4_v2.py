#!/usr/bin/env python3
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
    """Strip XML tags and decode common entities."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"').replace("&apos;","'").replace("&#x2013;","–").replace("&#x2014;","—").replace("&#x2009;"," ").replace("&#x00B0;","°").replace("&#xB0;","°").replace("&nbsp;"," ")
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
    if folder.endswith(".pdf"):
        if os.path.isfile(full):
            try:
                r = subprocess.run(["pdftotext","-layout", full, "-"], capture_output=True, text=True, timeout=60)
                return r.stdout, "pdf"
            except: return "", "err"
    if os.path.isdir(full) and os.path.isfile(os.path.join(full,"_meta.csv")):
        files, base = get_files_for_doi(folder, doi_keys)
        for p in files:
            if p.endswith(".html"):
                with open(p, errors="replace") as f:
                    text = f.read()
                return text, "html:"+base
        for p in files:
            if p.endswith(".pdf"):
                try:
                    r = subprocess.run(["pdftotext","-layout", p, "-"], capture_output=True, text=True, timeout=60)
                    return r.stdout, "pdf:"+base
                except: pass
        return "", "no_match"
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

rows = list(csv.DictReader(open(csv_path)))

results = []
for row in rows:
    rid = row["id"]
    url = row["source_url"]
    quote = row["evidence_quote"]
    val_raw = row["value_raw"]
    compound = row["compound_name"]
    folder = URLMAP.get(url, "")
    info = {"id": rid, "compound": compound, "url": url, "folder": folder}
    doi_keys = []
    if url.startswith("https://doi.org/"):
        doi_keys.append(url.replace("https://doi.org/",""))
    if url.startswith("pmc:"):
        doi_keys.append(url[4:])
    if url.startswith("legacy:"):
        doi_keys.append(url[7:])
    text, src = load_text_for(folder, doi_keys, url)
    info["src"] = src
    info["plen"] = len(text)
    text_fold = fold(text)
    quote_fold = fold(quote)
    info["quote_in"] = quote_fold in text_fold
    # also try with XML stripped
    if not info["quote_in"]:
        text_stripped = fold(strip_xml(text))
        info["quote_in_stripped"] = quote_fold in text_stripped
    else:
        info["quote_in_stripped"] = True
    info["doi_in"] = any(k.lower() in text.lower() for k in doi_keys) if doi_keys else None
    digits = re.findall(r"-?\d+\.?\d*", val_raw or "")
    info["digits_val"] = digits
    info["digits_in_quote"] = all(d in quote for d in digits) if digits else None
    info["val_raw"] = val_raw
    info["quote"] = quote
    results.append(info)

with open("/tmp/results_b4.json","w") as f:
    json.dump(results, f, indent=2)
for r in results:
    print(f"id={r['id']} src={r['src']} plen={r['plen']} q_in={r['quote_in']} q_strip={r['quote_in_stripped']} doi={r['doi_in']} dig_q={r['digits_in_quote']} val={r['val_raw']}")

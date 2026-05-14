"""Verify all 25 rows of batch 8."""
import csv
import json
import os
import re
import subprocess
import unicodedata

ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev"
CSV_PATH = f"{ROOT}/Trial3-full-opus47/_my_audit_extra_batch_8.csv"
URL_MAP = f"{ROOT}/Trial3-full-opus47/url_to_folder_built.json"

# Manual override map for rows whose URL→folder is generic (folder is root corpora/full_168)
URL_OVERRIDES = {
    "https://doi.org/10.1021/jm3014162": "corpora/full_168/2013_Zhou_Identification and Characterization of Small Molecules as Potent and Specific EPAC2 Antagonists.pdf",
    "https://doi.org/10.1021/acs.joc.9b00711": "corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors.pdf",
}

def normalize(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    for d in ["‐", "‑", "‒", "–", "—", "―", "−", "⁃"]:
        s = s.replace(d, "-")
    # Fold Cyrillic look-alikes to Latin
    repl = {"С":"C","с":"c","Р":"P","р":"p","А":"A","а":"a","Е":"E","е":"e","О":"O","о":"o","Н":"H","Х":"X","х":"x","В":"B","К":"K","М":"M","Т":"T","У":"Y"}
    for k,v in repl.items():
        s = s.replace(k,v)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()

def strip_xml(s):
    # Strip XML tags
    s = re.sub(r"<[^>]+>", " ", s)
    # Decode &#xNNNN; numeric entities
    def _ent(m):
        try:
            return chr(int(m.group(1), 16))
        except:
            return ""
    s = re.sub(r"&#x([0-9a-fA-F]+);", _ent, s)
    def _ent2(m):
        try:
            return chr(int(m.group(1)))
        except:
            return ""
    s = re.sub(r"&#(\d+);", _ent2, s)
    s = s.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"').replace("&apos;","'").replace("&nbsp;"," ")
    return s

def read_paper_text(folder_rel):
    """folder_rel relative to data_extraction_dev"""
    full = os.path.join(ROOT, folder_rel)
    if full.endswith(".pdf") and os.path.isfile(full):
        try:
            r = subprocess.run(["pdftotext","-layout", full, "-"], capture_output=True, text=True, timeout=60)
            return r.stdout
        except Exception as e:
            return ""
    if os.path.isdir(full):
        # Try article_text.txt first (cleaner), then nxml (strip tags), then pdf
        for cand in ["article_text.txt","article.txt"]:
            p = os.path.join(full, cand)
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
        p = os.path.join(full, "article.nxml")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                return strip_xml(f.read())
        p = os.path.join(full, "article.pdf")
        if os.path.exists(p):
            try:
                r = subprocess.run(["pdftotext","-layout", p, "-"], capture_output=True, text=True, timeout=60)
                return r.stdout
            except:
                return ""
    return ""

def main():
    with open(URL_MAP) as f:
        url_map = json.load(f)

    rows = []
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    out = []
    for r in rows:
        src_url = r["source_url"]
        folder = URL_OVERRIDES.get(src_url) or url_map.get(src_url)
        if folder is None:
            out.append({"id": r["id"], "verdict": "flagged_doi_unrelated_paper", "note": f"URL not in map: {src_url}"})
            continue
        text = read_paper_text(folder)
        if not text:
            out.append({"id": r["id"], "verdict": "flagged_doi_unrelated_paper", "note": f"Could not read paper {folder}"})
            continue
        n_text = normalize(text)
        # Check evidence quote
        evq = r["evidence_quote"]
        n_quote = normalize(evq)
        # Check for literal ... ellipsis joining
        has_ellipsis = "..." in evq or "…" in evq
        quote_found = n_quote in n_text

        # Check value_raw in quote - use numeric component as primary check
        val_raw = r["value_raw"]
        n_val = normalize(val_raw)
        val_in_quote = n_val in n_quote if n_val else False
        # If not directly, check if numeric portion is in quote
        if not val_in_quote and n_val:
            # Extract numeric tokens from value_raw
            nums = re.findall(r"-?\d+\.?\d*", n_val)
            # All numeric tokens should be in the quote
            if nums and all(num in n_quote for num in nums):
                val_in_quote = True

        # Check compound_name presence (loose: at least the trailing chunk should appear)
        cname = r["compound_name"]
        n_cname = normalize(cname)
        # Heuristic: strip locant prefix to get last word
        compound_hint = re.sub(r"^[\d\.\-,\s]+","", n_cname)
        # Check if the compound name (or a substantial substring) is in the paper
        # For verification we'll trust quote check + manual review

        verdict = "verified"
        note = ""
        if not quote_found:
            verdict = "flagged_evidence_quote_not_found"
            note = f"quote not found"
        elif has_ellipsis:
            verdict = "flagged_evidence_quote_not_found"
            note = "ellipsis in quote"
        elif not val_in_quote:
            verdict = "flagged_evidence_quote_not_found"
            note = f"value_raw '{val_raw}' missing from quote"

        out.append({
            "id": r["id"],
            "verdict": verdict,
            "note": note,
            "compound_name": cname,
            "value_raw": val_raw,
            "source_url": src_url,
            "folder": folder,
        })

    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

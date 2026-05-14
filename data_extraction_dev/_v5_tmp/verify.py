#!/usr/bin/env python3
"""Phase 4 verifier for extra_batch_5 (25 rows)."""
import json, csv, os, sys, re, subprocess, unicodedata, traceback

BASE = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev"
os.chdir(BASE)

m = json.load(open("trials/trial2/full-opus47/url_to_folder_built.json"))
rows = list(csv.DictReader(open("trials/trial2/full-opus47/_my_audit_extra_batch_5.csv")))

overrides = {
    "1642": "corpora/full_168/pharma_cocrystals/dichi_2025_polyphenols_thermal",
    "1853": "corpora/full_168/pharma_cocrystals/chmielewska_2020_API_fatty_alcohol_eutectic",
    "75":   "corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors",
}
specific_subdir = {
    "1785": "corpora/full_168/organic_synthesis/gomezayuso_2024_ugi_nitrogen_heterocycles",
    "1830": "corpora/full_168/organic_synthesis/ledermann_2023_iodoindoles_synthesis",
    "1571": "corpora/full_168/organic_synthesis/rios_2026_dhpm_vorinostat",
    "1736": "corpora/full_168/measurement_prediction/muller_2020_dsc-tga-pcm-thermophysical",
    "1469": "corpora/full_168/materials_inorganic/li_2025_coordination_polymer_eutectic",
}

def fetch_text_for_folder(folder):
    """Return (best_path_used, all_text_combined) for the folder."""
    # paths to try, in priority order:
    paths = []
    for ext in ["article.nxml", "article_text.txt", "metadata.json"]:
        p = os.path.join(folder, ext)
        if os.path.isfile(p): paths.append(p)
    # bare-file style siblings
    for ext in [".html", ".pdf", ".txt", ".nxml"]:
        p = folder + ext
        if os.path.isfile(p): paths.append(p)
    # Always include PDF if available
    pdf_in_folder = os.path.join(folder, "article.pdf")
    if os.path.isfile(pdf_in_folder): paths.append(pdf_in_folder)

    text_parts = []
    used = []
    for p in paths:
        try:
            if p.endswith(".pdf"):
                out = subprocess.run(["pdftotext","-layout",p,"-"], capture_output=True, timeout=45)
                if out.returncode == 0:
                    text_parts.append(out.stdout.decode('utf-8', errors='ignore'))
                    used.append(p)
            else:
                with open(p, encoding='utf-8', errors='ignore') as f:
                    text_parts.append(f.read())
                used.append(p)
        except Exception as e:
            text_parts.append("")
    return used, "\n".join(text_parts)

# Normalization helpers
DASHES = "‐‑‒–—−­"
DASH_RE = re.compile("[" + DASHES + "]")
WS_RE = re.compile(r'\s+')

def nfc_strip(s):
    s = unicodedata.normalize('NFKC', s)
    s = DASH_RE.sub('-', s)
    s = WS_RE.sub(' ', s)
    return s

def quote_substring_in(quote, text):
    q = nfc_strip(quote)
    t = nfc_strip(text)
    if q in t:
        return True
    # also try with degree-sign variants
    for v in [q.replace('°C','oC'), q.replace('°C','o C'), q.replace('°C','ºC'), q.replace('°C','C')]:
        if v in t: return True
    # try without space before °C
    q2 = re.sub(r'\s+°', '°', q)
    if q2 in t: return True
    return False

def value_in_quote(value_raw, quote):
    """Check the numeric value appears in the quote."""
    q = nfc_strip(quote)
    v = nfc_strip(value_raw)
    if v in q: return True
    # Strip units
    vnum = re.findall(r'-?\d+\.?\d*', v)
    return all(n in q for n in vnum) if vnum else False

# Process rows
results = []
for r in rows:
    rid = r['id']
    url = r['source_url']
    folder = specific_subdir.get(rid) or overrides.get(rid) or m.get(url)
    compound = r['compound_name']
    quote = r['evidence_quote']
    value_raw = r['value_raw']
    notes = r.get('notes','')
    data_type = r['data_type']

    verdict = {"row_id": rid, "verdict": "verified_extraction", "reason": "", "details": ""}

    if not folder:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_doi_unrelated_paper"
        verdict["details"] = f"No folder mapping for URL {url}"
        results.append(verdict)
        continue

    try:
        used, text = fetch_text_for_folder(folder)
    except Exception as e:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_doi_unrelated_paper"
        verdict["details"] = f"Cannot read paper: {e}"
        results.append(verdict)
        continue

    if not text:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_doi_unrelated_paper"
        verdict["details"] = f"No text recovered from {folder}"
        results.append(verdict)
        continue

    # 1. DOI/PMC presence
    doi_token = None
    if url.startswith("https://doi.org/"):
        doi_token = url.split("doi.org/")[1]
    elif url.startswith("pmc:"):
        doi_token = url.split("pmc:")[1]
    elif url.startswith("https://www.ncbi.nlm.nih.gov/pubmed/"):
        doi_token = url.rsplit('/',1)[-1]
    doi_present = doi_token and (doi_token in text or doi_token.lower() in text.lower())

    # Quote check
    quote_present = quote_substring_in(quote, text)
    has_ellipsis = ('...' in quote) or ('…' in quote)
    has_template = quote.startswith("Table ") and ("MP" in quote or "BP" in quote) and ":" in quote[:30]

    val_in_quote_ok = value_in_quote(value_raw, quote) if quote else False

    # gather details
    details_bits = []
    details_bits.append(f"folder={folder}")
    details_bits.append(f"doi_token={doi_token} present={doi_present}")
    details_bits.append(f"quote_present={quote_present}")
    details_bits.append(f"value_in_quote={val_in_quote_ok}")

    # Verdict logic
    if not doi_present:
        # leave for manual check; mark for further inspection
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_doi_unrelated_paper"
        verdict["details"] = "; ".join(details_bits)
    elif not quote_present:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_evidence_quote_not_found"
        verdict["details"] = "; ".join(details_bits)
    elif has_ellipsis:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_evidence_quote_not_found"
        verdict["details"] = "ellipsis joining; " + "; ".join(details_bits)
    elif has_template:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_evidence_quote_not_found"
        verdict["details"] = "templated quote; " + "; ".join(details_bits)
    elif not val_in_quote_ok:
        verdict["verdict"] = "flagged_review"
        verdict["reason"] = "flagged_evidence_quote_not_found"
        verdict["details"] = "value missing from quote; " + "; ".join(details_bits)
    else:
        verdict["verdict"] = "verified_extraction"
        verdict["details"] = "; ".join(details_bits)
    results.append(verdict)

with open("_v5_tmp/auto_results.json","w") as f:
    json.dump(results, f, indent=2)

# Quick tally
ver = sum(1 for r in results if r["verdict"]=="verified_extraction")
fla = len(results)-ver
print(f"auto_tally: verified={ver} flagged={fla}")
for r in results:
    print(r["row_id"], r["verdict"], r["reason"])

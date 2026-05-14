import os, re, json, csv, unicodedata, sys

def normalize(s):
    s = unicodedata.normalize('NFKC', s)  # NFKC handles more compat
    for ch in ['‐','‑','‒','–','—','―','−','-']:  # all dashes
        s = s.replace(ch, '-')
    # primes / quotes
    for ch in ['‘','’','‚','‛','′']:
        s = s.replace(ch, "'")
    s = s.replace('″', "''").replace('‴', "'''")
    for ch in ['“','”','„','‟']:
        s = s.replace(ch, '"')
    # NBSP family
    for ch in ['\xa0',' ',' ',' ',' ',' ',' ']:
        s = s.replace(ch, ' ')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

BASE = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/corpora/full_168"
CSV_PATH = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/Trial3-full-sonnet46/_my_audit_batch_2.csv"
MAP_PATH = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/Trial3-full-sonnet46/url_to_folder_map.json"

with open(MAP_PATH) as f:
    url_map = json.load(f)

with open(CSV_PATH, newline='') as f:
    rows = list(csv.DictReader(f))

results = []
for row in rows:
    rid = row['id']
    url = row['source_url']
    quote = row['evidence_quote']
    val_raw = row['value_raw']
    compound = row['compound_name']
    folder_rel = url_map.get(url)
    if folder_rel and '|' in folder_rel:
        token = folder_rel.split('|')[-1]
        found = None
        try:
            for f_name in os.listdir(BASE):
                if token.lower() in f_name.lower():
                    found = f_name; break
        except Exception:
            pass
        folder_rel = found
    if folder_rel and folder_rel.startswith("corpora/full_168/"):
        folder_rel = folder_rel.replace("corpora/full_168/", "")
    folder_path = os.path.join(BASE, folder_rel) if folder_rel else None
    if not folder_path or not os.path.exists(folder_path):
        results.append({"id": rid, "url": url, "verdict": "flagged_review",
                        "reason": "flagged_paper_unreadable", "details": f"folder for {url} not found"})
        continue
    paper_path = None
    for fn in ["article_text.txt", "article.nxml"]:
        p = os.path.join(folder_path, fn)
        if os.path.exists(p):
            paper_path = p; break
    if not paper_path:
        results.append({"id": rid, "url": url, "verdict": "flagged_review",
                        "reason": "flagged_paper_unreadable", "details": f"no text in {folder_path}"})
        continue
    text = open(paper_path, errors='ignore').read()
    n_text = normalize(text)
    n_quote = normalize(quote)
    # DOI tail
    doi_tail = url.split('/')[-1] if 'doi.org' in url else url.replace('pmc:','')
    doi_present = doi_tail.lower() in n_text.lower() or doi_tail.lower() in folder_path.lower()
    # quote check (full)
    quote_found = n_quote in n_text
    # Try a substring match: pick a 60-char anchor from middle of quote
    anchor_found = False
    if not quote_found and len(n_quote) > 60:
        mid = len(n_quote) // 2
        anchor = n_quote[max(0, mid-30):mid+30]
        anchor_found = anchor in n_text
    # also try first 40 chars and last 40 chars
    head_found = n_quote[:40] in n_text if len(n_quote) >= 40 else False
    tail_found = n_quote[-40:] in n_text if len(n_quote) >= 40 else False
    # find longest matching prefix in n_text (skip if quote_found)
    longest_match_len = 0
    if not quote_found:
        # check shrinking prefix
        for start in range(0, max(1, len(n_quote)-30), 5):
            chunk = n_quote[start:start+60]
            if chunk in n_text:
                longest_match_len = max(longest_match_len, 60)
    # value in quote
    n_val = normalize(val_raw)
    val_core = re.sub(r'\s*°?\s*C\s*$', '', n_val).strip()
    val_core = re.sub(r'^\s*(?:mp|m\.p\.|Mp|Tm|MP|bp|Bp|BP)\s*:?\s*', '', val_core).strip()
    val_in_quote = (val_core in n_quote) or (n_val in n_quote)
    has_ellipsis = '...' in quote or '…' in quote
    results.append({
        "id": rid, "url": url, "folder": os.path.basename(folder_path),
        "doi_present": doi_present, "quote_found": quote_found,
        "head_found": head_found, "tail_found": tail_found,
        "anchor_found": anchor_found, "longest_match_len": longest_match_len,
        "val_in_quote": val_in_quote, "val_core": val_core,
        "has_ellipsis": has_ellipsis,
    })

print(json.dumps(results, indent=2))

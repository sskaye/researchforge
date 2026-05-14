#!/usr/bin/env python3
"""Phase 4 verifier helper - extracts contexts around quotes for verification."""
import csv, json, os, re, unicodedata, sys, html
from xml.sax.saxutils import unescape

WD = sys.argv[1] if len(sys.argv) > 1 else '/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev'
CSV = f'{WD}/Trial3-full-opus47/_my_audit_batch_1.csv'
MAP = f'{WD}/Trial3-full-opus47/url_to_folder_rewritten.json'

with open(MAP) as f:
    url_map = json.load(f)

extras = {
    "https://doi.org/10.1021/acs.joc.9b00711": "corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors.pdf",
    "https://doi.org/10.1021/jo061443+": "corpora/full_168/2006_Sharik_Total Synthesis of (−)-Normalindine via Addition of Metallated 4- Methyl-3-cyanopyridine to an Enantiopure Sulfinimine.pdf",
    "https://doi.org/10.1134/S107042802211001X": "corpora/full_168/023_PMC9790764_Synthesis_and_Properties_of_13-Disubstituted_Ureas_and_Their_Isosteric_Analogs_Containing_",
    "https://doi.org/10.1134/S1070428022030101": "corpora/full_168/183_PMC9007260_Synthesis_and_Antimicrobial_Antiplatelet_and_Anticoagulant_Activities_of_New_Isatin_Deivat",
    "https://doi.org/10.1021/acs.joc.0c02731": "corpora/full_168/2021_Moncho_The Chemistry of Short-Lived α‑Fluorocarbocations.pdf",
}
url_map.update(extras)

def strip_xml(s):
    """Decode hex entities and strip XML tags."""
    # Convert &#x000b0; -> 0xb0 char etc.
    def repl_ent(m):
        try:
            return chr(int(m.group(1), 16))
        except Exception:
            return m.group(0)
    s = re.sub(r'&#x([0-9A-Fa-f]+);', repl_ent, s)
    s = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), s)
    s = html.unescape(s)
    # Strip tags
    s = re.sub(r'<[^>]+>', ' ', s)
    return s

def normtxt(s):
    s = strip_xml(s)
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\s+', ' ', s).strip()
    for ch in ['‐', '‑', '‒', '–', '—', '―', '−', '⁃', '­']:
        s = s.replace(ch, '-')
    # Cyrillic look-alikes
    cyr = {'С': 'C', 'с': 'c', 'А': 'A', 'а': 'a', 'Е': 'E', 'е': 'e',
           'О': 'O', 'о': 'o', 'Р': 'P', 'р': 'p', 'Х': 'X', 'х': 'x',
           'В': 'B', 'Н': 'H', 'К': 'K', 'М': 'M', 'Т': 'T'}
    for k, v in cyr.items():
        s = s.replace(k, v)
    s = s.replace('ᴅ', 'D').replace('ʟ', 'L')
    s = s.replace('′', "'").replace('″', '"')
    # Remove control chars
    s = ''.join(ch for ch in s if ch == ' ' or not unicodedata.category(ch).startswith('C'))
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def get_paper_text(folder_rel):
    folder = os.path.join(WD, folder_rel)
    if folder.endswith('.pdf'):
        import subprocess
        try:
            r1 = subprocess.run(['pdftotext', '-layout', folder, '-'], capture_output=True, text=True, timeout=60)
            r2 = subprocess.run(['pdftotext', folder, '-'], capture_output=True, text=True, timeout=60)
            return (r1.stdout or '') + '\n\n=== NO LAYOUT ===\n\n' + (r2.stdout or '')
        except Exception as e:
            return f"[pdf error: {e}]"
    for f in ['article.nxml', 'article_text.txt']:
        p = os.path.join(folder, f)
        if os.path.exists(p):
            return open(p, encoding='utf-8', errors='replace').read()
    pdf = os.path.join(folder, 'article.pdf')
    if os.path.exists(pdf):
        import subprocess
        r1 = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True, timeout=60)
        r2 = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True, timeout=60)
        return (r1.stdout or '') + '\n\n=== NO LAYOUT ===\n\n' + (r2.stdout or '')
    return ""

with open(CSV) as f:
    rows = list(csv.DictReader(f))

results = []
for r in rows:
    rid = r['id']
    url = r['source_url']
    quote = r['evidence_quote']
    val_raw = r['value_raw']
    compound = r['compound_name']

    folder = url_map.get(url)
    if not folder:
        m = re.search(r'PMC\d+', url)
        if m:
            folder = url_map.get(f"pmc:{m.group(0)}")
    if not folder:
        results.append({'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_paper_unreadable', 'details': f'URL {url} not in map'})
        continue

    txt = get_paper_text(folder)
    if not txt or len(txt) < 100:
        results.append({'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_paper_unreadable', 'details': f'Empty text for {folder}'})
        continue

    # DOI / PMC check: use raw text, not normalized
    doi_ok = False
    pmcm = re.search(r'PMC\d+', folder)
    doim = re.search(r'10\.[0-9]{4,9}/[^/\s)]+', url)
    pmid_m = re.search(r'PMC\d+', url)

    if pmcm and (pmcm.group(0) in txt or pmcm.group(0).replace('PMC','') in txt):
        doi_ok = True
    if doim:
        di = doim.group(0).rstrip('/').rstrip(')').rstrip('+')
        if di in txt or di.lower() in txt.lower():
            doi_ok = True
        frag = di.split('/', 1)[-1]
        if frag and frag in txt:
            doi_ok = True
    if pmid_m and pmid_m.group(0) in txt:
        doi_ok = True

    nquote = normtxt(quote)
    ntxt = normtxt(txt)
    quote_in = nquote in ntxt

    nval = normtxt(val_raw)
    # Check each numeric token from the value appears in the quote
    val_nums = re.findall(r'\d+(?:[.,]\d+)?', nval)
    val_in_quote = all(n in nquote for n in val_nums) if val_nums else True

    has_ellipsis = '...' in quote or '…' in quote

    print(f"\n=== Row {rid} ===")
    print(f"  doi_ok={doi_ok}, quote_in_text={quote_in}, val_in_quote={val_in_quote}, ellipsis={has_ellipsis}")
    if not quote_in:
        first40 = nquote[:40]
        idx = ntxt.find(first40)
        print(f"  first40={first40!r} -> idx={idx}")
        if idx >= 0:
            slice_end = idx + len(nquote) + 30
            print(f"  paper slice ({slice_end-idx} chars): {ntxt[idx:slice_end]!r}")

    res = {'id': rid, 'verdict': 'verified_extraction', 'reason': '', 'details': ''}
    if not doi_ok:
        res = {'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_doi_unrelated_paper', 'details': 'URL identifier not found in paper text'}
    elif has_ellipsis:
        res = {'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_evidence_quote_not_found', 'details': 'ellipsis present'}
    elif not quote_in:
        res = {'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_evidence_quote_not_found', 'details': 'quote not substring of paper'}
    elif not val_in_quote:
        res = {'id': rid, 'verdict': 'flagged_review', 'reason': 'flagged_evidence_quote_not_found', 'details': f'quote missing value {val_raw}'}
    results.append(res)

print("\n\n=== JSON SUMMARY ===")
print(json.dumps(results, indent=2, ensure_ascii=False))

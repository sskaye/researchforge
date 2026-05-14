"""Phase-4 verifier for _my_audit_extra_batch_6.csv."""
import json, csv, re, unicodedata, subprocess, os, sys

PAPER_ROOT = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev'
TRIAL_DIR = os.path.join(PAPER_ROOT, 'Trial3-full-opus47')

with open(os.path.join(TRIAL_DIR, 'url_to_folder_built.json')) as f:
    URL_MAP = json.load(f)

# Override generic 'corpora/full_168' entries with discovered specific files
URL_MAP['https://doi.org/10.1021/jm3014162'] = 'corpora/full_168/2013_Zhou_Identification and Characterization of Small Molecules as Potent and Specific EPAC2 Antagonists.pdf'
URL_MAP['https://doi.org/10.1021/acs.joc.9b00711'] = 'corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors.pdf'
URL_MAP['https://doi.org/10.1021/acs.joc.0c02731'] = 'corpora/full_168/2021_Moncho_The Chemistry of Short-Lived α‑Fluorocarbocations.pdf'

def load_paper_text(source_url):
    rel = URL_MAP.get(source_url)
    if not rel:
        return None, None
    full = os.path.join(PAPER_ROOT, rel)
    if os.path.isdir(full):
        # Prefer article_text.txt because NXML markup splits chemistry tokens
        for cand in ('article_text.txt', 'article.nxml'):
            p = os.path.join(full, cand)
            if os.path.exists(p):
                with open(p, encoding='utf-8', errors='replace') as f:
                    s = f.read()
                if cand == 'article.nxml':
                    s = re.sub(r'<[^>]+>', ' ', s)
                return s, p
        pdfp = os.path.join(full, 'article.pdf')
        if os.path.exists(pdfp):
            r = subprocess.run(['pdftotext','-layout',pdfp,'-'], capture_output=True)
            return r.stdout.decode('utf-8', errors='replace'), pdfp
        for fn in os.listdir(full):
            if fn.endswith('.pdf'):
                p = os.path.join(full, fn)
                r = subprocess.run(['pdftotext','-layout',p,'-'], capture_output=True)
                return r.stdout.decode('utf-8', errors='replace'), p
        return None, full
    if os.path.isfile(full):
        if full.endswith('.pdf'):
            r = subprocess.run(['pdftotext','-layout',full,'-'], capture_output=True)
            return r.stdout.decode('utf-8', errors='replace'), full
        with open(full, encoding='utf-8', errors='replace') as f:
            return f.read(), full
    return None, full

def normalize_text(s):
    s = unicodedata.normalize('NFC', s)
    # fold all hyphen/dash variants
    for ch in ['‐','‑','‒','–','—','−','-']:
        s = s.replace(ch, '-')
    s = re.sub(r'\s+', ' ', s)
    return s

def normalize_hard(s):
    s = normalize_text(s)
    # fold primes / apostrophes
    s = s.replace('′',"'").replace('’',"'").replace('‘',"'").replace('`',"'")
    # fold subscript/superscript common: ¹²³ ⁰¹² etc - skip
    return s

def find_substring(haystack, needle):
    if not needle:
        return True
    h = normalize_text(haystack)
    n = normalize_text(needle)
    if n in h:
        return True
    h2 = normalize_hard(haystack)
    n2 = normalize_hard(needle)
    if n2 in h2:
        return True
    # try with degree-sign and spacing tolerant
    h3 = re.sub(r'\s','', h2)
    n3 = re.sub(r'\s','', n2)
    if n3 in h3:
        return True
    return False

def has_url(text, url):
    if 'doi.org/' in url:
        doi = url.split('doi.org/',1)[1]
        return doi.lower() in text.lower()
    if url.startswith('pmc:'):
        pmc = url.split(':',1)[1]
        return pmc.lower() in text.lower() or pmc[3:].lower() in text.lower()
    if url.startswith('legacy:'):
        return True
    return url.lower() in text.lower()

def verify_row(r, text):
    flags = []
    notes = []
    rid = r['id']
    url = r['source_url']
    ev = r['evidence_quote']
    vr = r['value_raw']
    cn = r['compound_name']

    if text is None:
        return ['flagged_paper_not_found'], 'paper file missing'

    if not has_url(text, url):
        flags.append('flagged_doi_unrelated_paper')

    # evidence quote checks
    if '...' in ev or '…' in ev:
        flags.append('flagged_evidence_quote_not_found')
        notes.append('ellipsis joins non-adjacent spans')
    elif not find_substring(text, ev):
        flags.append('flagged_evidence_quote_not_found')
        notes.append('quote not contiguous substring')
    else:
        # value_raw must be inside ev
        if vr and not find_substring(ev, vr):
            flags.append('flagged_evidence_quote_not_found')
            notes.append(f'value_raw "{vr}" not in evidence_quote')

    return flags, '; '.join(notes)

def main():
    with open(os.path.join(TRIAL_DIR, '_my_audit_extra_batch_6.csv')) as f:
        rows = list(csv.DictReader(f))
    out = []
    # Cache paper text by source_url
    cache = {}
    for r in rows:
        url = r['source_url']
        if url not in cache:
            cache[url] = load_paper_text(url)
        text, path = cache[url]
        flags, notes = verify_row(r, text)
        out.append({
            'id': r['id'],
            'flags': flags,
            'notes': notes,
            'paper_path': path,
            'compound_name': r['compound_name'],
            'value_raw': r['value_raw'],
        })
        print(f"id={r['id']:>5} flags={flags} notes={notes}")
    with open('/tmp/stage1_extra6.json','w') as f:
        json.dump(out, f, indent=2)
    print('---')
    print(f'{len(out)} rows; flagged: {sum(1 for o in out if o["flags"])}')

if __name__ == '__main__':
    main()

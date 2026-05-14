import os, subprocess, re, unicodedata, json, csv, sys

manual_overrides = {
    "https://doi.org/10.1021/jm3014162": ("pdf-file", "corpora/full_168/2013_Zhou_Identification and Characterization of Small Molecules as Potent and Specific EPAC2 Antagonists.pdf"),
    "https://doi.org/10.1021/acs.joc.9b00711": ("pdf-file", "corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors.pdf"),
    "legacy:2000_Brown_Melting_Point_and_Molecular_Symmetry.pdf": ("pdf-file", "corpora/full_168/2000_Brown_Melting Point and Molecular Symmetry.pdf"),
}

ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev"

with open(os.path.join(ROOT, 'Trial3-full-opus47/url_to_folder_built.json')) as f:
    url_map = json.load(f)

def get_text(url):
    folder = manual_overrides.get(url)
    if folder:
        kind, path = folder
    else:
        p = url_map.get(url)
        if not p:
            return None, None
        path = p
        full = os.path.join(ROOT, p)
        if os.path.isfile(full):
            kind = "pdf-file"
        else:
            kind = None
            for n in ('article.nxml', 'article_text.txt', 'article.pdf'):
                if os.path.isfile(os.path.join(full, n)):
                    kind = {'article.nxml':'nxml','article_text.txt':'txt','article.pdf':'pdf'}[n]
                    break

    if kind == 'pdf-file':
        full = os.path.join(ROOT, path)
        r = subprocess.run(['pdftotext','-layout','-q',full,'-'],capture_output=True,timeout=60)
        return r.stdout.decode('utf-8','replace'), full
    elif kind == 'nxml':
        full = os.path.join(ROOT, path, 'article.nxml')
        with open(full,'r',encoding='utf-8',errors='replace') as f:
            return f.read(), full
    elif kind == 'txt':
        full = os.path.join(ROOT, path, 'article_text.txt')
        with open(full,'r',encoding='utf-8',errors='replace') as f:
            return f.read(), full
    elif kind == 'pdf':
        full = os.path.join(ROOT, path, 'article.pdf')
        r = subprocess.run(['pdftotext','-layout','-q',full,'-'],capture_output=True,timeout=60)
        return r.stdout.decode('utf-8','replace'), full
    return None, None

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFKC', s)
    # Decode generic entities
    s = re.sub(r'&#x[0-9A-Fa-f]+;', lambda m: chr(int(m.group(0)[3:-1],16)), s)
    s = re.sub(r'&#[0-9]+;', lambda m: chr(int(m.group(0)[2:-1])), s)
    s = s.replace('&deg;','°').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&apos;',"'").replace('&nbsp;',' ')
    # Strip XML/HTML tags
    s = re.sub(r'<[^>]+>', ' ', s)
    # Cyrillic 'С' to Latin 'C'
    s = s.replace('С','C').replace('с','c')
    # All hyphen variants → '-'
    s = re.sub(r'[‐‑‒–—―−­\-]', '-', s)
    # 'o C' (PDF: degree-mark fell to baseline 'o') → '°C'
    s = re.sub(r'\bo\s*C\b', '°C', s)
    s = re.sub(r'º\s*C', '°C', s)
    s = re.sub(r'°\s*C', '°C', s)
    # Whitespace collapse
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def norm_loose(s):
    """Strip every space for very-loose substring containment check."""
    return re.sub(r'\s+', '', norm(s))

def substr_in(needle, hay):
    return norm(needle) in norm(hay)

if __name__ == '__main__':
    rows=[]
    with open(os.path.join(ROOT, 'Trial3-full-opus47/_my_audit_extra_batch_8.csv'), newline='') as f:
        for r in csv.DictReader(f):
            rows.append(r)

    target_id = sys.argv[1] if len(sys.argv)>1 else None
    for r in rows:
        if target_id and r['id'] != target_id:
            continue
        url = r['source_url']
        text, fpath = get_text(url)
        if text is None:
            print(f"{r['id']}: NO PAPER")
            continue
        ev = r['evidence_quote']
        print(f"=== id={r['id']} === path={fpath}")
        print(f"compound: {r['compound_name']}")
        print(f"value_raw: {r['value_raw']} | celsius: {r['value_celsius']} | data_type: {r['data_type']}")
        print(f"location: {r['evidence_location']}")
        print(f"quote: {ev[:300]}")
        in_paper = substr_in(ev, text)
        in_paper_loose = norm_loose(ev) in norm_loose(text)
        print(f"quote_in_paper(normalized): {in_paper} loose: {in_paper_loose}")
        vr = r['value_raw']
        nv = norm(vr)
        nt = norm(text)
        nv_loose = norm_loose(vr)
        nt_loose = norm_loose(text)
        i = nt.find(nv)
        il = nt_loose.find(nv_loose)
        if i >= 0:
            print(f"value_at: ...{nt[max(0,i-150):i+len(nv)+150]}...")
        elif il >= 0:
            print(f"value_at_loose: ...{nt_loose[max(0,il-150):il+len(nv_loose)+150]}...")
        else:
            print(f"value_NOT_in_paper: {vr}")
        doi_substr = url.replace('https://doi.org/','')
        if doi_substr.startswith('pmc:'):
            doi_substr = doi_substr.split(':',1)[1]
        elif doi_substr.startswith('legacy:'):
            doi_substr = ''
        if doi_substr:
            print(f"doi_in_paper: {doi_substr in text or doi_substr in nt}")
        print()

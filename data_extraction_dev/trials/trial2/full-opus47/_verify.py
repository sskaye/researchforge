import csv, os, subprocess, re, sys

ROOT = '/sessions/practical-gifted-babbage/mnt/data_extraction_dev/mp_bp_full_set/'
CSV_PATH = '/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/phase4_group_3.csv'

def normalize(s):
    s = s.replace(' ',' ').replace(' ',' ').replace('​','').replace(' ',' ').replace(' ',' ')
    for d in ['‐','‑','‒','–','—','−']:
        s = s.replace(d,'-')
    s = s.replace('°','°')
    s = re.sub(r'\s+',' ',s).strip()
    return s

def load_paper(paper_dir):
    full = os.path.join(ROOT, paper_dir)
    if paper_dir.endswith('.pdf'):
        out = subprocess.run(['pdftotext','-layout', full,'-'], capture_output=True, text=True)
        return out.stdout, 'pdf-standalone'
    if os.path.isdir(full):
        txt = os.path.join(full,'article_text.txt')
        if os.path.exists(txt):
            with open(txt) as f: return f.read(), 'pmc_text'
        nxml = os.path.join(full,'article.nxml')
        if os.path.exists(nxml):
            with open(nxml) as f: return f.read(), 'nxml'
    html_path = full + '.html'
    pdf_path = full + '.pdf'
    if os.path.exists(html_path):
        with open(html_path) as f: return f.read(), 'html'
    if os.path.exists(pdf_path):
        out = subprocess.run(['pdftotext','-layout', pdf_path,'-'], capture_output=True, text=True)
        return out.stdout, 'pdf'
    return None, 'missing'

with open(CSV_PATH) as f:
    rows = list(csv.DictReader(f))

for r in rows:
    rid = r['id']
    pdir = r['paper_dir']
    text, mode = load_paper(pdir)
    if text is None:
        print(f"{rid}: MISSING mode={mode} ({pdir})")
        continue
    q = r['evidence_quote']
    qn = normalize(q)
    tn = normalize(text)
    found = qn in tn
    cn = normalize(r['compound_name'])
    cn_found = cn in tn
    print(f"{rid}: mode={mode} q_found={found} cn_found={cn_found} len_text={len(text)} q={q[:100]!r}")

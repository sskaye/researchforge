import re, sys, os
paper = sys.argv[1]
base = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/'
for d in os.listdir(base):
    if d.startswith(paper+'_'):
        full = base + d
        break
text_path = full + '/article_text.txt'
with open(text_path) as f:
    t = f.read()
patterns = [
    r'\bm\.?\s?p\.?\s*[:=]?\s*[><~]?\s*\d+[\.\d]*[\-–—]?\s*\d*[\.\d]*\s*°?\s*C',
    r'\bM\.?\s?[Pp]\.?\s*[:=]?\s*[><~]?\s*\d+[\.\d]*[\-–—]?\s*\d*[\.\d]*\s*°?\s*C',
    r'\bb\.?\s?p\.?\s*[:=]?\s*[><~]?\s*\d+[\.\d]*[\-–—]?\s*\d*[\.\d]*\s*°?\s*C',
    r'melting\s+point[^.]{0,80}\d+[^.]{0,30}',
    r'boiling\s+point[^.]{0,80}\d+[^.]{0,30}',
]
for pat in patterns:
    for m in re.finditer(pat, t, re.IGNORECASE):
        s = max(0, m.start()-100); e = min(len(t), m.end()+50)
        print('PAT[', pat[:20], '] ::', repr(t[s:e].replace('\n', ' '))[:300])
        print()

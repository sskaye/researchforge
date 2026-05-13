"""Extract mp/bp values with surrounding context (compound name + value).
Quote includes the IUPAC name + (code) ... mp ... °C in one verbatim span."""
import re, os, sys, csv

base = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/'

PAPERS = {
    '064': '10.1016/j.cdc.2021.100820',
    '068': '10.3390/molecules31050844',
    '069': '10.3390/ijms27052306',
    '070': '10.3390/molecules31050862',
    '071': '10.3390/molecules31040599',
    '072': '10.3390/molecules31040655',
    '073': '10.1039/d6ra01520d',
    '074': '10.3390/ijms27042032',
    '075': '10.3390/antibiotics15020127',
    '076': '10.1016/j.heliyon.2024.e31798',
    '078': '10.55730/1300-0527.3324',
}

CIT = {
    '064': 'Chemical Data Collections, 2022, 37, 100820',
    '068': 'Molecules, 2026, 31(5), 844',
    '069': 'Int J Mol Sci, 2026, 27(5), 2306',
    '070': 'Molecules, 2026, 31(5), 862',
    '071': 'Molecules, 2026, 31(4), 599',
    '072': 'Molecules, 2026, 31(4), 655',
    '073': 'RSC Adv., 2026, 16(22), 19729-19742',
    '074': 'Int J Mol Sci, 2026, 27(4), 2032',
    '075': 'Antibiotics (Basel), 2026, 15(2), 127',
    '076': 'Heliyon, 2024, 10(11), e31798',
    '078': 'Turk J Chem, 2022, 46(2), 506-522',
}


def get_dir(paper):
    for d in os.listdir(base):
        if d.startswith(paper + '_'):
            return base + d


def find_iupac_name(text, code, mp_idx, max_lookback=600):
    """Find IUPAC name preceding the FIRST occurrence of (code) before mp_idx.
    The synthesis section header reads: 'NAME (code)\n White crystals, m.p. ...'
    So we want the (code) that is immediately followed by characterization text."""
    start = max(0, mp_idx - max_lookback)
    chunk = text[start:mp_idx]
    code_pat = rf'\(\s*{re.escape(code)}\s*\)'
    matches = list(re.finditer(code_pat, chunk))
    if not matches:
        return None
    # Prefer the FIRST (code) in the lookback window — it's the synthesis section header
    first = matches[0]
    name_end = first.start()
    name_chunk = chunk[:name_end]
    # Look for IUPAC start markers (bracketed/locant patterns)
    # Common synthesis section patterns:
    # "...prepared from... Synthesis of <NAME> (code)"
    # We need to find the start of the chemical name.
    # Heuristic: look for a sentence boundary (period+space+capital) or "Synthesis of"
    syn_match = list(re.finditer(r'\b(?:Synthesis of|of)\s+', name_chunk))
    if syn_match:
        name = name_chunk[syn_match[-1].end():].strip()
    else:
        # last sentence
        sentences = re.split(r'(?<=[a-z])\.\s+(?=[A-Z\d(\[])', name_chunk)
        name = sentences[-1].strip()
    # If name starts with section-procedure phrase, drop those
    name = re.sub(r'^(?:was synthesized.*?for\s+\d+[a-z]?\.|was prepared.*?\.)\s*', '', name)
    name = name.strip().strip(',;:.')
    if len(name) < 8:
        return None
    # Exclude pure NMR/numeric noise
    if re.search(r'\bC\s*Ar\b|\bppm\b|\bMHz\b|\bNMR\b|\bIR\b|\bcm\s*-1\b|\bC=O\b', name):
        return None
    # Drop if it looks like the synthesis paragraph body rather than name
    if re.match(r'^(?:Compound|To a|A solution|Yield|White|Solid)\b', name, re.IGNORECASE):
        return None
    return name


def extract_paper(paper):
    pdir = get_dir(paper)
    with open(pdir + '/article_text.txt') as f:
        t = f.read()
    rows = []
    # main pattern: (code) ... mp/M.P./m.p. value °C — code can be 1, 1a, 2a, 4a, 11, 12 etc
    pat = re.compile(
        r'\(\s*(\d{1,3}[a-z]?\d?)\s*\)[^.]{0,300}?'
        r'\b(?:M\.?\s?[Pp]\.?|mp|m\.p\.|Mp|MP|melting\s+point|of)\s*[:=]?\s*'
        r'(>?\s*\d+(?:\.\d+)?(?:\s*[–—\-]\s*\d+(?:\.\d+)?)?)'
        r'\s*°?\s*C'
    )
    seen_starts = set()
    for m in pat.finditer(t):
        code = m.group(1)
        value_raw = m.group(2).strip().replace(' ', '')
        full_quote = t[m.start():m.end()]
        if m.start() in seen_starts:
            continue
        seen_starts.add(m.start())
        name = find_iupac_name(t, code, m.start() + 20)
        if not name:
            continue
        # Reject if name still looks like only a code or class-only
        if re.match(r'^(?:[Cc]arbohydrazide|[Cc]arboxamide|[Cc]omplex|[Cc]ompound|[Cc]omplex)\s+\d', name):
            continue
        # Reject if name is mostly NMR noise
        if re.search(r'\b(?:H NMR|13 C NMR|ppm|MHz|δ\s)', name):
            continue
        rows.append({
            'paper': paper,
            'doi': PAPERS[paper],
            'code': code,
            'name': name,
            'value_raw': value_raw + ' °C',
            'quote': full_quote,
            'start': m.start(),
        })
    return rows


def parse_value(value_raw):
    """Parse value_raw like '188-190' or '188-190 °C' or '>360' into (val, vmin, vmax, relation)."""
    s = value_raw.replace('°C', '').strip()
    relation = '='
    if s.startswith('>'):
        relation = '>'
        s = s[1:].strip()
    elif s.startswith('<'):
        relation = '<'
        s = s[1:].strip()
    # range?
    rm = re.match(r'^([\d.]+)\s*[–—\-]\s*([\d.]+)$', s)
    if rm:
        a = float(rm.group(1))
        b = float(rm.group(2))
        return ((a + b) / 2, a, b, relation)
    try:
        v = float(s)
        return (v, None, None, relation)
    except ValueError:
        return (None, None, None, relation)


if __name__ == '__main__':
    out_rows = []
    next_id = 1
    for p in sorted(PAPERS.keys()):
        rs = extract_paper(p)
        print(f'## Paper {p}: {len(rs)} rows')
        for r in rs[:30]:
            print(f"  code={r['code']} | name={r['name'][:80] if r['name'] else None} | val={r['value_raw']}")

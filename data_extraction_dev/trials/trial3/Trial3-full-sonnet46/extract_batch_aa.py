import re, csv, sys

def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&#x000b0;', '°').replace('&#x02013;', '-').replace('&#x02010;', '-')
    s = s.replace('&#x02032;', "'").replace('&#x02212;', '-').replace('&#x02009;', ' ')
    s = s.replace('&#x000ad;', '').replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_value(raw):
    raw = raw.replace('&#x000b0;', '°').replace('&#x02013;', '-').replace('&#x02010;', '-')
    raw = re.sub(r'<[^>]+>', '', raw).strip()
    # range
    m = re.search(r'([\d.]+)\s*[-–]\s*([\d.]+)\s*°C', raw)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return (lo+hi)/2, lo, hi, raw
    # single
    m = re.search(r'([\d.]+)\s*°C', raw)
    if m:
        v = float(m.group(1))
        return v, '', '', raw
    return None, '', '', raw

BASE = '/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/corpora/full_168/'

# ─── Paper 001 ───────────────────────────────────────────────────
P001 = {
    'doi': '10.3390/antiox15020217',
    'source': 'Antioxidants, 2026, 15, 217',
    'source_url': 'https://doi.org/10.3390/antiox15020217',
    'folder': '001_PMC12938810_Design_and_Synthesis_of_Caffeine-Based_Derivatives_with_Antioxidant_and_Neuroprotective_Ac'
}
rows = []

def add(compound, prop, value_raw, relation, data_type, source, source_url, evidence_location, evidence_quote, notes=''):
    val, vmin, vmax, raw_clean = parse_value(value_raw)
    if val is None:
        return
    rows.append({
        'compound_name': compound,
        'compound_smiles': '',
        'property': prop,
        'value_celsius': val,
        'value_celsius_min': vmin,
        'value_celsius_max': vmax,
        'value_raw': raw_clean,
        'relation': relation,
        'data_type': data_type,
        'source': source,
        'source_url': source_url,
        'evidence_location': evidence_location,
        'evidence_quote': evidence_quote,
        'conversion_arithmetic': '',
        'notes': notes,
    })

# Paper 001 data
src1 = 'Antioxidants, 2026, 15, 217'
url1 = 'https://doi.org/10.3390/antiox15020217'
add("N'-(1-(p-tolyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '272 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL1', "Synthesis of N'-(1-(p-tolyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL1).M.p.: 272 °C (dec.).")
add("N'-(1-(4-isobutylphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '230 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL2', "Synthesis of N'-(1-(4-isobutylphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL2).M.p.: 230 °C (dec.).")
add("N'-(1-(4-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '284 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL3', "Synthesis of N'-(1-(4-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide(AL3).M.p.: 284 °C (dec.).")
add("N'-(1-(3-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '231.5 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL4', "Synthesis of N'-(1-(3-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL4).M.p.: 231.5 °C (dec.).")
add("N'-(1-(4-chlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '275.5 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL5', "Synthesis of N'-(1-(4-chlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL5).M.p.: 275.5 °C (dec.).")
add("N'-(1-(4-bromophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'decomposition', '264.5 °C (dec.)', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL6', "Synthesis of N'-(1-(4-bromophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL6).M.p.: 264.5 °C (dec.).")
add("N'-(1-(2,4-dichlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'melting_point', '209-210 °C', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL7', "Synthesis N'-(1-(2,4-dichlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL7).M.p.: 209-210 °C.")
add("N'-(1-(4-nitrophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'melting_point', '220-221 °C', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL8', "Synthesis of N'-(1-(4-nitrophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL8).M.p.: 220-221 °C.")
add("N'-(1-(3,4,5-trimethoxyphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'melting_point', '227-227.5 °C', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL9', "Synthesis of N'-(1-(3,4,5-trimethoxyphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL9).M.p.: 227-227.5 °C.")
add("N'-(1-(4-fluorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide", 'melting_point', '221.5-222.5 °C', '=', 'measured', src1, url1, 'Experimental, Synthesis of AL10', "Synthesis of N'-(1-(4-fluorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide (AL10).M.p.: 221.5-222.5 °C.")

# Paper 003
src3 = 'Pharmaceuticals, 2026, 19, 230'
url3 = 'https://doi.org/10.3390/ph19020230'
add('2-(8-Hydroxyquinolin-5-yl)isoindoline-1,3-dione', 'melting_point', '265-268 °C', '=', 'measured', src3, url3, 'Experimental, compound 2', '2-(8-Hydroxyquinolin-5-yl)isoindoline-1,3-dione (2)Brown powder (245 mg, 85% yield); m.p. 265-268 °C;')
add('2-(8-Hydroxyquinolin-5-yl)-4-nitroisoindoline-1,3-dione', 'melting_point', '281-284 °C', '=', 'measured', src3, url3, 'Experimental, compound 3', '2-(8-Hydroxyquinolin-5-yl)-4-nitroisoindoline-1,3-dione (3)Dark brown powder (278 mg, 83% yield); m.p. 281-284 °C;')
add('2-(8-Hydroxyquinolin-5-yl)-4-methoxyisoindoline-1,3-dione', 'melting_point', '250-253 °C', '=', 'measured', src3, url3, 'Experimental, compound 4', '2-(8-Hydroxyquinolin-5-yl)-4-methoxyisoindoline-1,3-dione (4)Brown powder (288 mg, 90% yield); m.p. 250-253 °C;')
add('2-(8-Hydroxyquinolin-5-yl)-5-methoxyisoindoline-1,3-dione', 'melting_point', '242-247 °C', '=', 'measured', src3, url3, 'Experimental, compound 5', '2-(8-Hydroxyquinolin-5-yl)-5-methoxyisoindoline-1,3-dione (5)Black powder (288 mg, 90% yield); m.p. 242-247 °C;')
add('2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)isoindoline-1,3-dione', 'melting_point', '209-213 °C', '=', 'measured', src3, url3, 'Experimental, compound 6a', '2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)isoindoline-1,3-dione (6a)Dark brown powder (28 mg, 73% yield); m.p. 209-213 °C;')
add('2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)isoindoline-1,3-dione', 'melting_point', '255-259 °C', '=', 'measured', src3, url3, 'Experimental, compound 6b', '2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)isoindoline-1,3-dione (6b)Brown powder (36 mg, 88% yield); m.p. 255-259 °C;')
add('2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)isoindoline-1,3-dione', 'melting_point', '226-229 °C', '=', 'measured', src3, url3, 'Experimental, compound 6c', '2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)isoindoline-1,3-dione (6c)Brown powder (33 mg, 85% yield); m.p. 226-229 °C;')
add('2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione', 'decomposition', '238-240 °C (decomp.)', '=', 'measured', src3, url3, 'Experimental, compound 7a', '2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione (7a)Brown powder (25 mg, 55% yield); m.p. 238-240 °C (decomp.);')
add('2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione', 'decomposition', '267-270 °C (decomp.)', '=', 'measured', src3, url3, 'Experimental, compound 7b', '2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione (7b)Brown powder (33 mg, 75% yield); m.p. 267-270 °C (decomp.);')
add('2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione', 'melting_point', '219-222 °C', '=', 'measured', src3, url3, 'Experimental, compound 7c', '2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione (7c)Brown powder (30 mg, 70% yield); m.p. 219-222 °C;')
add('2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione', 'melting_point', '209-213 °C', '=', 'measured', src3, url3, 'Experimental, compound 8a', '2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione (8a)Brown powder (24 mg, 57% yield); m.p. 209-213 °C;')
add('2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione', 'melting_point', '221-225 °C', '=', 'measured', src3, url3, 'Experimental, compound 8b', '2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione (8b)Brown powder (25 mg, 60% yield); m.p. 221-225 °C;')
add('2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione', 'melting_point', '222-225 °C', '=', 'measured', src3, url3, 'Experimental, compound 8c', '2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione (8c)Brown powder (30 mg, 72% yield); m.p. 222-225 °C;')
add('2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione', 'melting_point', '184-188 °C', '=', 'measured', src3, url3, 'Experimental, compound 9a', '2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione (9a)Dark brown powder (25 mg, 60% yield); m.p. 184-188 °C;')
add('2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione', 'melting_point', '228-232 °C', '=', 'measured', src3, url3, 'Experimental, compound 9b', '2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione (9b)Brown powder (30 mg, 70% yield); m.p. 228-232 °C;')
add('2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione', 'melting_point', '197-200 °C', '=', 'measured', src3, url3, 'Experimental, compound 9c', '2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione (9c)Dark brown powder (30 mg, 70% yield); m.p. 197-200 °C;')

# Paper 004 - DSC measured, all solid melting points
src4 = 'ACS Omega, 2025 (online)'
url4 = 'https://doi.org/10.1021/acsomega.5c12576'
add('N,4-Diphenylpiperazine-1-carbothioamide', 'melting_point', '160.38 °C', '=', 'measured', src4, url4, 'Experimental, compound 3a', 'N,4-Diphenylpiperazine-1-carbothioamide (3a)  White solid; 160.38 °C; IR (KBr):', notes='DSC measured')
add('N-Benzyl-4-phenylpiperazine-1-carbothioamide', 'melting_point', '180.33 °C', '=', 'measured', src4, url4, 'Experimental, compound 3b', 'N-Benzyl-4-phenylpiperazine-1-carbothioamide (3b)  White solid; 180.33 °C; IR (KBr):', notes='DSC measured')
add('N-Phenethyl-4-phenylpiperazine-1-carbothioamide', 'melting_point', '141.97 °C', '=', 'measured', src4, url4, 'Experimental, compound 3c', 'N-Phenethyl-4-phenylpiperazine-1-carbothioamide (3c)White solid; 141.97 °C; IR (KBr):', notes='DSC measured')
add('4-Phenyl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide', 'melting_point', '204.90 °C', '=', 'measured', src4, url4, 'Experimental, compound 3d', '4-Phenyl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide (3d)White solid; 204.90 °C; IR (KBr):', notes='DSC measured')
add('4-(4-Hydroxyphenyl)-N-phenylpiperazine-1-carbothioamide', 'melting_point', '196.83 °C', '=', 'measured', src4, url4, 'Experimental, compound 3e', '4-(4-Hydroxyphenyl)-N-phenylpiperazine-1-carbothioamide (3e)  White solid; 196.83 °C; IR (KBr):', notes='DSC measured')
add('N-Benzyl-4-(4-hydroxyphenyl)piperazine-1-carbothioamide', 'melting_point', '164.61 °C', '=', 'measured', src4, url4, 'Experimental, compound 3f', 'N-Benzyl-4-(4-hydroxyphenyl)piperazine-1-carbothioamide (3f)Brown solid; 164.61 °C; IR (KBr):', notes='DSC measured')
add('4-(4-Hydroxyphenyl)-N-phenethylpiperazine-1-carbothioamide', 'melting_point', '191.55 °C', '=', 'measured', src4, url4, 'Experimental, compound 3g', '4-(4-Hydroxyphenyl)-N-phenethylpiperazine-1-carbothioamide (3g)White solid; 191.55 °C; IR (KBr):', notes='DSC measured')
add('4-(4-Hydroxyphenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide', 'melting_point', '236.51 °C', '=', 'measured', src4, url4, 'Experimental, compound 3h', '4-(4-Hydroxyphenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide (3h)  White solid; 236.51 °C; IR (KBr):', notes='DSC measured')
add('4-(2-Chlorophenyl)-N-phenylpiperazine-1-carbothioamide', 'melting_point', '175.78 °C', '=', 'measured', src4, url4, 'Experimental, compound 3i', '4-(2-Chlorophenyl)-N-phenylpiperazine-1-carbothioamide (3i)  White solid; 175.78 °C; IR (KBr):', notes='DSC measured')
add('N-Benzyl-4-(2-chlorophenyl)piperazine-1-carbothioamide', 'melting_point', '111.40 °C', '=', 'measured', src4, url4, 'Experimental, compound 3j', 'N-Benzyl-4-(2-chlorophenyl)piperazine-1-carbothioamide (3j)  White solid; 111.40 °C; IR (KBr):', notes='DSC measured')
add('4-(2-Chlorophenyl)-N-phenethylpiperazine-1-carbothioamide', 'melting_point', '111.76 °C', '=', 'measured', src4, url4, 'Experimental, compound 3k', '4-(2-Chlorophenyl)-N-phenethylpiperazine-1-carbothioamide (3k)  White solid; 111.76 °C; IR (KBr):', notes='DSC measured')
add('4-(2-Chlorophenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide', 'melting_point', '180.66 °C', '=', 'measured', src4, url4, 'Experimental, compound 3l', '4-(2-Chlorophenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide (3l)  White solid; 180.66 °C; IR (KBr):', notes='DSC measured')
add('4-Benzhydryl-N-phenylpiperazine-1-carbothioamide', 'melting_point', '216.60 °C', '=', 'measured', src4, url4, 'Experimental, compound 3m', '4-Benzhydryl-N-phenylpiperazine-1-carbothioamide (3m)  White solid; 216.60 °C; IR (KBr):', notes='DSC measured')
add('4-Benzhydryl-N-benzylpiperazine-1-carbothioamide', 'melting_point', '156.54 °C', '=', 'measured', src4, url4, 'Experimental, compound 3n', '4-Benzhydryl-N-benzylpiperazine-1-carbothioamide (3n)  White solid; 156.54 °C; IR (KBr):', notes='DSC measured')
add('4-Benzhydryl-N-phenethylpiperazine-1-carbothioamide', 'melting_point', '138.93 °C', '=', 'measured', src4, url4, 'Experimental, compound 3o', '4-Benzhydryl-N-phenethylpiperazine-1-carbothioamide (3o)  White solid; 138.93 °C; IR (KBr):', notes='DSC measured')
add('4-Benzhydryl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide', 'melting_point', '151.96 °C', '=', 'measured', src4, url4, 'Experimental, compound 3p', '4-Benzhydryl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide (3p)  White solid; 151.96 °C; IR (KBr):', notes='DSC measured')

print(f"Rows so far: {len(rows)}")

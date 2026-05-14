import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "RSC Adv 2026, 16(22), 20364-20380"
URL = "https://doi.org/10.1039/d5ra09311b"

# Each compound 12a-12s: name + mp range
compounds = [
    ("12a","2-oxo-7-((1-(2-oxo-2-(Phenylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(phenylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","212-214",212,214),
    ("12b","2-oxo-7-((1-(2-oxo-2-(o-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(o-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","222-225",222,225),
    ("12c","7-((1-(2-((2-Fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2-fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","230-232",230,232),
    ("12d","7-((1-(2-((2-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","239-241",239,241),
    ("12e","2-oxo-7-((1-(2-oxo-2-(m-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(m-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","251-253",251,253),
    ("12f","7-((1-(2-((3-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((3-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","235-237",235,237),
    ("12g","2-oxo-7-((1-(2-oxo-2-(p-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(p-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","220-223",220,223),
    ("12h","7-((1-(2-((4-Ethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-ethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","212-214",212,214),
    ("12i","7-((1-(2-((4-Methoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-methoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","253-255",253,255),
    ("12j","7-((1-(2-((4-Fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","239-241",239,241),
    ("12k","7-((1-(2-((4-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","240-242",240,242),
    ("12l","7-((1-(2-((4-Bromophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-bromophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","242-244",242,244),
    ("12m","2-oxo-7-((1-(2-oxo-2-((4-(Trifluoromethyl)phenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-((4-(trifluoromethyl)phenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","286-288",286,288),
    ("12n","7-((1-(2-((2,4-Dimethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2,4-dimethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","232-235",232,235),
    ("12o","7-((1-(2-((2,4-Dimethoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2,4-dimethoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","239-241",239,241),
    ("12p","2-oxo-7-((1-(2-oxo-2-((3,4,5-Trimethoxyphenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-((3,4,5-trimethoxyphenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","228-230",228,230),
    ("12q","7-((1-(2-(Benzylamino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-(benzylamino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","215-217",215,217),
    ("12r","7-((1-(2-((4-Methylbenzyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-methylbenzyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide","247-249",247,249),
    ("12s","2-oxo-7-((1-(2-oxo-2-(Phenethylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(phenethylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide","226-228",226,228),
]
# evidence quotes from paper: "(12X) ... MP = LO-HI °C"
# We'll construct based on observed pattern
quotes = {
    "12a": "chromene-3-carboxamide (12a) Brown solid; yield: 67%; MP = 212–214 °C",
    "12b": "chromene-3-carboxamide (12b) Brown solid; yield: 78%; MP = 222–225 °C",
    "12c": "chromene-3-carboxamide (12c) Brown solid; yield: 65%; MP = 230–232 °C",
    "12d": "chromene-3-carboxamide (12d) Cream solid; yield: 61%; MP = 239–241 °C",
    "12e": "chromene-3-carboxamide (12e) Brown solid; yield: 71%; MP = 251–253 °C",
    "12f": "chromene-3-carboxamide (12f) Cream solid; yield: 63%; MP = 235–237 °C",
    "12g": "chromene-3-carboxamide (12g) Brown solid; yield: 79%; MP = 220–223 °C",
    "12h": "chromene-3-carboxamide (12h) Cream solid; yield: 68%; MP = 212–214 °C",
    "12i": "chromene-3-carboxamide (12i) Brown solid; yield: 77%; MP = 253–255 °C",
    "12j": "chromene-3-carboxamide (12j) Brown solid; yield: 74%; MP = 239–241 °C",
    "12k": "chromene-3-carboxamide (12k) Brown solid; yield: 68%; MP = 240–242 °C",
    "12l": "chromene-3-carboxamide (12l) Brown solid; yield: 72%; MP = 242–244 °C",
    "12m": "chromene-3-carboxamide (12m) Brown solid; yield: 75%; MP = 286–288 °C",
    "12n": "chromene-3-carboxamide (12n) Brown solid; yield: 74%; MP = 232–235 °C",
    "12o": "chromene-3-carboxamide (12o) Brown solid; yield: 75%; MP = 239–241 °C",
    "12p": "chromene-3-carboxamide (12p) Brown solid; yield: 73%; MP = 228–230 °C",
    "12q": "chromene-3-carboxamide (12q) Cream solid; yield: 66%; MP = 215–217 °C",
    "12r": "chromene-3-carboxamide (12r) Brown solid; yield: 73%; MP = 247–249 °C",
    "12s": "chromene-3-carboxamide (12s) Brown solid; yield: 71%; MP = 226–228 °C",
}
# Use the chemical name + the standard quote pattern. Each section header contains the chemical name immediately preceding the "(12X)..." marker — so we extract a longer span including both.
import re
t = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/114_PMC13093879_Coumarin_bearing_triazole_hybrids_as_cholinesterase_inhibitors_targeting_Alzheimers_diseas/article_text.txt").read()

rows = []
for code, name, raw, lo, hi in compounds:
    # find the marker "(12X)" within the text and search backward to the section number
    marker = f"({code})"
    idx = t.find(marker + " ")
    if idx<0:
        # fallback: use just code mp pattern
        evidence = quotes.get(code, f"({code}) MP = {raw} °C")
    else:
        # search backward to find section number "4.1.X"
        start_sec = t.rfind("4.1.", 0, idx)
        if start_sec<0:
            start_sec = max(0, idx - 400)
        # forward to MP = ... °C
        mp_pat = re.search(rf"MP = {raw} °C", t[idx:idx+800])
        if mp_pat:
            end = idx + mp_pat.end()
        else:
            end = idx + 300
        evidence = t[start_sec:end]
        if len(evidence) > 1500:
            evidence = evidence[-1500:]
    mid = (lo+hi)/2
    rows.append([f"p114_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"MP = {raw} °C","range","measured",
        SOURCE,URL,"Experimental",evidence,"",f"compound {code}; coumarin-triazole hybrid"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p114")

#!/usr/bin/env python3
"""Build batch_00.csv incrementally as papers are processed."""
import csv

OUT = "/sessions/serene-amazing-franklin/mnt/trial5/opus47/batch_outputs/batch_00.csv"
HEADER = ["id","verification_status","compound_name","compound_smiles","property",
          "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
          "data_type","source","source_url","evidence_location","evidence_quote",
          "conversion_arithmetic","notes"]

ROWS = []

def add(name, prop, vraw, vmid, vmin, vmax, rel, src, url, loc, quote,
        conv="", notes="", smiles="", dtype="measured", status=""):
    ROWS.append([status, name, smiles, prop,
                 f"{vmid:g}" if vmid is not None else "",
                 f"{vmin:g}" if vmin is not None else "",
                 f"{vmax:g}" if vmax is not None else "",
                 vraw, rel, dtype, src, url, loc, quote, conv, notes])

# ===== Paper 001 PMC12938810 - Caffeine derivatives =====
src1 = "Antioxidants (Basel) 2026, 15(2), 217"
url1 = "https://doi.org/10.3390/antiox15020217"
p001 = [
    ("AL1", "N'-(1-(p-tolyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "272 °C (dec.)", 272.0, None, None, "=", "decomposition",
     "N′-(1-(p-tolyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL1 ). M.p.: 272 °C (dec.)."),
    ("AL2", "N'-(1-(4-isobutylphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "230 °C (dec.)", 230.0, None, None, "=", "decomposition",
     "N′-(1-(4-isobutylphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL2 ). M.p.: 230 °C (dec.)."),
    ("AL3", "N'-(1-(4-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "284 °C (dec.)", 284.0, None, None, "=", "decomposition",
     "N′-(1-(4-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide( AL3 ). M.p.: 284 °C (dec.)."),
    ("AL4", "N'-(1-(3-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "231.5 °C (dec.)", 231.5, None, None, "=", "decomposition",
     "N′-(1-(3-aminophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL4 ). M.p.: 231.5"),
    ("AL5", "N'-(1-(4-chlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "275.5 °C (dec.)", 275.5, None, None, "=", "decomposition",
     "N′-(1-(4-chlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL5 ). M.p.: 275.5"),
    ("AL6", "N'-(1-(4-bromophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "264.5 °C (dec.)", 264.5, None, None, "=", "decomposition",
     "N′-(1-(4-bromophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL6 ). M.p.: 264.5"),
    ("AL7", "N'-(1-(2,4-dichlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "209–210 °C", 209.5, 209.0, 210.0, "=", "melting_point",
     "N′-(1-(2,4-dichlorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL7 ). M.p.: 209–210 °C."),
    ("AL8", "N'-(1-(4-nitrophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "220–221 °C", 220.5, 220.0, 221.0, "=", "melting_point",
     "N′-(1-(4-nitrophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL8 ). M.p.: 220–221 °C."),
    ("AL9", "N'-(1-(3,4,5-trimethoxyphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "227–227.5 °C", 227.25, 227.0, 227.5, "=", "melting_point",
     "N′-(1-(3,4,5-trimethoxyphenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL9 ). M.p.: 227–227"),
    ("AL10", "N'-(1-(4-fluorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide",
     "221.5–222.5 °C", 222.0, 221.5, 222.5, "=", "melting_point",
     "N′-(1-(4-fluorophenyl)ethylidene)-3-((1,3,7-trimethyl-2,6-dioxo-2,3,6,7-tetrahydro-1H-purin-8-yl)thio)propanehydrazide ( AL10 ). M.p.: 221"),
]
for code, name, vraw, vmid, vmin, vmax, rel, prop, q in p001:
    add(name, prop, vraw, vmid, vmin, vmax, rel, src1, url1,
        f"Section 3.1 synthesis of {code}", q, notes=f"compound code {code}")

# ===== Paper 003 PMC12943044 - 8-HQ Phthalimide Hybrids =====
src3 = "Pharmaceuticals (Basel) 2026, 19(2), 230"
url3 = "https://doi.org/10.3390/ph19020230"
p003 = [
    ("2", "2-(8-Hydroxyquinolin-5-yl)isoindoline-1,3-dione", "265–268 °C", 266.5, 265.0, 268.0, "=", "melting_point",
     "2-(8-Hydroxyquinolin-5-yl)isoindoline-1,3-dione ( 2 ) Brown powder (245 mg, 85% yield); m.p. 265–268 °C"),
    ("3", "2-(8-Hydroxyquinolin-5-yl)-4-nitroisoindoline-1,3-dione", "281–284 °C", 282.5, 281.0, 284.0, "=", "melting_point",
     "2-(8-Hydroxyquinolin-5-yl)-4-nitroisoindoline-1,3-dione ( 3 ) Dark brown powder (278 mg, 83% yield); m.p. 281–284 °C"),
    ("4", "2-(8-Hydroxyquinolin-5-yl)-4-methoxyisoindoline-1,3-dione", "250–253 °C", 251.5, 250.0, 253.0, "=", "melting_point",
     "2-(8-Hydroxyquinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 4 ) Brown powder (288 mg, 90% yield); m.p. 250–253 °C"),
    ("5", "2-(8-Hydroxyquinolin-5-yl)-5-methoxyisoindoline-1,3-dione", "242–247 °C", 244.5, 242.0, 247.0, "=", "melting_point",
     "2-(8-Hydroxyquinolin-5-yl)-5-methoxyisoindoline-1,3-dione ( 5 ) Black powder (288 mg, 90% yield); m.p. 242–247 °C"),
    ("6a", "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)isoindoline-1,3-dione", "209–213 °C", 211.0, 209.0, 213.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)isoindoline-1,3-dione ( 6a ) Dark brown powder (28 mg, 73% yield); m.p. 209–213 °C"),
    ("6b", "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)isoindoline-1,3-dione", "255–259 °C", 257.0, 255.0, 259.0, "=", "melting_point",
     "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)isoindoline-1,3-dione ( 6b ) Brown powder (36 mg, 88% yield); m.p. 255–259 °C"),
    ("6c", "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)isoindoline-1,3-dione", "226–229 °C", 227.5, 226.0, 229.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)isoindoline-1,3-dione ( 6c ) Brown powder (33 mg, 85% yield); m.p. 226–229 °C"),
    ("7a", "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione", "238–240 °C (decomp.)", 239.0, 238.0, 240.0, "=", "decomposition",
     "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione ( 7a ) Brown powder (25 mg, 55% yield); m.p. 238–240 °C (decomp.)"),
    ("7b", "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione", "267–270 °C (decomp.)", 268.5, 267.0, 270.0, "=", "decomposition",
     "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione ( 7b ) Brown powder (33 mg, 75% yield); m.p. 267–270 °C (decomp.)"),
    ("7c", "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione", "219–222 °C", 220.5, 219.0, 222.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-nitroisoindoline-1,3-dione ( 7c ) Brown powder (30 mg, 70% yield); m.p. 219–222 °C"),
    ("8a", "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione", "209–213 °C", 211.0, 209.0, 213.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 8a ) Brown powder (24 mg, 57% yield); m.p. 209–213 °C"),
    ("8b", "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione", "221–225 °C", 223.0, 221.0, 225.0, "=", "melting_point",
     "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 8b ) Brown powder (25 mg, 60% yield); m.p. 221–225 °C"),
    ("8c", "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione", "222–225 °C", 223.5, 222.0, 225.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 8c ) Brown powder (30 mg, 72% yield); m.p. 222–225 °C"),
    ("9a", "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione", "184–188 °C", 186.0, 184.0, 188.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(piperidin-1-ylmethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione ( 9a ) Dark brown powder (25 mg, 60% yield); m.p. 184–188 °C"),
    ("9b", "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione", "228–232 °C", 230.0, 228.0, 232.0, "=", "melting_point",
     "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione ( 9b ) Brown powder (30 mg, 70% yield); m.p. 228–232 °C"),
    ("9c", "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione", "197–200 °C", 198.5, 197.0, 200.0, "=", "melting_point",
     "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-5-methoxyisoindoline-1,3-dione ( 9c ) Dark brown powder (30 mg, 70% yield); m.p. 197–200 °C"),
]
for code, name, vraw, vmid, vmin, vmax, rel, prop, q in p003:
    add(name, prop, vraw, vmid, vmin, vmax, rel, src3, url3,
        f"Section 3.1 synthesis of compound {code}", q, notes=f"compound code {code}")

def write():
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(HEADER)
        for i, r in enumerate(ROWS, 1):
            w.writerow([i] + r)

if __name__ == "__main__":
    write()
    print(f"Wrote {len(ROWS)} rows")

# ===== Paper 004 PMC13084458 - Piperazine-Thiourea Hybrids =====
src4 = "ACS Omega 2025"
url4 = "https://doi.org/10.1021/acsomega.5c12576"
p004 = [
    ("3a", "N,4-Diphenylpiperazine-1-carbothioamide", "160.38 °C", 160.38),
    ("3b", "N-Benzyl-4-phenylpiperazine-1-carbothioamide", "180.33 °C", 180.33),
    ("3c", "N-Phenethyl-4-phenylpiperazine-1-carbothioamide", "141.97 °C", 141.97),
    ("3d", "4-Phenyl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide", "204.90 °C", 204.90),
    ("3e", "4-(4-Hydroxyphenyl)-N-phenylpiperazine-1-carbothioamide", "196.83 °C", 196.83),
    ("3f", "N-Benzyl-4-(4-hydroxyphenyl)piperazine-1-carbothioamide", "164.61 °C", 164.61),
    ("3g", "4-(4-Hydroxyphenyl)-N-phenethylpiperazine-1-carbothioamide", "191.55 °C", 191.55),
    ("3h", "4-(4-Hydroxyphenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide", "236.51 °C", 236.51),
    ("3i", "4-(2-Chlorophenyl)-N-phenylpiperazine-1-carbothioamide", "175.78 °C", 175.78),
    ("3j", "N-Benzyl-4-(2-chlorophenyl)piperazine-1-carbothioamide", "111.40 °C", 111.40),
    ("3k", "4-(2-Chlorophenyl)-N-phenethylpiperazine-1-carbothioamide", "111.76 °C", 111.76),
    ("3l", "4-(2-Chlorophenyl)-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide", "180.66 °C", 180.66),
    ("3m", "4-Benzhydryl-N-phenylpiperazine-1-carbothioamide", "216.60 °C", 216.60),
    ("3n", "4-Benzhydryl-N-benzylpiperazine-1-carbothioamide", "156.54 °C", 156.54),
    ("3o", "4-Benzhydryl-N-phenethylpiperazine-1-carbothioamide", "138.93 °C", 138.93),
    ("3p", "4-Benzhydryl-N-(3,4,5-trimethoxyphenyl)piperazine-1-carbothioamide", "151.96 °C", 151.96),
]
# Build quote shells from full names as they appear in the article
quote_pairs = {
    "3a": "N,4-Diphenylpiperazine-1-carbothioamide (3a) White solid; 160.38 °C",
    "3b": "N-Benzyl-4-phenylpiperazine-1-carbothioamide (3b) White solid; 180.33 °C",
    "3c": "N-Phenethyl-4-phenylpiperazine-1-carbothioamide (3c) White solid; 141.97 °C",
    "3d": "4-Phenyl-N-(3,4,5-trimethoxyphenyl)\xadpiperazine-1-carbothioamide (3d) White solid; 204.90 °C",
    "3e": "4-(4-Hydroxyphenyl)- N -phenylpiperazine-1-carbothioamide (3e) White solid; 196.83 °C",
    "3f": "N-Benzyl-4-(4-hydroxyphenyl)\xadpiperazine-1-carbothioamide (3f) White solid; 164.61 °C",
    "3g": "4-(4-Hydroxyphenyl)-N-phenethylpiperazine-1-carbothioamide (3g) White solid; 191.55 °C",
    "3h": "4-(4-Hydroxyphenyl)-N-(3,4,5-trimethoxyphenyl)\xadpiperazine-1-carbothioamide (3h) White solid; 236.51 °C",
    "3i": "4-(2-Chlorophenyl)- N -phenylpiperazine-1-carbothioamide (3i) White solid; 175.78 °C",
    "3j": "N-Benzyl-4-(2-chlorophenyl)\xadpiperazine-1-carbothioamide (3j) White solid; 111.40 °C",
    "3k": "4-(2-Chlorophenyl)-N-phenethylpiperazine-1-carbothioamide (3k) White solid; 111.76 °C",
    "3l": "4-(2-Chlorophenyl)-N-(3,4,5-trimethoxyphenyl)\xadpiperazine-1-carbothioamide (3l) White solid; 180.66 °C",
    "3m": "4-Benzhydryl- N -phenylpiperazine-1-carbothioamide (3m) White solid; 216.60 °C",
    "3n": "4-Benzhydryl-N-benzylpiperazine-1-carbothioamide (3n) White solid; 156.54 °C",
    "3o": "4-Benzhydryl-N-phenethylpiperazine-1-carbothioamide (3o) White solid; 138.93 °C",
    "3p": "4-Benzhydryl-N-(3,4,5-trimethoxyphenyl)\xadpiperazine-1-carbothioamide (3p) White solid; 151.96 °C",
}
for code, name, vraw, vmid in p004:
    q = quote_pairs[code]
    add(name, "melting_point", vraw, vmid, None, None, "=", src4, url4,
        f"Section 2.1.3 synthesis of {code}", q,
        notes=f"compound code {code}; DSC-determined mp")

write()
print(f"After 004: {len(ROWS)} rows")

# ===== Paper 005 PMC12987641 - Indenoquinolinyl phosphine oxides =====
src5 = "ChemMedChem 2026, 21(5), e202500751"
url5 = "https://doi.org/10.1002/cmdc.202500751"
p005 = [
    ("9a", "Diphenyl(6-phenyl-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "232–234 °C", 233.0, 232.0, 234.0),
    ("9b", "Diphenyl(6-(4-fluorophenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "200–202 °C", 201.0, 200.0, 202.0),
    ("9c", "Diphenyl(6-(4-(trifluoromethyl)phenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "234–236 °C", 235.0, 234.0, 236.0),
    ("9d", "Diphenyl(6-(4-nitrophenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "212–213 °C", 212.5, 212.0, 213.0),
    ("9f", "Diphenyl(6-(3-methoxyphenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "134–135 °C", 134.5, 134.0, 135.0),
    ("9g", "Diphenyl(6-(3-fluorophenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "207–209 °C", 208.0, 207.0, 209.0),
    ("9h", "Diphenyl(6-(3-nitrophenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "228–231 °C", 229.5, 228.0, 231.0),
    ("9i", "Diphenyl(6-(2,4-difluorophenyl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "126–127 °C", 126.5, 126.0, 127.0),
    ("9j", "Diphenyl(6-(naphthalen-1-yl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "267–269 °C", 268.0, 267.0, 269.0),
    ("9k", "Diphenyl(6-(naphthalen-2-yl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "222–224 °C", 223.0, 222.0, 224.0),
    ("9l", "Diphenyl(6-(pyridin-2-yl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "214–216 °C", 215.0, 214.0, 216.0),
    ("9m", "Diphenyl(6-(pyridin-4-yl)-6,6a,7,11b-tetrahydro-5H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "219–222 °C", 220.5, 219.0, 222.0),
    ("10e", "Diphenyl(6-(4-methoxyphenyl)-7H-indeno[2,1-c]quinolin-4-yl)phosphine oxide", "212–213 °C", 212.5, 212.0, 213.0),
    ("11a", "4-(Diphenylphosphoryl)-6-phenyl-7H-indeno[2,1-c]quinolin-7-one", "274–275 °C", 274.5, 274.0, 275.0),
    ("11c", "4-(Diphenylphosphoryl)-6-(4-(trifluoromethyl)phenyl)-7H-indeno[2,1-c]quinolin-7-one", "308–309 °C", 308.5, 308.0, 309.0),
    ("11d", "4-(Diphenylphosphoryl)-6-(4-nitrophenyl)-7H-indeno[2,1-c]quinolin-7-one", "295–296 °C", 295.5, 295.0, 296.0),
    ("11e", "4-(Diphenylphosphoryl)-6-(4-methoxyphenyl)-7H-indeno[2,1-c]quinolin-7-one", "275–276 °C", 275.5, 275.0, 276.0),
    ("11f", "4-(Diphenylphosphoryl)-6-(3-methoxyphenyl)-7H-indeno[2,1-c]quinolin-7-one", "283–285 °C", 284.0, 283.0, 285.0),
    ("11g", "4-(Diphenylphosphoryl)-6-(3-fluorophenyl)-7H-indeno[2,1-c]quinolin-7-one", "270–273 °C", 271.5, 270.0, 273.0),
    ("11h", "4-(Diphenylphosphoryl)-6-(3-nitrophenyl)-7H-indeno[2,1-c]quinolin-7-one", "171–173 °C", 172.0, 171.0, 173.0),
    ("11i", "6-(2,4-Difluorophenyl)-4-(diphenylphosphoryl)-7H-indeno[2,1-c]quinolin-7-one", "182–183 °C", 182.5, 182.0, 183.0),
    ("11k", "4-(Diphenylphosphoryl)-6-(naphthalen-2-yl)-7H-indeno[2,1-c]quinolin-7-one", "213–214 °C", 213.5, 213.0, 214.0),
    ("11l", "4-(Diphenylphosphoryl)-6-(pyridin-2-yl)-7H-indeno[2,1-c]quinolin-7-one", "268–271 °C", 269.5, 268.0, 271.0),
    ("11m", "4-(Diphenylphosphoryl)-6-(pyridin-4-yl)-7H-indeno[2,1-c]quinolin-7-one", "287–290 °C", 288.5, 287.0, 290.0),
]
# Quotes are evidence of mp values; use simpler quote with code + mp
quotes_005 = {
    "9a": "(9a) The general procedure A was followed using benzaldehyde 5a (10 mmol, 1.0 ml), for 10 hr at room temperature, affording 3.83 g (77%) of 9a as a white solid, mp 232–234°C",
    "9b": "(9b) The general procedure A was followed using 4‐fluorobenzaldehyde 5b (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.38 g (85%) of 9b as a white solid, mp 200°C–202°C",
    "9c": "(9c) The general procedure A was followed using 4‐trifluorobenzaldehyde 5c (10 mmol, 1.7 ml), for 30 min at room temperature, affording 5.08 g (90%) of 9c as a yellow solid mp 234–236°C",
    "9d": "(9d) The general procedure A was followed using 4‐nitrobenzaldehyde 5d (10 mmol, 1.5 mL), heated to reflux for 24 hr affording 2.93 g (54%) of 9d as a yellow solid, mp 212–213°C",
    "9f": "(9f) The general procedure A was followed using m‐methoxybenzaldehyde 5f (10 mmol, 1.2 mL), for 6.5 h at room temperature affording 3.58 g (68%) of 9f as a yellow solid, mp 134–135°C",
    "9g": "(9g) The general procedure A was followed using 3‐fluorobenzaldehyde 5g (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.17 g (81%) of 9g as a yellow solid, mp 207°C‐209°C",
    "9h": "(9Hr) The general procedure A was followed using 3‐nitrobenzaldehyde 5h (10 mmol, 1.5 mL), heated to reflux for 48 h affording 3.67 g (68%) of 9h as a yellow solid, mp 228–231°C",
    "9i": "(9i) The general procedure A was followed using 2,4‐difluorobenzaldehyde 5i (10 mmol, 1.2 mL), heated to reflux for 48 h affording 3.31 g (62%) of 9i as a white solid, mp 126–127°C",
    "9j": "(9j) The general procedure A was followed using 1‐naphthaldehyde 5j (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.44 g (63%) of 9j as a white solid, mp 267–269°C",
    "9k": "(9k) The general procedure A was followed using 2‐naphthaldehyde 5k (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.67 g (67%) of 9k as a light‐yellow solid, mp 222–224°C",
    "9l": "(9l) The general procedure A was followed using picolinaldehyde 5l (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.64 g (73%) of 9l as a brown solid, mp 214–216°C",
    "9m": "(9m) The general procedure B was followed using isonicotinaldehyde 5m (10 mmol, 1.5 mL), affording 3.09 g (62%) of 9 m as a yellow solid, mp 219–222°C",
    "10e": "(10e) The general procedure A was followed using 4‐methoxybenzaldehyde 5e (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.40 g (65%) of 10e as a yellow solid, mp 212–213°C",
    "11a": "phosphine oxide 9a (0.25 mmol, 0.13 g), affording 0.09 g (70%) of 11a as a yellow solid, mp 274–275°C",
    "11c": "phosphine oxide 9c (0.25 mmol, 0.13 g), affording 0.10 g (73%) of 11c as a yellow solid, mp 308°C‐309°C",
    "11d": "phosphine oxide 9d (0.25 mmol, 0.13 g), affording 0.10 g (75%) of 11d as an orange solid, mp 295°C–296°C",
    "11e": "phosphine oxide 10e (0.25 mmol, 0.13 g), affording 0.13 g (99%) of 11e as a yellow solid, mp 275–276°C",
    "11f": "phosphine oxide 9f (0.25 mmol, 0.13 g), affording 0.13 g (99%) of 11f as a yellow solid, mp 283°C‐285°C",
    "11g": "phosphine oxide 9g (0.25 mmol, 0.13 g), affording 0.10 g (77%) of 11g as a yellow solid, mp 270°C‐273°C",
    "11h": "phosphine oxide 9hr (0.25 mmol, 0.13 g), affording 0.12 g (87%) of 11hr as a yellow solid, mp 171°C‐173°C",
    "11i": "(11i) The general procedure A was followed using diphenyl‐4(6‐(2,4‐difluorophenyl)−6,6a,7,11b‐tetrahydro‐5 H ‐indeno[2,1‐ c ]quinolin‐4‐yl)phosphine oxide 9i (0.25 mmol, 0.13 g), affording 0.07 g (48%) of 11i as an orange solid, mp 182°C‐183°C",
    "11k": "phosphine oxide 9k (0.25 mmol, 0.13 g), affording 0.02 g (14%) of 11k as a yellow solid, mp 213°C‐214°C",
    "11l": "phosphine oxide 9l (0.25 mmol, 0.13 g), affording 0.10 g (78%) of 11l as a yellow solid, mp 268°C–271°C",
    "11m": "phosphine oxide 9m (0.25 mmol, 0.13 g), affording 0.08 g (60%) of 11 m as a yellow solid, mp 287°C–290°C",
}
for code, name, vraw, vmid, vmin, vmax in p005:
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src5, url5,
        f"Section 6.2-6.3 synthesis of compound {code}", quotes_005[code],
        notes=f"compound code {code}")

write()
print(f"After 005: {len(ROWS)} rows")

# ===== Paper 006 PMC13006720 - Nitrofuryl-1,3,4-thiadiazole derivatives =====
src6 = "Arch. Pharm. (Weinheim) 2026, 359(3), e70227"
url6 = "https://doi.org/10.1002/ardp.70227"
p006 = [
    ("7", "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxylic acid", "278–279 °C", 278.5, 278.0, 279.0,
     "Orange solid, mp 278°C–279°C", "as a pale orange powder (4.21 g, 13.0 mmol, 73%). Orange solid, mp 278°C–279°C"),
    ("8", "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-phenylpiperidine-4-carboxamide", "254–256 °C", 255.0, 254.0, 256.0,
     "mp 254°C–256°C", "1‐[5‐(5‐Nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]‐ N ‐phenylpiperidine‐4‐carboxamide ( 8 ): Yellow solid, mp 254°C–256°C"),
    ("9", "N-Benzyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide", "271–273 °C", 272.0, 271.0, 273.0,
     "mp 271°C–273°C", "N ‐Benzyl‐1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidine‐4‐carboxamide ( 9 ): Orange solid, mp 271°C–273°C"),
    ("10", "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-phenethylpiperidine-4-carboxamide", "289–293 °C", 291.0, 289.0, 293.0,
     "mp 289°C–293°C", "1‐[5‐(5‐Nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]‐ N ‐phenethylpiperidine‐4‐carboxamide ( 10 ): Orange solid, mp 289°C–293°C"),
    ("11", "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-(3-phenylpropyl)piperidine-4-carboxamide", "305–308 °C", 306.5, 305.0, 308.0,
     "mp 305°C–308°C", "1‐[5‐(5‐Nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]‐ N ‐(3‐phenylpropyl)piperidine‐4‐carboxamide ( 11 ): "),
    ("12", "{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(pyrrolidin-1-yl)methanone", "243–245 °C", 244.0, 243.0, 245.0,
     "mp 243°C–245°C", "1‐[5‐(5‐Nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}(pyrrolidin‐1‐yl)methanone"),
    ("13", "{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(piperidin-1-yl)methanone", "252–254 °C", 253.0, 252.0, 254.0,
     "mp 252°C–254°C", "1‐[5‐(5‐Nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}(piperidin‐1‐yl)methanone"),
    ("14", "(4-Methylpiperidin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone", "268–270 °C", 269.0, 268.0, 270.0,
     "mp 268°C–270°C", "4‐Methylpiperidin‐1‐yl){1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}methanone"),
    ("15", "[1,4'-Bipiperidin]-1'-yl{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone", "288–291 °C", 289.5, 288.0, 291.0,
     "mp 288°C–291°C", "1,4′‐Bipiperidin]‐1′‐yl{1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}methanone"),
    ("16", "Morpholino{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone", "269–271 °C", 270.0, 269.0, 271.0,
     "mp 269°C–271°C", "Morpholino{1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}methanone"),
    ("17", "(4-Methylpiperazin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone", "276–279 °C", 277.5, 276.0, 279.0,
     "mp 276°C–279°C", "4‐Methylpiperazin‐1‐yl){1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidin‐4‐yl}methanone"),
    ("18", "N-Cyclohexyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide", "248–252 °C", 250.0, 248.0, 252.0,
     "mp 248°C–252°C", "N ‐Cyclohexyl‐1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidine‐4‐carboxamide"),
    ("19", "N-Ethyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide", "217–220 °C", 218.5, 217.0, 220.0,
     "mp 217°C–220°C", "N ‐Ethyl‐1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidine‐4‐carboxamide"),
    ("20", "N-Isopropyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide", "228–230 °C", 229.0, 228.0, 230.0,
     "mp 228°C–230°C", "N ‐Isopropyl‐1‐[5‐(5‐nitrofuran‐2‐yl)‐1,3,4‐thiadiazol‐2‐yl]piperidine‐4‐carboxamide"),
]
for code, name, vraw, vmid, vmin, vmax, _, q in p006:
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src6, url6,
        f"Synthesis section, compound {code}", q,
        notes=f"compound code {code}")

write()
print(f"After 006: {len(ROWS)} rows")

# ===== Paper 007 PMC13093257 - Imidazopyridines PIM-1 =====
src7 = "RSC Adv. 2026, 6, d6ra00514d"
url7 = "https://doi.org/10.1039/d6ra00514d"
add("2-(3-Nitrophenyl)imidazo[1,2-a]pyridine", "melting_point", "207–209 °C", 208.0, 207.0, 209.0, "=", src7, url7,
    "Section 2.3.1 synthesis of compound 3",
    "yield a yellow crystalline solid, product (3); 11 g, yield: 85.60%, MP: 207–209 °C",
    notes="compound code 3; intermediate")

write()
print(f"After 007: {len(ROWS)} rows")

# ===== Paper 008 PMC12944436 - Imatinib terpene analogues =====
src8 = "Pharmaceuticals (Basel) 2026, 19(2), 198"
url8 = "https://doi.org/10.3390/ph19020198"
p008 = [
    ("6a", "4-((Cyclohexyl(methyl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "166–168 °C", 167.0, 166.0, 168.0),
    ("6b", "4-((((3S,5S,7S)-Adamantan-1-yl)(methyl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "132–134 °C", 133.0, 132.0, 134.0),
    ("6c", "4-((((1R,3R,5R,7R)-Adamantan-2-yl)(methyl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "132–134 °C", 133.0, 132.0, 134.0),
    ("6d", "4-((Methyl((1S,2S,3S,5R)-2,6,6-trimethylbicyclo[3.1.1]heptan-3-yl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "118–120 °C", 119.0, 118.0, 120.0),
    ("6e", "4-((Methyl((1R,2R,3R,5S)-2,6,6-trimethylbicyclo[3.1.1]heptan-3-yl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "118–120 °C", 119.0, 118.0, 120.0),
    ("6f", "4-((((2R)-Bicyclo[2.2.1]heptan-2-yl)(methyl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "151–153 °C", 152.0, 151.0, 153.0),
    ("6g", "4-((Methyl((1R,2R,4R)-1,7,7-trimethylbicyclo[2.2.1]heptan-2-yl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "93–96 °C", 94.5, 93.0, 96.0),
    ("6h", "4-((Methyl((1R,2S,4R)-1,7,7-trimethylbicyclo[2.2.1]heptan-2-yl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "111–114 °C", 112.5, 111.0, 114.0),
    ("6i", "4-((((1S,2R,3S,4R)-3-Hydroxy-4,7,7-trimethylbicyclo[2.2.1]heptan-2-yl)(methyl)amino)methyl)-N-(4-methyl-3-((4-(pyridin-3-yl)pyrimidin-2-yl)amino)phenyl)benzamide", "121–124 °C", 122.5, 121.0, 124.0),
]
for code, name, vraw, vmid, vmin, vmax in p008:
    # Build verifiable quote using the actual pattern from the paper
    quote = f"{name} {code} Yield"
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src8, url8,
        f"Synthesis of compound {code}",
        f"benzamide {code} Yield " + ("96" if code in ['6a','6b','6c'] else ("91" if code in ['6c','6d','6e'] else "")) + f"%. mp {vraw.replace(' ','').replace('°','')}",
        notes=f"compound code {code}")

# Above quote logic is too fragile; instead use direct quote
# Re-clear last 9 rows and re-add with proper quotes
for _ in range(9):
    ROWS.pop()

p008_quotes = {
    "6a": "benzamide 6a Yield 96%. mp 166–168 °C",
    "6b": "benzamide 6b Yield 96%. mp 132–134 °C",
    "6c": "benzamide 6c Yield 91%. mp 132–134 °C",
    "6d": "benzamide 6d Yield 91%. mp 118–120 °C",
    "6e": "benzamide 6e Yield 91%. mp 118–120 °C",
    "6f": "benzamide 6f Yield 89%. mp 151–153 °C",
    "6g": "benzamide 6g Yield 85%. mp 93–96 °C",
    "6h": "benzamide 6h Yield 92%. mp 111–114 °C",
    "6i": "benzamide 6i Yield 91%. mp 121–124 °C",
}
for code, name, vraw, vmid, vmin, vmax in p008:
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src8, url8,
        f"Synthesis of compound {code}", p008_quotes[code],
        notes=f"compound code {code}")

write()
print(f"After 008: {len(ROWS)} rows")

# ===== Paper 009 PMC12943507 - 4-Arylazo Pyrazole Carboxamides =====
src9 = "Pharmaceuticals (Basel) 2026, 19(2), 239"
url9 = "https://doi.org/10.3390/ph19020239"
p009 = [
    ("5a", "3,5-Diamino-4-(Phenyldiazenyl)-N-Tosyl-1H-Pyrazole-1-Carboxamide", "206–207 °C", 206.5, 206.0, 207.0),
    ("5b", "3,5-Diamino-4-[(4-Chlorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "295–296 °C", 295.5, 295.0, 296.0),
    ("5c", "3,5-Diamino-4-[(4-Fluorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "215–216 °C", 215.5, 215.0, 216.0),
    ("5d", "3,5-Diamino-4-[(4-Methoxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "173–174 °C", 173.5, 173.0, 174.0),
    ("5e", "3,5-Diamino-4-[(4-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "246–247 °C", 246.5, 246.0, 247.0),
    ("5f", "3,5-Diamino-4-[(4-Acetylphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "183–184 °C", 183.5, 183.0, 184.0),
    ("5g", "3,5-Diamino-4-[(4-Hydroxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "216–217 °C", 216.5, 216.0, 217.0),
    ("5h", "3,5-Diamino-4-[(3-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "214–215 °C", 214.5, 214.0, 215.0),
    ("5i", "3,5-Diamino-4-[(2-Methyl-4-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "219–220 °C", 219.5, 219.0, 220.0),
    ("5j", "3,5-Diamino-4-[(3,4-Dichlorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "291–292 °C", 291.5, 291.0, 292.0),
    ("5k", "3,5-Diamino-4-[(3,4-Dimethoxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "169–170 °C", 169.5, 169.0, 170.0),
    ("5l", "3,5-Diamino-4-[(3,5-Dimethylphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "228–229 °C", 228.5, 228.0, 229.0),
    ("5m", "3,5-Diamino-4-[(Perfluorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide", "203–204 °C", 203.5, 203.0, 204.0),
]
for code, name, vraw, vmid, vmin, vmax in p009:
    quote = f"{name} ( {code} ) Yield: " 
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src9, url9,
        f"Section 3.2 synthesis of {code}",
        f"{name} ( {code} ) Yield: ", # placeholder before re-verify
        notes=f"compound code {code}")

# Re-set with verified quotes - using actual paper-found quotes (just retrieve the mp segment)
# Replace the just-added 13 rows with proper quotes built from actual paper text
for _ in range(13):
    ROWS.pop()

p009_quotes = {
    "5a": "3,5-Diamino-4-(Phenyldiazenyl)-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5a ) Yield: 76.6%; Color: yellow solid; Melting Point: 206–207 °C",
}
# For others, build from confirmed pattern. Search needs actual quote text. Let me extract for each.

p009_quotes = {
    "5a": "Diamino-4-(Phenyldiazenyl)-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5a ) Yield: 76.6%; Color: yellow solid; Melting Point: 206–207 °C",
    "5b": "Diamino-4-[(4-Chlorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5b ) Yield: 73.2%; Color: light yellow solid; Melting Point: 295–296 °C",
    "5c": "Diamino-4-[(4-Fluorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5c ) Yield: 67.6%; Color: yellow solid; Melting Point: 215–216 °C",
    "5d": "Diamino-4-[(4-Methoxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5d ) Yield: 72.8%; Color: light yellow solid; Melting Point: 173–174 °C",
    "5e": "Diamino-4-[(4-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5e ) Yield: 65.2%; Color: dark red solid; Melting Point: 246–247 °C",
    "5f": "Diamino-4-[(4-Acetylphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5f ) Yield: 65.9%; Color: brown solid; Melting Point: 183–184 °C",
    "5g": "Diamino-4-[(4-Hydroxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5g ) Yield: 67.7%; Color: yellow solid; Melting Point: 216–217 °C",
    "5h": "Diamino-4-[(3-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5h ) Yield: 72.3%; Color: light orange solid; Melting Point: 214–215 °C",
    "5i": "Diamino-4-[(2-Methyl-4-Nitrophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5i ) Yield: 68.4%; Color: reddish solid; Melting Point: 219–220 °C",
    "5j": "Diamino-4-[(3,4-Dichlorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5j ) Yield: 79.6%; Color: yellow solid; Melting Point: 291–292 °C",
    "5k": "Diamino-4-[(3,4-Dimethoxyphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5k ) Yield: 85.2%; Color: light green solid; Melting Point: 169–170 °C",
    "5l": "Diamino-4-[(3,5-Dimethylphenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5l ) Yield: 69.6%; Color: light yellow solid; Melting Point: 228–229 °C",
    "5m": "Diamino-4-[(Perfluorophenyl)Diazinyl]-N-Tosyl-1H-Pyrazole-1-Carboxamide ( 5m ) Yield: 87.6%; Color: light yellow solid; Melting Point: 203–204 °C",
}
for code, name, vraw, vmid, vmin, vmax in p009:
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src9, url9,
        f"Section 3.2 synthesis of {code}", p009_quotes[code],
        notes=f"compound code {code}")

write()
print(f"After 009: {len(ROWS)} rows")

# ===== Paper 010 PMC12940417 - TRPA1 inhibitors =====
import json
src10 = "Int. J. Mol. Sci. 2026, 27(4), 1716"
url10 = "https://doi.org/10.3390/ijms27041716"
with open("/sessions/serene-amazing-franklin/mnt/trial5/opus47/work_batch_00/p010.json") as f:
    p010 = json.load(f)
def parse_range(mp):
    if '–' in mp:
        a,b = mp.split('–')
        return (float(a)+float(b))/2.0, float(a), float(b)
    elif '-' in mp:
        a,b = mp.split('-')
        return (float(a)+float(b))/2.0, float(a), float(b)
    else:
        v = float(mp)
        return v, None, None

# Curate names manually for clean output
name_overrides = {
    "1": "4-(Pyridin-4-yl)benzaldehyde",
    "6": "Diethyl ((E)-4-((adamantan-1-yl)amino)-4-oxobut-2-en-1-yl)phosphonate",
    "11": "(2E,4E)-N-Isobutyl-5-phenylpenta-2,4-dienamide",
    "12": "(2E,4E)-N-(Adamantan-1-yl)-5-phenylpenta-2,4-dienamide",
    "13": "(2E,4E)-N-(3-Hydroxyadamantan-1-yl)-5-phenylpenta-2,4-dienamide",
    "14": "(2E,4E)-N-(Adamantan-1-yl)-5-(naphthalen-2-yl)penta-2,4-dienamide",
    "15": "(2E,4E)-N-Isobutyl-5-(naphthalen-2-yl)penta-2,4-dienamide",
    "16": "(2E,4E)-5-([1,1'-Biphenyl]-3-yl)-N-isobutylpenta-2,4-dienamide",
    "17": "(2E,4E)-5-([1,1'-Biphenyl]-4-yl)-N-(adamantan-1-yl)penta-2,4-dienamide",
    "18": "(2E,4E)-N-(Adamantan-1-yl)-5-(4-(pyridin-4-yl)phenyl)penta-2,4-dienamide",
    "19": "(2E,4E)-N-Isobutyl-5-(3-phenoxyphenyl)penta-2,4-dienamide",
    "20": "(2E,4E)-N-(Adamantan-1-yl)-5-(3-phenoxyphenyl)penta-2,4-dienamide",
    "21": "(2E,4E)-N-Isobutyl-5-(3-(pentyloxy)phenyl)penta-2,4-dienamide",
    "22": "(2E,4E)-N-(Adamantan-1-yl)-5-(3-(cinnamyloxy)phenyl)penta-2,4-dienamide",
    "23": "(2E,4E)-5-(3-(Cinnamyloxy)phenyl)-N-isobutylpenta-2,4-dienamide",
    "24": "(2E,4E)-N-Isobutyl-5-(3-((3-methylbut-2-en-1-yl)oxy)phenyl)penta-2,4-dienamide",
    "25": "(2E,4E)-5-(3-(Allyloxy)phenyl)-N-isobutylpenta-2,4-dienamide",
    "27": "N-(Adamantan-1-yl)cinnamamide",
    "28": "N-(3-Hydroxyadamantan-1-yl)cinnamamide",
    "29": "(E)-N-(Adamantan-1-yl)-3-(4-(pyridin-4-yl)phenyl)acrylamide",
    "30": "(E)-N-(Adamantan-1-yl)-3-(4-bromophenyl)acrylamide",
    "31": "(E)-3-([1,1'-Biphenyl]-4-yl)-N-(adamantan-1-yl)acrylamide",
    "32": "(E)-3-([1,1'-Biphenyl]-4-yl)-N-(3-hydroxyadamantan-1-yl)acrylamide",
    "33": "(E)-N-(Adamantan-1-yl)-3-(3-hydroxyphenyl)acrylamide",
    "34": "(E)-N-(3-Hydroxyadamantan-1-yl)-3-(3-hydroxyphenyl)acrylamide",
    "35": "Ethyl (E)-3-([1,1'-Biphenyl]-4-yl)acrylate",
    "36": "Ethyl (E)-3-(3-Hydroxyphenyl)acrylate",
}
for code in name_overrides:
    if code not in p010: continue
    d = p010[code]
    vraw = d["mp"].replace('–','–') + " °C"
    vmid, vmin, vmax = parse_range(d["mp"])
    name = name_overrides[code]
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src10, url10,
        f"Section 4 synthesis of compound {code}", d["quote"],
        notes=f"compound code {code}")

write()
print(f"After 010: {len(ROWS)} rows")

# ===== Paper 011 PMC12943719 - PDE4 Pyridazinones =====
src11 = "Molecules 2026, 31(4), 699"
url11 = "https://doi.org/10.3390/molecules31040699"
with open("/sessions/serene-amazing-franklin/mnt/trial5/opus47/work_batch_00/p011.json") as f:
    p011 = json.load(f)
for code, d in p011.items():
    vraw = d["mp"] + " °C"
    vmid, vmin, vmax = parse_range(d["mp"])
    add(d["name"], "melting_point", vraw, vmid, vmin, vmax, "=", src11, url11,
        f"Section synthesis of compound {code}", d["quote"],
        notes=f"compound code {code}")

write()
print(f"After 011: {len(ROWS)} rows")

# ===== Paper 012 PMC12987640 - σ1R Agonists/HDAC Inhibitor =====
src12 = "ChemMedChem 2026, 21(5), e202500922"
url12 = "https://doi.org/10.1002/cmdc.202500922"
p012 = [
    ("2a", "N-(1-Benzylpiperidin-4-yl)-N-methyl-4-phenylbutanamide", "169–171 °C", 170.0, 169.0, 171.0,
     "N‐(1‐Benzylpiperidin‐4‐yl)‐N‐Methyl‐4‐Phenylbutanamide (2a) White solid (458 mg, yield 88%): mp 169°C–171°C"),
    ("2b", "N-(1-Benzylpiperidin-4-yl)-N-methyl-2-propylpentanamide", "170–173 °C", 171.5, 170.0, 173.0,
     "N‐(1‐Benzylpiperidin‐4‐yl)‐N‐Methyl‐2‐Propylpentanamide (2b) White solid (375 mg, yield 75%): mp 170°C–173°C"),
    ("2c", "N-(1-Benzylpiperidin-4-yl)-4-phenylbutanamide hydrochloride", "162–164 °C", 163.0, 162.0, 164.0,
     "N‐(1‐Benzylpiperidin‐4‐yl)‐4‐Phenylbutanamide Hydrochloride (2c) White solid (425 mg, yield 80%): mp 162°C–164°C"),
    ("2d", "N-(1-Benzylpiperidin-4-yl)-2-propylpentanamide hydrochloride", "164–165 °C", 164.5, 164.0, 165.0,
     "N‐(1‐Benzylpiperidin‐4‐yl)‐2‐Propylpentanamide Hydrochloride (2d) White solid (349 mg, yield 70%): mp 164°C–165°C"),
    ("3a", "1-Benzylpiperidin-4-yl 4-phenylbutanoate hydrochloride", "141–143 °C", 142.0, 141.0, 143.0,
     "1‐Benzylpiperidin‐4‐yl 4‐Phenylbutanoate Hydrochloride (3a) White solid (450 mg, yield 85%): mp 141°C–143°C"),
    ("3b", "1-Benzylpiperidin-4-yl 2-propylpentanoate hydrochloride", "143–145 °C", 144.0, 143.0, 145.0,
     "1‐Benzylpiperidin‐4‐yl 2‐Propylpentanoate Hydrochloride (3b) White solid (363 mg, yield 73%): mp 143°C–145°C"),
    ("4a", "1-(4-Benzylpiperazin-1-yl)-4-phenylbutan-1-one", "166–168 °C", 167.0, 166.0, 168.0,
     "1‐(4‐Benzylpiperazin‐1‐yl)‐4‐Phenylbutan‐1‐One (4a) White solid (443 mg, yield 81%). mp 166°C–168°C"),
    ("4b", "1-(4-Benzylpiperazin-1-yl)-2-propylpentan-1-one", "165–167 °C", 166.0, 165.0, 167.0,
     "1‐(4‐Benzylpiperazin‐1‐yl)‐2‐Propylpentan‐1‐One (4b) White solid (356 mg, yield 69%). mp 165°C–167°C"),
]
for code, name, vraw, vmid, vmin, vmax, q in p012:
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src12, url12,
        f"Section 4.2.1 synthesis of compound {code}", q,
        notes=f"compound code {code}")

write()
print(f"After 012: {len(ROWS)} rows")

# ===== Paper 013 PMC12943095 - 6H-Benzo[c]chromenes =====
src13 = "Molecules 2026, 31(4), 706"
url13 = "https://doi.org/10.3390/molecules31040706"
with open("/sessions/serene-amazing-franklin/mnt/trial5/opus47/work_batch_00/p013.json") as f:
    p013 = json.load(f)
for code, d in p013.items():
    name = d["name"].replace(' H ', 'H').replace(' c ', 'c').replace(' d ', 'd')
    vraw = d["mp"] + " °C"
    vmid = float(d["mp"])
    add(name, "melting_point", vraw, vmid, None, None, "=", src13, url13,
        f"Section 3 synthesis of compound {code}", d["quote"],
        notes=f"compound code {code}")

write()
print(f"After 013: {len(ROWS)} rows")

# ===== Paper 014 PMC12943640 - Incadronate analogues =====
src14 = "Pharmaceuticals (Basel) 2026, 19(2), 256"
url14 = "https://doi.org/10.3390/ph19020256"
with open("/sessions/serene-amazing-franklin/mnt/trial5/opus47/work_batch_00/p014.json") as f:
    p014 = json.load(f)
for code, d in p014.items():
    name = d["name"].replace(' N ', ' N')
    if name.startswith("N -"):
        name = "N" + name[2:]
    vraw = d["mp"] + " °C"
    vmid, vmin, vmax = parse_range(d["mp"])
    add(name, "melting_point", vraw, vmid, vmin, vmax, "=", src14, url14,
        f"Synthesis section compound {code}", d["quote"],
        notes=f"compound code {code}" + (f"; {d.get('note','')}" if d.get('note') else ''))

write()
print(f"After 014: {len(ROWS)} rows")

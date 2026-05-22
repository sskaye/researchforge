"""Add mp rows for papers 049 and 055 (missed in first pass)."""
import csv, re
CSV_PATH = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_02.csv'
SKIP_PATH = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_02_skipped.tsv'

# Paper 049 — Molecules 2003, 8, 444-452, DOI 10.3390/80500444
src049 = "Molecules 2003, 8, 444-452"
url049 = "https://doi.org/10.3390/80500444"
# Read text to extract verbatim quote with compound name + value
p049 = open('/sessions/wizardly-beautiful-tesla/mnt/opus47_papers/Papers/049_PMC6147017_Synthesis_of_New_Pyrazole_and_Pyrimidine_Steroidal_Derivatives/article_text.txt').read()
rows049 = [
    # (compound, value_raw, val, vmin, vmax, qsubstr)
    ("1’-Methyl-5’-methylthio-pyrazolo[4’,3’:16,17]androst-5-en-3β-ol", "181-183", "182.0", "181", "183",
     "129.4 mg (70 %) of 3b , mp (ethanol): 181–183 °C"),
    ("6’-Methoxy-pyrimido[5’,4’:16,17]androst-5-en-3β-ol", "178-180", "179.0", "178", "180",
     "50.74 mg (68 %) of 4a , mp (acetone): 178–180 °C"),
    ("6’-Methoxy-2’-methyl-pyrimido[5’,4’:16,17]androst-5-en-3β-ol", "210-212", "211.0", "210", "212",
     "58.4 mg (75 %) of 4b , mp (acetone): 210–212 °C"),
    ("6’-Methoxy-2’-phenyl-pyrimido[5’,4’:16,17-c]androst-5-en-3β-ol", "241-243", "242.0", "241", "243",
     "57.12 mg (62 %) of 4c , mp (acetone): 241–243 °C"),
    ("2’-Amino-6’-methoxy-pyrimido[5’,4’:16,17]androst-5-en-3β-ol", "218-221", "219.5", "218", "221",
     "49.98 mg (64 %) of 4d , mp (acetone): 218–221 °C"),
]
codes049 = ["3b","4a","4b","4c","4d"]

# Paper 055 — Int J Mol Sci 2007, 8, 214-228, PMC only
src055 = "Int J Mol Sci 2007, 8, 214-228"
url055 = "pmc:PMC3685236"
rows055 = [
    ("3-Hydroxy-2,2-dimethyl-3-(4-biphenylyl)butanoic acid","142","142","","",
     "3-Hydroxy-2,2-dimethyl-3-(4-biphenylyl)butanoic acid: C 18 H 20 O 3 ; M w = 284.35 ; Melting point: 142 °C"),
    ("3-Hydroxy-2,2-dimethyl-3,3-diphenylpropanoic acid","162","162","","",
     "3-Hydroxy-2,2-dimethyl-3,3-diphenylpropanoic acid; C 17 H 18 O 3 ; M w = 270.32; Melting point: 162 °C"),
    ("3-Hydroxy-3-(4-biphenylyl)butanoic acid","136","136","","",
     "3-Hydroxy-3-(4-biphenylyl)butanoic acid; C 16 H 16 O 3 ; Mw = 256.30; Melting point: 136 °C"),
    ("2-[9-(9-Hydroxyfluorenyl)]-2-methylpropanoic acid","138","138","","",
     "2-[9-(9-Hydroxyfluorenyl)]-2-methylpropanoic acid; C 17 H 16 O 3 ; M w = 268.31; Melting point: 138 °C"),
    ("3-Hydroxy-2-methyl-3,3-diphenylpropanoic acid","180","180","","",
     "3-Hydroxy-2-methyl-3,3-diphenylpropanoic acid; C 16 H 16 O 3 ; M w = 256.30; Melting point: 180 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-(4-chlorophenyl)propanoic acid","142","142","","",
     "3-Hydroxy-2,2-dimethyl-3-(4-chlorophenyl)propanoic acid; C 11 H 13 ClO 3 ; M w = 228.67; Melting point: 142 °C"),
    ("3-Hydroxy-3-(2-chlorophenyl)propanoic acid","92","92","","",
     "3-Hydroxy-3-(2-chlorophenyl)propanoic acid; C 9 H 9 ClO 3 ; M w = 200.62; Melting point: 92 °C"),
    ("3-Hydroxy-2,2-dimethyl-(4-methoxyphenyl)butanoic acid","120","120","","",
     "3-Hydroxy-2,2-dimethyl-(4-methoxyphenyl)butanoic acid; C 13 H 18 O 4 ; M w = 238.28; Melting point: 120 °C"),
    ("2-Methyl-2-(1-(1-hydroxycyclohexyl))propanoic acid","89","89","","",
     "2-Hethyl-2-(1-(1-hydroxycyclohexyl))propanoic acid; C 10 H 18 O 3 ; M w = 186.25; Melting point: 89 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-phenylbutanoic acid","89","89","","",
     "3-Hydroxy-2,2-dimethyl-3-phenylbutanoic acid; C 12 H 16 O 3 ; M w = 208.26; Melting point: 89 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-phenylpropanoic acid","132","132","","",
     "3-Hydroxy-2,2-dimethyl-3-phenylpropanoic acid; C 11 H 14 O 3 ; M w = 194.23 ; Melting point: 132 °C"),
    ("3-Hydroxy-3,3-diphenylpropanoic acid","217","217","","",
     "3-Hydroxy-3,3-diphenylpropanoic acid; C 15 H 14 O 3 ; Mw = 242.09; Melting point: 217 °C"),
    ("2-(1′-(1′-Hydroxycyclohexyl))butanoic acid","86","86","","",
     "2-(1 ′ -(1 ′ -Hydroxycyclohexyl))butanoic acid; C 10 H 18 O 3 ; M w = 186.25; Melting point: 86 °C"),
]

# Confirm each 049 quote exists in paper text
issues = []
for q, *_ in [(q,) for *_, q in rows049]:
    if q not in p049:
        issues.append(q)
if issues:
    print("MISSING 049 quotes:", issues)

p055 = open('/sessions/wizardly-beautiful-tesla/mnt/opus47_papers/Papers/055_PMC3685236_Antiproliferative_Activity_of_-Hydroxy--Arylalkanoic_Acids/article_text.txt').read()
issues = []
for q, *_ in [(q,) for *_, q in rows055]:
    if q not in p055:
        issues.append(q[:60])
if issues:
    print("MISSING 055 quotes:")
    for q in issues: print(' ', q)

# load existing CSV to get next id
with open(CSV_PATH) as f:
    existing = list(csv.reader(f))
header = existing[0]
data = existing[1:]
existing_ids = [int(r[0]) for r in data]
next_id = max(existing_ids) + 1
print(f"Next id: {next_id}")

# Build rows
new_rows = []
for (name, raw, val, vmin, vmax, quote), code in zip(rows049, codes049):
    new_rows.append([str(next_id), "pending_verification", name, "", "melting_point", val, vmin, vmax,
        raw + " °C", "°C", "=", "measured", src049, url049,
        f"Experimental, characterization of compound {code}", quote, "", ""])
    next_id += 1

for (name, raw, val, vmin, vmax, quote) in rows055:
    new_rows.append([str(next_id), "pending_verification", name, "", "melting_point", val, vmin, vmax,
        raw + " °C", "°C", "=", "measured", src055, url055,
        "Experimental section, characterization paragraph", quote, "", ""])
    next_id += 1

with open(CSV_PATH, 'a', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in new_rows:
        assert len(r) == 18
        w.writerow(r)
print(f"Appended {len(new_rows)} rows. Next id = {next_id}")

# Remove 049 and 055 from skip
with open(SKIP_PATH) as f:
    skip = [line.rstrip("\n").split("\t") for line in f if line.strip()]
skip_new = [(loc, reason) for loc, reason in skip if not loc.startswith("049_") and not loc.startswith("055_")]
with open(SKIP_PATH, "w") as f:
    for loc, reason in skip_new:
        f.write(f"{loc}\t{reason}\n")
print(f"Skip list now has {len(skip_new)} entries")

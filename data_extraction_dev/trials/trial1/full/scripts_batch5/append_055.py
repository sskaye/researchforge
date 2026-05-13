import csv

SRC = "Int J Mol Sci 2007, 8(3), 214-228"
URL = "pmc:PMC3685236"
PATH = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/055_PMC3685236_Antiproliferative_Activity_of_-Hydroxy--Arylalkanoic_Acids/article_text.txt"

with open(PATH) as f:
    txt = f.read()

# (name, formula_blob, mp_text, value_celsius)
data = [
    ("3-Hydroxy-2,2-dimethyl-3-(4-biphenylyl)butanoic acid", "C 18 H 20 O 3", "Melting point: 142 °C", 142),
    ("3-Hydroxy-2,2-dimethyl-3,3-diphenylpropanoic acid",    "C 17 H 18 O 3", "Melting point: 162 °C", 162),
    ("3-Hydroxy-2-methyl-3-(2-chlorophenyl)propanoic acid",  "C 10 H 11 ClO 3", "Melting point: 84 0 C", 84),
    ("3-Hydroxy-3-(4-biphenylyl)butanoic acid",              "C 16 H 16 O 3", "Melting point: 136 °C", 136),
    ("2-[9-(9-Hydroxyfluorenyl)]-2-methylpropanoic acid",    "C 17 H 16 O 3", "Melting point: 138 °C", 138),
    ("3-Hydroxy-2-methyl-3,3-diphenylpropanoic acid",        "C 16 H 16 O 3", "Melting point: 180 °C", 180),
    ("3-Hydroxy-2,2-dimethyl-3-(4-chlorophenyl)propanoic acid", "C 11 H 13 ClO 3", "Melting point: 142 °C", 142),
    ("3-Hydroxy-3-(2-chlorophenyl)propanoic acid",           "C 9 H 9 ClO 3", "Melting point: 92 °C", 92),
    ("3-Hydroxy-2,2-dimethyl-(4-methoxyphenyl)butanoic acid", "C 13 H 18 O 4", "Melting point: 120 °C", 120),
    ("2-Methyl-2-(1-(1-hydroxycyclohexyl))propanoic acid",   "C 10 H 18 O 3", "Melting point: 89 °C", 89),
    ("3-Hydroxy-2,2-dimethyl-3-phenylbutanoic acid",         "C 12 H 16 O 3", "Melting point: 89 °C", 89),
    ("3-Hydroxy-3-(4-isobutylphenyl)butanoic acid",          "C 14 H 20 O 3", "Melting point : 90 °C", 90),
    ("3-Hydroxy-2,2-dimethyl-3-phenylpropanoic acid",        "C 11 H 14 O 3", "Melting point: 132 °C", 132),
    ("3-Hydroxy-3,3-diphenylpropanoic acid",                 "C 15 H 14 O 3", "Melting point: 217 °C", 217),
    ("2-(1'-(1'-Hydroxycyclohexyl))butanoic acid",           "C 10 H 18 O 3", "Melting point: 86 °C", 86),
]

next_id = 36
rows = []
for name, formula, mp_text, value in data:
    if mp_text not in txt:
        print(f"FAIL: {mp_text!r} not found")
        continue
    raw = mp_text.split(":",1)[1].strip()  # "142 °C" or "84 0 C"
    rows.append({
        "id": next_id,
        "verification_status": "pending_verification",
        "compound_name": name,
        "compound_smiles": "",
        "property": "melting_point",
        "value_celsius": value,
        "value_celsius_min": "",
        "value_celsius_max": "",
        "value_raw": raw,
        "relation": "=",
        "data_type": "measured",
        "source": SRC,
        "source_url": URL,
        "evidence_location": "Experimental section 3.1, compound characterization block",
        "evidence_quote": mp_text,
        "conversion_arithmetic": "",
        "notes": ""
    })
    next_id += 1

with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_5.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    for r in rows:
        writer.writerow(r)
print(f"appended {len(rows)} rows, next id={next_id}")

import csv

DOI = "https://doi.org/10.3390/80400363"
SRC = "Molecules 2003, 8(4), 363-373"

data = [
    ("6a",  "2-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester", 190, 192, "C 21 H 20 N 4 O 4"),
    ("6b",  "2-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester", 234, 236, "C 21 H 19 BrN 4 O 4"),
    ("7a",  "Cyano-{[4-(2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}acetic acid ethyl ester", 128, 130, "C 20 H 17 N 5 O 3"),
    ("7b",  "{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}cyano-acetic acid ethyl ester", 173, 175, "C 20 H 16 BrN 5 O 3"),
    ("8a",  "3-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione", 153, 155, "C 20 H 18 N 4 O 3"),
    ("8b",  "3-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione", 165, 167, "C 20 H 17 BrN 4 O 3"),
    ("9a",  "2-Methyl-3-{4-[N′-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one", 261, 263, "C 19 H 16 N 6 O 2"),
    ("9b",  "6-Bromo-2-methyl-3-{4-[N′-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one", 308, 310, "C 19 H 15 BrN 6 O 2"),
    ("10a", "3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol--4-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one", 180, 182, "C 18 H 15 N 7 O 2"),
    ("10b", "3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol--4-ylidene)hydrazino]phenyl}-6-bromo-2-methyl-3H-quinazolin-4-one", 244, 246, "C 18 H 14 BrN 7 O 2"),
    ("9c",  "2-Methyl-3-{4-[N′-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one", 302, 304, "C 25 H 20 N 6 O 2"),
    ("9d",  "6-Bromo-2-methyl-3-{4-[N′-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]-phenyl}-3H-quinazolin-4-one", 259, 261, "C 25 H 19 BrN 6 O 2"),
    ("11a", "3-[4-(3,5-Dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one", 205, 207, "C 26 H 22 N 6 O"),
    ("11b", "6 -Bromo-3-[4-(3,5-dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one", 238, 240, "C 26 H 21 BrN 6 O"),
    ("12a", "3-{4-[N′(4,6-Dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one", 285, 286, "C 21 H 18 N 6 O 2"),
    ("12b", "6-Bromo-3-{4-[N′(4,6-dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one", 210, 212, "C 21 H 17 BrN 6 O 2"),
]

with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/053_PMC6147013_Synthesis_of_Novel_3H-Quinazolin-4-ones_Containing_Pyrazolinone_Pyrazole_and_Pyrimidinone_/article_text.txt') as f:
    txt = f.read()

next_id = 2
rows = []
for label, name, lo, hi, formula in data:
    raw = f"{lo}-{hi} °C"
    mid = (lo+hi)/2
    cmin, cmax = lo, hi
    quote = f"M.p. {lo}-{hi} o C; Calculated for {formula}"
    if quote not in txt:
        print(f"FAIL quote not in source for {label}: {quote!r}")
        continue
    rows.append({
        "id": next_id,
        "verification_status": "pending_verification",
        "compound_name": name,
        "compound_smiles": "",
        "property": "melting_point",
        "value_celsius": mid,
        "value_celsius_min": cmin,
        "value_celsius_max": cmax,
        "value_raw": raw,
        "relation": "=",
        "data_type": "measured",
        "source": SRC,
        "source_url": DOI,
        "evidence_location": f"Experimental — compound {label}",
        "evidence_quote": quote,
        "conversion_arithmetic": "",
        "notes": ""
    })
    next_id += 1

with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_5.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    for r in rows:
        writer.writerow(r)
print("appended", len(rows), "rows. next id =", next_id)

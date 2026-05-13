import csv

DOI = "https://doi.org/10.3390/70700540"
SRC = "Molecules 2002, 7(7), 540-548"
PATH = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/054_PMC6146489_Michael_Reactions_of_Arylidenesulfonylacetonitriles._A_New_Route_to_Polyfunctional_Benzoaq/article_text.txt"

with open(PATH) as f:
    txt = f.read()

# Table 1 row patterns: "6a yellow 80 225-226 C 27 H 24..." each entry has "no. color yield mp_range formula..."
# Build evidence quote from "Compd_label color yield_pct mp_range"
# Each row pattern from the source — use 7-token prefix to ensure verbatim
# Source has flow: "6a yellow 80 225-226 C 27 H 24 N 2 O 4 S 68.64 5.08 5.93 6.78 DMF 472.23"
#
# Use the structural class as the name and append label
data = [
    # (label, name, lo, hi, mp_text_in_source)
    ("6a",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-imino-2-phenylsulphonyl-benzo[a]quinolizine (compound 6a, Ar = phenyl)", 225, 226, "6a yellow 80 225-226"),
    ("6b",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-imino-2-phenylsulphonyl-benzo[a]quinolizine (compound 6b, Ar = 4-chlorophenyl)", 264, 266, "6b dark 82 264-266"),
    ("6c",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-imino-2-phenylsulphonyl-benzo[a]quinolizine (compound 6c, Ar = 4-nitrophenyl)", 276, 277, "6c orange 78 276-277"),
    ("9a",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-imino-2-phenylsulphonyl-benzo[a]quinolizine (compound 9a)", 258, 259, "9a dark 84 258-259"),
    ("9b",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-imino-2-phenylsulphonyl-benzo[a]quinolizine (compound 9b)", 320, 322, "9b bright 77 320-322"),
    ("7a",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 7a)", 329, 331, "7a yellow 81 329-331"),
    ("7b",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 7b)", 206, 207, "7b yellow 85 206-207"),
    ("7c",  "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 7c)", 214, 215, "7c yellow 88 214-215"),
    ("10a", "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 10a)", 214, 216, "10a dark 86 214-216"),
    ("10b", "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 10b)", 223, 224, "10b bright 79 223-224"),
    ("10c", "2-aryl-6,7-dihydro-9,10-dimethoxy-4-iminobenzo[a]quinolizine (compound 10c)", 275, 277, "10c dark 89 275-277"),
    ("12b", "N-acetylimino derivative of compound 10 (compound 12b)", 153, 155, "12b dark 84 153-155"),
    ("12c", "N-acetylimino derivative of compound 10 (compound 12c)", 150, 151, "12c dark 78 150-151"),
    ("13b", "N-benzoylimino derivative of compound 10 (compound 13b)", 241, 242, "13b dark 77 241-242"),
    ("13c", "N-benzoylimino derivative of compound 10 (compound 13c)", 260, 262, "13c brown 79 260-262"),
    ("14c", "N-nitroso derivative of compound 10c (compound 14c)", 250, 251, "14c red 81 250-251"),
    ("15b", "carbonyl benzo[a]quinolizine derivative (compound 15b)", 294, 295, "15b yellow 78 294-295"),
    ("15c", "carbonyl benzo[a]quinolizine derivative (compound 15c)", 244, 246, "15c yellow 83 244-246"),
]

next_id = 18
rows = []
for label, name, lo, hi, prefix in data:
    raw = f"{lo}-{hi} °C"
    mid = (lo+hi)/2
    cmin, cmax = lo, hi
    quote = prefix  # already verbatim from the table
    if quote not in txt:
        print(f"FAIL: {label} quote not in source: {quote!r}")
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
        "evidence_location": f"Table 1, row {label} (column 'm.p. °C')",
        "evidence_quote": quote,
        "conversion_arithmetic": "",
        "notes": "Table 1: column 'm.p.°C'"
    })
    next_id += 1

with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_5.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    for r in rows:
        writer.writerow(r)
print(f"appended {len(rows)} rows, next id={next_id}")

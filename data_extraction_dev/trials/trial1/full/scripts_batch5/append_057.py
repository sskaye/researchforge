import csv

# Paper 057 only contains one specific identifiable compound bp value:
# "NBP of chlorine ... 239 K reported by multiple sources" — confirming literature value
# This is a compiled measured value (data_type = measured)

DOI = "https://doi.org/10.1021/acsomega.5c05503"
SRC = "ACS Omega 2025 (data quality machine learning thermophysical property prediction)"
PATH = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learning_for_Thermophysical_Property_Prediction_A_Cas/article_text.txt"

with open(PATH) as f:
    txt = f.read()

quote = "NBP of chlorine, which is stated to be 993.15 Kfar above the 239 K reported by multiple sources"
if quote not in txt:
    # Try a slightly tighter substring
    print("FAIL: quote not in source")
    print("Trying alt...")
    alt = "239 K reported by multiple sources"
    if alt in txt:
        print(f"Found alt: {alt!r}")
        quote = alt

next_id = 51
row = {
    "id": next_id,
    "verification_status": "pending_verification",
    "compound_name": "chlorine",
    "compound_smiles": "ClCl",
    "property": "boiling_point",
    "value_celsius": -34.15,
    "value_celsius_min": "",
    "value_celsius_max": "",
    "value_raw": "239 K",
    "relation": "=",
    "data_type": "measured",
    "source": SRC,
    "source_url": DOI,
    "evidence_location": "Discussion section, NBP discussion of chlorine",
    "evidence_quote": quote,
    "conversion_arithmetic": "239 K − 273.15 = −34.15 °C",
    "notes": "Paper cites 239 K as the correct value (vs erroneous 993.15 K in original dataset)"
}

with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_5.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    writer.writerow(row)
print(f"appended 1 row, next id={next_id+1}")

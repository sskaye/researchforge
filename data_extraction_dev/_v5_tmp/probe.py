import json, csv, os, sys, re, subprocess, unicodedata

BASE = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev"
os.chdir(BASE)

m = json.load(open("trials/trial2/full-opus47/url_to_folder_built.json"))
rows = list(csv.DictReader(open("trials/trial2/full-opus47/_my_audit_extra_batch_5.csv")))

overrides = {
    "1642": "corpora/full_168/pharma_cocrystals/dichi_2025_polyphenols_thermal",
    "1853": "corpora/full_168/pharma_cocrystals/chmielewska_2020_API_fatty_alcohol_eutectic",
    "75":   "corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors",
}

specific_subdir = {
    "1785": "corpora/full_168/organic_synthesis/gomezayuso_2024_ugi_nitrogen_heterocycles",
    "1830": "corpora/full_168/organic_synthesis/ledermann_2023_iodoindoles_synthesis",
    "1571": "corpora/full_168/organic_synthesis/rios_2026_dhpm_vorinostat",
    "1736": "corpora/full_168/measurement_prediction/muller_2020_dsc-tga-pcm-thermophysical",
    "1469": "corpora/full_168/materials_inorganic/li_2025_coordination_polymer_eutectic",
}

out = []
for r in rows:
    rid = r['id']
    url = r['source_url']
    folder = specific_subdir.get(rid) or overrides.get(rid) or m.get(url)
    exists = folder and (os.path.isdir(folder) or any(os.path.isfile(folder+e) for e in [".pdf",".html",".txt",".nxml"]))
    out.append({
        "id": rid,
        "url": url,
        "folder": folder,
        "exists": exists,
    })

with open("_v5_tmp/folders.json","w") as f:
    json.dump(out, f, indent=2)
print("ok", len(out))

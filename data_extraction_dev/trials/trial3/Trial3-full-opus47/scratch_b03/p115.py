import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Front Chem 2026, 14, 1758992"
URL = "https://doi.org/10.3389/fchem.2026.1758992"

q = "2.4 1-(fluoro (nitro)methyl)-2-(4-fluorophenyl)-1,2,3,4-tetrahydroisoquinoline 4c. (White solid, mp = 85–95 o C, 15.2 mg)"
rows = [["p115_4c_mp","pending_verification","1-(fluoro(nitro)methyl)-2-(4-fluorophenyl)-1,2,3,4-tetrahydroisoquinoline","",
    "melting_point","90","85","95","mp = 85–95 o C","range","measured",
    SOURCE,URL,"Experimental section 2.4",q,"",
    "compound 4c; tetrahydroisoquinoline; broad mp range"]]
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p115")

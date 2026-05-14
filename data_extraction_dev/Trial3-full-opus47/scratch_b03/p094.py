import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2002, 7(1), 96-103"
URL = "https://doi.org/10.3390/70100096"

data = [
    ("7","3-Allyl-6-(allylamino)-2-phenyl-3,4-dihydro-1,3,5-benzotriazocin-4-thione","153-154",153,154,
     "3-Allyl-6-(allylamino)-2-phenyl-3,4-dihydro-1,3,5-benzotriazocin-4-thione ( 7 ): 0.18g (38%); M.p. 153-154 o C"),
    ("8","2-Phenyl-4H-3,1-benzothiazin-4-imine","216-217",216,217,
     "2-Phenyl-4H-3,1-benzothiazin-4-imine ( 8 ): 0.25 g (78%); M.p. 216-217 o C"),
    ("9","2-Phenyl-3,4-dihydroquinazolin-4-thione","162-163",162,163,
     "2-Phenyl-3,4-dihydroquinazolin-4-thione ( 9 ): 0.17g (53%); M.p.162-163 o C"),
    ("10a","2,3-Diphenyl-3,4-dihydroquinazolin-4-imine","214-215",214,215,
     "2,3-Diphenyl-3,4-dihydroquinazolin-4-imine ( 10a ): 0.26g (62%); M.p. 214-215 o C"),
    ("10b","3-(4-Methylphenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine","207-208",207,208,
     "3-(4-Methylphenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine ( 10b ): 0.21g (48%); M.p.207-208 o C"),
    ("10c","3-(4-Chlorophenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine","183-184",183,184,
     "3-(4-Chlorophenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine ( 10c ): 0.27g (57%); M.p. 183-184 o C"),
    ("11","3-Benzyl-6-imino-2-phenyl-3,4,5,6-tetrahydro-1,3,5-benzotriazocin-4-thione","170-171",170,171,
     "3-Benzyl-6-imino-2-phenyl-3,4,5,6-tetrahydro-1,3,5-benzotriazocin-4-thione ( 11 ): 0.19g (38%);M.p. 170-171 o C"),
]
rows = []
for code, name, raw, lo, hi, q in data:
    mid=(lo+hi)/2
    rows.append([f"p094_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"M.p. {raw} oC","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; heterocyclic"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p094")

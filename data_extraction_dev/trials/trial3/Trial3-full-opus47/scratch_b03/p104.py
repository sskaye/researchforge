import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(2), 243-250"
URL = "https://doi.org/10.3390/80200243"

data = [
    ("TetA","Meso-5,5,7,12,12,14-hexamethyl-1,4,8,11-tetraazacyclotetradecane (Tet A) dihydrate","143-145",143,145,"range",
     "Tet A was synthesized as the dihydrate according to the literature [ 13 ] and was recrystallized from water prior to use. Its purity was checked by MP (143-145°C; Lit.146-148°C [ 14 ])"),
    ("TetA_napht","Meso-5,5,7,12,12,14-hexamethyl-1,4,8,11-tetraazacyclotetradecane-1,8-di-(1-methylnaphthalene)","257-260",257,260,"range",
     "Meso-5,5,7,12,12,14-hexamethyl-1,4,8,11-tetraazacyclotetradecane-1,8-di-(1-methylnaphthalene) To a stirred solution of 1-chloromethylnaphthalene (8.66g, 0.0490 mol) in THF (20 mL) was added tetA.2H 2 O (7.75g, 0.0242 mol) in methanol (100 mL) and a solution containing Na 2 CO 3 (5.20g, 0.0490 mol) in water (40 mL). The reaction mixture was refluxed for 24 hours. The solution was cooled to room temperature and the white solid that had precipitated during the reaction was filtered, washed with cold water and air-dried. The solid was recrystallized from THF and water (yield 6.75 g (81.4 %)). M.P. 257 - 260 ° C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    mid=(lo+hi)/2
    rows.append([f"p104_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"M.P. {raw}°C","range","measured",
        SOURCE,URL,"Synthesis",q,"",f"compound {code}; tetraazacyclotetradecane"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p104")

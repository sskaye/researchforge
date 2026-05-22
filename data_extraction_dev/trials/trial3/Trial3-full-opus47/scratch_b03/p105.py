import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(5), 481-495"
URL = "https://doi.org/10.3390/60500481"

data = [
    ("36","4-Amino-3-phenyl-1H-1,2,4-triazole","86-88",86,88,"range",
     "(96.71 g, 0.66 mol) was mixed with 260 mL of hydrazine hydrate (99%) and the mixture heated at 140 °C in a sealed tube over night. The precipitate was formed was isolated by filtration to yield 63.3 g (79%) of 36 as white needle shaped crystals, (m.p. 86-88 °C)"),
    ("18","3-Phenyl-1H-1,2,4-triazole","115-117",115,117,"range",
     "3-phenyl-1,2,4-triazole ( 18 ), which was obtained after repeated sublimation (140 °C, 5 mmHg) in 4.71 g (17 %) yield as a white powder with melting point 115-117 °C"),
    ("7","4-(Trans-2-butenyl)-5-methyl-3-phenyl-4H-1,2,4-triazole","103-104",103,104,"range",
     "4-(Trans-2-butenyl)-5-methyl-3-phenyl-4H-1,2,4-triazole ( 7 ). A solution containing 2-methyl-5-phenyl-1,3,5-oxadiazole (1.53 g, 9.58 mmol) and crotylamine (1.02 g, 14.4 mmol) in toluene (4 mL) was refluxed for 7 days. The crude product (2.05 g), gave after crystallization from toluene gave 0.98 g (48%) of pure 7 as colorless crystals. Mp. 103-104 °C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    mid=(lo+hi)/2
    rows.append([f"p105_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw} °C","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; triazole"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p105")

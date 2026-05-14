import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(7), 536-540"
URL = "https://doi.org/10.3390/80700536"

data = [
    ("1","1-Pentafluorophenyl-1H-Pyrrole","58-60",58,60,
     "1-pentafluorophenyl- 1H -pyrrole ( 1 ) (0.44 g, 1.89 mmol)"),
    ("2a","1-Pentafluorophenyl-1H-Pyrrole-2-Carbaldehyde","77-79",77,79,
     "to yield 2a as a colorless crystalline solid (0.38 g, 76% yield); m.p. 77-79 o C"),
    ("2b","1-(1-Pentafluorophenyl-1H-pyrrole-2-yl)-ethanone","45-48",45,48,
     "1-(1 -Pentafluorophenyl-1H-pyrrole-2-yl) -ethanone ( 2b ): 0.83 g (70% yield); m.p: 45-48 o C"),
    ("2c","1-(1-Pentafluorophenyl-1H-pyrrole-2-yl)-propan-1-one","75-77",75,77,
     "1-(1 -Pentafluorophenyl-1H-pyrrole-2-yl) -propan-1-one ( 2c ): 0.89 g (72% yield); m.p. 75-77 o C"),
    ("3a","1-Pentafluorophenyl-1H-pyrrole-3-carbaldehyde","53-56",53,56,
     "1 -Pentafluorophenyl-1H-pyrrole-3-carbaldehyde ( 3a ): m.p. 53-56 o C"),
    ("3b","1-(1-Pentafluorophenyl-1H-pyrrole-3-yl)-ethanone","114-115",114,115,
     "1 -(1 -Pentafluorophenyl-1H-pyrrole-3-yl) -ethanone ( 3b ): m.p. 114-115 o C"),
    ("3c","1-(1-Pentafluorophenyl-1H-pyrrole-3-yl)-propan-1-one","102-104",102,104,
     "1 -(1 -Pentafluorophenyl-1H-pyrrole-3-yl) -propan-1-one ( 3c ): m.p. 102-104 o C"),
]
# Custom evidence for compound 1: include the proper m.p. portion
data[0] = ("1","1-Pentafluorophenyl-1H-Pyrrole","58-60",58,60,
     "pure pyrrole 1 (2.98 g, 78% yield), m.p. 58-60 o C")

rows = []
for code, name, raw, lo, hi, q in data:
    mid = (lo+hi)/2
    rows.append([f"p088_{code}_mp","pending_verification",name,"",
                 "melting_point",f"{mid:g}",str(lo),str(hi),
                 f"m.p. {raw} oC","range","measured",
                 SOURCE,URL,"Experimental",q,"",f"compound {code}; pentafluorophenyl pyrrole"])
with open(csv_path,"a",newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p088")

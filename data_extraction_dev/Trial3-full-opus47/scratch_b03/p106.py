import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(8), 683-693"
URL = "https://doi.org/10.3390/60800683"

data = [
    ("6","2-(5-hydroxy-2-nitrophenyl)-4,6-dimethyl-1,2-dihydropyridine-3,5-dicarboxylic acid diethyl ester","206-208",206,208,"range",
     "into compounds 1 (5.57 g, 48 %) and 6 (2.32 g, 20 %); m.p. 206-208°C (hexane/ethyl acetate)"),
    ("7","4,6-Dimethyl 2-(2-nitro-phenyl)-1,2-dihydro-pyridine-3,5-dicarboxylic acid diethyl ester","158-160",158,160,"range",
     "and 7 (4.90 g, 20%), m.p. 158-160 °C; IR (CHCl 3 film) ν max /cm −1 : 3450 (NH), 1710 (C=O), 1650 (C=O)"),
    ("17","3-(2-oxopropyl)-1H-indole-2-carboxylic acid ethyl ester","114-116",114,116,"range",
     "3-(2-oxopropilpropyl)-1H-indole-2-carboxilatecarboxylic acid ethyl ester ( 17 ) (0.21 g, 40%); m.p. 114-116 °C"),
    ("18","3-(2-oxopropyl)-5-hydroxy-1H-indole-2-carboxylic acid ethyl ester","154-156",154,156,"range",
     "3-(2-oxopropyl)-5-hydroxy-1H-indole-2-carboxylic acid ethyl ester ( 18 ), m.p.Mp 154-156 °C, ; yield 0.313 g (56 %)"),
    ("12","2-methyl-quinoline-3-carboxylic acid ethyl ester","74-76",74,76,"range",
     "2-methyl- quinoline-3-carboxylic acid ethyl ester ( 12 ), m.p. 74-76 °C"),
    ("19","6-hydroxy-2-methyl-quinoline-3-carboxylic acid ethyl ester","98-100",98,100,"range",
     "6-hydroxy-2-methyl-oxyquinoline-3-carboxylic acid ethyl ester ( 19 , 0.3 g (54%); m.p. 98-100 °C"),
    ("20","6-hydroxy-2-methylquinoline-3-carboxylic acid ethyl ester","153-155",153,155,"range",
     "6-hydroxy-2-methylquinoline-3-carboxylic acid ethyl ester ( 20 ), yield 0.35 g (60 %); m.p. 153-155 °C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    mid=(lo+hi)/2
    rows.append([f"p106_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw}°C","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; Hantzsch product"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p106")

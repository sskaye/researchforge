import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2026, 31(5), 796"
URL = "https://doi.org/10.3390/molecules31050796"

data = [
    ("6","2-[(1'R,6'R)-6'-Isopropenyl-3'-methylcyclohex-2-en-1-yl]-4-[(E)-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol","45-48",45,48,
     "2-[(1′ R ,6′ R )-6′-Isopropenyl-3′-methylcyclohex-2-en-1-yl]-4-[( E )-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol ( 6 ): CBD (0.19 mmol scale), quantitative yield; purple solid; R f 0.38 (hexane/ethyl acetate = 5/1); mp 45–48 °C"),
    ("7","(Z)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6-dihydro-1H-benzo[c]chromen-1-one","130-132",130,132,
     "( Z )-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6-dihydro-1 H -benzo[ c ]chromen-1-one ( 7 ): CBN (0.19 mmol scale), 58% yield; orange solid; R f 0.13 (hexane/ethyl acetate = 10/1); mp 130–132 °C"),
    ("8","(Z)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6-dihydro-1H-benzo[c]chromen-1-one","63-65",63,65,
     "( Z )-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6-dihydro-1 H -benzo[ c ]chromen-1-one ( 8 ): 20% yield; brown solid; R f 0.50 (hexane/ethyl acetate = 10/1); mp 63–65 °C"),
    ("9","(Z)-(6aR,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,10a-hexahydro-1H-benzo[c]chromen-1-one","76-79",76,79,
     "( Z )-(6a R ,10a R )-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,10a-hexahydro-1 H -benzo[ c ]chromen-1-one ( 9 ): THC (50 μmol scale), 30% yield; red solid; R f 0.14 (hexane/ethyl acetate = 5/1); mp 76–79 °C"),
    ("10","(Z)-(6aR,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,10a-hexahydro-1H-benzo[c]chromen-1-one","63-65",63,65,
     "( Z )-(6a R ,10a R )-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,10a-hexahydro-1 H -benzo[ c ]chromen-1-one ( 10 ): 10% yield; red solid; R f 0.71 (hexane/ethyl acetate = 5/1); mp 63–65 °C"),
    ("11","2-[(E)-3,7-Dimethylocta-2,6-dien-1-yl]-4-[(E)-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol","72-74",72,74,
     "2-[( E )-3,7-Dimethylocta-2,6-dien-1-yl]-4-[( E )-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol ( 11 ): CBG (0.19 mmol scale), 83% yield; brown solid; R f 0.75 (hexane/dichloromethane = 4/1); mp 72–74 °C"),
    ("12","(Z)-(6aR,9S,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one","88-91",88,91,
     "( Z )-(6a R ,9 S ,10a R )-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1 H -benzo[ c ]chromen-1-one ( 12 ): HHC (0.16 mmol scale), 17% yield; orange solid; R f 0.38 (hexane/ethyl acetate = 6/1 × 3); mp 88–91 °C"),
    ("13","(Z)-(6aR,9R,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one","92-94",92,94,
     "( Z )-(6a R ,9 R ,10a R )-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1 H -benzo[ c ]chromen-1-one ( 13 ): 29% yield; orange solid; R f 0.50 (hexane/ethyl acetate = 6/1 × 3); mp 92–94 °C"),
    ("14","(Z)-(6aR,9S,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one","46-49",46,49,
     "( Z )-(6a R ,9 S ,10a R )-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1 H -benzo[ c ]chromen-1-one ( 14 ): 6% yield; orange solid; R f 0.50 (hexane/ethyl acetate = 6/1 × 2); mp 46–49 °C"),
    ("15","(Z)-(6aR,9R,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one","48-50",48,50,
     "( Z )-(6a R ,9 R ,10a R )-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1 H -benzo[ c ]chromen-1-one ( 15 ): 12% yield; red solid; R f 0.38 (hexane/ethyl acetate = 6/1 × 2); mp 48–50 °C"),
    ("16","2-Methyl-2-(4-methylpent-3-en-1-yl)-6-[(E)-(4-nitrophenyl)diazenyl]-7-pentyl-2H-chromen-5-ol","62-65",62,65,
     "2-Methyl-2-(4-methylpent-3-en-1-yl)-6-[( E )-(4-nitrophenyl)diazenyl]-7-pentyl-2 H -chromen-5-ol ( 16 ): CBC (0.33 mmol scale), 75% yield; brown solid R f 0.75 (hexane/dichloromethane = 2/1); mp 62–65 °C"),
    ("17","2,4-Dihydroxy-3-[(1'R,6'R)-6'-isopropenyl-3'-methylcyclohex-2-en-1-yl]-5-[(E)-(4-nitrophenyl)diazenyl]-6-pentylbenzoic acid","76-78",76,78,
     "2,4-Dihydroxy-3-[(1′ R ,6′ R )-6′-isopropenyl-3′-methylcyclohex-2-en-1-yl]-5-[( E )-(4-nitrophenyl)diazenyl]-6-pentylbenzoic acid ( 17 ): CBDA (0.41 mmol scale), 18% yield; orange solid R f 0.13 (hexane/ethyl acetate = 6/1); mp 76–78 °C"),
]
rows=[]
for code, name, raw, lo, hi, q in data:
    mid=(lo+hi)/2
    rows.append([f"p116_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"mp {raw} °C","range","measured",
        SOURCE,URL,"Spectral Data section 3.4",q,"",f"compound {code}; azo/quinoneimine cannabinoid product"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p116")

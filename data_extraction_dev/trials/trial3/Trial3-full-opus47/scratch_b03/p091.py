import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Int J Mol Sci 2007, 8(4), 304-315"
URL = "pmc:PMC3685385"

rows = []
# Compound 1 [C2Allylsul]Br : mp 145°C
rows.append(["p091_1_mp","pending_verification","[C2Allylsul]Br (diethyl-allyl-sulfonium bromide)","",
    "melting_point","145","145","145","M.p. 145° C","equal","measured",
    SOURCE,URL,"Synthesis section",
    "yield: 20.6 g, 98%; M.p. 145° C","",
    "compound 1; allyl-sulfonium bromide ionic liquid"])

# Table 1: Tm values listed only for compound 3
rows.append(["p091_3_mp","pending_verification","[C2Allylsul][Tf2N] (diethyl-allyl-sulfonium bis(trifluoromethanesulfonyl)imide)","",
    "melting_point","-60.19","-60.19","-60.19","T m −60.19 °C","equal","measured",
    SOURCE,URL,"Table 1 Physical properties of allyl-sulfonium ionic liquids",
    "Ionic liquids T g (°C) T m (°C) η (cP, 20°C) [C 4 Allylsul]I 2 −60.12 - 1080.0 [C 2 Allylsul][Tf 2 N] 3 - −60.19 42.6","",
    "compound 3; from Table 1 Tm column"])

# Tg values - report as glass transition? Spec says properties limited; skip Tg (not in scope)
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p091")

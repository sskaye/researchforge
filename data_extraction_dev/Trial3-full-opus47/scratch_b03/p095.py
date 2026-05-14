import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(3), 267-278"
URL = "https://doi.org/10.3390/60300267"

data = [  # code, name, raw, val(int), q
    ("2a","Methyl N-[phenylsulphonyl-glycyl]anthranilate",125,
     "Methyl N-[phenylsulphonyl-glycyl]anthranilate (2a).- From phenylglycyl chloride as colourless crystals (65%), m.p. 125°C"),
    ("2b","Methyl N-[4'-methylphenylsulphonyl-2-phenylglycyl]anthranilate",155,
     "Methyl N-[4'-methylphenylsulphonyl-2-phenylglycyl]anthranilate (2b).- From tosyl 2-phenylglycyl acid chloride as colourless crystals (71%) , m.p. 155°C"),
    ("2c","Methyl N-[4'-methylphenylsulphonyl-phenylalaninyl]anthranilate",120,
     "Methyl N-[4'-methylphenylsulphonyl-phenylalaninyl]anthranilate (2c).- From tosyl phenylalaninyl acid chloride as colourless crystals (68%), m.p. 120°C"),
    ("2d","Methyl N-[4'-methylphenylsulphonyl-β-alaninyl]anthranilate",130,
     "Methyl N-[4'-methylphenylsulphonyl- β -alaninyl]anthranilate (2d) .- From tosyl-β-alaninyl acid chloride as colourless crystals (73%), m.p. 130°C"),
    ("2e","Methyl N-[4'-methylphenylsulphonyl-DL-valinyl]anthranilate",170,
     "Methyl N-[4'-methylphenylsulphonyl-DL-valinyl]anthranilate (2e).- From tosyl-DL-valinyl acid chloride as colourless crystals (75%), m.p. 170°C"),
    ("2f","Methyl N-[4'-methylphenylsulphonyl-DL-leucinyl]anthranilate",165,
     "Methyl N-[4'-methylphenylsulphonyl-DL-leucinyl]anthranilate (2f) .- From tosyl-DL-leucine acid chloride as colourless crystals (68%), m.p. 165°C"),
    ("3a","3-Amino-2-(phenylsulphonamidomethyl)quinazolin-4(3H)-one",180,
     "3-Amino-2-(phenylsulphonamidomethyl)quinazolin-4(3H)-one (3a).- Colourless crystals (74%); m.p. 180°C"),
    ("3b","3-Amino-2-[1'(4-methylphenylsulphonyl)-1'-(phenyl)methyl]quinazolin-4(3H)-one",135,
     "3-Amino-2-(1`(4-methylphenylsulphonyl)-1`-(phenyl)methyl]quinazolin-4(3H)-one (3b).- Colourless crystals (65%), m.p. 135°C"),
    ("3c","3-Amino-2-[1'(4-methyl phenylsulphonamido)-1'-(benzyl)methyl]quinazoline-4(3H)-one",170,
     "3-Amino 2-[1`(4-methyl phenylsulphonamido)-1`-(benzyl)methyl]quinazo-line-4-(3H)-one (3c).- Colourless crystals (68%), m.p. 170°C"),
    ("3d","3-Amino-2-[4-methyl phenylsulphonamidoethyl]quinazolin-4-(3H)-one",185,
     "3-Amino-2-[4-methyl phenylsulphonamidoethyl]quinazolin-4-(3H)-one (3d).- Colourless crystals (70%), m.p. 185°C"),
    ("3e","3-Amino-2-[1'-(4-methylphenylsulphonamido)-1'-(iso-propyl)methyl]quinazolin-4-(3H)-one",190,
     "3-Amino-2-[1`-(4-methylphenylsulphonamido)-1`-(iso-propyl)methyl]quinazolin-4-(3H)-one (3e).- Colourless crystals (76%), m.p. 190°C"),
    ("3f","3-Amino-2-[1'-(4-methylphenylsulphonamido)-1'-(iso-butyl)methyl]quinazolin-4-(3H)-one",170,
     "3-Amino 2-[1`-(4-methylphenylsulphonamido)-1`-(iso-butyl)methyl]quina-zolin-4-(3H)-one (3f).- Colourless crystals (71%), m.p. 170°C"),
    ("4","Schiff's base of 3-amino-2-[1'-(4-methyl phenyl sulphonamido)-1'-(iso-propyl)methyl]-quinazolin-4-(3H)-one (4-chlorobenzaldehyde Schiff base)",160,
     "Schiff’s base of 3-amino-2-[1`-(4-methyl phenyl sulphonamido)-1`-(iso-propyl)methyl]-quinazolin-4-(3H)-one (4).- Prepared from 3e (0.01 mol) and 4-chlorobenzaldehyde (0.01 mol) in acetic acid (20 mL). The mixture was refluxed for 4 hrs., cooled and colected by filteration as pale brown crystals (69%); m.p. 160°C"),
    ("5a","2-(4-Chlorophenyl)-4,5,11-trihydro-1H[1,2,4]triazepino[7,1-b]quinazolin-11-one",260,
     "2-(4-Chlorophenyl)-4,5,11-trihydro-1H[1,2,4]triazepino[7,1-b]quinazolin-11-one (5a).- Prepared from 3d and 4-chlorobenzaldehyde as brown crystals (67%), m.p. 260°C"),
    ("5b","2-(4-Fluorophenyl)-4-isopropyl-4,10-dihydro-1H[1,2,4]triazino[6,1-b]-quinazolin-10-one",180,
     "2-(4-Fluorophenyl)-4-isopropyl-4,10-dihydro-1H[1,2,4]triazino[6,1-b]-quinazolin-10-one (5b).- Prepared from 3e and 4-fluorobenzaldehyde as pale brown crystals (62%), m.p. 180°C"),
    ("5c","2-(4-Methoxyphenyl)-4-isopropyl-4,10-dihydro-1H-[1,2,4]triazino[6,1-b]quinazolin-10-one",170,
     "2-(4-Methoxyphenyl-4-isopropyl-4,10-dihydro-1H-[1,2,4]triazino[6,1-b] quinazolin-10-one (5c).- Prepared from 3e and 4-methoxybenzaldehyde as brown crystals (60%), m.p. 170°C"),
    ("7","2-[11-Oxo-5,11-dihydro-1H-[1,2,4]triazepino[7,1-b]quinazolin-2-ylidine]-malononitrile",250,
     "2-[11-Oxo5,11-dihydro-1H-[1,2,4]triazepino[7,1-b]quinazolin-2-ylidine]-malononitrile (7).- From 3d and [bis(methylthio)methylene]malononitrile as yellow crystals (61%); m.p. 250°C"),
    ("9","Ethyl 1-[11-oxo-5,11-dihydro-[1,2,4]triazepino[7,1-b]quinazolinyl]formate",265,
     "Ethyl 1-[11-oxo-5,11-dihydro-[1,2,4]triazepino[7,1-b]quinazolinyl]formate (9).- Prepared from 3d (0.01 mol), ethyl chloroformate (0.03 mol) and TEA (0.5 mL) in DMF (20 mL). The mixture was refluxed for 8 hrs., cooled and acidified with dil. HCl. The solid obtained was collected and crystallized to give 9 as pale brown crystals (60%), m.p. 265°C"),
]
# Compounds with >300°C
data_gt = [
    ("6a","6,7,9,14,17-Pentahydronaphtho[2',3':3,4][1,2,5]triazocino[8,1-b]quinazolin-9,14,17-trione",300,
     "6,7,9,14,17-Pentahydronaphtho[2`,3`:3,4][1,2,5]triazocino[8,1-b]qinozolin-9,14,17-trione (6a).- Prepared in a similar fashion as 6a from 3d and 2,3-dichloro-1,4-naphthoquinone as deep brown crystals (63%), m.p. > 300°C"),
    ("6b","6-Isopropyl-6,8,13,16-tetrahydronaphtho[2',3':3,4][1,2,5]triazepino[7,1-b]-quinazolin-8-one",300,
     "(6b).- Prepared from 3e (0.01 mol); 2,3-dichloro-1,4-naphthoquinone (0.01 mol) in DMF (20 mL) and TEA (0.05 mL), the reaction mixture was refluxed for 6 hrs., cooled and acidified with HCl, the precipitate was filtered, washed with water and recrystallized to give 6a as dark brown crystals (60%); m.p. > 300°C"),
    ("7_alt","2-[11-Oxo-5,11-dihydro-1H-[1,2,4]triazepino[7,1-b]quinazolin-2-ylidine]-malononitrile (alternate prep)",300,
     "Cooling and acidification caused the precipitation of the product which was then collected and recrystallized to give 7 as pale yellow crystals (66%), m.p. > 300°C"),
    ("10","Ethyl-1-[12-oxo-6,12-dihydro[1,2,5]triazocino[8,1-b]quinazolinyl]acetate",300,
     "Ethyl-1-[12-oxo-6,12-dihydro[1,2,5]triazocino[8,1-b]quinazolinyl]acetate (10).- Prepared like 9 from 3d and ethyl chloroacetate as pale brown crystals (63%), m.p. > 300°C"),
]

rows=[]
for code, name, mp, q in data:
    rows.append([f"p095_{code}_mp","pending_verification",name,"",
        "melting_point",str(mp),str(mp),str(mp),f"m.p. {mp}°C","equal","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; quinazolinone"])
for code, name, mp, q in data_gt:
    rows.append([f"p095_{code}_mp","pending_verification",name,"",
        "melting_point",str(mp),"","",f"m.p. >{mp}°C","greater_than","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; >{mp}°C"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p095")

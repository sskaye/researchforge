import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2002, 7(2), 124-128"
URL = "https://doi.org/10.3390/70200124"

# Table 1: compounds 4a, 4b, 4c, trans-4d, trans-4e, trans-4f, trans-4g
# m.p. °C 135-6  >210 decom  147-8  176-7  183-4  Oil  172-3
table_q = "Table 1 Melting Points and Yields of Compounds 4a-g . Compound 4a 4b 4c trans -4d trans -4e trans -4f trans -4g m.p. °C 135-6 1) >210 decom 147-8 1) 176-7 1) 183-4 1) Oil 172-3 1)"

# 1a-1g from experimental sentence with their mps
text_q1 = "N-(3-Oxoalkyl)amides 1a (56%, m.p. 90-91°C); 1b ( 81 %, m.p. 104-105°C) and anti - 1e (14%, m.p.156-157°C) were obtained from the α,β-unsaturated ketones and chloroacetonitrile [ 6 , 9 ]; compounds 1c ( 69%, m.p. 109-110°C) and anti - 1g (55%, m.p. 74-75°C) — by reaction of Cl 3 CCH=NCOCH 2 Cl with enamines [ 7 ]; compound anti - 1d (88%, m.p.124-125°C) — by acylation of 1-( trans -2-aminocyclohexyl)-1-ethanone with chloroanhydride of chloroacetic acid [ 9 ]; compound 1f (19%, m.p. 201-202°C) — by interaction of (1-cyclohexenyloxy)(trimethyl)silane with PhCH=NMe and ClCH 2 COCl in the presence of TiCl 4 [ 9 ]."

rows = []
# Compounds 1a-1g
data1 = [
    ("1a","N-(3-Oxoalkyl)amide 1a","90-91",90,91,"range"),
    ("1b","N-(3-Oxoalkyl)amide 1b","104-105",104,105,"range"),
    ("1c","N-(3-Oxoalkyl)amide 1c","109-110",109,110,"range"),
    ("anti-1d","anti-N-(3-Oxoalkyl)amide 1d","124-125",124,125,"range"),
    ("anti-1e","anti-N-(3-Oxoalkyl)amide 1e","156-157",156,157,"range"),
    ("1f","N-(3-Oxoalkyl)amide 1f","201-202",201,202,"range"),
    ("anti-1g","anti-N-(3-Oxoalkyl)amide 1g","74-75",74,75,"range"),
]
for code, name, raw, lo, hi, rel in data1:
    mid=(lo+hi)/2
    rows.append([f"p097_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw}°C","range","measured",
        SOURCE,URL,"Experimental",text_q1,"",f"compound {code}; N-(3-oxoalkyl)chloroacetamide"])

# Compounds 4a-4g — use table_q
data4 = [
    ("4a","5,6-dihydropyridin-2(1H)-one 4a","135-136",135,136,"range"),
    ("4c","5,6-dihydropyridin-2(1H)-one 4c","147-148",147,148,"range"),
    ("trans-4d","trans-4a,5,6,7,8,8a-hexahydroquinolin-2(1H)-one trans-4d","176-177",176,177,"range"),
    ("trans-4e","trans-4a,5,6,7,8,8a-hexahydroquinolin-2(1H)-one trans-4e","183-184",183,184,"range"),
    ("trans-4g","trans-4a,5,6,7,8,8a-hexahydroquinolin-2(1H)-one trans-4g","172-173",172,173,"range"),
]
for code, name, raw, lo, hi, rel in data4:
    mid=(lo+hi)/2
    rows.append([f"p097_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw}°C","range","measured",
        SOURCE,URL,"Table 1",table_q,"",f"compound {code}; from Table 1"])
# 4b: >210 decom
rows.append(["p097_4b_decomp","pending_verification","5,6-dihydropyridin-2(1H)-one 4b","",
    "decomposition","210","","","m.p. >210 decom","greater_than","measured",
    SOURCE,URL,"Table 1",table_q,"",
    "compound 4b; >210°C decomp from Table 1"])
# 4f is Oil — skip (no mp)

with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p097")

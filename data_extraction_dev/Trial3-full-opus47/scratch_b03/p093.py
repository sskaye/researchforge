import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(8), 622-641"
URL = "https://doi.org/10.3390/80800622"

# Compound 2 is 4,4'-diacetyldiphenyl sulphide (from context: AlCl3+acetyl chloride+diphenylsulphoxide). Actually it's about diphenylsulphide. The name "( 2 )" is referenced in next compound prep "compound 2 (0.58 g, 0.00214 mole) in ethanol" but this paragraph at m.p 90-92 doesn't display "( 2 )". The previous header is the named compound. Search up more context.
# Actually based on "4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphide ( 5 ). A mixture of 2 (1.0 g, 0.0037 mole)" => 2 is "4,4'-diacetyl diphenyl sulphide" — but we need a verbatim quote with name+value. The first paragraph isn't preceded by a name printed adjacent. SKIP compound 2.

data = [
    ("5","4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphide","190-192",190,192,"range",
     "4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphide ( 5 ). A mixture of 2 (1.0 g, 0.0037 mole) and 3 (0.675 g, 0.0074 mole) in ethanol (30 mL) was refluxed for 7 hr in presence of two drops of piperidine. On cooling, yellow crystals separated from the reaction mixture and were recrystallized from C 2 H 5 OH. Yield 74.8%; m.p 190-192°C"),
    ("6","4,4'-Diacetylsemicarbazone diphenyl sulphide","300",300,300,"greater_than",
     "4,4'-Diacetylsemicarbazone diphenyl sulphide ( 6 ). To a mixture of semicarbazide hydrochloride (0.92 g, 0.00824 mole) and AcONa (1.04 g, 0.01264 mole) dissolved in water (8 mL) a solution of 2 (0.58 g, 0.00214 mole) in ethanol was added with continuous shaking. Ethanol was added if necessary to obtain a clear solution. Shaking was continued for further one hour, and the mixture was cooled in the refrigerator. The separated crystals were filtered off, washed with cold water, dried and crystallized from acetic acid. Yield 85.70%; m.p >300°C (decomp.)"),
    ("7","4-Acetyl-4'-acetylsemicarbazone diphenyl sulphide","190-191",190,191,"range",
     "4-Acetyl-4'-acetylsemicarbazone diphenyl sulphide ( 7 ). A solution of compound 2 (0.58 g, 0.00214 mole) in ethanol was added with continuous shaking to a mixture of 4 (0.23 g, 0.00206 mole) and AcONa (0.26 g, 0.00316 mole) dissolved in water (8 mL). The reaction mixture was worked up as in the case of 6 . The separated crystals were filtered off, washed with cold water, dried and crystallized from ethanol, m.p 190-191°C"),
    ("8","4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphide","300",300,300,"greater_than",
     "4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphide ( 8 ). This compound was obtained by the following two methods: Method A: To a mixture of 4 (0.08 g, 0.00582 mole) and AcONa (0.35 g, 0.0042 mole) dissolved in water (≈ 8 mL), a solution of 5 (1.0 g, 0.00291 mole) in ethanol was added with continuous shaking. The reaction mixture was worked up as in the case of 6 . The crystals formed were filtered off, washed with cold water, dried and recrystallized from AcOH, m.p >300°C (decomp.)"),
    ("14","4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphone","185",185,185,"equal",
     "4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphone ( 14 ). A mixture of 13 (1.0 g, 0.0033 mole) and 3 (0.675 g, 0.0074 mole) in ethanol (30 mL) containing a few drops of piperidine was refluxed for 7 hr. After cooling the pale yellow crystals formed were separated and recrystallized from ethanol, m.p 185°C"),
    ("15","4-Acetylsemicarbazone-4'-acetyldiphenyl sulphone","200",200,200,"equal",
     "4-Acetylsemicarbazone-4'-acetyldiphenyl sulphone ( 15 ). To a mixture of compound 5 (0.36 g, 0.0012 mole) and AcONa (0.26 g, 0.003) dissolved in water (8 mL) a solution of 13 (1.0 g, 0.0031 mole) in ethanol was added with continuous shaking. The reaction mixture was worked up as previously mentioned in the case of 6 . The separated crystals were filtered off, washed with cold water, dried and crystallized from ethanol, m.p 200°C"),
    ("16","4,4'-Diacetylthiosemicarbazone diphenyl sulphone","350",350,350,"greater_than",
     "4,4'-Diacetylthiosemicarbazone diphenyl sulphone ( 16 ). A mixture of 14 (1.0 g, 0.0026 mole) and 3 (0.972 g, 0.01 mole) in ethanol (30 mL) containing a few drops of piperidine was refluxed for 7 hr. After cooling the pale yellow crystals formed were separated, crystallized from AcOH, m.p >350 (decomp.)"),
    ("17","4,4'-Diacetylsemicarbazone diphenyl sulphone","350",350,350,"greater_than",
     "4,4'-Diacetylsemicarbazone diphenyl sulphone ( 17 ). To a mixture of 4 (1.47 g, 0.013 mole) and AcONa (0.81 g, 0.0099 mole) dissolved in water (8 mL) a solution of 13 (1.0 g, 0.00316 mole) in ethanol was added with continuous shaking. The reaction mixture was worked up as in the case of 6 . The separated crystals were filtered off, washed with cold water, dried and crystallized from AcOH, m.p >350°C (decomp.)"),
    ("18","4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphone","350",350,350,"greater_than",
     "4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphone ( 18 ). This compound was prepared by the following two methods: Method A: To a mixture of 4 (0.59 g, 0.00533 mole) and AcONa (0.32 g, 0.004 mole) dissolved in water (≈ 8 mL), a solution of 14 (1.0 g, 0.00266 mole) in ethanol was added with continuous shaking. The reaction mixture was worked up as in the case of 6 . The separated crystals were filtered off, washed with cold water, dried and crystallized from AcOH, m.p >350°C (decomp.)"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    if rel=="range":
        mid=(lo+hi)/2
        rows.append([f"p093_{code}_mp","pending_verification",name,"",
            "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p {raw}°C","range","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; diaryl sulphide/sulphone"])
    elif rel=="equal":
        rows.append([f"p093_{code}_mp","pending_verification",name,"",
            "melting_point",str(lo),str(lo),str(lo),f"m.p {raw}°C","equal","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; diaryl sulphide/sulphone"])
    elif rel=="greater_than":
        rows.append([f"p093_{code}_mp","pending_verification",name,"",
            "decomposition",raw,"","",f"m.p >{raw}°C (decomp.)","greater_than","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; decomp. observed; diaryl sulphone"])

with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p093")

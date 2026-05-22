import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(4), 300-322"
URL = "https://doi.org/10.3390/60400300"

data = [
    ("4a","2,2'-Diaminobenzophenone (4a)","134",134,134,"equal",
     "afford 4a (195 mg, quantitative yield), yellow crystals (from 80% aqueous methanol), m.p. 134°C"),
    ("4b","2,2'-Diamino-4,4'-dimethoxybenzophenone","138",138,138,"equal",
     "2,2’-Diamino-4,4’-dimethoxybenzophenone ( 4b ): 4b was prepared from 2,2’-Dinitro-4,4’-dimethoxybenzophenone [ 20 ] (250 mg, 0.75 mmol) under the same conditions as described for the synthesis of 4a . The product was recrystallized from methanol to afford 4b (185 mg, 90%): m.p. 138°C"),
    ("5a","2-(2'-aminobenzophenyl)amino-1,4-naphthoquinone","208",208,208,"equal",
     "to afford 5a (420 mg, 54%), red prisms (from EtOH), m.p. 208°C"),
    ("5b","2-(2'-amino-4,4'-dimethoxybenzophenyl)amino-1,4-naphthoquinone","214",214,214,"equal",
     "compound 5b was isolated (150 mg, 48%): red prisms (from EtOH), m.p. 214°C"),
    ("6a","10H-benzo[i]quino[2,3,4-kl]acridin-10-one","255",255,255,"equal",
     "10H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 6a ): ... eluting with CHCl 3 /MeOH 30:1) to afford 6a (335 mg, 93%), amorphous powder (CHCl 3 /MeOH, 9:1), m.p. 255°C"),
    ("6b","2,7-Dimethoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one","296",296,296,"equal",
     "Dimethoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 6b ): 5b (150 mg, 0.35 mmol) was treated with ammonia in methanol by the same procedure described for the synthesis of 6a . The product ( 6b ) was obtained after chromatography (eluting with chloroform/methanol, 30:1) (130 mg, 95%): amorphous powder (CHCl 3 /MeOH, 8:2), m.p. 296°C"),
    ("8","10H-benzo[i]pyrido[2,3,4-kl]acridin-9-one","258",258,258,"equal",
     "H-benzo[i]pyrido[2,3,4-kl]acridin-9-one ( 8 ): ... to afford 8 (70mg, 13%), amorphous powder (chloroform/methanol, 9:1), mp 258°C"),
    ("9","3(N)-(2,2'-diaminobenzophenone)-5-hydroxy-1,4-naphthoquinone","221",221,221,"equal",
     "3(N)-(2,2’-diaminobenzophenone)-5-hydroxy-1,4-naphthoquinone ( 9 ): 4a (100 mg, 0.47 mmol) and CeCl 3 ·7H 2 O (186 mg, 0.5 mmol) ... The solvent was then evaporated and the red product purified by chromatography (eluting with CHCl 3 /MeOH, 100:1) (144mg, 80%): red prisms (from EtOH), m.p. 221°C"),
    ("10","Hydroxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one","292",292,292,"equal",
     "Hydroxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 10 ): ... to afford 10 (61 mg, 98%), yellow needles (CHCl 3 -MeOH 50:1), m.p. 292°C"),
    ("11","Acetoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one","222",222,222,"equal",
     "Acetoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 11 ): 10 (10 mg, 0.029 mmol) was acetylated with acetic anhydride-pyridine, 1:1 (1 mL), at room temperature for 24 h. The reaction mixture was evaporated and chromatographed (eluting with CHCl 3 /MeOH, 40:1) to give 11 (11 mg, 95%), yellow needles (CHCl 3 /MeOH, 100:1), m.p. 222oC"),
    ("14","N-(4-methoxyaniline)-5-hydroxy-1,4-naphthoquinone","211",211,211,"equal",
     "N-(4-methoxyaniline)-5-hydroxy-1,4-naphthoquinone ( 14 ): ... (65 mg, 69%): red crystals (ethanol), m.p. 211°C"),
    ("17a","10H,11H,12H-dihydroquino[2,3,4-kl]acridine","186",186,186,"equal",
     "to afford 17a (515 mg, quantitative), amorphous powder (CHCl /MeOH, 20:1), m.p. 186°C"),
    ("17b","2,7-Dimethoxy-10H,11H,12H-dihydroquino[2,3,4-kl]acridine","218",218,218,"equal",
     "2,7-Dimethoxy-10H,11H,12H-dihydroquino[2,3,4-kl]acridine ( 17b ): Reacting 4b (520 mg, 1.9 mmol) with 1,3-cyclohexanedione (425 mg, 3.8 mmol) by the same procedure described for the synthesis of 17a afforded 17b (625mg, quantitative), amorphous powder (CHCl 3 /MeOH, 20:1), mp 218°C"),
    ("20","3-Nitro-10H-benzo[i]quino[2,3,4-kl]acridin-10-one","339",339,339,"equal",
     "3-Nitro-10H-benzo[i]quino [2,3,4-kl]acridin-10-one ( 20 ): Reaction of 6a (80 mg, 0.24 mmol) in conc.H 2 SO 4 /fuming HNO 3 , 1:1 (5mL), for 12 h. by the above general procedure followed by crystallization of the crude product from pyridine afforded 20 (48 mg, 53%), yellow needles, m.p. 339°C"),
    ("24","10H-quino[2,3,4-kl]acridin-10-one","254",254,254,"equal",
     "afford 24 (290 mg, 92%), amorphous powder (CHCl 3 /MeOH, 20:1), m.p. 254°C"),
    ("25","2,7-Dimethoxy-10H-quino[2,3,4-kl]acridin-10-one","291",291,291,"equal",
     "2,7-Dimethoxy-10H-quino[2,3,4-kl]acridin-10-one ( 25 ): Oxidation of 17b (360 mg, 1.1 mmol) by the same procedure described for the synthesis of 24 afforded 25 (340 mg, 90%), amorphous powder (CHCl 3 /MeOH, 20:1), m.p. 291°C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    rows.append([f"p102_{code}_mp","pending_verification",name,"",
        "melting_point",str(lo),str(lo),str(hi),f"m.p. {raw}°C","equal","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; pyridoacridine"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p102")

import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(3), 194"
URL = "https://doi.org/10.3390/60300194"

# (code, name, mp str, lo, hi, rel, quote)
data = [
    ("3","9-(Acetoxymethylidene)-1,4-dihydro-1,4-methanonaphthalene","78-79",78,79,"range",
     "9-(Acetoxymethylidene)-1,4-dihydro-1,4-methanonaphthalene ( 3 ). Solutions of anthranilic acid (55.4 g, 0.4 mol) and isopentyl nitrite (47.3 g, 0.4 mol) in tetrahydrofuran (200 mL) were added dropwise and simultaneously to a refluxing solution of 6-acetoxyfulvene (55 g, 0.4 mol) in tetrahydrofuran (100 mL) over a period of about 1 h. The solution was refluxed for a further 1 h cooled, made alkaline with aqueous sodium hydroxide (4%, 500 mL), and extracted with petroleum spirit (3 x 500 mL). The dried extracts were freed of solvent and the residue recrystallised from n-hexane to yield the title product as pale yellow crystals (38 g, 45%), m.p. 78-79 °C"),
    ("4_DNPH","9-formyl-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene 2,4-dinitrophenylhydrazone (from syn-aldehyde 4)","177-178",177,178,"range",
     "The syn -aldehyde 4 , was recovered from the least polar band as a colourless oil (0.4 g, 25%). 1 H-NMR (100 MHz): 3.25 (m, 1H, H 11 ), 4.15 (m, 2H, H 1,8 ), 6.88 (t, 2H, H 9,10), 6.90-7.40 (m, 4H, aromatic protons), 9.18 (d, 1H, J = 2.5 Hz, formyl proton); IR (nujol) cm -1 : 1730 cm -1 (carbonyl stretch); MS: m/z 170 (M+, 50%), 169 (17), 142 (16), 141 (100), 115 (41), 63 (12), 21 (45). The other peaks were less than 10%. The 2,4-dinitrophenylhydrazone derivative was recrystallised from ethyl acetate giving bright yellow crystals, m.p. 177-178 °C"),
    ("6_DNB","syn-9-(hydroxymethyl)-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene 3,5-dinitrobenzoate (from syn-alcohol 6)","137-140",137,140,"range",
     "The syn -alcohol 6 was recovered from the least polar band as a colourless liquid (0.25 g, 42%). 1 H-NMR (100 MHz): 2.50 (br s, 1H, OH), 2.84 (t, 1H, J = 8 Hz, H 11 ), 3.08 (d, 2H, J = 8 Hz, OCH 2 ), 3.67 (m, 2H, H 1,8 ), 6.80 (t, 2H, H 9,10 ), 6.9-7.5 (m, 4H, aromatic protons). The 3,5-dinitrobenzoyl derivative was recrystallised again from a mixture of benzene and petroleum spirit (twice) to give pale yellow crystals, m.p. 137-140 °C"),
    ("9","anti-9-(hydroxymethyl)-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene","50-51.5",50,51.5,"range",
     "The anti -alcohol 9 was recrystallised from a mixture of benzene and petroleum spirit as white needles (0.15 g, 25%) m.p. 50-51.5 °C"),
    ("7","syn-9-(tosyloxymethyl)-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene (syn-tosylate)","106-108",106,108,"range",
     "The syn -tosylate 7 , crystallised as large, colourless prisms (0.25g, 33%) m.p. 106-108 °C"),
    ("10","anti-9-(tosyloxymethyl)-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene (anti-tosylate)","105",105,105,"equal",
     "The anti -tosylate 10 , crystallised as colourless needles (0.15 g, 20%) m.p. 105-105 °C"),
    ("4_TsNHNHt","tosylhydrazone of 9-formyl-tricyclo[6.2.1.0(2,7)]undeca-2,4,6,9-tetraene (from syn-aldehyde 4)","134-135",134,135,"range",
     "tosylhydrazone of 9-formyl-tricyclo[6.2.1.0 2,7 ]undeca-2,4,6,9-tetraene ( 4 ). A solution of the syn- aldehyde 4 (0.5 g, 2.90 mmol) and N -tosylhydrazine (0.54 g, 2.9 mmol) in methanol (10 mL) containing two drops of concentrated hydrochloric acid was stirred for 1 h. The solvent was removed and the product dissolved in hot benzene (20 mL). On cooling the excess N -tosylhydrazine was removed by filtration and the filtrate freed of solvent. The residue was recrystallised from ethanol to give the product as colourless needles (0.6 g, 61%) m.p. 134-135 °C"),
    ("12","Tetramethyl 32,34-dioxa-33,35-dihydroxymethyldodecacyclo polyaromatic diol (compound 12)","221-223",221,223,"range",
     "Increasing the polarity to MeOH : EtOAc = 1 : 9 afforded 12 as a colourless solid (156 mg, 64%), m.p. 221-223 °C"),
    ("13","Tetramethyl 32,34-dioxa-33,35-diacetoxymethyldodecacyclo polyaromatic diacetate (compound 13)","245-247",245,247,"range",
     "The crude product was recrystallised from methanol as a colourless solid; yield: 72 mg, (93 %), mp 245-247 °C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    if rel=="range":
        mid=(lo+hi)/2
        rows.append([f"p099_{code}_mp","pending_verification",name,"",
            "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw} °C","range","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}"])
    else:
        rows.append([f"p099_{code}_mp","pending_verification",name,"",
            "melting_point",str(lo),str(lo),str(lo),f"m.p. {raw} °C","equal","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p099")

import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "ACS Omega 2026, 11(15), 23469-23479"
URL = "https://doi.org/10.1021/acsomega.6c01037"

data = [
    ("5","1-(2-(Benzyloxy)-4-methylphenyl)ethan-1-one","55-56",55,56,"range",
     "The raw product was recrystallized from ethanol to afford 6.2 g of white crystals (89%) of 5 , mp 55–56 °C"),
    ("6a","1-(2-(Benzyloxy)-5-bromo-4-methylphenyl)ethan-1-one","72-73",72,73,"range",
     "The raw product was recrystallized from ethanol to afford 6.5 g of white crystals (98%) of 6a , mp 72–73 °C"),
    ("6b","1-(2-(Benzyloxy)-5-chloro-4-methylphenyl)ethan-1-one","76-78",76,78,"range",
     "The raw product was recrystallized from ethanol to afford 1.6 g of white crystals of 6b (84%), mp 76–78 °C"),
    ("7a","1-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-bromoethan-1-one","76-78",76,78,"range",
     "The raw product was recrystallized from ethanol to afford 5.71 g of white crystals of 7a (82%), mp 76–78 °C"),
    ("7b","1-(2-(Benzyloxy)-5-chloro-4-methylphenyl)-2-bromoethan-1-one","80-82",80,82,"range",
     "The raw product was recrystallized from ethanol to afford 1.6 g of white crystals of 7b (89%), mp 80–82 °C"),
    ("8a","2-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-oxoethyl acetate","86-88",86,88,"range",
     "The raw product was recrystallized from ethanol to afford 4 g of slightly yellow crystals of 8a (78%), mp 86–88 °C"),
    ("8b","2-(2-(Benzyloxy)-5-chloro-4-methylphenyl)-2-oxoethyl acetate","90-92",90,92,"range",
     "The raw product was recrystallized from ethanol to afford 0.85 g of slightly yellow crystals of 8b (63%), mp 90–92 °C"),
    ("11","1-(2-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-oxoethyl)pyrrolidine-2,5-dione","88-90",88,90,"range",
     "The residue was recrystallized from ethanol to afford 550 mg of 11 as a slightly orange solid (66%), mp 88–90 °C"),
    ("9a","2-(5-Bromo-2-hydroxy-4-methylphenyl)-2-oxoethyl acetate","86-87",86,87,"range",
     "The residue was purified by CC [silica gel, heptane-EtOAc (9:1)] to afford 1.9 g of 9a as a white crystalline solid (98%), mp 86–87 °C"),
    ("9b","2-(5-Chloro-2-hydroxy-4-methylphenyl)-2-oxoethyl acetate","88-89",88,89,"range",
     "The residue was purified by recrystallization from ethanol to afford 0.520 g of 9b as a white crystalline solid. (86%), mp 88–89 °C"),
    ("12","1-(2-(5-Bromo-2-hydroxy-4-methylphenyl)-2-oxoethyl)pyrrolidine-2,5-dione","87-88",87,88,"range",
     "The residue was purified by recrystallization from ethyl acetate to afford 220 mg of 12 (80%), mp 87–88 °C"),
    ("1","Hofmeisterin I","86-87",86,87,"range",
     "The residue was purified by CC [silica gel, heptane-EtOAc (9:1)] to yield 800 mg of 1 as white crystals (61%), mp 86–87 °C"),
    ("10","2-(2-Acetoxy-4-methylphenyl)-2-oxoethyl acetate","46-48",46,48,"range",
     "The residue was purified by column CC [silica gel, heptane-EtOAc (9:1)] to yield 50 mg of 11 as a white solid (99%), mp 46–48 °C"),  # NB: text says "50 mg of 11" but section is for compound 10 (acetylated derivative) — caution: this is in section "Synthesis of 2-(2-Acetoxy-4-methylphenyl)-2-oxoethyl acetate ( 10 )" so compound number in text may be a typo. Use code 10
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    mid=(lo+hi)/2
    rows.append([f"p113_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"mp {raw} °C","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; hofmeisterin/analogue"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p113")

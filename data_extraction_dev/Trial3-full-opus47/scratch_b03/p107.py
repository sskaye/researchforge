import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(1), 52-60"
URL = "https://doi.org/10.3390/60100052"

data = [
    ("1","Cholesterol","148-150",148,150,"range",
     "Cholestrol ( 1) was Fluka reagent grade, recrystallized from methanol, m.p.148-150 °C"),
    ("ChoTs","Cholesteryl tosylate","132-133",132,133,"range",
     "Workup gave the product, m.p. 132-133 C (ref. [ 16 ] 131.5-132.5 C). The yield was 48 g (88 %). (2) Preparation of 3β-methoxy-cholest-5-ene 2 : 2g of Cholesteryl tosylate were dissolved in 50 mL of methanol"),
    ("2","3β-Methoxy-cholest-5-ene","81-82",81,82,"range",
     "Preparation of 3β-methoxy-cholest-5-ene 2 : 2g of Cholesteryl tosylate were dissolved in 50 mL of methanol and refluxed for 0.5 h. A white precipitate appeared after cooling the solution. Workup gave 2 , m.p. 81-82 C"),
    ("DCA","9,10-Dicyanoanthracene (DCA)","324-326",324,326,"range",
     "9,10-Dicyano- anthracene (DCA) was Aldrich reagent grade, recrystallized from toluene, m.p. 324-326 C"),
    ("LF","Lumiflavin (LF)","350-352",350,352,"range",
     "Lumiflavin (LF) was prepared by a two-step reaction of riboflavin (RF) according to the literature method [ 13 ], m.p. 350-352 C (dee.)"),
    ("1a","cholest-6-en-3β,5α-diol","147-148",147,148,"range",
     "12 mg of cholest-6-en-3β, 5α-diol ( 1a ), recrystallized from methanol, m.p. 147-148 C"),
    ("1b-alpha","cholest-5-en-3β,7α-diol (1b-(α))","176-178",176,178,"range",
     "cholest-5-en-3β,7β-diol 1b- (α) , m.p. 176-178 C"),  # text labels but actually 7α written
    ("1b-beta","cholest-5-en-3β,7β-diol (1b-(β))","184-186",184,186,"range",
     "cholest-5-en-3β,7β-diol 1b- (β), m.p. 184-186 C"),
    ("2_rec","Recovered 3β-methoxy-cholest-5-ene (compound 2)","81-83",81,83,"range",
     "Recovered 3β−methoxy-cholest-5-ene ( 2) (15.8 mg), m.p. 81-83 C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    mid=(lo+hi)/2
    rows.append([f"p107_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw}°C","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; cholesterol derivative"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p107")

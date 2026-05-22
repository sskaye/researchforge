import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2002, 7(8), 681-?"
URL = "https://doi.org/10.3390/70800681"

data = [
    ("2a","3-(2-furanyl)-6-(4-aminophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","229-231",229,231),
    ("2b","3-(2-furanyl)-6-(3-pyridyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","189-191",189,191),
    ("2c","3-(2-furanyl)-6-(1-naphthylmethyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","146-148",146,148),
    ("2d","3-(2-furanyl)-6-(3,5-dinitrophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","290-292",290,292),
    ("2e","3-(2-furanyl)-6-benzyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","111-113",111,113),
    ("2f","3-(2-furanyl)-6-(3-chlorophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","207-209",207,209),
    ("2g","3-(2-furanyl)-6-(2-nitrophenylmethyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","187-189",187,189),
    ("2h","3-2-furanyl-6-(2-chlorophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","169-171",169,171),
    ("2i","3-(2-furanyl)-6-(2-hydroxyphenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","273-275",273,275),
    ("2j","3,6-di(2-furanyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","204-206",204,206),
    ("2k","3-(2-furanyl)-6-phenyloxymethyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","115-117",115,117),
    ("2l","3-(2-furanyl)-6-(2-methoxyphenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","162-164",162,164),
    ("2m","3-(2-furanyl)-6-phenyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","203-205",203,205),
    ("2n","3-(2-furanyl)-6-(2,4-dichlorophenoxymethyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","193-195",193,195),
    ("2o","3-(2-furanyl)-6-(2-quinolyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","267-269",267,269),
    ("2p","3-(2-furanyl)-6-(4-nitrophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","304-306",304,306),
    ("2q","3-(2-furanyl)-6-(2-aminophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","144-146",144,146),
    ("2r","3-(2-furanyl)-6-(4-methoxyphenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole","177-179",177,179),
]
quotes = {
    "2a": "3-(2-furanyl)-6-(4-aminophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2a ): Yield 48 %; M.p. 229-231°C",
    "2b": "3-(2-furanyl)-6-(3-pyridyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2b ): Yield 57 %; Mp. 189-191°C",
    "2c": "3-(2-furanyl)-6-(1-naphthylmethyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2c ): Yield 64 %; Mp. 146-148°C",
    "2d": "3-(2-furanyl)-6-(3,5-dinitrophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2d ): Yield 55 %; Mp. 290-292°C",
    "2e": "3-(2-furanyl)-6-benzyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2e ): Yield 62 %; Mp.111-113°C",
    "2f": "3-(2-furanyl)-6-(3-chlorophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2f ): Yield 66 %; M.p.207-209°C",
    "2g": "3-(2-furanyl)-6-(2-nitrophenylmethyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2g ): Yield 59 %; M.p.187-189°C",
    "2h": "3-2-furanyl-6-(2-chlorophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2h ): Yield 54 %; M.p.169-171°C",
    "2i": "3-(2-furanyl)-6-(2-hydroxyphenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2i ): Yield 49 %; M.p. 273-275°C",
    "2j": "3,6-di(2-furanyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2j ): Yield 55 %; M.p. 204-206°C",
    "2k": "3-(2-furanyl)-6-phenyloxymethyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2k ): Yield 62 %; M.p.115-117°C",
    "2l": "3-(2-furanyl)-6-(2-methoxyphenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2l ): Yield 58 %; M.p. 162-164°C",
    "2m": "3-(2-furanyl)-6-phenyl-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2m ): Yield 53 %; M.p. 203-205°C",
    "2n": "3-(2-furanyl)-6-(2,4-dichlorophenoxymethyl ) -1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2n ): Yield 51 %; M.p.193-195°C",
    "2o": "3-(2-furanyl)-6-(2-quinolyl ) -1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2o ):Yield 48 %; M.p. 267-269°C",
    "2p": "3-(2-furanyl)-6-(4-nitrophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2p ): Yield 59 %; M.p. 304-306°C",
    "2q": "3-(2-furanyl)-6-(2-aminophenyl)-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2q ): Yield 46 %; M.p. 144-146°C",
    "2r": "3-(2-furanyl)-6-(4-methoxyphenyl )-1,2,4-triazolo[3,4-b]-1,3,4-thiadiazole ( 2r ): Yield 61 %; M.p. 177-179°C",
}
rows = []
for code, name, raw, lo, hi in data:
    mid = (lo+hi)/2
    rows.append([f"p090_{code}_mp","pending_verification",name,"",
                 "melting_point",f"{mid:g}",str(lo),str(hi),
                 f"M.p. {raw}°C","range","measured",SOURCE,URL,"Experimental",quotes[code],"",f"compound {code}; triazolothiadiazole"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p090")

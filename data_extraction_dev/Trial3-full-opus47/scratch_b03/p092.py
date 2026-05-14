import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(9), 784-795"
URL = "https://doi.org/10.3390/60900784"

data = [
    # base, hydrochloride pairs
    ("7a","3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one","119-121",119,121,
     "3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one ( 7a ) Base 7a was obtained in 64% yield, m.p. 119-121°C","base"),
    ("7a_HCl","3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one hydrochloride","210-213",210,213,
     "3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one ( 7a ) Base 7a was obtained in 64% yield, m.p. 119-121°C (methanol); 1 H-NMR: δ 1.92-2.17 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.35-2.66 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.10-3.24 (m, 4H, (CH 2 ) 2 NAr), δ 4.12 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.14 (s, 1H, CH =N), δ 6.87-8.38 (m, 9H Ar ); MS: m/z (I%); M 348 (92), 187 (100) 175 (56); Hydrochloride m.p. 210-213°C","HCl salt"),
    ("7b","3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one","102-103",102,103,
     "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one ( 7b ) Base 7b was obtained in 71% yield, m.p. 102-103°C","base"),
    ("7b_HCl","3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one hydrochloride","224-227",224,227,
     "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one ( 7b ) Base 7b was obtained in 71% yield, m.p. 102-103°C (acetone); 1 H-NMR: δ 1.94-2.16 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.34-2.59 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.72-3.91 (m, 4H, (CH 2 ) 2 NAr), δ 4.14 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.16 (s, 1H, CH =N), δ 8.31 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz), δ 7.44-8.38 (m, 4H Ar ); MS: m/z (I%); M 350 (5),187 (100), 177 (30); Hydrochloride m.p. 224-227°C","HCl salt"),
    ("7c","3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one","139-141",139,141,
     "3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one ( 7c ) Base 7c was obtained in 61% yield, m.p. 139-141°C","base"),
    ("7c_HCl","3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one hydrochloride","216-219",216,219,
     "3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one ( 7c ) Base 7c was obtained in 61% yield, m.p. 139-141°C (methanol); 1 H-NMR: δ 1.56-2.03 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.34-2.66 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ) , δ 3.12-3.25 (m, 4H, (CH 2 ) 2 NAr), δ 4.05 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.03 (s, 1H, CH =N), δ 6.81-8.37 (m, 9H Ar ); MS: m/z (I%); M 362 (69), 175 (100); Hydrochloride m.p. 216-219°C","HCl salt"),
    ("7d","3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one","95-97",95,97,
     "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one ( 7d ) Base 7d was obtained in 70% yield, m.p. 95-97°C","base"),
    ("7d_HCl","3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one hydrochloride","192-195",192,195,
     "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one ( 7d ) Base 7d was obtained in 70% yield, m.p. 95-97°C (acetone); 1 H-NMR: δ 1.62-2.01 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.34-2.54 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.74-3.96 (m, 4H, (CH 2 ) 2 NAr), δ 4.05 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.04 (s, 1H, CH =N), δ 8.30 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz), δ 7.50-8.37 (m, 4H Ar ); MS: m/z (I%); M 364 (21), 177 (100); Hydrochloride: m.p. 192-195°C","HCl salt"),
    ("8a","3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione","54-56",54,56,
     "3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8a ) Base 8a was obtained in 69% yield, m.p. 54-56°C","base"),
    ("8a_HCl","3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride","215-218",215,218,
     "3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8a ) Base 8a was obtained in 69% yield, m.p. 54-56°C (methanol); 1 H-NMR: δ 1.99-2.26 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.56-2.75 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.11-3.28 (m, 4H, (CH 2 ) 2 NAr), δ 4.45 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 6.91-8.55 (m, 14H Ar ); MS: m/z (I%); M 440 (10), 279 (6), 175 (100); Hydrochloride m.p. 215-218 °C","HCl salt"),
    ("8b","3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione","128-130",128,130,
     "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8b ) Base 8b was obtained in 63% yield, m.p. 128-130°C","base"),
    ("8b_HCl","3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride","226-229",226,229,
     "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8b ) Base 8b was obtained in 63% yield, m.p. 128-130°C (acetone); 1 H-NMR: δ 1.97-2.27 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.45-2.72 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.78-3.93 (m, 4H, (CH 2 ) 2 NAr), δ 4.44 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.49 (t, 1H, 5H Pyrim , J=4.7 Hz), δ 8.30 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz), δ 7.34-8.55 (m, 9H Ar ); MS: m/z (I%); M 442 (16), 279 (56), 177 (100); Hydrochloride m.p. 226-229°C","HCl salt"),
    ("8c","3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione","111-113",111,113,
     "3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8c ) Base 8c was obtained in 73% yield, m.p. 111-113 °C","base"),
    ("8c_HCl","3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride","179-183",179,183,
     "3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8c ) Base 8c was obtained in 73% yield, m.p. 111-113 °C (ethanol); 1 H-NMR: δ 1.72-2.03 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.41-2.70 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.14-3.29 (m, 4H, (CH 2 ) 2 NAr), δ 4.39 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 6.86-8.47 (m, 14H Ar ); MS: m/z (I%); M 454 (7), 175 (100); Hydrochloride m.p. 179-183°C","HCl salt"),
    ("8d","3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione","154-156",154,156,
     "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8d ) Base 8d was obtained in 58% yield, m.p. 154-156°C","base"),
    ("8d_HCl","3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride","207-209",207,209,
     "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione ( 8d ) Base 8d was obtained in 58% yield, m.p. 154-156°C (methanol); 1 H-NMR: δ 1.72-1.99 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.41-2.65 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.77-3.91 (m, 4H, (CH 2 ) 2 NAr), δ 4.39 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.48 (t, 1H, 5H Pyrim , J=4.7 Hz), δ 8.32 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz), δ 7.34-8.55 (m, 9H Ar ); MS: m/z (I%); M 456 (5), 177 (100); Hydrochloride m.p. 207-209°C","HCl salt"),
    ("9a","2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione","97-99",97,99,
     "2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9a ) Base 9a was obtained in 74% yield, m.p. 97-99°C","base"),
    ("9a_HCl","2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride","219-221",219,221,
     "2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9a ) Base 9a was obtained in 74% yield, m.p. 97-99°C (acetone); 1 H-NMR: δ 1.88-2.09 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.44-2.69 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.12-3.26 (m, 4H, (CH 2 ) 2 NAr), δ 4.25 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 6.85-7.74 (m, 12H Ar ); MS: m/z (I%); M 390 (22), 229 (14), 175 (100); Hydrochloride m.p. 219-221°C","HCl salt"),
    ("9b","2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydroppyridazine-3,6-dione","152-154",152,154,
     "2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydroppyridazine-3,6-dione ( 9b ) Base 9b was obtained in 72% yield, m.p. 152-154°C","base"),
    ("9b_HCl","2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydroppyridazine-3,6-dione hydrochloride","219-221",219,221,
     "2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydroppyridazine-3,6-dione ( 9b ) Base 9b was obtained in 72% yield, m.p. 152-154°C (methanol); 1 H-NMR: δ 1.84-2.06 (m, 2H, CH 2 CH 2 CH 2 ), δ 2.43-2.62 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.75-3.93 (m, 4H, (CH 2 ) 2 NAr), δ 4.25 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.47 (t, 1H, 5H Pyrim , J=4.7 Hz), δ 6.99-7.74 (m, 7H Ar ), 8.30 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz); MS: m/z (I%); M 392 (100), 229 (64), 177 (85); Hydrochloride m.p. 219-221°C","HCl salt"),
    ("9c","2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione","91-93",91,93,
     "2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9c ) Base 9c was obtained in 71% yield, m.p. 91-93°C","base"),
    ("9c_HCl","2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride","199-202",199,202,
     "2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9c ) Base 9c was obtained in 71% yield, m.p. 91-93°C (methanol-H 2 O 4:1); 1 H-NMR: δ 1.62-1.94 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.37-2.66 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.13-3.27 (m, 4H, (CH 2 ) 2 NAr), δ 4.20 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 6.86-7.72 (m, 12H Ar ); MS: m/z (I%); M 404 (9), 175 (100); Hydrochloride m.p.199-202°C","HCl salt"),
    ("9d","2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione","104-106",104,106,
     "2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9d ) Base 9d was obtained in 66% yield, m.p. 104-106 °C","base"),
    ("9d_HCl","2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride","203-205",203,205,
     "2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione ( 9d ) Base 9d was obtained in 66% yield, m.p. 104-106 °C (acetone); 1 H-NMR: δ 1.56-1.81 (m, 4H, CH 2 CH 2 CH 2 CH 2 ), δ 2.44-2.58 (m, 6H, CH 2 N(CH 2 ) 2 and CH 2 N (CH 2 ) 2 ), δ 3.75-3.91 (m, 4H, (CH 2 ) 2 NAr), δ 4.20 (t, 2H, CH 2 NC=O, J=6.6 Hz), δ 8.49 (t, 1H, 5H Pyrim , J=4.7 Hz), δ 6.97-7.74 (m, 7H Ar ), δ 8.30 (d, 2H, 4H Pyrim and 6H Pyrim , J=4.7 Hz); MS: m/z (I%); M 406 (33), 177 (100); Hydrochloride m.p. 203-205 °C","HCl salt"),
]
rows = []
for code, name, raw, lo, hi, q, note in data:
    mid=(lo+hi)/2
    rows.append([f"p092_{code}","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),
        f"m.p. {raw}°C","range","measured",
        SOURCE,URL,"Experimental",q,"",f"compound {code}; {note}; arylpiperazine"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p092")

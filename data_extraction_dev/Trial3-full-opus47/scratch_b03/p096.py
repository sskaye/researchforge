import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2001, 6(10), 803-814"
URL = "https://doi.org/10.3390/61000803"

# (code, name, raw, lo, hi, rel, q)
rows_data = [
    ("6a","16β-hydroxyaspidospermidine","55",55,55,"equal",
     "the less polar fraction contained colouress plates of 16β-hydroxyaspidospermidine ( 6a ) (1.24 g, 72.5%), m.p. 55°C"),
    ("7a","Na-formyl-16β-formyloxyaspidospermidine","70-72",70,72,"range",
     "give the N a -formyl-16β-formyloxyaspidospermidine 7a (130 mg, 90.1 %) as colourless plates, m.p. 70-2 °C"),
    ("1a","Na-formyl-16β-hydroxyaspidospermidine","66-68",66,68,"range",
     "N a - formyl-16β-hydroxyaspidospermidine ( 1a ) (68.5 mg, 98 %) as colouress plates, m.p. 66-68 °C"),
    ("3","16-hydroxy-1,2-dehydrovincadifformine","109-110",109,110,"range",
     "the second fraction contained 16-hydroxy-1,2-dehydrovinca-difformine ( 3 ) (151 mg, 30%) as an orange solid, m.p. 109-110°C"),
    ("4","16-hydroxy-1,2-dehydrovincadifformine Nb-oxide","176-178",176,178,"range",
     "16-hydroxy-1, 2-dehydrovincadifformine N b -oxide ( 4 ) (170 mg, 77.9%), which was recrystalised from dichloromethane-ether to give colourless prisms, m.p. 176-78 °C (dec.)"),
    ("vinca_Nb_oxide","vincadifformine Nb-oxide","160",160,160,"equal",
     "The less polar fraction contained vincadifformine-N b -oxide (36 mg, 18 %), m.p. 160°C (dec.)"),
    ("16oxo","16-oxoaspidospermidine","108-112",108,112,"range",
     "Concentration under reduced pressure gave 16-oxoaspidospermidine (0.75g, 88 %), which was recrystallised from methanol to afford colouress prisms; m.p. 108-112 °C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in rows_data:
    if rel=="range":
        mid=(lo+hi)/2
        rows.append([f"p096_{code}_mp","pending_verification",name,"",
            "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw} °C","range","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; aspidosperma alkaloid"])
    else:
        rows.append([f"p096_{code}_mp","pending_verification",name,"",
            "melting_point",str(lo),str(lo),str(lo),f"m.p. {raw} °C","equal","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; aspidosperma alkaloid"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p096")

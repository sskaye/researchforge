import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2002, 7(10), 756-766"
URL = "https://doi.org/10.3390/71000756"

data = [
    ("2","pyridothienopyridine (from ethyl cyanoacetate)","200",200,200,"equal",
     "Compound 2 (from ethyl cyanoacetate) was recrystallized from ethanol as yellow needles; m. p. 200 o C"),
    ("3","pyridothienopyridine-2,7-dione (from diethyl malonate)","320",320,320,"greater_than",
     "Compound 3 (from diethyl malonate) was recrystallized from ethanol as orange crystals; m. p. > 320 o C"),
    ("4","4-Amino-6-phenylaminothieno[3,2-d]pyrimidin-7-carbonitrile","271",271,271,"greater_than",
     "4-Amino-6- phenylaminothieno[3,2-d]pyrimidin-7-carbonitrile ( 4 ). A solution of 1 (0.001 mol) in formamide (10 mL) was refluxed for 2h. The precipitate that formed on cooling was filtered off and recrystallized from ethanol to give white powder; m.p. >271 o C"),
    ("5","6-Phenylamino-4-benzalaminothieno[3,2-d]pyrimidin-7-carbonitrile","243",243,243,"equal",
     "6-Phenylamino-4- benzalaminothieno[3,2-d]pyrimidin-7-carbonitrile ( 5 ). An equimolar mixture of 4 (0.01 mol) and benzaldehyde (0.01 mol) was dissolved in EtOH (30 mL) in the presence of a few drops of piperidine. The reaction mixture was refluxed for 2h and left to cool. The solid product was filtered off and recrystallized from pyridine as white crystals; m.p. 243 o C"),
    ("6","9-Amino-7-oxo-6-phenyl-4-phenylmethanimido-6,7-dihydropyrido[3',2':4,5]thieno[3,2-d]-pyrimidin-8-carbonitrile","220",220,220,"equal",
     "9-Amino-7-oxo-6-phenyl-4-phenylmethanimido-6,7- dihydropyrido[3',2':4,5]thieno[3,2-d]-pyrimidin-8-carbonitrile ( 6 ). Recrystallized from pyridine as white crystals; m.p. 220 o C"),
    ("10","7-Amino-9-oxo-10-phenyl-9,10-dihydropyrido[3',2':4,5]thieno[3,2-d][1,2,4]triazolo-[3,2-f]-pyrimidin-8-carbonitrile","236",236,236,"equal",
     "7-Amino-9-oxo-10-phenyl-9,10- dihydropyrido[3',2':4,5]thieno[3,2-d][1,2,4]triazolo-[3,2-f]-pyrimidin-8-carbonitrile ( 10 ). Recrystallized from acetonitrile as yellow crystals; m.p. 236 o C"),
    ("12","9-Amino-4-chloro-7-oxo-6-phenyl-6,7-dihydropyrido-[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbonitrile","158-160",158,160,"range",
     "9-Amino-4-chloro-7-oxo-6-phenyl-6,7-dihydropyrido -[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbo-nitrile ( 12 ). Recrystallized from acetonitrile as yellow crystals; m.p. 158-160 o C"),
    ("7","Ethyl N-(2,4-dicyano-5-phenylamino-3-yl)metanimidate","215",215,215,"equal",
     "Ethyl N-(2,4-dicyano-5-phenylamino-3-yl)metanimidate ( 7 ). A mixture of 1 (0.005 mol), triethyl orthoformate (3 mL) and acetic anhydride (20 mL) was heated under reflux for 5h. After cooling the precipitated solid was filtered off and recrystallized from ethanol as white crystals; m.p. 215 o C"),
    ("8","3-Amino-3,4-dihydro-4-imino-6-phenylaminothieno[3,2-d]pyrimidin-7-carbonitrile","185",185,185,"equal",
     "3-Amino-3,4-dihydro-4-imino-6- phenylaminoyhieno[3,2-d]pyrimidin-7-carbonitrile ( 8 ). Hydrazine hydrate (80%) (4 mL) was added to a suspension of 7 (0.005 mol) in dioxane (40 mL). The reaction mixture was stirred at room temperature for 1h. The precipitate which formed was filtered off, washed with water, dried in air and recrystallized from dioxane as white crystals; m.p. 185 o C"),
    ("9","8-Phenylaminothieno[3,2-d][1,2,4]triazolo[3,2-f]pyrimidin-7-carbonitrile","299",299,299,"equal",
     "8-Phenylaminothieno [3,2-d][1,2,4]triazolo[3,2-f]pyrimidin-7-carbonitrile ( 9 ). Compound 8 (0.001 mol) in an excess of triethyl orthoformate (7 mL) was refluxed for 1h. After cooling, the precipitated product was collected by filtration and recrystallized from ethanol-chloroform mixture as white needles; m.p. 299 o C"),
    ("11","4-Chloro-6-phenylamino-thieno[3,2-d]-1,2,3-triazin-7-carbonitrile","201",201,201,"equal",
     "4-Chloro-6-phenylamino- thieno[3,2-d]-1,2,3-triazin-7-carbonitrile ( 11 ). A solution of (0.01 mol) sodium nitrite in 10 mL of water was added to a cold solution of 1 (0.005 mol) in acetic acid (30 mL) and concentrated hydrochloric acid (15 mL). After completion of the addition, the ice bath was removed and stirring continued for an additional 2h. The crude product obtained was recrystallized from ethanol as white needles; m.p. 201 o C"),
    ("13","9-Amino-4-hydrazino-7-oxo-6-phenyl-6,7-dihydropyrido-[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbonitrile","262",262,262,"equal",
     "9-Amino-4-hydrazino-7-oxo-6-phenyl-6,7- dihydropyrido-[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbonitrile ( 13 ). A mixture of 12 (0.002 mol) and hydrazine hydrate (3 mL) in ethanol (20 mL) was refluxed for 1h. The precipitate that separated after cooling was recrystallized from dioxane as white crystals; m.p. 262 o C"),
    ("14","3-Amino-2,4-di(4,5-dihydro-1H-2-imidazolyl)-5-phenylaminothiophene","197",197,197,"equal",
     "3-Amino-2,4-di(4,5-dihydro-1H-2-imidazolyl)-5-phenylaminothiophene ( 14 ). To a suspension of 1 (0.002 mol), ethylenediamine (3 mL) and carbon disulfide (1 mL) were added dropwise. The reaction mixture was heated on a water bath for 2h. The precipitated solid was triturated with ethanol (10 mL), filtered off and recrystallized from ethanol to give golden yellow crystals; m.p. 197 o C"),
    ("15","5,6,12-Triphenyl-2,3,5,6,9,10-hexahydroimidazo[1,2-c]imidazo-[2'',1'':6',1']pyrimido[4',5':4,5]-thieno-[3,2-e]pyrimidine","215",215,215,"equal",
     "5,6,12-Triphenyl-2,3,5,6,9,10- hexahydroimidazo[1,2-c]imidazo-[2\",1\":6',1']pyrimido[4',5':4,5]-thieno-[3,2-e]pyrimidine ( 15 ). A mixture of 14 (0.005 mol), benzaldehyde (0.01 mol) and acetic acid (15 mL) was heated under reflux for 5 h. The precipitated solid was collected and recrystallized from dioxane in the form of white needles; m.p. 215 o C"),
    ("16","5-Ethoxy-6-phenyl-2,3,5,6,9,10-hexahydroimidazo[1,2-c]imidazo[2'',1'':6',1']pyrimido[4',5':4,5]-thieno[3,2-e]pyrimidine","163",163,163,"equal",
     "5-Ethoxy-6-phenyl-2,3,5,6,-9,10- hexahydroimidazo[1,2-c]imidazo[2\",1\":6',1']pyrimido[4',5':4,5]-thieno[3,2-e]pyrimidine ( 16 ). Compound 14 (0.001 mol) in triethyl orthoformate (14 mL) was heated under reflux for 3 h. The precipitated solid was collected and recrystallized from pyridine as pale yellow crystals; m.p. 163 o C"),
    ("17a","Compound 17a (dimethylthiomethylenemalononitrile-derived pyrimidodione)","172",172,172,"equal",
     "The separated solids were collected and recrystallized from the appropriate solvent. Compound 17a : gray crystals; m.p. 172 o C (from dioxane)"),
    ("17b","Compound 17b (2-acetyl-1,1-dimethylthiobuten-3-one-derived pyrimidodione)","179",179,179,"equal",
     "Compound 17b : orange crystals; m.p.179 o C (from methanol)"),
    ("18","7-(4,5-Dihydro-1H-2-imidazolyl)-2,3-dihydro-8-phenylaminoimidazo[1,2-c]thieno[2,3-e][1,2,3]-triazine","269",269,269,"equal",
     "7-(4,5-Dihydro-1H-2-imidazolyl)-2,3-dihydro-8- phenylaminoimidazo[1,2-c]thieno[2,3-e][1,2,3]-triazine ( 18 ). To a solution ... The forming precipitate was filtered off and recrystallized from ethanol as white needles; m.p. 269 o C"),
]
rows=[]
for code, name, raw, lo, hi, rel, q in data:
    if rel=="range":
        mid=(lo+hi)/2
        rows.append([f"p103_{code}_mp","pending_verification",name,"",
            "melting_point",f"{mid:g}",str(lo),str(hi),f"m.p. {raw} o C","range","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; thieno"])
    elif rel=="greater_than":
        rows.append([f"p103_{code}_mp","pending_verification",name,"",
            "melting_point",str(lo),"","",f"m.p. >{raw} o C","greater_than","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; >mp"])
    else:
        rows.append([f"p103_{code}_mp","pending_verification",name,"",
            "melting_point",str(lo),str(lo),str(lo),f"m.p. {raw} o C","equal","measured",
            SOURCE,URL,"Experimental",q,"",f"compound {code}; thieno"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p103")

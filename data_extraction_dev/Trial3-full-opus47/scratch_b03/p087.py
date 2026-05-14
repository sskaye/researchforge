import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(12), 910-923"
URL = "https://doi.org/10.3390/81200910"

# (code, name, mp_int, quote)
data = [
    ("1c","3-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxopropanal",189,
     "3-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxopropanal ( 1c ): Yellow crystals from ethanol; m.p.189°C"),
    ("3a","2-{2-[(2-Cyanophenyl)-hydrazono]-3-furan-2-yl-3-oxo-propylideneamino}-4,5,6,7-tetrahydrobenzo-[b]thiophene-3-carboxylic acid ethyl ester",174,
     "thiophene-3-carboxylic acid ethyl ester ( 3a ). Dark red crystals from ethanol; m.p. 174°C"),
    ("3b","2-{2-[(2-Methoxycarbonyl-phenyl)-hydrazono]-3-oxo-butylideneamino}-4,5,6,7-tetrahydrobenzo[b]-thiophene-3-carboxylic acid ethyl ester",181,
     "thiophene-3-carboxylic acid ethyl ester ( 3b ): Dark orange crystals from ethanol; m.p. 181°C"),
    ("3c","2-{3-(4-Chlorophenyl)-2-[(2-cyanophenyl)-hydrazono]-3-oxo-propylideneamino}-4,5,6,7-tetrahydro-benzo[b]thiophene-3-carboxylic acid ethyl ester",189,
     "tetrahydro-benzo[b]thiophene-3-carboxylic acid ethyl ester ( 3c ): Orange crystals from ethanol/dioxane (2:1); m.p. 189°C"),
    ("3d","2(N'-{2-Furan-2-yl)-2-oxo-1-[(4H-[1,2,4]triazol-3-ylimino)-methyl]-ethylidene}-hydrazino)benzoic acid methyl ester",260,
     "ethylidene}-hydrazino)benzoic acid methyl ester ( 3d ): Brown crystals from ethanol/dioxane; m.p. 260°C"),
    ("3e","2(N'-{2-(4-Chlorophenyl)-2-oxo-1-[(4H-[1,2,4]triazol-3-ylimino)-methyl]-ethylidene}-hydrazino)-benozonitrile",240,
     "ethylidene}-hydrazino)-benozonitrile (3e ): Light orange crystals from dioxane; m.p. 240°C"),
    ("3f","2-{N'-[2-Furan-2-yl-2-oxo-1-(pyrazin-2-yliminomethyl)-ethylidene]-hydrazino}-benzoic acid methyl ester",210,
     "ethylidene]-hydrazino}-benzoic acid methyl ester ( 3f ): Light brown crystals from ethanol/dioxane (2:1); m.p. 210°C"),
    ("3g","2-{N'-[2-(4-Chlorophenyl)-2-oxo-1-(pyrazin-2-yliminomethyl)-ethylidene]-hydrazino}-benzonitrile",255,
     "ethylidene]-hydrazino}-benzonitrile ( 3g ): Orange crystals from ethanol/dioxane (2:1); m.p. 255°C"),
    ("6","7-(4-Chlorophenyl)-6-(2-cyanophenylazo)-1,2,4-triazolo[1,5-a]pyrimidine",258,
     "7-(4-Chlorophenyl)-6-(2-cyanophenylazo)-1,2,4-triazolo[1,5-a]pyrimidine ( 6 ): Orange crystals from ethanol; m.p. 258°C"),
    ("8a","1-(2-Furyl)-3-hydrazono-2-(2-methoxycarbonylphenylhydrazono)-1-propanone",168,
     "1-(2-Furyl)-3-hydrazono-2-(2-methoxycarbonylphenylhydrazono)-1-propanone ( 8a ): Brown crystals from ethanol; m.p. 168°C"),
    ("8b","1-(4-Chlorophenyl)-3-hydrazono-2-(2-methoxycarbonylphenylhydrazono)-1-propanone",204,
     "1-(4-Chlorophenyl)-3-hydrazono-2-(2-methoxycarbonylphenylhydrazono)-1-propanone ( 8b ): Yellow crystals from ethanol: m.p. 204°C"),
    ("8c","1-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-phenylhydrazono-1-propanone",244,
     "1-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-phenylhydrazono-1-propanone ( 8c ): Orange crystals from ethanol/dioxane(2:1): m.p. 244°C"),
    ("8d","2-(2-Cyanophenylhydrazono)-1-(2-furyl)-3-phenylhydrazono-1-propanone",229,
     "2-(2-Cyanophenylhydrazono)-1-(2-furyl)-3-phenylhydrazono-1-propanone ( 8d ): Orange crystals from ethanol: m.p. 229°C"),
    ("9a","3-(2-Furyl) 4-(2-methoxycarbonylphenylazo)-pyrazole",160,
     "3-(2-Furyl) 4-(2-methoxycarbonylphenylazo)-pyrazole ( 9a ): Red crystals from ethanol; m.p. 160°C"),
    ("9b","3-(4-Chlorophenyl) 4-(2-methoxycarbonylphenylazo) pyrazole",189,
     "3-(4-Chlorophenyl) 4-(2-methoxycarbonylphenylazo) pyrazole ( 9b ): Orange crystals from ethanol: m.p. 189°C"),
    ("9c","3-(4-Chlorophenyl)-4-(2-methoxycarbonylphenylazo)-1-phenylpyrazole",242,
     "3-(4-Chlorophenyl)-4-(2-methoxycarbonylphenylazo)-1-phenylpyrazole ( 9c ): Light brown crystals from methanol: m.p. 242°C"),
    ("9d","4-(2-Cyanophenylazo)-3-(2-furyl)-1-phenylpyrazole",137,
     "4-(2-Cyanophenylazo)-3-(2-furyl)-1-phenylpyrazole ( 9d ): Orange crystals from ethanol; m.p. 137°C"),
    ("14","5-Amino-3-(4-chlorobenzoyl)-6-cyano-(2-cyanophenyl)-1,7-dihydro-7-iminopyrido[2,3-c]pyridazine",273,
     "iminopyrido [2,3-c] pyridazine ( 14 ): Green crystals from ethanol; m.p. 273°C"),
    ("15","2-{N-[2-(4-Chlorophenyl)-1-cyano-2-oxo-ethylidene]-hydrazino}-benzoic acid",238,
     "2-{N-[2-(4-Chlorophenyl)-1-cyano-2-oxo-ethylidene]-hydrazino}-benzoic acid ( 15 ): Green crystals from ethanol/ dioxane (2:1); m.p.238°C"),
    ("16a","3-(2-Furoyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxo-propanal-1-oxime",199,
     "3-(2-Furoyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxo-propanal-1-oxime ( 16a ): Yellow crystal from ethanol; m.p.199°C"),
    ("16b","3-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxo-propanal-1-oxime",186,
     "3-(4-Chlorophenyl)-2-(2-methoxycarbonylphenylhydrazono)-3-oxo-propanal-1-oxime ( 16b ): Yellow crystals from dioxane; m.p.186°C"),
    ("17a","4-(2-Furoyl)-2-(2-methoxycarbonylphenyl)-1,2,3-triazole",138,
     "4-(2-Furoyl)-2-(2-methoxycarbonylphenyl)-1,2,3-triazole ( 17a ): Yellow crystals from ethanol; m.p.138°C"),
    ("18","3-(4-Chlorophenyl)-3-oxo-2-(2-methoxycarbonylphenylhydrazono)propionitrile",175,
     "3-(4-Chlorophenyl)-3-oxo-2-(2-methoxycarbonylphenylhydrazono)propionitrile ( 18 ): Compound 1c (0.1 mol), hydroxylamine hydrochloride (0.1mol) and ammonium acetate (0.1 mol) and a few drops of ethanol were placed in the microwave oven and irradiated at 390 W for 30 min, then left to cool to room temperature, and the solid was collected and crystallized from ethanol, giving brown crystals; m.p.175°C"),
]
# Compound 13: m.p. >300°C — relation 'greater_than'
extra = [
    ("13","3-Amino-1-cyano-2-(2-furoyl-6-oxopyridazino[2,3-c]quinqzoline-4-yl) acrylonitrile",300,
     "acrylonitrile ( 13 ): Brown crystals from methanol; m.p. >300°C"),
]

rows = []
for code, name, mp, q in data:
    rows.append([f"p087_{code}_mp","pending_verification",name,"",
                 "melting_point",str(mp),str(mp),str(mp),f"m.p. {mp}°C","equal","measured",
                 SOURCE,URL,"Experimental",q,"",f"compound {code}; hydrazonopropanal derivative"])
for code, name, mp, q in extra:
    rows.append([f"p087_{code}_mp","pending_verification",name,"",
                 "melting_point",str(mp),"","",f"m.p. >300°C","greater_than","measured",
                 SOURCE,URL,"Experimental",q,"",f"compound {code}; >300°C"])

with open(csv_path, "a", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p087")

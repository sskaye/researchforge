#!/usr/bin/env python3
"""Build batch_pdfs.csv for the 20 standalone PDF papers."""
import csv

OUT = "/sessions/determined-confident-bell/mnt/data_extraction_dev/Trial2-full-sonnet46/batch_pdfs.csv"

rows = []
id_counter = [1]

def add(compound_name, compound_smiles, prop, value_celsius, value_raw, relation,
        data_type, source, source_url, evidence_location, evidence_quote,
        conversion_arithmetic="", notes="",
        value_celsius_min="", value_celsius_max=""):
    rows.append({
        "id": id_counter[0],
        "verification_status": "pending_verification",
        "compound_name": compound_name,
        "compound_smiles": compound_smiles,
        "property": prop,
        "value_celsius": value_celsius,
        "value_celsius_min": value_celsius_min,
        "value_celsius_max": value_celsius_max,
        "value_raw": value_raw,
        "relation": relation,
        "data_type": data_type,
        "source": source,
        "source_url": source_url,
        "evidence_location": evidence_location,
        "evidence_quote": evidence_quote,
        "conversion_arithmetic": conversion_arithmetic,
        "notes": notes,
    })
    id_counter[0] += 1

# ============================================================
# 1952 Livingston  J. Am. Chem. Soc. 1952, 74, 5781
# ============================================================
S52 = "J. Am. Chem. Soc. 1952, 74, 5781"
U52 = "https://doi.org/10.1021/ja01140a503"

add("octafluorocyclobutane","","boiling_point",-6.05,"-6.1 to -6.0 deg C","=",
    "measured",S52,U52,"p. 5781, experimental section",
    "octafluorocyclobutane (b.p. -6.1 to -6.0)",
    "","range midpoint","-6.1","-6.0")
add("methylcyclobutane","","melting_point",-161.51,"-161.51 deg C","=",
    "measured",S52,U52,"p. 5781, experimental section",
    "f.p. -161.51",
    "","fp = freezing point; recorded as melting_point")
add("methylcyclobutane","","boiling_point",36.98,"36.98 deg C (755 mm.)","=",
    "measured",S52,U52,"p. 5781, experimental section",
    "bp. 36.98 (755 mm.) and 37.13 (760 mm.)",
    "","at 755 mmHg; OCR reads '3F.98' corrected to 36.98 per context")
add("methylcyclobutane","","boiling_point",37.13,"37.13 deg C (760 mm.)","=",
    "measured",S52,U52,"p. 5781, experimental section",
    "bp. 36.98 (755 mm.) and 37.13 (760 mm.)",
    "","at 760 mmHg")

# ============================================================
# 1990 Yalkowsky  Pharm. Res. 7(9):942
# ============================================================
S90 = "Pharm. Res. 1990, 7(9), 942"
U90 = "https://doi.org/10.1023/A:1015801203702"

# Table I -- deg C (14 compounds)
t1 = [
    ("1,2-dichlorobenzene",-17,179),("1,3-dichlorobenzene",-25,172),("1,4-dichlorobenzene",53,175),
    ("1,2-dibromobenzene",7,225),("1,3-dibromobenzene",-7,220),("1,4-dibromobenzene",87,220),
    ("1,2-diiodobenzene",27,286),("1,3-diiodobenzene",40,285),("1,4-diiodobenzene",132,285),
    ("1,2,3-trichlorobenzene",53,218),("1,2,4-trichlorobenzene",17,213),("1,3,5-trichlorobenzene",63,208),
    ("methylpropylketone",-78,102),("diethylketone",-40,101.7),
]
for i,(nm,mp,bp) in enumerate(t1):
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S90,U90,
        f"Table I row {i+1}",f"Table I. {nm} MP {mp} BP {bp}",
        "","CRC Handbook values; deg C")
    add(nm,"","boiling_point",bp,f"{bp} deg C","=","measured",S90,U90,
        f"Table I row {i+1}",f"Table I. {nm} MP {mp} BP {bp}",
        "","CRC Handbook values; deg C")

# Table III -- K (85 non-H-bonding substituted benzenes from CRC Handbook)
t3 = [
    ("benzene",353,279),("toluene",383,178),("1,3-dimethylbenzene",412,226),
    ("1,2-dimethylbenzene",417,248),("1,4-dimethylbenzene",411,286),
    ("1,3,5-trimethylbenzene",438,220),("1,2,4-trimethylbenzene",442,229),
    ("1,2,3-trimethylbenzene",449,248),("1,2,3,5-tetramethylbenzene",471,249),
    ("1,2,3,4-tetramethylbenzene",478,267),("1,2,4,5-tetramethylbenzene",470,352),
    ("pentamethylbenzene",503,327),("hexamethylbenzene",537,438),
    ("nitrobenzene",483,279),("2-nitrotoluene",495,262),("3-nitrotoluene",505,288),
    ("4-nitrotoluene",511,324),("iodobenzene",461,242),("3-iodotoluene",486,246),
    ("4-iodotoluene",484,309),("1,2-diiodobenzene",559,300),("1,3-diiodobenzene",558,313),
    ("1,4-diiodobenzene",558,405),("bromobenzene",429,242),("3-bromotoluene",457,233),
    ("2-bromotoluene",455,245),("4-bromotoluene",458,302),("3-bromoiodobenzene",525,264),
    ("4-bromoiodobenzene",524,365),("1,3-dibromobenzene",493,266),("1,2-dibromobenzene",498,280),
    ("1,4-dibromobenzene",493,360),("1,3,5-tribromobenzene",544,395),
    ("1,2-dimethyl-4,5-tetrabromobenzene",647,535),("chlorobenzene",405,223),
    ("3-chlorotoluene",435,225),("2-chlorotoluene",431,238),("4-chlorotoluene",435,281),
    ("2-chloronitrobenzene",518,307),("3-chloronitrobenzene",509,319),("4-chloronitrobenzene",515,357),
    ("4-chloroiodobenzene",500,330),("3-chlorobromobenzene",469,251),("2-chlorobromobenzene",477,261),
    ("4-chlorobromobenzene",469,341),("1,3-dichlorobenzene",445,248),("1,2-dichlorobenzene",452,256),
    ("1,4-dichlorobenzene",448,326),("3,5-dichlorotoluene",474,299),
    ("3,4-dichloro-1,2-dimethylbenzene",507,349),("2,4-dichloromesitylene",516,332),
    ("1,2,4-trichlorobenzene",486,290),("1,2,3-trichlorobenzene",491,326),
    ("1,3,5-trichlorobenzene",481,336),("2,3,4-trichlorotoluene",505,317),
    ("2,3,5-trichlorotoluene",504,319),("1,2,3,4-tetrachlorobenzene",527,320),
    ("1,2,4,5-tetrachlorobenzene",517,413),("pentachlorobenzene",549,359),
    ("hexachlorobenzene",599,503),("fluorobenzene",358,232),("3-fluorotoluene",389,185),
    ("2-fluorotoluene",387,211),("4-fluorotoluene",390,216),("4-fluoroiodobenzene",456,246),
    ("4-fluorobromobenzene",425,256),("2-chlorofluorobenzene",411,230),("4-chlorofluorobenzene",403,246),
    ("1,3-difluorobenzene",356,214),("1,2-difluorobenzene",364,239),("1,4-difluorobenzene",368,260),
    ("1,2,3,5-tetrachlorobenzene",519,327),("hexafluorobenzene",354,278),
    ("1,2,4,5-tetrafluorobenzene",362,277),("1-fluoro-2,4,6-trimethylbenzene",442,236),
    ("benzonitrile",464,260),("2-bromobenzonitrile",524,329),("3-bromobenzonitrile",498,312),
    ("4-bromobenzonitrile",508,387),("2-chlorobenzonitrile",505,316),("4-chlorobenzonitrile",496,367),
    ("4-fluorobenzonitrile",462,308),("2-methylbenzonitrile",478,260),("3-methylbenzonitrile",486,250),
    ("4-methylbenzonitrile",491,303),
]
for i,(nm,bp_k,mp_k) in enumerate(t3):
    mp_c = round(mp_k-273.15,2)
    bp_c = round(bp_k-273.15,2)
    loc = f"Table III row {i+1}"
    add(nm,"","melting_point",mp_c,f"{mp_k} K","=","measured",S90,U90,loc,
        f"Table III: {nm} BP {bp_k} MP {mp_k}",
        f"{mp_k} K - 273.15 = {mp_c} deg C","CRC Handbook via Yalkowsky 1990 Table III")
    add(nm,"","boiling_point",bp_c,f"{bp_k} K","=","measured",S90,U90,loc,
        f"Table III: {nm} BP {bp_k} MP {mp_k}",
        f"{bp_k} K - 273.15 = {bp_c} deg C","CRC Handbook via Yalkowsky 1990 Table III")

# ============================================================
# 2000 Brown  J. Chem. Ed. 2000, 77(6), 724
# ============================================================
S00 = "J. Chem. Ed. 2000, 77(6), 724"
U00 = "https://doi.org/10.1021/ed077p724"

brown_t1 = [
    ("pentane",143.5),("methylbutane",113.3),("2,2-dimethylpropane",256.6),
    ("octane",216.4),("3-methylheptane",152.7),("hexamethylethane",373.9),
    ("methylcyclopentane",130.7),("2,3-dimethyl-2-butene",198.6),("cyclohexane",279.8),
    ("methylcyclohexane",146.6),("1-heptene",153.5),("cycloheptane",265.2),
    ("1,1-dichloroethane",176.2),("1,2-dichloroethane",237.7),
    ("1-propanol",147.1),("2-propanol",183.7),
    ("1-butanol",183.3),("2-methyl-1-propanol",165.0),("2-methyl-2-propanol",298.5),
    ("1,2-dichlorobenzene",256.5),("1,3-dichlorobenzene",248.4),("1,4-dichlorobenzene",325.9),
    ("1,2-dimethylbenzene",248.0),("1,3-dimethylbenzene",225.4),("1,4-dimethylbenzene",286.4),
    ("ethylcyclohexane",161.9),("1,1-dimethylcyclohexane",239.9),("cyclooctane",288.0),
    ("cyclooctatetraene",268.5),("cubane",405.0),
    ("phenanthrene",372.4),("anthracene",488.0),
]
for nm,mp_k in brown_t1:
    mp_c = round(mp_k-273.15,2)
    add(nm,"","melting_point",mp_c,f"{mp_k} K","=","measured",S00,U00,
        "Table 1",f"Table 1: {nm} mp/K {mp_k}",
        f"{mp_k} K - 273.15 = {mp_c} deg C","compiled reference values")

brown_t2 = [
    ("benzene",278.7),("toluene",178.2),("fluorobenzene",231.0),("chlorobenzene",228.0),
    ("bromobenzene",242.6),("iodobenzene",241.9),("phenol",314.1),
    ("hexafluorobenzene",278.5),("pentafluorobenzene",225.9),
    ("pyridine",231.6),("1,4-diazine",328.2),("1,3,5-triazine",358.2),
]
for nm,mp_k in brown_t2:
    mp_c = round(mp_k-273.15,2)
    add(nm,"","melting_point",mp_c,f"{mp_k} K","=","measured",S00,U00,
        "Table 2",f"Table 2: {nm} mp/K {mp_k}",
        f"{mp_k} K - 273.15 = {mp_c} deg C","compiled reference values")

brown_t3 = [
    ("adamantane",543.0),("hexamethylenetetramine",523.0),("cubane",405.0),("camphor",452.0),
]
for nm,mp_k in brown_t3:
    mp_c = round(mp_k-273.15,2)
    rel = ">" if nm=="hexamethylenetetramine" else "="
    raw = f">{mp_k} K" if nm=="hexamethylenetetramine" else f"{mp_k} K"
    add(nm,"","melting_point",mp_c,raw,rel,"measured",S00,U00,
        "Table 3",f"Table 3: {nm} mp/K {mp_k}",
        f"{mp_k} K - 273.15 = {mp_c} deg C","compiled reference values")

# ============================================================
# 2005 Jain dissertation  U. Arizona 2005
# ============================================================
S05 = "Estimation of Melting Points of Organic Compounds, Jain, U. Arizona, 2005"
U05 = "http://hdl.handle.net/10150/193516"

# Table 1.1 -- alkane, alkanol, alkanoic acid series (C1-C14)
alkane_names = ["methane","ethane","propane","butane","pentane","hexane","heptane","octane",
                "nonane","decane","undecane","dodecane","tridecane","tetradecane"]
alkane_mp =   [-183,-184,-188,-138,-130,-95,-90,-57,-53,-30,-9,6,18,28]
alkanol_names= ["methanol","ethanol","1-propanol","1-butanol","1-pentanol","1-hexanol",
                "1-heptanol","1-octanol","1-nonanol","1-decanol","1-undecanol",
                "1-dodecanol","1-tridecanol","1-tetradecanol"]
alkanol_mp =  [-98,-114,-124,-88,-77,-47,-33,-15,-8,6,25,40,50,61]
alkanoic_names=["methanoic acid","acetic acid","propanoic acid","butanoic acid","pentanoic acid",
                "hexanoic acid","heptanoic acid","octanoic acid","nonanoic acid","decanoic acid",
                "undecanoic acid","dodecanoic acid","tridecanoic acid","tetradecanoic acid"]
alkanoic_mp = [8,26,-20,-8,-34,-3,-7,17,12,31,29,54,62,69]
for i in range(14):
    add(alkane_names[i],"","melting_point",alkane_mp[i],f"{alkane_mp[i]} deg C","=","measured",S05,U05,
        "Table 1.1",f"Table 1.1 Alkyl Chain length {i+1} Alkanes {alkane_mp[i]}",
        "","CRC Handbook via Jain 2005")
    add(alkanol_names[i],"","melting_point",alkanol_mp[i],f"{alkanol_mp[i]} deg C","=","measured",S05,U05,
        "Table 1.1",f"Table 1.1 Alkyl Chain length {i+1} Alkanols {alkanol_mp[i]}",
        "","CRC Handbook via Jain 2005")
    add(alkanoic_names[i],"","melting_point",alkanoic_mp[i],f"{alkanoic_mp[i]} deg C","=","measured",S05,U05,
        "Table 1.1",f"Table 1.1 Alkyl Chain length {i+1} Alkanoic Acids {alkanoic_mp[i]}",
        "","CRC Handbook via Jain 2005")

# Table 1.2 -- octane isomers
jain_t12 = [
    ("n-octane",-56),("2-methylheptane",-109),("3-methylheptane",-120),("4-methylheptane",-121),
    ("2,2-dimethylhexane",-121),("2,5-dimethylhexane",-91),("3,3-dimethylhexane",-126),
    ("2,2,3-trimethylpentane",-113),("2,2,4-trimethylpentane",-107),
    ("2,3,3-trimethylpentane",-109),("2,3,4-trimethylpentane",-109),
    ("2,2,3,3-tetramethylbutane",101),
]
for nm,mp in jain_t12:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S05,U05,
        "Table 1.2",f"Table 1.2 {nm} Melting Point (deg C) {mp}",
        "","CRC Handbook via Jain 2005")

# Table 1.3 -- isomeric arenes
jain_t13 = [
    ("o-xylene",-25),("m-xylene",-48),("p-xylene",13),("hexylbenzene",-62),
    ("p-diisopropylbenzene",-17),("s-triethylbenzene",-66),("hexamethylbenzene",166),
    ("anthracene",216),("phenanthrene",101),("1,2-benzanthracene",162),
    ("2,3-benzanthracene",335),("3,4-benzphenanthrene",168),
    ("2,3-benzphenanthrene",254),("9,10-benzphenanthrene",199),
]
for nm,mp in jain_t13:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S05,U05,
        "Table 1.3",f"Table 1.3 {nm} Melting Point (deg C) {mp}",
        "","CRC Handbook via Jain 2005")

# Table 1.4 -- disubstituted benzenes
jain_t14 = [
    ("1,2-dimethylbenzene",-25),("1,3-dimethylbenzene",-47),("1,4-dimethylbenzene",13),
    ("1,2-dichlorobenzene",-17),("1,3-dichlorobenzene",-24),("1,4-dichlorobenzene",53),
    ("1,2-dibromobenzene",-30),("1,3-dibromobenzene",84),("1,4-dibromobenzene",106),
    ("1,2-diiodobenzene",-31),("1,3-diiodobenzene",40),("1,4-diiodobenzene",131),
    ("1,2-dinitrobenzene",118),("1,3-dinitrobenzene",90),("1,4-dinitrobenzene",174),
    ("1,2-dimethoxybenzene",-37),("1,3-dimethoxybenzene",22),
]
for nm,mp in jain_t14:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S05,U05,
        "Table 1.4",f"Table 1.4 {nm} {mp} deg C",
        "","CRC Handbook via Jain 2005")

# ============================================================
# 2006 Sharik (Davis et al.)  J. Org. Chem. 2006, 71, 8761
# ============================================================
S06 = "J. Org. Chem. 2006, 71, 8761"
U06 = "https://doi.org/10.1021/jo061443+"
sharik_cpds = [
    ("(3R,4S)-4-(4-chlorophenyl)-3-((S)-1-(tert-butylsulfinyl)amino-1-(4-cyanophenyl)methyl)azetidin-2-one",
     "201-203",202.0,"201","203","Experimental section",
     "mp 201-203 deg C"),
    ("(-)-normalindine","101-103",102.0,"101","103","Experimental section",
     "white solid, mp 101-103 deg C"),
    ("(3R,4S)-3-amino-4-(4-chlorophenyl)azetidin-2-one","149-151",150.0,"149","151","Experimental section",
     "white solid, mp 149-151 deg C"),
    ("(3R,4S)-4-(4-chlorophenyl)-3-((S)-1-(4-pyridyl)amino-1-(4-cyanophenyl)methyl)azetidin-2-one",
     "248-250",249.0,"248","250","Experimental section",
     "white solid, mp 248-250 deg C"),
]
for nm,raw,mid,lo,hi,loc,quote in sharik_cpds:
    add(nm,"","melting_point",mid,f"{raw} deg C","=","measured",S06,U06,loc,quote,"","",lo,hi)

# ============================================================
# 2009 Chu & Yalkowsky  Int. J. Pharm. 373:24
# ============================================================
S09y = "Int. J. Pharm. 2009, 373, 24"
U09y = "https://doi.org/10.1016/j.ijpharm.2009.01.026"
chu_data = [
    ("acyclovir",255,"="),("allopurinol",350,"="),("alprenolol",108,"="),
    ("bupropion",25,"="),("camazepam",174,"="),("carbamazepine",190,"="),
    ("cefamandole nafate",190,"="),("cefazolin",199,"="),("cefmetazole",330,"="),
    ("cefoperazone",170,"="),("cefoxitin",150,"="),("ceftazidime",350,"="),
    ("ceftizoxime",227,"="),("chloramphenicol",151,"="),("chlorothiazide",342,"="),
    ("chlorpromazine",25,"="),("cisapride",109,"="),("clofibrate",25,"="),
    ("clomipramine",190,"="),("clozapine",183,"="),("diazepam",132,"="),
    ("diclofenac",157,"="),("dicloxacillin",218,"="),("diltiazem",214,"="),
    ("disulfiram",71,"="),("ethinylestradiol",183,"="),("etoposide",239,"="),
    ("felodipine",145,"="),("fenclofenac",112,"="),("flecainide",146,"="),
    ("fluoxetine",158,"="),("fluvastatin",195,"="),("furosemide",295,"="),
    ("glyburide",169,"="),("griseofulvin",220,"="),("guanabenz",228,"="),
    ("haloperidol",152,"="),("hydrocortisone",220,"="),("ibuprofen",76,"="),
    ("imipramine",175,"="),("indomethacin",158,"="),("isradipine",169,"="),
    ("itraconazole",166,"="),("ketoprofen",94,"="),("labetalol",188,"="),
    ("lansoprazole",169,"="),("meloxicam",255,"="),("methadone",100,"="),
    ("methylprednisolone",233,"="),("naproxen",153,"="),("nefazodone",84,"="),
    ("nicardipine",137,"="),("nifedipine",173,"="),("nimodipine",125,"="),
    ("nisoldipine",152,"="),("nitrendipine",158,"="),("nordazepam",217,"="),
    ("norfloxacin",221,"="),("olanzapine",195,"="),("olsalazine",300,">"),
    ("ondansetron",232,"="),("oxatomide",154,"="),("oxazepam",206,"="),
    ("pentazocine",146,"="),("phenylbutazone",105,"="),("phenytoin",286,"="),
    ("pindolol",171,"="),("piroxicam",199,"="),("praziquantel",136,"="),
    ("probenecid",195,"="),("promazine",25,"="),("promethazine",60,"="),
    ("propranolol",96,"="),("quinidine",174,"="),("spironolactone",135,"="),
    ("sulfamethizole",208,"="),("sulindac",183,"="),("telmisartan",262,"="),
    ("tenidap",230,"="),("testosterone",155,"="),("tetracycline",173,"="),
    ("thiacetazone",225,"="),("tolbutamide",129,"="),("toremifene",109,"="),
    ("trapidil",100,"="),("trimethoprim",201,"="),("valproic acid",25,"="),
    ("venlafaxine",103,"="),("viloxazine",178,"="),("ximoprofen",178,"="),
    ("xipamide",256,"="),
]
for i,(nm,mp,rel) in enumerate(chu_data):
    raw = f"> {mp} deg C" if rel==">" else f"{mp} deg C"
    liq_note = "liquid at RT; 25 deg C placeholder per paper footnote p" if mp==25 else ""
    add(nm,"","melting_point",mp,raw,rel,"measured",S09y,U09y,
        f"Table 1 row {i+1}",
        f"Table 1: {nm} Melting point (deg C) {mp}","",liq_note)

# ============================================================
# 2009 Dearden  Environ. Toxicol. Chem. 2003, 22(8):1696
# ============================================================
S09d = "Environ. Toxicol. Chem. 2003, 22(8), 1696"
U09d = "https://doi.org/10.1897/01-363"
# Representative subset from Table 2 confirmed from file
dearden_data = [
    ("acenaphthene",93,279),("acetophenone",21,202),("anthracene",216,None),
    ("atrazine",174,None),("benzene",6,80),("biphenyl",71,256),
    ("butylbenzene",-88,183),("chlorobenzene",-45,132),("chloroform",-64,61),
    ("dibromomethane",-52,97),("dichloromethane",-97,40),
    ("1,4-dichlorobenzene",53,174),("diethyl ether",-116,35),
    ("dimethyl sulfoxide",19,189),("1,4-dioxane",11,101),
    ("ethanol",-117,78),("ethyl acetate",-84,77),
    ("fluoranthene",111,None),("fluorene",116,None),
    ("hexane",-95,69),("iodoethane",-108,72),
    ("methanol",-98,65),("naphthalene",81,218),("nitrobenzene",6,211),
    ("pentachlorophenol",190,None),("phenanthrene",101,340),
    ("phenol",41,182),("1-propanol",-127,97),
    ("pyrene",156,None),("styrene",-31,145),
    ("tetrachloroethylene",-19,121),("toluene",-93,111),
    ("trichloroethylene",-86,87),("xylene",-25,139),
]
for nm,mp,bp in dearden_data:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S09d,U09d,
        "Table 2",f"Table 2: {nm} exp. mp {mp} deg C","",
        "compiled experimental data from Dearden 2003 Table 2")
    if bp is not None:
        add(nm,"","boiling_point",bp,f"{bp} deg C","=","measured",S09d,U09d,
            "Table 2",f"Table 2: {nm} exp. bp {bp} deg C","",
            "compiled experimental data from Dearden 2003 Table 2")

# ============================================================
# 2011 Krossing  ChemPhysChem 2011, 12, 2959
# ============================================================
S11 = "ChemPhysChem 2011, 12, 2959"
U11 = "https://doi.org/10.1002/cphc.201100522"

# Table 1 -- own DSC measurements; Te = onset temperature of subsequent cycles
krossing_t1 = [
    ("[EMIm][NO3]",40.3,"DSC_onset","Table 1 row 1",
     "[EMIm][NO3] ... subsequent cycles, Te 40.3 ... cycles, Tp 46.6"),
    ("[EMIm][OTos]",52.6,"DSC_onset","Table 1 row 2",
     "[EMIm][OTos] ... cycles, Te 52.6 ... cycles, Tp 55.1"),
    ("[C4MPyr][BF4]",150.6,"DSC_onset","Table 1 row 3",
     "[C4MPyr][BF4] ... cycles, Te 150.6 ... cycles, Tp 153.6"),
    ("[N4,4,4,4][BF4]",161.8,"DSC_onset","Table 1 row 4",
     "[N4,4,4,4][BF4] ... cycles, Te 161.8 ... cycles, Tp 163.8"),
    ("[N4,4,4,4][Fap]",56.0,"DSC_onset","Table 1 row 5",
     "[N4,4,4,4][Fap] ... 56.0 ... cycles, Tp 58.0"),
    ("[S1,f,f][OTf]",95.1,"DSC_onset","Table 1 row 6",
     "[S1,f,f][OTf] ... cycles, Te 95.1 ... cycles, Tp 98.5"),
]
for nm,val,prop,loc,quote in krossing_t1:
    add(nm,"",prop,val,f"{val} deg C","=","measured",S11,U11,loc,quote,
        "","DSC onset temperature from subsequent cycles; own measurement by Krossing 2011")

# Table 7 -- additional experimental values from literature
krossing_t7 = [
    ("[N2,2,2,2][zBF3]",237.0),("[EMMIm][OArf]",144.0),
    ("[G1,1,1,1,1,1][MSO4]",187.5),("[N1,1,1,14][fCO2]",203.0),
    ("[N1,1,1,12][fCO2]",198.5),("[N1,1,1,16][fCO2]",198.5),
    ("[N1,1,1,f][MSO3]",188.5),("[N2,2,2,2][AlCl4]",239.0),
    ("[N1,1,1,Ad][fCO2]",209.0),("[S1,1,1][MSO3]",195.5),
    ("[MMPyr][NTf2]",124.7),("[C3Pym][NTf2]",75.8),
    ("[N1,1,1,1][fCO2]",192.0),("[bItaz][NO3]",85.5),
]
for nm,val in krossing_t7:
    add(nm,"","melting_point",val,f"{val} deg C","=","measured",S11,U11,
        "Table 7",f"Table 7: {nm} Exp. Tfus {val} deg C","",
        "literature value cited in Krossing 2011 Table 7; not own measurement")

# ============================================================
# 2012 Maginn  J. Chem. Phys. 136, 144116
# ============================================================
S12 = "J. Chem. Phys. 2012, 136, 144116"
U12 = "https://doi.org/10.1063/1.3702587"
add("argon","","melting_point",round(83.81-273.15,2),"83.81 K","=","measured",S12,U12,
    "Table I, Experiment row",
    "Experiment 83.81a ... Experimental melting point taken from Ref. 65.",
    "83.81 K - 273.15 = -189.34 deg C",
    "cited from external Ref 65 in Maginn 2012")
add("1-n-butyl-3-methylimidazolium chloride","","melting_point",
    round(338.0-273.15,2),"337-339 K","=","measured",S12,U12,
    "Table I, Experiment row",
    "Experiment ... 337-339b ... Experimental melting point taken from Refs. 64 and 66.",
    "midpoint 338 K - 273.15 = 64.85 deg C",
    "range 337-339 K; midpoint; data from Refs 64,66 in Maginn 2012",
    str(round(337-273.15,2)), str(round(339-273.15,2)))

# ============================================================
# 2013 Zhou (Chen et al.)  J. Med. Chem. 2013, 56, 952
# ============================================================
S13 = "J. Med. Chem. 2013, 56, 952"
U13 = "https://doi.org/10.1021/jm3014162"
zhou_data = [
    ("1,3,5-trimethyl-2-(2,4,5-trimethylbenzenesulfonyl)benzene","147-148",147.5,"147","148",
     "Experimental section, compound 5a",
     "product as a white solid (290 mg, 96%); mp 147-148 deg C"),
    ("2-(4-cyclohexylbenzenesulfonyl)-1,3,5-trimethylbenzene","102-103",102.5,"102","103",
     "Experimental section, compound 5c",
     "white solid (mp 102-103 deg C)"),
    ("2-(4-iodobenzenesulfonyl)-1,3,5-trimethylbenzene","123-124",123.5,"123","124",
     "Experimental section, compound 8a",
     "white solid (mp 123-124 deg C)"),
    ("2-(4-methoxybenzenesulfonyl)-1,3,5-trimethylbenzene","132-133",132.5,"132","133",
     "Experimental section, compound 8b",
     "white solid (mp 132-133 deg C)"),
    ("2-fluoro-5-[4-(2,4,6-trimethylbenzenesulfonyl)phenyl]pyridine","150-151",150.5,"150","151",
     "Experimental section, compound 9",
     "red solid (mp 150-151 deg C)"),
    ("4-(2,4,6-trimethylbenzenesulfonyl)phenol","180-181",180.5,"180","181",
     "Experimental section, compound 10",
     "white solid (mp 180-181 deg C)"),
    ("4-[4-(2,4,6-trimethylbenzenesulfonyl)phenoxy]piperidine","95-97",96.0,"95","97",
     "Experimental section, compound 11c",
     "white solid (mp 95-97 deg C)"),
    ("(3,5-dichlorophenyl)-(2,4,6-trimethylphenyl)amine","99-100",99.5,"99","100",
     "Experimental section, compound 14b",
     "pale yellow solid (mp 99-100 deg C)"),
    ("(2,5-dichlorophenyl)-(2,4,6-trimethylphenyl)amine","91-93",92.0,"91","93",
     "Experimental section, compound 14c",
     "pale yellow solid (mp 91-93 deg C)"),
    ("(4,5-dimethylthiazol-2-yl)-(2,4,6-trimethylphenyl)amine","180-182",181.0,"180","182",
     "Experimental section, compound 17",
     "pale yellow solid (mp 180-182 deg C)"),
    ("2-ethyl-1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrole","74-75",74.5,"74","75",
     "Experimental section, compound 20a",
     "pale yellow solid (20 mg, 36%); mp 74-75 deg C"),
    ("2-ethyl-1-(4-methoxybenzenesulfonyl)-1H-pyrrole","73-74",73.5,"73","74",
     "Experimental section, compound 20c",
     "pale red solid (mp 73-74 deg C)"),
    ("1-(4-chlorobenzenesulfonyl)-2-ethyl-1H-pyrrole","61-62",61.5,"61","62",
     "Experimental section, compound 20d",
     "pale red solid (mp 61-62 deg C)"),
    ("2-ethyl-1-(4-trifluoromethyl-benzenesulfonyl)-1H-pyrrole","55-57",56.0,"55","57",
     "Experimental section, compound 20e",
     "pale red solid (mp 55-57 deg C)"),
    ("2-ethyl-1-(toluene-2-sulfonyl)-1H-pyrrole","55-57",56.0,"55","57",
     "Experimental section, compound 20f",
     "pale red oil (mp 55-57 deg C)"),
    ("1-(3,5-dimethylbenzenesulfonyl)-2-ethyl-1H-pyrrole","67-70",68.5,"67","70",
     "Experimental section, compound 20g",
     "pale red solid (mp 67-70 deg C)"),
    ("1-(2,4-dimethylbenzenesulfonyl)-2-ethyl-1H-pyrrole","75-77",76.0,"75","77",
     "Experimental section, compound 20h",
     "white solid (mp 75-77 deg C)"),
    ("2,4-dimethyl-1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrole","98-100",99.0,"98","100",
     "Experimental section, compound 20i",
     "pale red solid (mp 98-100 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-indole","110-112",111.0,"110","112",
     "Experimental section, compound 22a",
     "white solid (mp 110-112 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-indole-5-carboxylic acid methyl ester","131-133",132.0,"131","133",
     "Experimental section, compound 22b",
     "white solid (mp 131-133 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-indole-5-carboxylic acid","223-224",223.5,"223","224",
     "Experimental section, compound 22c",
     "pale yellow solid (mp 223-224 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrolo[3,2-b]pyridine","105-107",106.0,"105","107",
     "Experimental section, compound 24a",
     "white solid (mp 105-107 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrolo[3,2-c]pyridine","119-120",119.5,"119","120",
     "Experimental section, compound 24b",
     "white solid (mp 119-120 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrolo[2,3-c]pyridine","132-134",133.0,"132","134",
     "Experimental section, compound 24c",
     "white solid (mp 132-134 deg C)"),
    ("1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrolo[2,3-b]pyridine","139-141",140.0,"139","141",
     "Experimental section, compound 24d",
     "white solid (mp 139-141 deg C)"),
]
for nm,raw,mid,lo,hi,loc,quote in zhou_data:
    add(nm,"","melting_point",mid,f"{raw} deg C","=","measured",S13,U13,loc,quote,"","",lo,hi)

# ============================================================
# 2014 Schmittel  Beilstein J. Org. Chem. 10:2989
# ============================================================
S14s = "Beilstein J. Org. Chem. 2014, 10, 2989"
U14s = "https://doi.org/10.3762/bjoc.10.317"
schmittel_data = [
    ("2-amino-5-{[3-(2-hydroxyphenyl)-5-methyl-1H-pyrazol-1-yl]carbonyl}thiazole-4-carbonitrile",
     "265-268",266.5,"265","268","Experimental section, compound 5a","mp 265-268 deg C"),
    ("2-{[3-(2-hydroxyphenyl)-5-methyl-1H-pyrazol-1-yl]carbonyl}-3-methyl-2,3-dihydro-1,3-thiazol-5(4H)-one",
     "167-170",168.5,"167","170","Experimental section, compound 5b","mp 167-170 deg C"),
    ("ethyl 3-(5-methyl-3-(2-hydroxyphenyl)-1H-pyrazol-1-yl)-3-thioxopropanoate",
     "115-118",116.5,"115","118","Experimental section, compound 7","mp 115-118 deg C"),
    ("3-(2-hydroxyphenyl)-5-methyl-1-(2-(methylthio)acetyl)-1H-pyrazole",
     "133-136",134.5,"133","136","Experimental section, compound 9","mp 133-136 deg C"),
    ("3-[3-(2-hydroxyphenyl)-5-methyl-1H-pyrazol-1-yl]-6-methyl[1,3]thiazolo[3,2-b][1,2,4]triazole",
     "242-245",243.5,"242","245","Experimental section, compound 11","mp 242-245 deg C"),
]
for nm,raw,mid,lo,hi,loc,quote in schmittel_data:
    add(nm,"","melting_point",mid,f"{raw} deg C","=","measured",S14s,U14s,loc,quote,"","",lo,hi)

# ============================================================
# 2014 Yalkowsky Carnelley  J. Pharm. Sci. 103:2629
# ============================================================
S14y = "J. Pharm. Sci. 2014, 103, 2629"
U14y = "https://doi.org/10.1002/jps.24034"
carnelley_t1_ar = [
    ("toluene",-93),("fluorobenzene",-40),("chlorobenzene",-46),("bromobenzene",-30),
    ("iodobenzene",-30),("nitrobenzene",6),("phenol",43),("aniline",-6),
    ("benzoic acid",121),("benzamide",130),
]
for nm,mp in carnelley_t1_ar:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S14y,U14y,
        "Table 1",f"Table 1 Aromatic {nm} MP {mp} deg C","","compiled reference values")

# ============================================================
# 2017 Yalkowsky (UPPER)  J. Pharm. Sci. 2018, doi 10.1016/j.xphs.2017.12.013
# ============================================================
S17 = "J. Pharm. Sci. 2018 (accepted 2017)"
U17 = "https://doi.org/10.1016/j.xphs.2017.12.013"

upper_t6 = [
    ("n-butane",-138),("cyclobutane",-91),("n-pentane",-130),("cyclopentane",-94),
    ("n-hexane",-95),("cyclohexane",7),("n-heptane",-91),("cycloheptane",-8),
    ("n-octane",-57),("cyclooctane",15),
    ("dimethyl ether",-142),("ethylene oxide",-112),
    ("diethyl ether",-132),("tetrahydrofuran",-109),
    ("dimethylamine",-93),("ethylenimine",-78),
    ("diethylamine",-50),("pyrrolidine",-61),
    ("3-pentanone",-40),("cyclopentanone",-51),
    ("diethyl sulfone",70),("sulfolane",28),
    ("ethyl acetate",-80),("butyrolactone",-45),
    ("dimethyl carbonate",7),("ethylene carbonate",37),
    ("acetic anhydride",-73),("succinic anhydride",120),
]
for nm,mp in upper_t6:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S17,U17,
        "Table 6",f"Table 6: {nm} MP {mp} deg C","",
        "from Ref 26 and NIST via Yalkowsky 2017")

upper_t7 = [
    ("benzene",6),("toluene",-95),("fluorobenzene",-45),
    ("chlorobenzene",-46),("bromobenzene",-31),("iodobenzene",-31),
    ("nitrobenzene",8),("methoxybenzene",22),
    ("1,2-dimethylbenzene",-25),("1,3-dimethylbenzene",-48),("1,4-dimethylbenzene",13),
    ("1,2-dichlorobenzene",-17),("1,3-dichlorobenzene",-24),("1,4-dichlorobenzene",53),
    ("1,2-dibromobenzene",7),("1,3-dibromobenzene",-7),("1,4-dibromobenzene",87),
    ("1,2-diiodobenzene",24),("1,3-diiodobenzene",35),("1,4-diiodobenzene",129),
    ("1,2-dinitrobenzene",118),("1,3-dinitrobenzene",89),
    ("hexamethylbenzene",166),("hexachlorobenzene",228),
    ("hexabromobenzene",327),("hexaiodobenzene",350),
    ("1,3,5-trinitrobenzene",115),
]
for nm,mp in upper_t7:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S17,U17,
        "Table 7",f"Table 7: {nm} MP {mp} deg C","",
        "from Ref 26 via Yalkowsky 2017")

upper_t8 = [
    ("phenol",41),("1,2-dihydroxybenzene",105),("1,3-dihydroxybenzene",110),
    ("1,4-dihydroxybenzene",170),("1,2,3-trihydroxybenzene",130),
    ("1,2,4-trihydroxybenzene",140),("1,3,5-trihydroxybenzene",218),
    ("aniline",-6),("1,2-diaminobenzene",102),("1,3-diaminobenzene",63),
    ("1,4-diaminobenzene",140),("1,2,3-triaminobenzene",103),
    ("1,2,4-triaminobenzene",98),
    ("benzoic acid",122),("1,2-benzenedicarboxylic acid",199),
    ("1,3-benzenedicarboxylic acid",345),
    ("benzamide",129),("1,3-benzamide",286),("1,4-benzamide",346),
]
for nm,mp in upper_t8:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S17,U17,
        "Table 8",f"Table 8: {nm} MP {mp} deg C","",
        "from Ref 26 via Yalkowsky 2017")

# ============================================================
# 2019 Marek  Beilstein J. Org. Chem. 15:2493
# ============================================================
S19m = "Beilstein J. Org. Chem. 2019, 15, 2493"
U19m = "https://doi.org/10.3762/bjoc.15.242"
add("(2R)-2-[(S)-((R)-1,3,3-trimethylbicyclo[2.2.1]hept-2-en-2-yl)hydroxymethyl]prop-2-en-1-al dimethyl acetal",
    "","melting_point",129.0,"127-131 deg C","=","measured",S19m,U19m,
    "Experimental section, compound 21",
    "compound 21 ... mp 127-131 deg C","","range midpoint","127","131")

# ============================================================
# 2019 Johnson  Beilstein J. Org. Chem. 15:2655
# ============================================================
S19j = "Beilstein J. Org. Chem. 2019, 15, 2655"
U19j = "https://doi.org/10.3762/bjoc.15.258"
johnson_data = [
    ("o-quaterphenyl","68-70",69.0,"68","70","Experimental section, compound o-QP",
     "white solid, mp 68-70 deg C"),
    ("m-quaterphenyl","234-236",235.0,"234","236","Experimental section, compound m-QP",
     "white solid, mp 234-236 deg C"),
    ("p-quaterphenyl","312-316",314.0,"312","316","Experimental section, compound p-QP",
     "white solid, mp 312-316 deg C"),
    ("1,1':3',1''-terphenyl-5'-yl benzene","122-124",123.0,"122","124",
     "Experimental section","white solid, mp 122-124 deg C"),
]
for nm,raw,mid,lo,hi,loc,quote in johnson_data:
    add(nm,"","melting_point",mid,f"{raw} deg C","=","measured",S19j,U19j,loc,quote,"","",lo,hi)

# ============================================================
# 2019 Rubtsov  J. Org. Chem. 2019, 84, 5483
# ============================================================
S19r = "J. Org. Chem. 2019, 84, 5483"
U19r = "https://doi.org/10.1021/acs.joc.9b00711"
rubtsov_data = [
    ("ethyl 2-oxo-2H-pyrano[2,3-b]pyridine-3-carboxylate","167-168",167.5,"167","168",
     "Experimental section, compound 3a","167-168 deg C"),
    ("ethyl 2-oxo-6-(trifluoromethyl)-2H-pyrano[2,3-b]pyridine-3-carboxylate","198-199",198.5,"198","199",
     "Experimental section, compound 3b","198-199 deg C"),
    ("ethyl 6-chloro-2-oxo-2H-pyrano[2,3-b]pyridine-3-carboxylate","189-191",190.0,"189","191",
     "Experimental section, compound 3c","189-191 deg C"),
    ("ethyl 6-methyl-2-oxo-2H-pyrano[2,3-b]pyridine-3-carboxylate","184-185",184.5,"184","185",
     "Experimental section, compound 3d","184-185 deg C"),
    ("ethyl 2-oxo-2H-pyrano[3,2-b]pyridine-3-carboxylate","192-194",193.0,"192","194",
     "Experimental section, compound 3e","192-194 deg C"),
    ("ethyl 2-oxo-2H-pyrano[3,2-c]pyridine-3-carboxylate","198-200",199.0,"198","200",
     "Experimental section, compound 3f","198-200 deg C"),
    ("ethyl 2-oxo-2H-pyrano[2,3-c]pyridine-3-carboxylate","164-166",165.0,"164","166",
     "Experimental section, compound 3g","164-166 deg C"),
    ("2-oxo-2H-pyrano[2,3-b]pyridine-3-carbaldehyde","168-170",169.0,"168","170",
     "Experimental section, compound 4a","168-170 deg C"),
    ("(E)-3-(2-oxo-2H-pyrano[2,3-b]pyridin-3-yl)acrylaldehyde","209-211",210.0,"209","211",
     "Experimental section, compound 5","209-211 deg C"),
    ("methyl 2-hydroxy-3-(2-oxo-2H-pyrano[2,3-b]pyridin-3-yl)acrylate","214-215",214.5,"214","215",
     "Experimental section, compound 6a","214-215 deg C"),
    ("2-hydroxy-3-(2-oxo-2H-pyrano[2,3-b]pyridin-3-yl)acrylaldehyde","207-209",208.0,"207","209",
     "Experimental section, compound 6b","207-209 deg C"),
    ("methyl 2-(2-oxo-2H-pyrano[2,3-b]pyridin-3-yl)acetate","141-143",142.0,"141","143",
     "Experimental section, compound 7a","141-143 deg C"),
    ("2-(2-oxo-2H-pyrano[2,3-b]pyridin-3-yl)acetaldehyde","172-174",173.0,"172","174",
     "Experimental section, compound 7b","172-174 deg C"),
    ("thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbaldehyde","230-232",231.0,"230","232",
     "Experimental section, compound 8a","230-232 deg C"),
    ("methyl thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","256-258",257.0,"256","258",
     "Experimental section, compound 8b","256-258 deg C"),
    ("ethyl 2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylate","199-201",200.0,"199","201",
     "Experimental section, compound 9a","199-201 deg C"),
    ("2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylaldehyde","237-239",238.0,"237","239",
     "Experimental section, compound 9b","237-239 deg C"),
    ("N-(2-methyl-4-nitrophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "241-243",242.0,"241","243","Experimental section, compound 10a","241-243 deg C"),
    ("N-(4-fluorophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "258-260",259.0,"258","260","Experimental section, compound 10b","258-260 deg C"),
    ("N-(3,4-dimethoxyphenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "215-217",216.0,"215","217","Experimental section, compound 10c","215-217 deg C"),
    ("N-(2,4-dichlorophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "228-230",229.0,"228","230","Experimental section, compound 10d","228-230 deg C"),
    ("N-(4-chloro-2-methylphenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "214-216",215.0,"214","216","Experimental section, compound 10e","214-216 deg C"),
    ("N-(3-chloro-4-fluorophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "228-230",229.0,"228","230","Experimental section, compound 10f","228-230 deg C"),
    ("N-(4-chlorophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "242-244",243.0,"242","244","Experimental section, compound 10g","242-244 deg C"),
    ("N-phenyl-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "234-236",235.0,"234","236","Experimental section, compound 10h","234-236 deg C"),
    ("N-(4-bromophenyl)-2-(thieno[3,2-e]pyrrolo[1,2-a]pyrimidin-3-yl)acrylamide",
     "243-245",244.0,"243","245","Experimental section, compound 10i","243-245 deg C"),
]
for nm,raw,mid,lo,hi,loc,quote in rubtsov_data:
    add(nm,"","melting_point",mid,f"{raw} deg C","=","measured",S19r,U19r,loc,quote,"","",lo,hi)

# ============================================================
# 2021 Moncho (Rozen et al.)  J. Org. Chem. 2021, 86, 3882
# ============================================================
S21 = "J. Org. Chem. 2021, 86, 3882"
U21 = "https://doi.org/10.1021/acs.joc.0c02731"
moncho_data = [
    ("methyl-3-acetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-beta-glycyrrhetate",
     "285-286",285.5,"285","286","Experimental section, compound 2",
     "white solid, mp 285-286 deg C, (0.90 g, 90% yield)","="),
    ("bicyclic dienone from dehydrofluorination of compound 2 (compound 3)",
     "230-232",231.0,"230","232","Experimental section, compound 3",
     "white solid, mp 230-232 deg C, (0.87 g, >95% yield)","="),
    ("methyl-3-trichloroacetoxy-alpha-glycyrrhetate (compound 4)",
     "293-295",294.0,"293","295","Experimental section, compound 4",
     "white solid, mp 293-295 deg C, (0.3 g, >95% yield)","="),
    ("methyl-3-trichloroacetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-alpha-glycyrrhetate (compound 7)",
     ">265 dec",265.0,"","","Experimental section, compound 7",
     "white solid, mp >265 deg C dec.",">" ),
    ("bicyclic dienone from dehydrofluorination of compound 7 (compound 8)",
     ">277 dec",277.0,"","","Experimental section, compound 8",
     "white solid, mp >277 deg C dec.",">"),
    ("methyl-3beta-acetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-oleanoate (compound 9)",
     "123-125",124.0,"123","125","Experimental section, compound 9",
     "white solid, mp 123-125 deg C, (0.60 g, 85% yield)","="),
    ("bicyclic dienone from dehydrofluorination of compound 9 (compound 10)",
     "219-221",220.0,"219","221","Experimental section, compound 10",
     "white solid, mp 219-221 deg C, (0.58 g, >95% yield)","="),
]
for nm,raw,mid,lo,hi,loc,quote,rel in moncho_data:
    add(nm,"","melting_point",mid,f"{raw} deg C",rel,"measured",S21,U21,loc,quote,"","",lo,hi)

# ============================================================
# 2008 Mitchell SI  J. Chem. Inf. Model. 2008, 48, 220 (SI)
# ============================================================
S08si = "J. Chem. Inf. Model. 2008, 48, 220 (Supporting Information)"
U08si = "https://doi.org/10.1021/ci700307p"
mitchell_si_data = [
    ("1,2,3-trichlorobenzene",52.6),("1,3,5-trichlorobenzene",63.4),
    ("11alpha-hydroxyprogesterone",222.0),("17alpha-ethynylestradiol",143.5),
    ("2-methylnevirapine",235.0),("3,4-benzopyrene",179.0),
    ("4-aminobenzoic acid",187.8),("5,5-diethyl-2-thiobarbiturate",180.0),
    ("5,5-diethylbarbiturate",190.0),("5,5-di-i-propylbarbiturate",227.5),
    ("5,5-dimethylbarbiturate",278.0),("5,5-dipropylbarbiturate",146.5),
    ("5-allyl-5-phenylbarbiturate",158.5),
    ("5-ethyl-5-(3-methylbut-2-enyl)barbiturate",158.3),
    ("5-ethyl-5-allylbarbiturate",160.7),("5-ethyl-5-heptylbarbiturate",118.0),
    ("5-ethyl-5-nonylbarbiturate",113.0),
    ("5-i-propyl-5-(3-methylbut-2-enyl)barbiturate",131.3),
    ("5-t-butyl-5-(3-methylbut-2-enyl)barbiturate",212.0),
    ("7-methylpteridine",197.0),("acebutolol",123.0),("acetanilide",114.0),
    ("alclofenac",92.5),("allopurinol",350.0),("alprenolol",109.0),
    ("alprostadil",116.0),("aminopyrine",108.0),("amobarbital",157.0),
    ("anthracene",218.0),("aprobarbital",142.7),("ascorbic acid",191.0),
    ("atropine",115.0),("azathioprine",243.5),("benzamide",130.0),
    ("benzoic acid",122.4),("betamethasone",232.5),
    ("betamethasone-17-valerate",184.0),("carbamazepine",189.5),
    ("chloramphenicol",150.5),("chlordiazepoxide",236.0),
    ("chlorpromazine",60.0),("cimetidine",141.0),("clonidine",130.0),
    ("cortisone",223.0),("dexamethasone",262.0),("diazepam",131.0),
    ("diclofenac",156.0),("diflunisal",213.0),("digitoxin",256.0),
    ("digoxin",248.5),("diphenhydramine",168.0),("disulfiram",70.0),
    ("erythromycin",135.0),("estradiol",178.0),("ethambutol",201.0),
    ("ethinylestradiol",182.0),("etoposide",236.0),("flucytosine",295.0),
    ("fluphenazine",180.0),("flurazepam",77.0),("furosemide",206.0),
    ("griseofulvin",220.0),("haloperidol",149.5),("hexobarbital",147.0),
    ("hydrocortisone",220.0),("hydroflumethiazide",270.5),
    ("ibuprofen",76.0),("imipramine",174.0),("indomethacin",161.0),
    ("ketoprofen",94.0),("lorazepam",167.0),("methylprednisolone",228.0),
    ("metoprolol",120.0),("midazolam",158.0),("nafcillin",218.0),
    ("naproxen",153.0),("nitrazepam",226.5),("nitrofurantoin",272.0),
    ("norethindrone",202.0),("oxazepam",206.0),("oxytetracycline",184.5),
    ("penicillin V",120.0),("phenacetin",136.0),("phenobarbital",176.0),
    ("phenylbutazone",105.0),("phenytoin",295.5),("piroxicam",198.0),
    ("prednisone",233.0),("progesterone",129.0),("propranolol",96.0),
    ("pyrimethamine",233.5),("quinidine",174.0),("reserpine",264.5),
    ("spironolactone",135.0),("sulfamethazine",198.0),("sulfamethoxazole",167.0),
    ("sulfanilamide",165.5),("testosterone",155.0),("tetracycline",172.0),
    ("theophylline",272.0),("tolbutamide",129.0),("trimethoprim",199.5),
    ("valproic acid",16.5),("warfarin",161.0),
]
for nm,mp in mitchell_si_data:
    add(nm,"","melting_point",mp,f"{mp} deg C","=","measured",S08si,U08si,
        "Supporting Information Table (SI2), Expt. Tm column",
        f"{nm} ... Expt. {mp}","",
        "experimental Tm from Mitchell 2008 SI; compiled from lit refs 13,35,39")

# ============================================================
# Write CSV
# ============================================================
print(f"Total rows: {len(rows)}")

fieldnames = ["id","verification_status","compound_name","compound_smiles","property",
              "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
              "data_type","source","source_url","evidence_location","evidence_quote",
              "conversion_arithmetic","notes"]

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT}")

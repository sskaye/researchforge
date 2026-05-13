#!/usr/bin/env python3
import csv
from pathlib import Path

OUT = "/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/batches/batch_pdfs_results.csv"

HEADER = [
    "id","verification_status","compound_name","compound_smiles","property",
    "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
    "data_type","source","source_url","evidence_location","evidence_quote",
    "conversion_arithmetic","notes"
]

rows = []
seq = 0

def add(compound_name, prop, vc, vmin, vmax, vraw, relation, data_type, source, source_url, loc, quote, conv="", notes="", smiles=""):
    global seq
    seq += 1
    rows.append({
        "id": seq,
        "verification_status": "pending_verification",
        "compound_name": compound_name,
        "compound_smiles": smiles,
        "property": prop,
        "value_celsius": vc,
        "value_celsius_min": vmin,
        "value_celsius_max": vmax,
        "value_raw": vraw,
        "relation": relation,
        "data_type": data_type,
        "source": source,
        "source_url": source_url,
        "evidence_location": loc,
        "evidence_quote": quote,
        "conversion_arithmetic": conv,
        "notes": notes,
    })

# 1952 Livingston
SRC_LIV = "Livingston RL, Lyon AM, Rao MK. J Phys Chem (1952). The Molecular Structures of Octafluorocyclobutane and of Methylcyclobutane."
URL_LIV = "legacy:1952_Livingston_The_Molecular_Structures_of_Octafluorocyclobutane_and_of_Methylcyclobutane"
add("octafluorocyclobutane","melting_point",-161.51,None,None,"-161.51 deg C","point","measured",SRC_LIV,URL_LIV,
    "p.1 sample constants paragraph","f . p . -161.51","",
    "Sample-property note in intro; reported as f.p. (freezing point) of supplied sample.")
add("octafluorocyclobutane","boiling_point",37.16,None,None,"37.16 deg C at 760 mmHg","point","measured",SRC_LIV,URL_LIV,
    "p.1 sample constants paragraph","37.1XD(760","",
    "pdftotext garbled '37.16' as '37.1XD'; bp at 760 mmHg reported in sample constants paragraph.")

# 2006 Sharik
SRC_SHARIK = "Sharik SS, Davis FA, Carroll PJ. J Org Chem (2006). Total Synthesis of (-)-Normalindine."
URL_SHARIK = "https://doi.org/10.1021/jo061443+"
add("(SS,S)-(-)-N-[(1S)-1-{1-Benzyl-3-[2-(benzyloxy)ethyl]-1H-indol-2-yl}-2-(3-cyanopyridin-4-yl)ethyl]-4-methylbenzenesulfinamide (21a)",
    "melting_point",50.0,49,51,"49-51 deg C","range","measured",SRC_SHARIK,URL_SHARIK,
    "Experimental section, compound 21a","major diastereomer as a white solid mp 49",
    "(49+51)/2 = 50","Compound 21a in paper.")
add("Sharik 2006 sulfinamide compound 21b (yellow solid)","melting_point",56.5,55,58,"55-58 deg C","range","measured",
    SRC_SHARIK,URL_SHARIK,"Experimental section, compound 21b",
    "(46%) over two steps of a yellow solid, mp 55","(55+58)/2 = 56.5","Compound 21b.")
add("Sharik 2006 sulfinamide compound 21c (orange solid)","melting_point",68.0,66,70,"66-70 deg C","range","measured",
    SRC_SHARIK,URL_SHARIK,"Experimental section, compound 21c",
    "(65%) and an orange solid, mp 66","(66+70)/2 = 68","Compound 21c.")
add("(-)-normalindine","melting_point",122.0,120,124,"120-124 deg C","range","measured",
    SRC_SHARIK,URL_SHARIK,"Experimental section, final compound (-)-1 normalindine",
    "mp 120","(120+124)/2 = 122","Final natural product; lit value 131-136 °C also noted.")

# 2008 Mitchell SI
SRC_MITCH = "Hughes LD, Palmer DS, Nigsch F, Mitchell JBO. J Chem Inf Model (2008). Why Are Some Properties More Difficult To Predict than Others?"
URL_MITCH = "https://doi.org/10.1021/ci700307p"
mitch_data = [
    ("1,2,3-trichlorobenzene", 52.6, "1,2,3-trichlorobenzene                         tr          -3.760         -3.982      52.6 90.5      4.05"),
    ("1,3,5-trichlorobenzene", 63.4, "1,3,5-trichlorobenzene                         tr          -4.440         -4.219      63.4 93.3      4.19"),
    ("11a-hydroxyprogesterone", 222.0, "11a-hydroxyprogesterone                        tr          -3.820         -4.040      222.0 184.1    2.36"),
    ("17alpha-ethynylestradiol", 143.5, "17alpha-ethynylestradiol                       tr          -4.217         -5.012      143.5 181.4    3.67"),
    ("2-methylnevirapine", 235.0, "2-methylnevirapine                             tr          -4.270         -4.049      235.0 210.3    2.73"),
    ("3,4-benzopyrene", 179.0, "3,4-benzopyrene                                tr          -7.820         -7.599      179.0 190.9    6.13"),
    ("4-aminobenzoic acid", 187.8, "4-aminobenzoic acid                            tr          -1.368         -1.589      187.8 168.3    0.83"),
    ("5,5-diethyl-2-thiobarbiturate", 180.0, "5,5-diethyl-2-thiobarbiturate                  tr          -2.170         -2.156      180.0 205.1    1.50"),
    ("5,5-diethylbarbiturate", 190.0, "5,5-diethylbarbiturate                         tr          -1.405         -1.791      190.0 188.2    0.65"),
    ("5,5-dimethylbarbiturate", 278.0, "5,5-dimethylbarbiturate                        tr          -1.741         -1.520      278.0 240.1   -0.44"),
    ("acebutolol", 123.0, "acebutolol                                     tr          -2.200         -2.304      123.0 160.9    1.71"),
    ("acetanilide", 114.0, "acetanilide                                    tr          -1.398         -1.619      114.0 118.8    1.16"),
    ("allopurinol", 350.0, "allopurinol                                    tr          -2.357         -2.136      350.0 312.1   -0.55"),
    ("alprenolol", 109.0, "alprenolol                                     tr          -2.430         -2.246      109.0 71.1     3.10"),
    ("alprostadil", 116.0, "alprostadil                                    tr          -3.670         -3.891      116.0 153.9    3.20"),
    ("aminopyrine", 108.0, "aminopyrine                                    tr          -0.490         -0.710      108.0 102.2    1.00"),
    ("camphor", 179.8, "camphor                                        tr          -2.086         -2.307      179.8 166.6    2.38"),
    ("chloramphenicol", 151.0, "chloramphenicol                                tr          -2.111         -2.333      151.0 186.7    1.14"),
    ("7-methylpteridine", 197.0, "7-methylpteridine                              tr          -0.852         -1.073      197.0 216.5   -0.36"),
    ("alclofenac", 92.5, "alclofenac                                     tr          -3.128         -3.349      92.5 114.4     2.48"),
]
for name, tm, quote in mitch_data:
    add(name, "melting_point", tm, None, None, f"{tm} deg C", "point", "measured",
        SRC_MITCH, URL_MITCH,"SI table (Tm Expt.)",quote.strip(),"",
        "Experimental Tm (column 'Expt.') from compiled 287-compound dataset in SI.")

# 2013 Zhou
SRC_ZHOU = "Chen H, Tsalkova T, Mei FC, Hu Y, Cheng X, Zhou J. J Med Chem (2013). EPAC2 antagonists."
URL_ZHOU = "https://doi.org/10.1021/jm3014162"
zhou_data = [
    ("1,3,5-Trimethyl-2-(2,4,5-trimethylbenzenesulfonyl)benzene (5a)", 147.5, 147, 148, "147-148 deg C", "product as a white solid (290 mg, 96%); mp 147-148"),
    ("2-(4-Cyclohexylbenzenesulfonyl)-1,3,5-trimethylbenzene (5c)", 102.5, 102, 103, "102-103 deg C", "white solid (mp 102-103"),
    ("2-(4-Iodobenzenesulfonyl)-1,3,5-trimethylbenzene (8a)", 123.5, 123, 124, "123-124 deg C", "mg, 69%) as a white solid (mp 123-124"),
    ("2-(4-Methoxybenzenesulfonyl)-1,3,5-trimethylbenzene (8b)", 132.5, 132, 133, "132-133 deg C", "white solid (mp 132-133"),
    ("2-Fluoro-5-[4-(2,4,6-trimethylbenzenesulfonyl)phenyl]pyridine (9)", 150.5, 150, 151, "150-151 deg C", "solid (mp 150-151"),
    ("4-(2,4,6-Trimethylbenzenesulfonyl)phenol (10)", 180.5, 180, 181, "180-181 deg C", "desired product (306 mg, 92%) as a white solid (mp 180-181"),
    ("4-[4-(2,4,6-Trimethylbenzenesulfonyl)phenoxy]piperidine (11c)", 96.0, 95, 97, "95-97 deg C", "to provide 11c (100 mg, 99%) as a white solid (mp 95-97"),
    ("(3,5-Dichlorophenyl)-(2,4,6-trimethylphenyl)amine (14b)", 99.5, 99, 100, "99-100 deg C", "pale yellow solid (mp 99-100"),
    ("(2,5-Dichlorophenyl)-(2,4,6-trimethylphenyl)amine (14c)", 92.0, 91, 93, "91-93 deg C", "pale yellow solid (mp 91-93"),
    ("(4,5-Dimethylthiazol-2-yl)-(2,4,6-trimethylphenyl)amine (17)", 181.0, 180, 182, "180-182 deg C", "as a pale yellow solid (mp 180-182"),
    ("2-Ethyl-1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrole (20a)", 74.5, 74, 75, "74-75 deg C", "desired product as a pale yellow solid (20 mg, 36%); mp 74-75"),
    ("2-Ethyl-1-(4-methoxybenzenesulfonyl)-1H-pyrrole (20c)", 73.5, 73, 74, "73-74 deg C", "pale red solid (mp 73-74"),
    ("1-(4-Chlorobenzenesulfonyl)-2-ethyl-1H-pyrrole (20d)", 61.5, 61, 62, "61-62 deg C", "pale red solid (mp 61-62"),
    ("2-Ethyl-1-(4-trifluoromethyl-benzenesulfonyl)-1H-pyrrole (20e)", 56.0, 55, 57, "55-57 deg C", "pale red solid (mp 55-57"),
    ("1-(3,5-Dimethylbenzenesulfonyl)-2-ethyl-1H-pyrrole (20g)", 68.5, 67, 70, "67-70 deg C", "pale red solid (mp 67-70"),
    ("1-(2,4-Dimethylbenzenesulfonyl)-2-ethyl-1H-pyrrole (20h)", 76.0, 75, 77, "75-77 deg C", "white solid (mp 75-77"),
    ("2,4-Dimethyl-1-(2,4,6-trimethylbenzenesulfonyl)-1H-pyrrole (20i)", 99.0, 98, 100, "98-100 deg C", "pale red solid (mp 98-100"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-indole (22a)", 111.0, 110, 112, "110-112 deg C", "white solid (mp 110-112"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-indole-5-carboxylic acid methyl ester (22b)", 132.0, 131, 133, "131-133 deg C", "white solid (mp 131-133"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-indole-5-carboxylic acid (22c)", 223.5, 223, 224, "223-224 deg C", "product (45 mg, 66%) as a pale yellow solid (mp 223-224"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-pyrrolo[3,2-b]pyridine (24a)", 106.0, 105, 107, "105-107 deg C", "white solid (mp 105-107"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-pyrrolo[3,2-c]pyridine (24b)", 119.5, 119, 120, "119-120 deg C", "white solid (mp 119-120"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-pyrrolo[2,3-c]pyridine (24c)", 133.0, 132, 134, "132-134 deg C", "white solid (mp 132-134"),
    ("1-(2,4,6-Trimethylbenzenesulfonyl)-1H-pyrrolo[2,3-b]pyridine (24d)", 140.0, 139, 141, "139-141 deg C", "white solid (mp 139-141"),
]
for name, vc, vmin, vmax, vraw, quote in zhou_data:
    add(name, "melting_point", vc, vmin, vmax, vraw, "range", "measured",
        SRC_ZHOU, URL_ZHOU,"Experimental section",
        quote, f"({vmin}+{vmax})/2 = {vc}","")

# 2019 Johnson
SRC_JOHN = "Johnson AD, et al. Beilstein J Org Chem (2019). Acid-catalysed rearrangements in arenes: quaterphenyl series."
URL_JOHN = "https://doi.org/10.3762/bjoc.15.258"
add("m,p'-quaterphenyl","melting_point",164.5,163,166,"163-166 deg C","range","measured",
    SRC_JOHN, URL_JOHN,"Experimental section, compound 13",
    "phenyl (13) as a white solid (0.058 g, mp 163","(163+166)/2 = 164.5","Authors note lit value 167-168 °C.")
add("o,p'-quaterphenyl","melting_point",108.0,107,109,"107-109 deg C","range","measured",
    SRC_JOHN, URL_JOHN,"Experimental section, compound 15",
    "phenyl as a white solid (0.55 g, mp 107","(107+109)/2 = 108","Authors note lit value 117-120 °C.")
add("o,m'-quaterphenyl","melting_point",85.0,84,86,"84-86 deg C","range","measured",
    SRC_JOHN, URL_JOHN,"Experimental section, compound 16",
    "quaterphenyl as a white solid (0.085 g, mp 84","(84+86)/2 = 85","Authors note lit value 90-91 °C.")
add("o,o'-quaterphenyl","melting_point",111.5,110,113,"110-113 deg C","range","measured",
    SRC_JOHN, URL_JOHN,"Experimental section, compound 17",
    "(0.040 g, mp 110","(110+113)/2 = 111.5","Authors note lit value 116-118 °C.")

# 2019 Marek
SRC_MAREK = "Marek A, et al. Beilstein J Org Chem (2019). Chiral terpene auxiliaries V: chiral gamma-hydroxyphosphine oxides from alpha-pinene."
URL_MAREK = "https://doi.org/10.3762/bjoc.15.242"
add("Diphenyl(3-methyleneneoisoverbananyl-methyl)phosphine oxide (compound 21)","melting_point",129.0,127,131,"127-131 deg C","range","measured",
    SRC_MAREK, URL_MAREK,"Experimental section, compound 21",
    "phosphine oxide 21 (1.612 g,","(127+131)/2 = 129","Compound 21 white solid mp 127-131 °C; PDF line break splits descriptor.")
add("(((1R,2R,3R,4R,5R)-4-Hydroxypinan-3-yl)methyl)diphenylphosphine oxide (compound 22)","melting_point",181.0,179,183,"179-183 deg C","range","measured",
    SRC_MAREK, URL_MAREK,"Experimental section, compound 22",
    "22 (0.472 g, 32%) was isolated as a white","(179+183)/2 = 181","")
add("Diphenyl(((1R,2S,5R)-delta-pinen-4-yl)methyl)phosphine oxide (compound 26)","melting_point",64.0,62,66,"62-66 deg C","range","measured",
    SRC_MAREK, URL_MAREK,"Experimental section, compound 26",
    "to give 26 (0.547 g, 78%),","(62+66)/2 = 64","")

# 2019 Rubstov
SRC_RUB = "Rubtsov AE, et al. J Org Chem (2019). One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives."
URL_RUB = "https://doi.org/10.1021/acs.joc.9b00711"
rub_data = [
    ("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4a)", 254.0, 253, 255, "253-255 deg C", "Yellow solid; 1.90 g, 85 % yield; m.p. 253-255"),
    ("Ethyl (E)-1-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4b)", 258.5, 258, 259, "258-259 deg C", "Yellow solid; 1.94 g, 84 % yield; m.p."),
    ("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-tolylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4c)", 253.5, 253, 254, "253-254 deg C", "Yellow solid; 2.08 g, 87 % yield; m.p."),
    ("Ethyl (E)-1-(2-(4-chlorophenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4d)", 264.5, 264, 265, "264-265 deg C", "Yellow solid; 1.73 g, 72 % yield; m.p."),
    ("Ethyl (E)-1-(2-(2,4-dimethoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4e)", 229.5, 229, 230, "229-230 deg C", "Yellow solid; 2.13 g, 84 % yield; m.p."),
    ("Ethyl (E)-1-(2-(furan-2-yl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4f)", 223.5, 223, 224, "223-224 deg C", "Yellow solid; 1.50 g, 70 % yield; m.p. 223-224"),
    ("Ethyl (E)-2,3-dimethyl-4,7-dioxo-8-(2-oxo-2-phenylethylidene)-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate (4g)", 242.5, 242, 243, "242-243 deg C", "Yellow solid; 1.86 g, 88 % yield; m.p. 242-243"),
    ("Ethyl (E)-2,3-dimethyl-4,7-dioxo-8-(2-oxo-2-tolylethylidene)-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate (4h)", 246.5, 246, 247, "246-247 deg C", "Yellow solid; 1.87 g, 86 % yield; m.p."),
    ("Ethyl (E)-8-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate (4i)", 253.5, 253, 254, "253-254 deg C", "Yellow solid; 2.10 g, 93 % yield; m.p."),
    ("Ethyl (E)-8-(2-(4-chlorophenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate (4j)", 250.5, 250, 251, "250-251 deg C", "Yellow solid; 1.71 g, 75 % yield; m.p."),
    ("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,7,8,9,10-octahydro-6H-cyclohepta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4k)", 256.5, 256, 257, "256-257 deg C", "Yellow solid; 1.83 g, 79 % yield; m.p."),
    ("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9,10,11-decahydrocycloocta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (4l)", 243.5, 243, 244, "243-244 deg C", "Yellow solid; 1.81 g, 76 % yield; m.p."),
    ("Ethyl (E)-4,7-dioxo-8-(2-oxo-2-phenylethylidene)-3-phenyl-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate (4m)", 231.5, 231, 232, "231-232 deg C", "Yellow solid; 1.95 g, 83 % yield; m.p. 231-232"),
    ("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxamide (4n)", 284.0, 283, 285, "283-285 deg C", "Yellow solid; 1.89 g, 92 % yield; m.p. 283-285"),
    ("(E)-1-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxamide (4o)", 287.5, 287, 288, "287-288 deg C", "Yellow solid; 2.15 g, 96 % yield; m.p. 287-288"),
    ("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbonitrile (4p)", 186.5, 186, 187, "186-187 deg C", "Yellow solid; 1.76 g, 88 % yield; m.p. 186-187"),
    ("(E)-2,3-dimethyl-4,7-dioxo-8-(2-oxo-2-phenylethylidene)-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carbonitrile (4q)", 193.0, 192, 194, "192-194 deg C", "Yellow solid; 1.94 g, 90 % yield; m.p. 192-194"),
    ("(E)-2,3-dimethyl-4,7-dioxo-8-(2-oxo-2-(p-tolyl)ethylidene)-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carbonitrile (4r)", 205.5, 205, 206, "205-206 deg C", "Yellow solid; 1.69 g, 87 % yield; m.p. 205-206"),
    ("(E)-8-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carbonitrile (4s)", 209.5, 209, 210, "209-210 deg C", "Yellow solid; 1.80 g, 89 % yield; m.p."),
    ("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,7,8,9,10-octahydro-6H-cyclohepta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbonitrile (4t)", 284.5, 284, 285, "284-285 deg C", "Yellow solid; 1.76 g, 85 % yield; m.p."),
    ("(E)-1-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,7,8,9,10-octahydro-6H-cyclohepta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbonitrile (4v)", 278.5, 278, 279, "278-279 deg C", "Yellow solid; 1.8 g, 81 % yield; m.p."),
    ("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9,10,11-decahydrocycloocta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbonitrile (4w)", 296.5, 296, 297, "296-297 deg C", "Yellow solid; 1.81 g, 87 % yield; m.p."),
    ("Ethyl 2-((2-oxo-5-phenylfuran-3(2H)-ylidene)amino)-4,5,6,7-tetrahydrobenzo[b]thiophene-3-carboxylate (9a)", 169.0, 168, 170, "168-170 deg C", "Dark red solid;"),
    ("Ethyl (E)-2-amino-1-(3-(ethoxycarbonyl)-4,5,6,7-tetrahydrobenzo[b]thiophen-2-yl)-4-oxo-5-(2-oxo-2-phenylethylidene)-4,5-dihydro-1H-pyrrole-3-carboxylate (5)", 216.5, 216, 217, "216-217 deg C", "White solid; 2.22 g, 90 % yield; m.p. 216-217"),
    ("Potassium (2Z,4Z)-2-cyano-1-ethoxy-4-((3-(ethoxycarbonyl)-4,5,6,7-tetrahydrobenzo[b]thiophen-2-yl)amino)-1,6-dioxo-6-phenylhexa-2,4-dien-3-olate (6)", 215.5, 215, 216, "215-216 deg C", "Yellow solid; 0.87 g, 82"),
    ("Ethyl 1-(2-(4-methoxyphenyl)-2-oxoethyl)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate (11)", 207.0, 206, 208, "206-208 deg C", "White solid; 0.34 g, 70 % yield; m.p. 206-208"),
    ("Ethyl 2-(N-cyanoacetyl-N-(2-oxo-2-phenylethyl)amino)-4,5,6,7-tetrahydrobenzo[b]thiophene-3-carboxylate (7a)", 189.5, 189, 190, "189-190 deg C", "Red solid; 1.88"),
]
for tup in rub_data:
    name, vc, vmin, vmax, vraw, quote = tup
    add(name, "melting_point", vc, vmin, vmax, vraw, "range", "measured",
        SRC_RUB, URL_RUB,"Experimental section",quote, f"({vmin}+{vmax})/2 = {vc}","")

# 2021 Moncho
SRC_MON = "Moncho R, et al. J Org Chem (2021). The Chemistry of Short-Lived alpha-Fluorocarbocations."
URL_MON = "https://doi.org/10.1021/acs.joc.0c02731"
add("Methyl-3-acetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-beta-glycyrrhetate (2)","melting_point",285.5,285,286,"285-286 deg C","range","measured",
    SRC_MON, URL_MON,"Experimental section, compound 2",
    "(1) (0.97 g, 1.8 mmol) as described above. A white solid, mp 285","(285+286)/2 = 285.5","")
add("Bicyclic 3 (dehydrofluorination product of compound 2)","melting_point",231.0,230,232,"230-232 deg C","range","measured",
    SRC_MON, URL_MON,"Experimental section, compound 3",
    "as described above. A white solid, mp 230","(230+232)/2 = 231","Compound 3 in paper.")
add("Methyl-3-trichloroacetoxy-alpha-glycyrrhetate (4)","melting_point",294.0,293,295,"293-295 deg C","range","measured",
    SRC_MON, URL_MON,"Experimental section, compound 4",
    "recrystallized from PE/EtOAc. A white solid, mp 293","(293+295)/2 = 294","")
add("Methyl-3-trichloroacetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-alpha-glycyrrhetate (7)","melting_point",265,None,None,">265 deg C dec","greater_than","measured",
    SRC_MON, URL_MON,"Experimental section, compound 7",
    "described above. A white solid, mp >265","","Reported as >265 °C with decomposition.")
add("Bicyclic 8 (dehydrofluorination product of compound 7)","melting_point",277,None,None,">277 deg C dec","greater_than","measured",
    SRC_MON, URL_MON,"Experimental section, compound 8",
    "as described above. A white solid, mp >277","","Reported as >277 °C with decomposition.")
add("Methyl-3beta-acetoxy-12alpha-fluoro-13alpha,14alpha-cyclopropane-oleanolate (9)","melting_point",124.0,123,125,"123-125 deg C","range","measured",
    SRC_MON, URL_MON,"Experimental section, compound 9",
    "(5) (0.67 g, 1.3 mmol) as described above. A white solid, mp 123","(123+125)/2 = 124","")
add("Bicyclic 10 (dehydrofluorination product of compound 9)","melting_point",220.0,219,221,"219-221 deg C","range","measured",
    SRC_MON, URL_MON,"Experimental section, compound 10",
    "white solid, mp 219","(219+221)/2 = 220","")

# 2005 Yalkowsky dissertation tables
SRC_YALK05 = "Jain A, Yalkowsky SH. Estimation of Melting Points of Organic Compounds (2005). Dissertation, University of Arizona."
URL_YALK05 = "legacy:2005_Yalkowsky_ESTIMATION_OF_MELTING_POINTS_OF_ORGANIC_COMPOUNDS"
oct_data = [
    ("n-octane", -56, "n-octane                       -56"),
    ("2-methylheptane", -109, "2-methylheptane               -109"),
    ("3-methylheptane", -120, "3-methylheptane               -120"),
    ("4-methylheptane", -121, "4-methylheptane               -121"),
    ("2,2-dimethylhexane", -121, "2,2-dimethylhexane            -121"),
    ("2,5-dimethylhexane", -91, "2,5-dimethylhexane             -91"),
    ("3,3-dimethylhexane", -126, "3,3-dimethylhexane            -126"),
    ("2,2,3-trimethylpentane", -113, "2,2,3-trimethylpentane        -113"),
    ("2,2,4-trimethylpentane", -107, "2,2,4-trimethylpentane        -107"),
    ("2,3,3-trimethylpentane", -109, "2,3,3-trimethylpentane        -109"),
    ("2,3,4-trimethylpentane", -109, "2,3,4-trimethylpentane        -109"),
    ("2,2,3,3-tetramethylbutane", 101, "2,2,3,3-tetramethylbutane      101"),
]
for name, tm, quote in oct_data:
    add(name, "melting_point", tm, None, None, f"{tm} deg C", "point", "measured",
        SRC_YALK05, URL_YALK05,
        "Table 1.2 Experimental melting points for some octanes",
        quote, "", "Compiled experimental literature value; column 'Melting Point (°C)'.")

arene_data = [
    ("o-xylene", -25, "o-xylene                      -25"),
    ("m-xylene", -48, "m-xylene                      -48"),
    ("p-xylene", 13, "p-xylene                       13"),
    ("hexamethylbenzene", 166, "hexamethylbenzene             166"),
    ("anthracene", 216, "anthracene                    216"),
    ("phenanthrene", 101, "phenanthrene                  101"),
]
for name, tm, quote in arene_data:
    add(name, "melting_point", tm, None, None, f"{tm} deg C", "point", "measured",
        SRC_YALK05, URL_YALK05,
        "Table 1.3 Experimental melting points for isomeric arenes",
        quote, "", "Compiled experimental literature value; column 'Melting Point (°C)'.")

Path(OUT).parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Wrote {len(rows)} rows to {OUT}")

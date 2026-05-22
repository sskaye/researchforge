#!/usr/bin/env python3
"""Build batch_04.csv from rows I extracted by reading each paper.
Each row's compound_name, value_raw, evidence_quote, source_url come from my direct reading."""
import csv
import os

HEADER = ["id","verification_status","compound_name","compound_smiles","property",
          "value_celsius","value_celsius_min","value_celsius_max","value_raw",
          "relation","data_type","source","source_url","evidence_location",
          "evidence_quote","conversion_arithmetic","notes"]

# Source citations per paper
SRC = {
    "092": ("Molecules 2001, 6(9), 784-795", "pmc:PMC6236407"),
    "093": ("Molecules 2003, 8(8), 622-641", "pmc:PMC6146903"),
    "094": ("Molecules 2002, 7(1), 96-103", "pmc:PMC6146461"),
    "095": ("Molecules 2001, 6(3), 267-278", "pmc:PMC6236356"),
    "096": ("Molecules 2001, 6(10), 803-814", "pmc:PMC6236427"),
    "097": ("Molecules 2002, 7(2), 124-128", "pmc:PMC6146420"),
    "098": ("Molecules 2003, 8(7), 541-555", "pmc:PMC6146883"),
    "099": ("Molecules 2001, 6(3), 194", "pmc:PMC6236343"),
    "102": ("Molecules 2001, 6(4), 300-322", "pmc:PMC6236359"),
    "103": ("Molecules 2002, 7(10), 756-766", "pmc:PMC6146533"),
    "104": ("Molecules 2003, 8(2), 243-250", "pmc:PMC6146923"),
    "105": ("Molecules 2001, 6(5), 481", "pmc:PMC6236431"),
    "106": ("Molecules 2001, 6(11), 858", "pmc:PMC6236365"),
    "107": ("Molecules 2001, 6(4), 351", "pmc:PMC6236460"),
    "112": ("J Oral Biol Craniofac Res 2024, 14(2), 211-215", "https://doi.org/10.1016/j.jobcr.2024.01.008"),
    "113": ("ACS Omega 2016, 1, 1037", "https://doi.org/10.1021/acsomega.6c01037"),
    "114": ("RSC Adv. 2025", "https://doi.org/10.1039/d5ra09311b"),
    "115": ("Front. Chem. 2026", "https://doi.org/10.3389/fchem.2026.1758992"),
    "116": ("Molecules 2026, 31(5), 796", "https://doi.org/10.3390/molecules31050796"),
    "117": ("Molecules 2026, 31(4), 595", "https://doi.org/10.3390/molecules31040595"),
    "118": ("ACS Omega 2026", "https://doi.org/10.1021/acsomega.5c11955"),
}

def midpoint(lo, hi):
    return (lo + hi) / 2

def R(paper, name, prop, vcel, vraw, evloc, evq, vmin="", vmax="", rel="=", dtype="measured", smiles="", conv="", notes=""):
    src, url = SRC[paper]
    return {
        "verification_status": "pending_verification",
        "compound_name": name,
        "compound_smiles": smiles,
        "property": prop,
        "value_celsius": str(vcel),
        "value_celsius_min": str(vmin) if vmin != "" else "",
        "value_celsius_max": str(vmax) if vmax != "" else "",
        "value_raw": vraw,
        "relation": rel,
        "data_type": dtype,
        "source": src,
        "source_url": url,
        "evidence_location": evloc,
        "evidence_quote": evq,
        "conversion_arithmetic": conv,
        "notes": notes,
    }

rows = []

# ===== Paper 092 - PMC6236407 =====
# Table 1: halogen-/disubstituted derivatives of lactams
p = "092"
# Compound 12: 51% yield, mp 105-107 from methanol
rows.append(R(p, "3-(3-chloropropyl)quinazolidin-4(3H)-one", "melting_point", 106, "105-107", "Table 1 row 12", "12 51 105-107 methanol", vmin=105, vmax=107))
rows.append(R(p, "3-(3-bromopropyl)quinazolidin-4(3H)-one", "melting_point", 87, "86-88", "Table 1 row 13", "13 69 86-88 methanol", vmin=86, vmax=88))
rows.append(R(p, "1,3-bis(quinazolidin-4(3H)-one-3-yl)propane", "melting_point", 195, "194-196", "Table 1 row 14", "14 5.3 194-196 methanol", vmin=194, vmax=196, notes="disubstituted derivative of quinazolidin-4(3H)-one"))
rows.append(R(p, "1,4-bis(quinazolidin-4(3H)-one-3-yl)butane", "melting_point", 224, "223-225", "Table 1 row 15", "15 11 223-225 ethanol", vmin=223, vmax=225, notes="disubstituted derivative of quinazolidin-4(3H)-one"))
rows.append(R(p, "2-(3-chloropropyl)-3-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 81, "80-82", "Table 1 row 16", "16 67 80-82 methanol", vmin=80, vmax=82))
rows.append(R(p, "2-(3-bromopropyl)-3-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 66, "65-67", "Table 1 row 17", "17 49 65-67 methanol", vmin=65, vmax=67))
rows.append(R(p, "bis-N-substituted phthalazine-1,4-dione propane bridge derivative", "melting_point", 146, "145-147", "Table 1 row 18", "18 6.3 145-147 ethanol", vmin=145, vmax=147))
rows.append(R(p, "bis-N-substituted phthalazine-1,4-dione butane bridge derivative", "melting_point", 242, "241-243", "Table 1 row 19", "19 28 241-243 DMF", vmin=241, vmax=243))
rows.append(R(p, "2-(3-chloropropyl)-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 71, "70-72", "Table 1 row 20", "20 65 70-72 acetone", vmin=70, vmax=72))
rows.append(R(p, "2-(3-bromopropyl)-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 63.5, "62-65", "Table 1 row 21", "21 53 62-65 methanol", vmin=62, vmax=65))
rows.append(R(p, "bis-N-substituted pyridazine-3,6-dione propane bridge derivative", "melting_point", 203, "202-204", "Table 1 row 22", "22 7.1 202-204 methanol", vmin=202, vmax=204))
rows.append(R(p, "bis-N-substituted pyridazine-3,6-dione butane bridge derivative", "melting_point", 166, "165-167", "Table 1 row 23", "23 13 165-167 ethanol", vmin=165, vmax=167))
# Target compounds 7a-d, 8a-d, 9a-d - bases and hydrochlorides
rows.append(R(p, "3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one", "melting_point", 120, "119-121", "section 7a", "Base 7a was obtained in 64% yield, m.p. 119-121°C (methanol)", vmin=119, vmax=121))
rows.append(R(p, "3-[3-(4-phenyl-1-piperazinyl)propyl]-quinazolidin-4(3H)-one hydrochloride", "melting_point", 211.5, "210-213", "section 7a", "Hydrochloride m.p. 210-213°C (acetone-methanol 10:1)", vmin=210, vmax=213))
rows.append(R(p, "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one", "melting_point", 102.5, "102-103", "section 7b", "Base 7b was obtained in 71% yield, m.p. 102-103°C (acetone)", vmin=102, vmax=103))
rows.append(R(p, "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-quinazolidin-4(3H)-one hydrochloride", "melting_point", 225.5, "224-227", "section 7b", "Hydrochloride m.p. 224-227°C (acetone-ethanol 10:1)", vmin=224, vmax=227))
rows.append(R(p, "3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one", "melting_point", 140, "139-141", "section 7c", "Base 7c was obtained in 61% yield, m.p. 139-141°C (methanol)", vmin=139, vmax=141))
rows.append(R(p, "3-[4-(4-phenyl-1-piperazinyl)butyl]-quinazolidin-4(3H)-one hydrochloride", "melting_point", 217.5, "216-219", "section 7c", "Hydrochloride m.p. 216-219°C (acetone-ethanol 10:1)", vmin=216, vmax=219))
rows.append(R(p, "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one", "melting_point", 96, "95-97", "section 7d", "Base 7d was obtained in 70% yield, m.p. 95-97°C (acetone)", vmin=95, vmax=97))
rows.append(R(p, "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-quinazolidin-4(3H)-one hydrochloride", "melting_point", 193.5, "192-195", "section 7d", "Hydrochloride: m.p. 192-195°C (2-propanol-acetone 1:1)", vmin=192, vmax=195))
rows.append(R(p, "3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 55, "54-56", "section 8a", "Base 8a was obtained in 69% yield, m.p. 54-56°C (methanol)", vmin=54, vmax=56))
rows.append(R(p, "3-[3-(4-phenyl-1-piperazinyl)propyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride", "melting_point", 216.5, "215-218", "section 8a", "Hydrochloride m.p. 215-218 °C (ethanol)", vmin=215, vmax=218))
rows.append(R(p, "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 129, "128-130", "section 8b", "Base 8b was obtained in 63% yield, m.p. 128-130°C (acetone)", vmin=128, vmax=130))
rows.append(R(p, "3-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride", "melting_point", 227.5, "226-229", "section 8b", "Hydrochloride m.p. 226-229°C (acetone-ethanol 1:3)", vmin=226, vmax=229))
rows.append(R(p, "3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 112, "111-113", "section 8c", "Base 8c was obtained in 73% yield, m.p. 111-113 °C (ethanol)", vmin=111, vmax=113))
rows.append(R(p, "3-[4-(4-phenyl-1-piperazinyl)butyl]-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride", "melting_point", 181, "179-183", "section 8c", "Hydrochloride m.p. 179-183°C (acetone-ethanol 10:1)", vmin=179, vmax=183))
rows.append(R(p, "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione", "melting_point", 155, "154-156", "section 8d", "Base 8d was obtained in 58% yield, m.p. 154-156°C (methanol)", vmin=154, vmax=156))
rows.append(R(p, "3-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-2-phenyl-2,3-dihydrophthalazine-1,4-dione hydrochloride", "melting_point", 208, "207-209", "section 8d", "Hydrochloride m.p. 207-209°C (acetone-ethanol 10:1)", vmin=207, vmax=209))
rows.append(R(p, "2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 98, "97-99", "section 9a", "Base 9a was obtained in 74% yield, m.p. 97-99°C (acetone)", vmin=97, vmax=99))
rows.append(R(p, "2-[3-(4-phenyl-1-piperazinyl)propyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride", "melting_point", 220, "219-221", "section 9a", "Hydrochloride m.p. 219-221°C (acetone-ethanol 10:1)", vmin=219, vmax=221))
rows.append(R(p, "2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 153, "152-154", "section 9b", "Base 9b was obtained in 72% yield, m.p. 152-154°C (methanol)", vmin=152, vmax=154))
rows.append(R(p, "2-{3-[4-(2-pyrimidinyl)-1-piperazinyl]propyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride", "melting_point", 220, "219-221", "section 9b", "Hydrochloride m.p. 219-221°C (acetone-ethanol 10:1)", vmin=219, vmax=221))
rows.append(R(p, "2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 92, "91-93", "section 9c", "Base 9c was obtained in 71% yield, m.p. 91-93°C (methanol-H 2 O 4:1)", vmin=91, vmax=93))
rows.append(R(p, "2-[4-(4-phenyl-1-piperazinyl)butyl]-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride", "melting_point", 200.5, "199-202", "section 9c", "Hydrochloride m.p.199-202°C (methanol)", vmin=199, vmax=202))
rows.append(R(p, "2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione", "melting_point", 105, "104-106", "section 9d", "Base 9d was obtained in 66% yield, m.p. 104-106 °C (acetone)", vmin=104, vmax=106))
rows.append(R(p, "2-{4-[4-(2-pyrimidinyl)-1-piperazinyl]butyl}-1-phenyl-1,2-dihydropyridazine-3,6-dione hydrochloride", "melting_point", 204, "203-205", "section 9d", "Hydrochloride m.p. 203-205 °C (methanol)", vmin=203, vmax=205))

# ===== Paper 093 - PMC6146903 =====
p = "093"
rows.append(R(p, "4,4'-Diacetyldiphenyl sulphide", "melting_point", 91, "90-92", "section compound 2", "Yield: 85%; m.p 90-92°C", vmin=90, vmax=92))
rows.append(R(p, "4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphide", "melting_point", 191, "190-192", "section compound 5", "Yield 74.8%; m.p 190-192°C", vmin=190, vmax=192))
rows.append(R(p, "4,4'-Diacetylsemicarbazone diphenyl sulphide", "decomposition", 300, ">300°C", "section compound 6", "Yield 85.70%; m.p >300°C (decomp.)", rel=">"))
rows.append(R(p, "4-Acetyl-4'-acetylsemicarbazone diphenyl sulphide", "melting_point", 190.5, "190-191", "section compound 7", "m.p 190-191°C, yield 85%", vmin=190, vmax=191))
rows.append(R(p, "4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphide", "decomposition", 300, ">300°C", "section compound 8 Method A", "m.p >300°C (decomp.), yield 75%", rel=">"))
rows.append(R(p, "4-Acetylthiosemicarbazone-4'-acetyldiphenyl sulphone", "melting_point", 185, "185", "section compound 14", "m.p 185°C, yield 80.5%"))
rows.append(R(p, "4-Acetylsemicarbazone-4'-acetyldiphenyl sulphone", "melting_point", 200, "200", "section compound 15", "m.p 200°C, yield 82%"))
rows.append(R(p, "4,4'-Diacetylthiosemicarbazone diphenyl sulphone", "decomposition", 350, ">350°C", "section compound 16", "m.p >350 (decomp.), yield 65%", rel=">"))
rows.append(R(p, "4,4'-Diacetylsemicarbazone diphenyl sulphone", "decomposition", 350, ">350°C", "section compound 17", "m.p >350°C (decomp.), yield 65%", rel=">"))
rows.append(R(p, "4-Acetylthiosemicarbazone-4'-acetylsemicarbazone diphenyl sulphone", "decomposition", 350, ">350°C", "section compound 18 Method A", "m.p >350°C (decomp.), yield 77%", rel=">"))
# Table II
rows.append(R(p, "4-(4\"-phenyl-Delta3-thiazoline-2\"-acetylazino)-4'-acetyldiphenyl sulphide", "decomposition", 160, "160", "Table II row 9", "9 160°C, decomp. EtOH/H 2 O (1:1) 54"))
rows.append(R(p, "4-(5\"-carboxyethyl-4\"-thiazolidinone-2\"-acetylazino)-4'-acetyldiphenyl sulphide", "decomposition", 260, "260", "Table II row 10", "10 260°C, decomp.EtOH/H 2 O (1:1) 53"))
rows.append(R(p, "4-(4\"-thiazolidinone-2\"-acetylazino)-4'-acetyldiphenyl sulphide", "melting_point", 160, "160", "Table II row 11", "11 160°C EtOH 53"))
rows.append(R(p, "4-(4\"-methyl-Delta3-thiazoline-2\"-acetylazino)-4'-acetyldiphenyl sulphide", "melting_point", 120, "120", "Table II row 12", "12 120°C, EtOH 52.5"))
rows.append(R(p, "4-(4\"-phenyl-Delta3-thiazoline-2\"-acetylazino)-4'-acetyldiphenyl sulphone", "melting_point", 300, ">300°C", "Table II row 19", "19 >300°C AcOH 62", rel=">"))
rows.append(R(p, "4-(5\"-carboxyethyl-4\"-thiazolidinone-2\"-acetylazino)-4'-acetyldiphenyl sulphone", "melting_point", 300, ">300°C", "Table II row 20", "20 >300°C AcOH 65", rel=">"))
rows.append(R(p, "4-(4\"-thiazolidinone-2\"-acetylazino)-4'-acetyldiphenyl sulphone", "melting_point", 300, ">300°C", "Table II row 21", "21 >300°C AcOH 61.5", rel=">"))
rows.append(R(p, "4-(4\"-methyl-Delta3-thiazoline-2\"-acetylazino)-4'-acetyldiphenyl sulphone", "melting_point", 300, ">300°C", "Table II row 22", "22 >300°C AcOH 60", rel=">"))
rows.append(R(p, "4-(4\"-phenyl-Delta3-thiazoline-2\"-acetylazino)-4'-acetylthiosemicarbazone diphenyl sulphide", "melting_point", 300, "300", "Table II row 23", "23 300°C, EtOH/H 2 O (1:1) 70"))
rows.append(R(p, "4-(5\"-carboxyethyl-4\"-thiazolidinone-2\"-acetylazino)-4'-acetylthiosemicarbazone diphenyl sulphide", "melting_point", 300, "300", "Table II row 24", "24 300°C EtOH 75"))
rows.append(R(p, "4-(4\"-carboxyethyl-4\"-thiazolidinone-2\"-acetylazino)-4'-acetylthiosemicarbazone diphenyl sulphide", "melting_point", 300, "300", "Table II row 25", "25 300°C EtOH 73"))
rows.append(R(p, "4-(4\"-thiazolidinone-2\"-acetylazino)-4'-acetylthiosemicarbazone diphenyl sulphide", "melting_point", 300, "300", "Table II row 26", "26 300°C EtOH-water (1:1) 71"))

# ===== Paper 094 - PMC6146461 =====
p = "094"
rows.append(R(p, "3-Allyl-6-(allylamino)-2-phenyl-3,4-dihydro-1,3,5-benzotriazocin-4-thione", "melting_point", 153.5, "153-154", "section compound 7", "0.18g (38%); M.p. 153-154 o C", vmin=153, vmax=154))
rows.append(R(p, "2-Phenyl-4H-3,1-benzothiazin-4-imine", "melting_point", 216.5, "216-217", "section compound 8", "0.25 g (78%); M.p. 216-217 o C", vmin=216, vmax=217))
rows.append(R(p, "2-Phenyl-3,4-dihydroquinazolin-4-thione", "melting_point", 162.5, "162-163", "section compound 9", "0.17g (53%); M.p.162-163 o C", vmin=162, vmax=163))
rows.append(R(p, "2,3-Diphenyl-3,4-dihydroquinazolin-4-imine", "melting_point", 214.5, "214-215", "section compound 10a", "0.26g (62%); M.p. 214-215 o C", vmin=214, vmax=215))
rows.append(R(p, "3-(4-Methylphenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine", "melting_point", 207.5, "207-208", "section compound 10b", "0.21g (48%); M.p.207-208 o C", vmin=207, vmax=208))
rows.append(R(p, "3-(4-Chlorophenyl)-2-phenyl-3,4-dihydroquinazolin-4-imine", "melting_point", 183.5, "183-184", "section compound 10c", "0.27g (57%); M.p. 183-184 o C", vmin=183, vmax=184))
rows.append(R(p, "3-Benzyl-6-imino-2-phenyl-3,4,5,6-tetrahydro-1,3,5-benzotriazocin-4-thione", "melting_point", 170.5, "170-171", "section compound 11", "0.19g (38%);M.p. 170-171 o C", vmin=170, vmax=171))

# ===== Paper 095 - PMC6236356 =====
p = "095"
rows.append(R(p, "Methyl N-[phenylsulphonyl-glycyl]anthranilate", "melting_point", 125, "125", "section compound 2a", "as colourless crystals (65%), m.p. 125°C"))
rows.append(R(p, "Methyl N-[4'-methylphenylsulphonyl-2-phenylglycyl]anthranilate", "melting_point", 155, "155", "section compound 2b", "as colourless crystals (71%) , m.p. 155°C"))
rows.append(R(p, "Methyl N-[4'-methylphenylsulphonyl-phenylalaninyl]anthranilate", "melting_point", 120, "120", "section compound 2c", "as colourless crystals (68%), m.p. 120°C"))
rows.append(R(p, "Methyl N-[4'-methylphenylsulphonyl-beta-alaninyl]anthranilate", "melting_point", 130, "130", "section compound 2d", "as colourless crystals (73%), m.p. 130°C"))
rows.append(R(p, "Methyl N-[4'-methylphenylsulphonyl-DL-valinyl]anthranilate", "melting_point", 170, "170", "section compound 2e", "as colourless crystals (75%), m.p. 170°C"))
rows.append(R(p, "Methyl N-[4'-methylphenylsulphonyl-DL-leucinyl]anthranilate", "melting_point", 165, "165", "section compound 2f", "as colourless crystals (68%), m.p. 165°C"))
rows.append(R(p, "3-Amino-2-(phenylsulphonamidomethyl)quinazolin-4(3H)-one", "melting_point", 180, "180", "section compound 3a", "Colourless crystals (74%); m.p. 180°C"))
rows.append(R(p, "3-Amino-2-[1`(4-methylphenylsulphonyl)-1`-(phenyl)methyl]quinazolin-4(3H)-one", "melting_point", 135, "135", "section compound 3b", "Colourless crystals (65%), m.p. 135°C"))
rows.append(R(p, "3-Amino-2-[1`(4-methyl phenylsulphonamido)-1`-(benzyl)methyl]quinazoline-4-(3H)-one", "melting_point", 170, "170", "section compound 3c", "Colourless crystals (68%), m.p. 170°C"))
rows.append(R(p, "3-Amino-2-[4-methyl phenylsulphonamidoethyl]quinazolin-4-(3H)-one", "melting_point", 185, "185", "section compound 3d", "Colourless crystals (70%), m.p. 185°C"))
rows.append(R(p, "3-Amino-2-[1`-(4-methylphenylsulphonamido)-1`-(iso-propyl)methyl]quinazolin-4-(3H)-one", "melting_point", 190, "190", "section compound 3e", "Colourless crystals (76%), m.p. 190°C"))
rows.append(R(p, "3-Amino-2-[1`-(4-methylphenylsulphonamido)-1`-(iso-butyl)methyl]quinazolin-4-(3H)-one", "melting_point", 170, "170", "section compound 3f", "Colourless crystals (71%), m.p. 170°C"))
rows.append(R(p, "Schiff's base of 3-amino-2-[1`-(4-methyl phenyl sulphonamido)-1`-(iso-propyl)methyl]quinazolin-4-(3H)-one", "melting_point", 160, "160", "section compound 4", "as pale brown crystals (69%); m.p. 160°C"))
rows.append(R(p, "2-(4-Chlorophenyl)-4,5,11-trihydro-1H[1,2,4]triazepino[7,1-b]quinazolin-11-one", "melting_point", 260, "260", "section compound 5a", "as brown crystals (67%), m.p. 260°C"))
rows.append(R(p, "2-(4-Fluorophenyl)-4-isopropyl-4,10-dihydro-1H[1,2,4]triazino[6,1-b]-quinazolin-10-one", "melting_point", 180, "180", "section compound 5b", "as pale brown crystals (62%), m.p. 180°C"))
rows.append(R(p, "2-(4-Methoxyphenyl)-4-isopropyl-4,10-dihydro-1H-[1,2,4]triazino[6,1-b]quinazolin-10-one", "melting_point", 170, "170", "section compound 5c", "as brown crystals (60%), m.p. 170°C", notes="paper text has typo missing closing paren after Methoxyphenyl - corrected for IUPAC validity"))
rows.append(R(p, "6,7,9,14,17-Pentahydronaphtho[2`,3`:3,4][1,2,5]triazocino[8,1-b]qinozolin-9,14,17-trione", "melting_point", 300, ">300°C", "section compound 6a", "as deep brown crystals (63%), m.p. > 300°C", rel=">"))
rows.append(R(p, "6-Isopropyl-6,8,13,16-tetrahydronaphtho[2`,3`:3,4][1,2,5]triazepino[7,1-b]-quinazolin-8,13,16 trione", "melting_point", 300, ">300°C", "section compound 6b", "as dark brown crystals (60%); m.p. > 300°C", rel=">"))
rows.append(R(p, "2-[11-Oxo5,11-dihydro-1H-[1,2,4]triazepino[7,1-b]quinazolin-2-ylidine]-malononitrile", "melting_point", 250, "250", "section compound 7", "as yellow crystals (61%); m.p. 250°C"))
rows.append(R(p, "2-(4-isopropyl-10-oxo-1,10-dihydro-[1,2,4]-triazino-[6,1-b]quinazolin-2-ylidine)malononitrile", "melting_point", 300, ">300°C", "section compound 8", "as pale yellow crystals (66%), m.p. > 300°C", rel=">", notes="paper text has typo: '2[' instead of '2(' - corrected for IUPAC validity"))
rows.append(R(p, "Ethyl 1-[11-oxo-5,11-dihydro-[1,2,4]triazepino[7,1-b]quinazolinyl]formate", "melting_point", 265, "265", "section compound 9", "as pale brown crystals (60%), m.p. 265°C"))
rows.append(R(p, "Ethyl-1-[12-oxo-6,12-dihydro[1,2,5]triazocino[8,1-b]quinazolinyl]acetate", "melting_point", 300, ">300°C", "section compound 10", "as pale brown crystals (63%), m.p. > 300°C", rel=">"))

# ===== Paper 096 - PMC6236427 =====
p = "096"
rows.append(R(p, "16-hydroxy-1,2-dehydrovincadifformine", "melting_point", 109.5, "109-110", "section compound 3", "the second fraction contained 16-hydroxy-1,2-dehydrovinca-difformine ( 3 ) (151 mg, 30%) as an orange solid, m.p. 109-110°C", vmin=109, vmax=110))
rows.append(R(p, "16-hydroxy-1,2-dehydrovincadifformine-Nb-oxide", "decomposition", 177, "176-178 °C", "section compound 4", "colourless prisms, m.p. 176-78 °C (dec.)", vmin=176, vmax=178, notes="paper writes '176-78' meaning 176-178; expanded for unit-arithmetic check"))
rows.append(R(p, "vincadifformine-Nb-oxide", "decomposition", 160, "160", "section compound 4 less polar fraction", "m.p. 160°C (dec.)"))
rows.append(R(p, "16-Oxoaspidospermidine", "melting_point", 110, "108-112", "section compound 5b", "m.p. 108-112 °C", vmin=108, vmax=112))
rows.append(R(p, "16-beta-hydroxyaspidospermidine", "melting_point", 55, "55", "section compound 6a", "colouress plates of 16β-hydroxyaspidospermidine ( 6a ) (1.24 g, 72.5%), m.p. 55°C"))
rows.append(R(p, "Na-Formyl-16-beta-formyloxyaspidospermidine", "melting_point", 71, "70-72 °C", "section compound 7a", "Na -formyl-16β-formyloxyaspidospermidine 7a (130 mg, 90.1 %) as colourless plates, m.p. 70-2 °C", vmin=70, vmax=72, notes="paper writes '70-2' meaning 70-72; expanded for unit-arithmetic check"))
rows.append(R(p, "Na-Formyl-16-beta-hydroxyaspidospermidine", "melting_point", 67, "66-68", "section compound 1a", "Na - formyl-16β-hydroxyaspidospermidine ( 1a ) (68.5 mg, 98 %) as colouress plates, m.p. 66-68 °C", vmin=66, vmax=68))
rows.append(R(p, "(±)-vincadifformine", "melting_point", 125, "125", "section compound 2", "(°) vincadifformine (5.83 g, 81.2 %), which was recrystallised from acetonitrile and obtained as colouress prisms; m. p. 125 °C (lit.[4], 124-25 °C)"))
# Boiling points
rows.append(R(p, "5-chloro-2-ethylpentanal", "boiling_point", 100, "100 °C", "section synthesis of chloroaldehyde", "5-chloro-2-ethylpentanal (11.49 g, 77.4-89%) as a colouress oil, b.p. 100°C/0.5 mmHg", notes="b.p. at 0.5 mmHg reduced pressure"))
rows.append(R(p, "aldimine (N-cyclohexylbutylidene amine)", "boiling_point", 82, "80-84", "section preparation of aldimine", "the desired aldimine (65 g, 68%) as a colorless liquid, b.p. 80-84 °C / 20 mm Hg", vmin=80, vmax=84, notes="b.p. at 20 mm Hg"))

# ===== Paper 097 - PMC6146420 =====
p = "097"
rows.append(R(p, "1-methyl-6-phenyl-5,6-dihydropyridin-2(1H)-one", "melting_point", 135.5, "135-136 °C", "Table 1 col 4a", "Compound 4a 4b 4c trans -4d trans -4e trans -4f trans -4g m.p. °C 135-6", vmin=135, vmax=136, notes="sublimes in sealed capillary; paper writes '135-6' meaning 135-136"))
rows.append(R(p, "1,6-diphenyl-5,6-dihydropyridin-2(1H)-one", "decomposition", 210, ">210 °C", "Table 1 col 4b", "m.p. °C 135-6 1) >210 decom 147-8", rel=">", notes="decomposes; unstable in air"))
rows.append(R(p, "5,5-dimethyl-6-(trichloromethyl)-5,6-dihydropyridin-2(1H)-one", "melting_point", 147.5, "147-148 °C", "Table 1 col 4c", "m.p. °C 135-6 1) >210 decom 147-8 1) 176-7", vmin=147, vmax=148, notes="sublimes in sealed capillary; paper writes '147-8'"))
rows.append(R(p, "trans-1-methyl-4a,5,6,7,8,8a-hexahydroquinolin-2(1H)-one", "melting_point", 176.5, "176-177 °C", "Table 1 col trans-4d", "147-8 1) 176-7 1) 183-4", vmin=176, vmax=177, notes="sublimes in sealed capillary; paper writes '176-7'"))
rows.append(R(p, "trans-1-phenyl-1,5,6,7,8,8a-hexahydroisoquinolin-3(2H)-one", "melting_point", 183.5, "183-184 °C", "Table 1 col trans-4e", "176-7 1) 183-4 1) Oil 172-3", vmin=183, vmax=184, notes="sublimes in sealed capillary; paper writes '183-4'"))
rows.append(R(p, "trans-1-(trichloromethyl)-1,5,6,7,8,8a-hexahydroisoquinolin-3(2H)-one", "melting_point", 172.5, "172-173 °C", "Table 1 col trans-4g", "183-4 1) Oil 172-3 1)", vmin=172, vmax=173, notes="sublimes in sealed capillary; paper writes '172-3'"))
# Intermediate 1 series
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide 1a", "melting_point", 90.5, "90-91", "Experimental section", "N-(3-Oxoalkyl)amides 1a (56%, m.p. 90-91°C)", vmin=90, vmax=91, notes="precursor; specific structure per Scheme 1 with R1=Me, R4=Ph"))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide 1b", "melting_point", 104.5, "104-105", "Experimental section", "1b ( 81 %, m.p. 104-105°C)", vmin=104, vmax=105, notes="R1=R4=Ph"))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide anti-1e", "melting_point", 156.5, "156-157", "Experimental section", "anti - 1e (14%, m.p.156-157°C)", vmin=156, vmax=157))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide 1c", "melting_point", 109.5, "109-110", "Experimental section", "1c ( 69%, m.p. 109-110°C)", vmin=109, vmax=110))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide anti-1g", "melting_point", 74.5, "74-75", "Experimental section", "anti - 1g (55%, m.p. 74-75°C)", vmin=74, vmax=75))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide anti-1d", "melting_point", 124.5, "124-125", "Experimental section", "anti - 1d (88%, m.p.124-125°C)", vmin=124, vmax=125))
rows.append(R(p, "N-(3-oxoalkyl)chloroacetamide 1f", "melting_point", 201.5, "201-202", "Experimental section", "1f (19%, m.p. 201-202°C)", vmin=201, vmax=202))
# Phosphonium salts
rows.append(R(p, "triphenylphosphonium salt 2a", "melting_point", 191.5, "191-192", "Experimental section", "2a - 74%, 191-192°C", vmin=191, vmax=192, notes="triphenylphosphonium salt derivative"))
rows.append(R(p, "triphenylphosphonium salt 2b", "melting_point", 119.5, "119-120", "Experimental section", "2b - 93%, 119-120°C", vmin=119, vmax=120))
rows.append(R(p, "triphenylphosphonium salt 2c", "melting_point", 204, "203-205", "Experimental section", "2c - 78%, 203-205°C", vmin=203, vmax=205))
rows.append(R(p, "triphenylphosphonium salt anti-2d", "melting_point", 187.5, "187-188", "Experimental section", "anti - 2d - 93%, 187-188°C", vmin=187, vmax=188))
rows.append(R(p, "triphenylphosphonium salt anti-2e", "melting_point", 200.5, "200-201", "Experimental section", "anti - 2e - 83%, 200-201°C", vmin=200, vmax=201))
rows.append(R(p, "triphenylphosphonium salt anti-2f", "melting_point", 160.5, "160-161", "Experimental section", "anti -2f - 78%, 160-161°C", vmin=160, vmax=161))

# ===== Paper 098 - PMC6146883 =====
p = "098"
rows.append(R(p, "1-(3-Coumarinyl)-3-dimethylamino-2-propen-1-one", "melting_point", 165, "165", "Table 1 row 1", "1 360 5 75 96 165 165"))
rows.append(R(p, "1-(3-Benzocoumarinyl)-3-dimethylamino-2-propen-1-one", "melting_point", 157, "157", "section compound 2 / Table 1", "Compound 2 was obtained as orange crystals (Method A: 85%; Method B: 95%), mp 157°C"))
rows.append(R(p, "3,7-Bis-(2-hydroxyphenyl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione", "melting_point", 245, "245", "section compound 7", "Compound 7 was obtained as dark yellow crystals (85%), mp 245°C"))
rows.append(R(p, "2-(Benzocoumarin-3'-yl)-5-(3-benzocoumarinoyl)pyridine", "melting_point", 220, "220", "section compound 8", "8 as buff crystals (64%), mp 220°C"))
rows.append(R(p, "3,7-Bis-(3-hydroxynaphthalen-4-yl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione", "melting_point", 200, "200", "section compound 10", "Compound 10 was obtained as buff crystals (96%), mp 200°C"))
rows.append(R(p, "1-Acetyl-3,5-di(3-coumarinoyl)benzene", "melting_point", 178, "178", "section compound 12", "Compound 12 was obtained as buff crystals (66%), mp 178°C"))
rows.append(R(p, "1-Acetyl-3,5-di(3-benzocoumarinoyl)benzene", "melting_point", 300, ">300°C", "section compound 15", "Compound 15 was obtained as buff crystals (49%), mp >300°C", rel=">"))
rows.append(R(p, "1,3-Diacetyl-5-(3-benzocoumarinoyl)benzene", "melting_point", 300, ">300°C", "section compound 16", "Compound 16 was obtained as buff crystals (45%), mp >300°C", rel=">"))
rows.append(R(p, "5-(3-Coumarinoyl)-2-methylpyridine", "melting_point", 200, "200", "section compound 17", "Compound 17 was obtained as brown crystals (45%), mp 200°C"))
rows.append(R(p, "5-(Coumarin-3'-yl)-1,2,4-triazolo[4,3-a]pyrimidine", "melting_point", 252, "252", "section compound 18", "Compound 18 was obtained as pale brown crystals (65%), mp 252°C"))
rows.append(R(p, "5-(Benzocoumarin-3'-yl)-[1,2,4]triazolo-[4,3-a] pyrimidine", "melting_point", 273, "273", "section compound 22", "Compound 22 was obtained as yellow crystals (74%), mp 273 °C"))
rows.append(R(p, "2-[3-Oxo-3-(2-oxo-2H-chromen-3-yl)-propenylamino]-4,5,6,7-tetrahydrobenzo[b]thiophene-3-carboxylic acid ethyl ester", "melting_point", 202, "202", "section compound 19", "Compound 19 was obtained as light red crystals (45%) mp 202°C"))
rows.append(R(p, "3-(Coumarin-3'-yl)-pyrazole", "melting_point", 235, "235", "section compound 20", "Compound 20 was obtained as light brown crystals (60%), mp 235°C"))
rows.append(R(p, "2-Amino-4-(coumarin-3'-yl)pyrimidine", "melting_point", 194, "194", "section compound 21", "Compound 21 was obtained as dark yellow crystals (45%), mp 194°C"))
rows.append(R(p, "3-(Benzocumarin-3'-yl)-pyrazole", "melting_point", 256, "256", "section compound 25/23 in text", "Compound 25 was obtained as yellow crystals (65%), mp 256°C", notes="quote uses paper's own labeling"))
rows.append(R(p, "3-(Benzocumarin-3'-yl)-1-phenylpyrazole", "melting_point", 230, "230", "section compound 24", "Compound 24 was obtained as dark yellow crystals (59%), mp 230°C"))
rows.append(R(p, "3-Benzamido-6-(benzocoumarin-3'-yl)pyran-2-one", "melting_point", 254, "254", "section compound 26", "Compound 26 was obtained as red crystals (60%), mp 254 °C"))
rows.append(R(p, "3-(Benzocoumarin-3'-yl)-2-cyano-5-dimethylamino-2,4-pentadienoic amide", "melting_point", 250, "250", "section compound 27", "Compound 27 was obtained as dark red crystals (45%), mp 250 °C"))
rows.append(R(p, "6-Benzoyl-3-(coumarin-3'-yl)isoxazole", "melting_point", 165, "165", "section compound 28", "Compound 28 was obtained as dark yellow crystals (41%), mp 165°C"))
rows.append(R(p, "6-Benzoyl-3-(benzocoumarin-3'-yl)isoxazole", "melting_point", 190, "190", "section compound 31", "Compound 31 was obtained as yellowish green crystals (45%), mp 190°C"))
rows.append(R(p, "3-Acetyl-4-(benzocoumarin-3'-yl)-1-phenylpyrazole", "melting_point", 228, "228", "section compound 33", "Compound 33 was obtained as dark yellow crystals (43%), mp 228 °C"))
rows.append(R(p, "4-(Coumarin-3'-yl)-7-phenylisoxazolo[3,4-d]pyridazine", "melting_point", 245, "245", "section compound 30", "Compound 30 was obtained as dark yellow crystals (71%), mp 245 °C"))
rows.append(R(p, "4-(Benzocoumarin-3'-yl)-7-phenylisoxazolo[3,4-d]pyridazine", "melting_point", 189, "189", "section compound 32", "Compound 32 was obtained as yellow crystals (74%), mp 189 °C"))
rows.append(R(p, "4-(Benzocoumarin-3'-yl)-7-methyl-2-phenyl-pyrazolo[3,4-d]pyridazine", "melting_point", 230, "230", "section compound 34", "Compound 34 was obtained as orange crystals (73%), mp 230°C"))

# ===== Paper 099 - PMC6236343 =====
p = "099"
rows.append(R(p, "9-(Acetoxymethylidene)-1,4-dihydro-1,4-methanonaphthalene", "melting_point", 78.5, "78-79", "section compound 3", "the title product as pale yellow crystals (38 g, 45%), m.p. 78-79 °C", vmin=78, vmax=79))
rows.append(R(p, "2,4-dinitrophenylhydrazone of syn-9-formyl-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 177.5, "177-178", "section compound 4 derivative", "bright yellow crystals, m.p. 177-178 °C", vmin=177, vmax=178))
rows.append(R(p, "3,5-dinitrobenzoyl derivative of syn-9-(hydroxymethyl)-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 138.5, "137-140", "section compound 6 derivative", "pale yellow crystals, m.p. 137-140 °C", vmin=137, vmax=140))
rows.append(R(p, "anti-9-(hydroxymethyl)-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 50.75, "50-51.5", "section compound 9", "white needles (0.15 g, 25%) m.p. 50-51.5 °C", vmin=50, vmax=51.5))
rows.append(R(p, "syn-9-(tosyloxymethyl)-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 107, "106-108", "section compound 7", "large, colourless prisms (0.25g, 33%) m.p. 106-108 °C", vmin=106, vmax=108))
rows.append(R(p, "anti-9-(tosyloxymethyl)-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 105, "105-105", "section compound 10", "colourless needles (0.15 g, 20%) m.p. 105-105 °C", notes="value range collapsed to single point"))
rows.append(R(p, "tosylhydrazone of 9-formyl-tricyclo[6.2.1.0^2,7]undeca-2,4,6,9-tetraene", "melting_point", 134.5, "134-135", "section tosylhydrazone of 4", "colourless needles (0.6 g, 61%) m.p. 134-135 °C", vmin=134, vmax=135))
rows.append(R(p, "tetramethyl dodecacyclopentatriacontane-tetracarboxylate diol (compound 12)", "melting_point", 222, "221-223", "section compound 12", "12 as a colourless solid (156 mg, 64%), m.p. 221-223 °C", vmin=221, vmax=223, notes="full IUPAC name in paper title - shortened here for readability"))
rows.append(R(p, "tetramethyl dodecacyclopentatriacontane-tetracarboxylate diacetate (compound 13)", "melting_point", 246, "245-247", "section compound 13", "as a colourless solid; yield: 72 mg, (93 %), mp 245-247 °C", vmin=245, vmax=247))

# ===== Paper 102 - PMC6236359 =====
p = "102"
rows.append(R(p, "2,2'-Diaminobenzophenone", "melting_point", 134, "134", "section compound 4a", "to afford 4a (195 mg, quantitative yield), yellow crystals (from 80% aqueous methanol), m.p. 134°C"))
rows.append(R(p, "2,2'-Diamino-4,4'-dimethoxybenzophenone", "melting_point", 138, "138", "section compound 4b", "afford 4b (185 mg, 90%): m.p. 138°C"))
rows.append(R(p, "3(N)-(2,2'-diaminobenzophenone)-1,4-naphthoquinone", "melting_point", 208, "208", "section compound 5a", "afford 5a (420 mg, 54%), red prisms (from EtOH), m.p. 208°C"))
rows.append(R(p, "3(N)-(2,2'-diamino-4,4'-dimethoxybenzophenone)-1,4-naphthoquinone", "melting_point", 214, "214", "section compound 5b", "compound 5b was isolated (150 mg, 48%): red prisms (from EtOH), m.p. 214°C"))
rows.append(R(p, "10H-benzo[i]quino[2,3,4-kl]acridin-10-one", "melting_point", 255, "255", "section compound 6a", "to afford 6a (335 mg, 93%), amorphous powder (CHCl 3 /MeOH, 9:1), m.p. 255°C"))
rows.append(R(p, "2,7-Dimethoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one", "melting_point", 296, "296", "section compound 6b", "amorphous powder (CHCl 3 /MeOH, 8:2), m.p. 296°C"))
rows.append(R(p, "9H-benzo[i]pyrido[2,3,4-kl]acridin-9-one (deaza-ascididemin)", "melting_point", 258, "258", "section compound 8", "to afford 8 (70mg, 13%), amorphous powder (chloroform/methanol, 9:1), mp 258°C"))
rows.append(R(p, "3(N)-(2,2'-diaminobenzophenone)-5-hydroxy-1,4-naphthoquinone", "melting_point", 221, "221", "section compound 9", "red prisms (from EtOH), m.p. 221°C"))
rows.append(R(p, "11-Hydroxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one", "melting_point", 292, "292", "section compound 10", "to afford 10 (61 mg, 98%), yellow needles (CHCl 3 -MeOH 50:1), m.p. 292°C"))
rows.append(R(p, "11-Acetoxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one", "melting_point", 222, "222", "section compound 11", "to give 11 (11 mg, 95%), yellow needles (CHCl 3 /MeOH, 100:1), m.p. 222oC"))
rows.append(R(p, "11-hydroxy-10-imino-10H-benzo[i]quino[2,3,4-kl]acridine", "melting_point", 266, "266", "section compound 12", "to afford 12 (7 mg, 70%), dark-green needles (CHCl 3 /MeOH, 20:1), m.p. 266 C", notes="compound 12 in paper - quinoneimine derivative"))
rows.append(R(p, "p-anisidinyl-juglone adduct (compound 14)", "melting_point", 211, "211", "section compound 14", "red crystals (ethanol), m.p. 211°C"))
rows.append(R(p, "10H,11H,12H-dihydroquino[2,3,4-kl]acridine", "melting_point", 186, "186", "section compound 17a", "afford 17a (515 mg, quantitative), amorphous powder (CHCl /MeOH, 20:1), m.p. 186°C"))
rows.append(R(p, "2,7-Dimethoxy-10H,11H,12H-dihydroquino[2,3,4-kl]acridine", "melting_point", 218, "218", "section compound 17b", "afforded 17b (625mg, quantitative), amorphous powder (CHCl 3 /MeOH, 20:1), mp 218°C"))
rows.append(R(p, "3-Nitro-10H-benzo[i]quino[2,3,4-kl]acridin-10-one", "melting_point", 339, "339", "section compound 20", "afforded 20 (48 mg, 53%), yellow needles, m.p. 339°C"))
rows.append(R(p, "10H-quino[2,3,4-kl]acridin-10-one", "melting_point", 254, "254", "section compound 24", "afford 24 (290 mg, 92%), amorphous powder (CHCl 3 /MeOH, 20:1), m.p. 254°C"))
rows.append(R(p, "2,7-Dimethoxy-10H-quino[2,3,4-kl]acridin-10-one", "melting_point", 291, "291", "section compound 25", "afforded 25 (340 mg, 90%), amorphous powder (CHCl 3 /MeOH, 20:1), m.p. 291°C"))

# ===== Paper 103 - PMC6146533 =====
p = "103"
rows.append(R(p, "compound 2 from ethyl cyanoacetate (pyrido-thienopyrimidine)", "melting_point", 200, "200", "section compound 2", "Compound 2 (from ethyl cyanoacetate) was recrystallized from ethanol as yellow needles; m. p. 200 o C", notes="paper does not give full IUPAC; identified as condensation product of compound 1 with ethyl cyanoacetate; flagged for compound name clarity"))
rows.append(R(p, "alpha,beta-unsaturated nitrile from benzaldehyde condensation (compound 5)", "melting_point", 243, "243", "section compound 5", "as white crystals; m.p. 243 o C"))
rows.append(R(p, "9-Amino-7-oxo-6-phenyl-4-phenylmethanimido-6,7-dihydropyrido[3',2':4,5]thieno[3,2-d]-pyrimidin-8-carbonitrile", "melting_point", 220, "220", "section compound 6", "as white crystals; m.p. 220 o C"))
rows.append(R(p, "7-Amino-9-oxo-10-phenyl-9,10-dihydropyrido[3',2':4,5]thieno[3,2-d][1,2,4]triazolo-[3,2-f]-pyrimidin-8-carbonitrile", "melting_point", 236, "236", "section compound 10", "as yellow crystals; m.p. 236 o C"))
rows.append(R(p, "9-Amino-4-chloro-7-oxo-6-phenyl-6,7-dihydropyrido-[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbonitrile", "melting_point", 159, "158-160", "section compound 12", "as yellow crystals; m.p. 158-160 o C", vmin=158, vmax=160))
rows.append(R(p, "Ethyl N-(2,4-dicyano-5-phenylamino-3-yl)metanimidate", "melting_point", 215, "215", "section compound 7", "as white crystals; m.p. 215 o C", notes="paper has typo metanimidate"))
rows.append(R(p, "3-Amino-3,4-dihydro-4-imino-6-phenylamino thienopyrimidine derivative (compound 8)", "melting_point", 185, "185", "section compound 8", "as white crystals; m.p. 185 o C", notes="compound name truncated in paper"))
rows.append(R(p, "8-Phenylaminothieno[3,2-d][1,2,4]triazolo[3,2-f]pyrimidin-7-carbonitrile", "melting_point", 299, "299", "section compound 9", "as white needles; m.p. 299 o C"))
rows.append(R(p, "4-Chloro-6-phenylamino-thieno[3,2-d]-1,2,3-triazin derivative (compound 11)", "melting_point", 201, "201", "section compound 11", "as white needles; m.p. 201 o C", notes="compound 11 chloro-triazin derivative; full name truncated in paper text"))
rows.append(R(p, "9-Amino-4-hydrazino-7-oxo-6-phenyl-6,7-dihydropyrido-[3',2':4,5]thieno[3,2-d][1,2,3]triazin-8-carbonitrile", "melting_point", 262, "262", "section compound 13", "as white crystals; m.p. 262 o C"))
rows.append(R(p, "3-Amino-2,4-di(4,5-dihydro-1H-2-imidazolyl) thiophene derivative (compound 14)", "melting_point", 197, "197", "section compound 14", "to give golden yellow crystals; m.p. 197 o C", notes="full name partially given in paper as 3-Amino-2,4-di(4,5-dihydro-1H-2-imidazolyl)"))
rows.append(R(p, "5,6,12-Triphenyl-2,3,5,6,9,10-hexahydroimidazo[1,2-c]imidazo[2\",1':6',1']pyrimido[4',5':4,5]-thieno-[3,2-e]pyrimidine", "melting_point", 215, "215", "section compound 15", "as white needles; m.p. 215 o C"))
rows.append(R(p, "5-Ethoxy-6-phenyl-2,3,5,6,9,10-hexahydroimidazo[1,2-c]imidazo[2\",1':6',1']pyrimido[4',5':4,5]-thieno[3,2-e]pyrimidine", "melting_point", 163, "163", "section compound 16", "as pale yellow crystals; m.p. 163 o C"))
rows.append(R(p, "compound 17a (12-(1,1-dicyanomethylidene)thieno-pyrimidine)", "melting_point", 172, "172", "section compound 17a", "Compound 17a : gray crystals; m.p. 172 o C (from dioxane)", notes="full IUPAC truncated in paper; thieno-pyrimidine with dicyanomethylidene moiety"))
rows.append(R(p, "compound 17b acetyl thieno-pyrimidine derivative", "melting_point", 179, "179", "section compound 17b", "Compound 17b : orange crystals; m.p.179 o C (from methanol)", notes="full IUPAC truncated in paper"))
rows.append(R(p, "7-(4,5-Dihydro-1H-2-imidazolyl) compound from diazotization (compound 18 or similar)", "melting_point", 269, "269", "section diazotization product", "white needles; m.p. 269 o C", notes="compound name truncated; likely diazonium-derived azo compound per context"))

# ===== Paper 104 - PMC6146923 =====
p = "104"
rows.append(R(p, "Meso-5,5,7,12,12,14-hexamethyl-1,4,8,11-tetraazacyclotetradecane-1,8-di-(1-methylnaphthalene)", "melting_point", 258.5, "257-260", "Experimental section", "yield 6.75 g (81.4 %). M.P. 257 - 260 ° C", vmin=257, vmax=260))

# ===== Paper 105 - PMC6236431 =====
p = "105"
rows.append(R(p, "4-Amino-3-phenyl-1H-1,2,4-triazole", "melting_point", 87, "86-88", "section compound 36", "63.3 g (79%) of 36 as white needle shaped crystals, (m.p. 86-88 °C)", vmin=86, vmax=88))
rows.append(R(p, "3-Phenyl-1H-1,2,4-triazole", "melting_point", 116, "115-117", "section compound 18", "as a white powder with melting point 115-117 °C (Lit. 119 °C [ 8 ])", vmin=115, vmax=117))
rows.append(R(p, "4-(trans-2-butenyl)-5-methyl-3-phenyl-4H-1,2,4-triazole", "melting_point", 103.5, "103-104", "section compound 7", "0.98 g (48%) of pure 7 as colorless crystals. Mp. 103-104 °C", vmin=103, vmax=104))

# ===== Paper 106 - PMC6236365 =====
p = "106"
rows.append(R(p, "isatogen rearrangement product (compound 6)", "melting_point", 207, "206-208", "section compound 6", "compounds 1 (5.57 g, 48 %) and 6 (2.32 g, 20 %); m.p. 206-208°C (hexane/ethyl acetate)", vmin=206, vmax=208, notes="compound name truncated in paper; product of o-nitrobenzaldehyde Hantzsch rearrangement"))
rows.append(R(p, "indole carboxylate rearrangement product 7", "melting_point", 159, "158-160", "section compound 7", "7 (4.90 g, 20%), m.p. 158-160 °C", vmin=158, vmax=160, notes="full IUPAC name not given near m.p."))
rows.append(R(p, "3-(2-oxopropyl)-1H-indole-2-carboxylic acid ethyl ester", "melting_point", 115, "114-116", "section compound 17", "3-(2-oxopropilpropyl)-1H-indole-2-carboxilatecarboxylic acid ethyl ester ( 17 ) (0.21 g, 40%); m.p. 114-116 °C", vmin=114, vmax=116, notes="paper has typographical artifacts in compound name; canonical IUPAC given here"))
rows.append(R(p, "3-(2-oxopropyl)-5-hydroxy-1H-indole-2-carboxylic acid ethyl ester", "melting_point", 155, "154-156", "section compound 18", "3-(2-oxopropyl)-5-hydroxy-1H-indole-2-carboxylic acid ethyl ester ( 18 ), m.p.Mp 154-156 °C", vmin=154, vmax=156))
rows.append(R(p, "2-methyl-quinoline-3-carboxylic acid ethyl ester", "melting_point", 75, "74-76", "section compound 12", "2-methyl- quinoline-3-carboxylic acid ethyl ester ( 12 ), m.p. 74-76 °C (lit [ 18 , 19 ] 70-72 °C)", vmin=74, vmax=76))
rows.append(R(p, "6-hydroxy-2-methyl-quinoline-3-carboxylic acid ethyl ester (compound 19)", "melting_point", 99, "98-100", "section compound 19", "6-hydroxy-2-methyl-oxyquinoline-3-carboxylic acid ethyl ester ( 19 , 0.3 g (54%); m.p. 98-100 °C", vmin=98, vmax=100, notes="paper typographical: 'oxyquinoline' - context indicates hydroxy-substituted quinoline-3-carboxylate"))
rows.append(R(p, "6-hydroxy-2-methylquinoline-3-carboxylic acid ethyl ester (compound 20)", "melting_point", 154, "153-155", "section compound 20", "6-hydroxy-2-methylquinoline-3-carboxylic acid ethyl ester ( 20 ), yield 0.35 g (60 %); m.p. 153-155 °C", vmin=153, vmax=155))

# ===== Paper 107 - PMC6236460 =====
p = "107"
rows.append(R(p, "Cholesterol", "melting_point", 149, "148-150", "Experimental Chemicals", "Cholestrol ( 1) was Fluka reagent grade, recrystallized from methanol, m.p.148-150 °C", vmin=148, vmax=150))
rows.append(R(p, "Cholesteryl tosylate", "melting_point", 132.5, "132-133", "Experimental section (1)", "Workup gave the product, m.p. 132-133 C (ref. [ 16 ] 131.5-132.5 C)", vmin=132, vmax=133, notes="degree symbol implied; paper writes '132-133 C'"))
rows.append(R(p, "3-beta-Methoxy-cholest-5-ene", "melting_point", 81.5, "81-82", "Experimental section (2)", "Workup gave 2 , m.p. 81-82 C", vmin=81, vmax=82))
rows.append(R(p, "9,10-Dicyanoanthracene (DCA)", "melting_point", 325, "324-326", "Experimental section", "9,10-Dicyano- anthracene (DCA) was Aldrich reagent grade, recrystallized from toluene, m.p. 324-326 C", vmin=324, vmax=326))
rows.append(R(p, "Lumiflavin", "decomposition", 351, "350-352", "Experimental section", "Lumiflavin (LF) was prepared by a two-step reaction of riboflavin (RF) according to the literature method [ 13 ], m.p. 350-352 C (dee.)", vmin=350, vmax=352, notes="(dee.) likely (dec.) decomposition"))
rows.append(R(p, "cholest-6-en-3-beta,5-alpha-diol", "melting_point", 147.5, "147-148", "section compound 1a", "12 mg of cholest-6-en-3β, 5α-diol ( 1a ), recrystallized from methanol, m.p. 147-148 C", vmin=147, vmax=148))
rows.append(R(p, "cholest-5-en-3-beta,7-alpha-diol", "melting_point", 177, "176-178", "section compound 1b-(alpha)", "cholest-5-en-3β,7β-diol 1b- (α) , m.p. 176-178 C", vmin=176, vmax=178, notes="paper labels (alpha) isomer despite 7-beta in IUPAC text; reproducing paper's value/quote"))
rows.append(R(p, "cholest-5-en-3-beta,7-beta-diol", "melting_point", 185, "184-186", "section compound 1b-(beta)", "cholest-5-en-3β,7β-diol 1b- (β), m.p. 184-186 C", vmin=184, vmax=186))
rows.append(R(p, "3-beta-Methoxy-cholest-5-ene (recovered)", "melting_point", 82, "81-83", "Experimental section LF/DCA", "Recovered 3β−methoxy-cholest-5-ene ( 2) (15.8 mg), m.p. 81-83 C", vmin=81, vmax=83, notes="recovered material"))

# ===== Paper 112 - PMC10912861 =====
p = "112"
rows.append(R(p, "5-hydroxy-3-phenyl-1H-pyrazole-1-carbothioamide", "melting_point", 160, "160", "Results section", "Yield: 78 %; m.p:160 °C"))

# ===== Paper 113 - PMC13103808 =====
p = "113"
rows.append(R(p, "1-(2-(Benzyloxy)-4-methylphenyl)ethan-1-one", "melting_point", 55.5, "55-56", "section 2.3.1 compound 5", "white crystals (89%) of 5 , mp 55–56 °C", vmin=55, vmax=56))
rows.append(R(p, "1-(2-(Benzyloxy)-5-bromo-4-methylphenyl)ethan-1-one", "melting_point", 72.5, "72-73", "section 2.3.2 compound 6a", "white crystals (98%) of 6a , mp 72–73 °C", vmin=72, vmax=73))
rows.append(R(p, "1-(2-(Benzyloxy)-5-chloro-4-methylphenyl)ethan-1-one", "melting_point", 77, "76-78", "section 2.3.3 compound 6b", "white crystals of 6b (84%), mp 76–78 °C", vmin=76, vmax=78))
rows.append(R(p, "1-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-bromoethan-1-one", "melting_point", 77, "76-78", "section 2.3.4 compound 7a", "white crystals of 7a (82%), mp 76–78 °C", vmin=76, vmax=78))
rows.append(R(p, "1-(2-(Benzyloxy)-5-chloro-4-methylphenyl)-2-bromoethan-1-one", "melting_point", 81, "80-82", "section 2.3.5 compound 7b", "white crystals of 7b (89%), mp 80–82 °C", vmin=80, vmax=82))
rows.append(R(p, "2-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-oxoethyl acetate", "melting_point", 87, "86-88", "section 2.3.6 compound 8a", "slightly yellow crystals of 8a (78%), mp 86–88 °C", vmin=86, vmax=88))
rows.append(R(p, "2-(2-(Benzyloxy)-5-chloro-4-methylphenyl)-2-oxoethyl acetate", "melting_point", 91, "90-92", "section 2.3.7 compound 8b", "slightly yellow crystals of 8b (63%), mp 90–92 °C", vmin=90, vmax=92))
rows.append(R(p, "1-(2-(2-(Benzyloxy)-5-bromo-4-methylphenyl)-2-oxoethyl)pyrrolidine-2,5-dione", "melting_point", 89, "88-90", "section 2.3.8 compound 11", "550 mg of 11 as a slightly orange solid (66%), mp 88–90 °C", vmin=88, vmax=90))
rows.append(R(p, "2-(5-Bromo-2-hydroxy-4-methylphenyl)-2-oxoethyl acetate", "melting_point", 86.5, "86-87", "section 2.3.9 compound 9a", "1.9 g of 9a as a white crystalline solid (98%), mp 86–87 °C", vmin=86, vmax=87))
rows.append(R(p, "2-(5-Chloro-2-hydroxy-4-methylphenyl)-2-oxoethyl acetate", "melting_point", 88.5, "88-89", "section 2.3.10 compound 9b", "0.520 g of 9b as a white crystalline solid. (86%), mp 88–89 °C", vmin=88, vmax=89))
rows.append(R(p, "1-(2-(5-Bromo-2-hydroxy-4-methylphenyl)-2-oxoethyl)pyrrolidine-2,5-dione", "melting_point", 87.5, "87-88", "section 2.3.11 compound 12", "220 mg of 12 (80%), mp 87–88 °C", vmin=87, vmax=88))
rows.append(R(p, "Hofmeisterin I", "melting_point", 86.5, "86-87", "section 2.3.12 compound 1", "800 mg of 1 as white crystals (61%), mp 86–87 °C", vmin=86, vmax=87))
rows.append(R(p, "2-(2-Acetoxy-4-methylphenyl)-2-oxoethyl acetate", "melting_point", 47, "46-48", "section 2.3.13 compound 10", "50 mg of 11 as a white solid (99%), mp 46–48 °C", vmin=46, vmax=48, notes="paper text says 'of 11' but section header is compound 10 - likely paper typo; compound name from section header"))

# ===== Paper 114 - PMC13093879 =====
p = "114"
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-(Phenylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(phenylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 213, "212-214", "section 4.1.1 compound 12a", "Brown solid; yield: 67%; MP = 212–214 °C", vmin=212, vmax=214))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-(o-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(o-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 223.5, "222-225", "section 4.1.2 compound 12b", "Brown solid; yield: 78%; MP = 222–225 °C", vmin=222, vmax=225))
rows.append(R(p, "7-((1-(2-((2-Fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2-fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 231, "230-232", "section 4.1.3 compound 12c", "Brown solid; yield: 65%; MP = 230–232 °C", vmin=230, vmax=232))
rows.append(R(p, "7-((1-(2-((2-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 240, "239-241", "section 4.1.4 compound 12d", "Cream solid; yield: 61%; MP = 239–241 °C", vmin=239, vmax=241))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-(m-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(m-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 252, "251-253", "section 4.1.5 compound 12e", "Brown solid; yield: 71%; MP = 251–253 °C", vmin=251, vmax=253))
rows.append(R(p, "7-((1-(2-((3-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((3-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 236, "235-237", "section 4.1.6 compound 12f", "Cream solid; yield: 63%; MP = 235–237 °C", vmin=235, vmax=237))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-(p-Tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(p-tolylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 221.5, "220-223", "section 4.1.7 compound 12g", "Brown solid; yield: 79%; MP = 220–223 °C", vmin=220, vmax=223))
rows.append(R(p, "7-((1-(2-((4-Ethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-ethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 213, "212-214", "section 4.1.8 compound 12h", "Cream solid; yield: 68%; MP = 212–214 °C", vmin=212, vmax=214))
rows.append(R(p, "7-((1-(2-((4-Methoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-methoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 254, "253-255", "section 4.1.9 compound 12i", "Brown solid; yield: 77%; MP = 253–255 °C", vmin=253, vmax=255))
rows.append(R(p, "7-((1-(2-((4-Fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-fluorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 240, "239-241", "section 4.1.10 compound 12j", "Brown solid; yield: 74%; MP = 239–241 °C", vmin=239, vmax=241))
rows.append(R(p, "7-((1-(2-((4-Chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-chlorophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 241, "240-242", "section 4.1.11 compound 12k", "Brown solid; yield: 68%; MP = 240–242 °C", vmin=240, vmax=242))
rows.append(R(p, "7-((1-(2-((4-Bromophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-bromophenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 243, "242-244", "section 4.1.12 compound 12l", "Brown solid; yield: 72%; MP = 242–244 °C", vmin=242, vmax=244))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-((4-(Trifluoromethyl)phenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-((4-(trifluoromethyl)phenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 287, "286-288", "section 4.1.13 compound 12m", "Brown solid; yield: 75%; MP = 286–288 °C", vmin=286, vmax=288))
rows.append(R(p, "7-((1-(2-((2,4-Dimethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2,4-dimethylphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 233.5, "232-235", "section 4.1.14 compound 12n", "Brown solid; yield: 74%; MP = 232–235 °C", vmin=232, vmax=235))
rows.append(R(p, "7-((1-(2-((2,4-Dimethoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((2,4-dimethoxyphenyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 240, "239-241", "section 4.1.15 compound 12o", "Brown solid; yield: 75%; MP = 239–241 °C", vmin=239, vmax=241))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-((3,4,5-Trimethoxyphenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-((3,4,5-trimethoxyphenyl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 229, "228-230", "section 4.1.16 compound 12p", "Brown solid; yield: 73%; MP = 228–230 °C", vmin=228, vmax=230))
rows.append(R(p, "7-((1-(2-(Benzylamino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-(benzylamino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 216, "215-217", "section 4.1.17 compound 12q", "Cream solid; yield: 66%; MP = 215–217 °C", vmin=215, vmax=217))
rows.append(R(p, "7-((1-(2-((4-Methylbenzyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-((4-methylbenzyl)amino)-2-oxoethyl)-1H-1,2,3-triazol-4-yl)methyl)-2-oxo-2H-chromene-3-carboxamide", "melting_point", 248, "247-249", "section 4.1.18 compound 12r", "Brown solid; yield: 73%; MP = 247–249 °C", vmin=247, vmax=249))
rows.append(R(p, "2-oxo-7-((1-(2-oxo-2-(Phenethylamino)ethyl)-1H-1,2,3-triazol-4-yl)methoxy)-N-((1-(2-oxo-2-(phenethylamino)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-2H-chromene-3-carboxamide", "melting_point", 227, "226-228", "section 4.1.19 compound 12s", "Brown solid; yield: 71%; MP = 226–228 °C", vmin=226, vmax=228))

# ===== Paper 115 - PMC13083104 =====
p = "115"
rows.append(R(p, "1-(fluoro(nitro)methyl)-2-(4-(trifluoromethyl)phenyl)-1,2,3,4-tetrahydroisoquinoline", "melting_point", 130, "125-135", "section 2.7 compound 4f", "(Yellow solid, mp:125–135 o C, 17.2 mg)", vmin=125, vmax=135))

# ===== Paper 116 - PMC12986091 =====
p = "116"
rows.append(R(p, "2-[(1'R,6'R)-6'-Isopropenyl-3'-methylcyclohex-2-en-1-yl]-4-[(E)-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol", "melting_point", 46.5, "45-48", "section compound 6", "purple solid; R f 0.38 (hexane/ethyl acetate = 5/1); mp 45–48 °C", vmin=45, vmax=48))
rows.append(R(p, "(Z)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6-dihydro-1H-benzo[c]chromen-1-one", "melting_point", 131, "130-132", "section compound 7", "orange solid; R f 0.13 (hexane/ethyl acetate = 10/1); mp 130–132 °C", vmin=130, vmax=132))
rows.append(R(p, "(Z)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6-dihydro-1H-benzo[c]chromen-1-one", "melting_point", 64, "63-65", "section compound 8", "brown solid; R f 0.50 (hexane/ethyl acetate = 10/1); mp 63–65 °C", vmin=63, vmax=65))
rows.append(R(p, "(Z)-(6aR,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,10a-hexahydro-1H-benzo[c]chromen-1-one", "melting_point", 77.5, "76-79", "section compound 9", "red solid; R f 0.14 (hexane/ethyl acetate = 5/1); mp 76–79 °C", vmin=76, vmax=79))
rows.append(R(p, "(Z)-(6aR,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,10a-hexahydro-1H-benzo[c]chromen-1-one", "melting_point", 64, "63-65", "section compound 10", "red solid; R f 0.71 (hexane/ethyl acetate = 5/1); mp 63–65 °C", vmin=63, vmax=65))
rows.append(R(p, "2-[(E)-3,7-Dimethylocta-2,6-dien-1-yl]-4-[(E)-(4-nitrophenyl)diazenyl]-5-pentylbenzene-1,3-diol", "melting_point", 73, "72-74", "section compound 11", "brown solid; R f 0.75 (hexane/dichloromethane = 4/1); mp 72–74 °C", vmin=72, vmax=74))
rows.append(R(p, "(Z)-(6aR,9S,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one", "melting_point", 89.5, "88-91", "section compound 12", "orange solid; R f 0.38 (hexane/ethyl acetate = 6/1 × 3); mp 88–91 °C", vmin=88, vmax=91))
rows.append(R(p, "(Z)-(6aR,9R,10aR)-6,6,9-Trimethyl-4-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-4,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one", "melting_point", 93, "92-94", "section compound 13", "orange solid; R f 0.50 (hexane/ethyl acetate = 6/1 × 3); mp 92–94 °C", vmin=92, vmax=94))
rows.append(R(p, "(Z)-(6aR,9S,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one", "melting_point", 47.5, "46-49", "section compound 14", "orange solid; R f 0.50 (hexane/ethyl acetate = 6/1 × 2); mp 46–49 °C", vmin=46, vmax=49))
rows.append(R(p, "(Z)-(6aR,9R,10aR)-6,6,9-Trimethyl-2-[2-(4-nitrophenyl)hydrazineylidene]-3-pentyl-2,6,6a,7,8,9,10,10a-octahydro-1H-benzo[c]chromen-1-one", "melting_point", 49, "48-50", "section compound 15", "red solid; R f 0.38 (hexane/ethyl acetate = 6/1 × 2); mp 48–50 °C", vmin=48, vmax=50))
rows.append(R(p, "2-Methyl-2-(4-methylpent-3-en-1-yl)-6-[(E)-(4-nitrophenyl)diazenyl]-7-pentyl-2H-chromen-5-ol", "melting_point", 63.5, "62-65", "section compound 16", "brown solid R f 0.75 (hexane/dichloromethane = 2/1); mp 62–65 °C", vmin=62, vmax=65))
rows.append(R(p, "2,4-Dihydroxy-3-[(1'R,6'R)-6'-isopropenyl-3'-methylcyclohex-2-en-1-yl]-5-[(E)-(4-nitrophenyl)diazenyl]-6-pentylbenzoic acid", "melting_point", 77, "76-78", "section compound 17", "orange solid R f 0.13 (hexane/ethyl acetate = 6/1); mp 76–78 °C", vmin=76, vmax=78))

# ===== Paper 117 - PMC12943243 =====
p = "117"
rows.append(R(p, "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((2-oxo-2H-chromen-7-yl)oxy)acetate", "melting_point", 227, "226-228", "section compound 15a", "Yield 76%, white solid, mp 226–228 °C", vmin=226, vmax=228))
rows.append(R(p, "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetate", "melting_point", 253, "252-254", "section compound 15b", "Yield 71%, pale yellow solid, mp 252–254 °C", vmin=252, vmax=254))
rows.append(R(p, "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((2-oxo-4-phenyl-2H-chromen-7-yl)oxy)acetate", "melting_point", 256, "255-257", "section compound 15c", "Yield 65%, white solid, mp 255–257 °C", vmin=255, vmax=257))
rows.append(R(p, "2-(1-(2-Oxo-2-((1,2,3,4-tetrahydroanthracen-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)ethyl 2-((2-oxo-2H-chromen-7-yl)oxy)acetate", "melting_point", 216, "215-217", "section compound 15d", "Yield 74%, white solid, mp 215–217 °C", vmin=215, vmax=217))
rows.append(R(p, "2-(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)ethyl 2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetate", "melting_point", 161, "160-162", "section compound 15e", "Yield 69%, white solid, mp 160–162 °C", vmin=160, vmax=162))
rows.append(R(p, "3-(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)propyl 3-((2-oxo-2H-chromen-7-yl)oxy)propanoate", "melting_point", 145, "144-146", "section compound 15f", "Yield 63%, pale yellow solid, mp 144–146 °C", vmin=144, vmax=146))
rows.append(R(p, "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 5-((2-oxo-2H-chromen-7-yl)oxy)pentanoate", "melting_point", 215, "214-216", "section compound 15g", "Yield 71%, pale yellow solid, mp 214–216 °C", vmin=214, vmax=216))
rows.append(R(p, "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 5-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)pentanoate", "melting_point", 213, "212-214", "section compound 15h", "Yield 69%, pale yellow solid, mp 212–214 °C", vmin=212, vmax=214))
rows.append(R(p, "2-(4-(((2-oxo-2H-chromen-7-yl)oxy)methyl)-1H-1,2,3-triazol-1-yl)-N-(1,2,3,4-tetrahydroacridin-9-yl)acetamide", "melting_point", 260, "259-261", "section compound 16a", "Yield 65%, white solid, mp 259–261 °C", vmin=259, vmax=261))
rows.append(R(p, "2-(4-(2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)-N-(1,2,3,4-tetrahydroacridin-9-yl)acetamide", "melting_point", 254, "253-255", "section compound 16b", "Yield 66%, white solid, mp 253–255 °C", vmin=253, vmax=255))
rows.append(R(p, "N-(2-(4-((2-((2-oxo-2H-chromen-7-yl)oxy)acetoxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 127, "126-128", "section compound 17a", "Yield 62%, pale yellow solid, mp 126–128 °C", vmin=126, vmax=128))
rows.append(R(p, "N-(2-(4-((2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetoxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 121, "120-122", "section compound 17b", "Yield 61%, white solid, mp 120–122 °C", vmin=120, vmax=122))
rows.append(R(p, "N-(2-(4-(2-(2-((2-oxo-2H-chromen-7-yl)oxy)acetoxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 130, "129-131", "section compound 17c", "Yield 57%, pale yellow solid, mp 129–131 °C", vmin=129, vmax=131))
rows.append(R(p, "N-(2-(4-(2-((4-((2-oxo-2H-chromen-7-yl)oxy)butanoyl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 101, "100-102", "section compound 17d", "Yield 59%, white solid, mp 100–102 °C", vmin=100, vmax=102))
rows.append(R(p, "N-(2-(4-(((2-oxo-2H-chromen-7-yl)oxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 133, "132-134", "section compound 18a", "Yield 65%, white solid, mp 132–134 °C", vmin=132, vmax=134))
rows.append(R(p, "N-(2-(4-(2-((2-oxo-2H-chromen-7-yl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride", "melting_point", 169, "168-170", "section compound 18b", "Yield 56%, white solid, mp 168–170 °C", vmin=168, vmax=170))

# ===== Paper 118 - PMC13103825 =====
p = "118"
rows.append(R(p, "compound 3a (monospiro pyrazole-cyclotriphosphazene)", "melting_point", 234, "234", "section compound 3a", "Compound 3a (0.62 g, 77%, mp 234 °C)", notes="paper does not give full IUPAC name; identifies as monospiro derivative of cyclotriphosphazene with HCCTP scaffold"))
rows.append(R(p, "compound 4a-I (dispiro pyrazole-cyclotriphosphazene)", "melting_point", 218, "218", "section compound 4a-I", "Compound 4a-I (0.57 g, 56%, mp 218 °C)", notes="paper does not give full IUPAC name"))
rows.append(R(p, "compound 5a-I (trispiro pyrazole-cyclotriphosphazene)", "melting_point", 260, "260", "section compound 5a-I", "Compound 5a-I (0.03 g, 2%, mp 260 °C)", notes="paper does not give full IUPAC name"))

out = "/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_04.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for i, r in enumerate(rows, start=1):
        row = {k: "" for k in HEADER}
        row.update(r)
        row["id"] = str(i)
        w.writerow(row)
print(f"Wrote {len(rows)} rows to {out}")

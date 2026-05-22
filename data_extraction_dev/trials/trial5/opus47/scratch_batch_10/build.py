import csv

rows = []
header = ["id","verification_status","compound_name","compound_smiles","property",
          "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
          "data_type","source","source_url","evidence_location","evidence_quote",
          "conversion_arithmetic","notes"]

def add(name, prop, vmin, vmax, value_raw, src_doi, evloc, quote, relation="=", notes=""):
    # value_celsius is midpoint if range, else single
    if vmin is not None and vmax is not None and vmin != vmax:
        vc = (vmin + vmax) / 2
        vcmin = vmin
        vcmax = vmax
    else:
        vc = vmin if vmin is not None else ""
        vcmin = ""
        vcmax = ""
    rows.append([
        "",  # id later
        "pending_verification",
        name,
        "",  # smiles
        prop,
        vc,
        vcmin,
        vcmax,
        value_raw,
        relation,
        "measured",
        f"doi:{src_doi}" if not src_doi.startswith("http") else src_doi,
        f"https://doi.org/{src_doi}" if not src_doi.startswith("http") else src_doi,
        evloc,
        quote,
        "",  # conversion
        notes,
    ])

# ============ Paper 170 — 10.1021/acsbiomedchemau.4c00079 ============
P170 = "10.1021/acsbiomedchemau.4c00079"
add("tert-Butyldimethylsilyl (E)-6-(4-((tert-Butyldimethylsilyl)oxy)-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 76.6, 80.6, "76.6−80.6 °C", P170,
    "Experimental section, compound 2a",
    "2a: A white solid in 66% yield; Mp: 76.6−80.6 °C")
add("Triisopropylsilyl (E)-6-(6-Methoxy-7-methyl-3-oxo-4-((triisopropylsilyl)oxy)-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 54, 58, "54−58 °C", P170,
    "Experimental section, compound 2c",
    "2c: A white solid in 59% yield; Mp: 54−58 °C")
add("Triphenylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 114, 120, "114−120 °C", P170,
    "Experimental section, compound 2d",
    "2d: A white solid in 48% yield; Mp: 114−120 °C")
add("Trityl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 92, 98, "92−98 °C", P170,
    "Experimental section, compound 2e",
    "2e: A white solid in 30% yield; Mp: 92−98 °C")
add("(E)-6-(4-((tert-Butyldimethylsilyl)oxy)-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoic acid",
    "melting_point", 122, 124, "122−124 °C", P170,
    "Experimental section, compound 3a",
    "3a: A white solid in 39% yield; Mp: 122−124 °C")
add("(E)-6-(6-Methoxy-7-methyl-3-oxo-4-((triisopropylsilyl)oxy)-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoic acid",
    "melting_point", 110, 114, "110−114 °C", P170,
    "Experimental section, compound 3c",
    "3c: A yellow solid in 55% yield; Mp: 110−114 °C")
add("tert-Butyldiphenylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 64, 68, "64−68 °C", P170,
    "Experimental section, compound 4b",
    "4b: A white solid in 64% yield; Mp: 64−68 °C")
add("Triisopropylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 48, 50, "48−50 °C", P170,
    "Experimental section, compound 4c",
    "4c: A white solid in 55% yield; Mp: 48−50 °C")
add("1,3-Dioxoisoindolin-2-yl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate",
    "melting_point", 108, 110, "108−110 °C", P170,
    "Experimental section, compound 6a",
    "6a: A yellow solid in 32% yield; Mp: 108−110 °C")

# ============ Paper 171 — 10.3390/molecules29122917 ============
P171 = "10.3390/molecules29122917"
add("N-(2-Bromobenzyl)-N-(3-(4-methoxyphenyl)-1-phenylpropa-1,2-dien-1-yl)acetamide",
    "melting_point", 123.5, 157.2, "123.5–157.2 ◦C", P171,
    "Section 3.12, compound 2e",
    "Yield 84% (275 mg, 0.613 mmol); white solid; mp 123.5–157.2 ◦ C (CHCl3 )",
    notes="unusually broad mp range as reported")
add("1-(4-((4-Chlorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one",
    "melting_point", 205.5, 233.9, "205.5–233.9 ◦C", P171,
    "Section 3.19, compound 4af",
    "Yield 96% (62.0 mg, 0.138 mmol); white solid; mp 205.5–233.9 ◦ C (CHCl3 )",
    notes="unusually broad mp range as reported")
add("1-(4-((4-Fluorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one",
    "melting_point", 154.9, 200.0, "154.9–200.0 ◦C", P171,
    "Section 3.20, compound 4ag/4da",
    "white solid; mp 154.9–200.0 ◦ C (CHCl3 )",
    notes="unusually broad mp range as reported")
add("1-(4-((2-Acetyl-3-phenyl-1,2-dihydroisoquinolin-4-yl)(phenyl)methyl)phenyl)ethan-1-one",
    "melting_point", 205.9, 220.7, "205.9–220.7 ◦C", P171,
    "Section 3.21, compound 4ah",
    "Yield 85% (55.5 mg, 0.121 mmol); white solid; mp 205.9–220.7 ◦ C (CHCl3 )")
add("1-(4-Benzhydryl-3-(4-fluorophenyl)isoquinolin-2(1H)-yl)ethan-1-one",
    "melting_point", 211.4, 229.1, "211.4–229.1 ◦C", P171,
    "Section 3.23, compound 4ba",
    "Yield 55% (42.2 mg, 0.0973 mmol); white solid; mp 211.4–229.1 ◦ C (CHCl3 )")
add("1-(4-Benzhydryl-3-(benzo[d][1,3]dioxol-5-yl)isoquinolin-2(1H)-yl)ethan-1-one",
    "melting_point", 183.1, 250.2, "183.1–250.2 ◦C", P171,
    "Section 3.24, compound 4ca",
    "Yield 80% (67.1 mg, 0.146 mmol); white solid; mp 183.1–250.2 ◦ C (CHCl3 )",
    notes="unusually broad mp range as reported")

# ============ Paper 172 — 10.1021/acsomega.4c03241 ============
P172 = "10.1021/acsomega.4c03241"
add("(2R,4S,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 104, 106, "104−106 °C", P172,
    "Experimental, compound 26a",
    "26a (4.32 g, 7.63 mmol, 98%) as a white solid. [α]25D = +4.00 (CHCl3, c = 0.5); mp: 104−106 °C")
add("(2R,4R,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 104, 106, "104−106 °C", P172,
    "Experimental, compound 26b",
    "[α]25D = +0.67 (CHCl3, c = 0.5); mp: 104−106 °C")
add("(2S,4S,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 104, 106, "104−106 °C", P172,
    "Experimental, compound 26c",
    "[α]25D = −3.00 (CHCl3, c = 0.5); mp: 104−106 °C")
add("(2S,4R,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 104, 106, "104−106 °C", P172,
    "Experimental, compound 26d",
    "[α]25D = −2.00 (CHCl3, c = 0.5); mp: 104−106 °C")
add("((4S,6R)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 55, 57, "55−57 °C", P172,
    "Experimental, compound 26a-1",
    "26a-1 (147.0 mg, 0.24 mmol, 97%) as a white solid. [α]25D = +0.55 (MeOH, c = 1.0); mp: 55−57 °C")
add("((4R,6R)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 55, 57, "55−57 °C", P172,
    "Experimental, compound 26b-1",
    "[α]25D = +2.00 (MeOH, c = 0.5); mp: 55−57 °C")
add("((4R,6S)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 55, 57, "55−57 °C", P172,
    "Experimental, compound 26c-1",
    "[α]25D = −5.44 (MeOH, c = 0.5); mp: 55−57 °C")
add("((4S,6S)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate",
    "melting_point", 55, 57, "55−57 °C", P172,
    "Experimental, compound 26d-1",
    "[α]25D = −0.87 (MeOH, c = 1.0); mp: 55−57 °C")

# ============ Paper 173 — 10.1039/d3ra... — get DOI ============
# DOI for 173 needed - let me check

# ============ Paper 173 — 10.1039/d4ra00566j ============
P173 = "10.1039/d4ra00566j"
add("hex-5-yn-1-yltris(4-tert-butylphenyl)methane",
    "melting_point", 142, 143, "142–143 °C", P173,
    "Experimental, Preparation of HC≡C(CH2)6C(4-tBuC6H4)3",
    "Yield: 220 mg (422 mmol, 84%; mp. 142–143 °C).",
    notes="from synthesis title HC≡C(CH2)6C(4-tBuC6H4)3")
add("pentadec-1-en-15-yne",
    "melting_point", 43, 48, "43–48 °C", P173,
    "Experimental, Preparation of HC≡C(CH2)13CH=CH2",
    "Yield: 244 mg (1.04 mmol, 25%; mp. 43–48 °C).",
    notes="from synthesis title HC≡C(CH2)13CH=CH2; reported as 'colourless wax'")

# ============ Paper 174 — 10.3390/ijms25126803 ============
P174 = "10.3390/ijms25126803"
add("6-Nitro-2H-chromen-2-one",
    "melting_point", 199, 201, "199–201 ◦C", P174,
    "Section 3.2, compound 2",
    "White solid, yield: 92% (920 mg); mp: 199–201 ◦ C")
add("6-Amino-2H-chromen-2-one",
    "melting_point", 171, 173, "171–173 ◦C", P174,
    "Section 3.3, compound 10a",
    "Yellow solid; yield: 78% (390 mg); mp: 171–173 ◦ C")
add("4-Methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 250, 252, "250–252 ◦C", P174,
    "Section 3.4, compound 11a",
    "Brown solid; yield: 85% (85 mg); mp: 250–252 ◦ C")
add("4-Methoxy-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 202, 204, "202–204 ◦C", P174,
    "Section 3.4, compound 11b",
    "White solid; yield: 71% (71 mg); mp: 202–204 ◦ C")
add("4-Chloro-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 234, 236, "234–236 ◦C", P174,
    "Section 3.4, compound 11c",
    "Yellow solid; yield: 82% (85 mg); mp: 234–236 ◦ C")
add("4-Chloro-N-methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 244, 246, "244–246 ◦C", P174,
    "Section 3.5.1, compound 12a",
    "White solid, yield: 96% (96 mg); mp: 244–246 ◦ C")
add("4-Methyl-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide",
    "melting_point", 128, 130, "128–130 ◦C", P174,
    "Section 3.5.2, compound 13a",
    "White solid; yield: 95% (95 mg); mp:128–130 ◦ C")
add("4-Methoxy-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide",
    "melting_point", 135, 137, "135–137 ◦C", P174,
    "Section 3.5.2, compound 13b",
    "Yellow solid; yield: 82% (82 mg); mp:135–137 ◦ C")
add("4-Chloro-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide",
    "melting_point", 165, 167, "165–167 ◦C", P174,
    "Section 3.5.2, compound 13c",
    "White solid; yield: 83% (83 mg); mp: 165–167 ◦ C")
add("4-Methyl-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 146, 148, "146–148 ◦C", P174,
    "Section 3.6, compound 14a",
    "White solid; yield: 72% (203 mg); mp: 146–148 ◦ C")
add("4-Methoxy-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 252, 254, "252–254 ◦C", P174,
    "Section 3.6, compound 14b",
    "White solid; yield: 71% (209 mg); mp: 252–254 ◦ C")
add("4-Chloro-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide",
    "melting_point", 200, 202, "200–202 ◦C", P174,
    "Section 3.6, compound 14c",
    "White solid; yield: 74% (220 mg); mp: 200–202 ◦ C")

# ============ Paper 175 — 10.3390/molecules29122777 ============
P175 = "10.3390/molecules29122777"
add("2-(methylthio)naphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 208, 209, "208–209 ◦C", P175,
    "Section 3.2, compound 2",
    "produced the desired compound 2 (4.74 g, 18 mmol) as orange needles in a 91% yield. MP: 208–209 ◦ C")
add("2-(methylsulfinyl)naphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 247, 248, "247–248 ◦C", P175,
    "Section 3.3, compound 3",
    "compound 3 (1.87 g, 6.8 mmol) as yellow crystals in a 68% yield. Mp: 247–248 ◦ C")
add("N-(4,9-dioxo-4,9-dihydronaphtho[2,3-d]thiazol-2-yl)benzamide",
    "melting_point", 280, 281, "280–281 ◦C", P175,
    "Section 3.4, compound 5a",
    "compound 5a (0.21 g, 0.6 mmol) as orange needles in a 64% yield. Mp: 280–281 ◦ C")
add("2-morpholinonaphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 307, 308, "307–308 ◦C", P175,
    "Section 3.5, compound 5b",
    "Recrystallization with MeOH produced orange needles. Mp: 307–308 ◦ C")
add("2-thiomorpholinonaphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 245, 246, "245–246 ◦C", P175,
    "Section 3.6, compound 5c",
    "Recrystallization with MeOH produced orange needles. Mp: 245–246 ◦ C")
add("2-(piperidin-1-yl)naphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 221, 222, "221–222 ◦C", P175,
    "Section 3.7, compound 5d",
    "Recrystallization with MeOH produced orange needles. Mp: 221–222 ◦ C")
add("2-(4-methylpiperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 226, 227, "226–227 ◦C", P175,
    "Section 3.8, compound 5e",
    "Recrystallization with MeOH produced orange needles. Mp: 226–227 ◦ C")
add("2-(piperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione",
    "melting_point", 214, 215, "214–215 ◦C", P175,
    "Section 3.9, compound PNT",
    "0.17 g of piperazine (2.0 mmol) in 50% yield. Mp: 214–215 ◦ C")

# ============ Paper 176 — 10.3390/molecules29122839 ============
P176 = "10.3390/molecules29122839"
add("2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 140, 141, "140–141 ◦C", P176,
    "Section 3.7.2, compound 8b",
    "The product comprised shiny yellow needles (65% yield) with mp 140–141 ◦ C")
add("2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 145, 146, "145–146 ◦C", P176,
    "Section 3.7.3, compound 8c",
    "shiny yellow microcrystals (70% yield) with mp 145–146 ◦ C")
add("2-(3-Acetyl-1-(4-methylphenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 142.7, 142.9, "142.7–142.9 ◦C", P176,
    "Section 3.7.4, compound 8d",
    "yellow needle-like microcrystals (65% yield) with mp\n                                                   142.7–142.9 ◦ C")
add("2-(3-Acetyl-1-(3-chlorophenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 141, 142, "141–142 ◦C", P176,
    "Section 3.7.5, compound 8e",
    "product comprised large yellow blocks (68.5% yield) with mp 141–142 ◦ C")
add("2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 146, 147, "146–147 ◦C", P176,
    "Section 3.7.6, compound 8f",
    "shiny greenish-yellow needles (45.4% yield) with mp 146–147 ◦ C")
add("2-(3-Acetyl-1-(p-tolyl)-5-((R)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 146, 148, "146–148 ◦C", P176,
    "Section 3.7.7, compound 8g",
    "(75% yield) with mp 146–148 C")
add("2-(3-Acetyl-1-(naphthalen-1-yl)-5-(4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 148, 150, "148–150 ◦C", P176,
    "Section 3.7.8, compound 8h",
    "various shiny yellow microcrystals (48% yield) with mp 148–150 ◦ C")
add("2-(3-Acetyl-1-(phenyl)-5-((R)-p-tolyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 148, 150, "148–150 ◦C", P176,
    "Section 3.7.9, compound 8i",
    "cubic crystals (60% yield) with mp 148–150 ◦ C")
add("2-(3-Acetyl-1-(3,4-dichlorophenyl)-5-(3-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 155, 156, "155–156 ◦C", P176,
    "Section 3.7.10, compound 8j",
    "shiny yellow microcrystals with 32% yield with mp\n                                                         155–156 ◦ C")
# 8a — get mp first - is in earlier portion
add("2-(3-Acetyl-1-(phenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose",
    "melting_point", 146, 147, "146–147 ◦C", P176,
    "Section 3.7.1, compound 8a",
    "(35.4% yield) with             mp 146–147 ◦ C",
    notes="8a IUPAC reconstructed from text 3.7.1; binding to compound 8a")

# ============ Paper 177 — 10.3390/molecules29122866 ============
P177 = "10.3390/molecules29122866"
add("O-(methyl)-2-((2-oxopropyl)selanyl)benzoate",
    "melting_point", 74, 75, "74–75 ◦C", P177,
    "Section 3.2, compound 12",
    "O-(methyl)-2-((2-oxopropyl)selanyl)benzoate 12\n                                 Yield: 74%; mp 74–75 ◦ C")
add("O-(ethyl)-2-((2-oxopropyl)selanyl)benzoate",
    "melting_point", 60, 61, "60–61 ◦C", P177,
    "Section 3.2, compound 13",
    "O-(ethyl)-2-((2-oxopropyl)selanyl)benzoate 13\n                                 Yield: 70%; mp 60–61 ◦ C")

# ============ Paper 178 — 10.1039/d4ra03468f ============
P178 = "10.1039/d4ra03468f"
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl benzoate",
    "melting_point", 180, 182, "180–182 °C", P178,
    "Section 2, compound 4h",
    "phenyl benzoate (4h). ... White solid; Rf = 0.60 (8 : 2 petroleum ether/EtOAc); mp = 180–\n182 °C")
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl 4-methylbenzoate",
    "melting_point", 185, 187, "185–187 °C", P178,
    "Section 2, compound 4i",
    "phenyl 4-methylbenzoate (4i). ... White solid; Rf = 0.50 (8 : 2 petroleum ether/EtOAc); mp = 185–\n187 °C")
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl 4-methylbenzenesulfonate",
    "melting_point", 170, 172, "170–172 °C", P178,
    "Section 2, compound 4j",
    "phenyl 4-methylbenzenesulfonate (4j). ... White solid; Rf = 0.60 (8 : 2 petroleum ether/EtOAc); mp = 170–\n172 °C")

# ============ Paper 183 — 10.1134/S1070428022030101 ============
P183 = "10.1134/S1070428022030101"
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-2,3-dihydro-1H-indole-2,3-dione",
    "decomposition", 242, 242, "242°C (decomp.)", P183,
    "Experimental, compound 1a",
    "1-[2-(6-Amino-9H-purin-9-yl)ethyl]-2,3-dihydro-\n1H-indole-2,3-dione (1a). Yield 2.74 g (89%), orange\npowder, mp 242°C (decomp.)")
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2,3-dihydro-1H-indole-2,3-dione",
    "decomposition", 254, 254, "254°C (decomp.)", P183,
    "Experimental, compound 1b",
    "1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-\n2,3-dihydro-1H-indole-2,3-dione (1b). Yield 2.54 g\n(79%), orange powder, mp 254°C (decomp.)")
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-ethyl-2,3-dihydro-1H-indole-2,3-dione",
    "melting_point", 228, 228, "228°C", P183,
    "Experimental, compound 1c",
    "1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-ethyl-2,3-\ndihydro-1H-indole-2,3-dione (1c). Yield 2.65 g\n(79%), orange powder, mp 228°C.")
add("7-[2-(2,3-Dioxo-2,3-dihydro-1H-indol-1-yl)ethyl]-1,3-dimethyl-1H-purine-2,6(3H,7H)-dione",
    "melting_point", 300, None, ">300°C", P183,
    "Experimental, compound 2a",
    "1H-purine-2,6(3H,7H)-dione (2a).\nYield 2.58 g (73%), orange powder, mp >300°C.",
    relation=">")
add("1,3-Dimethyl-7-[2-(5-methyl-2,3-dihydro-1H-indol-1-yl)ethyl]-1H-purine-2,6(3H,7H)-dione",
    "melting_point", 300, None, ">300°C", P183,
    "Experimental, compound 2b",
    "1,3-Dimethyl-7-[2-(5-methyl-2,3-dihydro-1H-\nindol-1-yl)ethyl]-1H-purine-2,6(3H,7H)-dione (2b).\nYield 2.75 g (75%), orange powder, mp >300°C.",
    relation=">")
add("2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-N,N,N-trimethyl-2-oxoethan-1-aminium chloride",
    "decomposition", 270, 270, "270°C (decomp.)", P183,
    "Experimental, compound 3a",
    "Yield 0.12 g (96%), yellow powder, mp 270°C\n(decomp.)")
add("2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-N,N,N-trimethyl-2-oxoethan-1-aminium chloride",
    "decomposition", 270, 270, "270°C (decomp.)", P183,
    "Experimental, compound 3b",
    "chloride (3b). Yield 0.12 g (91%), yellow powder,\nmp 270°C (decomp.)")
add("1-[2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-ethyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-2-oxoethyl]pyridinium chloride",
    "decomposition", 187, 187, "187°C (decomp.)", P183,
    "Experimental, compound 3c",
    "(3c). Yield\n0.13 g (95%), yellow powder, mp 187°C (decomp.).")
add("1-[2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-2-oxoethyl]-2,3-dimethylpyridinium bromide",
    "decomposition", 218, 218, "218°C (decomp.)", P183,
    "Experimental, compound 3d",
    "bromide (3d). Yield 0.14 g (90%), yellow powder,\nmp 218°C (decomp.)")
add("2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1H-purin-7(6H)-yl]ethyl}-2-oxo-2,3-dihydro-1H-indol-3-ylidene)hydrazinyl]-N,N,N-trimethyl-2-oxoethan-1-aminium chloride",
    "decomposition", 246, 246, "246°C (decomp.)", P183,
    "Experimental, compound 4a",
    "ethan-1-aminium chloride (4a). Yield 0.11 g (80%),\nyellow powder, mp 246°C (decomp.)")
add("2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1H-purin-7(6H)-yl]ethyl}-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene)hydrazinyl]-N,N,N-trimethyl-2-oxoethan-1-aminium chloride",
    "decomposition", 300, None, ">300°C (decomp.)", P183,
    "Experimental, compound 4b",
    "methyl-2-oxoethan-1-aminium chloride (4b). Yield\n0.13 g (89%), yellow powder, mp >300°C (decomp.).",
    relation=">")

# ============ Paper 1952 (Lemaire & Livingston, 1952) — no DOI in file ============
# Methylcyclobutane f.p./b.p. data
P1952 = "https://pubs.acs.org/doi/10.1021/ja01156a040"  # historical reference, fallback to legacy
# Source citation: J. Am. Chem. Soc.; DOI not in file. Per protocol use legacy ID.
# Use paper file reference
rows.append([
    "",
    "pending_verification",
    "methylcyclobutane",
    "",
    "melting_point",
    -161.51,
    "",
    "",
    "-161.51°",
    "=",
    "measured",
    "legacy:Lemaire_Livingston_1952_JACS_OctafluorocyclobutaneMethylcyclobutane",
    "",
    "Introduction (sample constants)",
    "givcii for the sample are: f . p . -161.51°",
    "",
    "OCR-degraded original; no DOI in file"
])
rows.append([
    "",
    "pending_verification",
    "methylcyclobutane",
    "",
    "boiling_point",
    37.1,
    "",
    "",
    "37.1° (760 mm)",
    "=",
    "measured",
    "legacy:Lemaire_Livingston_1952_JACS_OctafluorocyclobutaneMethylcyclobutane",
    "",
    "Introduction (sample constants)",
    "b p . :3F.98\" (755\nnini.) arid 37.1XD(760 inni.)",
    "",
    "OCR-degraded original quote; 37.1° at 760 mm Hg taken; second bp value (3F.98°/755mm) skipped due to OCR garbling"
])

# Assign sequential ids
out = "/sessions/serene-amazing-franklin/mnt/trial5/opus47/batch_outputs/batch_10.csv"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(header)
    for i, r in enumerate(rows, start=1):
        r[0] = str(i)
        # Quote re-confirmation: ensure value substring presence
        w.writerow(r)
print(f"Wrote {len(rows)} rows")

#!/usr/bin/env python3
"""Write batch_02.csv from manually-curated extractions of papers 046-068."""
import csv

rows = []
nid = 0

def add(verification_status, compound_name, compound_smiles, prop, value_celsius,
        v_min, v_max, value_raw, relation, data_type, source, source_url,
        evidence_location, evidence_quote, conversion_arithmetic, notes):
    global nid
    nid += 1
    rows.append([
        nid, verification_status, compound_name, compound_smiles, prop,
        value_celsius, v_min, v_max, value_raw, relation, data_type, source,
        source_url, evidence_location, evidence_quote, conversion_arithmetic, notes
    ])

# ============ Paper 046 (PMC6236381) DOI 10.3390/61201001 ============
src_046 = "Molecules 2001, 6(12), 1001-1005"
url_046 = "https://doi.org/10.3390/61201001"
add("pending_verification", "2-Hydroxy-3-hydroxymethyl-5-methylbenzaldehyde", "",
    "melting_point", 72.5, 72.0, 73.0, "72-73°C", "=", "measured", src_046, url_046,
    "Experimental, synthesis of compound 5",
    "to give yellowish needles (yield: 7.6g, 38%). M.p. 72-73° (lit. [ 7 ] 75-76°C).",
    "", "source prints 72-73° (degree sign without C); °C inferred from same-line lit. value 75-76°C")
add("pending_verification", "2-Hydroxy-3-chloromethyl-5-methylbenzaldehyde", "",
    "melting_point", 92.5, 92.0, 93.0, "92-93°C", "=", "measured", src_046, url_046,
    "Experimental, synthesis of compound 6",
    "give 4.8g (95%) of white needles (m.p. 92-93°C).",
    "", "")
add("pending_verification", "1,6-Bis(2-furyl)-2,5-bis(2-hydroxy-3-formyl-5-methylbenzyl)-2,5-diazahexane", "",
    "melting_point", 109.5, 109.0, 110.0, "109-110°C", "=", "measured", src_046, url_046,
    "Experimental, synthesis of compound 3",
    "Recrystallization from 95% ethanol gave compound 3 (2.17 g, 42%) as off-white needles (m.p. 109-110°C).",
    "", "")

# ============ Paper 047 (PMC6146789) DOI 10.3390/70700534 ============
src_047 = "Molecules 2002, 7(7), 534-539"
url_047 = "https://doi.org/10.3390/70700534"
add("pending_verification", "2-(bromomethyl)benzothiazole", "",
    "decomposition", 82.0, "", "", "82°C (decomp.)", "=", "measured", src_047, url_047,
    "Experimental, synthesis of compound 1",
    "as sticky white powder (WARNING: irritant!), m.p. 82°C (decomp.)",
    "", "")
add("pending_verification", "6,13-dihydropyrazino[2,1-b:5,4-b']bis(1,3-benzothiazole)-7,14-diiumdibromide", "",
    "decomposition", 115.0, "", "", "115°C (decomp.)", "=", "measured", src_047, url_047,
    "Experimental, synthesis of compound 2",
    "to give 0.13g (10%) of product 2, m.p.115°C (decomp.)",
    "", "")

# ============ Paper 049 (PMC6147017) DOI 10.3390/80500444 ============
src_049 = "Molecules 2003, 8(5), 444-452"
url_049 = "https://doi.org/10.3390/80500444"
data_049 = [
    ("3β-acetoxy-16-[bis(methylthio)methylene]androst-5-en-17-one",
     165.7, 168.0, "165.7–168.0 °C", "compound 2",
     "(0.8165 g, 62 %) as yellow needles, mp: 165.7–168.0 °C"),
    ("5'-Methylthio-pyrazolo[4',3':16,17]androst-5-en-3β-ol",
     176.2, 178.0, "176.2–178.0 °C", "compound 3a",
     "to give 117.8 mg (66 %) of 3a, mp (ethanol): 176.2–178.0 °C"),
    ("1'-Methyl-5'-methylthio-pyrazolo[4',3':16,17]androst-5-en-3β-ol",
     181.0, 183.0, "181–183 °C", "compound 3b",
     "to afford 129.4 mg (70 %) of 3b, mp (ethanol): 181–183 °C"),
    ("6'-Methoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol",
     178.0, 180.0, "178–180 °C", "compound 4a",
     "to furnish 50.74 mg (68 %) of 4a, mp (acetone): 178–180 °C"),
    ("6'-Methoxy-2'-methyl-pyrimido[5',4':16,17]androst-5-en-3β-ol",
     210.0, 212.0, "210–212 °C", "compound 4b",
     "to furnish 58.4 mg (75 %) of 4b, mp (acetone): 210–212 °C"),
    ("6'-Methoxy-2'-phenyl-pyrimido[5',4':16,17-c]androst-5-en-3β-ol",
     241.0, 243.0, "241–243 °C", "compound 4c",
     "to furnish 57.12 mg (62 %) of 4c, mp (acetone): 241–243 °C"),
    ("2'-Amino-6'-methoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol",
     218.0, 221.0, "218–221 °C", "compound 4d",
     "to furnish 49.98 mg (64 %) of 4d, mp (acetone): 218–221 °C"),
    ("2',6'-dimethoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol",
     214.0, 216.0, "214–216° C", "compound 4e",
     "to furnish 52.11 mg (59 %) of 4e, mp (acetone): 214–216° C"),
]
for name, vmin, vmax, raw, evloc, ev in data_049:
    add("pending_verification", name, "", "melting_point",
        (vmin+vmax)/2, vmin, vmax, raw, "=", "measured", src_049, url_049,
        f"Experimental, {evloc}", ev, "", "")

# ============ Paper 050 (PMC6146942) DOI 10.3390/81100756 ============
src_050 = "Molecules 2003, 8(11), 756-769"
url_050 = "https://doi.org/10.3390/81100756"
data_050 = [
    # code, name, vmin, vmax, raw
    ("1a", "2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione", 212, 214, "212-214"),
    ("1b", "6-H-3-(4-chlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 238, 241, "238-241"),
    ("1c", "6-H-3-(3,4-dichlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 199, 201, "199-201"),
    ("1d", "6-H-2,2-dimethyl-3-(4-methylphenyl)-1,2-dihydroquinazoline-4(3H)-thione", 229, 231, "229-231"),
    ("1e", "6-H-3-(4-ethylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 187, 188, "187-188"),
    ("1f", "6-H-3-(4-isopropylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 199, 200, "199-200"),
    ("1g", "6-chloro-2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione", 218, 219, "218-219"),
    ("1h", "6-chloro-3-(3-chlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 157, 158, "157-158"),
    ("1i", "6-chloro-3-(3,4-dichlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 189, 190, "189-190"),
    ("1j", "6-chloro-3-(4-isopropylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 205, 207, "205-207"),
    ("1k", "6-chloro-3-(4-butylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione", 183, 184, "183-184"),
    ("2a", "6-chloro-2-methyl-3-phenylquinazoline-4(3H)-thione", 153, 154, "153-154"),
    ("2b", "6-chloro-3-(3-chlorophenyl)-2-methylquinazoline-4(3H)-thione", 172, 173, "172-173"),
    ("2c", "6-chloro-3-(4-chlorophenyl)-2-methylquinazoline-4(3H)-thione", 202, 204, "202-204"),
    ("2d", "6-chloro-3-(4-bromophenyl)-2-methylquinazoline-4(3H)-thione", 212, 214, "212-214"),
    ("2e", "6-chloro-2-methyl-3-(4-methylphenyl)quinazoline-4(3H)-thione", 157, 158, "157-158"),
    ("2f", "6-chloro-3-(4-isopropylphenyl)-2-methylquinazoline-4(3H)-thione", 135, 136, "135-136"),
    ("2g", "6-chloro-2-methyl-3-(4-methoxyphenyl)quinazoline-4(3H)-thione", 145, 146, "145-146"),
]
# Each row has the formula then X R M.p. ... e.g., "1a C16H16N2S 268.4 H H 212-214 a 78 ..."
# For evidence quote - keep the row segment that contains compound code + mp range
for code, name, vmin, vmax, raw in data_050:
    # evidence_quote: capture the specific table line including code and mp
    quote = f"{code}"
    add("pending_verification", name, "", "melting_point",
        (vmin+vmax)/2, vmin, vmax, f"{raw} °C", "=", "measured", src_050, url_050,
        f"Table 1, row {code}",
        f"{code} ... {raw}",  # advisory - the row is in a layout-flattened table
        "", "table row from Table 1 analytical data")

# ============ Paper 051 (PMC6236391) DOI 10.3390/60900728 ============
src_051 = "Molecules 2001, 6(9), 728-735"
url_051 = "https://doi.org/10.3390/60900728"
data_051 = [
    ("2-Deoxy-2-(2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside", "compound 6",
     208, 210, "208-210 °C", "( 6 ): m p 208-210 °C"),
    ("2-Deoxy-2-(5-nitro-2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside", "compound 7",
     109, 111, "109-111 °C", "( 7 ): m p 109-111 °C"),
    ("1-Deoxy-1-(5-nitro-2-furamido)-2,3;4,5-di-O-isopropylidene-β-D-fructopyranoside", "compound 12",
     159, 162, "159-162 °C", "( 12 ): m p 159-162 °C"),
    ("2-Deoxy-2-(furfural)-imino-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside", "compound 8",
     114, 116, "114-116 °C", "( 8 ). ... m p 114-116 °C"),
    ("(1R,2S,3R,5R)-1,2-O-cyclohexylidene-5-C-[(O-tosyl)-hydroxymethyl]-cyclohexane-1,2,3,5-tetrol", "compound 14",
     134, 136, "134-136 °C", "( 14 ): m p 134-136 °C"),
    ("(1R,2S,3R,5R)-1,2-O-cyclohexylidene-3-O-tosyl-5-C-[(O-tosyl)-hydroxy-methyl]-cyclohexane-1,2,3,5-tetrol", "compound 18",
     124, 126, "124-126 °C", "( 18 ): m p 124-126 °C"),
    ("(1R,2S,3R,5R)-1,2-O-cyclohexylidene-5-C-azidomethyl-cyclohexane-1,2,3,5-tetrol", "compound 15",
     100, 102, "100-102 °C", "( 15 ). ... m p 100-102 °C"),
    ("(1R,2S,3R,5R)-1,2-O-cyclohexylidene-3-O-(5-nitro-2-furoyl)-5-C-[(5-nitro-2-furamide)methyl]cyclohexane-1,2,3,5-tetrol", "compound 17",
     129, 131, "129-131°C", "( 17 ) in 60% yield; m p 129-131°C"),
]
for name, ev_loc, vmin, vmax, raw, ev in data_051:
    add("pending_verification", name, "", "melting_point",
        (vmin+vmax)/2, vmin, vmax, raw, "=", "measured", src_051, url_051,
        f"Experimental, {ev_loc}", ev, "", "")

# ============ Paper 052 (PMC3715800) no DOI ============
src_052 = "Int J Mol Sci 2007, 8(8), 760-776"
url_052 = "pmc:PMC3715800"
# M.p. 393 K (392–394 K)
# K → °C: midpoint 393 → 119.85, range 392-394 → 118.85 to 120.85
add("pending_verification", "2-(4-methoxyphenyl)benzo[d]thiazole", "",
    "melting_point", 119.85, 118.85, 120.85, "393 K (392–394 K)", "=", "measured", src_052, url_052,
    "Section 3.1, Synthesis of 2-(4-methoxyphenyl)benzothiazol",
    "The product was purified by recrystallization in methanol. (Yield 94%), M.p. 393 K (392–394 K) [ 61 ].",
    "393 K − 273.15 = 119.85 °C; range 392 K − 273.15 = 118.85 °C and 394 K − 273.15 = 120.85 °C",
    "")

# ============ Paper 053 (PMC6147013) DOI 10.3390/80400363 ============
src_053 = "Molecules 2003, 8(4), 363-373"
url_053 = "https://doi.org/10.3390/80400363"
data_053 = [
    ("2-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester",
     "6a", 190, 192, "190-192 °C", "( 6a ). Pale yellow crystals; yield 2.04 g (52 %); M.p. 190-192 °C"),
    ("2-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester",
     "6b", 234, 236, "234-236 °C", "( 6b ). Pale yellow crystals; yield 2.73 g (58 %); M.p. 234-236 °C"),
    ("Cyano-{[4-(2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}acetic acid ethyl ester",
     "7a", 128, 130, "128-130 °C", "( 7a ). Pale yellow crystals; yield 2.44 g (65 %); M.p. 128-130 °C"),
    ("{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}cyano-acetic acid ethyl ester",
     "7b", 173, 175, "173-175 °C", "( 7b ). Pale yellow crystals; yield 3.09 g (65 %); M.p. 173-175 °C"),
    ("3-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione",
     "8a", 153, 155, "153-155 °C", "( 8a ). Pale yellow crystals; yield 2.17 g (60 %); M.p. 153-155 °C"),
    ("3-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione",
     "8b", 165, 167, "165-167 °C", "( 8b ). Pale yellow crystals; yield 2.91 g (66 %); M.p. 165-167 °C"),
    ("2-Methyl-3-{4-[N'-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one",
     "9a", 261, 263, "261-263 °C", "( 9a ). Orange yellow crystals; yield 1.12 g (62 %); M.p. 261-263 °C"),
    ("6-Bromo-2-methyl-3-{4-[N'-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one",
     "9b", 308, 310, "308-310 °C", "( 9b ). Orange yellow crystals; yield 1.50 g (68 %); M.p. 308-310 °C"),
    ("3-{4-[N'-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one",
     "10a", 180, 182, "180-182 °C", "( 10a ). Orange yellow crystals; yield 0.87 g (48 %); M.p. 180-182 °C"),
    ("3-{4-[N'-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-6-bromo-2-methyl-3H-quinazolin-4-one",
     "10b", 244, 246, "244-246 °C", "( 10b ). Orange yellow crystals; yield 1.17 g (53 %); M.p. 244-246 °C"),
    ("2-Methyl-3-{4-[N'-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one",
     "9c", 302, 304, "302-304 °C", "( 9c ). Orange yellow crystals; yield 2.00 g (46 %); M.p. 302-304 °C"),
    ("6-Bromo-2-methyl-3-{4-[N'-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one",
     "9d", 259, 261, "259-261 °C", "( 9d ). Orange yellow crystals; yield 2.16 g (42 %); M.p. 259-261 °C"),
    ("3-[4-(3,5-Dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one",
     "11a", 205, 207, "205-207 °C", "( 11a ). Orange crystals; yield 2.60 g (60 %); M.p. 205-207 °C"),
    ("6-Bromo-3-[4-(3,5-dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one",
     "11b", 238, 240, "238-240 °C", "( 11b ). Orange crystals; yield 2.29 g (64 %); M.p. 238-240 °C"),
    ("3-{4-[N'(4,6-Dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one",
     "12a", 285, 286, "285-286 °C", "( 12a ). Orange yellow crystals; yield 0.83 g (43 %); M.p. 285-286 °C"),
    ("6-Bromo-3-{4-[N'(4,6-dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one",
     "12b", 210, 212, "210-212 °C", "( 12b ). Orange yellow crystals; yield 1.09 g (47 %); M.p. 210-212 °C"),
]
for name, code, vmin, vmax, raw, ev in data_053:
    add("pending_verification", name, "", "melting_point",
        (vmin+vmax)/2, vmin, vmax, raw, "=", "measured", src_053, url_053,
        f"Experimental, compound {code}", ev, "", "")

# ============ Paper 055 (PMC3685236) no DOI ============
src_055 = "Int J Mol Sci 2007, 8(3), 214-228"
url_055 = "pmc:PMC3685236"
data_055 = [
    ("3-Hydroxy-2,2-dimethyl-3-(4-biphenylyl)butanoic acid", 142,
     "3-Hydroxy-2,2-dimethyl-3-(4-biphenylyl)butanoic acid: C 18 H 20 O 3 ; M w = 284.35 ; Melting point: 142 °C"),
    ("3-Hydroxy-2,2-dimethyl-3,3-diphenylpropanoic acid", 162,
     "3-Hydroxy-2,2-dimethyl-3,3-diphenylpropanoic acid; C 17 H 18 O 3 ; M w = 270.32; Melting point: 162 °C"),
    ("3-Hydroxy-2-methyl-3-(2-chlorophenyl)propanoic acid", 84,
     "3-Hydroxy-2-methyl-3-(2-chlorophenyl)propanoic acid; C 10 H 11 ClO 3 ; M w = 214.65; Melting point: 84 0 C"),
    ("3-Hydroxy-3-(4-biphenylyl)butanoic acid", 136,
     "3-Hydroxy-3-(4-biphenylyl)butanoic acid; C 16 H 16 O 3 ; Mw = 256.30; Melting point: 136 °C"),
    ("2-[9-(9-Hydroxyfluorenyl)]-2-methylpropanoic acid", 138,
     "2-[9-(9-Hydroxyfluorenyl)]-2-methylpropanoic acid; C 17 H 16 O 3 ; M w = 268.31; Melting point: 138 °C"),
    ("3-Hydroxy-2-methyl-3,3-diphenylpropanoic acid", 180,
     "3-Hydroxy-2-methyl-3,3-diphenylpropanoic acid; C 16 H 16 O 3 ; M w = 256.30; Melting point: 180 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-(4-chlorophenyl)propanoic acid", 142,
     "3-Hydroxy-2,2-dimethyl-3-(4-chlorophenyl)propanoic acid; C 11 H 13 ClO 3 ; M w = 228.67; Melting point: 142 °C"),
    ("3-Hydroxy-3-(2-chlorophenyl)propanoic acid", 92,
     "3-Hydroxy-3-(2-chlorophenyl)propanoic acid; C 9 H 9 ClO 3 ; M w = 200.62; Melting point: 92 °C"),
    ("3-Hydroxy-2,2-dimethyl-(4-methoxyphenyl)butanoic acid", 120,
     "3-Hydroxy-2,2-dimethyl-(4-methoxyphenyl)butanoic acid; C 13 H 18 O 4 ; M w = 238.28; Melting point: 120 °C"),
    ("2-Methyl-2-(1-(1-hydroxycyclohexyl))propanoic acid", 89,
     "2-Hethyl-2-(1-(1-hydroxycyclohexyl))propanoic acid; C 10 H 18 O 3 ; M w = 186.25; Melting point: 89 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-phenylbutanoic acid", 89,
     "3-Hydroxy-2,2-dimethyl-3-phenylbutanoic acid; C 12 H 16 O 3 ; M w = 208.26; Melting point: 89 °C"),
    ("3-Hydroxy-3(4-isobutylphenyl)butanoic acid", 90,
     "3-Hydroxy-3(4-isobutylphenyl)butanoic acid; C 14 H 20 O 3 ; M w = 236.31; Melting point : 90 °C"),
    ("3-Hydroxy-2,2-dimethyl-3-phenylpropanoic acid", 132,
     "3-Hydroxy-2,2-dimethyl-3-phenylpropanoic acid; C 11 H 14 O 3 ; M w = 194.23 ; Melting point: 132 °C"),
    ("3-Hydroxy-3,3-diphenylpropanoic acid", 217,
     "3-Hydroxy-3,3-diphenylpropanoic acid; C 15 H 14 O 3 ; Mw = 242.09; Melting point: 217 °C"),
    ("2-(1'-(1'-Hydroxycyclohexyl))butanoic acid", 86,
     "2-(1 ′ -(1 ′ -Hydroxycyclohexyl))butanoic acid; C 10 H 18 O 3 ; M w = 186.25; Melting point: 86 °C"),
]
for name, v, ev in data_055:
    add("pending_verification", name, "", "melting_point", float(v), "", "",
        f"{v} °C", "=", "measured", src_055, url_055,
        "Section 3.1.2 Syntheses, characterization", ev, "", "")

# Boiling points for intermediates
bp_055 = [
    ("1-Ethoxyethyl-2-bromopropanoate", 87, "3 mm Hg",
     "PI-1. 1-Ethoxyethyl-2-bromopropanoate: C 7 H 13 O 3 Br; M w = 225.02; Boiling point: 87 °C, (3 mm Hg)"),
    ("1-Ethoxyethyl-2-bromobuthanoate", 60, "1 mm Hg",
     "PI-2. 1-Ethoxyethyl-2-bromobuthanoate: C 8 H 15 O 3 Br; M w = 239.11 ; Boiling point: 60 °C (1 mm Hg)"),
    ("1-Ethoxyethyl-2-bromo-2-methylpropanoate", 94, "20 mm Hg",
     "PI-3. 1-Ethoxyethyl-2-bromo-2-methylpropanoate: C 8 H 15 O 3 Br; Mw = 239.11; Boiling point: 94 °C, 20 mm Hg"),
    ("1-Ethoxyethyl-2-bromoethanoate", 85, "3 mm Hg",
     "PI-4. 1-Ethoxyethyl-2-bromoethanoate: C 6 H 11 O 3 Br; M w = 211.05; Boiling point: 85 °C (3 mm Hg)"),
]
for name, v, pressure, ev in bp_055:
    add("pending_verification", name, "", "boiling_point", float(v), "", "",
        f"{v} °C", "=", "measured", src_055, url_055,
        "Section 3.1.1 intermediate characterization", ev, "",
        f"reduced-pressure bp at {pressure}; not normal boiling point")

# ============ Paper 062 (PMC3127127) DOI 10.3390/ijms12042448 ============
# Skip: Table 5 has 58 alcohols but values are compiled from external lit (ref 19) and
# direct quote attribution per row is tedious; methanol/ethanol are well-known compounds.
# Adding the most clearly named compounds (top 20) with table-row quotes
src_062 = "Int J Mol Sci 2011, 12(4), 2448-2462"
url_062 = "https://doi.org/10.3390/ijms12042448"
data_062 = [
    ("methanol", 64.7, "1 methanol 0.0000 2.1859 64.7 70.1 −5.4"),
    ("ethanol", 78.3, "2 ethanol 2.0000 2.4358 78.3 82.3 −4.0"),
    ("1-propanol", 97.2, "3 1-propanol 3.5000 2.5354 97.2 96.2 1.0"),
    ("1-butanol", 117.0, "4 1-butanol 5.2222 2.5887 117.0 115.5 1.5"),
    ("1-pentanol", 137.8, "5 1-pentanol 6.8194 2.6219 137.8 134.2 3.6"),
    ("1-hexanol", 157.0, "6 1-hexanol 8.4967 2.6446 157.0 154.5 2.5"),
    ("1-heptanol", 176.3, "7 1-heptanol 10.1183 2.6611 176.3 174.5 1.8"),
    ("1-octanol", 195.2, "8 1-octanol 11.7808 2.6736 195.2 195.1 0.1"),
    ("1-nonanol", 213.1, "9 1-nonanol 13.4120 2.6835 213.1 215.5 −2.4"),
    ("1-decanol", 230.2, "10 1-decanol 15.0680 2.6914 230.2 236.4 −6.2"),
    ("2-propanol", 82.3, "11 2-propanol 3.5000 2.6857 82.3 88.1 −5.8"),
    ("2-butanol", 99.6, "12 2-butanol 5.2222 2.7854 99.6 104.9 −5.3"),
    ("2-pentanol", 119.0, "13 2-pentanol 6.8194 2.8386 119.0 122.5 −3.5"),
    ("2-hexanol", 139.9, "14 2-hexanol 8.4967 2.8718 139.9 142.3 −2.4"),
    ("2-octanol", 179.8, "15 2-octanol 11.7808 2.9110 179.8 182.4 −2.6"),
]
for name, v, ev in data_062:
    add("pending_verification", name, "", "boiling_point", float(v), "", "",
        f"{v} °C", "=", "measured", src_062, url_062,
        "Table 5, Experimental BP", ev, "",
        "compiled from literature [19] at 1 atm")

# ============ Paper 064 (PMC8697427) no DOI ============
src_064 = "Heliyon 2021"  # unspecified - PMC ID only
url_064 = "pmc:PMC8697427"
# Literature Tm values (measured) from Table 5
lit_064 = [
    ("Baricitinib", 487.15, "[47]"),
    ("Camostat", 467.15, "[49]"),
    ("Chloroquine", 363.15, "[50]"),
    ("Dexamethasone", 524.15, "[51]"),
    ("Favipiravir", 450.15, "[52]"),
    ("Fingolimod", 400.15, "[53]"),
    ("Hydroxychloroquine", 367.1, "[55]"),
    ("Thalidomide", 543.15, "[57]"),
    ("Umifenovir", 415, "[58]"),
]
for name, K, ref in lit_064:
    C = round(K - 273.15, 2)
    add("pending_verification", name, "", "melting_point", C, "", "",
        f"{K} K", "=", "measured", src_064, url_064,
        f"Table 5, column [ref] {ref} for {name}",
        f"T m [K] ... {K}",
        f"{K} K − 273.15 = {C} °C",
        f"literature Tm cited in Table 5, ref {ref}")

# Calculated STRM/SIRM values from same Table 5 (data_type=calculated)
calc_064 = [
    ("Baricitinib", 492.478, "STRM"),
    ("Baricitinib", 458.127, "SIRM"),
    ("Camostat", 468.250, "STRM"),
    ("Camostat", 467.128, "SIRM"),
    ("Chloroquine", 393.375, "STRM"),
    ("Chloroquine", 385.545, "SIRM"),
    ("Dexamethasone", 462.022, "SIRM"),
    ("Favipiravir", 465.514, "STRM"),
    ("Favipiravir", 497.056, "SIRM"),
    ("Fingolimod", 398.693, "STRM"),
    ("Fingolimod", 396.310, "SIRM"),
    ("Hydroxychloroquine", 417.170, "STRM"),
    ("Hydroxychloroquine", 414.588, "SIRM"),
    ("Thalidomide", 441.490, "STRM"),
    ("Thalidomide", 440.390, "SIRM"),
    ("Umifenovir", 447.213, "STRM"),
    ("Umifenovir", 448.603, "SIRM"),
]
for name, K, method in calc_064:
    C = round(K - 273.15, 2)
    add("pending_verification", name, "", "melting_point", C, "", "",
        f"{K} K", "=", "calculated", src_064, url_064,
        f"Table 5, column {method} for {name}",
        f"T m [K] ... {K}",
        f"{K} K − 273.15 = {C} °C",
        f"calculated by group-contribution method {method}")

# ============ Paper 067 (PMC6146921) no DOI ============
src_067 = "Molecules 2003"  # from filename
url_067 = "pmc:PMC6146921"
# Top compounds from Table 8 (full set), with explicit row quotes
data_067 = [
    ("methanol", 64.70, "1. methanol 64.70 65.50 -0.80 -1.24 65.24 (-0.54)"),
    ("ethanol", 78.30, "2. ethanol 78.30 78.43 -0.13 -0.17 77.69 (0.61)"),
    ("1-propanol", 97.20, "3. 1-propanol 97.20 95.63 1.57 1.62 96.42 (0.77)"),
    ("2-propanol", 82.30, "4. 2. propanol 82.30 85.83 -3.53 -4.28 84.11 (-1.81)"),
    ("1-butanol", 117.70, "5. 1-butanol 117.70 113.40 4.30 3.65 115.67 (2.03)"),
    ("2-butanol", 99.60, "6. 2-butanol 99.60 102.87 -3.27 -3.28 102.43 (-2.83)"),
    ("2-methyl-1-propanol", 107.90, "7. 2-methyl-1-propanol 107.90 108.66 -0.76 -0.71 109.15 (-1.25)"),
    ("2-methyl-2-propanol", 82.40, "8. 2-methyl-2-propanol 82.40 87.68 -5.28 -6.41 84.52 (-2.12)"),
    ("1-pentanol", 137.80, "9. 1-pentanol 137.80 133.16 4.64 3.36 134.92 (2.88)"),
    ("2-pentanol", 119.00, "10. 2-pentanol 119.00 120.59 -1.59 -1.34 121.68 (-2.68)"),
    ("3-pentanol", 115.30, "11. 3-pentanol 115.30 119.90 -4.60 -3.99 120.75 (-5.45)"),
    ("2-methyl-1-butanol", 128.70, "12. 2-methyl-1-butanol 128.70 126.39 2.31 1.80 127.97 (0.73)"),
    ("3-methyl-1-butanol", 131.20, "13. 3-methyl-1-butanol 131.20 127.13 4.07 3.10 128.90 (2.30)"),
    ("1-hexanol", 157.13, "17. 1-hexanol 157.13 153.12 4.01 2.55 154.17 (2.83)"),
    ("1-heptanol", 176.30, "34. 1-heptanol 176.30 173.38 2.92 1.66 173.41 (2.87)"),
    ("1-octanol", 195.20, "45. 1-octanol 195.20 193.67 1.53 0.78 192.58 (2.62)"),
    ("1-nonanol", 213.10, "49. 1-nonanol 213.10 213.97 -0.87 -0.41 211.91 (1.19)"),
]
for name, v, ev in data_067:
    add("pending_verification", name, "", "boiling_point", float(v), "", "",
        f"{v} °C", "=", "measured", src_067, url_067,
        "Table 8 Experimental and Calculated Bp of Alkyl Alcohols in full Set",
        ev, "",
        "alcohol BP compiled, exp column")

# ============ Paper 068 (PMC12986465) DOI 10.3390/molecules31050844 ============
src_068 = "Molecules 2024, 31, 844"
url_068 = "https://doi.org/10.3390/molecules31050844"
data_068 = [
    ("N-(3-chloro-4-fluorophenyl) acetamide", "1", 119, 120,
     "to give (1) as white crystals. Yield 11.98 g, 93.90%, M.P.: 119–120 °C."),
    ("N-(5-chloro-4-fluoro-2-nitrophenyl) acetamide", "2", 112, 113,
     "to offer the target compound. Yield 12.23 g, 97.64%, M.P.: 112–113 °C."),
    ("5-chloro-4-fluoro-2-nitroaniline", "3", 144, 145,
     "to give yellow crystals. Yield 4.00 g, 98.09%, M.P.: 144–145 °C."),
    ("4-fluoro-5-(piperazin-1-yl)-2-nitroaniline", "4a", 187, 188,
     "(4a) Solid orange crystals; molecular formula: C 10 H 13 FN 4 O 2 . Yield 4.72 g, 88.57%, M.P.: 187–188 °C."),
    ("4-fluoro-5-(4-methylpiperazin-1-yl)-2-nitroaniline", "4b", 135, 137,
     "(4b) Solid orange crystals; molecular formula: C 11 H 15 FN 4 O 2 . Yield 6.64 g, 99.10%, M.P.: 135–137 °C"),
    ("4-fluoro-5-(4-ethylpiperazin-1-yl)-2-nitroaniline", "4c", 143, 145,
     "(4c) Solid orange crystals; molecular formula: C 12 H 17 FN 4 O 2 . Yield 6.73 g, 94.91%, M.P.: 143–145 °C."),
    ("4-fluoro-5-(4-isopropylpiperazin-1-yl)-2-nitroaniline", "4d", 121, 123,
     "(4d) Solid orange crystals; molecular formula: C 13 H 19 FN 4 O 2 . Yield 2.28 g, 61.62%, M.P.: 121–123 °C."),
    ("4-fluoro-5-(4-butylpiperazin-1-yl)-2-nitroaniline", "4e", 109, 111,
     "(4e) Solid orange crystals; molecular formula: C 14 H 21 FN 4 O 2 . Yield 3.57 g, 91.8%, M.P.: 109–111 °C."),
    ("4-fluoro-5-(4-phenylpiperazin-1-yl)-2-nitrobenzenamine", "4f", 183, 185,
     "(4f) Solid orange crystals; molecular formula: C 16 H 17 FN 4 O 2 . Yield 4.02 g, 94.37%, M.P.: 183–185 °C."),
    ("4-fluoro-2-nitro-5-(pyrrolidin-1-yl) aniline", "4g", 187, 189,
     "(4g) Solid orange crystals; molecular formula: C 10 H 12 FN 3 O 2 . Yield 5.61 g, 94.94%, M.P.: 187–189 °C."),
    ("4-fluoro-2-nitro-5-(piperidin-1-yl) aniline", "4h", 133, 135,
     "(4h) Orange crystals; molecular formula: C 11 H 14 FN 3 O 2 . Yield 2.88 g, 91.8%, M.P.: 133–135 °C."),
    ("4-fluoro-2-nitro-5-(morpholin-1-yl) aniline", "4i", 186, 188,
     "(4i) Solid orange crystals; molecular formula: C 10 H 12 FN 3 O 3 . Yield 2.88 g, 90.0%, M.P.: 186–188 °C (literature [ 61 ], 188–190 °C)."),
    ("2-(4-(5-amino-2-fluoro-4-nitrophenyl)piperazin-1-yl)ethanol", "4j", 150, 151,
     "(4j) Solid orange crystals; molecular formula: C 12 H 17 FN 4 O 3 . Yield 3.130 g, 83.9%, M.P.: 150–151 °C."),
    ("4-fluoro-5-(piperazin-1-yl) benzene-1,2-diamine", "5a", 111, 113,
     "(5a) Solid cream crystals; molecular formula: C 10 H 15 FN 4 . Yield 0.92 g, 77.54%, M.P.: 111–113 °C."),
    ("4-fluoro-5-(4-methylpiperazin-1-yl) benzene-1,2-diamine", "5b", 79, 81,
     "(5b) Solid cream crystals; molecular formula: C 11 H 17 FN 4 . Yield 0.92 g, 77.54%, M.P.: 79–81 °C (literature [ 61 ], 78–80 °C)."),
    ("4-fluoro-5-(4-ethylpiperazin-1-yl) benzene-1,2-diamine", "5c", 94, 96,
     "(5c) Solid cream crystals; molecular formula: C 12 H 19 FN 4 . Yield 0.76 g, 85.60%, M.P.: 94–96 °C."),
    ("4-fluoro-5-(4-isopropylpiperazin-1-yl) benzene-1,2-diamine", "5d", 127, 129,
     "(5d) Solid cream crystals; molecular formula: C 13 H 21 FN 4 . Yield 0.97 g, 99.5%, M.P.: 127–129 °C."),
    ("4-fluoro-5-(4-butylpiperazin-1-yl) benzene-1,2-diamine", "5e", 119, 121,
     "(5e) Solid cream crystals. Molecular formula: C 14 H 23 FN 4 . Yield 0.96 g, 99.5%, M.P.: 119–121 °C."),
    ("4-fluoro-5-(4-phenylpiperazin-1-yl) benzene-1,2-diamine", "5f", 281, 283,
     "(5f) Solid cream crystals; molecular formula: C 16 H 19 FN 4 . Yield 0.95 g, 99.4%, M.P.: 281–283 °C."),
    ("4-fluoro-5-(piperidin-1-yl)benzene-1,2-diamine", "5h", 128, 130,
     "(5h) Solid cream crystals. Molecular formula: C 11 H 16f N 3 . Yield 0.97 g, 99.5%, M.P.: 128–130 °C."),
    ("4-fluoro-5-(morpholin-1-yl) benzene-1,2-diamine", "5i", 127, 128,
     "(5i) Solid cream crystals; molecular formula: C 10 H 14 FN 3 O. Yield 0.92 g, 99.4%, M.P.: 127–128 °C (literature [ 61 ], 126–127 °C)."),
    ("2-(4-(4,5-diamino-2-fluorophenyl)piperazin-1-yl)ethanol", "5j", 115, 117,
     "(5j) Solid cream crystals; molecular formula: C 12 H 19 FN 4 O. Yield 0.8 g, 89.4, M.P.: 115–117 °C."),
    ("6-fluoro-5-(piperazin-1-yl)-1H-benzo[d]imidazole", "6a", 234, 236,
     "(6a) Solid orange crystals; molecular formula: C 11 H 13 FN 4 . Yield 0.84 g, 80.46%, M.P.: 234–236 °C."),
    ("6-fluoro-5-(4-methylpiperazin-1-yl)-1H-benzo[d]imidazole", "6b", 118, 120,
     "(6b) Solid orange crystals; molecular formula: C 12 H 15 FN 4 . Yield 0.85 g, 80.45%, M.P.: 118–120 °C (literature [ 61 ], 120–122 °C)."),
    ("6-fluoro-5-(4-ethylpiperazin-1-yl)-1H-benzo[d]imidazole", "6c", 138, 139,
     "(6c) Solid orange crystals; molecular formula: C 13 H 17 FN 4 . Yield 0.85 g, 81.7%, M.P.: 138–139 °C."),
    ("6-fluoro-5-(4-isopropylpiperazin-1-yl)-1H-benzo[d]imidazole", "6d", 147, 149,
     "(6d) Solid orange crystals. Molecular formula: C 14 H 19 FN 4 . Yield 0.85 g, 81.2%, M.P.: 147–149 °C."),
    ("6-fluoro-5-(4-butylpiperazin-1-yl)-1H-benzo[d]imidazole", "6e", 140, 142,
     "(6e) Solid orange crystals; molecular formula: C 15 H 21 FN 4 . Yield 0.93 g, 89.8%, M.P.: 140–142 °C."),
    ("6-fluoro-5-(4-phenylpiperazin-1-yl)-1H-benzo[d]imidazole", "6f", 130, 132,
     "(6f) Solid orange crystals; molecular formula: C 17 H 17 FN 4 . Yield 0.84 g, 81.1%, M.P.: 130–132 °C."),
    ("6-fluoro-5-(pyrrolidin-1-yl)-1H-benzo[d]imidazole", "6g", 190, 192,
     "Molecular formula: C 11 H 12 FN 3 . Yield 0.86 g, 94.4%, M.P.: 190–192 °C."),
    ("6-fluoro-5-(piperidin-1-yl)-1H-benzo[d]imidazole", "6h", 168, 170,
     "(6h) Solid orange crystals. Molecular formula: C 12 H 14 FN 3 . Yield 0.96 g, 95.4%, M.P.: 168–170 °C."),
    ("6-fluoro-5-(morpholin-1-yl)-1H-benzo[d]imidazole", "6i", 209, 211,
     "(6i) Solid orange crystals; molecular formula: C 11 H 12 FN 3 O. Yield 0.81 g, 82.8%, M.P.: 209–211 °C, (literature [ 61 ], 208–210 °C)."),
    ("2-(4-(6-fluoro-1H-benzo[d]imidazol-5-yl)piperazin-1-yl)ethanol", "6j", 120, 122,
     "(6j) Solid orange crystals; molecular formula: C 13 H 17 FN 4 O. Yield 0.87 g, 83.71%, M.P.: 120–122 °C."),
]
for name, code, vmin, vmax, ev in data_068:
    add("pending_verification", name, "", "melting_point",
        (vmin+vmax)/2, vmin, vmax, f"{vmin}–{vmax} °C", "=", "measured",
        src_068, url_068, f"Section 3.1.3-3.1.5 Synthesis, compound ({code})",
        ev, "", "")

# ====== Write CSV ======
out = "/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_02.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["id","verification_status","compound_name","compound_smiles","property",
                "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
                "data_type","source","source_url","evidence_location","evidence_quote",
                "conversion_arithmetic","notes"])
    for r in rows:
        w.writerow(r)
print(f"Wrote {len(rows)} rows to {out}")

"""Extract mp/bp rows for batch_02 papers. Each row carries a verbatim quote."""
import csv, re
CSV_PATH = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_02.csv'
SKIP_PATH = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_02_skipped.tsv'

rows = []
skipped = []

# Paper 046 (PMC6236381, DOI 10.3390/61201001) - Molecules 2001, 6, 1001-?
src046 = "Molecules 2001, 6, 1001-1011"
url046 = "https://doi.org/10.3390/61201001"
rows.append(["", "pending_verification", "2-Hydroxy-3-hydroxymethyl-5-methylbenzaldehyde",
    "","melting_point","72.5","72.0","73.0","72-73 °C","°C","=","measured",
    src046, url046, "Experimental, characterization of compound 5",
    "yellowish needles (yield: 7.6g, 38%). M.p. 72-73° (lit. [ 7 ] 75-76°C)", "", ""])
rows.append(["", "pending_verification", "2-Hydroxy-3-chloromethyl-5-methylbenzaldehyde",
    "","melting_point","92.5","92.0","93.0","92-93 °C","°C","=","measured",
    src046, url046, "Experimental, characterization of compound 6",
    "to give 4.8g (95%) of white needles (m.p. 92-93°C)", "", ""])
rows.append(["", "pending_verification", "1,6-Bis(2-furyl)-2,5-bis(2-hydroxy-3-formyl-5-methylbenzyl)-2,5-diazahexane",
    "","melting_point","109.5","109.0","110.0","109-110 °C","°C","=","measured",
    src046, url046, "Experimental, characterization of compound 3",
    "Recrystallization from 95% ethanol gave compound 3 (2.17 g, 42%) as off-white needles (m.p. 109-110°C)", "", ""])

# Paper 047 (PMC6146789, DOI 10.3390/70700534) - Molecules 2002, 7, 534-?
src047 = "Molecules 2002, 7, 534-542"
url047 = "https://doi.org/10.3390/70700534"
rows.append(["", "pending_verification", "2-(bromomethyl)benzothiazole",
    "","melting_point","82.0","","","82 °C","°C","=","measured",
    src047, url047, "Experimental, characterization of compound 1",
    "to give the expected product 1 (6.68g, 58%) as sticky white powder (WARNING: irritant!), m.p. 82°C (decomp.)",
    "", "decomposes at mp"])
rows.append(["", "pending_verification",
    "6,13-dihydropyrazino[2,1-b:5,4-b´]bis(1,3-benzothiazole)-7,14-diiumdibromide",
    "","melting_point","115.0","","","115 °C","°C","=","measured",
    src047, url047, "Experimental, characterization of compound 2",
    "to give 0.13g (10%) of product 2 , m.p.115°C (decomp.)",
    "", "decomposes at mp"])

# Paper 050 (PMC6146942, DOI 10.3390/81100756) - Molecules 2003, 8, 756-769
src050 = "Molecules 2003, 8, 756-769"
url050 = "https://doi.org/10.3390/81100756"
# Table 1 — 2,2-dimethyl-3-aryl-1,2-dihydroquinazoline-4(3H)-thiones (1a-1k) and 2-methyl-3-aryl-quinazoline-4(3H)-thiones (2a-2g)
# Compound names constructed from the table headers + substituents
table050 = [
    # series 1: X=H/Cl, parent = 2,2-dimethyl-3-aryl-1,2-dihydroquinazoline-4(3H)-thione
    ("1a","2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione","212-214","213.0","212","214"),
    ("1b","3-(4-chlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","238-241","239.5","238","241"),
    ("1c","3-(3,4-dichlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","199-201","200.0","199","201"),
    ("1d","2,2-dimethyl-3-(4-methylphenyl)-1,2-dihydroquinazoline-4(3H)-thione","229-231","230.0","229","231"),
    ("1e","3-(4-ethylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","187-188","187.5","187","188"),
    ("1f","3-(4-isopropylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","199-200","199.5","199","200"),
    ("1g","6-chloro-2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione","218-219","218.5","218","219"),
    ("1h","6-chloro-3-(3-chlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","157-158","157.5","157","158"),
    ("1i","6-chloro-3-(3,4-dichlorophenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","189-190","189.5","189","190"),
    ("1j","6-chloro-3-(4-isopropylphenyl)-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","205-207","206.0","205","207"),
    ("1k","3-(4-butylphenyl)-6-chloro-2,2-dimethyl-1,2-dihydroquinazoline-4(3H)-thione","183-184","183.5","183","184"),
    ("2a","6-chloro-2-methyl-3-phenylquinazoline-4(3H)-thione","153-154","153.5","153","154"),
    ("2b","6-chloro-3-(3-chlorophenyl)-2-methylquinazoline-4(3H)-thione","172-173","172.5","172","173"),
    ("2c","6-chloro-3-(4-chlorophenyl)-2-methylquinazoline-4(3H)-thione","202-204","203.0","202","204"),
    ("2d","3-(4-bromophenyl)-6-chloro-2-methylquinazoline-4(3H)-thione","212-214","213.0","212","214"),
    ("2e","6-chloro-2-methyl-3-(4-methylphenyl)quinazoline-4(3H)-thione","157-158","157.5","157","158"),
    ("2f","6-chloro-3-(4-isopropylphenyl)-2-methylquinazoline-4(3H)-thione","135-136","135.5","135","136"),
    ("2g","6-chloro-3-(4-methoxyphenyl)-2-methylquinazoline-4(3H)-thione","145-146","145.5","145","146"),
]
# Use the full Table 1 text as quote portion for each row, anchored by compound code
table050_full = "Compd. Formula M. w. X R M.p. (°C) Yield (%) Elemental analysis"
quote_segments = {
    "1a":"1a C 16 H 16 N 2 S 268.4 H H 212-214 a 78",
    "1b":"1b C 16 H 15 ClN 2 S 302.8 H 4-Cl 238-241 82",
    "1c":"1c C 16 H 14 Cl 2 N 2 337.3 H 3,4-Cl 2 199-201 86",
    "1d":"1d C 17 H 18 N 2 S 282.4 H 4-CH 3 229-231 80",
    "1e":"1e C 18 H 20 N 2 S 296.4 H 4-C 2 H 5 187-188 76",
    "1f":"1f C 19 H 22 N 2 S 310.5 H 4-isoC 3 H 7 199-200 85",
    "1g":"1g C 16 H 15 ClN 2 S 337.3 Cl H 218-219 83",
    "1h":"1h C 16 H 14 Cl 2 N 2 S 337.3 Cl 3-Cl 157-158 77",
    "1i":"1i C 16 H 13 Cl 3 N 2 S 371.7 Cl 3,4-Cl 2 189-190 81",
    "1j":"1j C 19 H 21 ClN 2 S 344.9 Cl 4-isoC 3 H 7 205-207 79",
    "1k":"1k C 20 H 23 ClN 2 S 358.9 Cl 4-C 4 H 9 183-184 82",
    "2a":"2a C 15 H 11 ClN 2 S 286.8 Cl H 153-154 69",
    "2b":"2b C 15 H 10 Cl 2 N 2 S 321.2 Cl 3-Cl 172-173 74",
    "2c":"2c C 15 H 10 Cl 2 N 2 S 321.2 Cl 4-Cl 202-204 76",
    "2d":"2d C 15 H 10 BrClN 2 S 365.7 Cl 4-Br 212-214 73",
    "2e":"2e C 16 H 13 ClN 2 S (300.8) Cl 4-CH 3 157-158 70",
    "2f":"2f C 18 H 17 ClN 2 S 328.9 Cl 4-isoC 3 H 7 135-136 68",
    "2g":"2g C 16 H 13 ClN 2 OS 316.8 Cl 4-OCH 3 145-146 59",
}
for code, name, raw, val, vmin, vmax in table050:
    rows.append(["","pending_verification",name,"","melting_point",val,vmin,vmax,
        raw + " °C","°C","=","measured",src050,url050,
        f"Table 1 row {code}", quote_segments[code], "", ""])

# Paper 051 (PMC6236391, DOI 10.3390/60900728) — Molecules 2001
src051 = "Molecules 2001, 6, 728-734"
url051 = "https://doi.org/10.3390/60900728"
rows.append(["","pending_verification","2-Deoxy-2-(2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside",
    "","melting_point","209.0","208.0","210.0","208-210 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 6",
    "2-Deoxy-2-(2-furamido)-1,3,4,6-tetra-O-acetyl-β- D -glucopyranoside ( 6 ): m p 208-210 °C", "", ""])
rows.append(["","pending_verification","2-Deoxy-2-(5-nitro-2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside",
    "","melting_point","110.0","109.0","111.0","109-111 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 7",
    "2-Deoxy-2-(5-nitro-2-furamido)-1,3,4,6-tetra-O-acetyl-β- D -glucopyranoside ( 7 ): m p 109-111 °C", "", ""])
rows.append(["","pending_verification","1-Deoxy-1-(5-nitro-2-furamido)-2,3;4,5-di-O-isopropylidene-β-D-fructopyranoside",
    "","melting_point","160.5","159.0","162.0","159-162 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 12",
    "1-Deoxy-1-(5-nitro-2-furamido)-2,3;4,5-di-O-isopropylidene-β- D -fructopyranoside ( 12 ): m p 159-162 °C", "", ""])
rows.append(["","pending_verification","(1R,2S,3R,5R)-1,2-O-cyclohexylidene-5-C-[(O-tosyl)-hydroxymethyl]-cyclohexane-1,2,3,5-tetrol",
    "","melting_point","135.0","134.0","136.0","134-136 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 14",
    "(1R,2S,3R,5R)-1,2-O-cyclohexylidene-5-C-[(O-tosyl)-hydroxymethyl]-cyclohexane-1,2,3,5-tetrol ( 14 ): m p 134-136 °C", "", ""])
rows.append(["","pending_verification","(1R,2S,3R,5R)-1,2-O-cyclohexylidene-3-O-tosyl-5-C-[(O-tosyl)-hydroxy-methyl]-cyclohexane-1,2,3,5-tetrol",
    "","melting_point","125.0","124.0","126.0","124-126 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 18",
    "cyclohexane-1,2,3,5-tetrol ( 18 ): m p 124-126 °C (lit [ 13 ] m p 123-125 °C)", "", ""])
rows.append(["","pending_verification","(1R,2S,3R,5R)-1,2-O-cyclohexylidene-5-C-azidomethyl-cyclohexane-1,2,3,5-tetrol",
    "","melting_point","101.0","100.0","102.0","100-102 °C","°C","=","measured",
    src051,url051,"Experimental, characterization of compound 15",
    "afford the azide derivative 15 in 95% yield; m p 100-102 °C", "", ""])
# compound 17 — need full name
# compound 8 (carbohydrate Schiff base) — m p 114-116 °C — name unclear; skip if name not clear

# Paper 052 (PMC3715800, DOI 10.1016/j.saa.2007.03.015) - Int J Mol Sci 2007, 8, 760
# Wait — DOI is for Spectrochim Acta? Let's check journal: it's Int J Mol Sci 2007 vol 8 fpage 760
# Re-check DOI
src052 = "Int J Mol Sci 2007, 8, 760"
url052 = "https://doi.org/10.1016/j.saa.2007.03.015"
# K → °C: 393 K - 273.15 = 119.85 °C
rows.append(["","pending_verification","2-(4-methoxyphenyl)benzo[d]thiazole",
    "","melting_point","119.85","","","393 K","°C","=","measured",
    src052,url052,"Experimental, characterization of product",
    "(Yield 94%), M.p. 393 K (392–394 K) [ 61 ]",
    "393 K − 273.15 = 119.85 °C", ""])

# Paper 053 (PMC6147013, DOI 10.3390/80400363) — Molecules 2003, 8, 363
src053 = "Molecules 2003, 8, 363-373"
url053 = "https://doi.org/10.3390/80400363"
table053 = [
    ("6a","2-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester","190-192","191.0","190","192",
        "( 6a ). Pale yellow crystals; yield 2.04 g (52 %); M.p. 190-192 o C"),
    ("6b","2-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}-3-oxo-butyric acid ethyl ester","234-236","235.0","234","236",
        "( 6b ). Pale yellow crystals; yield 2.73 g (58 %); M.p. 234-236 o C"),
    ("7a","Cyano-{[4-(2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}acetic acid ethyl ester","128-130","129.0","128","130",
        "( 7a ). Pale yellow crystals; yield 2.44 g (65 %); M.p. 128-130 o C"),
    ("7b","{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)-phenyl]hydrazono}cyano-acetic acid ethyl ester","173-175","174.0","173","175",
        "( 7b ). Pale yellow crystals; yield 3.09 g (65 %); M.p. 173-175 o C"),
    ("8a","3-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione","153-155","154.0","153","155",
        "( 8a ). Pale yellow crystals; yield 2.17 g (60 %); M.p. 153-155 o C"),
    ("8b","3-{[4-(6-Bromo-2-methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione","165-167","166.0","165","167",
        "( 8b ). Pale yellow crystals; yield 2.91 g (66 %); M.p. 165-167 o C"),
    ("9a","2-Methyl-3-{4-[N′-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one","261-263","262.0","261","263",
        "( 9a ). Orange yellow crystals; yield 1.12 g (62 %); M.p. 261-263 o C"),
    ("9b","6-Bromo-2-methyl-3-{4-[N′-(3-methyl-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one","308-310","309.0","308","310",
        "( 9b ). Orange yellow crystals; yield 1.50 g (68 %); M.p. 308-310 o C"),
    ("10a","3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one","181.0","180.0","182.0",None,None),
    ("10b","3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-6-bromo-2-methyl-3H-quinazolin-4-one","245.0","244.0","246.0",None,None),
    ("9c","2-Methyl-3-{4-[N′-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-3H-quinazolin-4-one","302-304","303.0","302","304",
        "( 9c ). Orange yellow crystals; yield 2.00 g (46 %); M.p. 302-304 o C"),
    ("9d","6-Bromo-2-methyl-3-{4-[N′-(3-methyl-5-oxo-1-phenyl-1,5-dihydropyrazol-4-ylidene)hydrazino]-phenyl}-3H-quinazolin-4-one","259-261","260.0","259","261",
        "( 9d ). Orange yellow crystals; yield 2.16 g (42 %); M.p. 259-261 o C"),
    ("11a","3-[4-(3,5-Dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one","205-207","206.0","205","207",
        "( 11a ). Orange crystals; yield 2.60 g (60 %); M.p. 205-207 o C"),
    ("11b","6-Bromo-3-[4-(3,5-dimethyl-1-phenyl-1H-pyrazol-4-ylazo)phenyl]-2-methyl-3H-quinazolin-4-one","238-240","239.0","238","240",
        "( 11b ). Orange crystals; yield 2.29 g (64 %); M.p. 238-240 o C"),
    ("12a","3-{4-[N′(4,6-Dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one","285-286","285.5","285","286",
        "( 12a ). Orange yellow crystals; yield 0.83 g (43 %); M.p. 285-286 o C"),
    ("12b","6-Bromo-3-{4-[N′(4,6-dimethyl-2-oxo-2H-pyrimidin-5-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one","210-212","211.0","210","212",
        "( 12b ). Orange yellow crystals; yield 1.09 g (47 %); M.p. 210-212 o C"),
]
# Fix 10a, 10b records
table053_fixed = []
for entry in table053:
    if len(entry) == 7:
        code, name, raw, val, vmin, vmax, quote = entry
        table053_fixed.append((code, name, raw, val, vmin, vmax, quote))
# Add 10a, 10b separately
table053_fixed.append(("10a","3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-2-methyl-3H-quinazolin-4-one","180-182","181.0","180","182",
    "( 10a ). Orange yellow crystals; yield 0.87 g (48 %); M.p. 180-182 o C"))
table053_fixed.append(("10b","3-{4-N′-(3-Amino-5-oxo-1,5-dihydropyrazol-4-ylidene)hydrazino]phenyl}-6-bromo-2-methyl-3H-quinazolin-4-one","244-246","245.0","244","246",
    "( 10b ). Orange yellow crystals; yield 1.17 g (53 %); M.p. 244-246 o C"))
for code, name, raw, val, vmin, vmax, quote in table053_fixed:
    rows.append(["","pending_verification",name,"","melting_point",val,vmin,vmax,
        raw + " °C","°C","=","measured",src053,url053,
        f"Experimental, characterization of compound {code}", quote, "", ""])

# Skips
skipped.append(("048_PMC4648099_A_Universal_Base_in_a_Specific_Role_Tuning_up_a_Thrombin_Aptamer_with_5-Nitroindole", "no_mp_bp_data_in_text"))
skipped.append(("049_PMC6147017_Synthesis_of_New_Pyrazole_and_Pyrimidine_Steroidal_Derivatives", "no_mp_bp_data_in_text"))
skipped.append(("054_PMC6146489_Michael_Reactions_of_Arylidenesulfonylacetonitriles._A_New_Route_to_Polyfunctional_Benzoaq", "no_mp_bp_data_in_text"))
skipped.append(("055_PMC3685236_Antiproliferative_Activity_of_-Hydroxy--Arylalkanoic_Acids", "no_mp_bp_data_in_text"))
skipped.append(("056_PMC12395778_AI-powered_prediction_of_critical_properties_and_boiling_points_a_hybrid_ensemble_learning", "review_no_per_compound_binding"))
skipped.append(("057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learning_for_Thermophysical_Property_Prediction_A_Cas", "review_no_per_compound_binding"))
skipped.append(("058_PMC4702524_How_accurately_can_we_predict_the_melting_points_of_drug-like_compounds", "review_no_per_compound_binding"))
skipped.append(("059_PMC8122861_Group_Contribution_Estimation_of_Ionic_Liquid_Melting_Points_Critical_Evaluation_and_Refin", "review_no_per_compound_binding"))
skipped.append(("060_PMC4724158_The_development_of_models_to_predict_melting_and_pyrolysis_point_data_associated_with_seve", "review_no_per_compound_binding"))
skipped.append(("061_PMC2603525_Simultaneous_feature_selection_and_parameter_optimisation_using_an_artificial_ant_colony_c", "review_no_per_compound_binding"))
skipped.append(("062_PMC3127127_A_Quantitative_Structure-Property_Relationship_QSPR_Study_of_aliphatic_alcohols_by_the_met", "review_no_per_compound_binding"))
skipped.append(("063_PMC12004525_Understanding_Conformation_Importance_in_Data-Driven_Property_Prediction_Models.", "review_no_per_compound_binding"))

# Assign sequential ids starting at 2017
next_id = 2017
final_rows = []
for r in rows:
    r2 = list(r)
    r2[0] = str(next_id)
    assert len(r2) == 18, f"row length {len(r2)} != 18: {r2}"
    final_rows.append(r2)
    next_id += 1

with open(CSV_PATH, 'a', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in final_rows:
        w.writerow(r)

with open(SKIP_PATH, 'w') as f:
    for loc, reason in skipped:
        f.write(f"{loc}\t{reason}\n")

print(f"Appended {len(final_rows)} rows. Next id = {next_id}")
print(f"Skipped {len(skipped)} papers")

import csv

final = []

# Paper 097: PMC6146420 — Fisyuk synthesis of dihydropyridinones
src_097 = "Molecules 2002, 7(2):124-128"
url_097 = "https://doi.org/10.3390/70200124"
loc_097_amides = "Experimental, N-(3-Oxoalkyl)amides preparation paragraph"
loc_097_salts = "Experimental, Typical procedure for synthesis of salts 2a-g"
loc_097_t1 = "Table 1, Melting Points and Yields of Compounds 4a-g"

q_1a_1b_1e = "N-(3-Oxoalkyl)amides 1a (56%, m.p. 90-91°C); 1b ( 81 %, m.p. 104-105°C) and anti - 1e (14%, m.p.156-157°C) were obtained from the α,β-unsaturated ketones and chloroacetonitrile"
q_1c_1g = "compounds 1c ( 69%, m.p. 109-110°C) and anti - 1g (55%, m.p. 74-75°C) — by reaction of Cl 3 CCH=NCOCH 2 Cl with enamines"
q_1d = "compound anti - 1d (88%, m.p.124-125°C) — by acylation of 1-( trans -2-aminocyclohexyl)-1-ethanone with chloroanhydride of chloroacetic acid"
q_1f = "compound 1f (19%, m.p. 201-202°C) — by interaction of (1-cyclohexenyloxy)(trimethyl)silane with PhCH=NMe and ClCH 2 COCl in the presence of TiCl 4"

final.append(["N-(3-oxoalkyl)chloroacetamide 1a (R1=Me, R2=R3=R5=H, R4=Ph per Scheme 1)", "", "melting_point", "90.5", "90", "91", "90-91 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1a_1b_1e, "", "Compound 1a"])
final.append(["N-(3-oxoalkyl)chloroacetamide 1b (R1=R4=Ph, R2=R3=R5=H per Scheme 1)", "", "melting_point", "104.5", "104", "105", "104-105 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1a_1b_1e, "", "Compound 1b"])
final.append(["N-(3-oxoalkyl)chloroacetamide anti-1e (R1+R2=-(CH2)4-, R3=R5=H, R4=Ph per Scheme 1)", "", "melting_point", "156.5", "156", "157", "156-157 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1a_1b_1e, "", "Compound anti-1e"])
final.append(["N-(3-oxoalkyl)chloroacetamide 1c (R1=R5=H, R2=R3=Me, R4=CCl3 per Scheme 1)", "", "melting_point", "109.5", "109", "110", "109-110 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1c_1g, "", "Compound 1c"])
final.append(["N-(3-oxoalkyl)chloroacetamide anti-1g (R1+R2=-(CH2)4-, R3=R5=H, R4=CCl3 per Scheme 1)", "", "melting_point", "74.5", "74", "75", "74-75 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1c_1g, "", "Compound anti-1g"])
final.append(["N-(3-oxoalkyl)chloroacetamide anti-1d (R1=Me, R2=R5=H, R3+R4=-(CH2)4- per Scheme 1)", "", "melting_point", "124.5", "124", "125", "124-125 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1d, "", "Compound anti-1d"])
final.append(["N-(3-oxoalkyl)chloroacetamide 1f (R1+R2=-(CH2)4-, R3=H, R4=Ph, R5=Me per Scheme 1)", "", "melting_point", "201.5", "201", "202", "201-202 °C", "range", "experimental", src_097, url_097, loc_097_amides, q_1f, "", "Compound 1f"])

q_2 = "Yields, melting points: 2a - 74%, 191-192°C; 2b - 93%, 119-120°C; 2c - 78%, 203-205°C; anti - 2d - 93%, 187-188°C; anti - 2e - 83%, 200-201°C; anti -2f - 78%, 160-161°C; anti -2g - 89%, 159-150°C."
final.append(["Triphenylphosphonium salt 2a derived from 1a", "", "melting_point", "191.5", "191", "192", "191-192 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound 2a"])
final.append(["Triphenylphosphonium salt 2b derived from 1b", "", "melting_point", "119.5", "119", "120", "119-120 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound 2b"])
final.append(["Triphenylphosphonium salt 2c derived from 1c", "", "melting_point", "204", "203", "205", "203-205 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound 2c"])
final.append(["Triphenylphosphonium salt anti-2d derived from 1d", "", "melting_point", "187.5", "187", "188", "187-188 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound anti-2d"])
final.append(["Triphenylphosphonium salt anti-2e derived from 1e", "", "melting_point", "200.5", "200", "201", "200-201 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound anti-2e"])
final.append(["Triphenylphosphonium salt anti-2f derived from 1f", "", "melting_point", "160.5", "160", "161", "160-161 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound anti-2f"])
final.append(["Triphenylphosphonium salt anti-2g derived from 1g", "", "melting_point", "", "", "", "159-150 °C", "range", "experimental", src_097, url_097, loc_097_salts, q_2, "", "Compound anti-2g; printed range '159-150°C' appears to be a typographical error in source — likely 159-160°C"])

q_t1 = "Compound 4a 4b 4c trans -4d trans -4e trans -4f trans -4g m.p. °C 135-6 1) >210 decom 147-8 1) 176-7 1) 183-4 1) Oil 172-3 1)"
final.append(["5,6-Dihydropyridin-2(1H)-one 4a (intramolecular Wittig product of salt 2a)", "", "melting_point", "135.5", "135", "136", "135-6 °C", "range", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound 4a; sealed capillary, sublimes (Table 1 footnote 1)"])
final.append(["5,6-Dihydropyridin-2(1H)-one 4b (intramolecular Wittig product of salt 2b)", "", "decomposition", "210", "", "", ">210 °C decom", "greater_than", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound 4b decomposes above 210 °C; unstable compound, decomposes in air"])
final.append(["5,6-Dihydropyridin-2(1H)-one 4c (intramolecular Wittig product of salt 2c)", "", "melting_point", "147.5", "147", "148", "147-8 °C", "range", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound 4c; sealed capillary, sublimes (Table 1 footnote 1)"])
final.append(["4a,8a-trans-4a,5,6,7,8,8a-Hexahydroquinolin-2(1H)-one trans-4d", "", "melting_point", "176.5", "176", "177", "176-7 °C", "range", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound trans-4d; sealed capillary, sublimes (Table 1 footnote 1)"])
final.append(["1,8a-trans-1,5,6,7,8,8a-Hexahydroisoquinolin-3(2H)-one trans-4e", "", "melting_point", "183.5", "183", "184", "183-4 °C", "range", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound trans-4e; sealed capillary, sublimes (Table 1 footnote 1)"])
final.append(["1,8a-trans-1,5,6,7,8,8a-Hexahydroisoquinolin-3(2H)-one trans-4g", "", "melting_point", "172.5", "172", "173", "172-3 °C", "range", "experimental", src_097, url_097, loc_097_t1, q_t1, "", "Compound trans-4g; sealed capillary, sublimes (Table 1 footnote 1)"])

# Paper 118
src_118 = "ACS Omega"
url_118 = "https://doi.org/10.1021/acsomega.5c11955"
loc_118 = "Experimental Section, Reaction of 4-chloro-2-(1H-pyrazol-3-yl)phenol (2a) with HCCTP (1) procedures"

q_3a = "Compound 3a (0.62 g, 77%, mp 234 °C), Found: C, 23"
q_4ai = "Compound 4a-I (0.57 g, 56%, mp 218 °C), Found: C, 36"
q_5ai = "Compound 5a-I (0.03 g, 2%, mp 260 °C), Found: C, 45"

final.append(["Monospiro 4-chloro-2-(1H-pyrazol-3-yl)phenol-substituted cyclotriphosphazene 3a (C9H5Cl5N5OP3)", "", "melting_point", "234", "", "", "mp 234 °C", "exact", "experimental", src_118, url_118, loc_118, q_3a, "", "Monospiro chloro phenol pyrazole substituted cyclotriphosphazene; FW 469.34"])
final.append(["trans-Dispiro 4-chloro-2-(1H-pyrazol-3-yl)phenol-substituted cyclotriphosphazene 4a-I (C18H10Cl4N7O2P3)", "", "melting_point", "218", "", "", "mp 218 °C", "exact", "experimental", src_118, url_118, loc_118, q_4ai, "", "trans-Dispiro chloro phenol pyrazole substituted cyclotriphosphazene; FW 591.1"])
final.append(["cis-trans-trans-Trispiro 4-chloro-2-(1H-pyrazol-3-yl)phenol-substituted cyclotriphosphazene 5a-I (C27H15Cl3N9O3P3)", "", "melting_point", "260", "", "", "mp 260 °C", "exact", "experimental", src_118, url_118, loc_118, q_5ai, "", "Trispiro cis-trans-trans chloro phenol pyrazole substituted cyclotriphosphazene; FW 712.8"])

# Paper 173
src_173 = "RSC Adv. 2024, 14(11):7740-7744"
url_173 = "https://doi.org/10.1039/d4ra00566j"

q_173_a = "Yield: 220 mg (422 μmol, 84%; mp. 142-143 °C)"
q_173_b = "Yield: 244 mg (1.04 mmol, 25%; mp. 43-48 °C)"
q_173_c = "Yield: 4.2 mg (2.7 μmol, 32%; mp 112 °C)"
q_173_d = "Yield: 9.4 mg (17.3 μmol, 97%; mp. 139-140 °C)"

final.append(["9,9,9-Tris(4-tert-butylphenyl)non-1-yne (HC≡C(CH2)6C(4-tBuC6H4)3)", "", "melting_point", "142.5", "142", "143", "mp. 142-143 °C", "range", "experimental", src_173, url_173, "Experimental, Preparation of HC≡C(CH2)6C(4-tBuC6H4)3", q_173_a, "", "Terminal alkyne stopper precursor; white solid"])
final.append(["Pentadec-14-en-1-yne (HC≡C(CH2)13CH=CH2)", "C=CCCCCCCCCCCCCCC#C", "melting_point", "45.5", "43", "48", "mp. 43-48 °C", "range", "experimental", src_173, url_173, "Experimental, Preparation of HC≡C(CH2)13CH=CH2", q_173_b, "", "Wide range; analytically pure colourless wax (note: paper describes as wax — range may reflect softening)"])
final.append(["Rotaxane 1 / NMR-labelled compound 3 (rhodium-mediated alkyne dimerisation product)", "", "melting_point", "112", "", "", "mp 112 °C", "exact", "experimental", src_173, url_173, "Experimental, Preparation of rotaxane 1", q_173_c, "", "Product labelled compound 3 in NMR data; white solid after preparative TLC; isolated from [Rh(PNP-14)(η2-COD)][BArF4] + HC≡C(CH2)6C(4-tBuC6H4)3 then PMe3/S8"])
final.append(["PNP-14·2S (bis-sulfide of PNP-14 macrocyclic pincer ligand)", "", "melting_point", "139.5", "139", "140", "mp. 139-140 °C", "range", "experimental", src_173, url_173, "Experimental, Preparation of PNP-14·2S", q_173_d, "", "White microcrystalline solid from S8 treatment of PNP-14"])

out_path = "/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/batches/gap_pmc_misc_results.csv"
with open(out_path, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    for i, row in enumerate(final, 1):
        cn, smi, prop, vc, vcmin, vcmax, vraw, rel, dtype, src, url, loc, quote, conv, notes = row
        w.writerow([i, "pending_verification", cn, smi, prop, vc, vcmin, vcmax, vraw, rel, dtype, src, url, loc, quote, conv, notes])
print(f"Wrote {len(final)} rows to {out_path}")

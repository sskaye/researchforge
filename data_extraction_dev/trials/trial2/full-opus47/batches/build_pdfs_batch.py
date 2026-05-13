import csv
rows = []
def add(**kwargs):
    base = {'id': len(rows)+1,'verification_status': 'pending_verification','compound_name': '','compound_smiles': '','property': '','value_celsius': '','value_celsius_min': '','value_celsius_max': '','value_raw': '','relation': '=','data_type': 'measured','source': '','source_url': '','evidence_location': '','evidence_quote': '','conversion_arithmetic': '','notes': '',}
    base.update(kwargs)
    rows.append(base)

src_1952 = "J. Am. Chem. Soc. 1952, 74, 5781"
url_1952 = "legacy:1952_Livingston_The_Molecular_Structures_of_Octafluorocyclobutane_and_of_Methylcyclobutane.pdf"
add(compound_name="methylcyclobutane", property="melting_point", value_celsius=-161.51, value_raw="-161.51 °C", source=src_1952, source_url=url_1952, evidence_location="p.5781, Experimental", evidence_quote="f . p . -161.51")
add(compound_name="methylcyclobutane", property="boiling_point", value_celsius=36.98, value_raw="36.98 °C (755 mm)", source=src_1952, source_url=url_1952, evidence_location="p.5781, Experimental", evidence_quote="b p . :3F.98\" (755 nini.) arid 37.1XD(760 inni.)", notes="bp at 755 mm Hg")
add(compound_name="methylcyclobutane", property="boiling_point", value_celsius=37.18, value_raw="37.18 °C (760 mm)", source=src_1952, source_url=url_1952, evidence_location="p.5781, Experimental", evidence_quote="b p . :3F.98\" (755 nini.) arid 37.1XD(760 inni.)", notes="bp at 760 mm Hg")
add(compound_name="octafluorocyclobutane", property="boiling_point", value_celsius=-6.05, value_celsius_min=-6.1, value_celsius_max=-6.0, value_raw="-6.1 to -6.0 °C", source=src_1952, source_url=url_1952, evidence_location="p.5781, Experimental", evidence_quote="octufluoro lobuta11e ( t ) . l ) . ---6.1\" tu", notes="OCR rendering of b.p. -6.1 to -6.0")

src_1990 = "Pharm. Res. 1990, 7, 942"
url_1990 = "legacy:1990_Yalkowsky_Melting_Point_Boiling_Point_and_Symmetry.pdf"
t1_1990 = [("1,2-Dichlorobenzene", -17, 179), ("1,3-Dichlorobenzene", -25, 172), ("1,4-Dichlorobenzene", 53, 175),("1,2-Dibromobenzene", 7, 225), ("1,3-Dibromobenzene", -7, 220), ("1,4-Dibromobenzene", 87, 220),("1,2-Diiodobenzene", 27, 286), ("1,3-Diiodobenzene", 40, 285), ("1,4-Diiodobenzene", 132, 285),("1,2,3-Trichlorobenzene", 53, 218), ("1,2,4-Trichlorobenzene", 17, 213), ("1,3,5-Trichlorobenzene", 63, 208)]
for cname, mp, bp in t1_1990:
    add(compound_name=cname, property="melting_point", value_celsius=mp, value_raw=f"{mp} °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote=f"{cname}", notes="Table I MP (OCR'd from image-only PDF)")
    add(compound_name=cname, property="boiling_point", value_celsius=bp, value_raw=f"{bp} °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote=f"{cname}", notes="Table I BP (OCR'd)")
add(compound_name="2-pentanone (methyl propyl ketone)", property="melting_point", value_celsius=-78, value_raw="-78 °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote="Methylpropylketone")
add(compound_name="2-pentanone (methyl propyl ketone)", property="boiling_point", value_celsius=102, value_raw="102 °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote="Methylpropylketone")
add(compound_name="3-pentanone (diethyl ketone)", property="melting_point", value_celsius=-40, value_raw="-40 °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote="Diethylketone")
add(compound_name="3-pentanone (diethyl ketone)", property="boiling_point", value_celsius=101.7, value_raw="101.7 °C", source=src_1990, source_url=url_1990, evidence_location="Table I", evidence_quote="Diethylketone")

src_2000 = "J. Chem. Educ. 2000, 77, 724"
url_2000 = "https://doi.org/10.1021/ed077p724"
for cname, mp_k in [("pentane",143.5),("methylbutane",113.3),("2,2-dimethylpropane",256.6),("octane",216.4),("3-methylheptane",152.7),("hexamethylethane",373.9),("methylcyclopentane",130.7),("2,3-dimethyl-2-butene",198.6),("cyclohexane",279.8),("methylcyclohexane",146.6),("1-heptene",153.5),("cycloheptane",265.2),("1,1-dichloroethane",176.2),("1,2-dichloroethane",237.7),("1-propanol",147.1),("2-propanol",183.7),("1-butanol",183.3),("2-methyl-1-propanol",165),("2-methyl-2-propanol",298.5),("o-dichlorobenzene",256.5),("m-dichlorobenzene",248.4),("p-dichlorobenzene",325.9),("o-xylene",248.0),("m-xylene",225.4),("p-xylene",286.4),("ethylcyclohexane",161.9),("1,1-dimethylcyclohexane",239.9),("cyclooctane",288.0),("cyclooctatetraene",268.5),("cubane",405),("phenanthrene",372.4),("anthracene",488)]:
    mp_c = round(mp_k - 273.15, 2)
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_k} K", source=src_2000, source_url=url_2000, evidence_location="Table 1", evidence_quote=f"{cname}", conversion_arithmetic=f"{mp_k} K - 273.15 = {mp_c} °C", notes="Table 1")
for cname, mp_k in [("benzene",278.7),("toluene",178.2),("fluorobenzene",231),("chlorobenzene",228.0),("bromobenzene",242.6),("iodobenzene",241.9),("phenol",314.1),("hexafluorobenzene",278.5),("pentafluorobenzene",225.9),("pyridine",231.6),("1,4-diazine",328.2),("1,3,5-triazine",358.2)]:
    mp_c = round(mp_k - 273.15, 2)
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_k} K", source=src_2000, source_url=url_2000, evidence_location="Table 2", evidence_quote=f"{cname}", conversion_arithmetic=f"{mp_k} K - 273.15 = {mp_c} °C", notes="Table 2")
for cname, mp_k in [("adamantane",543),("camphor",452)]:
    mp_c = round(mp_k - 273.15, 2)
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_k} K", source=src_2000, source_url=url_2000, evidence_location="Table 3", evidence_quote=f"{cname}", conversion_arithmetic=f"{mp_k} K - 273.15 = {mp_c} °C", notes="Table 3 cage molecules")

src_2005 = "Yalkowsky Estimation of Melting Points of Organic Compounds, PhD thesis 2005, Univ. Arizona"
url_2005 = "legacy:2005_Yalkowsky_ESTIMATION_OF_MELTING_POINTS_OF_ORGANIC_COMPOUNDS.pdf"
for cname, mp_c in [("n-octane",-56),("2-methylheptane",-109),("3-methylheptane",-120),("4-methylheptane",-121),("2,2-dimethylhexane",-121),("2,5-dimethylhexane",-91),("3,3-dimethylhexane",-126),("2,2,3-trimethylpentane",-113),("2,2,4-trimethylpentane",-107),("2,3,3-trimethylpentane",-109),("2,3,4-trimethylpentane",-109),("2,2,3,3-tetramethylbutane",101)]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_c} °C", source=src_2005, source_url=url_2005, evidence_location="Table 1.2", evidence_quote=f"{cname}", notes="Table 1.2 (Experimental melting points for some octanes)")

src_2006 = "J. Org. Chem. 2006, 71, 8761"
url_2006 = "https://doi.org/10.1021/jo061443+"
add(compound_name="(SS)-(E)-N-((1-Benzyl-3-(2-(benzyloxy)ethyl)-1H-indol-2-yl)methylene)-2-methylpropane-2-sulfinamide", property="melting_point", value_celsius=148.5, value_celsius_min=147, value_celsius_max=150, value_raw="147-150 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 20c", evidence_quote="mp 147–150 °C; [α]20D 35.6 (c 2.1, CHCl3); 1H NMR (CDCl3) δ 8.91 (s, 1 H), 7.79 (d, J =", notes="compound 20c")
add(compound_name="(SS,S)-(-)-N-[(1S)-1-{1-Benzyl-3-[2-(benzyloxy)ethyl]-1H-indol-2-yl}-2-(3-cyanopyridin-4-yl)ethyl]-4-methylbenzenesulfinamide", property="melting_point", value_celsius=50, value_celsius_min=49, value_celsius_max=51, value_raw="49-51 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 21a", evidence_quote="major diastereomer as a white solid mp 49–51 °C; [α]20D -44.0 (c .43, CHCl3); 1H NMR", notes="compound 21a")
add(compound_name="(SS,S)-(-)-N-[(1S)-2-(3-Cyanopyridin-4-yl)-1-(1-(4-methoxybenzyl)-3-{2-[(4-methoxybenzyl)oxy]ethyl}-1H-indol-2-yl)ethyl]-4-methylbenzenesulfinamide", property="melting_point", value_celsius=56.5, value_celsius_min=55, value_celsius_max=58, value_raw="55-58 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 21b", evidence_quote="chromatography (12.5–40% acetone:hexanes) afforded 5.9 g (81%) as a white solid; mp 55–", notes="compound 21b")
add(compound_name="(1S,3S)-(-)-3-{1-Benzyl-3-[2-(benzyloxy)ethyl]-1H-indol-2-yl}-1-methyl-1,2,3,4-tetrahydro-2,7-naphthyridine", property="melting_point", value_celsius=56.5, value_celsius_min=55, value_celsius_max=58, value_raw="55-58 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 23a", evidence_quote="(46%) over two steps of a yellow solid, mp 55–58 °C; [α]20D −47.3 (c 1.35, CHCl3); 1H NMR", notes="compound 23a")
add(compound_name="(1S,3S)-(-)-3-(1-(4-Methoxybenzyl)-3-{2-[(4-methoxybenzyl)oxy]ethyl}-1H-indol-2-yl)-1-methyl-1,2,3,4-tetrahydro-2,7-naphthyridine", property="melting_point", value_celsius=68, value_celsius_min=66, value_celsius_max=70, value_raw="66-70 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 23b", evidence_quote="(65%) and an orange solid, mp 66–70 °C; [α]20D −43.3 (c 1.0, CHCl3); 1H NMR (CDCl3) δ", notes="compound 23b")
add(compound_name="2-{2-[(1S,3S)-1-Methyl-1,2,3,4-tetrahydro-2,7-naphthyridin-3-yl]-1H-indol-3-yl}ethanol", property="melting_point", value_celsius=204, value_celsius_min=203, value_celsius_max=205, value_raw="203-205 °C", source=src_2006, source_url=url_2006, evidence_location="Compound 24", evidence_quote="Flash chromatography (MeOH:CHCl3, 2%–8%) afforded 0.99 g (64%) of a white powder, mp", notes="compound 24")
add(compound_name="(-)-Normalindine", property="melting_point", value_celsius=122, value_celsius_min=120, value_celsius_max=124, value_raw="120-124 °C [lit. 131-136 °C]", source=src_2006, source_url=url_2006, evidence_location="Compound 9 (Normalindine)", evidence_quote="mp 120–124 °C [lit.2f 131–136 °C]; [α]20D −204.0 (c 0.4, CHCl3) [lit2f. [α]20D −210 (c 0.1,", notes="compound 9")

src_2008m = "J. Chem. Inf. Model. 2008, 48, 220"
url_2008m = "https://doi.org/10.1021/ci700307p"
for cname, mp_e, mp_p in [("1,2,3-trichlorobenzene",52.6,90.5),("1,3,5-trichlorobenzene",63.4,93.3),("11α-hydroxyprogesterone",222.0,184.1),("17α-ethynylestradiol",143.5,181.4),("2-methylnevirapine",235.0,210.3),("3,4-benzopyrene",179.0,190.9),("4-aminobenzoic acid",187.8,168.3),("5,5-diethyl-2-thiobarbiturate",180.0,205.1),("5,5-diethylbarbiturate",190.0,188.2),("5,5-di-i-propylbarbiturate",227.5,189.6),("5,5-dimethylbarbiturate",278.0,240.1),("5,5-dipropylbarbiturate",146.5,156.6),("5-allyl-5-phenylbarbiturate",158.5,196.4),("5-ethyl-5-(3-methylbut-2-enyl)barbiturate",158.3,169.0),("5-ethyl-5-allylbarbiturate",160.7,157.9),("5-ethyl-5-heptylbarbiturate",118.0,111.4),("5-ethyl-5-nonylbarbiturate",113.0,108.3),("5-i-propyl-5-(3-methylbut-2-enyl)barbiturate",131.3,169.2),("5-t-butyl-5-(3-methylbut-2-enyl)barbiturate",212.0,174.1),("7-methylpteridine",197.0,216.5),("acebutolol",123.0,160.9),("acetanilide",114.0,118.8),("alclofenac",92.5,114.4)]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_e, value_raw=f"{mp_e} °C", data_type="measured", source=src_2008m, source_url=url_2008m, evidence_location="SI Table (Expt. Tm column)", evidence_quote=f"{cname}", notes="SI 287-compound dataset; Expt Tm column")
    add(compound_name=cname, property="melting_point", value_celsius=mp_p, value_raw=f"{mp_p} °C", data_type="calculated", source=src_2008m, source_url=url_2008m, evidence_location="SI Table (Pred. Tm column)", evidence_quote=f"{cname}", notes="SI dataset; Pred Tm (QSPR model)")

src_2014y = "J. Pharm. Sci. 2014, 103, 2629"
url_2014y = "https://doi.org/10.1002/jps.24034"
for cname, mp_c in [("toluene",-93),("fluorobenzene",-40),("chlorobenzene",-46),("bromobenzene",-30),("iodobenzene",-30),("nitrobenzene",6),("phenol",43),("aniline",-6),("benzoic acid",121),("benzamide",130),("ethane",-183),("fluoromethane",-142),("chloromethane",-114),("bromomethane",-87),("nitromethane",-30),("methanol",-98),("methylamine",-94),("acetic acid",17),("acetamide",81)]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_c} °C", source=src_2014y, source_url=url_2014y, evidence_location="Table 1 (Toluene and Ethane Homomorphs)", evidence_quote=f"{cname}", notes="Table 1")

src_2014s = "Beilstein J. Org. Chem. 2014, 10, 2989"
url_2014s = "https://doi.org/10.3762/bjoc.10.317"
add(compound_name="1,1'-(1,2-Phenylene)bis(3-cyclohexylthiourea)", property="melting_point", value_celsius=185, value_raw="185 °C", source=src_2014s, source_url=url_2014s, evidence_location="Compound 1c", evidence_quote="White solid: mp = 185 °C, 95% yield (6.85 g, 17.6 mmol); IR", notes="compound 1c (C20H30N4S2 cyclohexyl)")
add(compound_name="1,1'-(1,2-Phenylene)bis(3-benzylthiourea)", property="melting_point", value_celsius=159, value_raw="159 °C", source=src_2014s, source_url=url_2014s, evidence_location="Compound 1b", evidence_quote="White solid: mp = 159 °C, 86% yield (6.51 g, 15.9 mmol); IR", notes="compound 1b")
add(compound_name="1-Phenyl-3-phenylimino-1H,3H-[1,2,4]thiadiazolo[4,3-a]benzimidazole", property="melting_point", value_celsius=170, value_raw="170 °C", source=src_2014s, source_url=url_2014s, evidence_location="Compound 2a", evidence_quote="solid: mp = 170 °C, 68% yield (582 mg, 1.70 mmol); IR (KBr)", notes="compound 2a")
add(compound_name="1-Benzyl-3-benzylimino-1H,3H-[1,2,4]thiadiazolo[4,3-a]benzimidazole", property="melting_point", value_celsius=106, value_raw="106 °C", source=src_2014s, source_url=url_2014s, evidence_location="Compound 2b", evidence_quote="yellow solid: mp = 106 °C, 79% yield (730 mg, 1.97 mmol); IR", notes="compound 2b")
add(compound_name="1-Cyclohexyl-3-cyclohexylimino-1H,3H-[1,2,4]thiadiazolo[4,3-a]benzimidazole", property="melting_point", value_celsius=116, value_raw="116 °C", source=src_2014s, source_url=url_2014s, evidence_location="Compound 2c", evidence_quote="solid: mp = 116 °C, 83% yield (734 mg, 2.07 mmol); IR (KBr)", notes="compound 2c")

src_2017 = "Int. J. Pharm. (Yalkowsky & Alantary review, 2017)"
url_2017 = "legacy:2017_Yalkowsky_Estimation_of_melting_points_of_organics.pdf"
for cname, mp_c in [("n-butane",-138),("cyclobutane",-91),("n-pentane",-130),("cyclopentane",-94),("n-hexane",-95),("cyclohexane",7),("n-heptane",-91),("cycloheptane",-8),("n-octane",-57),("cyclooctane",15),("dimethyl ether",-142),("ethylene oxide",-112),("diethyl ether",-132),("tetrahydrofuran",-109),("diethyl sulfide",-104),("tetrahydrothiophene",-99),("dimethyl amine",-93),("ethylenimine",-78),("diethyl amine",-50),("pyrrolidine",-61),("3-pentanone",-40),("cyclopentanone",-51),("diethyl sulfone",70),("sulfolane",28),("ethyl acetate",-80),("butyrolactone",-45),("dimethyl carbonate",7),("ethylene carbonate",37),("acetic anhydride",-73),("succinic anhydride",120)]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_c} °C", source=src_2017, source_url=url_2017, evidence_location="Table 6", evidence_quote=f"{cname}", notes="Table 6 (linear and cyclic analogs)")

src_2019j = "Beilstein J. Org. Chem. 2019, 15, 2655"
url_2019j = "https://doi.org/10.3762/bjoc.15.258"
add(compound_name="m,p'-quaterphenyl", property="melting_point", value_celsius=164.5, value_celsius_min=163, value_celsius_max=166, value_raw="163-166 °C", source=src_2019j, source_url=url_2019j, evidence_location="Compound 13", evidence_quote="phenyl (13) as a white solid (0.058 g, mp 163–166 °C, lit", notes="compound 13")
add(compound_name="o,p'-quaterphenyl", property="melting_point", value_celsius=108, value_celsius_min=107, value_celsius_max=109, value_raw="107-109 °C", source=src_2019j, source_url=url_2019j, evidence_location="Compound 15", evidence_quote="phenyl as a white solid (0.55 g, mp 107–109 °C, lit 117–120 °C,", notes="compound 15")
add(compound_name="o,m'-quaterphenyl", property="melting_point", value_celsius=85, value_celsius_min=84, value_celsius_max=86, value_raw="84-86 °C", source=src_2019j, source_url=url_2019j, evidence_location="Compound 16", evidence_quote="quaterphenyl as a white solid (0.085 g, mp 84–86 °C, lit", notes="compound 16")
add(compound_name="o,o'-quaterphenyl", property="melting_point", value_celsius=111.5, value_celsius_min=110, value_celsius_max=113, value_raw="110-113 °C", source=src_2019j, source_url=url_2019j, evidence_location="Compound 17", evidence_quote="(0.040 g, mp 110–113 °C, lit 116–118 °C, 20% yield). 1H NMR", notes="compound 17")

src_2019m = "Beilstein J. Org. Chem. 2019, 15, 2493"
url_2019m = "https://doi.org/10.3762/bjoc.15.242"
add(compound_name="Diphenyl(((1R,2R,5S)-δ-pinen-3-yl)methyl)phosphine oxide", property="melting_point", value_celsius=129, value_celsius_min=127, value_celsius_max=131, value_raw="127-131 °C", source=src_2019m, source_url=url_2019m, evidence_location="Compound 21", evidence_quote="92%) was obtained as a white solid, mp 127–131 °C,", notes="compound 21")
add(compound_name="(((1R,2R,3R,4R,5R)-4-Hydroxypinan-3-yl)methyl)diphenylphosphine oxide", property="melting_point", value_celsius=181, value_celsius_min=179, value_celsius_max=183, value_raw="179-183 °C", source=src_2019m, source_url=url_2019m, evidence_location="Compound 22", evidence_quote="solid (mp 179–183 °C,", notes="compound 22")
add(compound_name="Diphenyl(((1R,2S,5R)-δ-pinen-4-yl)methyl)phosphine oxide", property="melting_point", value_celsius=64, value_celsius_min=62, value_celsius_max=66, value_raw="62-66 °C", source=src_2019m, source_url=url_2019m, evidence_location="Compound 26", evidence_quote="mp 62–66 °C,", notes="compound 26")

src_2019r = "J. Org. Chem. 2019 (manuscript) — Rubstov et al."
url_2019r = "legacy:2019_Rubstov_One-pot_synthesis_of_thieno32-epyrrolo12-apyrimidine_derivatives_scaffold.pdf"
for cname, label, mp_mid, mp_min, mp_max, ev in [
("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4a",254,253,255,"Yellow solid; 1.90 g, 85 % yield; m.p. 253-255 °С"),
("Ethyl (E)-1-(2-(4-methylphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4b",258.5,258,259,"Yellow solid; 1.94 g, 84 % yield; m.p."),
("Ethyl (E)-1-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4c",253.5,253,254,"Yellow solid; 2.08 g, 87 % yield; m.p."),
("Ethyl (E)-1-(2-(4-chlorophenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4d",264.5,264,265,"Yellow solid; 1.73 g, 72 % yield; m.p."),
("Ethyl (E)-1-(2-(2,4-dimethoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4e",229.5,229,230,"Yellow solid; 2.13 g, 84 % yield; m.p."),
("Ethyl (E)-1-(3,3-dimethyl-2-oxobutylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4f",223.5,223,224,"Yellow solid; 1.50 g, 70 % yield; m.p. 223-224 °С"),
("Ethyl (E)-8-(2-phenyl-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate","4g",242.5,242,243,"Yellow solid; 1.86 g, 88 % yield; m.p. 242-243 °С"),
("Ethyl (E)-8-(2-(4-methylphenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate","4h",246.5,246,247,"Yellow solid; 1.87 g, 86 % yield; m.p."),
("Ethyl (E)-8-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate","4i",253.5,253,254,"Yellow solid; 2.10 g, 93 % yield; m.p."),
("Ethyl (E)-8-(2-(4-chlorophenyl)-2-oxoethylidene)-2,3-dimethyl-4,7-dioxo-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate","4j",250.5,250,251,"Yellow solid; 1.71 g, 75 % yield; m.p."),
("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,7,8,9,10-octahydro-6H-cyclohepta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4k",256.5,256,257,"Yellow solid; 1.83 g, 79 % yield; m.p."),
("Ethyl (E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9,10,11-decahydrocycloocta[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","4l",243.5,243,244,"Yellow solid; 1.81 g, 76 % yield; m.p."),
("Ethyl (E)-4,7-dioxo-8-(2-oxo-2-phenylethylidene)-3-phenyl-4,5,7,8-tetrahydropyrrolo[1,2-a]thieno[3,2-e]pyrimidine-6-carboxylate","4m",231.5,231,232,"Yellow solid; 1.95 g, 83 % yield; m.p. 231-232 °С"),
("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxamide","4n",284,283,285,"Yellow solid; 1.89 g, 92 % yield; m.p. 283-285 °С"),
("(E)-1-(2-(4-methoxyphenyl)-2-oxoethylidene)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxamide","4o",287.5,287,288,"Yellow solid; 2.15 g, 96 % yield; m.p. 287-288 °С"),
("(E)-2,5-dioxo-1-(2-oxo-2-phenylethylidene)-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carbonitrile","4p",186.5,186,187,"Yellow solid; 1.76 g, 88 % yield; m.p. 186-187 °С"),
("Ethyl 2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","13",276,275,277,"White solid; 0.44 g, 83 % yield; m.p. 275-277 °С"),
("Ethyl 1-(2-(4-methoxyphenyl)-2-oxoethyl)-2,5-dioxo-1,2,4,5,6,7,8,9-octahydrobenzo[4,5]thieno[3,2-e]pyrrolo[1,2-a]pyrimidine-3-carboxylate","11",207,206,208,"White solid; 0.34 g, 70 % yield; m.p. 206-208 °С"),]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_mid, value_celsius_min=mp_min, value_celsius_max=mp_max, value_raw=f"{mp_min}-{mp_max} °C", source=src_2019r, source_url=url_2019r, evidence_location=f"Compound {label}", evidence_quote=ev, notes=f"compound {label}")

src_2021 = "J. Org. Chem. 2021, 86, 3882"
url_2021 = "https://doi.org/10.1021/acs.joc.0c02731"
add(compound_name="Methyl-3-acetoxy-12α-fluoro-13α,14α-cyclopropane-β-glycyrrhetate", property="melting_point", value_celsius=285.5, value_celsius_min=285, value_celsius_max=286, value_raw="285-286 °C", source=src_2021, source_url=url_2021, evidence_location="Compound 2", evidence_quote="(1) (0.97 g, 1.8 mmol) as described above. A white solid, mp 285−", notes="compound 2")
add(compound_name="Bicyclic 3 (dehydrofluorination product of 2)", property="melting_point", value_celsius=231, value_celsius_min=230, value_celsius_max=232, value_raw="230-232 °C", source=src_2021, source_url=url_2021, evidence_location="Compound 3", evidence_quote="as described above. A white solid, mp 230−232 °C, (0.87 g, >95%", notes="compound 3")
add(compound_name="Methyl-3-trichloroacetoxy-α-glycyrrhetate", property="melting_point", value_celsius=294, value_celsius_min=293, value_celsius_max=295, value_raw="293-295 °C", source=src_2021, source_url=url_2021, evidence_location="Compound 4", evidence_quote="recrystallized from PE/EtOAc. A white solid, mp 293−295 °C, (0.3 g,", notes="compound 4")
add(compound_name="Bicyclic 8 (dehydrofluorination product of 7)", property="melting_point", value_celsius_min=277, value_raw=">277 °C dec.", relation=">", source=src_2021, source_url=url_2021, evidence_location="Compound 8", evidence_quote="as described above. A white solid, mp >277 °C dec., (0.28 g, >95%", notes="compound 8; decomposition")
add(compound_name="Methyl-3β-acetoxy-12α-fluoro-13α,14α-cyclopropane-oleanolate", property="melting_point", value_celsius=124, value_celsius_min=123, value_celsius_max=125, value_raw="123-125 °C", source=src_2021, source_url=url_2021, evidence_location="Compound 9", evidence_quote="(5) (0.67 g, 1.3 mmol) as described above. A white solid, mp 123−", notes="compound 9")
add(compound_name="Bicyclic 10 (dehydrofluorination product of 9)", property="melting_point", value_celsius=220, value_celsius_min=219, value_celsius_max=221, value_raw="219-221 °C", source=src_2021, source_url=url_2021, evidence_location="Compound 10", evidence_quote="white solid, mp 219−221 °C, (0.58 g, >95% yield) was obtained; 1H", notes="compound 10")

src_2013z = "J. Med. Chem. 2013, 56, 952"
url_2013z = "https://doi.org/10.1021/jm3014162"
for cname, label, mp_mid, mp_min, mp_max, ev in [
("1,3,5-Trimethyl-2-(2,4,5-trimethylbenzenesulfonyl)benzene","5a",147.5,147,148,"product as a white solid (290 mg, 96%); mp 147-148 °C; HPLC purity 98.4% (tR = 25.33"),
("2-(4-Cyclohexylbenzenesulfonyl)-1,3,5-trimethylbenzene","5c",102.5,102,103,"compound 5a. The title compound was obtained as a white solid (mp 102-103 °C). HPLC"),
("2-(4-Iodobenzenesulfonyl)-1,3,5-trimethylbenzene","8a",123.5,123,124,"mg, 69%) as a white solid (mp 123-124 °C). HPLC purity 96.0% (tR = 23.82 min). 1H NMR"),
("2-(4-Methoxybenzenesulfonyl)-1,3,5-trimethylbenzene","8b",132.5,132,133,"compound 8a. The title compound was obtained as a white solid (mp 132-133 °C). HPLC"),]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_mid, value_celsius_min=mp_min, value_celsius_max=mp_max, value_raw=f"{mp_min}-{mp_max} °C", source=src_2013z, source_url=url_2013z, evidence_location=f"Compound {label}", evidence_quote=ev, notes=f"compound {label}")

src_2009y = "Int. J. Pharm. 2009, 373, 24"
url_2009y = "https://doi.org/10.1016/j.ijpharm.2008.12.034"
for cname, mp_c in [("Acyclovir",255),("Allopurinol",350),("Alprenolol",108),("Bupropion",25),("Camazepam",174),("Carbamazepine",190),("Cefamandole nafate",190),("Cefazolin",199),("Cefmetazole",330)]:
    add(compound_name=cname, property="melting_point", value_celsius=mp_c, value_raw=f"{mp_c} °C", source=src_2009y, source_url=url_2009y, evidence_location="Table 1 (Drug physical properties)", evidence_quote=f"{cname}", notes="Table 1; MP compiled from refs")

out = '/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/batches/batch_pdfs_results.csv'
fields = ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']
with open(out, 'w', encoding='utf-8') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(fields)
    for r in rows:
        w.writerow([r[k] for k in fields])
print(f"Wrote {len(rows)} rows to {out}")

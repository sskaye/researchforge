import csv
import os

rows = []
def add(**kw):
    base = {
        'id': len(rows)+1,
        'verification_status': 'pending_verification',
        'compound_name':'', 'compound_smiles':'',
        'property':'melting_point',
        'value_celsius':'', 'value_celsius_min':'', 'value_celsius_max':'',
        'value_raw':'', 'relation':'eq',
        'data_type':'measured', 'source':'', 'source_url':'',
        'evidence_location':'Experimental section',
        'evidence_quote':'', 'conversion_arithmetic':'',
        'notes':''
    }
    base.update(kw)
    rows.append(base)

src127 = "Russ. J. Org. Chem. 2022, 58(10), 1434-1437"
url127 = "https://doi.org/10.1134/S1070428022100086"
add(compound_name="6-[(2-Hydroxybenzylidene)amino]-2-methylquinolin-4-ol", value_celsius_min=326, value_celsius_max=327, value_raw="326-327 C", source=src127, source_url=url127, evidence_quote="Yield 0.20 g (72%), mp 326–327°C, R f 0.52 (EtOH–xylene, 1:1).", notes="range")
add(compound_name="2-(4-Hydroxy-2-methylquinolin-6-yl)-1H-isoindole-1,3(2H)-dione", value_celsius=350, value_raw="350 C (decomp.)", source=src127, source_url=url127, evidence_quote="Yield 0.27 g (89%), mp 350°C (decomp.), R f 0.57 (EtOH–xylene, 1:1.5).", notes="decomposes")
add(compound_name="N-(4-Hydroxy-2-methylquinolin-6-yl)-N'-phenylthiourea", value_celsius=325, value_raw="325 C (decomp.)", source=src127, source_url=url127, evidence_quote="Yield 1.30 g (85%), mp 325°C (decomp.), R f 0.60 (EtOH–xylene, 1:2.5).", notes="decomposes")
add(compound_name="N-(4-Hydroxy-2-methylquinolin-6-yl)thiourea", value_celsius_min=242, value_celsius_max=243, value_raw="242-243 C", source=src127, source_url=url127, evidence_quote="Yield 1.51 g (65%), mp 242–243°C, R f 0.52 (EtOH–xylene, 1:2).", notes="range")
add(compound_name="2-[(4-Hydroxy-2-methylquinolin-6-yl)imino]-1,3-thiazolidin-4-one", value_celsius=375, value_raw="375 C (decomp.)", source=src127, source_url=url127, evidence_quote="Yield 0.23 g (85%), mp 375°C (decomp.), R f 0.50 (EtOH–xylene, 1:3).", notes="decomposes")
add(compound_name="2-Methyl-6-{[4-phenyl-1,3-thiazol-2(3H)ylidene]amino}quinolin-4-ol", value_celsius_min=305, value_celsius_max=306, value_raw="305-306 C", source=src127, source_url=url127, evidence_quote="Yield 0.31 g (93%), mp 305–306°C, R f 0.67 (EtOH–PhMe, 1:1).", notes="range")

src128 = "Molecules 2002, 7(10), 767-776"
url128 = "https://doi.org/10.3390/71000767"
add(compound_name="(2S,11S,3Z,9Z)-2,11-Di[(tert-butoxycarbonyl)amino]-1,12-diphenyldodeca-3,9-diene", value_celsius_min=91, value_celsius_max=93, value_raw="91-93 C", source=src128, source_url=url128, evidence_quote="yield 626 mg (57%); yellow solid; mp 91–93 o C; –4.7 ( c 0.9, CHCl 3 )", notes="range")
add(compound_name="(5S,14S,6Z,12Z)-1,5,14,18-Tetra[(tert-butoxycarbonyl)amino]-octadeca-6,12-diene", value_celsius_min=87, value_celsius_max=88, value_raw="87-88 C", source=src128, source_url=url128, evidence_quote="yield 611 mg (43%); white solid; mp 87–88 o C; +0.5 ( c 1.0, CHCl 3 )", notes="range")
add(compound_name="(5R)-1,5-Di[(tert-butoxycarbonyl)amino]-dodecane", value_celsius_min=63, value_celsius_max=64, value_raw="63-64 C", source=src128, source_url=url128, evidence_quote="Yield 365 mg (91%); white solid; mp 63–64 o C, –2.3 ( c 1.0, CHCl 3 )", notes="range")

src129 = "Molecules 2002, 7(2), 252"
url129 = "https://doi.org/10.3390/70200252"
add(compound_name="3-Ethoxycarbonyl-2-benzyl isoquinolinium bromide", value_celsius_min=132, value_celsius_max=134, value_raw="132-34 C", source=src129, source_url=url129, evidence_quote="3-Ethoxycarbonyl-2-benzyl isoquinolinium bromide ( 5a ). Yield = 90%; mp = 132-34°C (moisture sensitive)", notes="range")
add(compound_name="3-Ethoxycarbonyl-2-(3-hydroxypropyl)-isoquinolinium chloride", value_celsius_min=142, value_celsius_max=144, value_raw="142-44 C", source=src129, source_url=url129, evidence_quote="3-Ethoxycarbonyl-2-(3-hydroxypropyl)-isoquinolinium chloride ( 5c ). Yield = 53%; mp = 142-44°C (moisture sensitive)", notes="range")
add(compound_name="10-Oxo-6,7,8,10-tetrahydro-9-oxo-[5a]-azonia-cyclohepta[b]naphtalene bromide", value_celsius_min=244, value_celsius_max=246, value_raw="244-46 C", source=src129, source_url=url129, evidence_quote="10-Oxo-6,7,8,10-tetrahydro-9-oxo-[5a]-azonia-cyclohepta[b]naphtalene bromide ( 5d ). Yield = 75%, mp = 244-46°C (hygroscopic salt)", notes="range")
add(compound_name="3-Ethoxycarbonyl-2-ethoxycarbonylmethyl-6,7-dimethoxy isoquinolinium bromide", value_celsius_min=190, value_celsius_max=192, value_raw="190-92 C", source=src129, source_url=url129, evidence_quote="3-Ethoxycarbonyl-2-ethoxycarbonylmethyl-6,7-dimethoxy isoquinolinium bromide ( 5e ). Yield = 86%, mp = 190-92°C (moisture sensitive)", notes="range")
add(compound_name="3-Ethoxycarbonyl-2-ethoxycarbonylmethyl isoquinolinium bromide", value_celsius_min=152, value_celsius_max=154, value_raw="152-54 C", source=src129, source_url=url129, evidence_quote="3-Ethoxycarbonyl-2-ethoxycarbonylmethyl isoquinolinium bromide ( 5f ). Yield = 96%, mp = 152‑54°C (moisture sensitive)", notes="range")

src131 = "Molecules 2002, 7(2), 315-319"
url131 = "https://doi.org/10.3390/70200315"
add(compound_name="2-Hydroxy-4-O-methoxymethylbenzaldehyde", value_celsius_min=50, value_celsius_max=51, value_raw="50-51 C", source=src131, source_url=url131, evidence_quote="Chromatography on silica gel (25% EtOAc/hexanes) afforded a white solid (118 mg, 84%); Mp: 50-51 o C; IR (KBr): 3158 (OH)")
add(compound_name="2-Methoxy-4-O-methoxymethylbenzaldehyde", value_celsius_min=73, value_celsius_max=74, value_raw="73-74 C", source=src131, source_url=url131, evidence_quote="Chromatography on silica gel (25% EtOAc/hexanes) afforded a white solid (1.69 g, 93%); Mp: 73-74 o C; IR (neat) cm -1 : 1682 (CO)")
add(compound_name="3-(4-Hydroxy-2-methoxyphenyl)-propanoic acid", value_celsius_min=105, value_celsius_max=106, value_raw="105-106 C", source=src131, source_url=url131, evidence_quote="Chromatography on silica gel (5% MeOH in 50% EtOAc/hexanes) afforded a white solid (405 mg, 81%); Mp: 105-106 o C; IR (neat) cm -1 : 3386 (OH)")
add(compound_name="6-Methoxy-1-oxaspiro[4,5]deca-6,9-diene-8-one", value_celsius_min=108, value_celsius_max=109, value_raw="108-109 C", source=src131, source_url=url131, evidence_quote="Chromatography on silica gel (75% EtOAc/hexanes) afforded a white solid (46 mg, 46%); Mp: 108-109 o C; IR (neat) cm -1 : 1788 (CO ester)")

src133 = "Molecules 2002, 7(4), 382"
url133 = "https://doi.org/10.3390/70400382"
add(compound_name="2-[3-Chloro-2-(toluene-4-sulfonylmethyl)propenyl]-1-methyl-5-nitro-1H-imidazole", value_celsius=134, value_raw="134 C", source=src133, source_url=url133, evidence_quote="2-[3-chloro-2-(toluene-4-sulfonylmethyl)propenyl]-1-methyl-5-nitro-1 H -imidazole ( 3 ) ( E : Z , 1:2): Brown solid, mp 134 °C (ethanol).")
add(compound_name="(E)-3-(1-Methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester", value_celsius=115, value_raw="115 C", source=src133, source_url=url133, evidence_quote="3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester ( 4E ): Yellow solid, mp 115 °C (ethanol).")
add(compound_name="(Z)-3-(1-Methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester", value_celsius=118, value_raw="118 C", source=src133, source_url=url133, evidence_quote="3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester ( 4Z ): Yellow solid, mp 118 °C (ethanol).")

src135 = "Molecules 2001, 6(3), 253"
url135 = "https://doi.org/10.3390/60300253"
add(compound_name="2-Thiocyanatothiophene", property="boiling_point", value_celsius_min=134, value_celsius_max=136, value_raw="134-136 C/12 mm", source=src135, source_url=url135, evidence_quote="2-Thiocyanatothiophene (5): Yellow oil, bp 134-136°C/12 mm", notes="reduced pressure 12 mm Hg")

src137 = "Molecules 2001, 6(3), 244"
url137 = "https://doi.org/10.3390/60300244"
add(compound_name="1-Bromo-2,5-diisopropylborolane", property="boiling_point", value_celsius=42, value_raw="42 C at 0.2 mm", source=src137, source_url=url137, evidence_quote="The yellow residue was distilled to give 1-bromo-2,5-diisopropylborolane, a colorless oil (12.8 g, 76%) b.p. 42°C at 0.2 mm", notes="reduced pressure 0.2 mm Hg")
add(compound_name="cis- and trans-2,5-Diisopropyl-B-methoxyborolanes (mixture)", property="boiling_point", value_celsius=47, value_raw="47 C at 1 mmHg", source=src137, source_url=url137, evidence_quote="The residue was distilled to give a mixture of cis - and trans -2,5-diisopropyl- B -methoxyborolanes ( 14 ) and ( 15 ), as a colorless oil (6.4 g, 48%); b.p. 47 °C at 1 mmHg", notes="reduced pressure 1 mmHg; cis/trans mixture")

src138 = "Molecules 2002, 7(7), 554"
url138 = "https://doi.org/10.3390/70700554"
add(compound_name="7,9-Diphenyltetrazolo[1,5-c]pyrrolo-7H-[3,2-e]pyrimidine", value_celsius_min=215, value_celsius_max=217, value_raw="215-17 C", source=src138, source_url=url138, evidence_quote="7,9-Diphenyltetrazolo[1,5-c]pyrrolo-7H-[3,2-e]pyrimidine ( 3a ): Yield: 61 % (Method A), 60 % (Method B); mp: 215-17°C")
add(compound_name="7-(4-Fluorophenyl)-9-phenyltetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=217, value_celsius_max=219, value_raw="217-19 C", source=src138, source_url=url138, evidence_quote="7-(4-Fluorophenyl)-9-phenyltetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3b ): Yield: 70 % (Method A), 56 % (Method B); mp: 217-19°C")
add(compound_name="7-(4-Chlorophenyl)-9-phenyl-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=218, value_celsius_max=220, value_raw="218-20 C", source=src138, source_url=url138, evidence_quote="7-(4-Chlorophenyl)-9-phenyl-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3c ): Yield: 70 % (Method A), 64 % (Method B); mp: 218-20°C")
add(compound_name="7-(3-Chloro-4-fluorophenyl)-9-phenyl-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=212, value_celsius_max=214, value_raw="212-14 C", source=src138, source_url=url138, evidence_quote="7-(3-Chloro-4-fluorophenyl)-9-phenyl-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3d) : Yield: 64 % (Method A), 63 % (Method B); mp: 212-14°C")
add(compound_name="7-Phenyl-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=216, value_celsius_max=218, value_raw="216-18 C", source=src138, source_url=url138, evidence_quote="7-Phenyl-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3e ): Yield: 70 % (Method A), 56 % (Method B); mp: 216-18°C")
add(compound_name="7,9-Di(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=237, value_celsius_max=239, value_raw="237-39 C", source=src138, source_url=url138, evidence_quote="7,9-Di(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3f ): Yield: 77 % (Method A), 75 % (Method B); mp: 237-39°C")
add(compound_name="7-(4-Fluorophenyl)-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=245, value_celsius_max=247, value_raw="245-47 C", source=src138, source_url=url138, evidence_quote="7-(4-Fluoropheny)l-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3g ): Yield: 63 % (Method A), 61 % (Method B); mp: 245-47°C")
add(compound_name="7-(3-Chloro-4-fluorophenyl)-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=219, value_celsius_max=221, value_raw="219-21 C", source=src138, source_url=url138, evidence_quote="7-(3-Chloro-4-fluorophenyl)-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3h ): Yield: 56 % (Method A), 58 % (Method B); mp: 219-21°C")
add(compound_name="7-Phenyl-9-(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=233, value_celsius_max=235, value_raw="233-35 C", source=src138, source_url=url138, evidence_quote="7-(4-Phenyl)-9-(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3i ): Yield: 80 % (Method A), 71 % (Method B); mp: 233-35°C")
add(compound_name="7-(4-Fluorophenyl)-9-(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=226, value_celsius_max=228, value_raw="226-28 C", source=src138, source_url=url138, evidence_quote="7-(4-Fluorophenyl)-9-(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3j ): Yield: 67 % (Method A), 66 % (Method B); mp: 226-28°C")
add(compound_name="7,9-Di(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=224, value_celsius_max=225, value_raw="224-25 C", source=src138, source_url=url138, evidence_quote="7,9-Di(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3k ): Yield: 77 % (Method A), 70 % (Method B); mp: 224-25°C")
add(compound_name="7-(3-Chloro-4-fluorophenyl)-9-(4-chlorophenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=220, value_celsius_max=222, value_raw="220-22 C", source=src138, source_url=url138, evidence_quote="7-(3-Chloro-4-fluoropheny)l-9-(4-chlorophenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 3l ): Yield: 65 % (Method A), 63 % (Method B); mp: 220-22°C")
add(compound_name="1-(4-Chlorophenyl)-N-ethoxymethylene-2-amino-3-cyano-4-phenylpyrrole", value_celsius_min=130, value_celsius_max=131, value_raw="130-31 C", source=src138, source_url=url138, evidence_quote="1-(4-Chlorophenyl)-N-ethoxymethylene-2-amino-3-cyano-4-phenylpyrrole ( 6a ): Yield: 70 %; mp: 130-31°C")
add(compound_name="1-Phenyl-N-ethoxymethylene-2-amino-3-cyano-4-(4-methoxyphenyl)pyrrole", value_celsius_min=159, value_celsius_max=160, value_raw="159-60 C", source=src138, source_url=url138, evidence_quote="1-Phenyl-N-ethoxymethylene-2-amino-3-cyano-4-(4-methoxyphenyl)pyrrole ( 6b ): Yield: 72 %; mp: 159-60°C")
add(compound_name="1,4-Di(4-methoxyphenyl)-N-ethoxymethylene-2-amino-3-cyanopyrrole", value_celsius_min=117, value_celsius_max=118, value_raw="117-18 C", source=src138, source_url=url138, evidence_quote="1,4-Di(4-methoxyphenyl)-N-ethoxymethylene-2-amino-3-cyanopyrrole ( 6c ): Yield: 73 %; mp: 117-18°C")
add(compound_name="1,4-Di(4-chlorophenyl)-N-ethoxymethylene-2-amino-3-cyanopyrrole", value_celsius_min=200, value_celsius_max=201, value_raw="200-01 C", source=src138, source_url=url138, evidence_quote="1,4-Di(4-chlorophenyl)-N-ethoxymethylene-2-amino-3-cyanopyrrole ( 6e) : Yield: 81 %; mp: 200-01°C")
add(compound_name="3-Amino-4-imino-5-phenyl-7-(4-chlorophenyl)-7H-pyrrolo[2,3-d]pyrimidine", value_celsius_min=201, value_celsius_max=202, value_raw="201-02 C", source=src138, source_url=url138, evidence_quote="3-Amino-4-imino-5-phenyl-7-(4-chlorophenyl)-7H-pyrrolo[2,3-d]pyrimidine ( 7a ): Yield: 89 %; mp: 201-02°C")
add(compound_name="3-Amino-4-imino-5-(4-methoxyphenyl)-7-phenyl-7H-pyrrolo[2,3-d]pyrimidine", value_celsius_min=193, value_celsius_max=195, value_raw="193-95 C", source=src138, source_url=url138, evidence_quote="3-Amino-4-imino-5-(4-methoxyphenyl)-7-phenyl-7H-pyrrolo[2,3-d]pyrimidine ( 7b ): Yield: 88 %; mp: 193-95°C")
add(compound_name="3-Amino-4-imino-5-(4-chlorophenyl)-7-phenyl-7H-pyrrolo[2,3-d]pyrimidine", value_celsius_min=204, value_celsius_max=206, value_raw="204-06 C", source=src138, source_url=url138, evidence_quote="3-Amino-4-imino-5-(4-chlorophenyl)-7-phenyl-7H-pyrrolo[2,3-d]pyrimidine ( 7d ): Yield: 86 %; mp: 204-06°C")
add(compound_name="7-(4-Chlorophenyl)-9-phenyl-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=256, value_celsius_max=258, value_raw="256-58 C", source=src138, source_url=url138, evidence_quote="7-(4-Chorophenyl)-9-phenyl-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 4a ): Yield: 69 % (Method A), 57 % (Method B); mp: 256-58°C")
add(compound_name="7-Phenyl-9-(4-methoxyphenyl)triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=225, value_celsius_max=226, value_raw="225-26 C", source=src138, source_url=url138, evidence_quote="7-Phenyl-9-(4-methoxyphenyl)triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 4b ): Yield: 55 % (Method A), 62 % (Method B); mp: 225-26°C")
add(compound_name="7,9-Di(4-methoxyphenyl)triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=204, value_celsius_max=205, value_raw="204-05 C", source=src138, source_url=url138, evidence_quote="7,9-Di(4-methoxyphenyltriazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 4c ): Yield: 85 % (Method A), 75 % (Method B); mp: 204-05°C")
add(compound_name="7-Phenyl-9-(4-chlorophenyl)-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=240, value_celsius_max=242, value_raw="240-42 C", source=src138, source_url=url138, evidence_quote="7-(4-Phenyl)-9-(4-chlorophenyl)-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 4d ): Yield: 70 % (Method A), 72 % (Method B); mp: 240-42°C")
add(compound_name="7,9-Di(4-chlorophenyl)-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine", value_celsius_min=237, value_celsius_max=239, value_raw="237-39 C", source=src138, source_url=url138, evidence_quote="7,9-Di(4-chlorophenyl)-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine ( 4e ): Yield: 85 % (Method A), 82 % (Method B); mp: 237-39°C")

src139 = "Molecules 2001, 6(11), 881-891"
url139 = "https://doi.org/10.3390/61100881"
add(compound_name="(Diacetoxyiodo)benzene", value_celsius_min=161, value_celsius_max=163, value_raw="161-63", source=src139, source_url=url139, evidence_quote="H B 73 161-63 161.1-162.2 [ 20 ]", evidence_location="Table 1", notes="R=H; PhI(OAc)2")
add(compound_name="1-(Diacetoxyiodo)-4-fluorobenzene", value_celsius_min=180, value_celsius_max=182, value_raw="180-82", source=src139, source_url=url139, evidence_quote="4-F A 71 180-82 177.0-179.8 [ 20 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-2-chlorobenzene", value_celsius_min=140, value_celsius_max=142, value_raw="140-42", source=src139, source_url=url139, evidence_quote="2-Cl B 45 140-42 140-142 [ 8 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-3-chlorobenzene", value_celsius_min=156, value_celsius_max=158, value_raw="156-58", source=src139, source_url=url139, evidence_quote="3-Cl B 68 156-58 153.1-154.7 [ 20 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-4-chlorobenzene", value_celsius_min=114, value_celsius_max=116, value_raw="114-16", source=src139, source_url=url139, evidence_quote="4-Cl C 69 114-16 109.8-113.2 [ 20 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-4-bromobenzene", value_celsius_min=120, value_celsius_max=122, value_raw="120-22", source=src139, source_url=url139, evidence_quote="4-Br C 50 120-22 120-122 [ 8 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-2-methylbenzene", value_celsius_min=140, value_celsius_max=142, value_raw="140-42", source=src139, source_url=url139, evidence_quote="2-Me C 64 140-42 140-142 [ 21 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-3-methylbenzene", value_celsius_min=153, value_celsius_max=155, value_raw="153-55", source=src139, source_url=url139, evidence_quote="3-Me B 71 153-55 154 [ 22 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-4-methylbenzene", value_celsius_min=108, value_celsius_max=110, value_raw="108-10", source=src139, source_url=url139, evidence_quote="4-Me B 77 108-10 106-110 [ 20 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-2-methoxybenzene", value_celsius_min=147, value_celsius_max=149, value_raw="147-49", source=src139, source_url=url139, evidence_quote="2-OMe B 65 147-49 146.9-150.1 [ 20 ]", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-3-methoxybenzene", value_celsius_min=133, value_celsius_max=135, value_raw="133-35", source=src139, source_url=url139, evidence_quote="3-OMe C 74 133-35 not reported", evidence_location="Table 1")
add(compound_name="1-(Diacetoxyiodo)-4-methoxybenzene", value_celsius_min=88, value_celsius_max=90, value_raw="88-90", source=src139, source_url=url139, evidence_quote="4-OMe D 73 88-90 92.4-96.0 [ 20 ]", evidence_location="Table 1")
add(compound_name="Iodylbenzene", value_celsius=236, value_raw="236 expl.", source=src139, source_url=url139, evidence_quote="H 8 86 236 expl. 235 expl. [ 23 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Methoxyiodylbenzene", value_celsius=224, value_raw="224 expl.", source=src139, source_url=url139, evidence_quote="4-OMe 8 85 224 expl. 225 dec. [ 24 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="2-Methyliodylbenzene", value_celsius=209, value_raw="209 expl.", source=src139, source_url=url139, evidence_quote="2-Me 8 61 209 expl. 208 [ 25 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="3-Methyliodylbenzene", value_celsius=219, value_raw="219 expl.", source=src139, source_url=url139, evidence_quote="3-Me 8 77 219 expl. 220 expl. [ 26 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Methyliodylbenzene", value_celsius=226, value_raw="226 expl.", source=src139, source_url=url139, evidence_quote="4-Me 8 80 226 expl. 229 dec. [ 27 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Fluoroiodylbenzene", value_celsius=262, value_raw="262 expl.", source=src139, source_url=url139, evidence_quote="4-F 12 91 262 expl. 248 [ 28 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="3-Chloroiodylbenzene", value_celsius=232, value_raw="232 expl.", source=src139, source_url=url139, evidence_quote="3-Cl 12 75 232 expl. 233 expl. [ 29 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Chloroiodylbenzene", value_celsius=248, value_raw="248 expl.", source=src139, source_url=url139, evidence_quote="4-Cl 12 80 248 expl. 243 expl. [ 29 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Bromoiodylbenzene", value_celsius=241, value_raw="241 expl.", source=src139, source_url=url139, evidence_quote="4-Br 16 73 241 expl. 240 expl. [ 30 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="3-Nitroiodylbenzene", value_celsius=233, value_raw="233 expl.", source=src139, source_url=url139, evidence_quote="3-NO 2 8 85 233 expl. 214 dec. [ 31 ]", evidence_location="Table 2", notes="decomposes with explosion")
add(compound_name="4-Nitroiodylbenzene", value_celsius=230, value_raw="230 expl.", source=src139, source_url=url139, evidence_quote="4-NO 2 16 58 230 expl. 215 dec. [ 31 ]", evidence_location="Table 2", notes="decomposes with explosion")

src141 = "Molecules 2001, 6(9), 736"
url141 = "https://doi.org/10.3390/60900736"
add(compound_name="Tyrindoleninone", value_celsius=109.5, value_raw="109.5 C", source=src141, source_url=url141, evidence_quote="Tyrindoleninone: [ 112 ] red needles, mp 109.5 °C")
add(compound_name="Tyrindolinone", value_celsius=117, value_raw="117 C", source=src141, source_url=url141, evidence_quote="Tyrindolinone: [ 112 ] yellow needles, mp 117 °C")
add(compound_name="6-Bromoisatin", value_celsius=270, value_raw="270 C", source=src141, source_url=url141, evidence_quote="It is readily synthesised (see Figure 12 b) from 3-bromoaniline by the Marvel and Hiers (1941) modification of the Sandmeyer reaction (1919) followed by a pH-based separation procedure from the 4-isomer [ 118 ]. Mp 270 °C [ 118 ]; 273-274 °C [ 41 ]", notes="literature value cited; alt value 273-274 also given")

src142 = "Molecules 2002, 7(5), 437"
url142 = "https://doi.org/10.3390/70500437"
add(compound_name="Methyl 6-deoxy-2,3-O-isopropylidene-5-cyano-alpha-D-mannofuranoside (cyanohydrin 2)", value_celsius_min=119, value_celsius_max=121, value_raw="119-121 C", source=src142, source_url=url142, evidence_quote="afford white needles of cyanohydrin 2 (5.6 g, 92% yield); mp 119–121 °C")
add(compound_name="Methyl 5-O-acetyl-5-cyano-6-deoxy-2,3-O-isopropylidene-alpha-D-mannofuranoside", value_celsius_min=58, value_celsius_max=59, value_raw="58-59 C", source=src142, source_url=url142, evidence_quote="acetylation of 2 (1.22 g, 5 mmol) with Ac 2 O (7 mL) in pyridine (15 mL) overnight followed by concentration and co-evaporation with toluene at diminished pressure gave 3 (1.28 g, 90% yield) as white needles after recrystallization from a 2:1 (v/v) mixture of EtOAc–hexane; R f 0.48; mp 58–59 °C")

src143 = "Molecules 2003, 8(10), 735-743"
url143 = "https://doi.org/10.3390/81000735"
add(compound_name="4-(Methylbenzoyl)-3-[2-(4-methylbenzoyl)-2-oxo(3-hydrofuryl-5-oxy)methylphenyl)methoxy]-(5H)-furan-2-one", value_celsius=98, value_raw="98", source=src143, source_url=url143, evidence_quote="4 p -CH 3 C 6 H 4 o- C 6 H 4 (CH 2 -) 2 24 98", evidence_location="Table 1", notes="bis-ether product (4)")

src146 = "Org. Process Res. Dev. 2024, 28(1), 273-280"
url146 = "https://doi.org/10.1021/acs.oprd.3c00353"
add(compound_name="MMV693183 (N-((S)-1-((R)-2,4-dihydroxy-3,3-dimethylbutanamido)propan-2-yl)-2,4,5-trifluorobenzamide)", value_celsius=101, value_raw="101 C", source=src146, source_url=url146, evidence_quote="Melting point: 101 °C.", evidence_location="Experimental Section, MMV693183 synthesis")

for i, r in enumerate(rows, 1):
    r['id'] = i

header = ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']
out = '/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/batches/batch_pmc_07_results.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(header)
    for r in rows:
        w.writerow([r[c] for c in header])
print(f"Wrote {len(rows)} rows to {out}")

import csv, os

rows = []
nid = 0
def add(**kw):
    global nid
    nid += 1
    r = {c: '' for c in ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']}
    r['id']=nid
    r['verification_status']='pending_verification'
    r['relation']='='
    r['data_type']='measured'
    r.update(kw)
    rows.append(r)

# ==== Paper 122 ====
SRC122 = "RSC Adv. 2026, 16(22), 19903-19919"
URL122 = "https://doi.org/10.1039/d6ra02006b"

add(compound_name="N,N'-((sulfonyl)-bis(1,4-phenylene))bis(2-oxopropanehydrazonoyl chloride) (BHC)",
    property='melting_point', value_celsius=274.0, value_celsius_min=273.0, value_celsius_max=275.0,
    value_raw='273–275 °C',
    source=SRC122, source_url=URL122,
    evidence_location='Section 2.1.3 (Synthesis of BHC)',
    evidence_quote='to afford BHC as faint brown, fine crystals (4.15 g, 89% yield). Mp 273–275 °C (Lit. 271–273 (ref. 28 ))')

add(compound_name="1,1'-((Sulfonylbis(4,1-phenylene))bis(5-imino-4,5-dihydro-1,3,4-selenadiazole-4,2-diyl))-bis-(ethan-1-one) (BISDA)",
    property='melting_point', value_celsius=300.0,
    value_raw='> 300 °C', relation='>',
    source=SRC122, source_url=URL122,
    evidence_location='Section 2.1.4 (Synthesis of BISDA)',
    evidence_quote='to give BISDA as a brown microcrystalline powder (0.493 g, yield 83%). Mp > 300 °C (decomposes without melting)',
    notes='decomposes without melting')

# ==== Paper 123 ====
SRC123 = "Int. J. Mol. Sci. 2026, 27, 1738"
URL123 = "https://doi.org/10.3390/ijms27041738"

add(compound_name='Compound 4 (6-iodoquinazoline precursor, yellowish solid)',
    property='melting_point', value_celsius=189.5, value_celsius_min=188.0, value_celsius_max=191.0,
    value_raw='188–191 °C', source=SRC123, source_url=URL123,
    evidence_location='Experimental section, compound 4',
    evidence_quote='to give 4 as a yellowish solid (2.44 g, 70%). Rf = 0.22 (CH 2 Cl 2 ) and mp: 188–191 °C')

add(compound_name='N-(3-chlorophenyl)-6-iodoquinazoline-4-amine (5a)',
    property='melting_point', value_celsius=220.0, value_celsius_min=219.0, value_celsius_max=221.0,
    value_raw='219–221 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 5a',
    evidence_quote='Synthesis of N -(3-chlorophenyl)-6-iodoquinazoline-4-amine ( 5a ) An amount of 679 mg, 89%; mp: 219–221 °C')

add(compound_name='N-(4-fluorophenyl)-6-iodoquinazoline-4-amine (5b)',
    property='melting_point', value_celsius=276.0, value_celsius_min=275.0, value_celsius_max=277.0,
    value_raw='275–277 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 5b',
    evidence_quote='Synthesis of N -(4-fluorophenyl)-6-iodoquinazoline-4-amine ( 5b ) An amount of 657 mg, 90%; mp: 275–277 °C')

add(compound_name='4-N-(3-chlorophenyl)-6-(4-methylphenylacetylene)quinazoline (6a, QN017)',
    property='melting_point', value_celsius=201.0, value_celsius_min=200.0, value_celsius_max=202.0,
    value_raw='200–202 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 6a (QN017)',
    evidence_quote='6-(4-methylphenylacetylene) quinazoline ( 6a ) QN017 An amount of 60.7 mg, 82%; mp: 200–202 °C')

add(compound_name='4-N-(3-chlorophenyl)-6-(2,5-dimethylphenylacetylene)quinazoline (6b, QN019)',
    property='melting_point', value_celsius=224.0, value_celsius_min=223.0, value_celsius_max=225.0,
    value_raw='223–225 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 6b (QN019)',
    evidence_quote='(2,5-dimethylphenylacetylene) quinazoline ( 6b ) QN019 An amount of 50 mg, 65%; mp: 223–225 °C')

add(compound_name='4-N-(3-chlorophenyl)-6-(4-methoxyphenylacetylene)quinazoline (6c, QN023)',
    property='melting_point', value_celsius=252.5, value_celsius_min=252.0, value_celsius_max=253.0,
    value_raw='252–253 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 6c (QN023)',
    evidence_quote='-(4-methoxyphenylacetylene) quinazoline ( 6c ) QN023 An amount of 60.2 mg, 78%; mp: 252–253 °C')

add(compound_name='4-N-(3-chlorophenyl)-6-(3-chlorophenylacetylene)quinazoline (6d, QN022)',
    property='melting_point', value_celsius=231.0, value_celsius_min=230.0, value_celsius_max=232.0,
    value_raw='230–232 °C', source=SRC123, source_url=URL123,
    evidence_location='Synthesis of 6d (QN022)',
    evidence_quote='6-(3-chlorophenylacetylene) quinazoline ( 6d ) QN022 An amount of 58.5 mg, 75%; mp: 230–232 °C')

# ==== Paper 124 ====
SRC124 = "BMC Chemistry 2025, 19, 113"
URL124 = "https://doi.org/10.1186/s13065-025-01402-8"

c124_entries = [
    ('Compound 4 (5,6-dichloro-benzimidazole precursor, white powder)','225–227 °C',226.0,225.0,227.0,'Synthesis of compound 4','to obtain compound 4 (2.35 g, 81%) as a white powder; mp 225–227 °C'),
    ('Methyl 2-(5,6-dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetate (6)','210–212 °C',211.0,210.0,212.0,'Synthesis of compound 6','to afford compound 6 (2.10 g, 85%) as a white powder; mp 210–212 °C'),
    ('2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetohydrazide (8)','268–270 °C',269.0,268.0,270.0,'Synthesis of compound 8','to give compound 8 (1.24 g, 83%) as a buff powder; mp 268–270 °C'),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(3-hydroxybenzylidene)acetohydrazide (10a)",'168–170 °C',169.0,168.0,170.0,'Compound 10a',"N '-(3-hydroxybenzylidene)acetohydrazide (10a) A white precipitate was obtained in a yield of 72%; mp 168–170 °C"),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(4-hydroxybenzylidene)acetohydrazide (10b)",'163–165 °C',164.0,163.0,165.0,'Compound 10b',"N '-(4-hydroxybenzylidene)acetohydrazide (10b) A white precipitate was obtained in a yield of 67%; mp 163–165 °C"),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(3-methoxybenzylidene)acetohydrazide (10c)",'255–257 °C',256.0,255.0,257.0,'Compound 10c',"N '-(3-methoxybenzylidene)acetohydrazide (10c) A buff precipitate was obtained in a yield of 83%; mp 255–257 °C"),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(4-methoxybenzylidene)acetohydrazide (10d)",'265–267 °C',266.0,265.0,267.0,'Compound 10d',"N '-(4-methoxybenzylidene)acetohydrazide (10d) A white precipitate was obtained in a yield of 70%; mp 265–267 °C"),
    ('2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)acetic acid (10e)','153–155 °C',154.0,153.0,155.0,'Compound 10e','etyl)hydrazono)methyl)phenoxy)acetic acid (10e) A white precipitate was obtained in a yield of 68%; mp 153–155 °C'),
    ('2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)acetic acid (10f)','163–165 °C',164.0,163.0,165.0,'Compound 10f','cetyl)hydrazono)methyl)phenoxy)acetic acid (10f) A buff precipitate was obtained in a yield of 74%; mp 163–165 °C'),
    ('Methyl 2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)acetate (10g)','189–191 °C',190.0,189.0,191.0,'Compound 10g',')acetyl)hydrazono) methyl)phenoxy)acetate (10g) A white precipitate was obtained in a yield of 81%; mp 189–191 °C'),
    ('Methyl 2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)acetate (10h)','195–197 °C',196.0,195.0,197.0,'Compound 10h','l)acetyl)hydrazono)methyl)phenoxy)acetate (10h) A white precipitate was obtained in a yield of 76%; mp 195–197 °C'),
    ('2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)propanoic acid (10i)','164–166 °C',165.0,164.0,166.0,'Compound 10i','o)methyl)phenoxy)propanoic acid (10i) A yellowish-white precipitate was obtained in a yield of 83%; mp 164–166 °C'),
    ('Ethyl 2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)phenoxy)propanoate (10j)','200–202 °C',201.0,200.0,202.0,'Compound 10j','etyl) hydrazono)methyl)phenoxy)propanoate (10j) A white precipitate was obtained in a yield of 71%; mp 200–202 °C'),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(3-hydroxy-4-methoxybenzylidene)acetohydrazide (10k)",'156–158 °C',157.0,156.0,158.0,'Compound 10k','droxy-4-methoxy benzylidene)acetohydrazide (10k) A buff precipitate was obtained in a yield of 69%; mp 156–158 °C'),
    ("2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)-N'-(4-hydroxy-3-methoxybenzylidene)acetohydrazide (10l)",'151–153 °C',152.0,151.0,153.0,'Compound 10l','roxy-3-methoxy benzylidene)acetohydrazide (10l) A white precipitate was obtained in a yield of 78%; mp 151–153 °C'),
    ('2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)-2-methoxyphenoxy)acetic acid (10m)','262–264 °C',263.0,262.0,264.0,'Compound 10m',') -2-methoxyphenoxy)acetic acid (10m) A yellowish-white precipitate was obtained in a yield of 72%; mp 262–264 °C'),
    ('2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)-2-methoxyphenoxy)acetic acid (10n)','260–263 °C',261.5,260.0,263.0,'Compound 10n','zono)methyl)-2-methoxyphenoxy)acetic acid (10n) A white precipitate was obtained in a yield of 80%; mp 260–263 °C'),
    ('Methyl 2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)-2-methoxyphenoxy)acetate (10o)','186–188 °C',187.0,186.0,188.0,'Compound 10o','hydrazono)methyl)-2-methoxyphenoxy)acetate (10o) A buff precipitate was obtained in a yield of 69%; mp 186–188 °C'),
    ('Methyl 2-(4-((2-(2-(5,6-Dichloro-2-(4-methoxyphenyl)-1H-benzo[d]imidazol-1-yl)acetyl)hydrazono)methyl)-2-methoxyphenoxy)acetate (10p)','190–192 °C',191.0,190.0,192.0,'Compound 10p','ydrazono)methyl)-2-methoxyphenoxy)acetate (10p) A white precipitate was obtained in a yield of 77%; mp 190–192 °C'),
]
for name,raw,c,lo,hi,loc,quote in c124_entries:
    add(compound_name=name, property='melting_point',
        value_celsius=c, value_celsius_min=lo, value_celsius_max=hi, value_raw=raw,
        source=SRC124, source_url=URL124, evidence_location=loc, evidence_quote=quote)

# ==== Paper 125 ====
SRC125 = "RSC Adv. 2025, 15, 5895-5905"
URL125 = "https://doi.org/10.1039/d4ra07810a"

c125_entries = [
    ("N'-(4-Hydroxybenzylidene)benzo[d]thiazole-2-carbohydrazide (6a)", '285–257 °C', 271.0, 257.0, 285.0, 'Section 3.1.1.1, Compound 6a',
     'N ′-(4-Hydroxybenzylidene)benzo[ d ]thiazole-2-carbohydrazide (6a) Yield: 98%; mp 285–257 °C', 'flagged_review',
     'flagged_value_out_of_range; source reports descending "285-257" -- likely typographic error in paper; recorded verbatim'),
    ("N'-(4-Hydroxy-3-methoxybenzylidene)benzo[d]thiazole-2-carbohydrazide (6b)", '232–234 °C', 233.0, 232.0, 234.0, 'Section 3.1.1.2, Compound 6b',
     'N′ -(4-Hydroxy-3-methoxybenzylidene)benzo[ d ]thiazole-2-carbohydrazide (6b) Yield: 91%; mp 232–234 °C', None, ''),
    ("N'-(3-Hydroxy-4-methoxybenzylidene)benzo[d]thiazole-2-carbohydrazide (6c)", '250–252 °C', 251.0, 250.0, 252.0, 'Section 3.1.1.3, Compound 6c',
     "N '-(3-Hydroxy-4-methoxybenzylidene)benzo[ d ]thiazole-2-carbohydrazide (6c) Yield: 78%; mp 250–252 °C", None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)phenyl methanesulfonate (6d)', '219–221 °C', 220.0, 219.0, 221.0, 'Section 3.1.1.4, Compound 6d',
     '4-((2-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)phenyl methanesulfonate (6d) Yield: 76%; mp 219–221 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl methanesulfonate (6e)', '185–187 °C', 186.0, 185.0, 187.0, 'Section 3.1.1.5, Compound 6e',
     '-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl methanesulfonate (6e) Yield: 80%; mp 185–187 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl methanesulfonate (6f)', '221–223 °C', 222.0, 221.0, 223.0, 'Section 3.1.1.6, Compound 6f',
     '-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl methanesulfonate (6f) Yield: 99%; mp 221–223 °C', None,
     'name as printed appears identical to 6e in this segment; structural difference vs 6e per scheme; retained verbatim'),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)phenyl ethanesulfonate (6g)', '191–193 °C', 192.0, 191.0, 193.0, 'Section 3.1.1.7, Compound 6g',
     '4-((2-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)phenyl ethanesulfonate (6g) Yield: 72%; mp 191–193 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl ethanesulfonate (6h)', '175–177 °C', 176.0, 175.0, 177.0, 'Section 3.1.1.8, Compound 6h',
     '2-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl ethanesulfonate (6h) Yield: 78%; mp 175–177 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl ethanesulfonate (6i)', '215–217 °C', 216.0, 215.0, 217.0, 'Section 3.1.1.9, Compound 6i',
     '-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyph-enyl ethanesulfonate (6i) Yield: 65%; mp 215–217 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)phenyl propane-1-sulfonate (6j)', '176–178 °C', 177.0, 176.0, 178.0, 'Section 3.1.1.10, Compound 6j',
     '4-((2-(Benzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)phenyl propane-1-sulfonate (6j) Yield: 65%; mp 176–178 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl propane-1-sulfonate (6k)', '150–152 °C', 151.0, 150.0, 152.0, 'Section 3.1.1.11, Compound 6k',
     'enzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl propane-1-sulfonate (6k) Yield: 66%; mp 150–152 °C', None, ''),
    ('4-((2-(Benzo[d]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl propane-1-sulfonate (6l)', '210–212 °C', 211.0, 210.0, 212.0, 'Section 3.1.1.12, Compound 6l',
     'enzo[ d ]thiazole-2-carbonyl)hydrazono)methyl)-2-methoxyphenyl propane-1-sulfonate (6l) Yield: 70%; mp 210–212 °C', None, ''),
]
for name,raw,c,lo,hi,loc,quote,vstat,nt in c125_entries:
    extra = {}
    if vstat: extra['verification_status'] = vstat
    if nt: extra['notes'] = nt
    add(compound_name=name, property='melting_point', value_celsius=c, value_celsius_min=lo, value_celsius_max=hi, value_raw=raw,
        source=SRC125, source_url=URL125, evidence_location=loc, evidence_quote=quote, **extra)

# ==== Paper 126 ====
SRC126 = "Polymers 2026, 18, 655"
URL126 = "https://doi.org/10.3390/polym18050655"
add(compound_name='L-lactide', property='melting_point', value_celsius=98.11, value_raw='98.11 °C',
    source=SRC126, source_url=URL126, evidence_location='Section 3.5 (DSC)',
    evidence_quote='The melting point of the purified lactide was found to be 98.11 °C',
    notes='abstract reports 98.1 °C (truncated form of same DSC measurement); only the precise DSC value retained to avoid intra-paper duplicate')
add(compound_name='L-polylactide (PLA)', property='melting_point', value_celsius=160.0, value_raw='about 160 °C', relation='~',
    source=SRC126, source_url=URL126, evidence_location='Materials section (Section 2.1)',
    evidence_quote='L-polylactide with molecular weight about 165 kDa and melting temperature about 160 °C')

# ==== Paper 127 ====
SRC127 = "Russian Journal of Organic Chemistry 2022, 58, 1434-1437"
URL127 = "https://doi.org/10.1134/S1070428022100086"

c127_entries = [
    ('6-[(2-Hydroxybenzylidene)amino]-2-methylquinolin-4-ol (2)','melting_point','326–327°C',326.5,326.0,327.0,'=',
     'Synthesis of compound 2','Yield 0.20 g (72%), mp 326–327°C, R f 0.52 (EtOH–xylene, 1:1)'),
    ('2-(4-Hydroxy-2-methylquinolin-6-yl)-1H-isoindole-1,3(2H)-dione (3)','decomposition','350°C (decomp.)',350.0,None,None,'=',
     'Synthesis of compound 3','Yield 0.27 g (89%), mp 350°C (decomp.), R f 0.57 (EtOH–xylene, 1:1.5)'),
    ("N-(4-Hydroxy-2-methylquinolin-6-yl)-N'-phenylthiourea (4)",'decomposition','325°C (decomp.)',325.0,None,None,'=',
     'Synthesis of compound 4','Yield 1.30 g (85%), mp 325°C (decomp.), R f 0.60 (EtOH–xylene, 1:2.5)'),
    ('N-(4-Hydroxy-2-methylquinolin-6-yl)thiourea (5)','melting_point','242–243°C',242.5,242.0,243.0,'=',
     'Synthesis of compound 5','Yield 1.51 g (65%), mp 242–243°C, R f 0.52 (EtOH–xylene, 1:2)'),
    ('2-[(4-Hydroxy-2-methylquinolin-6-yl)imino]-1,3-thiazolidin-4-one (6)','decomposition','375°C (decomp.)',375.0,None,None,'=',
     'Synthesis of compound 6','Yield 0.23 g (85%), mp 375°C (decomp.), R f 0.50 (EtOH–xylene, 1:3)'),
    ('2-Methyl-6-{[4-phenyl-1,3-thiazol-2(3H)ylidene]amino}quinolin-4-ol (7)','melting_point','305–306°C',305.5,305.0,306.0,'=',
     'Synthesis of compound 7','Yield 0.31 g (93%), mp 305–306°C, R f 0.67 (EtOH–PhMe, 1:1)'),
]
for name,prop,raw,c,lo,hi,rel,loc,quote in c127_entries:
    add(compound_name=name, property=prop, value_celsius=c,
        value_celsius_min=(lo if lo is not None else ''),
        value_celsius_max=(hi if hi is not None else ''),
        value_raw=raw, relation=rel,
        source=SRC127, source_url=URL127, evidence_location=loc, evidence_quote=quote)

# ==== Paper 128 ====
SRC128 = "Molecules 2002, 7, 767-776"
URL128 = "https://doi.org/10.3390/71000767"

add(compound_name='(2S,11S,3Z,9Z)-2,11-Di[(tert-butoxycarbonyl)amino]-1,12-diphenyldodeca-3,9-diene (2a)',
    property='melting_point', value_celsius=92.0, value_celsius_min=91.0, value_celsius_max=93.0,
    value_raw='91–93 °C', source=SRC128, source_url=URL128,
    evidence_location='Experimental, Compound 2a',
    evidence_quote='(2S,11S,3Z,9Z)-2,11-Di[(tert-butoxycarbonyl)amino]-1,12-diphenyldodeca-3,9-diene ( 2a ): yield 626 mg (57%); yellow solid; mp 91–93 o C')

add(compound_name='(5S,14S,6Z,12Z)-1,5,14,18-Tetra[(tert-butoxycarbonyl)amino]-octadeca-6,12-diene (2b)',
    property='melting_point', value_celsius=87.5, value_celsius_min=87.0, value_celsius_max=88.0,
    value_raw='87–88 °C', source=SRC128, source_url=URL128,
    evidence_location='Experimental, Compound 2b',
    evidence_quote='4,18-Tetra[(tert-butoxycarbonyl)amino]-octadeca-6,12-diene ( 2b ): yield 611 mg (43%); white solid; mp 87–88 o C')

add(compound_name='(5R)-1,5-Di[(tert-butoxycarbonyl)amino]-dodecane (5)',
    property='melting_point', value_celsius=63.5, value_celsius_min=63.0, value_celsius_max=64.0,
    value_raw='63–64 °C', source=SRC128, source_url=URL128,
    evidence_location='Experimental, Compound 5',
    evidence_quote='Yield 365 mg (91%); white solid; mp 63–64 o C')

# ==== Paper 129 ====
SRC129 = "Molecules 2002, 7, 252-263"
URL129 = "https://doi.org/10.3390/70200252"

add(compound_name='Compound 4a (3-ethoxycarbonyl-6,7-dimethoxyisoquinoline + diethyl aminomalonate adduct, yellowish needles)',
    property='melting_point', value_celsius=175.0, value_celsius_min=174.0, value_celsius_max=176.0,
    value_raw='174–176 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 4a',
    evidence_quote='Recrystallization from AcOEt gave 0.94 g. of pure compound 4a (70% yield) as yellowish needles. Mp = 174-76°C',
    notes='source uses abbreviated range "174-76°C" (i.e. 174–176 °C); value_raw normalized to full form per skill convention; evidence_quote verbatim')

add(compound_name='Compound 4b (3-ethoxycarbonylisoquinoline + diethyl aminomalonate adduct, colourless oil)',
    property='boiling_point', value_celsius=80.0, value_raw='80 °C',
    source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 4b',
    evidence_quote='4b was obtained in 80% yield (1.2 g.) as a mobile and colourless oil (bp = 80°C / 0.4 Torr)',
    notes='bp at reduced pressure 0.4 Torr (not atmospheric); value_raw simplified to °C; full quote contains pressure context')

add(compound_name='3-Ethoxycarbonyl-2-benzyl isoquinolinium bromide (5a)',
    property='melting_point', value_celsius=133.0, value_celsius_min=132.0, value_celsius_max=134.0,
    value_raw='132–134 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 5a',
    evidence_quote='3-Ethoxycarbonyl-2-benzyl isoquinolinium bromide ( 5a ). Yield = 90%; mp = 132-34°C (moisture sensitive)',
    notes='source uses abbreviated range "132-34°C" (i.e. 132–134 °C); value_raw normalized; quote verbatim')

add(compound_name='3-Ethoxycarbonyl-2-(3-hydroxypropyl)-isoquinolinium chloride (5c)',
    property='melting_point', value_celsius=143.0, value_celsius_min=142.0, value_celsius_max=144.0,
    value_raw='142–144 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 5c',
    evidence_quote='3-Ethoxycarbonyl-2-(3-hydroxypropyl)-isoquinolinium chloride ( 5c ). Yield = 53%; mp = 142-44°C (moisture sensitive)',
    notes='abbreviated range "142-44°C" normalized; quote verbatim')

add(compound_name='10-Oxo-6,7,8,10-tetrahydro-9-oxo-[5a]-azonia-cyclohepta[b]naphtalene bromide (5d)',
    property='melting_point', value_celsius=245.0, value_celsius_min=244.0, value_celsius_max=246.0,
    value_raw='244–246 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 5d',
    evidence_quote='10-Oxo-6,7,8,10-tetrahydro-9-oxo-[5a]-azonia-cyclohepta[b]naphtalene bromide ( 5d ). Yield = 75%, mp = 244-46°C (hygroscopic salt)',
    notes='abbreviated range "244-46°C" normalized; quote verbatim')

add(compound_name='3-Ethoxycarbonyl-2-ethoxycarbonylmethyl-6,7-dimethoxy isoquinolinium bromide (5e)',
    property='melting_point', value_celsius=191.0, value_celsius_min=190.0, value_celsius_max=192.0,
    value_raw='190–192 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 5e',
    evidence_quote='3-Ethoxycarbonyl-2-ethoxycarbonylmethyl-6,7-dimethoxy isoquinolinium bromide ( 5e ). Yield = 86%, mp = 190-92°C (moisture sensitive)',
    notes='abbreviated range normalized; quote verbatim')

add(compound_name='3-Ethoxycarbonyl-2-ethoxycarbonylmethyl isoquinolinium bromide (5f)',
    property='melting_point', value_celsius=153.0, value_celsius_min=152.0, value_celsius_max=154.0,
    value_raw='152–154 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Compound 5f',
    evidence_quote='3-Ethoxycarbonyl-2-ethoxycarbonylmethyl isoquinolinium bromide ( 5f ). Yield = 96%, mp = 152‑54°C (moisture sensitive)',
    notes='abbreviated range normalized; quote verbatim')

add(compound_name='Salt 5b (3-Ethoxycarbonyl-2-benzyl isoquinolinium salt, colourless needles)',
    property='melting_point', value_celsius=93.0, value_celsius_min=92.0, value_celsius_max=94.0,
    value_raw='92–94 °C', source=SRC129, source_url=URL129,
    evidence_location='Experimental, Salt 5b (alternative preparation)',
    evidence_quote='The salt 5b was obtained in 86% yield (2.04 g.) as colourless needles, mp = 92-94°C',
    notes='alternative preparation of salt 5b; quote verbatim; range "92-94°C" normalized')

# ==== Paper 130 ====
SRC130 = "Molecules 2002, 7, 840-847"
URL130 = "https://doi.org/10.3390/71100840"

add(compound_name='4,5,6,7-Tetrachloro-2-phenyl-1,3-benzodioxole (13)',
    property='melting_point', value_celsius=114.5, value_celsius_min=114.0, value_celsius_max=115.0,
    value_raw='114–115 °C', source=SRC130, source_url=URL130,
    evidence_location='Experimental, Compound 13',
    evidence_quote='4,5,6,7-Tetetrachloro-2-phenyl-1,3-benzodioxole ( 13 ) : 21%; colorless needles (from methanol); mp 114–115 °C (lit [ 15 ] mp 119 °C)',
    notes='paper printed name as "Tetetrachloro" (sic) — likely typo for Tetrachloro')

add(compound_name='4,5,6,7-Tetrachloro-2,2-diphenyl-1,3-benzodioxole (14)',
    property='melting_point', value_celsius=152.5, value_celsius_min=152.0, value_celsius_max=153.0,
    value_raw='152–153 °C', source=SRC130, source_url=URL130,
    evidence_location='Experimental, Compound 14',
    evidence_quote='4,5,6,7-Tetrachloro-2,2-diphenyl-1,3-benzodioxole ( 14 ) : 26%; colorless prisms (from chloroform–methanol 1/1); mp 152–153 °C (lit [ 16 ] mp 141 °C)')

add(compound_name='4,5,6,7-Tetrachloro-2-(2,5-dimethylphenyl)-2-(4-methylphenyl)-1,3-benzodioxole (17)',
    property='melting_point', value_celsius=132.5, value_celsius_min=132.0, value_celsius_max=133.0,
    value_raw='132–133 °C', source=SRC130, source_url=URL130,
    evidence_location='Experimental, Compound 17',
    evidence_quote='5-dimethylphenyl)-2-(4-methylphenyl)-1,3-benzodioxole ( 17 ) : 14%; colorless prisms (from hexane); mp 132–133 °C')

add(compound_name='6,7,8,9-Tetrachloro-10a,11-dihydro-4bH-5,10-dioxabenzo[b]fluorene (18)',
    property='melting_point', value_celsius=158.75, value_celsius_min=158.0, value_celsius_max=159.5,
    value_raw='158–159.5 °C', source=SRC130, source_url=URL130,
    evidence_location='Experimental, Compound 18 (from toluene + o-chloranil)',
    evidence_quote='hydro-4bH-5,10-dioxabenzo[b]fluorene ( 18 ) : 5%; colorless needles (from chloroform–methanol 1/1); mp 158–159.5 °C')

add(compound_name='6,7,8,9-Tetrachloro-10a,11-dihydro-4bH-5,10-dioxabenzo[b]fluorene (18, from indene + o-chloranil)',
    property='melting_point', value_celsius=156.5, value_celsius_min=156.0, value_celsius_max=157.0,
    value_raw='156–157 °C', source=SRC130, source_url=URL130,
    evidence_location='Experimental, Reaction of Indene with o-Chloranil, Compound 18',
    evidence_quote='give 18 (212 mg, 12%): mp and mixed mp 156–157 °C',
    notes='same compound 18 as previous row, alternative synthesis route (indene); paper distinguishes the two preparations')

# ==== Paper 131 ====
SRC131 = "Molecules 2002, 7, 315-319"
URL131 = "https://doi.org/10.3390/70200315"

add(compound_name='2-Hydroxy-4-O-methoxymethylbenzaldehyde (5)',
    property='melting_point', value_celsius=50.5, value_celsius_min=50.0, value_celsius_max=51.0,
    value_raw='50-51 °C', source=SRC131, source_url=URL131,
    evidence_location='Experimental, Compound 5',
    evidence_quote='afforded a white solid (118 mg, 84%); Mp: 50-51 o C')

add(compound_name='2-Methoxy-4-O-methoxymethylbenzaldehyde (6)',
    property='melting_point', value_celsius=73.5, value_celsius_min=73.0, value_celsius_max=74.0,
    value_raw='73-74 °C', source=SRC131, source_url=URL131,
    evidence_location='Experimental, Compound 6',
    evidence_quote='afforded a white solid (1.69 g, 93%); Mp: 73-74 o C')

add(compound_name='3-(4-hydroxy-2-methoxyphenyl)-propanoic acid (7)',
    property='melting_point', value_celsius=105.5, value_celsius_min=105.0, value_celsius_max=106.0,
    value_raw='105-106 °C', source=SRC131, source_url=URL131,
    evidence_location='Experimental, Compound 7',
    evidence_quote='afforded a white solid (405 mg, 81%); Mp: 105-106 o C')

add(compound_name='6-Methoxy-1-oxaspiro[4,5]deca-6,9-diene-8-one (3)',
    property='melting_point', value_celsius=108.5, value_celsius_min=108.0, value_celsius_max=109.0,
    value_raw='108-109 °C', source=SRC131, source_url=URL131,
    evidence_location='Experimental, Compound 3',
    evidence_quote='afforded a white solid (46 mg, 46%); Mp: 108-109 o C')

# ==== Paper 133 ====
SRC133 = "Molecules 2002, 7, 382-385"
URL133 = "https://doi.org/10.3390/70400382"

add(compound_name='2-[3-chloro-2-(toluene-4-sulfonylmethyl)propenyl]-1-methyl-5-nitro-1H-imidazole (3) (E:Z 1:2)',
    property='melting_point', value_celsius=134.0, value_raw='134 °C',
    source=SRC133, source_url=URL133,
    evidence_location='Experimental, Compound 3',
    evidence_quote='2-[3-chloro-2-(toluene-4-sulfonylmethyl)propenyl]-1-methyl-5-nitro-1 H -imidazole ( 3 ) ( E : Z , 1:2): Brown solid, mp 134 °C (ethanol)')

add(compound_name='3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester (4E)',
    property='melting_point', value_celsius=115.0, value_raw='115 °C',
    source=SRC133, source_url=URL133,
    evidence_location='Experimental, Compound 4E',
    evidence_quote='3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester ( 4E ): Yellow solid, mp 115 °C (ethanol)')

add(compound_name='3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester (4Z)',
    property='melting_point', value_celsius=118.0, value_raw='118 °C',
    source=SRC133, source_url=URL133,
    evidence_location='Experimental, Compound 4Z',
    evidence_quote='3-(1-methyl-5-nitro-1H-imidazol-2-yl)-2-(2-methyl-2-nitropropyl)prop-2-ene-1-sulfinic acid p-tolyl ester ( 4Z ): Yellow solid, mp 118 °C (ethanol)')

# ==== Paper 134 ====
SRC134 = "Molecules 2002, 7, 511-516"
URL134 = "https://doi.org/10.3390/70700511"

add(compound_name="N,N'-(1R,2R)-(-)-1,2-cyclohexylenebis(2-hydroxyacetophenonylideneimine) (2)",
    property='melting_point', value_celsius=144.5, value_celsius_min=144.0, value_celsius_max=145.0,
    value_raw='144-145°C', source=SRC134, source_url=URL134,
    evidence_location='Experimental, Compound 2',
    evidence_quote='Recrystallization from absolute ethanol afforded yellow needles (303mg, 70.5%); mp: 144-145°C')

add(compound_name='(1S,2S)-(-)-1,2-diphenylethylenebis(2-hydroxyacetophenonylideneimine) (3)',
    property='melting_point', value_celsius=174.0, value_celsius_min=173.0, value_celsius_max=175.0,
    value_raw='173-175°C', source=SRC134, source_url=URL134,
    evidence_location='Experimental, Compound 3',
    evidence_quote='afforded bright yellow crystals (312mg, 69.6%), mp: 173-175°C')

add(compound_name="R-(+)-1,1'-binaphthalene-2,2'-diaminobis(2-hydroxyacetophenonylideneimine) (4)",
    property='melting_point', value_celsius=263.0, value_celsius_min=262.0, value_celsius_max=264.0,
    value_raw='262–264 °C', source=SRC134, source_url=URL134,
    evidence_location='Experimental, Compound 4',
    evidence_quote='afforded bright yellow needles (118mg, 25.1%), mp: 262-264°',
    notes='source omits "C" after degree symbol; value_raw normalized to °C since the paper section uses °C throughout for mp values; quote verbatim')

# ==== Write CSV ====
fieldnames = ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']
out = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_10.csv'
with open(out,'w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,fieldnames=fieldnames,quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print('Total rows:', len(rows))
print('Output:', out)

# Counts per paper
from collections import Counter
c = Counter(r['source_url'] for r in rows)
for k,v in c.items():
    print(' ', k, '->', v)

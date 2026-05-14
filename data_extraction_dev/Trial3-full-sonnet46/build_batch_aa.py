import csv, io, sys

COLS = ['id','verification_status','compound_name','compound_smiles','property',
        'value_celsius','value_celsius_min','value_celsius_max','value_raw','relation',
        'data_type','source','source_url','evidence_location','evidence_quote',
        'conversion_arithmetic','notes']

def mid(lo, hi): return (lo+hi)/2

rows = []

def add(compound, prop, vc, vcmin, vcmax, raw, rel, dtype, src, url, loc, quote, conv='', notes=''):
    rows.append({
        'id': '',
        'verification_status': 'pending_verification',
        'compound_name': compound,
        'compound_smiles': '',
        'property': prop,
        'value_celsius': vc,
        'value_celsius_min': vcmin,
        'value_celsius_max': vcmax,
        'value_raw': raw,
        'relation': rel,
        'data_type': dtype,
        'source': src,
        'source_url': url,
        'evidence_location': loc,
        'evidence_quote': quote,
        'conversion_arithmetic': conv,
        'notes': notes,
    })

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 005  DOI: 10.1002/cmdc.202500751
# ChemMedChem 2025 (online)
# ═══════════════════════════════════════════════════════════════════════════
s5 = 'ChemMedChem, 2025 (online)'
u5 = 'https://doi.org/10.1002/cmdc.202500751'

# 9-series (tetrahydro phosphine oxides)
add('Diphenyl(6-Phenyl-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(232,234),232,234,'232-234°C','=','measured',s5,u5,
    'Experimental section 6.2.2.1, compound 9a',
    "Diphenyl(6-Phenyl-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9a) The general procedure A was followed using benzaldehyde 5a (10 mmol, 1.0 ml), for 10 hr at room temperature, affording 3.83 g (77%) of 9a as a white solid, mp 232-234°C (ethyl acetate/hexane).")

add('Diphenyl(6-(4-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    201,200,202,'200°C-202°C','=','measured',s5,u5,
    'Experimental section 6.2.2.2, compound 9b',
    "Diphenyl(6-(4-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9b) The general procedure A was followed using 4-fluorobenzaldehyde 5b (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.38 g (85%) of 9b as a white solid, mp 200°C-202°C (ethyl acetate/hexane).")

add('Diphenyl(6-(4-(Trifluoromethyl)Phenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(234,236),234,236,'234-236°C','=','measured',s5,u5,
    'Experimental section 6.2.2.3, compound 9c',
    "Diphenyl(6-(4-(Trifluoromethyl)Phenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9c) The general procedure A was followed using 4-trifluorobenzaldehyde 5c (10 mmol, 1.7 ml), for 30 min at room temperature, affording 5.08 g (90%) of 9c as a yellow solid mp 234-236°C (ethyl acetate/hexane).")

add('Diphenyl(6-(4-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(212,213),212,213,'212-213°C','=','measured',s5,u5,
    'Experimental section 6.2.2.4, compound 9d',
    "Diphenyl(6-(4-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9d) The general procedure A was followed using 4-nitrobenzaldehyde 5d (10 mmol, 1.5 mL), heated to reflux for 24 hr affording 2.93 g (54%) of 9d as a yellow solid, mp 212-213°C (ethyl acetate/hexane).")

add('Diphenyl(6-(3-Methoxyphenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(134,135),134,135,'134-135°C','=','measured',s5,u5,
    'Experimental section 6.2.2.5, compound 9f',
    "Diphenyl(6-(3-Methoxyphenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9f) The general procedure A was followed using m-methoxybenzaldehyde 5f (10 mmol, 1.2 mL), for 6.5 h at room temperature affording 3.58 g (68%) of 9f as a yellow solid, mp 134-135°C (ethyl acetate/hexane).")

add('Diphenyl(6-(3-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(207,209),207,209,'207°C-209°C','=','measured',s5,u5,
    'Experimental section 6.2.2.6, compound 9g',
    "Diphenyl(6-(3-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9g) The general procedure A was followed using 3-fluorobenzaldehyde 5g (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.17 g (81%) of 9g as a yellow solid, mp 207°C-209°C (ethyl acetate/hexane).")

add('Diphenyl(6-(3-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(228,231),228,231,'228-231°C','=','measured',s5,u5,
    'Experimental section 6.2.2.7, compound 9Hr',
    "Diphenyl(6-(3-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9Hr) The general procedure A was followed using 3-nitrobenzaldehyde 5h (10 mmol, 1.5 mL), heated to reflux for 48 h affording 3.67 g (68%) of 9h as a yellow solid, mp 228-231°C (ethyl acetate/hexane).")

add('Diphenyl(6-(2,4-Difluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(126,127),126,127,'126-127°C','=','measured',s5,u5,
    'Experimental section 6.2.2.8, compound 9i',
    "Diphenyl(6-(2,4-Difluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9i) The general procedure A was followed using 2,4-difluorobenzaldehyde 5i (10 mmol, 1.2 mL), heated to reflux for 48 h affording 3.31 g (62%) of 9i as a white solid, mp 126-127°C (ethyl acetate/hexane).")

add('Diphenyl(6-(Naphthalen-1-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(267,269),267,269,'267-269°C','=','measured',s5,u5,
    'Experimental section 6.2.2.9, compound 9j',
    "Diphenyl(6-(Naphthalen-1-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9j) The general procedure A was followed using 1-naphthaldehyde 5j (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.44 g (63%) of 9j as a white solid, mp 267-269°C (ethyl acetate/hexane).")

add('Diphenyl(6-(Naphthalen-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(222,224),222,224,'222-224°C','=','measured',s5,u5,
    'Experimental section 6.2.2.10, compound 9k',
    "Diphenyl(6-(Naphthalen-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9k) The general procedure A was followed using 2-naphthaldehyde 5k (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.67 g (67%) of 9k as a light-yellow solid, mp 222-224°C (ethyl acetate/hexane).")

add('Diphenyl(6-(Pyridin-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(214,216),214,216,'214-216°C','=','measured',s5,u5,
    'Experimental section 6.2.2.11, compound 9l',
    "Diphenyl(6-(Pyridin-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9l) The general procedure A was followed using picolinaldehyde 5l (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.64 g (73%) of 9l as a brown solid, mp 214-216°C (ethyl acetate/hexane).")

add('Diphenyl(6-(Pyridin-4-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(219,222),219,222,'219-222°C','=','measured',s5,u5,
    'Experimental section 6.2.2.12, compound 9m',
    "Diphenyl(6-(Pyridin-4-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9m) The general procedure B was followed using isonicotinaldehyde 5m (10 mmol, 1.5 mL), affording 3.09 g (62%) of 9 m as a yellow solid, mp 219-222°C (ethyl acetate/hexane).")

add('Diphenyl(6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide','melting_point',
    mid(212,213),212,213,'212-213°C','=','measured',s5,u5,
    'Experimental section 6.2.2.13, compound 10e',
    "Diphenyl(6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (10e) The general procedure A was followed using 4-methoxybenzaldehyde 5e (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.40 g (65%) of 10e as a yellow solid, mp 212-213°C (ethyl acetate/hexane).")

# 11-series (aromatic, quinolinone phosphine oxides)
add('4-(Diphenylphosphoryl)-6-Phenyl-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(274,275),274,275,'274-275°C','=','measured',s5,u5,
    'Experimental section 6.3.2.1, compound 11a',
    "4-(Diphenylphosphoryl)-6-Phenyl-7H-Indeno[2,1-c]Quinolin-7-One (11a) The general procedure A was followed using diphenyl(6-phenyl-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9a (0.25 mmol, 0.13 g), affording 0.09 g (70%) of 11a as a yellow solid, mp 274-275°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(4-(Trifluoromethyl)Phenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(308,309),308,309,'308°C-309°C','=','measured',s5,u5,
    'Experimental section 6.3.2.2, compound 11c',
    "4-(Diphenylphosphoryl)-6-(4-(Trifluoromethyl)Phenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11c) The general procedure A was followed using diphenyl(6-(4-(trifluoromethyl)phenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9c (0.25 mmol, 0.13 g), affording 0.10 g (73%) of 11c as a yellow solid, mp 308°C-309°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(4-Nitrophenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(295,296),295,296,'295°C-296°C','=','measured',s5,u5,
    'Experimental section 6.3.2.3, compound 11d',
    "4-(Diphenylphosphoryl)-6-(4-Nitrophenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11d) The general procedure A was followed using diphenyl(6-(4-nitrophenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9d (0.25 mmol, 0.13 g), affording 0.10 g (75%) of 11d as an orange solid, mp 295°C-296°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(275,276),275,276,'275-276°C','=','measured',s5,u5,
    'Experimental section 6.3.2.4, compound 11e',
    "4-(Diphenylphosphoryl)-6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11e) The general procedure A was followed using diphenyl(6-(4-methoxyphenyl)-7 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 10e (0.25 mmol, 0.13 g), affording 0.13 g (99%) of 11e as a yellow solid, mp 275-276°C (ethyl acetate/hexane).")

add('4-(Diphenylphosphoryl)-6-(3-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(283,285),283,285,'283°C-285°C','=','measured',s5,u5,
    'Experimental section 6.3.2.5, compound 11f',
    "4-(Diphenylphosphoryl)-6-(3-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11f) The general procedure A was followed using diphenyl(6-(3-methoxyphenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9f (0.25 mmol, 0.13 g), affording 0.13 g (99%) of 11f as a yellow solid, mp 283°C-285°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(3-Fluorophenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(270,273),270,273,'270°C-273°C','=','measured',s5,u5,
    'Experimental section 6.3.2.6, compound 11g',
    "4-(Diphenylphosphoryl)-6-(3-Fluorophenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11g) The general procedure B was followed using diphenyl(6-(3-fluorophenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9g (0.25 mmol, 0.13 g), affording 0.10 g (77%) of 11g as a yellow solid, mp 270°C-273°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(3-Nitrophenyl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(171,173),171,173,'171°C-173°C','=','measured',s5,u5,
    'Experimental section 6.3.2.7, compound 11hr',
    "4-(Diphenylphosphoryl)-6-(3-Nitrophenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11h) The general procedure B was followed using diphenyl(6-(3-nitrophenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9hr (0.25 mmol, 0.13 g), affording 0.12 g (87%) of 11hr as a yellow solid, mp 171°C-173°C (ethyl ether/ethyl acetate).")

add('6-(2,4-Difluorophenyl)-4-(Diphenylphosphoryl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(182,183),182,183,'182°C-183°C','=','measured',s5,u5,
    'Experimental section 6.3.2.8, compound 11i',
    "6-(2,4-Difluorophenyl)-4-(Diphenylphosphoryl)-7H-Indeno[2,1-c]Quinolin-7-One (11i) The general procedure A was followed using diphenyl-4(6-(2,4-difluorophenyl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9i (0.25 mmol, 0.13 g), affording 0.07 g (48%) of 11i as an orange solid, mp 182°C-183°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(Naphthalen-2-Yl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(213,214),213,214,'213°C-214°C','=','measured',s5,u5,
    'Experimental section 6.3.2.9, compound 11k',
    "4-(Diphenylphosphoryl)-6-(Naphthalen-2-Yl)-7H-Indeno[2,1-c]Quinolin-7-One (11k) The general procedure A was followed using diphenyl(6-(naphthalen-2-yl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9k (0.25 mmol, 0.13 g), affording 0.02 g (14%) of 11k as a yellow solid, mp 213°C-214°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(Pyridin-2-Yl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(268,271),268,271,'268°C-271°C','=','measured',s5,u5,
    'Experimental section 6.3.2.10, compound 11l',
    "4-(Diphenylphosphoryl)-6-(Pyridin-2-Yl)-7H-Indeno[2,1-c]Quinolin-7-One (11l) The general procedure B was followed using diphenyl(6-(pyridin-2-yl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9l (0.25 mmol, 0.13 g), affording 0.10 g (78%) of 11l as a yellow solid, mp 268°C-271°C (ethyl ether/ethyl acetate).")

add('4-(Diphenylphosphoryl)-6-(Pyridin-4-Yl)-7H-Indeno[2,1-c]Quinolin-7-One','melting_point',
    mid(287,290),287,290,'287°C-290°C','=','measured',s5,u5,
    'Experimental section 6.3.2.11, compound 11m',
    "4-(Diphenylphosphoryl)-6-(Pyridin-4-Yl)-7H-Indeno[2,1-c]Quinolin-7-One (11m) The general procedure B was followed using diphenyl(6-(pyridin-4-yl)-6,6a,7,11b-tetrahydro-5 H -indeno[2,1- c ]quinolin-4-yl)phosphine oxide 9m (0.25 mmol, 0.13 g), affording 0.08 g (60%) of 11 m as a yellow solid, mp 287°C-290°C (ethyl ether/ethyl acetate).")

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 006  DOI: 10.1002/ardp.70227
# Archiv der Pharmazie 2026, 359(3)
# ═══════════════════════════════════════════════════════════════════════════
s6 = 'Archiv der Pharmazie, 2026, 359(3)'
u6 = 'https://doi.org/10.1002/ardp.70227'

add('5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-amine','melting_point',
    mid(278,279),278,279,'278°C-279°C','=','measured',s6,u6,
    'Experimental, compound 7',
    "The solid residue was filtered and washed with EtOH to give the pure product 7 as a pale orange powder (4.21 g, 13.0 mmol, 73%). Orange solid, mp 278°C-279°C. IR (KBr)")

add('1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-phenylpiperidine-4-carboxamide','melting_point',
    mid(254,256),254,256,'254°C-256°C','=','measured',s6,u6,
    'Experimental, compound 8',
    "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]- N -phenylpiperidine-4-carboxamide ( 8 ): Yellow solid, mp 254°C-256°C. IR (KBr)")

add('N-Benzyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide','melting_point',
    mid(271,273),271,273,'271°C-273°C','=','measured',s6,u6,
    'Experimental, compound 9',
    "N -Benzyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide ( 9 ): Orange solid, mp 271°C-273°C. IR (KBr)")

add('1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-phenethylpiperidine-4-carboxamide','melting_point',
    mid(289,293),289,293,'289°C-293°C','=','measured',s6,u6,
    'Experimental, compound 10',
    "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]- N -phenethylpiperidine-4-carboxamide ( 10 ): Orange solid, mp 289°C-293°C. IR (KBr)")

add('1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]-N-(3-phenylpropyl)piperidine-4-carboxamide','melting_point',
    mid(305,308),305,308,'305°C-308°C','=','measured',s6,u6,
    'Experimental, compound 11',
    "1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]- N -(3-phenylpropyl)piperidine-4-carboxamide ( 11 ): Orange solid, mp 305°C-308°C. IR (KBr)")

add('{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(pyrrolidin-1-yl)methanone','melting_point',
    mid(243,245),243,245,'243°C-245°C','=','measured',s6,u6,
    'Experimental, compound 12',
    "{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(pyrrolidin-1-yl)methanone ( 12 ): Orange solid, mp 243°C-245°C. IR (KBr)")

add('{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(piperidin-1-yl)methanone','melting_point',
    mid(252,254),252,254,'252°C-254°C','=','measured',s6,u6,
    'Experimental, compound 13',
    "{1-[5-(5-Nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}(piperidin-1-yl)methanone ( 13 ): Orange solid, mp 252°C-254°C. IR (KBr)")

add('(4-Methylpiperidin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone','melting_point',
    mid(268,270),268,270,'268°C-270°C','=','measured',s6,u6,
    'Experimental, compound 14',
    "(4-Methylpiperidin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone ( 14 ): Orange solid, mp 268°C-270°C. IR (KBr)")

add("[1,4'-Bipiperidin]-1'-yl{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone",'melting_point',
    mid(288,291),288,291,'288°C-291°C','=','measured',s6,u6,
    'Experimental, compound 15',
    "[1,4'-Bipiperidin]-1'-yl{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone ( 15 ): Yellow solid, mp 288°C-291°C. IR (KBr)")

add('Morpholino{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone','melting_point',
    mid(269,271),269,271,'269°C-271°C','=','measured',s6,u6,
    'Experimental, compound 16',
    "Morpholino{1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone ( 16 ): Yellow solid, mp 269°C-271°C. IR (KBr)")

add('(4-Methylpiperazin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone','melting_point',
    mid(276,279),276,279,'276°C-279°C','=','measured',s6,u6,
    'Experimental, compound 17',
    "(4-Methylpiperazin-1-yl){1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidin-4-yl}methanone ( 17 ): Orange solid, mp 276°C-279°C. IR (KBr)")

add('N-Cyclohexyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide','melting_point',
    mid(248,252),248,252,'248°C-252°C','=','measured',s6,u6,
    'Experimental, compound 18',
    "N -Cyclohexyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide ( 18 ): Orange solid, mp 248°C-252°C. IR (KBr)")

add('N-Ethyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide','melting_point',
    mid(217,220),217,220,'217°C-220°C','=','measured',s6,u6,
    'Experimental, compound 19',
    "N -Ethyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide ( 19 ): Orange solid, mp 217°C-220°C. IR (KBr)")

add('N-Isopropyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide','melting_point',
    mid(228,230),228,230,'228°C-230°C','=','measured',s6,u6,
    'Experimental, compound 20',
    "N -Isopropyl-1-[5-(5-nitrofuran-2-yl)-1,3,4-thiadiazol-2-yl]piperidine-4-carboxamide ( 20 ): Orange solid, mp 228°C-230°C. IR (KBr)")

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 012  DOI: 10.1002/cmdc.202500922
# ChemMedChem 2025 (online)
# ═══════════════════════════════════════════════════════════════════════════
s12 = 'ChemMedChem, 2025 (online)'
u12 = 'https://doi.org/10.1002/cmdc.202500922'

add('N-(1-Benzylpiperidin-4-yl)-N-Methyl-4-Phenylbutanamide','melting_point',
    mid(169,171),169,171,'169°C-171°C','=','measured',s12,u12,
    'Experimental section 4.2.1.1, compound 2a',
    "N-(1-Benzylpiperidin-4-yl)-N-Methyl-4-Phenylbutanamide (2a) White solid (458 mg, yield 88%): mp 169°C-171°C; 1 H NMR (hydrochloride salt,")

add('N-(1-Benzylpiperidin-4-yl)-N-Methyl-2-Propylpentanamide','melting_point',
    mid(170,173),170,173,'170°C-173°C','=','measured',s12,u12,
    'Experimental section 4.2.1.2, compound 2b',
    "N-(1-Benzylpiperidin-4-yl)-N-Methyl-2-Propylpentanamide (2b) White solid (375 mg, yield 75%): mp 170°C-173°C; 1 H NMR (500 MHz, CDCl 3 ):")

add('N-(1-Benzylpiperidin-4-yl)-4-Phenylbutanamide Hydrochloride','melting_point',
    mid(162,164),162,164,'162°C-164°C','=','measured',s12,u12,
    'Experimental section 4.2.1.3, compound 2c',
    "N-(1-Benzylpiperidin-4-yl)-4-Phenylbutanamide Hydrochloride (2c) White solid (425 mg, yield 80%): mp 162°C-164°C; 1 H NMR (400 MHz, DMSO- d 6")

add('N-(1-Benzylpiperidin-4-yl)-2-Propylpentanamide Hydrochloride','melting_point',
    mid(164,165),164,165,'164°C-165°C','=','measured',s12,u12,
    'Experimental section 4.2.1.4, compound 2d',
    "N-(1-Benzylpiperidin-4-yl)-2-Propylpentanamide Hydrochloride (2d) White solid (349 mg, yield 70%): mp 164°C-165°C; 1 H NMR (400 MHz, DMSO- d 6")

add('1-Benzylpiperidin-4-yl 4-Phenylbutanoate Hydrochloride','melting_point',
    mid(141,143),141,143,'141°C-143°C','=','measured',s12,u12,
    'Experimental section 4.2.1.5, compound 3a',
    "1-Benzylpiperidin-4-yl 4-Phenylbutanoate Hydrochloride (3a) White solid (450 mg, yield 85%): mp 141°C-143°C; 1 H NMR (400 MHz, DMSO- d 6")

add('1-Benzylpiperidin-4-yl 2-Propylpentanoate Hydrochloride','melting_point',
    mid(143,145),143,145,'143°C-145°C','=','measured',s12,u12,
    'Experimental section 4.2.1.6, compound 3b',
    "1-Benzylpiperidin-4-yl 2-Propylpentanoate Hydrochloride (3b) White solid (363 mg, yield 73%): mp 143°C-145°C; 1 H NMR (400 MHz, DMSO- d 6")

add('1-(4-Benzylpiperazin-1-yl)-4-Phenylbutan-1-One','melting_point',
    mid(166,168),166,168,'166°C-168°C','=','measured',s12,u12,
    'Experimental section 4.2.1.7, compound 4a',
    "1-(4-Benzylpiperazin-1-yl)-4-Phenylbutan-1-One (4a) White solid (443 mg, yield 81%). mp 166°C-168°C; 1 H NMR (500 MHz, CDCl 3 ):")

add('1-(4-Benzylpiperazin-1-yl)-2-Propylpentan-1-One','melting_point',
    mid(165,167),165,167,'165°C-167°C','=','measured',s12,u12,
    'Experimental section 4.2.1.8, compound 4b',
    "1-(4-Benzylpiperazin-1-yl)-2-Propylpentan-1-One (4b) White solid (356 mg, yield 69%). mp 165°C-167°C; 1 H NMR (500 MHz, CDCl 3 ):")

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 020  DOI: 10.3390/molecules29122942
# Molecules 2024, 29, 2942
# ═══════════════════════════════════════════════════════════════════════════
s20 = 'Molecules, 2024, 29, 2942'
u20 = 'https://doi.org/10.3390/molecules29122942'

add('5-Acetyl-1,6-dihydroxy-4-methylpyridin-2(1H)-one','melting_point',
    mid(178,179),178,179,'178-179 °C','=','measured',s20,u20,
    'Experimental, compound B',
    "the N -hydroxypyridinedione B almost quantitatively (1.32 g, 98%); m.p. 178-179 °C (MeOH/ n -pentane, dry Et 2 O")

add('2-(4-(Methylthio)benzyloxy)isoindolin-1,3-dione','melting_point',
    147,147,'','147 °C','=','measured',s20,u20,
    'Experimental, compound 1',
    "The compound 2-(4-(Methylthio)benzyl-oxy)isoindolin-1,3-dione ( 1 ) was synthesized from (4-(bromomethyl)phenyl)(methyl)sulfane according to the general procedure. White solid (697.7 mg, 95%). R f = 0.54 (CH 2 Cl 2 ), m.p. 147 °C,")

add('Methyl 4-[1-(1,3-dioxoisoindole-2-yl-oxy)ethyl]benzoate','melting_point',
    mid(170,171),170,171,'170-171 °C','=','measured',s20,u20,
    'Experimental, compound 2',
    "The compound Methyl 4-[1-(1,3-dioxoisoindole-2-yl-oxy)ethyl] benzoate ( 2 ) was synthesized from methyl 4-(1-bromoethyl)benzoate (1.5 equiv.) according to the general procedure. White solid (136.7 mg, 74%). R f = 0.35 (CH 2 Cl 2 ), m.p. 170-171 °C,")

add('2-(Allyloxy)isoindoline-1,3-dione','melting_point',
    mid(120,121),120,121,'120-121 °C','=','measured',s20,u20,
    'Experimental, compound 3',
    "The resulting crude mixture is purified by recrystallization (EtOH). White foamy solid (214.6 mg, 62%). R f = 0.5 (AcOEt), m.p. 120-121 °C.")

add('Methyl 3,5-dichloro-4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)benzoate','melting_point',
    mid(145,147),145,147,'145-147 °C','=','measured',s20,u20,
    'Experimental, compound 4',
    "The compound Methyl 3,5-dichloro-4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)benzoate ( 4 ) was synthesized from methyl 4-(bromomethyl)-3,5-dichlorobenzoate (300.0 mg, 1.01 mmol) according to the general procedure. Pink solid (226.9 mg, 89%). R f = 0.67 (CH 2 Cl 2 ), m.p. 145-147 °C.")

add('2-(Pentyloxy)isoindoline-1,3-dione','melting_point',
    mid(80,82),80,82,'80-82 °C','=','measured',s20,u20,
    'Experimental, compound 6',
    "yloxy)isoindoline-1,3-dione ( 6 ) was synthesized from pentil-1-ol (1 equiv.) according to the procedure followed for the compound 3 (48 h). The crude yellow solid was purified with column chromatography (7:3 HexaneL AcOEt) and recrystallized from EtOH. White solid (528 mg, 64%). R f = 0.5 (AcOEt), m.p. 80-82 °C,")

add('2-(But-3-yn-1-yloxy)isoindoline-1,3-dione','melting_point',
    104,104,'','104 °C','=','measured',s20,u20,
    'Experimental, compound 7',
    "1-yloxy)isoindoline-1,3-dione ( 7 ) was synthesized from butin-1-ol (1 equiv.) according to the procedure followed for compound 3 (48 h). The compound underwent purification by column chromatography (7: 3 Hexane: AcOEt) and recrystallization from EtOH. White solid (473 mg, 60%). R f = 0.45 (AcOEt), m.p. 104 °C.")

add('2-(Prop-2-yn-1-yloxy)isoindoline-1,3-dione','melting_point',
    mid(149,150),149,150,'149-150 °C','=','measured',s20,u20,
    'Experimental, compound 8',
    ")isoindoline-1,3-dione ( 8 ) was synthesized from propin-1-ol (1 equiv.) according to the procedure followed for the compound 3 (48 h). The compound underwent purification by column chromatography (7: 3 Hexane: AcOEt) and recrystallization from EtOH. White solid (389.1 mg, 53%). R f = 0.33 (AcOEt), m.p. 149-150 °C.")

add("Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-6'-chlorobenzoate",'melting_point',
    mid(165,168),165,168,'165-168 °C','=','measured',s20,u20,
    'Experimental, compound 9',
    "The compound Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-6'-chlorobenzoate ( 9 ) was synthesized from methyl 4-(bromomethyl)-3-chlorobenzoate (1 equiv.), according to the general procedure. White solid (150.5 mg, 86%). R f = 0.53 (CH 2 Cl 2 ), m.p. 165-168 °C.")

add("Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-6'-cyanobenzoate",'melting_point',
    mid(165,168),165,168,'165-168 °C','=','measured',s20,u20,
    'Experimental, compound 10',
    "The compound Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-6'-cyanobenzoate ( 10 ) was synthesized from methyl 4-(bromomethyl)-3-cyanobenzoate (1equiv.) according to the general procedure. White solid (102.7 mg, 89.5%). R f = 0.53 (CH 2 Cl 2 ), m.p. 165-168 °C.")

add('Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-3-fluorobenzoate','melting_point',
    mid(165,168),165,168,'165-168 °C','=','measured',s20,u20,
    'Experimental, compound 11',
    "The compound Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)-3-fluorobenzoate ( 11 ) was synthesized from methyl 4-(bromomethyl)-3-fluorobenzoate (1 equiv.) according to the general procedure. White solid (139.8 mg, 79%). R f = 0.12 (CH 2 Cl 2 ), m.p. 165-168 °C.")

add('Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)benzoate','melting_point',
    mid(155,158),155,158,'155-158 °C','=','measured',s20,u20,
    'Experimental, compound 13',
    "The compound Methyl 4-(((1,3-dioxoisoindolin-2-yl)oxy)methyl)benzoate ( 13 ) was synthesized from methyl 4-(bromomethyl)benzoate (1equiv.) according to the general procedure. Pink solid (758.3 mg, 99%). R f = 0.53 (CH 2 Cl 2 ), m.p. 155-158 °C.")

add('1,6-Dihydroxy-4-methyl-5-(1-(((4-(methylthio)benzyl)oxy)imino)ethyl)pyridin-2(1H)-one','decomposition',
    mid(110,115),110,115,'110-115 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 33',
    "The compound 1,6-Dihydroxy-4-methyl-5-(1-(((4(methylthio)benzyl)oxy)imino)ethyl)pyridin-2(1H)-one ( 33 ) was synthesized from the compound 15 (1.05 equiv.) according to the general procedure. Green solid (100.7 mg, 61%). R f = 0.25 (AcOEt), m.p. 110-115 °C (dec.).")

add('Methyl-4-(1-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)benzoate','decomposition',
    130,130,'','130 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 34',
    "The compound Methyl-4-(1-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)benzoate ( 34 ) was synthesized from the compound 16 (1.05 equiv.) according to the general procedure. Green solid (92.7 mg, 80%). R f = 0.10 (AcOEt), m.p. 130 °C (dec.).")

add('1,6-Dihydroxy-5-(1-(((3-methoxybenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one','decomposition',
    mid(120,122),120,122,'120-122 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 35',
    "The compound 1,6-Dihydroxy-5-(1-(((3-methoxybenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one ( 35 ) was synthesized from the compound 17 (1.05 equiv.) according to the general procedure. Green solid (96.9 mg, 54%). R f = 0.20 (AcOEt), m.p. 120-122 °C (dec.).")

add('Methyl 3,5-dichloro-4-((((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)methyl)benzoate','decomposition',
    mid(117,119),117,119,'117-119 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 36',
    "The compound Methyl 3,5-dichloro-4-((((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)methyl)benzoate ( 36 ) was synthesized from the compound 18 (46.8 mg, 0.19 mmol) according to the general procedure. Yellow solid (62.5 mg, 89%). R f = 0.09 (EtOAc/MeOH 3:1), m.p. 117-119 °C (dec.).")

add('N-(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)furan-2-carboxamide','decomposition',
    mid(118,120),118,120,'118-120 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 37',
    "N -(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)furan-2-carboxamide (37) was synthesized from the compound 29 (1.05 equiv.) according to the general procedure. Blue solid (19 mg, 44%). R f = 0.25 (AcOEt), m.p. 118-120 °C (dec.).")

add('5-(1-(((3,5-Difluorophenyl)(pyridin-2-yl)methoxy)imino)ethyl)-1,6-dihydroxy-4-methylpyridin-2(1H)-one','decomposition',
    mid(102,104),102,104,'102-104 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 38',
    "The compound 5-(1-(((3,5-Difluorophenyl)(pyridin-2-yl)methoxy)imino)ethyl)-1,6-dihydroxy-4-methylpyridin-2(1H)-one ( 38 ) was synthesized from the compound 32 (1.05 equiv.) according to the general procedure. Green solid (46 mg, 44%). R f = 0.25 (AcOEt), m.p. 102-104 °C (dec.).")

add('1,6-Dihydroxy-5-(1-(((4-hydroxybenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one','decomposition',
    mid(98,100),98,100,'98-100 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 39',
    "The compound 1,6-Dihydroxy-5-(1-(((4-hydroxybenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one ( 39 ) was synthesized from the compound 19 (1.05 equiv.) according to the general procedure. Hydroscopic red solid (119.9 mg, 97%). R f = 0.25 (AcOEt), m.p. 98-100 °C (dec.).")

add('5-(1-((But-3-yn-1-yloxy)imino)ethyl)-1,6-dihydroxy-4-methylpyridin-2(1H)-one','decomposition',
    mid(86,89),86,89,'86-89 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 41',
    "The compound 5-(1-((But-3-yn-1-yloxy)imino)ethyl)-1,6-dihydroxy-4-methylpyridin-2(1H)-one ( 41 ) was synthesized from the compound 21 (1.05 equiv.) according to the general procedure. Green solid (27 mg, 24%). R f = 0.30 (1:1 AcOEt:MeOH), m.p. 86-89 °C (dec.).")

add('1,6-Dihydroxy-4-methyl-5-(1-((prop-2-yn-1-yloxy)imino)ethyl)pyridin-2(1H)-one','decomposition',
    mid(78,80),78,80,'78-80 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 42',
    "The compound 1,6-Dihydroxy-4-methyl-5-(1-((prop-2-yn-1-yloxy)imino)ethyl)pyridin-2(1H)-one ( 42 ) was synthesized from the compound 22 (1.05 equiv.) according to the general procedure. Green solid (32.3 mg, 54%). R f = 0.30 (1:1 AcOEt:MeOH), m.p. 78-80 °C (dec.).")

add("2'-Chloro-4'-((((1'-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate",'decomposition',
    155,155,'','155 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 43',
    "The compound 2'-Chloro-4'-((((1'-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate ( 43 ) was synthesized from the compound 23 (1.05 equiv.) according to the general procedure. Green solid (86.4mg, 50.8%). R f = 0.10 (AcOEt), m.p. 155 °C (dec.).")

add("2'-Cyano-4'-((((1'-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate",'melting_point',
    115,115,'','115 °C','=','measured',s20,u20,
    'Experimental, compound 44',
    "The compound 2'-Cyano-4'-((((1'-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate ( 44 ) was synthesized from the compound 24 (1.05 equiv.) according to the general procedure. Blue solid (45mg, 55.6%). R f = 0.10 (AcOEt), m.p. 115 °C.")

add('Methyl 4-((((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)methyl)-3-fluorobenzoate','decomposition',
    130,130,'','130 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 45',
    "The compound Methyl 4-((((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)methyl)-3-fluorobenzoate ( 45 ) was synthesized from the compound 25 (1.05 equiv.) according to the general procedure. Green solid (131.3 mg, 46%). R f = 0.05 (AcOEt), m.p. 130 °C (dec.).")

add('1,6-Dihydroxy-4-methyl-5-(1-((1-phenylethoxy)imino)ethyl)pyridin-2(1H)-one','melting_point',
    mid(130,132),130,132,'130-132 °C','=','measured',s20,u20,
    'Experimental, compound 46',
    "The compound 1,6-Dihydroxy-4-methyl-5-(1-((1-phenylethoxy)imino)ethyl)pyridin-2(1 H )-one ( 46 ) was synthesized from the compound 26 (100.0 mg, 0.73 mmol) according to the general procedure. Beige solid (135.0 mg, 67%). R f = 0.08 (EtOAc/MeOH 3:1), m.p. 130-132 °C.")

add("4'-((((1'-(1,2-Dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate",'decomposition',
    120,120,'','120 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 47',
    "The compound 4'-((((1'-Dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-5-yl)ethylidene)amino)oxy)methyl)methyl benzoate ( 47 ) was synthesized from the compound 27 (1.05 equiv.) according to the general procedure. Green solid (86.4 mg, 50.8%). R f = 0.10 (AcOEt), m.p. 120 °C (dec.).")

add('1,6-Dihydroxy-5-(1-(((4-fluorobenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one','melting_point',
    mid(105,107),105,107,'105-107 °C','=','measured',s20,u20,
    'Experimental, compound 48',
    "obenzyl)oxy)imino)ethyl)pyridin-2(1H)-one ( 48 ) was synthesized from the compound 28 (110.0 mg, 0.65 mmol) according to the general procedure. The brownish residual solid was also triturated with n -pentane to afford the title compound as a brown solid (212.4 mg, 97%). R f = 0.05 (EtOAc/MeOH 3:1), m.p. 105-107 °C.")

add('N-(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)quinoline-2-carboxamide','decomposition',
    mid(108,110),108,110,'108-110 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 49',
    "-(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)quinoline-2-carboxamide ( 49 ) was synthesized from the hydroxylamine 30 (60.0 mg, 0.17 mmol) according to the general procedure. Beige solid (36.4 mg, 41%). R f = 0.11 (EtOAc/MeOH 3:1), m.p. 108-110 °C (dec.).")

add('N-(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)thiazole-2-carboxamide','decomposition',
    mid(117,119),117,119,'117-119 °C (dec.)','=','measured',s20,u20,
    'Experimental, compound 50',
    "-(2-(3,5-Difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)thiazole-2-carboxamide ( 50 ) was synthesized from the hydroxylamine 31 (132.0 mg, 0.44 mmol) according to the general procedure. Green solid (69.3 mg, 34%). R f = 0.11 (EtOAc/MeOH 3:1), m.p. 117-119 °C (dec.).")

add('2,6-Diamino-4-(2\',4\',5\'-trichloro)-1,6-dihydropyrimidine 1-oxide','melting_point',
    135,135,'','135 °C','=','measured',s20,u20,
    'Experimental, compound 56',
    "The compound 2,6-Diamino-4-(2',4',5'-trichloro)-1,6-dihydropyrimidine 1-oxide ( 56 ) was synthesized from the compound 52 (1 equiv.) according to the general procedure with a reaction time of 16 h. White solid (120.6 mg, 41%). R f = 0.25 (3:1 AcOEt: MeOH), m.p. 135 °C.")

add('2,6-Diamino-4-(2\',4\'-dichloro)-1,6-dihydropyrimidine 1-oxide','melting_point',
    160,160,'','160 °C','=','measured',s20,u20,
    'Experimental, compound 57',
    "The compound 2,6-Diamino-4-(2',4'-dichloro)-1,6-dihydropyrimidine 1-oxide ( 57 ) was synthesized from the compound 53 (1 equiv.) according to the general procedure with a reaction time of 16 h. White solid (169.5 mg, 45%). R f = 0.28 (3:1 AcOEt: MeOH), m.p. 160 °C.")

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 021  DOI: 10.3390/molecules28227590
# Molecules 2023, 28, 7590
# ═══════════════════════════════════════════════════════════════════════════
s21 = 'Molecules, 2023, 28, 7590'
u21 = 'https://doi.org/10.3390/molecules28227590'

add('(R)-Phenyl(6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)methanone','melting_point',
    186,186,'','186 °C','=','measured',s21,u21,
    'Experimental, compound 10a',
    "(R)-Phenyl(6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)methanone ( 10a ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 49% as an off-white solid. mp 186 °C.")

add('(R)-[1,1\'-biphenyl]-4-yl(4\'-(p-tolylsulfinyl)-[1,1\':3\':4\',1\'\'-quaterphenyl]-6\'-yl)methanone','melting_point',
    116,116,'','116 °C','=','measured',s21,u21,
    'Experimental, compound 10b',
    "(R)-[1,1'-biphenyl]-4-yl(4'-(p-tolylsulfinyl)-[1,1':3':4'',1'''-quaterphenyl]-6'-yl)methanone ( 10b ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 27% as an off-white solid. mp 116 °C.")

add('(R)-(4-methoxy-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(4-methoxyphenyl)methanone','melting_point',
    188,188,'','188 °C','=','measured',s21,u21,
    'Experimental, compound 10c',
    "(R)-(4-methoxy-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(4-methoxyphenyl)methanone ( 10c ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 26% as a yellow solid. mp 188 °C.")

add('(R)-(6\'-(p-tolylsulfinyl)-4-(trifluoromethyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(4-(trifluoromethyl)phenyl)methanone','melting_point',
    91,91,'','91 °C','=','measured',s21,u21,
    'Experimental, compound 10d',
    "(R)-(6'-(p-tolylsulfinyl)-4-(trifluoromethyl)-[1,1':3',1''-terphenyl]-4'-yl)(4-(trifluoromethyl)phenyl)methanone ( 10d ) prepared from 300 mg (1.95 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 41% as an off-white solid. mp 91 °C.")

add('(R)-(4\'\'-fluoro-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    164,164,'','164 °C','=','measured',s21,u21,
    'Experimental, compound 10e',
    "(R)-(4''-fluoro-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10e ) prepared from 600 mg (3.98 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 41% as an off-white solid. mp 164 °C.")

add('(R)-(4\'\'-bromo-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    167,167,'','167 °C','=','measured',s21,u21,
    'Experimental, compound 10f',
    "(R)-(4''-bromo-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10f ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 46% as a white solid. mp 167 °C.")

add('(R)-(4-fluoro-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(4-fluorophenyl)methanone','melting_point',
    190,190,'','190 °C','=','measured',s21,u21,
    'Experimental, compound 10g',
    "(R)-(4-fluoro-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(4-fluorophenyl)methanone ( 10g ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 36% as an off-white solid. mp 190 °C.")

add('(R)-(4-bromo-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(4-bromophenyl)methanone','melting_point',
    235,235,'','235 °C','=','measured',s21,u21,
    'Experimental, compound 10h',
    "(R)-(4-bromo-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(4-bromophenyl)methanone ( 10h ) prepared from 600 mg (3.89 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 46% as an off-white solid. mp 235 °C.")

add('(R)-(4-iodo-6\'-(p-tolylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(4-iodophenyl)methanone','melting_point',
    234,234,'','234 °C','=','measured',s21,u21,
    'Experimental, compound 10i',
    "(R)-(4-iodo-6'-(p-tolylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(4-iodophenyl)methanone ( 10i ) prepared from 300 mg (1.95 mmol) ( R )- p -tolyl methyl sulfoxide (( R )- 7a ). Yield: 43% as an off-white solid. mp 234 °C.")

add('Phenyl(6\'-(phenylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)methanone','melting_point',
    140,140,'','140 °C','=','measured',s21,u21,
    'Experimental, compound 10j',
    "Phenyl(6'-(phenylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)methanone ( 10j ) prepared from 309 mg (2.20 mmol) methylphenylsulfoxide. Yield: 39% as an off-white solid. mp 140 °C.")

add('(6\'-((4-methoxyphenyl)sulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    94,94,'','94 °C','=','measured',s21,u21,
    'Experimental, compound 10k',
    "(6'-((4-methoxyphenyl)sulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10k ) prepared from 355 mg (2.09 mmol) 4-methoxyphenylmethylsulfoxide. Yield: 42% as an off-white solid. mp 94 °C.")

add('(6\'-((4-bromophenyl)sulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    92,92,'','92 °C','=','measured',s21,u21,
    'Experimental, compound 10l',
    "(6'-((4-bromophenyl)sulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10l ) prepared from 438 mg (2.00 mmol) 4-bromophenylmethylsulfoxid. Yield: 43% as a white solid. mp 92 °C.")

add('(6\'-((4-chlorophenyl)sulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    122,122,'','122 °C','=','measured',s21,u21,
    'Experimental, compound 10m',
    "(6'-((4-chlorophenyl)sulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10m ) prepared from 350 mg (2.00 mmol) 4-chlorophenylmethylsulfoxid. Yield: 40 % as a white solid. mp 122 °C.")

add('Phenyl(6\'-(pyridin-2-ylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)methanone','melting_point',
    110,110,'','110 °C','=','measured',s21,u21,
    'Experimental, compound 10n',
    "Phenyl(6'-(pyridin-2-ylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)methanone ( 10n ) prepared from 300 mg (2.12 mmol) 2-pyridylmethylsulfoxid. Yield: 36% as a white solid. mp 110 °C.")

add('(6\'-(cyclohexylsulfinyl)-[1,1\':3\',1\'\'-terphenyl]-4\'-yl)(phenyl)methanone','melting_point',
    160,160,'','160 °C','=','measured',s21,u21,
    'Experimental, compound 10o',
    "(6'-(cyclohexylsulfinyl)-[1,1':3',1''-terphenyl]-4'-yl)(phenyl)methanone ( 10o ) prepared from 304 mg (2.08 mmol) cyclohexylmethylsulfoxid. Yield: 46% as a white solid. mp 160 °C.")

# ═══════════════════════════════════════════════════════════════════════════
# PAPER 023  DOI: 10.1134/S107042802211001X
# Russian J. Organic Chemistry 2022, 58(11), 1561-1568
# ═══════════════════════════════════════════════════════════════════════════
s23 = 'Russian Journal of Organic Chemistry, 2022, 58(11), 1561-1568'
u23 = 'https://doi.org/10.1134/S107042802211001X'

add("1,1'-(Ethane-1,2-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    212.7,212.7,'','212.7°C','=','measured',s23,u23,
    'Experimental, compound 4a',
    "The product was purified by recrystallization from ethanol. Yield 0.219 g (98%), mp 212.7°C. 1 H NMR spectrum (DMSO- d 6")

add("1,1'-(Propane-1,3-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    163.5,163.5,'','163.5°C','=','measured',s23,u23,
    'Experimental, compound 4b',
    "1,1'-(Propane-1,3-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4b) was prepared similarly to compound 4a from 0.2 g of compound 2 and 0.034 g of 1,3-diaminopropane ( 3b ). Yield 0.232 g (99%), mp 163.5°C.")

add("1,1'-(Butane-1,4-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    143.5,143.5,'','143.5°C','=','measured',s23,u23,
    'Experimental, compound 4c',
    "1,1'-(Butane-1,4-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4c) was prepared similarly to compound 4a from 0.2 g of compound 2 and 0.04 g of 1,4-diaminobutane ( 3c ). Yield 0.153 g (63%), mp 143.5°C.")

add("1,1'-(Pentane-1,5-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    127.1,127.1,'','127.1°C','=','measured',s23,u23,
    'Experimental, compound 4d',
    "1,1'-(Pentane-1,5-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4d) was prepared similarly to compound 4a from 0.2 g compound 2 and 0.05 g of 1,5-diaminopentane ( 3d ). Yield 0.188 g (76%), mp 127.1°C.")

add("1,1'-(Hexane-1,6-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    128.9,128.9,'','128.9°C','=','measured',s23,u23,
    'Experimental, compound 4e',
    "1,1'-(Hexane-1,6-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4e) was prepared similarly to compound 4a from 0.2 g compound 2 and 0.055 g 1,6-diaminohexane ( 3e ). Yield 0.247 g (98%), mp 128.9°C.")

add("1,1'-(Heptane-1,7-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    120.4,120.4,'','120.4°C','=','measured',s23,u23,
    'Experimental, compound 4f',
    "1,1'-(Heptane-1,7-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4f) was prepared similarly to compound 4a from 0.2 g compound 2 and 0.06 g 1,7-diaminoheptane ( 3f ). Yield 0.184 g (71%), mp 120.4°C.")

add("1,1'-(Octane-1,8-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    109.9,109.9,'','109.9°C','=','measured',s23,u23,
    'Experimental, compound 4g',
    "1,1'-(Octane-1,8-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4g) was prepared similarly to compound 4a from 0.2 g of compound 2 and 0.066 g of 1,8-diaminooctane ( 3g ). Yield 0.210 g (79%), mp 109.9°C.")

add("1,1'-(Decane-1,10-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea}",'melting_point',
    99.6,99.6,'','99.6°C','=','measured',s23,u23,
    'Experimental, compound 4h',
    "1,1'-(Decane-1,10-diyl)bis{3-[(3,5-dimethyladamantan-1-yl)methyl]urea} (4h) was prepared similarly to compound 4a from 0.2 g compound 2 and 0.08 g of 1,10-diaminodecane ( 3h ). Yield 0.263 g (94%), mp 99.6°C.")

add("4-[(4-{3-[(3,5-Dimethyladamantan-1-yl)methyl]ureido}cyclohexyl)oxy]benzoic acid",'melting_point',
    240.1,240.1,'','240.1°C','=','measured',s23,u23,
    'Experimental, compound 4i',
    "4-[(4-{3-[(3,5-Dimethyladamantan-1-yl)methyl]ureido}cyclohexyl)oxy]benzoic acid (4i) was prepared similarly to compound 4a from 0.2 g compound 2 and 0.22 g of trans -4-(cyclohexyloxy)benzoic acid ( 3i ). Yield 0.260 g (63%), mp 240.1°C.")

# ═══════════════════════════════════════════════════════════════════════════
# Now load trial2 rows for the 14 papers that were already there
# DOIs to KEEP from trial2: all except 005, 006, 012 (fresh above)
# ═══════════════════════════════════════════════════════════════════════════
FRESH_URLS = {u5, u6, u12, u20, u21, u23}
# 020,021,023 are fresh above; 022 is NONE

import csv as csvmod
trial2_rows = []
with open('/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/trials/trial2/full-sonnet46/batch_aa.csv') as f:
    for r in csvmod.DictReader(f):
        if r['source_url'] not in FRESH_URLS:
            trial2_rows.append(r)

print(f"Fresh rows: {len(rows)}")
print(f"Trial2 rows kept: {len(trial2_rows)}")

# Write output
OUT = '/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_aa.csv'
with open(OUT, 'w', newline='') as f:
    w = csvmod.DictWriter(f, fieldnames=COLS, quoting=csvmod.QUOTE_ALL)
    w.writeheader()
    n = 1
    # First write trial2 rows
    for r in trial2_rows:
        r['id'] = n
        r['verification_status'] = 'pending_verification'
        w.writerow({c: r.get(c,'') for c in COLS})
        n += 1
    # Then write fresh rows
    for r in rows:
        r['id'] = n
        w.writerow({c: r.get(c,'') for c in COLS})
        n += 1

print(f"Total rows written: {n-1}")
print(f"Output: {OUT}")

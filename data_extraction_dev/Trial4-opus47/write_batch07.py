#!/usr/bin/env python3
"""Write batch_07.csv from LLM-extracted rows.
Each row is hand-extracted by reading the paper file directly.
"""
import csv

HEADER = [
    "id", "verification_status", "compound_name", "compound_smiles",
    "property", "value_celsius", "value_celsius_min", "value_celsius_max",
    "value_raw", "relation", "data_type", "source", "source_url",
    "evidence_location", "evidence_quote", "conversion_arithmetic", "notes",
]

ROWS = []


def add(compound, prop, vc, vmin, vmax, raw, rel, dt, source, url, loc, quote, conv="", notes="", smiles=""):
    ROWS.append({
        "compound_name": compound,
        "compound_smiles": smiles,
        "property": prop,
        "value_celsius": vc,
        "value_celsius_min": vmin if vmin is not None else "",
        "value_celsius_max": vmax if vmax is not None else "",
        "value_raw": raw,
        "relation": rel,
        "data_type": dt,
        "source": source,
        "source_url": url,
        "evidence_location": loc,
        "evidence_quote": quote,
        "conversion_arithmetic": conv,
        "notes": notes,
    })


# -----------------------------------------------------------------------------
# Paper 168 - Quality not Quantity: Marine Natural Products - PMC3756327
# -----------------------------------------------------------------------------
SRC_168 = "Mar Drugs. 2013 PMC3756327"
URL_168 = "pmc:PMC3756327"
add(
    compound="Sulfolane",
    prop="melting_point", vc=28.0, vmin=None, vmax=None, raw="28 °C", rel="=",
    dt="measured", source=SRC_168, url=URL_168,
    loc="Bromomethylation section, paragraph on sulfolane solvent",
    quote="Sulfolane is a polar aprotic solvent that is chemically and thermally stable, miscible with water and organic solvents, and does not damage PS. Therefore, it is an ideal solvent for performing many different reactions on the surface of PS plates, although its relatively high melting point (28 °C) introduces some difficulties in handling.",
)


# -----------------------------------------------------------------------------
# Paper 169 - Triazole-Incorporated Indole-Pyrazolone - PMC11843341
# -----------------------------------------------------------------------------
SRC_169 = "ACS Omega 2025 PMC11843341"
URL_169 = "pmc:PMC11843341"
P169 = [
    ("5a", "4-((1-((1-(2-Bromobenzyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "178–180 °C", 179.0, 178.0, 180.0),
    ("5b", "4-((1-((1-(2-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "180–200 °C", 190.0, 180.0, 200.0),
    ("5c", "4-((1-((1-(3-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "180–200 °C", 190.0, 180.0, 200.0),
    ("5d", "4-((1-((1-(4-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "178–180 °C", 179.0, 178.0, 180.0),
    ("5e", "5-Methyl-4-((1-((1-(2-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "240–242 °C", 241.0, 240.0, 242.0),
    ("5f", "5-Methyl-4-((1-((1-(3-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "210–212 °C", 211.0, 210.0, 212.0),
    ("5g", "5-Methyl-4-((1-((1-(4-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "150–152 °C", 151.0, 150.0, 152.0),
    ("5h", "5-Methyl-2-phenyl-4-((1-((1-(o-tolyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one", "220–222 °C", 221.0, 220.0, 222.0),
    ("5i", "4-((1-((1-(2-Methoxyphenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "230–232 °C", 231.0, 230.0, 232.0),
    ("5j", "4-((1-((1-(3,4-Dimethylphenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "208–210 °C", 209.0, 208.0, 210.0),
    ("5k", "4-((1-((1-Benzyl-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "210–212 °C", 211.0, 210.0, 212.0),
    ("5l", "4-((3-((3-Methyl-5-oxo-1-phenyl-1,5-dihydro-4H-pyrazol-4-ylidene)methyl)-1H-indol-1-yl)methyl)-1H-1,2,3-triazol-1-yl butyrate", "200–210 °C", 205.0, 200.0, 210.0),
    ("5m", "5-Methyl-2-phenyl-4-((1-((1-(2,4,5-trifluorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one", "200–202 °C", 201.0, 200.0, 202.0),
    ("5n", "5-Methyl-2-phenyl-4-((1-((1-(2,4,6-tribromophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one", "200–202 °C", 201.0, 200.0, 202.0),
    ("5o", "5-Methyl-4-((1-((1-(2-methyl-5-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one", "210–212 °C", 211.0, 210.0, 212.0),
]
P169_QUOTES = {
    "5a": "pyrazol-3-one ( 5a ) Yellow solid (0.390 g, 97%), mp: 178–180 °C",
    "5b": "pyrazol-3-one ( 5b ) Yellow solid (0.414 g, 95%), mp: 180–200 °C",
    "5c": "pyrazol-3-one ( 5c ) Yellow solid (0.410 g, 94%), mp: 180–200 °C",
    "5d": "pyrazol-3-one ( 5d ) Yellow solid (0.391 g, 90%), mp: 178–180 °C",
    "5e": "pyrazol-3-one ( 5e ) Yellow solid (0.392 g, 88%), mp: 240–242 °C",
    "5f": "pyrazol-3-one ( 5f ) Yellow solid (0.384 g, 86%), mp: 210–212 °C",
    "5g": "pyrazol-3-one ( 5g ) Yellow solid (0.401 g, 90%), mp: 150–152 °C",
    "5h": "pyrazol-3-one ( 5h ) Yellow solid (0.358 g, 83%), mp: 220–222 °C",
    "5i": "pyrazol-3-one ( 5i ) Yellow solid (0.375 g, 87%), mp: 230–232 °C",
    "5j": "pyrazol-3-one ( 5j ) Yellow solid (0.361 g, 84%), mp: 208–210 °C",
    "5k": "pyrazol-3-one ( 5k ) Yellow solid (0.379 g, 90%), mp: 210–212 °C",
    "5l": "1H-1,2,3-triazol-1-yl butyrate ( 5l ) Yellow solid (0.438 g, 93%), mp: 200–210 °C",
    "5m": "pyrazol-3-one ( 5m ) Yellow solid (0.380 g, 91%), mp: 200–202 °C",
    "5n": "pyrazol-3-one ( 5n ) Yellow solid (0.366 g, 89%), mp: 200–202 °C",
    "5o": "pyrazol-3-one ( 5o ) Yellow solid (0.405 g, 89%), mp: 210–212 °C",
}
for code, name, raw, vc, vmin, vmax in P169:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_169, URL_169,
        f"Experimental section, compound ({code})", P169_QUOTES[code])


# -----------------------------------------------------------------------------
# Paper 170 - Mycophenolic Acid Analogues - PMC11843339 - DOI 10.1021/acsbiomedchemau.4c00079
# -----------------------------------------------------------------------------
SRC_170 = "ACS Bio Med Chem Au 2025 PMC11843339"
URL_170 = "https://doi.org/10.1021/acsbiomedchemau.4c00079"
P170 = [
    ("2a", "tert-Butyldimethylsilyl (E)-6-(4-((tert-Butyldimethylsilyl)oxy)-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "76.6–80.6 °C", 78.6, 76.6, 80.6, "2a: A white solid in 66% yield; Mp: 76.6–80.6 °C"),
    ("2c", "Triisopropylsilyl (E)-6-(6-Methoxy-7-methyl-3-oxo-4-((triisopropylsilyl)oxy)-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "54–58 °C", 56.0, 54.0, 58.0, "2c: A white solid in 59% yield; Mp: 54–58 °C"),
    ("2d", "Triphenylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "114–120 °C", 117.0, 114.0, 120.0, "2d: A white solid in 48% yield; Mp: 114–120 °C"),
    ("2e", "Trityl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "92–98 °C", 95.0, 92.0, 98.0, "2e: A white solid in 30% yield; Mp: 92–98 °C"),
    ("3a", "(E)-6-(4-((tert-Butyldimethylsilyl)oxy)-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoic acid", "122–124 °C", 123.0, 122.0, 124.0, "3a: A white solid in 39% yield; Mp: 122–124 °C"),
    ("3c", "(E)-6-(6-Methoxy-7-methyl-3-oxo-4-((triisopropylsilyl)oxy)-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoic acid", "110–114 °C", 112.0, 110.0, 114.0, "3c: A yellow solid in 55% yield; Mp: 110–114 °C"),
    ("4b", "tert-Butyldiphenylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "64–68 °C", 66.0, 64.0, 68.0, "4b: A white solid in 64% yield; Mp: 64–68 °C"),
    ("4c", "Triisopropylsilyl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "48–50 °C", 49.0, 48.0, 50.0, "4c: A white solid in 55% yield; Mp: 48–50 °C"),
    ("6a", "1,3-Dioxoisoindolin-2-yl (E)-6-(4-Hydroxy-6-methoxy-7-methyl-3-oxo-1,3-dihydroisobenzofuran-5-yl)-4-methylhex-4-enoate", "108–110 °C", 109.0, 108.0, 110.0, "6a : A yellow solid in 32% yield; Mp: 108–110 °C"),
]
for code, name, raw, vc, vmin, vmax, quote in P170:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_170, URL_170,
        f"Experimental section, compound {code}", quote)


# -----------------------------------------------------------------------------
# Paper 171 - 1,2-Dihydroisoquinolines by Pd-Catalyzed - PMC11206658
# -----------------------------------------------------------------------------
SRC_171 = "Molecules 2024 PMC11206658"
URL_171 = "pmc:PMC11206658"
P171 = [
    ("2e", "N-(2-Bromobenzyl)-N-(3-(4-methoxyphenyl)-1-phenylpropa-1,2-dien-1-yl)acetamide", "123.5–157.2 °C", 140.35, 123.5, 157.2,
     "3.12. N-(2-Bromobenzyl)-N-(3-(4-methoxyphenyl)-1-phenylpropa-1,2-dien-1-yl)acetamide ( 2e ) Yield 84% (275 mg, 0.613 mmol); white solid; mp 123.5–157.2 °C (CHCl 3 )"),
    ("4af", "1-(4-((4-Chlorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one", "205.5–233.9 °C", 219.7, 205.5, 233.9,
     "3.19. 1-(4-((4-Chlorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one ( 4af ) Yield 96% (62.0 mg, 0.138 mmol); white solid; mp 205.5–233.9 °C (CHCl 3 )"),
    ("4ag/4da", "1-(4-((4-Fluorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one", "154.9–200.0 °C", 177.45, 154.9, 200.0,
     "3.20. 1-(4-((4-Fluorophenyl)(phenyl)methyl)-3-phenylisoquinolin-2(1H)-yl)ethan-1-one ( 4ag / 4da ) Yield 81% (50.8 mg, 0.117 mmol) from 2a with 3g , and yield 66% (46.2 mg, 0.107 mmol) from 2d with 3a ; white solid; mp 154.9–200.0 °C (CHCl 3 )"),
    ("4ah", "1-(4-((2-Acetyl-3-phenyl-1,2-dihydroisoquinolin-4-yl)(phenyl)methyl)phenyl)ethan-1-one", "205.9–220.7 °C", 213.3, 205.9, 220.7,
     "3.21. 1-(4-((2-Acetyl-3-phenyl-1,2-dihydroisoquinolin-4-yl)(phenyl)methyl)phenyl)ethan-1-one ( 4ah ) Yield 85% (55.5 mg, 0.121 mmol); white solid; mp 205.9–220.7 °C (CHCl 3 )"),
    ("4ba", "1-(4-Benzhydryl-3-(4-fluorophenyl)isoquinolin-2(1H)-yl)ethan-1-one", "211.4–229.1 °C", 220.25, 211.4, 229.1,
     "3.23. 1-(4-Benzhydryl-3-(4-fluorophenyl)isoquinolin-2(1H)-yl)ethan-1-one ( 4ba ) Yield 55% (42.2 mg, 0.0973 mmol); white solid; mp 211.4–229.1 °C (CHCl 3 )"),
    ("4ca", "1-(4-Benzhydryl-3-(benzo[d][1,3]dioxol-5-yl)isoquinolin-2(1H)-yl)ethan-1-one", "183.1–250.2 °C", 216.65, 183.1, 250.2,
     "3.24. 1-(4-Benzhydryl-3-(benzo[d][1,3]dioxol-5-yl)isoquinolin-2(1H)-yl)ethan-1-one ( 4ca ) Yield 80% (67.1 mg, 0.146 mmol); white solid; mp 183.1–250.2 °C (CHCl 3 )"),
]
for code, name, raw, vc, vmin, vmax, quote in P171:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_171, URL_171,
        f"Experimental section, compound {code}", quote,
        notes="wide mp range as printed")


# -----------------------------------------------------------------------------
# Paper 172 - Ieodomycins - PMC11209911
# -----------------------------------------------------------------------------
SRC_172 = "Molecules 2024 PMC11209911"
URL_172 = "pmc:PMC11209911"
P172 = [
    ("26a", "(2S,4R,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate", "104–106 °C", 105.0, 104.0, 106.0,
     "[α] D 25 = +4.00 (CHCl 3 , c = 0.5); mp: 104–106 °C"),
    ("26b", "(2R,4R,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate", "104–106 °C", 105.0, 104.0, 106.0,
     "[α] D 25 = +0.67 (CHCl 3 , c = 0.5); mp: 104–106 °C"),
    ("26c", "(2S,4S,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate", "104–106 °C", 105.0, 104.0, 106.0,
     "[α] D 25 = −3.00 (CHCl 3 , c = 0.5); mp: 104–106 °C"),
    ("26d", "(2R,4S,E)-2,4-Dihydroxy-8-iodo-7-methyloct-7-en-1-yl 2,4,6-triisopropylbenzenesulfonate", "104–106 °C", 105.0, 104.0, 106.0,
     "[α] D 25 = −2.00 (CHCl 3 , c = 0.5); mp: 104–106 °C"),
    ("26a-1", "((4S,6R)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate", "55–57 °C", 56.0, 55.0, 57.0,
     "[α] D 25 = +0.55 (MeOH, c = 1.0); mp: 55–57 °C"),
    ("26b-1", "((4R,6R)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate", "55–57 °C", 56.0, 55.0, 57.0,
     "[α] D 25 = +2.00 (MeOH, c = 0.5); mp: 55–57 °C"),
    ("26c-1", "((4S,6S)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate", "55–57 °C", 56.0, 55.0, 57.0,
     "[α] D 25 = −5.44 (MeOH, c = 0.5); mp: 55–57 °C"),
    ("26d-1", "((4R,6S)-6-((E)-4-Iodo-3-methylbut-3-en-1-yl)-2,2-dimethyl-1,3-dioxan-4-yl)methyl 2,4,6-triisopropylbenzenesulfonate", "55–57 °C", 56.0, 55.0, 57.0,
     "[α] D 25 = −0.87 (MeOH, c = 1.0); mp: 55–57 °C"),
]
for code, name, raw, vc, vmin, vmax, quote in P172:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_172, URL_172,
        f"Experimental section, compound {code}", quote)


# -----------------------------------------------------------------------------
# Paper 173 - Capture of mechanically interlocked molecules - PMC10914095
# DOI 10.1039/d4ra00566j (from title metadata)
# -----------------------------------------------------------------------------
SRC_173 = "RSC Adv. 2024 PMC10914095"
URL_173 = "https://doi.org/10.1039/d4ra00566j"
P173 = [
    ("HC≡C(CH2)6C(4-tBuC6H4)3",
     "Yield: 220 mg (422 μmol, 84%; mp. 142–143 °C)",
     142.5, 142.0, 143.0, "142–143 °C",
     "Preparation of HC C(CH 2 ) 6 C(4- t BuC 6 H 4 ) 3"),
    ("HC≡C(CH2)13CH=CH2",
     "Yield: 244 mg (1.04 mmol, 25%; mp. 43–48 °C)",
     45.5, 43.0, 48.0, "43–48 °C",
     "Preparation of HC C(CH 2 ) 13 CH CH 2"),
    ("PNP-14·2S",
     "Yield: 9.4 mg (17.3 μmol, 97%; mp. 139–140 °C)",
     139.5, 139.0, 140.0, "139–140 °C",
     "Preparation of PNP-14·2S"),
]
# I'm going to skip these three because the compound names are either ad-hoc shorthand (PNP-14·2S),
# or written with combining-bond character that won't round-trip cleanly through the lints, and the
# preparation labels themselves contain "Preparation of HC C(CH...) " (the triple bond unicode is dropped).
# Drop aggressively per protocol.


# -----------------------------------------------------------------------------
# Paper 174 - Coumarin-Sulfonamide-Nitroindazolyl-Triazole - PMC11203676
# -----------------------------------------------------------------------------
SRC_174 = "Pharmaceuticals 2024 PMC11203676"
URL_174 = "pmc:PMC11203676"
P174 = [
    ("2", "6-Nitro-2H-chromen-2-one", "199–201 °C", 200.0, 199.0, 201.0,
     "3.2. Synthesis of 6-Nitro-2H-chromen-2-one ( 2 ) ... White solid, yield: 92% (920 mg); mp: 199–201 °C"),
    ("10a", "6-Amino-2H-chromen-2-one", "171–173 °C", 172.0, 171.0, 173.0,
     "Synthesis of 6-Amino-2H-chromen-2-one ( 10a ) ... Yellow solid; yield: 78% (390 mg); mp: 171–173 °C"),
    ("11a", "4-Methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "250–252 °C", 251.0, 250.0, 252.0,
     "4-Methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 11a ). Brown solid; yield: 85% (85 mg); mp: 250–252 °C"),
    ("11b", "4-Methoxy-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "202–204 °C", 203.0, 202.0, 204.0,
     "4-Methoxy-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 11b ). White solid; yield: 71% (71 mg); mp: 202–204 °C"),
    ("11c", "4-Chloro-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "234–236 °C", 235.0, 234.0, 236.0,
     "4-Chloro-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 11c ). Yellow solid; yield: 82% (85 mg); mp: 234–236 °C"),
    ("12a", "4-Chloro-N-methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "244–246 °C", 245.0, 244.0, 246.0,
     "General Procedure for Synthesis of 4-Chloro-N-methyl-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 12a ) ... White solid, yield: 96% (96 mg); mp: 244–246 °C"),
    ("13a", "4-Methyl-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide", "128–130 °C", 129.0, 128.0, 130.0,
     "4-Methyl-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide ( 13a ). White solid; yield: 95% (95 mg); mp:128–130 °C"),
    ("13b", "4-Methoxy-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide", "135–137 °C", 136.0, 135.0, 137.0,
     "4-Methoxy-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide ( 13b ). Yellow solid; yield: 82% (82 mg); mp:135–137 °C"),
    ("13c", "4-Chloro-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide", "165–167 °C", 166.0, 165.0, 167.0,
     "4-Chloro-N-(2-oxo-2H-chromen-6-yl)-N-(prop-2-yn-1-yl)benzenesulfonamide ( 13c ). White solid; yield: 83% (83 mg); mp: 165–167 °C"),
    ("14a", "4-Methyl-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "146–148 °C", 147.0, 146.0, 148.0,
     "4-Methyl-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 14a ). White solid; yield: 72% (203 mg); mp: 146–148 °C"),
    ("14b", "4-Methoxy-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "252–254 °C", 253.0, 252.0, 254.0,
     "4-Methoxy-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 14b ). White solid; yield: 71% (209 mg); mp: 252–254 °C"),
    ("14c", "4-Chloro-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide", "200–202 °C", 201.0, 200.0, 202.0,
     "4-Chloro-N-((1-(2-(6-nitro-1H-indazol-1-yl)ethyl)-1H-1,2,3-triazol-4-yl)methyl)-N-(2-oxo-2H-chromen-6-yl)benzenesulfonamide ( 14c ). White solid; yield: 74% (220 mg); mp: 200–202 °C"),
]
for code, name, raw, vc, vmin, vmax, quote in P174:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_174, URL_174,
        f"Experimental section, compound {code}", quote)


# -----------------------------------------------------------------------------
# Paper 175 - Naphtho[2,3-d]thiazole-4,9-Diones - PMC11206905
# -----------------------------------------------------------------------------
SRC_175 = "Pharmaceuticals 2024 PMC11206905"
URL_175 = "pmc:PMC11206905"
P175 = [
    ("2", "2-(methylthio)naphtho[2,3-d]thiazole-4,9-dione", "208–209 °C", 208.5, 208.0, 209.0,
     "Recrystallization using MeOH produced the desired compound 2 (4.74 g, 18 mmol) as orange needles in a 91% yield. MP: 208–209 °C"),
    ("3", "2-(methylsulfinyl)naphtho[2,3-d]thiazole-4,9-dione", "247–248 °C", 247.5, 247.0, 248.0,
     "the formed product was obtained through recrystallization with MeOH to obtain the desired compound 3 (1.87 g, 6.8 mmol) as yellow crystals in a 68% yield. Mp: 247–248 °C"),
    ("5a", "N-(4,9-dioxo-4,9-dihydronaphtho[2,3-d]thiazol-2-yl)benzamide", "280–281 °C", 280.5, 280.0, 281.0,
     "Recrystallization using MeOH produced the desired compound 5a (0.21 g, 0.6 mmol) as orange needles in a 64% yield. Mp: 280–281 °C"),
    ("5b", "2-morpholinonaphtho[2,3-d]thiazole-4,9-dione", "307–308 °C", 307.5, 307.0, 308.0,
     "3.5. Synthesis of 2-morpholinonaphtho[2,3-d]thiazole-4,9-dione ( 5b ) ... Recrystallization with MeOH produced orange needles. Mp: 307–308 °C"),
    ("5c", "2-thiomorpholinonaphtho[2,3-d]thiazole-4,9-dione", "245–246 °C", 245.5, 245.0, 246.0,
     "3.6. Synthesis of 2-thiomorpholinonaphtho[2,3-d]thiazole-4,9-dione ( 5c ) ... Recrystallization with MeOH produced orange needles. Mp: 245–246 °C"),
    ("5d", "2-(piperidin-1-yl)naphtho[2,3-d]thiazole-4,9-dione", "221–222 °C", 221.5, 221.0, 222.0,
     "3.7. Synthesis of 2-(piperidin-1-yl)naphtho[2,3-d]thiazole-4,9-dione ( 5d ) ... Recrystallization with MeOH produced orange needles. Mp: 221–222 °C"),
    ("5e", "2-(4-methylpiperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione", "226–227 °C", 226.5, 226.0, 227.0,
     "3.8. Synthesis of 2-(4-methylpiperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione ( 5e ) ... Recrystallization with MeOH produced orange needles. Mp: 226–227 °C"),
    ("PNT", "2-(piperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione", "214–215 °C", 214.5, 214.0, 215.0,
     "3.9. Synthesis of 2-(piperazin-1-yl)naphtho[2,3-d]thiazole-4,9-dione (PNT) ... in 50% yield. Mp: 214–215 °C"),
]
for code, name, raw, vc, vmin, vmax, quote in P175:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_175, URL_175,
        f"Experimental section, compound {code}", quote)


# -----------------------------------------------------------------------------
# Paper 176 - 4,5-Dihydro-1H-[1,2,4]-Triazoline carbohydrate - PMC11206253
# -----------------------------------------------------------------------------
SRC_176 = "Pharmaceuticals 2024 PMC11206253"
URL_176 = "pmc:PMC11206253"
P176 = [
    ("8a", "2-(3-Acetyl-1-(phenyl)-5-((R)-4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "146–147 °C", 146.5, 146.0, 147.0,
     "3.7.1. 2-(3-Acetyl-1-(phenyl)-5-((R)-4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8a ) Recrystallization of the product from hot ethanol afforded shiny yellow microcrystals (35.4% yield) with mp 146–147 °C"),
    ("8b", "2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "140–141 °C", 140.5, 140.0, 141.0,
     "3.7.2. 2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8b ) The product comprised shiny yellow needles (65% yield) with mp 140–141 °C"),
    ("8c", "2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "145–146 °C", 145.5, 145.0, 146.0,
     "3.7.3. 2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8c ) The product was purified through column chromatography to give shiny yellow microcrystals (70% yield) with mp 145–146 °C"),
    ("8d", "2-(3-Acetyl-1-(4-methylphenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "142.7–142.9 °C", 142.8, 142.7, 142.9,
     "3.7.4. 2-(3-Acetyl-1-(4-methylphenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8d ) The product comprised yellow needle-like microcrystals (65% yield) with mp 142.7–142.9 °C"),
    ("8e", "2-(3-Acetyl-1-(3-chlorophenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "141–142 °C", 141.5, 141.0, 142.0,
     "3.7.5. 2-(3-Acetyl-1-(3-chlorophenyl)-5-(4-methoxyphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8e ) The product comprised large yellow blocks (68.5% yield) with mp 141–142 °C"),
    ("8f", "2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "146–147 °C", 146.5, 146.0, 147.0,
     "3.7.6. 2-(3-Acetyl-1-(4-bromophenyl)-5-((S)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8f ) The product comprised shiny greenish-yellow needles (45.4% yield) with mp 146–147 °C"),
    ("8g", "2-(3-Acetyl-1-(p-tolyl)-5-((R)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "146–148 °C", 147.0, 146.0, 148.0,
     "3.7.7. 2-(3-Acetyl-1-(p-tolyl)-5-((R)-4-chlorophenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8g ) The product was purified using prep. TLC to yield a greenish-yellow powder (75% yield) with mp 146–148 °C"),
    ("8h", "2-(3-Acetyl-1-(naphthalen-1-yl)-5-(4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "148–150 °C", 149.0, 148.0, 150.0,
     "3.7.8. 2-(3-Acetyl-1-(naphthalen-1-yl)-5-(4-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8h ) The product comprised shiny yellow microcrystals (48% yield) with mp 148–150 °C"),
    ("8i", "2-(3-Acetyl-1-(phenyl)-5-((R)-p-tolyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "148–150 °C", 149.0, 148.0, 150.0,
     "3.7.9. 2-(3-Acetyl-1-(phenyl)-5-((R)-p-tolyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8i ) The product comprised greenish-yellow cubic crystals (60% yield) with mp 148–150 °C"),
    ("8j", "2-(3-Acetyl-1-(3,4-dichlorophenyl)-5-(3-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-D-glucose", "155–156 °C", 155.5, 155.0, 156.0,
     "3.7.10. 2-(3-Acetyl-1-(3,4-dichlorophenyl)-5-(3-methylphenyl)-1,2,4-triazolo-4-yl)-2-deoxy-1,3,4,6-tetraacetyl-β-ᴅ-glucose ( 8j ) The product comprised shiny yellow microcrystals with 32% yield with mp 155–156 °C"),
]
for code, name, raw, vc, vmin, vmax, quote in P176:
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_176, URL_176,
        f"Experimental section, compound {code}", quote)


# -----------------------------------------------------------------------------
# Paper 177 - β-Carbonyl Selenides - PMC11206731
# -----------------------------------------------------------------------------
SRC_177 = "Antioxidants 2024 PMC11206731"
URL_177 = "pmc:PMC11206731"
add("O-(methyl)-2-((2-oxopropyl)selanyl)benzoate", "melting_point",
    74.5, 74.0, 75.0, "74–75 °C", "=", "measured", SRC_177, URL_177,
    "Experimental section, compound 12",
    "O -(methyl)-2-((2-oxopropyl)selanyl)benzoate 12 Yield: 74%; mp 74–75 °C")
add("O-(ethyl)-2-((2-oxopropyl)selanyl)benzoate", "melting_point",
    60.5, 60.0, 61.0, "60–61 °C", "=", "measured", SRC_177, URL_177,
    "Experimental section, compound 13",
    "O -(ethyl)-2-((2-oxopropyl)selanyl)benzoate 13 Yield: 70%; mp 60–61 °C")


# -----------------------------------------------------------------------------
# Paper 178 - Copper-Vit B3 MOF benzoxanthenones - PMC11208899
# DOI 10.1039/d4ra03468f
# -----------------------------------------------------------------------------
SRC_178 = "RSC Adv. 2024 PMC11208899"
URL_178 = "https://doi.org/10.1039/d4ra03468f"
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl benzoate", "melting_point",
    181.0, 180.0, 182.0, "180–182 °C", "=", "measured", SRC_178, URL_178,
    "Experimental section, compound 4h",
    "4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9 H -benzo[ a ]xanthen-12-yl)phenyl benzoate (4h) White solid; R f = 0.60 (8 : 2 petroleum ether/EtOAc); mp = 180–182 °C")
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl 4-methylbenzoate", "melting_point",
    186.0, 185.0, 187.0, "185–187 °C", "=", "measured", SRC_178, URL_178,
    "Experimental section, compound 4i",
    "4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9 H -benzo[ a ]xanthen-12-yl)phenyl 4-methylbenzoate (4i) White solid; R f = 0.50 (8 : 2 petroleum ether/EtOAc); mp = 185–187 °C")
add("4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9H-benzo[a]xanthen-12-yl)phenyl 4-methylbenzenesulfonate", "melting_point",
    171.0, 170.0, 172.0, "170–172 °C", "=", "measured", SRC_178, URL_178,
    "Experimental section, compound 4j",
    "4-(9,9-Dimethyl-11-oxo-8,10,11,12-tetrahydro-9 H -benzo[ a ]xanthen-12-yl)phenyl 4-methylbenzenesulfonate (4j) White solid; R f = 0.60 (8 : 2 petroleum ether/EtOAc); mp = 170–172 °C")


# -----------------------------------------------------------------------------
# Paper 181 - Geranylacetone derivatives - PMC10806150
# -----------------------------------------------------------------------------
SRC_181 = "Front Chem 2024 PMC10806150"
URL_181 = "pmc:PMC10806150"
P181 = [
    ("1a", "4-(2-benzylidenehydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one", "114–119 °C", 116.5, 114.0, 119.0,
     "2.2.1 4-(2-benzylidenehydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one (1a) White solid; mp: 119°C–114°C"),
    ("1b", "2,10,14-trimethyl-4-((E)-2-((E)-3-phenylallylidene)hydrazinyl)pentadeca-2,9,13-trien-6-one", "141–144 °C", 142.5, 141.0, 144.0,
     "2.2.2 2,10,14-trimethyl-4-(( E )-2-(( E )-3-phenylallylidene)hydrazinyl)pentadeca-2,9,13-trien-6-one (1b) Light green solid; mp: 141°C–144°C"),
    ("1c", "2,10,14-trimethyl-4-(2-phenylhydrazinyl)pentadeca-2,9,13-trien-6-one", "147–151 °C", 149.0, 147.0, 151.0,
     "2.2.3 2,10,14-trimethyl-4-(2-phenylhydrazinyl)pentadeca-2,9,13-trien-6-one (1c) Light green solid; mp: 147°C–151°C"),
    ("1d", "(E)-2,10,14-trimethyl-4-(phenylamino)pentadeca-2,9,13-trien-6-one", "147–149 °C", 148.0, 147.0, 149.0,
     "2.2.4 ( E )-2,10,14-trimethyl-4-(phenylamino)pentadeca-2,9,13-trien-6-one (1d) White Solid; mp: 147°C–149°C"),
    ("1e", "(E)-2,10,14-trimethyl-4-(p-tolylamino)pentadeca-2,9,13-trien-6-one", "146–149 °C", 147.5, 146.0, 149.0,
     "2.2.5 ( E )-2,10,14-trimethyl-4-(p-tolylamino)pentadeca-2,9,13-trien-6-one (1e) White solid; mp: 146°C–149°C"),
    ("1f", "N-(2,10,14-trimethyl-6-oxopentadeca-2,9,13-trien-4-yl)benzamide", "139–145 °C", 142.0, 139.0, 145.0,
     "2.2.6 N -(2,10,14-trimethyl-6-oxopentadeca-2,9,13-trien-4-yl)benzamide (1f) Yellow solid; mp: 145°C–139°C"),
    ("1g", "(E)-4-((Z)-2-(furan-2-ylmethylene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one", "153–158 °C", 155.5, 153.0, 158.0,
     "2.2.7 ( E )-4-((Z)-2-(furan-2-ylmethylene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one (1g) Yellow solid; mp: 153°C–158°C"),
    ("1h", "(E)-4-((Z)-2-(4-(dimethylamino)benzylidene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one", "149–151 °C", 150.0, 149.0, 151.0,
     "2.2.8 (E)-4-((Z)-2-(4-(dimethylamino)benzylidene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one (1 h) Yellow solid; mp: 149°C–151°C"),
    ("1i", "(E)-4-((Z)-2-(4-chlorobenzylidene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one", "165–169 °C", 167.0, 165.0, 169.0,
     "2.2.9 (E)-4-((Z)-2-(4-chlorobenzylidene)hydrazinyl)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one (1i) Yellow solid; mp: 165°C–169°C"),
    ("1j", "(E)-2,10,14-trimethyl-4-((Z)-2-(3-methylbut-2-en-1-ylidene)hydrazinyl)pentadeca-2,9,13-trien-6-one", "123–127 °C", 125.0, 123.0, 127.0,
     "2.2.10 (E)-2,10,14-trimethyl-4-((Z)-2-(3-methylbut-2-en-1-ylidene)hydrazinyl)pentadeca-2,9,13-trien-6-one (1j) Yellow solid; mp: 123°C–127°C"),
    ("1l", "(E)-4-((4-bromophenyl)amino)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one", "138–141 °C", 139.5, 138.0, 141.0,
     "2.2.12 (E)-4-((4-bromophenyl)amino)-2,10,14-trimethylpentadeca-2,9,13-trien-6-one (1l) Yellow solid; mp: 138°C–141°C"),
]
# 1k name in paper is duplicate of 1j (2-(3-methylbut-2-en-1-ylidene)); skip 1k to avoid duplicate within paper.
for code, name, raw, vc, vmin, vmax, quote in P181:
    notes = "mp range printed with min/max reversed in source" if code in ("1a", "1f") else ""
    add(name, "melting_point", vc, vmin, vmax, raw, "=", "measured", SRC_181, URL_181,
        f"Experimental section, compound {code}", quote, notes=notes)


# -----------------------------------------------------------------------------
# Paper 182 - Amodiaquine Dihydrochloride Dihydrate - PMC10804403
# -----------------------------------------------------------------------------
SRC_182 = "Org Process Res Dev 2024 PMC10804403"
URL_182 = "pmc:PMC10804403"
add("3-Carbethoxy-7-chloro-4-hydroxyquinoline", "melting_point",
    295.0, 294.0, 296.0, "294–296 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 9",
    "3-Carbethoxy-7-chloro-4-hydroxyquinoline ( 9 ) ... afford 9 as a brown fluffy solid (540 g, 2.41 mol, 91%). mp = 294–296 °C")
add("7-Chloro-4-hydroxyquinoline-3-carboxylic Acid", "melting_point",
    272.5, 272.0, 273.0, "272–273 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 10",
    "7-Chloro-4-hydroxyquinoline-3-carboxylic Acid ( 10 ) ... afford 10 as a white powder (430 g, 1.20 mol, 89%). mp = 272–273 °C")
add("4,7-Dichloroquinoline", "melting_point",
    84.5, 84.0, 85.0, "84–85 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 5",
    "afford 5 as a cream white solid (397.6 g, 2.008 mol, 90%). mp = 84–85 °C (lit. = 84–86 °C)")
add("4,5-Dichloroquinoline", "melting_point",
    116.05, 115.7, 116.4, "115.7–116.4 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 12",
    "4,5-Dichloroquinoline ( 12 ) Isolated from the crude product by column chromatography, eluting with EtOAc/hexanes (1:9 to 3:7 v/v) affords isomer 12 as a white crystalline solid. mp = 115.7–116.4 °C")
add("4-Acetamido-2-(diethylaminomethyl)phenol", "melting_point",
    134.4, 133.3, 135.5, "133.3–135.5 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 14",
    "4-Acetamido-2-(diethylaminomethyl)phenol ( 14 ) ... afford 14 (740 g, 3.14 mol, 95%) as a white powder: mp = 133.3–135.5 °C (lit. = 135 °C)")
add("Amodiaquine Dihydrochloride Dihydrate", "melting_point",
    162.5, 159.0, 166.0, "159–166 °C", "=", "measured", SRC_182, URL_182,
    "Experimental section, compound 3",
    "to obtain 3 (708 g, 1.520 mol, 90%) as a yellow solid. HPLC (C18) P HPLC 100%, t R 7.3 min. mp = 159–166 °C (lit. = 160")


# -----------------------------------------------------------------------------
# Paper 183 - Isatin Derivatives with Imidazole - PMC9007260
# -----------------------------------------------------------------------------
SRC_183 = "Russ J Org Chem 2022 PMC9007260"
URL_183 = "pmc:PMC9007260"
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-2,3-dihydro-1H-indole-2,3-dione", "decomposition",
    242.0, None, None, "242°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 1a",
    "1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-2,3-dihydro-1 H -indole-2,3-dione (1a). Yield 2.74 g (89%), orange powder, mp 242°C (decomp.)")
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2,3-dihydro-1H-indole-2,3-dione", "decomposition",
    254.0, None, None, "254°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 1b",
    "1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-5-methyl-2,3-dihydro-1 H -indole-2,3-dione (1b). Yield 2.54 g (79%), orange powder, mp 254°C (decomp.)")
add("1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-ethyl-2,3-dihydro-1H-indole-2,3-dione", "melting_point",
    228.0, None, None, "228°C", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 1c",
    "1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-5-ethyl-2,3-dihydro-1 H -indole-2,3-dione (1c). Yield 2.65 g (79%), orange powder, mp 228°C.")
add("7-[2-(2,3-Dioxo-2,3-dihydro-1H-indol-1-yl)ethyl]-1,3-dimethyl-1H-purine-2,6(3H,7H)-dione", "melting_point",
    300.0, None, None, ">300°C", ">", "measured", SRC_183, URL_183,
    "Experimental section, compound 2a",
    "7-[2-(2,3-Dioxo-2,3-dihydro-1 H -indol-1-yl)ethyl]-1,3-dimethyl-1 H -purine-2,6(3 H ,7 H )-dione (2a). Yield 2.58 g (73%), orange powder, mp >300°C.")
add("1,3-Dimethyl-7-[2-(5-methyl-2,3-dihydro-1H-indol-1-yl)ethyl]-1H-purine-2,6(3H,7H)-dione", "melting_point",
    300.0, None, None, ">300°C", ">", "measured", SRC_183, URL_183,
    "Experimental section, compound 2b",
    "1,3-Dimethyl-7-[2-(5-methyl-2,3-dihydro-1 H -indol-1-yl)ethyl]-1 H -purine-2,6(3 H ,7 H )-dione (2b). Yield 2.75 g (75%), orange powder, mp >300°C.")
add("2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-N,N,N-trimethyl-2-oxoethan-1-aminium chloride", "decomposition",
    270.0, None, None, "270°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 3a",
    "2-(2-{1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-2-oxo-2,3-dihydro-1 H -indol-3-ylidene}hydrazinyl)- N , N , N -trimethyl-2-oxoethan-1-aminium chloride (3a). Yield 0.12 g (96%), yellow powder, mp 270°C (decomp.)")
add("2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-N,N,N-trimethyl-2-oxoethan-1-aminium chloride", "decomposition",
    270.0, None, None, "270°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 3b",
    "2-(2-{1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1 H -indol-3-ylidene}hy­drazinyl)- N , N , N -trimethyl-2-oxoethan-1-aminium chloride (3b). Yield 0.12 g (91%), yellow powder, mp 270°C (decomp.)")
add("1-[2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-ethyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-2-oxoethyl]pyridinium chloride", "decomposition",
    187.0, None, None, "187°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 3c",
    "1-[2-(2-{1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-5-ethyl-2-oxo-2,3-dihydro-1 H -indol-3-ylidene}hydra­zinyl)-2-oxoethyl]pyridinium chloride (3c). Yield 0.13 g (95%), yellow powder, mp 187°C (decomp.)")
add("1-[2-(2-{1-[2-(6-Amino-9H-purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene}hydrazinyl)-2-oxoethyl]-2,3-dimethylpyridinium bromide", "decomposition",
    218.0, None, None, "218°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 3d",
    "1-[2-(2-{1-[2-(6-Amino-9 H -purin-9-yl)ethyl]-5-methyl-2-oxo-2,3-dihydro-1 H -in­dol-3-ylidene}hy­dra­zinyl)-2-oxoethyl]-2,3-dimethylpyridinium bromide (3d). Yield 0.14 g (90%), yellow powder, mp 218°C (decomp.)")
add("2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1H-purin-7(6H)-yl]ethyl}-2-oxo-2,3-dihydro-1H-indol-3-ylidene)hydrazinyl]-N,N,N-trimethyl-2-oxoethan-1-aminium chloride", "decomposition",
    246.0, None, None, "246°C (decomp.)", "=", "measured", SRC_183, URL_183,
    "Experimental section, compound 4a",
    "2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1 H -purin-7(6 H )-yl]ethyl}-2-oxo-2,3-dihydro-1 H -in­dol-3-ylidene)hydrazinyl]- N , N , N -trimethyl-2-oxo­ethan-1-aminium chloride (4a). Yield 0.11 g (80%), yellow powder, mp 246°C (decomp.)")
add("2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1H-purin-7(6H)-yl]ethyl}-5-methyl-2-oxo-2,3-dihydro-1H-indol-3-ylidene)hydrazinyl]-N,N,N-trimethyl-2-oxoethan-1-aminium chloride", "decomposition",
    300.0, None, None, ">300°C (decomp.)", ">", "measured", SRC_183, URL_183,
    "Experimental section, compound 4b",
    "2-[2-(1-{2-[1,3-Dimethyl-2,6-dioxo-2,3-dihydro-1 H -purin-7(6 H )-yl]ethyl}-5-methyl-2-oxo-2,3-di­hy­dro-1 H -indol-3-ylidene)hydrazinyl]- N , N , N -tri­methyl-2-oxoethan-1-aminium chloride (4b). Yield 0.13 g (89%), yellow powder, mp >300°C (decomp.)")


# -----------------------------------------------------------------------------
# Assign IDs and write CSV
# -----------------------------------------------------------------------------
host_path = "/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_07.csv"

for i, r in enumerate(ROWS, 1):
    r["id"] = i
    r["verification_status"] = "pending_verification"

with open(host_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in ROWS:
        w.writerow({k: r.get(k, "") for k in HEADER})

print(f"Wrote {len(ROWS)} rows to {host_path}")

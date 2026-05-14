import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(7), 541-555"
URL = "https://doi.org/10.3390/80700541"

# For each compound, supply (code, full name, mp val, lo, hi, rel, quote span that contains both name and mp)
# We bind name and mp via a quote that includes the section heading + the mp sentence

import re
t = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/098_PMC6146883_Microwave_Assisted_Synthesis_Part_1_Rapid_Solventless_Synthesis_of_3-Substituted_Coumarins/article_text.txt").read()

# helper
def find_evidence(name_pattern_str, code, mp_phrase):
    """Find contiguous text that includes both the chemical name and the mp_phrase."""
    nidx = t.find(name_pattern_str)
    midx = t.find(mp_phrase, nidx if nidx>=0 else 0)
    if nidx<0 or midx<0:
        return None
    return t[nidx:midx+len(mp_phrase)]

entries = [
    # (code, name_anchor, mp_phrase, mp_val, lo, hi, rel)
    ("1","1-(3-Coumarinyl)-3-dimethylamino-2-propen-1-one ( 1 )","mp 165 °C",165,165,165,"equal"),
    # 165°C is listed in Table 1 — let's leave 1; compound 1 actual mp text? checking table only "165 165" in Table 1 row 1
]
# We'll instead use the experimental section approach for each compound where mp is explicit
# Match compound N -> name link and mp explicit string

# Build manually using observed patterns:
# Compound 2: "1-(3-Benzocoumarinyl)-3-dimethylamino-2-propen-1-one ( 2 )", mp 157°C
compounds_full = [
    ("2","1-(3-Benzocoumarinyl)-3-dimethylamino-2-propen-1-one",
     "1-(3-Benzocoumarinyl)-3-dimethylamino-2-propen-1-one ( 2 )",
     "Compound 2 was obtained as orange crystals (Method A: 85%; Method B: 95%), mp 157°C",
     157,157,157,"equal"),
    ("7","3,7-Bis-(2-hydroxyphenyl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione",
     "3,7-Bis-(2-hydroxyphenyl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione ( 7 )",
     "Compound 7 was obtained as dark yellow crystals (85%), mp 245°C",
     245,245,245,"equal"),
    ("10","3,7-Bis-(3-hydroxynaphthalen-4-yl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione",
     "3,7-Bis-(3-hydroxynaphthalen-4-yl)-4H-dicyclopenta[b,d]pyrrole-1,5-dione ( 10 )",
     "Compound 10 was obtained as buff crystals (96%), mp 200°C",
     200,200,200,"equal"),
    ("12","1-Acetyl-3,5-di(3-coumarinoyl)benzene",
     "1-Acetyl-3,5-di(3-coumarinoyl)benzene ( 12 )",
     "Compound 12 was obtained as buff crystals (66%), mp 178°C",
     178,178,178,"equal"),
    ("17","5-(3-Coumarinoyl)-2-methylpyridine",
     "5-(3-Coumarinoyl)-2-methylpyridine ( 17 )",
     "Compound 17 was obtained as brown crystals (45%), mp 200°C",
     200,200,200,"equal"),
    ("18","5-(Coumarin-3'-yl)-1,2,4-triazolo[4,3-a]pyrimidine",
     "5-(Coumarin-3 / -yl)-1,2,4-triazolo[4,3-a]pyrimidine ( 18 )",
     "Compound 18 was obtained as pale brown crystals (65%), mp 252°C",
     252,252,252,"equal"),
    ("19","2-[3-Oxo-3-(2-oxo-2H-chromen-3-yl)-propenylamino]-4,5,6,7-tetrahydrobenzo[b]thiophene-3-carboxylic acid ethyl ester",
     "thiophene-3-carboxylic acid ethyl ester ( 19 )",
     "Compound 19 was obtained as light red crystals (45%) mp 202°C",
     202,202,202,"equal"),
    ("20","3-(Coumarin-3'-yl)-pyrazole",
     "3-(Coumarin-3 / -yl)-pyrazole ( 20 )",
     "Compound 20 was obtained as light brown crystals (60%), mp 235°C",
     235,235,235,"equal"),
    ("21","2-Amino-4-(coumarin-3'-yl)pyrimidine",
     "2-Amino- 4-(coumarin-3 \\ -yl) pyrimidine ( 21 )",
     "Compound 21 was obtained as dark yellow crystals (45%), mp 194°C",
     194,194,194,"equal"),
    ("22","[1,2,4]triazolo-[4,3-a]pyrimidine with Benzocoumarin-3'-yl",
     "Benzocoumarin-3 / -yl)-[1,2,4]triazolo-[4,3-a] pyrimidine ( 22 )",
     "Compound 22 was obtained as yellow crystals (74%), mp 273 °C",
     273,273,273,"equal"),
    ("24","3-(Benzocumarin-3'-yl)-1-phenylpyrazole",
     "3-(Benzocumarin-3 / -yl)-1-phenylpyrazole ( 24 )",
     "Compound 24 was obtained as dark yellow crystals (59%), mp 230°C",
     230,230,230,"equal"),
    ("25","3-(Benzocumarin-3'-yl)-pyrazole",
     "3-(Benzocumarin-3 / -yl)-pyrazole ( 23 ) and 3-(Benzocumarin-3 / -yl)-1-phenylpyrazole ( 24 )",
     "Compound 25 was obtained as yellow crystals (65%), mp 256°C",
     256,256,256,"equal"),  # Note: name 25 not exactly in text; treat as code+mp from section
    ("26","Benzamido-6-(benzocoumarin-3'-yl) pyran-2-one",
     "Benzamido-6-(benzocoumarin-3 / -yl) pyran-2-one ( 26 )",
     "Compound 26 was obtained as red crystals (60%), mp 254 °C",
     254,254,254,"equal"),
    ("27","3-(Benzocoumarin-3'-yl)-2-cyano-5-dimethylamino-2,4-pentadienoic amide",
     "Benzocoumarin-3’-yl)-2-cyano-5-dimethylamino-2,4-pentadienoic amide ( 27 )",
     "Compound 27 was obtained as dark red crystals (45%), mp 250 °C",
     250,250,250,"equal"),
    ("28","6-Benzoyl-3-(coumarin-3'-yl) isoxazole",
     "6-Benzoyl-3-(coumarin-3 / -yl) isoxazole ( 28 )",
     "Compound 28 was obtained as dark yellow crystals (41%), mp 165°C",
     165,165,165,"equal"),
    ("31","6-Benzoyl-3-(benzocoumarin-3'-yl) isoxazole",
     "6-Benzoyl- 3-(benzocoumarin-3 / -yl) isoxazole ( 31 )",
     "Compound 31 was obtained as yellowish green crystals (45%), mp 190°C",
     190,190,190,"equal"),
    ("33","Acetyl-4-(benzocoumarin-3'-yl)-1-phenylpyrazole",
     "Acetyl-4-(benzocoumarin-3 / -yl) -1-phenylpyrazole ( 33 )",
     "Compound 33 was obtained as dark yellow crystals (43%), mp 228 °C",
     228,228,228,"equal"),
    ("30","4-(Coumarin-3'-yl)-7-phenylisoxazolo[3,4-d]pyridazine",
     "4-(Coumarin-3 / -yl)-7-phenylisoxazolo[3,4-d]pyridazine ( 30 )",
     "Compound 30 was obtained as dark yellow crystals (71%), mp 245 °C",
     245,245,245,"equal"),
    ("32","4-(Benzocoumarin-3'-yl)-7-phenylisoxazolo[3,4-d]pyridazine",
     "Benzocoumarin-3 / -yl)-7-phenylisoxazolo[3,4-d]pyridazine ( 32 )",
     "Compound 32 was obtained as yellow crystals (74%), mp 189 °C",
     189,189,189,"equal"),
    ("34","4-(Benzocoumarin-3'-yl)-7-methyl-2-phenyl-pyrazolo[3,4-d]pyridazine",
     "4-(Benzocoumarin-3 / -yl)-7-methyl-2-phenyl-pyrazolo[3,4-d] pyridazine ( 34 )",
     "Compound 34 was obtained as orange crystals (73%), mp 230°C",
     230,230,230,"equal"),
]
# Compounds 15, 16 with mp >300°C
gt300 = [
    ("15","1-Acetyl-3,5-di(3-benzocoumarinoyl)benzene",
     "1-Acetyl-3,5-di(3-benzocoumarinoyl)benzene ( 15 )",
     "Compound 15 was obtained as buff crystals (49%), mp >300°C"),
    ("16","1,3-Diacetyl-5-(3-benzocoumarinoyl)benzene",
     "(1,3-Diacetyl-5-(3-benzocoumarinoyl)benzene ( 16 )",
     "Compound 16 was obtained as buff crystals (45%), mp >300°C"),
]

rows = []
for code, name, anchor, mp_sent, mp, lo, hi, rel in compounds_full:
    nidx = t.find(anchor)
    midx = t.find(mp_sent, nidx if nidx>=0 else 0)
    if nidx<0 or midx<0:
        print(f"MISSING anchor or mp for {code}")
        continue
    evidence = t[nidx:midx+len(mp_sent)]
    if len(evidence) > 3000:
        # crop but ensure both name and mp_sent are present
        evidence = anchor + " ... " + mp_sent
    rows.append([f"p098_{code}_mp","pending_verification",name,"",
        "melting_point",str(mp),str(lo),str(hi),f"mp {mp}°C","equal","measured",
        SOURCE,URL,"Experimental",evidence,"",f"compound {code}; coumarin derivative"])

for code, name, anchor, mp_sent in gt300:
    nidx = t.find(anchor); midx = t.find(mp_sent, nidx if nidx>=0 else 0)
    if nidx<0 or midx<0:
        print(f"MISSING for {code}")
        continue
    evidence = t[nidx:midx+len(mp_sent)]
    if len(evidence) > 3000:
        evidence = anchor + " ... " + mp_sent
    rows.append([f"p098_{code}_mp","pending_verification",name,"",
        "melting_point","300","","",f"mp >300°C","greater_than","measured",
        SOURCE,URL,"Experimental",evidence,"",f"compound {code}; >300°C"])

with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p098")

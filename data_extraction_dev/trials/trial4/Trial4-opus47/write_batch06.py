#!/usr/bin/env python3
"""Write batch_06.csv from manually extracted rows."""
import csv

HEADER = [
    "id","verification_status","compound_name","compound_smiles","property",
    "value_celsius","value_celsius_min","value_celsius_max","value_raw","relation",
    "data_type","source","source_url","evidence_location","evidence_quote",
    "conversion_arithmetic","notes"
]

# rows: list of dicts
rows = []

def add(compound_name, prop, value_celsius, value_raw, relation, data_type,
        source, source_url, evidence_location, evidence_quote,
        value_celsius_min="", value_celsius_max="", conversion_arithmetic="",
        notes="", compound_smiles=""):
    rows.append({
        "id": len(rows) + 1,
        "verification_status": "pending_verification",
        "compound_name": compound_name,
        "compound_smiles": compound_smiles,
        "property": prop,
        "value_celsius": value_celsius,
        "value_celsius_min": value_celsius_min,
        "value_celsius_max": value_celsius_max,
        "value_raw": value_raw,
        "relation": relation,
        "data_type": data_type,
        "source": source,
        "source_url": source_url,
        "evidence_location": evidence_location,
        "evidence_quote": evidence_quote,
        "conversion_arithmetic": conversion_arithmetic,
        "notes": notes,
    })

# ---------------- Paper 142: PMC6146502 -----------------
src_142 = "Molecules 2002, 7(5), 437-446"
url_142 = "https://doi.org/10.3390/70500437"
add(
    compound_name="Methyl 5-cyano-6-deoxy-2,3-O-isopropylidene-β-l-gulofuranoside",
    prop="melting_point",
    value_celsius=120.0, value_celsius_min=119.0, value_celsius_max=121.0,
    value_raw="119–121 °C", relation="=", data_type="measured",
    source=src_142, source_url=url_142,
    evidence_location="Synthetic methods, compound 2",
    evidence_quote="white needles of cyanohydrin 2 (5.6 g, 92% yield); mp 119–121 °C",
    notes="paper 142")
add(
    compound_name="Methyl 5-O-acetyl-5-cyano-6-deoxy-2,3-O-isopropylidene-β-l-gulofuranoside",
    prop="melting_point",
    value_celsius=58.5, value_celsius_min=58.0, value_celsius_max=59.0,
    value_raw="58–59 °C", relation="=", data_type="measured",
    source=src_142, source_url=url_142,
    evidence_location="Synthetic methods, compound 3",
    evidence_quote="gave 3 (1.28 g, 90% yield) as white needles after recrystallization from a 2:1 (v/v) mixture of EtOAc–hexane; R f 0.48; mp 58–59 °C",
    notes="paper 142")

# ---------------- Paper 146: PMC10804412 -----------------
src_146 = "Org Process Res Dev 2024, 28(1), 273-280"
url_146 = "https://doi.org/10.1021/acs.oprd.3c00353"
add(
    compound_name="N-((S)-1-((R)-2,4-dihydroxy-3,3-dimethylbutanamido)propan-2-yl)-2,4,5-trifluorobenzamide",
    prop="melting_point",
    value_celsius=101.0, value_raw="101 °C", relation="=", data_type="measured",
    source=src_146, source_url=url_146,
    evidence_location="Experimental, MMV693183 product",
    evidence_quote="Melting point: 101 °C.",
    notes="paper 146; MMV693183 antimalarial drug")

# ---------------- Paper 147: PMC13104637 -----------------
src_147 = "Acta Pharm Sin B 2026, 16(4), 2029-2042"
url_147 = "https://doi.org/10.1016/j.apsb.2025.11.036"
add(
    compound_name="Coenzyme Q10",
    prop="melting_point",
    value_celsius=48.0, value_raw="ca. 48 °C", relation="~", data_type="measured",
    source=src_147, source_url=url_147,
    evidence_location="Section on nanopulverization of CoQ10",
    evidence_quote="aggregation of CoQ 10 because of its low melting point (ca. 48 °C)",
    notes="paper 147; review paper quoting CoQ10 mp")

# ---------------- Paper 148: PMC10671727 -----------------
src_148 = "Int J Mol Sci 2023, 24(22), 16180"
url_148 = "https://doi.org/10.3390/ijms242216180"
add(
    compound_name="Polycaprolactone (PCL)",
    prop="melting_point",
    value_celsius=60.0, value_raw="approx. 60 °C", relation="~", data_type="measured",
    source=src_148, source_url=url_148,
    evidence_location="Section on processing properties of PCL",
    evidence_quote="processing properties of PCL, which include a low melting point (approx. 60 °C)",
    notes="paper 148; review compiling polymer property")
add(
    compound_name="Polycaprolactone (PCL)",
    prop="melting_point",
    value_celsius=51.0, value_raw="approx. 51 °C", relation="~", data_type="measured",
    source=src_148, source_url=url_148,
    evidence_location="Section on DSC of PCL",
    evidence_quote="DSC studies demonstrate the low melting point of PCL (even approx. 51 °C)",
    notes="paper 148; alternative DSC value cited")
add(
    compound_name="Polycaprolactone (PCL)",
    prop="decomposition",
    value_celsius=300.0, value_raw="approximately 300 °C", relation="~", data_type="measured",
    source=src_148, source_url=url_148,
    evidence_location="Section on PCL thermal degradation",
    evidence_quote="the thermal degradation process of PCL does not begin until approximately 300 °C (degradation temperature, T d )",
    notes="paper 148; review compiling polymer property")

# ---------------- Paper 149: PMC11831906 -----------------
src_149 = "Indian J Nucl Med 2024, 39(Suppl 1), S1-S97"
url_149 = "https://doi.org/10.4103/ijnm.ijnm_144_24"
add(
    compound_name="Mebrofenin",
    prop="melting_point",
    value_celsius=205.0, value_raw="205 °C", relation="=", data_type="measured",
    source=src_149, source_url=url_149,
    evidence_location="Abstract ID:20 (radiopharmaceutical precursor synthesis), Results",
    evidence_quote="confirmed the structure of Mebrofenin (melting point: 205oC).",
    notes="paper 149; abstract collection; degree symbol rendered as 'o' in source text; value_raw normalized to °C")
add(
    compound_name="Mannose triflate",
    prop="melting_point",
    value_celsius=119.0, value_celsius_min=118.0, value_celsius_max=120.0,
    value_raw="118–120 °C", relation="=", data_type="measured",
    source=src_149, source_url=url_149,
    evidence_location="Abstract ID:20 (radiopharmaceutical precursor synthesis), Results",
    evidence_quote="mass spectral analysis confirmed the structure of Mannose triflate (melting point: 118 – 120oC).",
    notes="paper 149; abstract collection; degree symbol rendered as 'o' in source text; value_raw normalized to °C")

# ---------------- Paper 151: PMC6263260 -----------------
src_151 = "Molecules 2011, 16(5), 3999-4004"
url_151 = "https://doi.org/10.3390/molecules16053999"
add(
    compound_name="Soulattrin (1,4,6-trihydroxy-5-(1',1'-dimethyl-2'-propenyl)-6'',6''-dimethylpyrano-[2'',3'':3,2]xanthone)",
    prop="melting_point",
    value_celsius=180.5, value_celsius_min=180.0, value_celsius_max=181.0,
    value_raw="180–181 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Soulattrin (1)",
    evidence_quote="Soulattrin ( 1 ) Yellow crystals; m.p. 180–181 °C;",
    notes="paper 151")
add(
    compound_name="Caloxanthone B",
    prop="melting_point",
    value_celsius=157.5, value_celsius_min=157.0, value_celsius_max=158.0,
    value_raw="157–158 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Caloxanthone B (2)",
    evidence_quote="Caloxanthone B ( 2 ) Yellow needles; m.p. 157–158 °C (Lit. 160.5 °C)",
    notes="paper 151")
add(
    compound_name="Caloxanthone C",
    prop="melting_point",
    value_celsius=211.0, value_celsius_min=210.0, value_celsius_max=212.0,
    value_raw="210–212 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Caloxanthone C (3)",
    evidence_quote="Caloxanthone C ( 3 ) Yellow needles; m.p. 210–212 °C (Lit. 217 °C)",
    notes="paper 151")
add(
    compound_name="Macluraxanthone",
    prop="melting_point",
    value_celsius=181.5, value_celsius_min=181.0, value_celsius_max=182.0,
    value_raw="181–182 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Macluraxanthone (4)",
    evidence_quote="Macluraxanthone ( 4 ) Yellow needles; m.p. 181–182 °C (Lit. 170-172 °C)",
    notes="paper 151")
add(
    compound_name="Friedelin",
    prop="melting_point",
    value_celsius=245.5, value_celsius_min=245.0, value_celsius_max=246.0,
    value_raw="245–246 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Friedelin (5)",
    evidence_quote="Friedelin ( 5 ) White needles; m.p. 245–246 °C (Lit. 246–248 °C)",
    notes="paper 151")
add(
    compound_name="Stigmasterol",
    prop="melting_point",
    value_celsius=156.0, value_celsius_min=155.0, value_celsius_max=157.0,
    value_raw="155–157 °C", relation="=", data_type="measured",
    source=src_151, source_url=url_151,
    evidence_location="Section 3.4 Spectral Data, Stigmasterol (6)",
    evidence_quote="Stigmasterol ( 6 ) White needles; m.p. 155–157 °C (Lit. 168–169 °C)",
    notes="paper 151")

# ---------------- Paper 152: PMC6264337 -----------------
src_152 = "Molecules 2011, 16(10), 8670-8683"
url_152 = "https://doi.org/10.3390/molecules16108670"
add(
    compound_name="1,7-Dithio-4,10,13-trioxocyclopentadecane",
    prop="melting_point",
    value_celsius=63.5, value_celsius_min=63.0, value_celsius_max=64.0,
    value_raw="63–64 °C", relation="=", data_type="measured",
    source=src_152, source_url=url_152,
    evidence_location="Section 3.1.2, compound B3",
    evidence_quote="1,7-Dithio-4,10,13-trioxocyclopentadecane ( B3 ): Starting with diethylene glycol ditosylate (1.75 gr, 4.24 mmol), triethyleneglycoldithiol (1.26 g, 6.99 mmol) and Cs 2 CO 3 (7 g, 21.2 mmol) the title compound (0,88 g, 48%) was obtained as yellow crystal. Melting point: 63–64 °C.",
    notes="paper 152")
add(
    compound_name="1,10-Dithio-4,7,13,16-tetraoxocyclooctadecane",
    prop="melting_point",
    value_celsius=93.5, value_celsius_min=93.0, value_celsius_max=94.0,
    value_raw="93–94 °C", relation="=", data_type="measured",
    source=src_152, source_url=url_152,
    evidence_location="Section 3.1.2, compound B5",
    evidence_quote="When triethyleneglycol dichloride was used, the yield was improved to 38%. Melting point: 93–94 °C.",
    notes="paper 152")

# ---------------- Paper 154: PMC5513518 -----------------
src_154 = "Materials (Basel) 2010, 3(2), 1015-1030"
url_154 = "https://doi.org/10.3390/ma3021015"
add(
    compound_name="Polyethylene (HDPE) from K10/TMA support activator",
    prop="melting_point",
    value_celsius=133.7, value_raw="133.7 °C", relation="=", data_type="measured",
    source=src_154, source_url=url_154,
    evidence_location="Table 3, entry 1 (K10/TMA), Tm column",
    evidence_quote="1 K10/TMA 19,143 133.7",
    notes="paper 154; HDPE obtained via K10/TMA support activator; column header Tm(°C)")
add(
    compound_name="Polyethylene (HDPE) from K10/TEA support activator",
    prop="melting_point",
    value_celsius=133.4, value_raw="133.4 °C", relation="=", data_type="measured",
    source=src_154, source_url=url_154,
    evidence_location="Table 3, entry 2 (K10/TEA), Tm column",
    evidence_quote="2 K10/TEA 7,143 133.4",
    notes="paper 154; HDPE obtained via K10/TEA support activator; column header Tm(°C)")
add(
    compound_name="Polyethylene (HDPE) from K30/TMA support activator",
    prop="melting_point",
    value_celsius=134.0, value_raw="134.0 °C", relation="=", data_type="measured",
    source=src_154, source_url=url_154,
    evidence_location="Table 3, entry 3 (K30/TMA), Tm column",
    evidence_quote="3 K30/TMA 3,857 134.0",
    notes="paper 154; HDPE obtained via K30/TMA support activator; column header Tm(°C)")
add(
    compound_name="Polyethylene (HDPE) from K30/TEA support activator",
    prop="melting_point",
    value_celsius=134.5, value_raw="134.5 °C", relation="=", data_type="measured",
    source=src_154, source_url=url_154,
    evidence_location="Table 3, entry 4 (K30/TEA), Tm column",
    evidence_quote="4 K30/TEA 15,000 134.5",
    notes="paper 154; HDPE obtained via K30/TEA support activator; column header Tm(°C)")

# ---------------- Paper 155: PMC6259158 -----------------
src_155 = "Molecules 2010, 15(10), 6733-6742"
url_155 = "https://doi.org/10.3390/molecules15106733"
add(
    compound_name="Mesuarianone (1,5-dihydroxy-6',6'-dimethylpyrano[2',3':3,4]-6''-(2-methyl-2-pentenyl)-6''-methylpyrano[2'',3'':6,7]-xanthone)",
    prop="melting_point",
    value_celsius=166.5, value_celsius_min=166.0, value_celsius_max=167.0,
    value_raw="166-167 °C", relation="=", data_type="measured",
    source=src_155, source_url=url_155,
    evidence_location="Section 3.4 Spectral Data, Mesuarianone (1)",
    evidence_quote="Mesuarianone ( 1 ). Yellow solid. m.p. 166-167 °C.",
    notes="paper 155")
add(
    compound_name="Mesuasinone (1,6-dihydroxy-2-(3',7'-dimethyl-2',6'-octenyl)-6'',6''-dimethylpyrano-[2'',3'':3,4]-xanthone)",
    prop="melting_point",
    value_celsius=118.5, value_celsius_min=118.0, value_celsius_max=119.0,
    value_raw="118-119 °C", relation="=", data_type="measured",
    source=src_155, source_url=url_155,
    evidence_location="Section 3.4 Spectral Data, Mesuasinone (2)",
    evidence_quote="Mesuasinone ( 2 ). Yellow solid. m.p. 118-119 °C.",
    notes="paper 155")
add(
    compound_name="Stigmasterol",
    prop="melting_point",
    value_celsius=155.5, value_celsius_min=155.0, value_celsius_max=156.0,
    value_raw="155-156 °C", relation="=", data_type="measured",
    source=src_155, source_url=url_155,
    evidence_location="Section 3.4 Spectral Data, Stigmasterol (6)",
    evidence_quote="Stigmasterol ( 6 ). White needles. m.p. 155-156 °C (Lit. 168-169 °C)",
    notes="paper 155")
add(
    compound_name="Friedelin",
    prop="melting_point",
    value_celsius=245.5, value_celsius_min=245.0, value_celsius_max=246.0,
    value_raw="245-246 °C", relation="=", data_type="measured",
    source=src_155, source_url=url_155,
    evidence_location="Section 3.4 Spectral Data, Friedelin (7)",
    evidence_quote="Friedelin ( 7 ). White needles. m.p. 245-246 °C (Lit. 260-263 °C)",
    notes="paper 155")
add(
    compound_name="Betulinic acid",
    prop="melting_point",
    value_celsius=290.5, value_celsius_min=290.0, value_celsius_max=291.0,
    value_raw="290-291 °C", relation="=", data_type="measured",
    source=src_155, source_url=url_155,
    evidence_location="Section 3.4 Spectral Data, Betulinic acid (8)",
    evidence_quote="Betulinic acid ( 8 ). White solid. m.p. 290-291 °C (Lit. 291-292 °C)",
    notes="paper 155")

# ---------------- Paper 156: PMC7123108 -----------------
src_156 = "Biology of Macrofungi 2019; pp 319-349"
url_156 = "https://doi.org/10.1007/978-3-030-02622-6_16"
add(
    compound_name="Cordycepin (3'-Deoxyadenosine)",
    prop="melting_point",
    value_celsius=225.5, value_raw="225.5 °C", relation="=", data_type="measured",
    source=src_156, source_url=url_156,
    evidence_location="Properties table for cordycepin",
    evidence_quote="Molecular formula C 10 H 13 N 5 O 3 Molar mass 251.24 g mol −1 Melting point 225.5 °C, 499 K, 438 °F",
    notes="paper 156; book chapter on Cordycepin properties")

# ---------------- Paper 157: PMC3716435 -----------------
src_157 = "Int J Mol Sci 2007, 8(7), 662-669"
url_157 = "https://doi.org/10.3390/ijms8070662"
# Paper has DOI? Actually let me check - we saw no DOI in nxml, use PMC
src_url_157 = "pmc:PMC3716435"
add(
    compound_name="Dehydrocholic acid",
    prop="melting_point",
    value_celsius=243.0, value_raw="243 °C", relation="=", data_type="measured",
    source=src_157, source_url=src_url_157,
    evidence_location="Table 3, host melting Tm column, clathrate B (1·DMSO)",
    evidence_quote="1 ·DMSO (clathrate B) 15.5 16 155 243 189 −34",
    notes="paper 157; Tm of dehydrocholic acid host after guest release; column header 'Host melting T m °C'")

# ---------------- Paper 158: PMC3783257 -----------------
src_158 = "Mar Drugs 2004, 2(4), 185-191"
url_158 = "pmc:PMC3783257"
add(
    compound_name="Philinopgenin A (16β-acetoxyholosta-9(11),24(25)-diene-3β-ol)",
    prop="melting_point",
    value_celsius=208.5, value_celsius_min=208.5, value_celsius_max=208.5,
    value_raw="208.5–208.5 °C", relation="=", data_type="measured",
    source=src_158, source_url=url_158,
    evidence_location="Spectral Data, Philinopgenin A (1)",
    evidence_quote="Philinopgenin A ( 1 ): a white powder, mp 208.5–208.5 °C;",
    notes="paper 158; source prints identical min and max")
add(
    compound_name="Philinopgenin B (20,25-epoxylanosta-8(9)-ene-3β-ol 18(16)-lactone)",
    prop="melting_point",
    value_celsius=213.0, value_celsius_min=212.5, value_celsius_max=213.5,
    value_raw="212.5–213.5 °C", relation="=", data_type="measured",
    source=src_158, source_url=url_158,
    evidence_location="Spectral Data, Philinopgenin B (2)",
    evidence_quote="Philinopgenin B ( 2 ): a white powder, mp 212.5–213.5°C;",
    notes="paper 158")
add(
    compound_name="Philinopgenin C (16β-acetoxyholosta-8(9),24(25)-diene-3β-ol)",
    prop="melting_point",
    value_celsius=217.0, value_celsius_min=216.5, value_celsius_max=217.5,
    value_raw="216.5–217.5 °C", relation="=", data_type="measured",
    source=src_158, source_url=url_158,
    evidence_location="Spectral Data, Philinopgenin C (3)",
    evidence_quote="Philinopgenin C ( 3 ): a white powder, mp 216.5–217.5 °C;",
    notes="paper 158")

# ---------------- Paper 160: PMC6147103 -----------------
src_160 = "Molecules 2003, 8(11), 780-787"
url_160 = "https://doi.org/10.3390/81100780"
add(
    compound_name="N,N-Bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane",
    prop="melting_point",
    value_celsius=83.0, value_celsius_min=82.0, value_celsius_max=84.0,
    value_raw="82-84°C", relation="=", data_type="measured",
    source=src_160, source_url=url_160,
    evidence_location="Experimental, Synthesis of L via Method C",
    evidence_quote="The resulting solid was crystallised from ethyl acetate to give white crystals (2.5 g, 90%); melting point: 82-84°C",
    notes="paper 160")
add(
    compound_name="[N,N-Bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane](3,5-dimethylpyrazole)copper(II) dinitrate",
    prop="melting_point",
    value_celsius=189.0, value_celsius_min=188.0, value_celsius_max=190.0,
    value_raw="188-190 °C", relation="=", data_type="measured",
    source=src_160, source_url=url_160,
    evidence_location="Experimental, Synthesis of Cu(L)(L0)(NO3)2 complex",
    evidence_quote="Blue crystals formed after a few days, which were filtered and washed with small amounts of cold ethanol and dried in air; melting point: 188-190 °C",
    notes="paper 160")

# ---------------- Paper 161: PMC6146427 -----------------
src_161 = "Molecules 2002, 7(2), 189-199"
url_161 = "https://doi.org/10.3390/70200189"
# Table 1 dec temps for compounds 1-10
dec_data = [
    ("N'-(p-toluenesulfonylphenoxy)carbimidoyl azide", 96, "96"),
    ("N'-(p-toluenesulfonyl-4-methylphenoxy)carbimidoyl azide", 92, "92"),
    ("N'-(p-toluenesulfonyl-2,6-dimethylphenoxy)carbimidoyl azide", 94, "94"),
    ("N'-(p-toluenesulfonyl-4-methoxyphenoxy)carbimidoyl azide", 77, "77"),
    ("N'-(p-toluenesulfonyl)(4-chlorophenoxy)carbimidoyl azide", 98, "98"),
    ("N'-(p-toluenesulfonyl-4-bromophenoxy)carbimidoyl azide", 104, "104"),
    ("N'-(p-toluenesulfonyl-4-nitrophenoxy)carbimidoyl azide", 117, "117"),
    ("N'-(p-toluenesulfonyl-2,4,6-trimethylphenoxy)carbimidoyl azide", 101, "101"),
    ("N'-(mesitylsulfonyl-2,4,6-trimethylphenoxy)carbimidyl azide", 120, "120"),
    ("N'-Cyano-2,4,6-trimethylphenoxycarbimidyl azide", 119, "119"),
]
quotes_161 = [
    "H ( 1 ) 96 6( 1X ) 94",
    "4-CH 3 ( 2 ) 92 4( 2X ) 96",
    "DM f ( 3 ) 94 3( 3X ) 97",
    "4-MeO- ( 4 ) 77 6( 4X ) 94",
    "4-Cl ( 5 ) 98 9( 5X ) 91",
    "4-Br ( 6 ) 104 9( 6X ) 91",
    "4-NO 2 ( 7 ) 117 13( 7X ) 87",
    "TM g ( 8 ) 101 3.5( 8X ) 96.5",
    "TM Z=Ms h ( 9 ) 120 14.3( 9X ) 85.5",
    "TM Z=CN ( 10 ) 119 3.5( 10X ) 96.5",
]
for (name, val, raw), q in zip(dec_data, quotes_161):
    add(compound_name=name,
        prop="decomposition", value_celsius=float(val), value_raw=f"{raw} °C",
        relation="=", data_type="measured", source=src_161, source_url=url_161,
        evidence_location="Table 1, Azide dec. temp. (oC) column",
        evidence_quote=q,
        notes="paper 161; solid-phase decomposition temperature from Table 1; source uses 'oC' for °C")
add(
    compound_name="N-4-(methoxyphenyl)-N'-(4-mesitylsulfonyl)-O-(2,4,6-trimethylphenoxy)isourea",
    prop="melting_point",
    value_celsius=175.5, value_celsius_min=175.0, value_celsius_max=176.0,
    value_raw="175–176 °C", relation="=", data_type="measured",
    source=src_161, source_url=url_161,
    evidence_location="Experimental, characterization of 9P",
    evidence_quote="Crystallization from methanol gave 1.2 g (46%) of N-4-(methoxyphenyl)-N'-(4-mesitylsulfonyl)-O-(2,4,6-trimethylphenoxy)isourea ( 9P ), mp.175-6oC.",
    notes="paper 161; source prints '175-6oC' (175–176 °C)")

# ---------------- Paper 162: PMC5521752 -----------------
src_162 = "Materials (Basel) 2010, 3(6), 3625-3641"
url_162 = "https://doi.org/10.3390/ma3063625"
add(
    compound_name="4-methoxy-2,2,6,6-tetramethyl-1-piperidinyloxyl (MeO-TEMPO)",
    prop="melting_point",
    value_celsius=39.85, value_raw="313 K", relation="=", data_type="measured",
    source=src_162, source_url=url_162,
    evidence_location="Section 3.2 Sample preparation, MeO-TEMPO discussion",
    evidence_quote="Gas adsorption of MeO-TEMPO (melting point 313 K) was carried out according to our previous study",
    conversion_arithmetic="313 K - 273.15 = 39.85 °C",
    notes="paper 162")

# ---------------- Paper 163: PMC6146543 -----------------
src_163 = "Molecules 2002, 7(1), 38-50"
url_163 = "https://doi.org/10.3390/70100038"
add(
    compound_name="Caledonixanthone G",
    prop="melting_point",
    value_celsius=201.0, value_raw="201°C", relation="=", data_type="measured",
    source=src_163, source_url=url_163,
    evidence_location="Spectral Data, Caledonixanthone G (8)",
    evidence_quote="Caledonixanthone G ( 8 ): Isolated as orange prisms (MeOH); melting point 201°C;",
    notes="paper 163")

# ---------------- Paper 164: PMC7158184 -----------------
src_164 = "Pulp and Paper Industry 2015; pp 103-195"
url_164 = "https://doi.org/10.1016/B978-0-12-803409-5.00008-2"
add(
    compound_name="1-Bromo-3-chloro-5,5-dimethylhydantoin (BCDMH)",
    prop="melting_point",
    value_celsius=161.0, value_celsius_min=159.0, value_celsius_max=163.0,
    value_raw="159–163 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section on BCDMH (1-bromo-3-chloro-5,5-dimethylhydantoin)",
    evidence_quote="It is a white crystalline compound slightly soluble in water having a melting point of 159–163 °C",
    notes="paper 164; sentence attribution ambiguous between BCDMH and 1,3-dichloro-5,5-dimethylhydantoin; paragraph context describes BCDMH")
add(
    compound_name="Chlorine dioxide",
    prop="melting_point",
    value_celsius=-59.0, value_raw="−59 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Table 8.8 Physical properties of chlorine dioxide",
    evidence_quote="Melting point of −59 °C Boiling point of 11 °C",
    notes="paper 164")
add(
    compound_name="Chlorine dioxide",
    prop="boiling_point",
    value_celsius=11.0, value_raw="11 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Table 8.8 Physical properties of chlorine dioxide",
    evidence_quote="Melting point of −59 °C Boiling point of 11 °C",
    notes="paper 164")
add(
    compound_name="Glutaraldehyde (1,5-Pentanedial)",
    prop="melting_point",
    value_celsius=-14.0, value_raw="−14 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.9 Glutaraldehyde",
    evidence_quote="It is miscible with water and having melting and boiling points −14 °C and 187 °C, respectively.",
    notes="paper 164")
add(
    compound_name="Glutaraldehyde (1,5-Pentanedial)",
    prop="boiling_point",
    value_celsius=187.0, value_raw="187 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.9 Glutaraldehyde",
    evidence_quote="It is miscible with water and having melting and boiling points −14 °C and 187 °C, respectively.",
    notes="paper 164")
add(
    compound_name="Bronopol (2-Bromo-2-nitropropane-1,3-diol)",
    prop="melting_point",
    value_celsius=130.0, value_raw="about 130 °C", relation="~", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.10 Bronopol",
    evidence_quote="Bronopol (2-bromo-2-nitropropane-1,3-diol) is a white crystalline odorless substance melting at about 130 °C.",
    notes="paper 164")
add(
    compound_name="2,2-Dibromo-3-nitrilopropionamide (DBNPA)",
    prop="melting_point",
    value_celsius=124.5, value_raw="124.5 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.12 DBNPA",
    evidence_quote="It is a white crystalline powder having melting point of 124.5 °C, water solubility 15,000 mg/L at 20 °C",
    notes="paper 164")
add(
    compound_name="Dazomet (3,5-dimethyl-1,3,5-2H-tetrahydrothiadiazine-2-thione)",
    prop="melting_point",
    value_celsius=104.5, value_celsius_min=104.0, value_celsius_max=105.0,
    value_raw="104–105 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section on Dazomet",
    evidence_quote="It has a melting point of 104–105 °C, flash point 156 °C,",
    notes="paper 164")
add(
    compound_name="2-(thiocyanomethylthio)benzothiazole (TCMTB)",
    prop="boiling_point",
    value_celsius=120.0, value_raw=">120 °C", relation=">", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.16 TCMTB",
    evidence_quote="It has low aqueous solubility having boiling point: >120 °C, melting point: <−10 °C",
    notes="paper 164")
add(
    compound_name="2-(thiocyanomethylthio)benzothiazole (TCMTB)",
    prop="melting_point",
    value_celsius=-10.0, value_raw="<−10 °C", relation="<", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Section 8.3.16 TCMTB",
    evidence_quote="It has low aqueous solubility having boiling point: >120 °C, melting point: <−10 °C",
    notes="paper 164")
add(
    compound_name="50% aqueous glutaraldehyde",
    prop="boiling_point",
    value_celsius=100.5, value_raw="100.5 °C", relation="=", data_type="measured",
    source=src_164, source_url=url_164,
    evidence_location="Table 8.14 Physical properties of 50% aqueous glutaraldehyde",
    evidence_quote="Boiling point 100.5 °C Freezing point −21 °C",
    notes="paper 164; aqueous solution (50%), not pure compound")

# ---------------- Paper 165: PMC6236387 -----------------
src_165 = "Molecules 2001, 6(3), 279-286"
url_165 = "https://doi.org/10.3390/60300279"
add(
    compound_name="Anthraquinone",
    prop="melting_point",
    value_celsius=284.0, value_raw="284 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, Anthraquinone",
    evidence_quote="Anthraquinone : mp 284°;",
    notes="paper 165; source prints '284°', interpreted as °C")
add(
    compound_name="Anthrone",
    prop="melting_point",
    value_celsius=152.0, value_raw="152 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, Anthrone",
    evidence_quote="Anthrone : mp 152°;",
    notes="paper 165; source prints '152°', interpreted as °C")
add(
    compound_name="2-Methoxyanthraquinone",
    prop="melting_point",
    value_celsius=196.0, value_raw="196 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, 2-Methoxyanthraquinone",
    evidence_quote="2-Methoxyanthraquinone : mp 196°;",
    notes="paper 165; source prints '196°', interpreted as °C")
add(
    compound_name="2-Chloroanthraquinone",
    prop="melting_point",
    value_celsius=209.0, value_raw="209 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, 2-Chloroanthraquinone",
    evidence_quote="2-Chloroanthraquinone: mp 209°;",
    notes="paper 165; source prints '209°', interpreted as °C")
add(
    compound_name="1-Tetralone",
    prop="boiling_point",
    value_celsius=119.0, value_celsius_min=118.0, value_celsius_max=120.0,
    value_raw="118–120 °C (at 8 mmHg)", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, 1-Tetralone",
    evidence_quote="1-Tetralone : bp 118-120°/8 mm.;",
    notes="paper 165; bp measured at reduced pressure (8 mmHg), not standard atmospheric pressure")
add(
    compound_name="1-Indanone",
    prop="melting_point",
    value_celsius=40.0, value_raw="40 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, 1-Indanone",
    evidence_quote="1-Indanone : mp 40°C;",
    notes="paper 165")
add(
    compound_name="2-Coumaranone",
    prop="melting_point",
    value_celsius=49.0, value_raw="49 °C", relation="=", data_type="measured",
    source=src_165, source_url=url_165,
    evidence_location="Spectral Data, 2-Coumaranone",
    evidence_quote="2-Coumaranone : mp 49°;",
    notes="paper 165; source prints '49°', interpreted as °C")

# ---------------- Paper 166: PMC5445842 -----------------
src_166 = "Materials (Basel) 2010, 3(4), 2772-2800"
url_166 = "https://doi.org/10.3390/ma3042772"
add(
    compound_name="6,13-bis(1-naphthyl)pentacene",
    prop="melting_point",
    value_celsius=272.0, value_raw="272 °C", relation="=", data_type="measured",
    source=src_166, source_url=url_166,
    evidence_location="Discussion of compounds 50–51 (Figure 6)",
    evidence_quote="The 1-naphthyl isomer 50 had a higher melting point (272 °C) compared to the 2-naphthyl isomer 51 (160 °C)",
    notes="paper 166; review compiling mp from cited literature")
add(
    compound_name="6,13-bis(2-naphthyl)pentacene",
    prop="melting_point",
    value_celsius=160.0, value_raw="160 °C", relation="=", data_type="measured",
    source=src_166, source_url=url_166,
    evidence_location="Discussion of compounds 50–51 (Figure 6)",
    evidence_quote="The 1-naphthyl isomer 50 had a higher melting point (272 °C) compared to the 2-naphthyl isomer 51 (160 °C)",
    notes="paper 166; review compiling mp from cited literature")
add(
    compound_name="6,13-bis(triisopropylsilylethynyl)pentacene (TIPS-pentacene)",
    prop="decomposition",
    value_celsius=265.0, value_raw="265 °C", relation="=", data_type="measured",
    source=src_166, source_url=url_166,
    evidence_location="Table 2, compound 1 row, T_d (DSC)/°C column",
    evidence_quote="T d (DSC)/°C 1 328 643 – 649 0.15 1.84 – 265",
    notes="paper 166; decomposition temperature determined by DSC; column header T_d (DSC)/°C")

# ---------------- WRITE CSV -----------------
with open("/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_06.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows")

#!/usr/bin/env python3
"""Build batch_05.csv from manually-extracted data."""
import csv

import os
OUT = "/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial3-full-opus47/batch_05.csv"
if not os.path.isdir(os.path.dirname(OUT)):
    OUT = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_05.csv"

cols = ["id","verification_status","compound_name","compound_smiles","property",
        "value_celsius","value_celsius_min","value_celsius_max","value_raw",
        "relation","data_type","source","source_url","evidence_location",
        "evidence_quote","conversion_arithmetic","notes"]

rows = []
i = 0

def midpoint(lo, hi):
    return (lo + hi) / 2.0

def add(compound, prop, v_c, vmin, vmax, v_raw, relation, data_type, source, url, loc, quote, conv="", notes=""):
    global i
    i += 1
    rows.append({
        "id": f"b05-{i:03d}",
        "verification_status": "pending_verification",
        "compound_name": compound,
        "compound_smiles": "",
        "property": prop,
        "value_celsius": v_c,
        "value_celsius_min": vmin,
        "value_celsius_max": vmax,
        "value_raw": v_raw,
        "relation": relation,
        "data_type": data_type,
        "source": source,
        "source_url": url,
        "evidence_location": loc,
        "evidence_quote": quote,
        "conversion_arithmetic": conv,
        "notes": notes,
    })

# ============== Paper 149: SNMICON 2024 Abstracts ==============
src149 = "Indian J Nucl Med 2024 39(Suppl 1) S1-S97"
url149 = "pmc:PMC11831906"
add("Mebrofenin","melting_point",205,"","","205 °C","=","measured",src149,url149,
    "Abstract (radiopharmaceutical synthesis section)",
    "FT-IR, ¹H, and ¹³C NMR spectra confirmed the structure of Mebrofenin (melting point: 205oC)",
    "","radiopharmaceutical synthesis abstract")
add("Mannose triflate","melting_point",119,118,120,"118–120 °C","=","measured",src149,url149,
    "Abstract (radiopharmaceutical synthesis section)",
    "mass spectral analysis confirmed the structure of Mannose triflate (melting point: 118 – 120oC)",
    "","radiopharmaceutical synthesis abstract")
add("L,L-EC","melting_point",228.5,225,232,"225–232 °C","=","measured",src149,url149,
    "Abstract (radiopharmaceutical synthesis section)",
    "Characteristic IR spectra confirmed the structure of L, L-EC (melting point: 225-232 oC)",
    "","L,L-ethylenedicysteine")

# ============== Paper 151: Soulattri pyranoxanthone ==============
src151 = "Molecules 2011 16(5) 3999-4004"
url151 = "https://doi.org/10.3390/molecules16053999"
add("Soulattrin","melting_point",180.5,180,181,"180–181 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Soulattrin (1)",
    "Soulattrin ( 1 ) Yellow crystals; m.p. 180–181 °C",
    "","new pyranoxanthone (1)")
add("Caloxanthone B","melting_point",157.5,157,158,"157–158 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Caloxanthone B (2)",
    "Caloxanthone B ( 2 ) Yellow needles; m.p. 157–158 °C",
    "","known xanthone (2)")
add("Caloxanthone C","melting_point",211,210,212,"210–212 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Caloxanthone C (3)",
    "Caloxanthone C ( 3 ) Yellow needles; m.p. 210–212 °C",
    "","known xanthone (3)")
add("Macluraxanthone","melting_point",181.5,181,182,"181–182 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Macluraxanthone (4)",
    "Macluraxanthone ( 4 ) Yellow needles; m.p. 181–182 °C",
    "","known xanthone (4)")
add("Friedelin","melting_point",245.5,245,246,"245–246 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Friedelin (5)",
    "Friedelin ( 5 ) White needles; m.p. 245–246 °C",
    "","triterpene (5)")
add("Stigmasterol","melting_point",156,155,157,"155–157 °C","=","measured",src151,url151,
    "Section 3.4 Spectral Data, Stigmasterol (6)",
    "Stigmasterol ( 6 ) White needles; m.p. 155–157 °C",
    "","steroid (6); lit. value 168-169 °C")

# ============== Paper 152: Thio-Oxocrown Ethers ==============
src152 = "Molecules 2011 16(10) 8670"
url152 = "https://doi.org/10.3390/molecules16108670"
add("1,7-Dithio-4,10,13-trioxocyclopentadecane (B3)","melting_point",63.5,63,64,"63–64 °C","=","measured",src152,url152,
    "Experimental synthesis of B3",
    "1,7-Dithio-4,10,13-trioxocyclopentadecane ( B3 ): Starting with diethylene glycol ditosylate (1.75 gr, 4.24 mmol), triethyleneglycoldithiol (1.26 g, 6.99 mmol) and Cs 2 CO 3 (7 g, 21.2 mmol) the title compound (0,88 g, 48%) was obtained as yellow crystal. Melting point: 63–64 °C",
    "","thio-oxocrown ether B3")
add("1,10-Dithio-4,7,13,16-tetraoxocyclooctadecane (B5)","melting_point",93.5,93,94,"93–94 °C","=","measured",src152,url152,
    "Experimental synthesis of B5",
    "1,10-Dithio-4,7,13,16-tetraoxocyclooctadecane ( B5 ): Starting with triethyleneglycol ditosylate (2.91 g, 6.36 mmol), triethyleneglycol dithiol (1.26 g, 6.99 mmol) and Cs 2 CO 3 (10.30 g, 31.8 mmol) the title compound (0.27 g, 14 %) was obtained as a yellowish solid. When triethyleneglycol dichloride was used, the yield was improved to 38%. Melting point: 93–94 °C",
    "","thio-oxocrown ether B5")

# ============== Paper 153: Organo-niobate Ionic Liquids ==============
src153 = "Int J Mol Sci 2007 8(5) 392-398"
url153 = "pmc:PMC3692303"
# Paper 153 ionic mixture rows DROPPED:
# Table 1 cells are tightly packed numeric grids without compound name in
# contiguous span — quotes either need ellipsis (forbidden) or numbers alone
# (no compound token). Per protocol drop bare codes. The mixtures are
# identified only by composition mol%.

# ============== Paper 155: Pyranoxanthones from Mesua beccariana ==============
src155 = "Molecules 2010 15(10) 6733-6742"
url155 = "https://doi.org/10.3390/molecules15106733"
add("Mesuarianone","melting_point",166.5,166,167,"166-167 °C","=","measured",src155,url155,
    "Section 3.4 Spectral Data, Mesuarianone (1)",
    "Mesuarianone ( 1 ). Yellow solid. m.p. 166-167 °C",
    "","new pyranoxanthone (1)")
add("Mesuasinone","melting_point",118.5,118,119,"118-119 °C","=","measured",src155,url155,
    "Section 3.4 Spectral Data, Mesuasinone (2)",
    "Mesuasinone ( 2 ). Yellow solid. m.p. 118-119 °C",
    "","new pyranoxanthone (2)")
add("Stigmasterol","melting_point",155.5,155,156,"155-156 °C","=","measured",src155,url155,
    "Section 3.4 Spectral Data, Stigmasterol (6)",
    "Stigmasterol ( 6 ). White needles. m.p. 155-156 °C",
    "","steroid (6); lit. 168-169 °C")
add("Friedelin","melting_point",245.5,245,246,"245-246 °C","=","measured",src155,url155,
    "Section 3.4 Spectral Data, Friedelin (7)",
    "Friedelin ( 7 ). White needles. m.p. 245-246 °C",
    "","triterpene (7); lit. 260-263 °C")
add("Betulinic acid","melting_point",290.5,290,291,"290-291 °C","=","measured",src155,url155,
    "Section 3.4 Spectral Data, Betulinic acid (8)",
    "Betulinic acid ( 8 ). White solid. m.p. 290-291 °C",
    "","(8); lit. 291-292 °C")

# ============== Paper 156: Cordycepin ==============
src156 = "Biology of Macrofungi 2019 319-349"
url156 = "pmc:PMC7123108"
add("Cordycepin (3'-Deoxyadenosine)","melting_point",225.5,"","","225.5 °C","=","measured",src156,url156,
    "Table 16.1 Cordycepin molecular information",
    "Fig. 16.1 Molecular structure of adenosine, deoxyadenosine and cordycepin (3′-deoxyadenosine) Table 16.1 Cordycepin molecular information Name IUPAC name 9-(3-Deoxy-β-D-ribofuranosyl)adenine Other names Cordycepine, 3′-Deoxyadenosine Identifiers CAS number 73–03-3 PubChem 6303 ChemSpider 6064 ChEMBL CHEMBL305686 InChlKey OFEZSBMBBKLLBJ- Properties Molecular formula C 10 H 13 N 5 O 3 Molar mass 251.24 g mol −1 Melting point 225.5 °C, 499 K, 438 °F",
    "",
    "reference table for cordycepin; book chapter; 499 K and 438 °F also given as conversions")

# ============== Paper 157: Dehydrocholic acid clathrates ==============
src157 = "Int J Mol Sci 2007 8(7) 662-669"
url157 = "pmc:PMC3716435"
add("Dehydrocholic acid (1·0.5 acetone clathrate A, host)","melting_point",244,"","","244","=","measured",src157,url157,
    "Table 3",
    "1 ·0.5 AC (clathrate A) 6.0 6.7 86.2 244",
    "","host melting Tm after guest release; host = dehydrocholic acid (1)")
add("Dehydrocholic acid (1·DMSO clathrate B, host)","melting_point",243,"","","243","=","measured",src157,url157,
    "Table 3",
    "1 ·DMSO (clathrate B) 15.5 16 155 243",
    "","host melting Tm after guest release; host = dehydrocholic acid (1)")
add("Dehydrocholic acid (1·0.9 NMP clathrate C, host)","melting_point",243,"","","243","=","measured",src157,url157,
    "Table 3",
    "1 ·0.9 NMP (clathrate C); 18.5 18.3 160 243",
    "","host melting Tm after guest release; host = dehydrocholic acid (1)")
add("Dehydrocholic acid (1·0.83 DMF clathrate D, host)","melting_point",244,"","","244","=","measured",src157,url157,
    "Table 3",
    "1 ·0.83 DMF (clathrate D) 5.44 13.1 122 244",
    "","host melting Tm after guest release; host = dehydrocholic acid (1)")

# ============== Paper 158: Philinopgenins ==============
src158 = "Mar Drugs 2004 2(4) 185-191"
url158 = "pmc:PMC3783257"
add("Philinopgenin A","melting_point",208.5,"","","208.5–208.5 °C","=","measured",src158,url158,
    "Spectral Data, Philinopgenin A (1)",
    "Philinopgenin A ( 1 ): a white powder, mp 208.5–208.5 °C",
    "","apparent typo in paper; single value 208.5 reported as range")
add("Philinopgenin B","melting_point",213,212.5,213.5,"212.5–213.5°C","=","measured",src158,url158,
    "Spectral Data, Philinopgenin B (2)",
    "Philinopgenin B ( 2 ): a white powder, mp 212.5–213.5°C",
    "","new triterpenoid aglycone (2)")
add("Philinopgenin C","melting_point",217,216.5,217.5,"216.5–217.5 °C","=","measured",src158,url158,
    "Spectral Data, Philinopgenin C (3)",
    "Philinopgenin C ( 3 ): a white powder, mp 216.5–217.5 °C",
    "","new triterpenoid aglycone (3)")

# ============== Paper 160: Pyrazolylmethyl aminoethane / Cu complex ==============
src160 = "Molecules 2003 8(11) 780-787"
url160 = "https://doi.org/10.3390/81100780"
add("N,N-Bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane","melting_point",83,82,84,"82-84°C","=","measured",src160,url160,
    "Experimental synthesis section (Method C)",
    "Synthesis of [N,N-bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane] using Method C. A mixture of 1-hydroxymethyl-3,5-dimethylpyrazole (2.52 g, 20 mmol) and aminoethanol (0.61g, 10 mmol) was introduced into a Pyrex tube, which was then placed in a microwave reactor and irradiated with microwaves (60W) in the absence of solvent for 20 min. The reaction mixture was extracted with dichloromethane and washed with water to eliminate the residual ethanolamine. The organic solution was dried and the solvent was removed under reduced pressure. The resulting solid was crystallised from ethyl acetate to give white crystals (2.5 g, 90%); melting point: 82-84°C (ethyl acetate)",
    "","tridentate ligand (L)")
add("[N,N-Bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane](3,5-dimethylpyrazole) copper(II) dinitrate","melting_point",189,188,190,"188-190 °C","=","measured",src160,url160,
    "Experimental synthesis section, copper(II) complex",
    "Synthesis of [N,N-Bis(3,5-dimethylpyrazol-1-ylmethyl)-1-hydroxy-2-aminoethane](3,5dimethyl-pyrazole) copper(II) dinitrate The copper(II) complex was prepared by the addition of a solution of tridentate ligand (0.277 g; 1mmol) in ethanol (3 mL) to a solution of copper(II) dinitrate [Cu(NO 3 ) 2 ·3H 2 O] (0.2415 g, 1mmol) in ethanol (3 mL). The resulting solution was filtered and allowed to stand at 25°C. Blue crystals formed after a few days, which were filtered and washed with small amounts of cold ethanol and dried in air; melting point: 188-190 °C (ethanol)",
    "","Cu(II) complex")

# ============== Paper 161: Imidoyl azides decomposition temps ==============
src161 = "Molecules 2002 7(2) 189-199"
url161 = "https://doi.org/10.3390/70200189"
# Y = H, 4-CH3, DM=2,6-Me2, 4-MeO, 4-Cl, 4-Br, 4-NO2, TM=2,4,6-Me3, TM(Z=Ms), TM(Z=CN)
imid = [
    ("Imidoyl azide 1 (Y=H, Z=Tosyl)",96,"96","H ( 1 ) 96 6( 1X )"),
    ("Imidoyl azide 2 (Y=4-CH3, Z=Tosyl)",92,"92","4-CH 3 ( 2 ) 92 4( 2X )"),
    ("Imidoyl azide 3 (Y=DM=2,6-Dimethyl, Z=Tosyl)",94,"94","DM f ( 3 ) 94 3( 3X )"),
    ("Imidoyl azide 4 (Y=4-MeO, Z=Tosyl)",77,"77","4-MeO- ( 4 ) 77 6( 4X )"),
    ("Imidoyl azide 5 (Y=4-Cl, Z=Tosyl)",98,"98","4-Cl ( 5 ) 98 9( 5X )"),
    ("Imidoyl azide 6 (Y=4-Br, Z=Tosyl)",104,"104","4-Br ( 6 ) 104 9( 6X )"),
    ("Imidoyl azide 7 (Y=4-NO2, Z=Tosyl)",117,"117","4-NO 2 ( 7 ) 117 13( 7X )"),
    ("Imidoyl azide 8 (Y=TM=2,4,6-Trimethyl, Z=Tosyl)",101,"101","TM g ( 8 ) 101 3.5( 8X )"),
    ("Imidoyl azide 9 (Y=TM, Z=Ms=Mesitylsulfonyl)",120,"120","TM Z=Ms h ( 9 ) 120 14.3( 9X )"),
    ("Imidoyl azide 10 (Y=TM, Z=CN)",119,"119","TM Z=CN ( 10 ) 119 3.5( 10X )"),
]
for name, tc, raw, marker in imid:
    add(name,"decomposition",tc,"","",f"{raw} °C","=","measured",src161,url161,
        f"Table 1 row Y={marker.split('(')[0].strip()}",
        marker,
        "","Table 1: column 'Azide dec. temp. (oC)'; decomposition temperature as solid (capillary mp tube)")

# ============== Paper 162: MeO-TEMPO ==============
src162 = "Materials (Basel) 2010 3(6) 3625-3641"
url162 = "https://doi.org/10.3390/ma3063625"
# 313 K = 39.85 °C
add("4-Methoxy-2,2,6,6-tetramethylpiperidine-1-oxyl (MeO-TEMPO)","melting_point",39.85,"","","313 K","=","measured",src162,url162,
    "Section on TPP/MeO-TEMPO IC preparation",
    "Gas adsorption of MeO-TEMPO (melting point 313 K)",
    "313 K - 273.15 = 39.85 °C",
    "value from previous study cited [24]")

# ============== Paper 163: Caledonixanthone G ==============
src163 = "Molecules 2002 7(1) 38-50"
url163 = "https://doi.org/10.3390/70100038"
add("Caledonixanthone G","melting_point",201,"","","201°C","=","measured",src163,url163,
    "Experimental, Caledonixanthone G (8)",
    "Caledonixanthone G ( 8 ): Isolated as orange prisms (MeOH); melting point 201°C",
    "","new xanthone derivative")

# ============== Paper 164: Microbiological problems (book chapter) ==============
src164 = "Pulp and Paper Industry 2015 103-195"
url164 = "pmc:PMC7158184"
add("1,3-Dichloro-5,5-dimethylhydantoin","melting_point",161,159,163,"159–163 °C","=","measured",src164,url164,
    "Section on disinfectant compounds",
    "It is a white crystalline compound slightly soluble in water having a melting point of 159–163 °C, 1,3-dichloro-5,5-dimethylhydantoin",
    "","cited from Rao et al. 2002; book chapter reference value")
add("Chlorine dioxide","melting_point",-59,"","","−59 °C","=","measured",src164,url164,
    "Table 8.8 Physical properties of chlorine dioxide",
    "Figure 8.4 Structure of chlorine dioxide. Table 8.8 Physical properties of chlorine dioxide Molecular weight of 67.45 Gas at normal temperatures and pressures Melting point of −59 °C Boiling point of 11 °C",
    "","reference table value")
add("Chlorine dioxide","boiling_point",11,"","","11 °C","=","measured",src164,url164,
    "Table 8.8 Physical properties of chlorine dioxide",
    "Figure 8.4 Structure of chlorine dioxide. Table 8.8 Physical properties of chlorine dioxide Molecular weight of 67.45 Gas at normal temperatures and pressures Melting point of −59 °C Boiling point of 11 °C",
    "","reference table value")
add("Glutaraldehyde (1,5-pentanedial)","melting_point",-14,"","","−14 °C","=","measured",src164,url164,
    "Section 8.3.9 Glutaraldehyde",
    "Glutaraldehyde is an amber-colored liquid usually supplied in solutions of acidic pH. As with other aldehydes, the two aldehyde groups react readily under suitable conditions, particularly with proteins. It is miscible with water and having melting and boiling points −14 °C and 187 °C, respectively",
    "","review-cited physical property")
add("Glutaraldehyde (1,5-pentanedial)","boiling_point",187,"","","187 °C","=","measured",src164,url164,
    "Section 8.3.9 Glutaraldehyde",
    "Glutaraldehyde is an amber-colored liquid usually supplied in solutions of acidic pH. As with other aldehydes, the two aldehyde groups react readily under suitable conditions, particularly with proteins. It is miscible with water and having melting and boiling points −14 °C and 187 °C, respectively",
    "","review-cited physical property")

# ============== Paper 165: Pyrophosphoryl chloride intramolecular acylation ==============
src165 = "Molecules 2001 6(3) 279-286"
url165 = "https://doi.org/10.3390/60300279"
add("Anthraquinone","melting_point",284,"","","284 °C","=","measured",src165,url165,
    "Spectral Data, Anthraquinone",
    "Anthraquinone : mp 284°",
    "","°C implied")
add("Anthrone","melting_point",152,"","","152 °C","=","measured",src165,url165,
    "Spectral Data, Anthrone",
    "Anthrone : mp 152°",
    "","°C implied")
add("2-Methoxyanthraquinone","melting_point",196,"","","196 °C","=","measured",src165,url165,
    "Spectral Data, 2-Methoxyanthraquinone",
    "2-Methoxyanthraquinone : mp 196°",
    "","°C implied")
add("2-Chloroanthraquinone","melting_point",209,"","","209 °C","=","measured",src165,url165,
    "Spectral Data, 2-Chloroanthraquinone",
    "2-Chloroanthraquinone: mp 209°",
    "","°C implied")
add("1-Indanone","melting_point",40,"","","40°C","=","measured",src165,url165,
    "Spectral Data, 1-Indanone",
    "1-Indanone : mp 40°C",
    "")
add("2-Coumaranone","melting_point",49,"","","49 °C","=","measured",src165,url165,
    "Spectral Data, 2-Coumaranone",
    "2-Coumaranone : mp 49°",
    "","°C implied")

# ============== Paper 168: Marine natural products review ==============
src168 = "Mar Drugs 2005 3(2) 36-63"
url168 = "pmc:PMC3756327"
add("Sulfolane","melting_point",28,"","","28 °C","=","measured",src168,url168,
    "Section on Friedel-Crafts alkylation",
    "Sulfolane is a polar aprotic solvent that is chemically and thermally stable, miscible with water and organic solvents, and does not damage PS. Therefore, it is an ideal solvent for performing many different reactions on the surface of PS plates, although its relatively high melting point (28 °C) introduces some difficulties in handling",
    "","review-cited physical property")

# ============== Paper 169: Indole-pyrazolone 1,2,3-triazoles ==============
src169 = "ACS Bio Med Chem Au 2025 5(1) 66-77"
url169 = "https://doi.org/10.1021/acsbiomedchemau.4c00060"
trz = [
    ("4-((1-((1-(2-Bromobenzyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5a)",179,178,180,"178–180 °C","5a"),
    ("4-((1-((1-(2-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5b)",190,180,200,"180–200 °C","5b"),
    ("4-((1-((1-(3-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5c)",190,180,200,"180–200 °C","5c"),
    ("4-((1-((1-(4-Chlorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5d)",179,178,180,"178–180 °C","5d"),
    ("5-Methyl-4-((1-((1-(2-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5e)",241,240,242,"240–242 °C","5e"),
    ("5-Methyl-4-((1-((1-(3-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5f)",211,210,212,"210–212 °C","5f"),
    ("5-Methyl-4-((1-((1-(4-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5g)",151,150,152,"150–152 °C","5g"),
    ("5-Methyl-2-phenyl-4-((1-((1-(o-tolyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one (5h)",221,220,222,"220–222 °C","5h"),
    ("4-((1-((1-(2-Methoxyphenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5i)",231,230,232,"230–232 °C","5i"),
    ("4-((1-((1-(3,4-Dimethylphenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5j)",209,208,210,"208–210 °C","5j"),
    ("4-((1-((1-Benzyl-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5k)",211,210,212,"210–212 °C","5k"),
    ("4-((3-((3-Methyl-5-oxo-1-phenyl-1,5-dihydro-4H-pyrazol-4-ylidene)methyl)-1H-indol-1-yl)methyl)-1H-1,2,3-triazol-1-yl butyrate (5l)",205,200,210,"200–210 °C","5l"),
    ("5-Methyl-2-phenyl-4-((1-((1-(2,4,5-trifluorophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one (5m)",201,200,202,"200–202 °C","5m"),
    ("5-Methyl-2-phenyl-4-((1-((1-(2,4,6-tribromophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2,4-dihydro-3H-pyrazol-3-one (5n)",201,200,202,"200–202 °C","5n"),
    ("5-Methyl-4-((1-((1-(2-methyl-5-nitrophenyl)-1H-1,2,3-triazol-4-yl)methyl)-1H-indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3H-pyrazol-3-one (5o)",211,210,212,"210–212 °C","5o"),
]
quotes169 = {
"5a":"4-((1-((1-(2-Bromobenzyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5a ) Yellow solid (0.390 g, 97%), mp: 178–180 °C",
"5b":"4-((1-((1-(2-Chlorophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5b ) Yellow solid (0.414 g, 95%), mp: 180–200 °C",
"5c":"4-((1-((1-(3-Chlorophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5c ) Yellow solid (0.410 g, 94%), mp: 180–200 °C",
"5d":"4-((1-((1-(4-Chlorophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5d ) Yellow solid (0.391 g, 90%), mp: 178–180 °C",
"5e":"5-Methyl-4-((1-((1-(2-nitrophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5e ) Yellow solid (0.392 g, 88%), mp: 240–242 °C",
"5f":"5-Methyl-4-((1-((1-(3-nitrophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5f ) Yellow solid (0.384 g, 86%), mp: 210–212 °C",
"5g":"5-Methyl-4-((1-((1-(4-nitrophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5g ) Yellow solid (0.401 g, 90%), mp: 150–152 °C",
"5h":"5-Methyl-2-phenyl-4-((1-((1-(o-tolyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2,4-dihydro-3 H -pyrazol-3-one ( 5h ) Yellow solid (0.358 g, 83%), mp: 220–222 °C",
"5i":"4-((1-((1-(2-Methoxyphenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5i ) Yellow solid (0.375 g, 87%), mp: 230–232 °C",
"5j":"4-((1-((1-(3,4-Dimethylphenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5j ) Yellow solid (0.361 g, 84%), mp: 208–210 °C",
"5k":"4-((1-((1-Benzyl-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-5-methyl-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5k ) Yellow solid (0.379 g, 90%), mp: 210–212 °C",
"5l":"4-((3-((3-Methyl-5-oxo-1-phenyl-1,5-dihydro-4 H -pyrazol-4-ylidene)methyl)-1 H -indol-1-yl)methyl)-1 H -1,2,3-triazol-1-yl butyrate ( 5l ) Yellow solid (0.438 g, 93%), mp: 200–210 °C",
"5m":"5-Methyl-2-phenyl-4-((1-((1-(2,4,5-trifluorophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2,4-dihydro-3 H -pyrazol-3-one ( 5m ) Yellow solid (0.380 g, 91%), mp: 200–202 °C",
"5n":"5-Methyl-2-phenyl-4-((1-((1-(2,4,6-tribromophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2,4-dihydro-3 H -pyrazol-3-one ( 5n ) Yellow solid (0.366 g, 89%), mp: 200–202 °C",
"5o":"5-Methyl-4-((1-((1-(2-methyl-5-nitrophenyl)-1 H -1,2,3-triazol-4-yl)methyl)-1 H -indol-3-yl)methylene)-2-phenyl-2,4-dihydro-3 H -pyrazol-3-one ( 5o ) Yellow solid (0.405 g, 89%), mp: 210–212 °C",
}
for name, tc, vmin, vmax, raw, code in trz:
    add(name,"melting_point",tc,vmin,vmax,raw,"=","measured",src169,url169,
        f"Experimental section, compound {code}",
        quotes169[code],
        "",f"triazole-indole-pyrazolone derivative ({code})")

# Write CSV
with open(OUT,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"Wrote {len(rows)} rows to {OUT}")

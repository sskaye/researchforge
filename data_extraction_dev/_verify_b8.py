#!/usr/bin/env python3
"""Batch verifier for batch 8 rows."""
import re, unicodedata, json, os, sys

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in [('–', '-'), ('—', '-'), ('‐', '-'), ('‑', '-'), ('−', '-'), ('­', ''), ('°', '°')]:
        s = s.replace(a, b)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s

BASE = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev'

def load_paper(path):
    full = os.path.join(BASE, path)
    texts = []
    if os.path.isdir(full):
        for fn in ('article_text.txt', 'article.nxml'):
            p = os.path.join(full, fn)
            if os.path.exists(p):
                texts.append(open(p, encoding='utf-8', errors='ignore').read())
        # Also look for HTML/text alternatives
        for f in os.listdir(full):
            if f.endswith('.html') or f.endswith('.txt') or f.endswith('.nxml'):
                fp = os.path.join(full, f)
                if fp not in [os.path.join(full,'article_text.txt'), os.path.join(full,'article.nxml')]:
                    try:
                        texts.append(open(fp, encoding='utf-8', errors='ignore').read())
                    except: pass
        return '\n'.join(texts) if texts else None
    if os.path.exists(full):
        return open(full, encoding='utf-8', errors='ignore').read()
    return None

ROWS = [
    # (id, paper_path_or_tmp, doi_or_id_to_check, evidence_quote, value_raw_check, compound_substr, notes)
    ("1825", "corpora/full_168/organic_synthesis/khalifa_2024_thiopyrimidine_sulfonamide.html", "10.3390/molecules29194778", "White powder, mp 245–247 °C, 613 mg, 84%", "245-247", "Thiomorpholinosulfonyl"),
    ("271", "corpora/full_168/013_PMC12943095_Original_Synthesis_of_Substituted_6H-Benzocchromene_Derivatives_Using_a_TDAE_and_Pd-Cataly", "PMC12943095", "8-fluoro-6-(4-nitrobenzyl)-6 H -benzo[ c ]chromene ( 5g ). Yield: 80%; Mp: 132 °C;", "132", "5g"),
    ("141", "corpora/full_168/004_PMC13084458_Piperazine-Thiourea_Hybrids_as_Novel_Antiplatelet_Agents_Targeting_COX-1_Synthesis_in_Vitr", "PMC13084458", "N-Benzyl-4-(2-chlorophenyl)­piperazine-1-carbothioamide (3j) White solid; 111.40 °C;", "111.40", "3j"),
    ("1528", "/tmp/kim.txt", "5c13222", "6-(Trifluoromethyl)quinolin-2(1H)-one (2h). A white solid; m.p. = 195-196 °C.", "195-196", "2h"),
    ("530", "corpora/full_168/035_PMC6259131_Convenient_Synthesis_and_Antimicrobial_Activity_of_Some_Novel_Amino_Acid_Coupled_Triazoles", "PMC6259131", "Colorless crystals (0.26 g, 56 %); mp 73-74 °C", "73-74", "10b"),
    ("1426", "corpora/full_168/178_PMC11208899_CopperVit_B3_MOF_preparation_characterization_and_catalytic_evaluation_in_a_one-pot_synthe", "PMC11208899", "White solid; Rf = 0.60 (8:2 petroleum ether/EtOAc); mp = 180–182 °C", "180-182", "4h"),
    ("128", "corpora/full_168/003_PMC12943044_Design_and_Biological_Evaluation_of_Mannich-Modified_8-HydroxyquinolinePhthalimide_Hybrids", "PMC12943044", "2-(8-Hydroxy-7-((4-methylpiperazin-1-yl)methyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 8b ) Brown powder (25 mg, 60% yield); m.p. 221–225 °C;", "221-225", "8b"),
    ("1271", "corpora/full_168/138_PMC6146434_Annellation_of_Triazole_and_Tetrazole_Systems_onto_Pyrrolo23-dpyrimidines_Synthesis_of_Tet", "PMC6146434", "1-Phenyl-N-ethoxymethylene-2-amino-3-cyano-4-(4-methoxyphenyl)pyrrole ( 6b ): Yield: 72 %; mp: 159-60°C", "159-60", "6b"),
    ("1838", "/tmp/ledermann.txt", "bjoc.19.99", "compound 5r (207 mg, 43%) was isolated as a yellow solid, Mp 133.6 °C, Rf (n-", "133.6", "5r"),
    ("1502", "/tmp/huang.txt", "10.3390/molecules31030494", "(Sp)-2,2′-(1,4(1,4)-dibenzenacyclohexaphane-12,43-diyl)diphenol [(Sp)-2a]. White solid (940 mg, 80% yield); M.p. 218-219 °C", "218-219", "2a"),
    ("379", "corpora/full_168/023_PMC9790764_Synthesis_and_Properties_of_13-Disubstituted_Ureas_and_Their_Isosteric_Analogs_Containing_", "PMC9790764", "Yield 0.153 g (63%), mp 143.5 °C", "143.5", "4c"),
    ("1619", None, "10.4103/japtr.JAPTR_70_17", "Piroxicam-Nicotinamide ... 162-165", "162-165", "Piroxicam-Nicotinamide"),
    ("1717", "corpora/full_168/materials_inorganic", "10.3390/nano14131077", "Na3 PO4 ·12H2 O         65–69       190", "65-69", "Na3PO4"),
    ("181", "corpora/full_168/006_PMC13006720_Exploring_Novel_Nitrofuryl134ThiadiazoleBased_Derivatives_Design_Synthesis_and_Evaluation_", "PMC13006720", "( 17 ): Orange solid, mp 276°C–279°C.", "276-279", "17"),
    ("1739", "corpora/full_168/measurement_prediction", "10.3390/ma13204486", "Dodecane              112-40-3       Paraffin      209.14 ± 1.45   −10.2 ± 0.94     −8 ± 0.25", "-8", "dodecane"),
    ("1368", "corpora/full_168/169_PMC11843341_Antimicrobial_Efficacy_of_123-Triazole-Incorporated_Indole-Pyrazolone_against_Drug-Resista", "PMC11843341", "Yellow solid (0.380 g, 91%), mp: 200–202 °C", "200-202", "5m"),
    ("30", "corpora/full_168", "jm3014162", "white solid (mp 132-133", "132-133", "8b"),
    ("552", "corpora/full_168/036_PMC6193216_Synthesis_of_Chromenoimidazoles_Annulated_with_an_Azaindole_Moiety_through_a_Base-Promoted", "PMC6193216", "mp >300 °C", ">300", "7b"),
    ("334", "corpora/full_168/020_PMC11206691_N-Hydroxypiridinedione_A_Privileged_Heterocycle_for_Targeting_the_HBV_RNase_H", "PMC11206691", "White solid (150.5 mg, 86%). R f = 0.53 (CH 2 Cl 2 ), m.p. 165-168 °C", "165-168", "9"),
    ("681", "corpora/full_168/053_PMC6147013_Synthesis_of_Novel_3H-Quinazolin-4-ones_Containing_Pyrazolinone_Pyrazole_and_Pyrimidinone_", "PMC6147013", "3-{[4-(2-Methyl-4-oxo-4H-quinazolin-3-yl)phenyl]hydrazono}-pentane-2,4-dione ( 8a ). Pale yellow crystals; yield 2.17 g (60 %); M.p. 153-155 o C", "153-155", "8a"),
    ("1527", "/tmp/kim.txt", "5c13222", "6-Chloroquinolin-2(1H)-one (2g). A white solid; m.p. = 264-265 °C.", "264-265", "2g"),
    ("206", "corpora/full_168/011_PMC12943719_Discovery_of_Potent_PDE4_Inhibitors_with_32H-Pyridazinone_Scaffold_Synthesis_In_Silico_Stu", "PMC12943719", "5-Acetyl-2-ethyl-4-(3-hydroxyphenylamino)-6-phenylpyridazin-3(2H)-one, 2h Yield = 22%; mp = 185–187 °C (EtOH);", "185-187", "2h"),
    ("129", "corpora/full_168/003_PMC12943044_Design_and_Biological_Evaluation_of_Mannich-Modified_8-HydroxyquinolinePhthalimide_Hybrids", "PMC12943044", "2-(8-Hydroxy-7-(morpholinomethyl)quinolin-5-yl)-4-methoxyisoindoline-1,3-dione ( 8c ) Brown powder (30 mg, 72% yield); m.p. 222–225 °C;", "222-225", "8c"),
    ("211", "corpora/full_168/011_PMC12943719_Discovery_of_Potent_PDE4_Inhibitors_with_32H-Pyridazinone_Scaffold_Synthesis_In_Silico_Stu", "PMC12943719", "5-Acetyl-2-ethyl-4-(4-methoxyphenylamino)-6-phenylpyridazin-3(2H)-one, 2m Yield = 67%; mp = 161–162 °C (EtOH);", "161-162", "2m"),
    ("1193", "corpora/full_168/123_PMC12941058_Design_Synthesis_Antiproliferative_Potency_and_In_Silico_Studies_of_Novel_Alkynyl_Quinazol", "PMC12941058", "to give iodo compound 2 (17.7 g, 84%). Rf = 0.21 (Hexane/EtOAc, 1:4) and mp (dec.): 219–221 °C.", "219-221", "2"),
]

for rid, path, doi_id, quote, val, comp in ROWS:
    if path is None:
        print(f'ROW {rid}: NO_PATH')
        continue
    if path.startswith('/tmp/'):
        try:
            with open(path) as f:
                txt = f.read()
        except:
            txt = None
    else:
        txt = load_paper(path)
    if txt is None:
        print(f'ROW {rid}: NO_TEXT path={path}')
        continue
    nt = norm(txt)
    nq = norm(quote)
    quote_in = nq in nt
    doi_in = doi_id.lower() in nt.lower() if doi_id else True
    val_in = norm(val) in nq
    print(f'ROW {rid}: doi_in_paper={doi_in} quote_present={quote_in} val_in_quote={val_in}')
    if not quote_in:
        # find partial
        head = nq[:50]
        idx = nt.find(head)
        print(f'   q-head idx={idx}')
        if idx > 0:
            print('   context:', repr(nt[idx:idx+len(nq)+50]))

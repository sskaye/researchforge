"""Scan remaining batch 5 papers (057-063) for compound-specific mp/bp values."""
import os, re, json

ROOT = "/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set"
papers = [
    "057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learning_for_Thermophysical_Property_Prediction_A_Cas",
    "058_PMC4702524_How_accurately_can_we_predict_the_melting_points_of_drug-like_compounds",
    "059_PMC8122861_Group_Contribution_Estimation_of_Ionic_Liquid_Melting_Points_Critical_Evaluation_and_Refin",
    "060_PMC4724158_The_development_of_models_to_predict_melting_and_pyrolysis_point_data_associated_with_seve",
    "061_PMC2603525_Simultaneous_feature_selection_and_parameter_optimisation_using_an_artificial_ant_colony_c",
    "062_PMC3127127_A_Quantitative_Structure-Property_Relationship_QSPR_Study_of_aliphatic_alcohols_by_the_met",
    "063_PMC12004525_Understanding_Conformation_Importance_in_Data-Driven_Property_Prediction_Models.",
]

for p in papers:
    path = os.path.join(ROOT, p, "article_text.txt")
    if not os.path.exists(path):
        print(f"!!! missing {path}")
        continue
    with open(path) as f:
        t = f.read()
    nxml_path = os.path.join(ROOT, p, "article.nxml")
    nxml = open(nxml_path).read() if os.path.exists(nxml_path) else ""
    doi_m = re.search(r'<article-id pub-id-type="doi">([^<]+)</article-id>', nxml)
    pmc_m = re.search(r'<article-id pub-id-type="pmc">([^<]+)</article-id>', nxml)
    pmid_m = re.search(r'<article-id pub-id-type="pmid">([^<]+)</article-id>', nxml)
    print(f"=== {p[:60]} ===")
    print(f"  DOI: {doi_m.group(1) if doi_m else '-'}, PMC: {pmc_m.group(1) if pmc_m else '-'}, PMID: {pmid_m.group(1) if pmid_m else '-'}")
    print(f"  chars: {len(t)}")
    # Count mp/bp mentions
    mp_count = len(re.findall(r'[Mm]elt(?:ing)?\s*[Pp]oint|m\.?p\.?\b|Tm\b|Tfus', t))
    bp_count = len(re.findall(r'[Bb]oil(?:ing)?\s*[Pp]oint|b\.?p\.?\b|Tb\b|NBP', t))
    print(f"  mp_mentions: {mp_count}, bp_mentions: {bp_count}")
    # Look for compound-value patterns
    pats = [
        (r'M\.?[Pp]\.?\s*[:=]?\s*\d+(?:[.,-]\d+)?\s*°?C', 'mp_C'),
        (r'\d+(?:\.\d+)?\s*°C', 'celsius'),
        (r'\d+(?:\.\d+)?\s*K\b', 'kelvin_temp'),
        (r'[Tt][bm]\s*=\s*\d', 'Tb_Tm_eq'),
    ]
    for pat, name in pats:
        hits = re.findall(pat, t)
        if hits:
            print(f"  {name} hits: {len(hits)}, sample: {hits[:3]}")

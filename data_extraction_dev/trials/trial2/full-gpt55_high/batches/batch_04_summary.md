# Batch 04 mp/bp Extraction Summary

Scope: only papers listed in `batch_04.csv`.

Output CSV: `Trial2-full-gpt55_high/batches/batch_04_extracted.csv`

Rows extracted: 63

Flagged rows: 0

Verification status: all rows are `pending_verification`. Phase 3 deterministic checks passed; Phase 4 independent fresh-context verification has not been run.

Phase 3 command:

```bash
python3 /Users/skaye/.codex/skills/mp-bp-extraction/scripts/run_all_checks.py /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial2-full-gpt55_high/batches/batch_04_extracted.csv --paper-root /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp_bp_full_set --out /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial2-full-gpt55_high/batches/batch_04_flags.csv
```

Phase 3 result: required fields, CSV quoting, compound-name validation, value range, unit arithmetic, DOI lookup, evidence quote lookup, and within-paper deduplication all passed.

## Per-Paper Notes

- `005_PMC12987641_Synthesis_Biological_Evaluation_and_Theoretical_Study_of_Indenoquinolinylphosphine_Oxide_D`: 12 melting-point rows extracted for indenoquinolinylphosphine oxide derivatives 9a-9m.
- `013_PMC12943095_Original_Synthesis_of_Substituted_6H-Benzocchromene_Derivatives_Using_a_TDAE_and_Pd-Cataly`: 8 melting-point rows extracted for benzo[c]chromene products 5a-5h.
- `022_PMC9764318_CaIO32_nanoparticles_fabrication_and_application_as_an_eco-friendly_and_recyclable_catalys`: no rows added; candidate table uses product codes/structures without full compound names in the text snippet reviewed.
- `031_PMC6193241_Revision_of_the_Structure_and_Total_Synthesis_of_Topsentin_C`: 6 melting-point rows extracted, including nitrovinyl indole intermediates and Topsentin C.
- `039_PMC6263281_Synthesis_of_Ginkgolic_Acid_Analogues_and_Evaluation_of_Their_Molluscicidal_Activity`: 5 melting-point rows extracted for ethyl 6-methylsalicylate and selected ginkgolic acid analogues.
- `047_PMC6146789_Synthesis_and_Theoretical_Study_of_a_New_Type_of_Pentacyclic_bis-Benzothiazolium_Compound`: 2 decomposition rows extracted.
- `055_PMC3685236_Antiproliferative_Activity_of_-Hydroxy--Arylalkanoic_Acids`: 4 boiling-point rows and 1 melting-point row extracted.
- `063_PMC12004525_Understanding_Conformation_Importance_in_Data-Driven_Property_Prediction_Models.`: no rows added; candidate content was dataset/model-level melting-point discussion rather than directly extractable compound rows in the reviewed text.
- `073_PMC13085778_Donoracceptor_dichotomy_in_novel_Schiff_bases_comprehensive_spectroscopic_and_DFT_investig`: 3 table melting-point rows extracted for Schiff base compounds I-III; compound names are formula-plus-table-label because the table uses roman-numeral identities.
- `082_PMC7332229_Azaphenantherene_derivatives_as_inhibitor_of_SARS_CoV-2_Mpro_Synthesis_physicochemical_qua`: no rows added; candidate preparation text had identity/substituent ambiguity, so rows were dropped.
- `091_PMC3685385_Sulfonium-based_Ionic_Liquids_Incorporating_the_Allyl_Functionality`: 1 melting-point row extracted for `[C2Allylsul][Br]`.
- `099_PMC6236343_7-1-AcetoxymethylideneBenzonorbornadiene_A_Versatile_Reagent_for_the_Synthesis_of_7-Formyl`: no rows added in this conservative partial pass; candidate stereochemical derivative rows need slower identity verification.
- `113_PMC13103808_Comparative_Antinociceptive_Evaluation_of_Hofmeisterin_I_and_Analogues_from_Hofmeisteria_s`: no rows added in this conservative partial pass; many candidates were intermediates with repeated code labels requiring slower reconciliation.
- `121_PMC12985495_Spectroscopic_Studies_of_6-Membered_Lipoic_Acid_Derivative_123-Trithiane-4-pentanoic_Acid_`: 1 melting-point row extracted for trisulfur lipoic acid.
- `129_PMC6146463_Reactivity_of_3-Ethoxycarbonyl_Isoquinolinium_Salts_Towards_Various_Nucleophilic_Reagents_`: 4 melting-point rows extracted.
- `138_PMC6146434_Annellation_of_Triazole_and_Tetrazole_Systems_onto_Pyrrolo23-dpyrimidines_Synthesis_of_Tet`: no rows added in this conservative partial pass; many extractable-looking rows remain but need full row-by-row review because of dense repeated heterocycle series.
- `149_PMC11831906_SNMICON_2024_Abstracts`: 3 melting-point rows extracted from the abstract result paragraph.
- `158_PMC3783257_Philinopgenin_A_B_and_C_Three_New_Triterpenoid_Aglycones_from_the_Sea_Cucumber_Pentacta_qu`: 3 melting-point rows extracted for Philinopgenins A-C.
- `167_PMC3002819_Posters_PDD_PMS_PNM_PPAT_POT`: no rows added; reviewed candidates were mostly formulation/polymer thermal-analysis context rather than clean compound mp/bp rows.
- `175_PMC11206905_Synthesis_and_Photophysical_Characterization_of_Fluorescent_Naphtho23-dthiazole-49-Diones_`: 5 melting-point rows extracted.
- `183_PMC9007260_Synthesis_and_Antimicrobial_Antiplatelet_and_Anticoagulant_Activities_of_New_Isatin_Deivat`: 5 melting/decomposition rows extracted.
- `materials_inorganic/liu_2023_alsife_phases_alloys`: no rows added in this partial pass.
- `measurement_prediction/berg_2015_apparatus-vapor-pressure`: no rows added in this partial pass.
- `measurement_prediction/rolka_2021_medium-temp-pcm-thistory`: no rows added in this partial pass.
- `organic_synthesis/kim_2026_2quinolone_synthesis`: no rows added in this partial pass.
- `organic_synthesis/yanovich_2024_spiroheterocycles_rh_catalysis`: no rows added in this partial pass.
- `pharma_cocrystals/khan_2017_piroxicam_cocrystal`: no rows added in this partial pass.

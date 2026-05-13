# Batch 06 mp/bp extraction summary

Output: `batch_06_extracted.csv`

Phase 3 checks:

- Command: `python3 /Users/skaye/.codex/skills/mp-bp-extraction/scripts/run_all_checks.py /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial2-full-gpt55_high/batches/batch_06_extracted.csv --paper-root /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp_bp_full_set --out /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial2-full-gpt55_high/batches/batch_06_flags.csv`
- Result: passed. Required fields, CSV quote lint, compound-name check, value-range check, unit-conversion check, DOI verification, evidence-quote verification, and within-paper dedup all exited 0.
- Phase 4 independent verification was not performed in this single-agent pass, so rows remain `pending_verification`.

Per-paper notes:

- `007_PMC13093257_From_in_silico_and_machine_learning_model_to_validation_discovery_of_novel_amide-functiona`: 1 row extracted for 2-(3-nitrophenyl)imidazo[1,2-a]pyridine.
- `015_PMC12943364_Dual_Inhibition_of_PB2_and_JAK2_for_Influenza_A_Strategy_Combining_Antiviral_and_Host-Dire`: 5 rows extracted for PB01-PB05 melting points.
- `024_PMC10113129_Computational_Drug_Designing_Synthesis_Characterization_and_Anti-bacterial_Activity_Evalua`: no rows in this partial. Candidate text found general method/high-melting discussion only; no row-level value was extracted.
- `033_PMC7148931_Synthesis_and_antimicrobial_activity_of_novel_quinazolinonethiazolidinequinoline_compounds`: 14 rows extracted for intermediates III/IV and V1-V12.
- `041_PMC6146472_Synthesis_of_Some_Aldoxime_Derivatives_of_4H-Pyran-4-ones`: 6 rows extracted for pyranone derivatives 2a, 2b, 3a, 3b, 6a, and 7a.
- `049_PMC6147017_Synthesis_of_New_Pyrazole_and_Pyrimidine_Steroidal_Derivatives`: 8 rows extracted for steroidal derivatives 2, 3a, 3b, and 4a-4e.
- `057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learning_for_Thermophysical_Property_Prediction_A_Cas`: no rows in this partial. Boiling-point content appears dataset/model-oriented and was not reduced to individual compound rows here.
- `067_PMC6146921_Total_and_Local_Quadratic_Indices_of_the_Molecular_Pseudographs_Atom_Adjacency_Matrix_Appl`: no rows in this partial. Prediction/QSPR content deferred.
- `075_PMC12937307_Design_Synthesis_Spectral_Structural_Analysis_and_Biological_Evaluation_of_Novel_Pyrazole_`: no rows in this partial.
- `084_PMC5445742_Synthesis_of_Aryliron_Complexes_CpFeCO2Ar_by_Palladium-Catalyzed_Reactions_of_CpFeCO2I_wit`: no rows in this partial.
- `093_PMC6146903_Syntheses_of_New_Unsymmetrical_Symmetrical_Diaryl-sulphides_Diarylsulphones_Containing_Thi`: no rows in this partial.
- `103_PMC6146533_A_Simple_Synthesis_of_Some_New_Thienopyridine_and_Thieno-pyrimidine_Derivatives`: no rows in this partial.
- `115_PMC13083104_Formal_organocatalytic_fluoronitromethane_addition_to_tetrahydroisoquinolines_through_a_CD`: no rows in this partial.
- `123_PMC12941058_Design_Synthesis_Antiproliferative_Potency_and_In_Silico_Studies_of_Novel_Alkynyl_Quinazol`: no rows in this partial.
- `131_PMC6146477_Synthesis_of_6-Methoxy-1-oxaspiro45deca-69-diene-8-one`: no rows in this partial.
- `141_PMC6236399_Tyrian_Purple_66-Dibromoindigo_and_Related_Compounds`: no rows in this partial.
- `152_PMC6264337_Synthesis_Metal_Ion_Complexation_and_Computational_Studies_of_Thio_Oxocrown_Ethers`: no rows in this partial.
- `161_PMC6146427_Functionalization_of_Phenyl_Rings_by_Imidoylnitrenes._3_The_Effects_of_Resonance_Steric_an`: no rows in this partial.
- `169_PMC11843341_Antimicrobial_Efficacy_of_123-Triazole-Incorporated_Indole-Pyrazolone_against_Drug-Resista`: 15 rows extracted for compounds 5a-5o.
- `177_PMC11206731_Synthesis_of_a_New_Class_of_-Carbonyl_Selenides_Functionalized_with_Ester_Groups_with_Anti`: 2 rows extracted for selenobenzoates 12 and 13.
- `materials_inorganic/elbeih_2022_an_negdn_energetic_composite`: no rows in this partial. Listed as paired file; local HTML was a Europe PMC shell and local `pdftotext` was unavailable.
- `materials_inorganic/longley_2021_il_zif8_melting_mof`: no rows in this partial. Listed as paired file; local HTML was not suitable for row extraction and local `pdftotext` was unavailable.
- `measurement_prediction/mital_2021_il-melting-group-contribution`: no rows in this partial. Listed as paired file; model/table extraction deferred.
- `organic_synthesis/alsayari_2021_pyrazolothiazole_antimicrobial`: no rows in this partial. Listed as paired file; local HTML was not suitable for row extraction and local `pdftotext` was unavailable.
- `organic_synthesis/nakanishi_2024_pyridine_ch_arylation`: no rows in this partial. HTML contained an extractable mp for 2a, but paired-file sources are not handled by the Phase 3 paper-root quote verifier, so it was deferred.
- `pharma_cocrystals/bock_2024_cardarine_polymorphs`: no rows in this partial. Listed as paired file; local HTML was a Europe PMC shell and local `pdftotext` was unavailable.
- `pharma_cocrystals/lee_2021_ginsenoside_K_polymorphs`: no rows in this partial. Listed as paired file; local HTML was a Europe PMC shell and local `pdftotext` was unavailable.

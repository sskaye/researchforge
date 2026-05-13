# Extraction notes — Phase 6 end-to-end run

- Adapter: `mp_bp`
- Input: `/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_dev_set`
- Verifier prompt SHA-256: `55edff7c09beef1fa57a137bf1080d5972f7b3c2dacc1cb8f9b8f2fc503412c1`
- Seed: `20260511`
- Accept threshold: `0.98`

**Status: ACCEPTED**  
Pass rate: **1.0000** (50/50)

## Pipeline funnel

| Stage | Kept | Notes |
|---|---:|---|
| Phase 4 emit | 410 | skipped 1415 |
| Phase 5a validate_row | 410 | dropped 0 |
| Phase 5e delivered | 410 | quarantined 0 |

## Verification

- audited: **50**
- pass: **50**, fail: **0**, error: **0**
- sanity rate: 1.00

## Sampling

- random_frac: 0.15, min_pool: 30
- total rows: 410
- stratified: 166, random: 62, top_up: 0
- audit pool size: **50**

## Coverage warnings (5)

- `056_PMC12395778_AI-powered_prediction_of_critical_properties_and_boiling_points_a_hybrid_ensemble_learning` — silent_miss_abstract_mentions_property: Abstract mentions property keywords but no candidates were enumerated. Check ingestion and find_candidates.
- `056_PMC12395778_AI-powered_prediction_of_critical_properties_and_boiling_points_a_hybrid_ensemble_learning` — property_table_zero_candidates: Table 'Table 4' headers/caption mention property keywords but no candidates were enumerated for the paper.
- `056_PMC12395778_AI-powered_prediction_of_critical_properties_and_boiling_points_a_hybrid_ensemble_learning` — abstract_claim_far_above_actual: Abstract claims 150 compounds but emitted+skipped = 0 (0 % of claim).
- `058_PMC4702524_How_accurately_can_we_predict_the_melting_points_of_drug-like_compounds` — abstract_claim_far_above_actual: Abstract claims 706 compounds but emitted+skipped = 18 (3 % of claim).
- `064_PMC8697427_Thermodynamic_properties_of_active_pharmaceutical_ingredients_that_are_of_interest_in_COVI` — abstract_claim_far_above_actual: Abstract claims 3510 compounds but emitted+skipped = 66 (2 % of claim).

## Per-article summary

| Article | Candidates | Kept | Skipped |
|---|---:|---:|---:|
| 010_PMC12940417_Targeting_TRPA1_with_Novel_Synthetic_Compoun | 31 | 29 | 2 |
| 011_PMC12943719_Discovery_of_Potent_PDE4_Inhibitors_with_32H | 55 | 52 | 3 |
| 013_PMC12943095_Original_Synthesis_of_Substituted_6H-Benzocc | 34 | 34 | 0 |
| 017_PMC10673250_Exploring_Alkyl_Ester_Salts_of_L-Amino_Acid_ | 12 | 9 | 3 |
| 020_PMC11206691_N-Hydroxypiridinedione_A_Privileged_Heterocy | 39 | 29 | 10 |
| 026_PMC8332001_Synthesis_of_novel_seco-acyclo-N-diazolyl-thi | 5 | 3 | 2 |
| 028_PMC10671214_Diastereoselective_Synthesis_of_DispiroImida | 35 | 34 | 1 |
| 050_PMC6146942_Synthesis_Biological_Evaluation_of_Quinazolin | 21 | 16 | 5 |
| 056_PMC12395778_AI-powered_prediction_of_critical_properties | 0 | 0 | 0 |
| 058_PMC4702524_How_accurately_can_we_predict_the_melting_poi | 18 | 0 | 18 |
| 064_PMC8697427_Thermodynamic_properties_of_active_pharmaceut | 66 | 46 | 20 |
| 138_PMC6146434_Annellation_of_Triazole_and_Tetrazole_Systems | 81 | 27 | 54 |
| 141_PMC6236399_Tyrian_Purple_66-Dibromoindigo_and_Related_Co | 15 | 2 | 13 |
| 157_PMC3716435_Inclusion_Compounds_of_Dehydrocholic_Acid_wit | 14 | 0 | 14 |
| 164_PMC7158184_The_Control_of_Microbiological_Problems | 29 | 2 | 27 |
| 178_PMC11208899_CopperVit_B3_MOF_preparation_characterizatio | 13 | 13 | 0 |
| 2008_Mitchell_Why Are Some Properties More Difficult To Pred | 143 | 0 | 143 |
| 2009_Dearden_Quantitative structure‐property relationships f | 810 | 73 | 737 |
| 2011_Krossing_Is Universal, Simple Melting Point Prediction  | 394 | 36 | 358 |
| 2014_Schmittel_A one-pot multistep cyclization yielding thia | 10 | 5 | 5 |

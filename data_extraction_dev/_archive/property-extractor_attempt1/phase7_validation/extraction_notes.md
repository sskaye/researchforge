# Extraction notes — Phase 6 end-to-end run

- Adapter: `mp_bp`
- Input: `/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_val_set`
- Verifier prompt SHA-256: `55edff7c09beef1fa57a137bf1080d5972f7b3c2dacc1cb8f9b8f2fc503412c1`
- Seed: `20260511`
- Accept threshold: `0.98`

**Status: ACCEPTED**  
Pass rate: **1.0000** (50/50)

## Pipeline funnel

| Stage | Kept | Notes |
|---|---:|---|
| Phase 4 emit | 139 | skipped 599 |
| Phase 5a validate_row | 139 | dropped 0 |
| Phase 5e delivered | 139 | quarantined 0 |

## Verification

- audited: **50**
- pass: **50**, fail: **0**, error: **0**
- sanity rate: 1.00

## Sampling

- random_frac: 0.15, min_pool: 30
- total rows: 139
- stratified: 31, random: 21, top_up: 0
- audit pool size: **50**

## Coverage warnings (0)


## Per-article summary

| Article | Candidates | Kept | Skipped |
|---|---:|---:|---:|
| 004_PMC13084458_Piperazine-Thiourea_Hybrids_as_Novel_Antipla | 0 | 0 | 0 |
| 023_PMC9790764_Synthesis_and_Properties_of_13-Disubstituted_ | 19 | 9 | 10 |
| 029_PMC9486790_Synthesis_and_pesticidal_activity_of_new_134- | 16 | 3 | 13 |
| 031_PMC6193241_Revision_of_the_Structure_and_Total_Synthesis | 14 | 13 | 1 |
| 057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learnin | 0 | 0 | 0 |
| 060_PMC4724158_The_development_of_models_to_predict_melting_ | 17 | 4 | 13 |
| 078_PMC10763787_New_bis-isoxazole_with_monoterpenic_skeleton | 6 | 2 | 4 |
| 096_PMC6236427_Synthesis_of_the_Aspidosperma_Alkaloid_Na-For | 13 | 5 | 8 |
| 098_PMC6146883_Microwave_Assisted_Synthesis_Part_1_Rapid_Sol | 27 | 7 | 20 |
| 102_PMC6236359_Synthesis_and_Electrophilic_Substitution_of_P | 16 | 14 | 2 |
| 113_PMC13103808_Comparative_Antinociceptive_Evaluation_of_Ho | 13 | 3 | 10 |
| 143_PMC6147071_Novel_4-Aroyl-3-alkoxy-25H-furanones_as_Precu | 22 | 0 | 22 |
| 151_PMC6263260_A_New_Pyranoxanthone_from_Calophyllum_soulatt | 7 | 0 | 7 |
| alsayari_2021_pyrazolothiazole_antimicrobial | 1 | 0 | 1 |
| berg_2015_apparatus-vapor-pressure | 2 | 0 | 2 |
| chen_2024_carbon_hydrated_salt_pcm | 0 | 0 | 0 |
| dichi_2025_polyphenols_thermal | 143 | 5 | 138 |
| fernandes_2018_pyridazine_suzuki | 0 | 0 | 0 |
| khalifa_2024_thiopyrimidine_sulfonamide | 182 | 46 | 136 |
| khan_2017_piroxicam_cocrystal | 2 | 0 | 2 |
| ledermann_2023_iodoindoles_synthesis | 40 | 16 | 24 |
| liu_2023_alsife_phases_alloys | 97 | 2 | 95 |
| longley_2021_il_zif8_melting_mof | 1 | 0 | 1 |
| nakanishi_2024_pyridine_ch_arylation | 100 | 10 | 90 |
| pachernegg_2024_20-ils-physicochemical | 0 | 0 | 0 |
| weng_2020_itraconazole_terephthalic_cocrystal | 0 | 0 | 0 |

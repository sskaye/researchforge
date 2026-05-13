# Batch 07 extraction summary

Total rows emitted: 142

Phase 3 checks:
- CSV/value/name/unit/dedup checks passed with `run_all_checks.py` (no `--paper-root`).
- With `--paper-root`, all indexed PMC-paper rows were repaired to quote-locating form; the only remaining deterministic failures are rows 137-142 from `organic_synthesis/diaba_2024_dichlorolactams_synthesis`, because that assigned paper is a paired HTML/PDF file rather than a paper subdirectory indexed by the checker.

- `008_PMC12944436_Rational_Design_Synthesis_and_Molecular_Docking_of_Novel_Terpene_Analogues_of_Imatinib_and`: 9 rows, 0 flagged. 6a-i terpene analogue melting points.
- `124_PMC11844072_Novel_56-dichlorobenzimidazole_derivatives_as_dual_BRAFWT_and_BRAFV600E_inhibitors_design_`: 19 rows, 0 flagged. benzimidazole derivative melting points.
- `170_PMC11843339_Design_and_Synthesis_of_Mycophenolic_Acid_Analogues_for_Osteosarcoma_Cancer_Treatment`: 9 rows, 0 flagged. mycophenolic-acid analogue melting points.
- `178_PMC11208899_CopperVit_B3_MOF_preparation_characterization_and_catalytic_evaluation_in_a_one-pot_synthe`: 3 rows, 0 flagged. new benzoxanthenone derivative melting points.
- `017_PMC10673250_Exploring_Alkyl_Ester_Salts_of_L-Amino_Acid_Derivatives_of_Ibuprofen_Physicochemical_Chara`: 33 rows, 0 flagged. Table 2 Tonset/Tmax/Tm; Tg skipped.
- `026_PMC8332001_Synthesis_of_novel_seco-acyclo-N-diazolyl-thione_nucleosides_analogous_derived_from_acetic`: 5 rows, 0 flagged. named precursor/ligand melting points; metal complexes skipped as bare codes.
- `034_PMC6259447_Synthesis_of_New_Racemic_-Diaminocarboxylic_Ester_Derivatives`: 11 rows, 0 flagged. N-alkylation product melting points.
- `086_PMC6146888_Synthesis_and_Bioactivity_of_a-Aminophosphonates_Containing_Fluorine`: 16 rows, 0 flagged. α-aminophosphonate melting points.
- `142_PMC6146502_Synthesis_Crystal_Structure_and_Conformation_of_Methyl_5-O-acetyl-5-cyano-6-deoxy-23-O-iso`: 2 rows, 0 flagged. gulofuranoside melting points.
- `050_PMC6146942_Synthesis_Biological_Evaluation_of_Quinazoline-4-thiones`: 18 rows, 0 flagged. Table 1 quinazoline-thione melting points.
- `068_PMC12986465_Synthesis_Characterization_and_Bioactivity_Investigation_of_Novel_Benzimidazole_Derivative`: 3 rows, 0 flagged. named starting compounds only; coded series skipped.
- `133_PMC6146437_Synthesis_of_New_Active_Sulfones_in_the_5-Nitroimidazole_Series`: 3 rows, 0 flagged. sulfone/nitroimidazole melting points.
- `153_PMC3692303_Organo-niobate_Ionic_Liquids_Synthesis_Characterization_and_Application_as_Acid_Catalyst_i`: 4 rows, 0 flagged. ionic mixture melting points.
- `162_PMC5521752_Preparation_and_Characterization_of_New_Inclusion_Compounds_Using_Stable_Nitroxide_Radical`: 1 rows, 0 flagged. MeO-TEMPO melting point converted from K.
- `organic_synthesis/diaba_2024_dichlorolactams_synthesis`: 6 rows, 0 flagged. HTML characterization melting points.

## Skipped / no emitted rows
- `042_PMC6146455_Synthesis_of_Novel_Quinazoline_Derivatives_via_Pyrimidine_ortho-Quinodimethane`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `058_PMC4702524_How_accurately_can_we_predict_the_melting_points_of_drug-like_compounds`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `076_PMC11152677_Highly_efficient_CdSCeO2Ag3PO4_nanocomposite_as_novel_heterogenous_catalyst_for_Knoevenage`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `094_PMC6146461_Synthesis_of_Heterocyclic_Skeletons_by_the_Reaction_of_N1-2-Cyanophenyl-benzimidoyl_Chlori`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `104_PMC6146923_Synthesis_and_X-ray_Crystal_Structure_of_Meso-557121214-hexamethyl-14811-tetraazacyclotetr`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `116_PMC12986091_Structural_Elucidation_of_Azo_and_Quinoneimine_Products_Formed_in_Diazonium-Based_Color_Re`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `materials_inorganic/gemini_2023_il_surfactants_cu2o`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `materials_inorganic/ma_2021_dftnan`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `measurement_prediction/muller_2020_dsc-tga-pcm-thermophysical`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `organic_synthesis/norouzi_2024_pyrrole_fused_benzazepine`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `pharma_cocrystals/chmielewska_2020_API_fatty_alcohol_eutectic`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).
- `pharma_cocrystals/liu_2024_matrine_salts_thermal`: no reliable row emitted from readable text; skipped rather than guessing (no compound-bound value, bare-code/figure-only data, prediction summary only, or paired PDF text unavailable without pdftotext).

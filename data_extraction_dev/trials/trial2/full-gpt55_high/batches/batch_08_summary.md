# Batch 08 mp/bp extraction summary

Total rows emitted: 166

All emitted rows have `verification_status=pending_verification`; no rows were marked `flagged_review` in the CSV. Rows include `paper_key=<manifest key>` in notes.

## Per-paper row counts

- `009_PMC12943507_Design_and_Synthesis_of_4-Arylazo_Pyrazole_Carboxamides_as_Dual_AChEBChE_Inhibitors_Kineti`: 13
- `018_PMC10672206_Graphene_OxideCholesterol-Substituted_Zinc_Phthalocyanine_Composites_with_Enhanced_Photody`: 2
- `027_PMC9188358_Efficient_One-Pot_Synthesis_of_Indolhydroxy_Derivatives_Catalyzed_by_SnCl2_DFT_Calculation`: 7
- `035_PMC6259131_Convenient_Synthesis_and_Antimicrobial_Activity_of_Some_Novel_Amino_Acid_Coupled_Triazoles`: 18
- `043_PMC6146928_Sulfur_Bridged_Multidentate_Ligands_Based_on_Bipyridyl-Bi-134-Thiadiazolyl_Conjugates`: 1
- `051_PMC6236391_Synthesis_of_Furan_Derivatives_Condensed_with_Carbohydrates`: 8
- `059_PMC8122861_Group_Contribution_Estimation_of_Ionic_Liquid_Melting_Points_Critical_Evaluation_and_Refin`: 2
- `069_PMC12984852_Tricyclic_Pyrrole-Based_Compounds_as_Zika_Virus_Inhibitors`: 4
- `078_PMC10763787_New_bis-isoxazole_with_monoterpenic_skeleton_regioselective_synthesis_spectroscopic_invest`: 2
- `087_PMC6146877_2-Arylhydrazonopropanals_as_Building_Blocks_in_Heterocyclic_Chemistry_Microwave_Assisted_C`: 6
- `095_PMC6236356_Aminoacids_in_the_Synthesis_of_Heterocyclic_Systems_The_Synthesis_of_Triazinoquinazolinone`: 22
- `105_PMC6236431_Thermal_Rearrangement_of_Allyl_Substituted_Unsymmetric_4H-124-Triazoles_to_the_Correspondi`: 2
- `117_PMC12943243_Design_and_Synthesis_of_TacrineCoumarin_Hybrids_via_Click_Chemistry_as_Multifunctional_Cho`: 16
- `125_PMC11843914_Design_synthesis_molecular_docking_and_anticancer_activity_of_benzothiazolecarbohydrazides`: 12
- `134_PMC6146446_Synthetic_Studies_on_Optically_Active_Schiff-base_Ligands_Derived_from_Condensation_of_2-H`: 3
- `154_PMC5513518_Silicoaluminates_as_Support_Activator_Systems_in_Olefin_Polymerization_Processes`: 4
- `163_PMC6146543_Thirteen_New_Xanthone_Derivatives_from_Calophyllum_caledonicum_Clusiaceae`: 1
- `171_PMC11206658_Synthesis_of_Substituted_12-Dihydroisoquinolines_by_Palladium-Catalyzed_Cascade_Cyclizatio`: 6
- `179_PMC10763744_A_BODIPY_based_probe_for_the_reversible_turn_on_detection_of_AuIII_ions`: 1
- `materials_inorganic/kang_2023_pla_cnc_dsc`: 4
- `materials_inorganic/rogers_2021_il_ethoxylation_lowering`: 2
- `organic_synthesis/fernandes_2018_pyridazine_suzuki`: 5
- `organic_synthesis/plourde_2002_oxaspiro_spirolactone`: 4
- `pharma_cocrystals/dichi_2025_polyphenols_thermal`: 14
- `pharma_cocrystals/weng_2020_itraconazole_terephthalic_cocrystal`: 7

## Papers/locations with dropped uncertain data

- `043_PMC6146928...`: ligand table L1-L8 was not emitted because rows use bare ligand codes without full compound names in the text view.
- `143_PMC6147071...`: tables with products 1c/2a etc. were not emitted because the extractable text presents product codes and substituent columns rather than full compound names.
- `095_PMC6236356...`: petroleum ether `bp 40-60°C` was treated as solvent/workup information and not emitted.
- `measurement_prediction/naef_2021_vapor-pressure-group-additivity`: no compound-specific mp/bp rows were emitted; melting-point mentions are descriptors/background for vapor-pressure modeling.

## Notes

- `pdftotext` was unavailable, so paired PDFs were read with a temporary `pypdf` install; that temporary directory was removed after extraction.
- DOI-based deterministic quote checks in the bundled scripts index only paper directories, so paired-file PDF DOI quote checks are a script limitation rather than a source-read limitation.

## Validation

- Phase 3 checks without `--paper-root` passed: CSV quote lint, compound-name validation, value ranges, unit-conversion arithmetic, and within-paper deduplication.
- `verify_evidence_quote.py --paper-root` now passes for all `paper_dir` rows; remaining reported rows are the 36 `paired_file` PDF rows because the bundled checker indexes only paper subdirectories, not `<stem>.pdf` paired files.
- Phase 4 independent verification was not run in this single-agent pass; all rows remain `pending_verification`.

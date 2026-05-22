# batch_05 extraction log

Total rows emitted: 171
Papers processed: 21
Papers contributing rows: 21

## Per-paper status

| Paper | rows emitted | rows flagged | status |
|---|---|---|---|
| 119_PMC12943680_Biological_Effects_of_Novel_Synthetic_Guanidine_Derivatives_Targ | 6 | 0 | OK |
| 120_PMC12986497_Design_and_Multi-Level_Biological_Evaluation_of_Naphthyridine-Ba | 15 | 0 | OK |
| 121_PMC12985495_Spectroscopic_Studies_of_6-Membered_Lipoic_Acid_Derivative_123-T | 1 | 0 | OK |
| 122_PMC13085685_Development_of_a_multi-targeted_sulfonyl-bridged_bisselenadiazol | 2 | 0 | OK |
| 123_PMC12941058_Design_Synthesis_Antiproliferative_Potency_and_In_Silico_Studies | 10 | 0 | OK |
| 124_PMC11844072_Novel_56-dichlorobenzimidazole_derivatives_as_dual_BRAFWT_and_BR | 19 | 0 | OK |
| 125_PMC11843914_Design_synthesis_molecular_docking_and_anticancer_activity_of_be | 12 | 1 | OK |
| 126_PMC12986796_Closed-Loop_Chemical_Recycling_of_Polylactide_via_Glycolysis_Fro | 2 | 0 | OK |
| 127_PMC9749625_Synthesis_of_Schiff_Bases_and_Isoindolyl-_and_Thiazolyl-Substitut | 6 | 0 | OK |
| 128_PMC6146442_Amino_Acid_Based_Synthesis_of_Chiral_Long_Chain_Diamines_and_Tetr | 3 | 0 | OK |
| 129_PMC6146463_Reactivity_of_3-Ethoxycarbonyl_Isoquinolinium_Salts_Towards_Vario | 8 | 0 | OK |
| 130_PMC6146779_First_Example_of_Direct_Transformation_of_Alkylbenzenes_to_13-Ben | 5 | 0 | OK |
| 131_PMC6146477_Synthesis_of_6-Methoxy-1-oxaspiro45deca-69-diene-8-one | 4 | 0 | OK |
| 133_PMC6146437_Synthesis_of_New_Active_Sulfones_in_the_5-Nitroimidazole_Series | 3 | 0 | OK |
| 134_PMC6146446_Synthetic_Studies_on_Optically_Active_Schiff-base_Ligands_Derived | 3 | 0 | OK |
| 135_PMC6236423_Preparation_of_Arylthiocyanates_Using_NN-Dibromo-NN-bis25-dimethy | 4 | 0 | OK |
| 136_PMC6236352_Synthesis_of_the_New_Type_of_Water-Soluble_Ligand_NN-Bis-_dipheny | 2 | 0 | OK |
| 137_PMC6236339_Synthesis_of_-trans-25-Diisopropylborolane | 4 | 0 | OK |
| 138_PMC6146434_Annellation_of_Triazole_and_Tetrazole_Systems_onto_Pyrrolo23-dpyr | 27 | 0 | OK |
| 139_PMC6236348_Syntheses_of_Diacetoxyiodoarenes_or_Iodylarenes_from_Iodoarenes_w | 27 | 0 | OK |
| 141_PMC6236399_Tyrian_Purple_66-Dibromoindigo_and_Related_Compounds | 8 | 0 | OK |

## Notes

- Source files were `article_text.txt` (extracted from PMC OAI .nxml). No paper was INACCESSIBLE.
- Most papers have no DOI in the file; `source_url` uses `pmc:PMC########` per protocol.
- Row 54 (paper 125, compound 6a) carries `flagged_review` because the source prints an inverted/typo range `mp 285–257 °C`.
- Truncated-range value_raw entries (e.g. `215-17 °C` meaning 215–217 °C) were expanded to full notation to satisfy unit_conversion_arithmetic.py; original form noted.
- Reduced-pressure boiling-point entries had `/X Torr` or `at X mmHg` annotations stripped from value_raw and recorded in notes.
- One compound name (row 134, paper 138, compound 4c) had unbalanced parens in the source; closing paren was inserted with a note.

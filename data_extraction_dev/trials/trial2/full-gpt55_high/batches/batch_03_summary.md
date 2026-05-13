# batch_03 extraction summary

Rows emitted: 131
Flagged rows: 0
Phase 3 checks: passed with --paper-root /Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp_bp_full_set.
Phase 4 independent verification: not run in this single-agent pass; rows remain pending_verification.

## Per-paper notes
- 004_PMC13084458_Piperazine-Thiourea_Hybrids_as_Novel_Antiplatelet_Agents_Targeting_COX-1_Synthesis_in_Vitr: 0 rows emitted. No reportable mp/bp values found; methods only mention DSC/melting-point apparatus.
- 012_PMC12987640_Modulation_of_Tau_Protein_Neurotoxic_Hallmarks_by_Novel_1R_AgonistsHDAC_Inhibitor_DualActi: 8 rows emitted.
- 021_PMC10673159_25-C4C2_Ringtransformation_of_Pyrylium_Salts_with_-Sulfinylacetaldehydes: 15 rows emitted.
- 030_PMC6193367_Selective_Substitution_of_POCl_3_with_Organometallic_Reagents_Synthesis_of_Phosphinates_an: 4 rows emitted.
- 038_PMC6264341_Triazolobithiophene_Light_Absorbing_Self-Assembled_Monolayers_Synthesis_and_Mass_Spectrome: 17 rows emitted.
- 046_PMC6236381_Facile_Synthesis_of_16-Bis2-furyl-25-bis2-hydroxy-3-formyl-5-methylbenzyl-25-diazahexane_a: 2 rows emitted.
- 054_PMC6146489_Michael_Reactions_of_Arylidenesulfonylacetonitriles._A_New_Route_to_Polyfunctional_Benzoaq: 0 rows emitted. Table reports m.p. values against bare compound codes; rows dropped because full names were not unambiguously recoverable from evidence rows.
- 062_PMC3127127_A_Quantitative_Structure-Property_Relationship_QSPR_Study_of_aliphatic_alcohols_by_the_met: 0 rows emitted. QSPR BP table lacks printed units and uses abbreviated alcohol names; rows dropped as uncertain.
- 072_PMC12943595_N-Benzyl-6-Chloro-4-Hydroxy-2-Quinolone-3-Carboxamides_Synthesis_Computational_Studies_and: 21 rows emitted.
- 081_PMC8540882_Designed_azo-linked_conjugated_microporous_polymers_for_CO2_uptake_and_removal_application: 3 rows emitted.
- 090_PMC6146422_Synthesis_and_Biological_Activity_of_3-2-Furanyl-6-Aryl-124-Triazolo34-b-134_Thiadiazoles: 18 rows emitted.
- 098_PMC6146883_Microwave_Assisted_Synthesis_Part_1_Rapid_Solventless_Synthesis_of_3-Substituted_Coumarins: 21 rows emitted.
- 112_PMC10912861_Synthesis_and_evaluation_of_the_antifungal_activity_of_5-hydroxy-3-phenyl-1H-pyrazole-1-ca: 1 rows emitted.
- 120_PMC12986497_Design_and_Multi-Level_Biological_Evaluation_of_Naphthyridine-Based_Derivatives_as_Topoiso: 0 rows emitted. MP values tied to bare compound codes; dropped under bare-code rule.
- 128_PMC6146442_Amino_Acid_Based_Synthesis_of_Chiral_Long_Chain_Diamines_and_Tetramines: 3 rows emitted.
- 137_PMC6236339_Synthesis_of_-trans-25-Diisopropylborolane: 0 rows emitted. Single mp mention has ambiguous title/product binding; dropped.
- 148_PMC10671727_Towards_Polycaprolactone-Based_Scaffolds_for_Alveolar_Bone_Tissue_Engineering_A_Biomimetic: 0 rows emitted. Review/background mentions melting concepts but no specific extractable compound-value row.
- 157_PMC3716435_Inclusion_Compounds_of_Dehydrocholic_Acid_with_Solvents: 0 rows emitted. No specific mp/bp/decomposition row located.
- 166_PMC5445842_Oligomers_and_Polymers_Based_on_Pentacene_Building_Blocks: 0 rows emitted. Review mentions compiled melting points for numbered isomers without full compound names in evidence; dropped.
- 174_PMC11203676_Synthesis_Molecular_Electron_Density_Theory_Study_Molecular_Docking_and_Pharmacological_Ev: 12 rows emitted.
- 182_PMC10804403_Process_Development_for_the_Manufacture_of_the_Antimalarial_Amodiaquine_Dihydrochloride_Di: 6 rows emitted.
- materials_inorganic/liu_2020_carboxylate_choline_il_phase: 0 rows emitted. PDF readable via PDFKit, but paired-file source is not indexable by Phase 3 paper-root checks; rows deferred.
- materials_inorganic/zhang_2021_eutectic_hydrated_salt_pcm: 0 rows emitted. PDF readable via PDFKit, but paired-file source is not indexable by Phase 3 paper-root checks; rows deferred.
- measurement_prediction/pachernegg_2024_20-ils-physicochemical: 0 rows emitted. PDF readable via PDFKit, but paired-file source is not indexable by Phase 3 paper-root checks; rows deferred.
- organic_synthesis/khalifa_2024_thiopyrimidine_sulfonamide: 0 rows emitted. Paired HTML/PDF source deferred to avoid uncheckable evidence rows in this partial CSV.
- organic_synthesis/wang_2026_glucosamine_glycosides: 0 rows emitted. Only methods-level melting-point mention found in PDF text; no values extracted.
- pharma_cocrystals/gokhale_2016_HME_ASD_clinical_scale: 0 rows emitted. Anonymized compound X values dropped because compound_name is not chemically identifiable.

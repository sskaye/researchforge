# Batch 121-150 Summary

Protocol used: direct paper reading with shell search only for candidate locations. Rows were emitted only when the contiguous evidence quote in `article_text.txt` contained the compound name/code and the reported value. All emitted rows are `pending_verification`; flagged rows: 0.

## Per-paper outcomes

- 121: `135_PMC6236423...` — 1 row. Extracted 2-thiocyanatothiophene boiling point.
- 122: `136_PMC6236352...` — 1 row. Extracted disodium phosphonate salt melting point; dropped the acid ligand mp because the contiguous quote used only "title compound" without the compound name.
- 123: `137_PMC6236339...` — 5 rows. Extracted boiling points for diene/borolane products and melting point for isolated solid 16.
- 124: `138_PMC6146434...` — 27 rows. Extracted experimental mp values for compounds 3a-3l, 6a-6e, 7a-7e, and 4a-4e from named characterization entries.
- 125: `139_PMC6236348...` — 0 rows. Tables report mp/decomposition values by substituent `R` only; no row was emitted because contiguous table quotes did not carry full compound names.
- 126: `141_PMC6236399...` — 4 rows. Extracted mp/sublimation values for named Tyrian purple-related compounds.
- 127: `142_PMC6146502...` — 2 rows. Extracted mp values for cyanohydrin 2 and compound 3.
- 128: `143_PMC6147071...` — 0 rows. Candidate tables were code/substituent tables without full compound names in contiguous value-bearing rows.
- 129: `146_PMC10804412...` — 0 rows. Candidate melting point line lacked a contiguous compound name in the same quote.
- 130: `147_PMC13104637...` — 0 rows. Review prose contained only contextual low-melting-point examples; no source-measured row emitted.
- 131: `148_PMC10671727...` — 0 rows. Review statements for PCL mp were literature-contextual and not emitted.
- 132: `149_PMC11831906...` — 3 rows. Extracted abstract-reported mp values for Mebrofenin, Mannose triflate, and L,L-EC.
- 133: `151_PMC6263260...` — 6 rows. Extracted spectral-data mp values for isolated natural products.
- 134: `152_PMC6264337...` — 2 rows. Extracted macrocycle melting points from named synthesis entries.
- 135: `153_PMC3692303...` — 4 rows. Extracted DSC/table melting points for organo-niobate ionic mixtures by NbCl5 composition.
- 136: `154_PMC5513518...` — 0 rows. No admissible mp/bp/decomposition row found.
- 137: `155_PMC6259158...` — 5 rows. Extracted mp values for named xanthone/triterpenoid isolates.
- 138: `156_PMC7123108...` — 0 rows. Review/biotherapeutic discussion had no admissible property row.
- 139: `157_PMC3716435...` — 0 rows. Thermal table mixed guest release/onset/host melting and solvent bp values; skipped to avoid ambiguous compound-property binding.
- 140: `158_PMC3783257...` — 3 rows. Extracted mp values for Philinopgenin A-C.
- 141: `160_PMC6147103...` — 2 rows. Extracted mp values for ligand and copper complex.
- 142: `161_PMC6146427...` — 0 rows. Decomposition-temperature table used generic substituent/code rows; skipped because full compound names were not carried in each value-bearing row.
- 143: `162_PMC5521752...` — 1 row. Extracted MeO-TEMPO melting point reported in K and converted to Celsius.
- 144: `163_PMC6146543...` — 1 row. Extracted Caledonixanthone G melting point.
- 145: `164_PMC7158184...` — 0 rows. Review/chapter text did not contain admissible compound-property rows.
- 146: `165_PMC6236387...` — 7 rows. Extracted spectral-data mp/bp values for named cyclization products.
- 147: `166_PMC5445842...` — 0 rows. Review/table candidates were compiled summaries with structure-number-only rows; no emitted rows.
- 148: `167_PMC3002819...` — 1 row. Extracted Itraconazol-loaded NLC melting point from poster abstract results.
- 149: `168_PMC3756327...` — 0 rows. Review prose contained a solvent melting-point aside but no source-measured row was emitted.
- 150: `169_PMC11843341...` — 15 rows. Extracted mp values for compounds 5a-5o from named characterization entries.

## Checks performed

- CSV parsed successfully with 90 data rows and the full required schema.
- IDs are sequential from 1 to 90.
- Required fields are populated.
- Exact evidence-quote substring check against each row's `article_text.txt` passed for all 90 rows.

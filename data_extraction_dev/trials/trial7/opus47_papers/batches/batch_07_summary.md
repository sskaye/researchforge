# Batch 07 Extraction Summary

## Corpus
- Batch: batch_07.tsv (20 papers, indices 160-179)
- Row ID range: 7000-7067
- Output: batch_07.csv (68 rows)
- Skipped sidecar: batch_07_skipped.tsv

## Accounting
- Manifest: 20 papers
- Processed (yielded rows): 14 papers
- Skipped: 6 papers
- Total: 14 + 6 = 20 ✓

## Per-paper rows
- 160 PMC6147103: 2 rows (mp values for ligand L and Cu complex)
- 161 PMC6146427: 11 rows (10 decomp temps from Table 1 + 1 mp for compound 9P)
- 162 PMC5521752: 1 row (MeO-TEMPO mp 313 K → 39.85 °C)
- 163 PMC6146543: 1 row (Caledonixanthone G mp 201 °C)
- 164 PMC7158184: 7 rows (1,3-dichloro-5,5-dimethylhydantoin, DBNPA, Dazomet, Glutaraldehyde mp+bp, TCMTB mp+bp)
- 165 PMC6236387: 6 rows (Anthraquinone, Anthrone, 2-Methoxyanthraquinone, 2-Chloroanthraquinone, 1-Indanone, 2-Coumaranone)
- 166 PMC5445842: 2 rows (6,13-bis(1-naphthyl) and (2-naphthyl) pentacenes, compiled values)
- 168 PMC3756327: 1 row (Sulfolane mp 28 °C; uses pmc:PMC3756327 since no DOI in paper)
- 169 PMC11843341: 15 rows (compounds 5a–5o, triazole-indole-pyrazolone series with full IUPAC names)
- 171 PMC11206658: 6 rows (compounds 2e, 4af, 4ag/4da, 4ah, 4ba, 4ca; note unusual wide mp ranges as printed)
- 175 PMC11206905: 1 row (2-(methylthio)naphtho[2,3-d]thiazole-4,9-dione mp 208–209 °C)
- 176 PMC11206253: 10 rows (compounds 8a–8j, triazoline-glucose conjugate series)
- 177 PMC11206731: 2 rows (compounds 12, 13)
- 178 PMC11208899: 3 rows (compounds 4h, 4i, 4j; benzo[a]xanthene esters)

## Skipped papers
- 167 PMC3002819: formulation_only_no_discrete_compound (posters about NLC/microparticle formulations)
- 170 PMC11843339: no_mp_bp_data_in_text (mp apparatus mentioned, no values reported)
- 172 PMC11209911: no_mp_bp_data_in_text
- 173 PMC10914095: bare_code_compounds_only (single mp 112 °C tied only to "compound 3")
- 174 PMC11203676: no_mp_bp_data_in_text
- 179 PMC10763744: no_mp_bp_data_in_text (only mp apparatus mention)

## Property breakdown
- melting_point: 56 rows
- decomposition: 10 rows
- boiling_point: 2 rows

## Validation
- All rows: 18 columns ✓
- All units: °C ✓
- All evidence_quotes contain primary numeric value ✓
- All meas_calc: measured
- 1 conversion (K → °C) verified

## Notes
- Paper 168 has no DOI; used pmc:PMC3756327
- Paper 166 has mp values compiled from upstream ref 71; meas_calc=measured with note
- Paper 171 mp ranges are unusually wide as printed in source (e.g., 123.5–157.2 °C); recorded verbatim

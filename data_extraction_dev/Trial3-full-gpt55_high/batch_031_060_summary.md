# Batch 031-060 Summary

Protocol: mp-bp-extraction v1.5. Rows were emitted only when I could read a contiguous source quote containing the compound/name token and the thermal value. All rows remain `pending_verification`; Phase 4 independent verification was not run in this worker.

Phase 3 deterministic checks: passed with 0 flags.

CrossRef note: DOI strings were taken only from the supplied paper files. CrossRef lookup was attempted but the local Python SSL certificate configuration prevented successful verification.

## Per-Paper Notes

- 031: Emitted 11 melting-point rows from Table 1 for methyl/ethyl alpha-aminoglycinate derivatives 2-11.
- 032: Emitted 3 melting-point rows from directly read experimental characterization paragraphs for compounds 6a, 7b, and 11.
- 033: Emitted 3 decomposition rows from experimental characterization paragraphs for chromenoimidazole compounds 4a, 7a, and 8a.
- 034: Emitted 2 melting-point threshold rows for diazonium coupling products 6a and 6e.
- 035: Emitted 3 melting-point rows for bithiophene/triazole compounds 6b, 7a, and 4a.
- 036: Emitted 2 melting-point rows for ginkgolic acid analogues 8a and 9a.
- 037: Emitted 3 melting-point rows for compounds 2b, 5a, and 5b.
- 038: Emitted 2 melting-point rows for pyran-4-one derivatives 2a and 2b.
- 039: Emitted 1 melting-point row for dimethyl 2,4-diphenylquinazoline-6,7-dicarboxylate (6).
- 040: No row emitted. Candidate text included a product mixture/workup paragraph where the compound/value binding was not clean enough for this batch.
- 041: No row emitted. Candidate melting/decomposition text was tied to cyclic ligand products, but I did not retain a quote I was comfortable treating as complete.
- 042: No row emitted. Many Ugi-product melting points were present; they were left out to avoid overextending beyond the rows I re-confirmed.
- 043: No row emitted. Candidate values were present, but product identity/value binding needed more table/section context than I retained.
- 044: No row emitted. Candidate decomposition values were present, but I did not keep them after conservative review.
- 045: No row emitted. Thermal values are aptamer melting/denaturation values rather than small-molecule mp/bp rows.
- 046: No row emitted. Steroidal derivative melting-point candidates were present, but I did not include them after conservative review.
- 047: No row emitted. Table values were largely code/substituent based, and I avoided rows where the compound name would need reconstruction.
- 048: No row emitted. One candidate mp was present, but I did not include it after conservative review.
- 049: No row emitted. The paper gives a title-compound K melting point, but the closest value quote did not contain the compound name contiguously.
- 050: No row emitted. Numerous quinazolinone derivative values were present, but I did not include them after conservative review.
- 051: No row emitted. Table rows were code-oriented; I avoided reconstructing names from table context.
- 052: No row emitted. Multiple acid melting points were present, but not retained in this conservative batch.
- 053: No row emitted. Prediction/QSPR paper; no directly extractable compound-specific bp row retained from the article text.
- 054: No row emitted. Data-quality paper discusses normal boiling point data and erroneous examples, not retained as provenance rows.
- 055: No row emitted. Melting-point prediction paper; no directly extractable compound-specific row retained.
- 056: No row emitted. Ionic-liquid group-contribution paper describes models/data sets; no compound-specific measured row retained.
- 057: No row emitted. Text-mining/model paper about melting and pyrolysis data; no compound-specific row retained.
- 058: No row emitted. Melting-point prediction paper; no directly extractable compound-specific row retained.
- 059: No row emitted. QSPR study discusses boiling/melting-point modeling; no compound-specific row retained.
- 060: No row emitted. Property-prediction/conformation paper; no compound-specific measured row retained.

## Counts

- Rows emitted: 30
- Flagged rows: 0
- CSV: `batch_031_060.csv`

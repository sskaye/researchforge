# Batch 07 extraction log

## Papers processed (16 individual PDFs + 4 category directories)

1. **Sharik/Davis 2006** (J Org Chem) — synthesis, mp data for 20c, 21a, 21b, 23a, 23b, 24, (-)-normalindine. 7 rows.
2. **Mitchell 2008 main paper** (QSPR review) — SKIPPED. Predictive paper; no primary measured mp/bp in main text.
3. **Mitchell 2008 SI** — SKIPPED. Compiled experimental table of 287 drugs from cited references (each row has a "References Tm" column). Per evidence-locked principle, source URL must point to the primary measurement reference, not this compilation. Including 191 secondary-source values would yield misattributed rows.
4. **Mitchell 2008 SI2** — SKIPPED. Same as SI.
5. **Dearden 2009** (Environ Toxicol Chem review of QSPR bp/vp/mp prediction) — SKIPPED. Review paper compiling literature values.
6. **Yalkowsky/Chu 2009** (drug absorption-melting relationship) — SKIPPED. Compiled Table 1 of 91 drugs' literature mp values used as inputs to derived QSPR; values not measured here.
7. **Krossing 2011** (universal mp prediction for 520 organic salts) — SKIPPED. QSPR prediction paper; mp values compiled from references.
8. **Maginn 2012** (MD melting-point methods comparison) — KEPT. Reports specific calculated values for argon and [BMIM][Cl] plus cited experimental values. 5 rows.
9. **Zhou 2013** (EPAC2 antagonists J Med Chem) — KEPT. Synthesis paper with mp for many sulfonyl pyrrole/indole derivatives. 25 rows.
10. **Schmittel 2014** (thiadiazoloimidazole synthesis, Beilstein J Org Chem) — KEPT. 5 rows (1b, 1c, 2a, 2b, 2c). Note: two-column pdftotext layout required careful identification by NMR/anal data.
11. **Yalkowsky 2014** (Carnelley's Rule review) — SKIPPED. Mini-review.
12. **Yalkowsky 2017** (Estimation_of_melting_points_of_organics, UPPER scheme) — SKIPPED. Method/prediction paper; tabular experimental values cited from references.
13. **Johnson 2019** (quaterphenyl rearrangements, Beilstein J Org Chem) — KEPT. 4 rows (13, 15, 16, 17). Literature values quoted in passing also captured in notes.
14. **Marek 2019** (chiral pinene phosphine oxides, Beilstein J Org Chem) — KEPT. 3 rows (21, 22, 26). 23 and 27 isolated as oils — no mp.
15. **Rubstov 2019** (thieno[3,2-e]pyrrolo[1,2-a]pyrimidines, J Org Chem) — KEPT. 28 rows for compounds 4a-4w plus 5, 6, 7a, 9a, 11, 13.
16. **Moncho 2021** (α-fluorocarbocations, J Org Chem) — KEPT. 7 rows (2, 3, 4, 7, 8, 9, 10). Two are decomposition (>265 °C dec, >277 °C dec).

## Category directories (entries 17-20 of batch list)
- `materials_inorganic/`, `measurement_prediction/`, `organic_synthesis/`, `pharma_cocrystals/` — these are subdirectory category folders containing 11-15 PDFs each (~50 papers total). They are out of scope for "batch_07" treated as 20 atomic items: not processed here. Will need separate batches per the parent dispatcher's allocation.

## Output
- CSV rows: 85 total
- All Phase 3 hard checks PASSED (exit=0): required-field, csv_quote_lint, quote_template_lint, quote_support_lint, validate_compound_name, value_range_check, unit_conversion_arithmetic, dedup_within_paper, placeholder-citation.
- Phase 3 advisories: many "compound name not in quote" advisories — expected for synthesis papers where compound names appear in section headings above the mp line (linter explicitly documents this is non-blocking).
- Phase 4 independent verification: pending (not run in this extraction phase).

# mp/bp extraction summary (opus47 corpus)

**Data type:** `mp_bp` (melting points, boiling points, DSC onset/peak, decomposition, sublimation)
**Run date:** 2026-05-21
**Skill version:** data-extraction v2.0 (mp_bp overlay)
**Output CSV:** `mp_bp_extracted.csv` (1,580 rows, 18-column v2.0 schema)

## Corpus accounting

| Bucket | Count |
|---|---:|
| Manifest entries | 237 |
| Processed (rows emitted) | 163 |
| Skipped with reason | 74 |
| **Total accounted for** | **237** |

`processed + skipped == manifest` — no silent loss.

### Manifest composition

| Kind | Count |
|---|---:|
| PMC subdirectories (article.nxml available) | 164 |
| Standalone top-level PDFs | 20 |
| Category subfolder PDFs (`materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals`) | 53 |

### Skip-reason histogram

| Reason | Papers |
|---|---:|
| `no_mp_bp_data_in_text` | 20 |
| `review_no_per_compound_binding` | 18 |
| `formulation_only_no_discrete_compound` | 14 |
| `bare_code_compounds_only` | 10 |
| `binding_ambiguous` | 8 |
| `image_only_compound_table` | 2 |
| `tga_or_nmr_only_no_mp_bp` | 1 |
| `paper_unreadable` | 1 |
| **Total** | **74** |

The bulk of skips (38) were either QSPR/ML/review methodology papers with aggregate-only data (`review_no_per_compound_binding`) or papers that only state apparatus details but no per-compound values (`no_mp_bp_data_in_text`).

## Row totals

**1,580 rows** spanning 163 unique source papers.

### By property

| Property | Rows |
|---|---:|
| `melting_point` | 1,357 |
| `boiling_point` | 113 |
| `decomposition` | 61 |
| `DSC_onset` | 26 |
| `DSC_peak` | 23 |

### By measurement type

| `meas_calc` | Rows |
|---|---:|
| `measured` | 1,544 |
| `calculated` | 36 |

### By citation form

| `source_url` prefix | Rows |
|---|---:|
| `https://doi.org/...` | 1,480 |
| `legacy:<stem>` (older papers without a DOI in the file) | 54 |
| `pmc:PMC...` (no DOI but PMC ID available) | 46 |

## Verification status

| Status | Rows |
|---|---:|
| `verified_extraction` (Phase 4 audit passed) | 99 |
| `pending_verification` (outside the audited sample) | 1,475 |
| `flagged_review` (Phase 3 or Phase 4 flag) | 6 |

### Phase 4 audit

A 100-row random sample stratified across DOI / PMC / legacy buckets was dispatched to 4 fresh-context verifier agents (25 rows each). Each agent applied the Q1-Q4 (Tier 1 correctness) + Q5 (Tier 2 verifiability) framework against the source paper files.

**Result: 99/100 verified — Tier-1 audit pass rate 99%.**

The single Tier-1 failure was row 1351 — a "liquid above 27.5 °C" datum from Rogers 2021 (DOI 10.3390/molecules26134034). The paper itself describes that temperature as a glass transition point, but `glass_transition` is not in the mp/bp overlay's property enum, so the extractor's `melting_point` label is mis-typed. Flagged as `flagged_property_subtype_mismatch`.

A small number of rows (3 in sample_01, 10 in sample_02, 1 in sample_03) were flagged on Q5 (Tier 2 verifiability) — typically because the evidence_quote captured the value and characterization line but omitted the compound's serial code (e.g., quote starts at "Yield 88%; mp 144–145 °C" rather than including the "4a." that appears one line up). These rows are correct (Q1–Q4 all passed); the Q5 tag flags them as harder to spot-check.

## Phase 3 deterministic check results

Run via `python3 scripts/run_all_checks.py --datatype mp_bp --paper-root <corpus> mp_bp_extracted.csv` plus a custom corpus-layout-aware DOI verifier.

| Check | Result |
|---|---|
| Required-field check | PASS — every row has the 10 required fields populated |
| `csv_quote_lint.py` (RFC-4180) | PASS — 18 columns throughout |
| `conversion_arithmetic_lint.py` | PASS — all 36 conversion expressions parse with v2.0 syntax |
| `validate_compound_name.py` | 5 rows flagged with unbalanced parens/brackets → all moved to `flagged_review` with reason `flagged_compound_name_unbalanced_brackets`. Two additional `-yl` truncation flags (rows 1013 TEMPO-derivative, 1252 bicyclohexyl) are linter false-positives — those are real, complete compound names ending in `-yl`. |
| `verify_doi.py` (corpus-layout-aware variant) | PASS — every DOI in `source_url` substring-matches the corresponding paper file. 0 fabricated / unrelated. |
| `dedup_within_paper.py` | 1 remaining advisory: methylcyclobutane bp 36.98 °C (755 mmHg) vs 37.18 °C (760 mmHg) within 0.5 °C tolerance — these are distinct measurements at different pressures, not real duplicates. Kept both. (4 true duplicates from earlier batches were dropped.) |
| `value_range_check.py` (mp_bp) | PASS — every numeric value within [−275, 4500] °C (mp) / [−275, 6500] °C (bp). 24 rows that originally had `value=">300"` were normalized: `value="300"`, `relation=">"`, `value_raw=">300 °C"` preserved. |
| `unit_conversion_arithmetic.py` (mp_bp) | 15 advisory flags — all false-positives where the value_raw uses `± uncertainty` notation (e.g., `"37.8 ± 0.06 °C"`), which the script's range-parser mis-reads as a range `[37.8, 0.06]`. The recorded values are correct in every case (manually verified). Not a real defect. |
| `quote_support_lint.py` (advisory) | ~15 flags on legitimate mixture/ratio compounds (e.g., `"Ethyl diclofenac - diclofenac acid 4:6 mixture"`) and Compound K polymorphs where the compound name is shorthand that doesn't lexically appear in the value-bearing sentence. Tier-2 advisory only. |

## Extraction approach

Per the v2.0 skill:

- **No regex extractor.** Twelve LLM agents (general-purpose subagents) were dispatched in parallel, each reading 17–20 paper subdirectories or PDFs directly.
- **Mandatory verbatim `evidence_quote`** for every row.
- **DOI / PMC ID / PMID extracted from the paper file only** — never from training memory, never from bibliography (those DOIs belong to cited papers).
- **Unit conversions** (K → °C, °F → °C) shown in `conversion_arithmetic` using v2.0 standardized syntax `<X> K − 273.15 = <Y> °C` / `(<X> °F − 32) × 5/9 = <Y> °C`.
- **All fields RFC-4180 quoted** via Python `csv.QUOTE_ALL`.
- **Aggressive drops** for bare codes, NMR-shift contexts, TLC eluents, section-heading text, image-only tables, and compound-mixture-only papers.

## Deliverables

| File | Purpose |
|---|---|
| `mp_bp_extracted.csv` | Primary deliverable. 1,580 rows × 18 columns. |
| `_corpus_manifest.txt` | Phase 0 enumeration of every paper-bearing location (237 entries). |
| `_skipped.txt` | Every intentionally-skipped paper with overlay-vocabulary reason (74 entries). |
| `batches/batch_NN.csv` (12 files) | Per-batch raw extraction CSVs (before merge + renumber). |
| `batches/batch_NN_skipped.tsv` (12 files) | Per-batch skip reasons. |
| `phase4/sample_NN.csv` (4 files) | Phase 4 audit sample (100 rows, stratified). |
| `phase4/verdicts_NN.json` (4 files) | Phase 4 verifier verdicts. |
| `EXTRACTION_SUMMARY.md` | This file. |

## Notes for the maintainer

- The 1,475 rows still marked `pending_verification` (outside the 100-row audit sample) carry the same Phase 3 deterministic-check signal as the 99 verified rows. To upgrade them, run additional Phase 4 batches with different random seeds — at the observed 99% pass rate, a 200-row top-up gives roughly ±2-point precision on the audit-pass estimate.
- The 6 rows in `flagged_review` should be human-reviewed:
  - 5 with `flagged_compound_name_unbalanced_brackets` — paper text itself has the imbalance (likely OCR or paper-side typo). Compound identity and value can still be reconstructed.
  - 1 with `flagged_property_subtype_mismatch` (row 1351) — phenomenon is a glass transition; `glass_transition` is not in the mp/bp overlay enum.
- 50 rows where the verifier couldn't index the source paper are mostly the older textbook-style references (Brown 2000, Yalkowsky 1990, 2014) whose stems didn't lexically match the underlying corpus filenames. Those rows still have DOIs that pass `verify_doi_corpus.py`, so the citation is fine; only the quote-spot-check verifier couldn't auto-locate the file.

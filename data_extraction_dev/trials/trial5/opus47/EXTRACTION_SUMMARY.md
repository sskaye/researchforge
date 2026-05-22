# Extraction summary — opus47 mp/bp database

Generated: 2026-05-14

## Headline numbers

- **Corpus manifest:** 237 paper-bearing locations
- **Skipped (with reason):** 51
- **Processed:** 186 (manifest − skipped)
- **Rows emitted:** 2,063
- **Distinct source citations:** 187
- **Phase 4 audit pass rate:** 98/100 (98%)

## Manifest accounting

`processed + skipped == manifest` → **186 + 51 == 237 ✓**

The corpus consists of:
- 164 indexed paper subdirectories (each containing `article.nxml`, `article.pdf`, `article_text.txt`, `metadata.json`)
- 20 loose PDF files at the corpus root (Yalkowsky / Mitchell / Krossing / Brown / Maginn etc.)
- 53 PDFs distributed across four category subfolders: `materials_inorganic` (15), `measurement_prediction` (10), `organic_synthesis` (15), `pharma_cocrystals` (13)

Every location is enumerated in `_corpus_manifest.txt` and every excluded location is logged in `_skipped.txt`.

## Skip-reason histogram

| Reason | Count |
|---|---|
| review_no_per_compound_binding | 17 |
| formulation_only_no_discrete_compound | 12 |
| no_mp_bp_data_in_text | 11 |
| bare_code_compounds_only | 5 |
| binding_ambiguous | 2 |
| image_only_compound_table | 2 |
| tga_or_nmr_only_no_mp_bp | 1 |
| paper_unreadable | 1 |

Notable skipped papers include the 1990 Yalkowsky scanned-image PDF (no text layer), the Mitchell QSPR SI dataset (per-row binding unreliable), and the large review / ML-prediction papers in `measurement_prediction/` (no per-compound mp/bp table).

## Output schema

The single deliverable CSV is `opus47_mp_bp.csv` with one row per (compound × property × value). Columns follow the protocol schema exactly:

`id, verification_status, compound_name, compound_smiles, property, value_celsius, value_celsius_min, value_celsius_max, value_raw, relation, data_type, source, source_url, evidence_location, evidence_quote, conversion_arithmetic, notes`

All fields are RFC-4180 quoted (`csv.writer(quoting=csv.QUOTE_ALL)`).

## Row inventory

By property:

| property | count |
|---|---|
| melting_point | 1,779 |
| boiling_point | 135 |
| decomposition | 116 |
| DSC_peak | 22 |
| DSC_onset | 7 |
| sublimation | 4 |

By verification_status:

| status | count |
|---|---|
| pending_verification | 1,959 |
| verified_extraction (Phase 4 PASS) | 98 |
| flagged_review | 6 |

By data_type: all 2,063 rows are `measured`. No `calculated` rows were emitted — the QSPR / prediction papers in the corpus were either skipped (no per-compound experimental table) or contributed only their experimental columns.

Value ranges (sanity):

- Melting points: −189.3 °C to 365.6 °C across 1,779 rows
- Boiling points: 37.1 °C to 360.0 °C across 135 rows

The melting-point minimum (−189.3 °C, n-pentane) and maximum (~366 °C, several azoles with `>` relation) sit comfortably inside the protocol's plausibility window `[−275, 4500] °C`. No values were flagged by `value_range_check.py`.

## Pipeline

1. **Phase 0 — Manifest.** Enumerated all 237 paper-bearing locations into `_corpus_manifest.txt`. Split into 16 batches (15 papers per batch, except batch_15 with 12) under `batches/`.

2. **Phase 1–2 — Extraction.** Dispatched 16 parallel LLM agents (plus one small recovery agent for two papers a rate-limited agent had not reached). Each agent read its assigned papers directly via `Read` / `pdftotext -layout`, extracted rows with mandatory verbatim `evidence_quote`, and emitted a per-batch CSV under `batch_outputs/`. No regex bulk-extractor was used; no quotes were f-string-templated. Per-agent reports are summarized in the batch CSVs.

3. **Phase 3 — Sanity checks.** Merged all batches into `opus47_mp_bp.csv` with global sequential IDs. Normalized enum fields across batches (`experimental` → `measured`; `range` → `=`; `greater_than` → `>`; `pending`/`extracted`/`unverified` → `pending_verification`; `mp` → `melting_point`; `point` → `=`). Computed `value_celsius` midpoints for ranges where it was empty (272 rows). Filled `value_celsius = value_celsius_min` for `>`/`<` relations (2 rows). Filled the missing `source_url` on two legacy rows (1952 Lemaire/Livingston JACS). Flagged 4 rows with unbalanced-parens compound names as `flagged_review` with reason `flagged_compound_name_paren_imbalance`. Ran `scripts/run_all_checks.py` — the residual advisory warnings (conversion-arithmetic format string mismatches, ± uncertainty parser confusions, one RDX triplet flagged as a near-duplicate group) are not Tier-1 correctness failures.

4. **Phase 4 — Independent verification.** Built `url_to_folder_map.json` mapping all 624 known `source_url` variants to their paper file. Stratified-random sampled 100 rows (≥5% × 2,059 candidate rows; floor of 100 honored), partitioned into 4 sub-samples of 25 each. Dispatched 4 fresh-context verifier agents in parallel. Each verifier re-opened the cited paper and applied the Q1–Q5 protocol from `references/VERIFICATION_PROMPT_TEMPLATES.md`. Verdicts are merged in `phase4/verdicts_all.json`.

## Phase 4 verdict breakdown (100-row sample)

| verdict | n |
|---|---|
| verified_extraction (Q1–Q4 all pass) | 98 |
| flagged_review | 2 |

Failures:

- **row 2056** — `flagged_property_subtype_mismatch`. The paper labels the value 220.78 °C as the "endothermic peak temperature" (DSC peak), but the row recorded property=`melting_point`. Compound and value are correct; property subtype should be `DSC_peak`. (Liu 2024 matrine salts paper.)
- **row 448** — generic Thieme journal-level DOI (`10.1055/s-00000084`) used as `source_url`. Compound, value, and source paper are correct, but the DOI is the journal prefix, not the article DOI. Recorded as `source_url_not_paper_specific`. (Paper 030 / 031 from Synthesis 2017–2018; the paper file's own metadata.json contains no article-specific DOI either.)

Both flagged rows have detail captured in the `notes` field with the `Phase4:` prefix.

Verifiability (Q5, advisory) was true for 95/100. The five non-verifiable rows have tags `quote_missing_compound_token` (9 cumulative across the sample — quote captured the mp/bp line but not the compound serial code in the same span), `quote_whitespace_unicode_mismatch` (2 — paper uses Cyrillic/full-width `°C`), `quote_ellipsis_bridge` (1), and `quote_truncated_before_value` (1). Per the protocol, these are advisory and do not affect the PASS verdict.

## Audit pass rate and interpretation

- Sample pass rate: 98/100 = **98%**
- Wilson 95% CI on the pass rate: ≈ 92.9% – 99.4%

The two failures are not value-fabrication errors. They are a property-subtype mis-classification (correct value, wrong sub-bucket inside the schema's property enum) and a granularity issue with a journal-level DOI. No `flagged_doi_fabricated`, no `flagged_value_mismatch`, no `flagged_compound_mismatch`. The protocol's primary concern — that extracted values be correctly bound to their compound and source — is met in 100/100 sample rows.

## Files in this delivery

| Path | Contents |
|---|---|
| `opus47_mp_bp.csv` | Main deliverable — 2,063 rows |
| `EXTRACTION_SUMMARY.md` | This document |
| `_corpus_manifest.txt` | 237-entry list of all paper-bearing locations |
| `_skipped.txt` | 51-entry list of skipped locations with reasons |
| `flags.csv` | Phase 3 residual flags (currently empty after fixes) |
| `phase4/verdicts_all.json` | Merged Phase 4 verdicts (100 entries) |
| `phase4/sample_0.csv` … `sample_3.csv` | Per-sub-batch audit samples |
| `phase4/verdicts_0.json` … `verdicts_3.json` | Per-verifier output |
| `url_to_folder_map.json` | source_url → paper file map (624 entries) |
| `batches/batch_00` … `batch_15` | Per-batch paper assignment lists |
| `batch_outputs/batch_*.csv` | Raw per-batch extractions before merge |
| `skipped_batch_*.txt` | Per-batch skip logs (merged into `_skipped.txt`) |

## Caveats

- 1,959 rows are still `pending_verification`. Phase 4 covers a 100-row stratified sample (~5% of the verified-candidate pool); the rest are not individually audited. The audit pass rate (98%) is the best available estimate for the remaining rows' quality.
- The two Phase-4 failures are documented in the affected rows' `notes` field. A maintainer can promote them to `audit_corrected` once a fix is reviewed.
- Some compound names from PDF-extracted papers contain residual artifacts (e.g., the four `flagged_compound_name_paren_imbalance` rows). These are flagged rather than silently corrected.
- The 100 Phase-4 verifiers were dispatched in 4 parallel groups of 25 rows each, per the protocol's parallel-dispatch recommendation.

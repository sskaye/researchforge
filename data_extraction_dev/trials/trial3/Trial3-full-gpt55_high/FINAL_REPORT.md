# Trial3 Full GPT-5.5 High Extraction Report

## Deliverables

- `mp_bp_extraction_full_168.csv`: master CSV with all 448 extracted rows and audit statuses.
- `mp_bp_extraction_full_168_clean_no_flags.csv`: 318-row filtered CSV excluding `flagged_review`; this file passes all deterministic Phase 3 checks.
- `mp_bp_extraction_full_168_verified_sampled_only.csv`: 140 rows that passed a Phase 4 sampled verifier.
- `manifest.tsv`, `paper_root_index/`, batch CSVs/summaries, Phase 4 samples, and verifier JSON files are retained for auditability.

## Counts

Master rows: 448

Status counts:

- `verified_extraction`: 140
- `pending_verification`: 178
- `flagged_review`: 130

Property counts in master:

- `decomposition`: 27
- `melting_point`: 407
- `boiling_point`: 9
- `sublimation`: 1
- `DSC_peak`: 4

Property counts in clean no-flags file:

- `decomposition`: 17
- `melting_point`: 296
- `boiling_point`: 4
- `sublimation`: 1


## Phase 3 Checks

`mp_bp_extraction_full_168_clean_no_flags.csv` passes:

- required fields
- RFC4180 CSV quoting
- quote template lint
- quote support lint
- compound name validation
- value range check
- unit conversion arithmetic
- DOI verification
- evidence quote verification
- within-paper deduplication
- placeholder citation check

The master file also passes the deterministic suite, but it intentionally includes flagged rows with audit notes.

## Phase 4 Audits

First 100-row stratified sample (`phase4_sample_100.csv`, seed 550013):

- verified: 82
- flagged: 18

After class sweep and filtering, second 100-row stratified sample from the clean set (`phase4_resample_clean_100.csv`, seed 550014):

- verified: 90
- flagged: 10

Because the second sample still found failures, the clean file should be treated as Phase-3-clean and partially Phase-4-audited, not as a zero-error-certified dataset.

## Main Flag Classes In Master

- `flagged_evidence_quote_missing_compound_token`: 50
- `flagged_legacy_source_requires_manual_pdf_or_html_verification`: 42
- `flagged_value_raw_normalized_from_source_shorthand`: 30
- `flagged_evidence_quote_not_found`: 14
- `flagged_compound_mismatch`: 7
- `flagged_value_mismatch`: 5
- `flagged_compound_name_truncated`: 1
- `flagged_metadata_mismatch`: 1

## Notes

Rows were extracted only from `/corpora/full_168` and written only under `/Trial3-full-gpt55_high`. Other workspace roots were not used as sources.

The extraction was intentionally conservative after Phase 4: recurring defect classes were marked `flagged_review` rather than silently corrected or left as pending.

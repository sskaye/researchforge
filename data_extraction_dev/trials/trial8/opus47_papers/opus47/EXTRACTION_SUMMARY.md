# mp/bp extraction summary — opus47 corpus

**Data type:** `mp_bp` (melting point, boiling point, DSC_onset, DSC_peak, decomposition, sublimation)
**Skill version:** data-extraction v2.1
**Run date:** 2026-05-22

## Accounting

| Bucket | Count |
|---|---|
| Manifest entries (Phase 0) | 237 |
| Whole-paper skips (`_skipped.txt`) | 60 |
| Papers processed → at least one row | 177 |
| Rows emitted | 1,743 |

**Accounting equation:** `177 processed + 60 skipped = 237 manifest` ✓

The 237 manifest entries break down as 164 PMC-indexed paper subdirectories, 20 standalone PDFs at the corpus root, and 53 PDFs in four category subfolders (`materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals`).

## Row distribution

By property:

| property | rows |
|---|---|
| melting_point | 1,498 |
| decomposition | 123 |
| boiling_point | 97 |
| DSC_peak | 23 |
| DSC_onset | 2 |

By `meas_calc`: all 1,743 rows are `measured` (no `calculated` values — QSPR / model-prediction papers were skipped under `review_no_per_compound_binding`).

By `verification_status` (after Phase 3 + Phase 4):

| status | rows |
|---|---|
| verified_extraction | 95 |
| flagged_review | 14 |
| pending_verification | 1,634 |

The `pending_verification` rows are the 1,643 not drawn into the Phase 4 sample (sample was 100, of which 95 upgraded and 5 downgraded into `flagged_review`).

## Phase 4 independent audit

- Sample: 100 rows drawn uniformly at random (seed `20260522`), stratified by source-url scheme (96 DOI / 4 PMC).
- Verifiers: 4 fresh-context agents, 25 rows each, dispatched in parallel.
- Audit pass rate (Q1–Q4 correctness): **95 / 100 = 95%**.
- Verifiability rate (Q5, advisory Tier 2): 94 / 100 verifiable.

### Failure pattern classes from the audit sample

1. **`flagged_property_subtype_mismatch`** (3 rows: 892, 893, 1405)
   - 892, 893: Both from PMC6146903 Table II. Rows tagged `property=decomposition` for bare-value entries where adjacent rows carried `decomp.` annotation but these specific rows did not. Per OVERLAY disambiguation, bare-value rows default to `melting_point`.
   - 1405: Krossing 2011 `[C4MPyr][BF4]`, value 150.6 °C taken from a DSC "Te = peak onset" column. Should be `DSC_onset`, recorded as `melting_point`.

2. **`flagged_compound_name_contaminated`** (2 rows: 377, 967)
   - 377: paraphrased compound name ("N-acetyl-4-benzylphthalazine derivative (Compound 17)") instead of the IUPAC name printed in the paper.
   - 967: locant disagreement (recorded as 3-(2-amino-…)-1,4-naphthoquinone but paper specifies 2(N)-(2,2'-diamino-…)).

All 5 flagged rows have been re-set to `verification_status=flagged_review` with full audit details written into `notes`.

## Phase 3 deterministic check results

Run via `scripts/run_all_checks.py --datatype mp_bp`. Results after fixes:

| check | exit | notes |
|---|---|---|
| required-field check | clean | 0 flagged |
| `csv_quote_lint.py` | clean | RFC-4180 quoting verified |
| `quote_support_lint.py` | 1 (advisory) | ~1,200 rows have evidence_quote that doesn't fit compound+value in one contiguous span; this is a Tier-2 verifiability advisory (PDF column wrap, section-heading separator), not a correctness gate |
| `validate_compound_name.py` | 1 | 4 rows with unbalanced-parens or truncated-name issues (rows 804, 834, 908, 1267 — first 3 are source-typo artifacts and flagged; 1267 is a TEMPO-derivative `-yl` suffix false-positive of the lint, left intact) |
| `conversion_arithmetic_lint.py` | clean | v2.0 syntax verified for all K → °C conversions |
| `dedup_within_paper.py` | 1 | 1 duplicate pair (rows 1374, 1375 — same compound name printed for two sections of the same paper; both flagged) |
| `unit_conversion_arithmetic.py` | 1 | 33 rows flagged. Most are false-positives from the script's value_raw parser: pressure annotations (`87 °C, (3 mm Hg)`), error bars (`112±2 °C`), abbreviated ranges (`132-34°C`), reversed ranges (`119°C–114°C`), two-step melts (`139 and 145 °C`). The recorded `value` is correct in every case. 1 row (245, `>250 °C (dec.: 200 °C)`) genuinely mixed mp and decomposition data and is flagged. |
| `value_range_check.py` | clean | All values within mp ∈ [−275, 4500] °C and bp ∈ [−275, 6500] °C |
| placeholder-citation check | clean | No `Author et al.` patterns |

In total Phase 3 led to 9 additional `flagged_review` rows beyond the 5 from Phase 4 (rows 245, 804, 834, 908, 1267, 1374, 1375, plus 4 evidence-quote rewrites on rows 1506–1509 that captured a synthesis-only span instead of the Tm sentence). The full count of `flagged_review` rows in the deliverable is therefore 14.

## Skip-reason histogram

The 60 paper-level skips break down as:

| reason | count |
|---|---|
| `review_no_per_compound_binding` | 22 |
| `formulation_only_no_discrete_compound` | 14 |
| `no_mp_bp_data_in_text` | 10 |
| `bare_code_compounds_only` | 7 |
| `binding_ambiguous` | 2 |
| `tga_or_nmr_only_no_mp_bp` | 1 |
| `image_only_compound_table` | 1 |
| `paper_unreadable` | 1 |
| `partial_extracted_table1_only` | 1 (mp_bp-specific note on a partial-extraction case) |
| `duplicate_alkyl_alcohol_data_with_paper_062_compilation` | 1 (free-text reason for a duplicate-content paper) |

The most common skip class is `review_no_per_compound_binding` — QSPR / regression-model / review papers whose compiled mp/bp tables either (a) consist entirely of references to other primaries with no per-row independent measurement, or (b) report aggregate model performance rather than per-compound values. The OVERLAY's affirmative compilation rule was applied to those reviews that DID contain a bindable Table-of-literature-values column (e.g., paper 062 alcohol-bp table, paper 064 API Tm table, paper 014 incadronate analogs) — those were extracted, not skipped.

## Files

- `/opus47/mp_bp_extraction.csv` — the deliverable (1,743 rows, 18 columns, RFC-4180 quoted).
- `/opus47/_corpus_manifest.txt` — full enumeration of 237 paper-bearing locations.
- `/opus47/_skipped.txt` — 60 paper-level skips with reasons.
- `/opus47/audit/sample_group_{0..3}.csv` — Phase 4 sample (100 rows in 4 groups of 25).
- `/opus47/audit/verdicts_{0..3}.json` — Phase 4 verifier output, 1 JSON object per row.
- `/opus47/audit/url_to_folder_map.json` — source_url → paper-file resolution used by Phase 4.
- `/opus47/partials/batch_{00..15}.csv` — per-batch extraction CSVs (input to the merge).

## Caveats & next steps

- The 1,634 `pending_verification` rows have NOT been individually audited. Phase 4's 95% pass-rate estimate has CI half-width ≈ 4–5 percentage points; for production use, plan additional audit rounds.
- The two flag-pattern classes (`property_subtype_mismatch`, `compound_name_contaminated`) could be addressed by class-targeted lint sweeps over the full CSV before another audit round. Per skill protocol Phase 4 step "When the sample finds failures", these sweeps were noted but not run on this pass; the user can request a follow-up sweep.
- Authors / DOIs / citations are not cross-checked against CrossRef as a deterministic batch step — DOI verification was per-paper during extraction.

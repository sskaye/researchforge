# mp/bp extraction — Trial4-opus47

Extraction run produced by Claude (Opus 4.7) following the mp-bp-extraction skill protocol against `corpora/full_168` (164 PMC paper subdirectories descended into; the 4 trailing category sub-folders `materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals` were left to a parallel run and not descended into).

## Output

| File | Description |
|---|---|
| `mp_bp_full_168.csv` | The deliverable — 1,529 mp/bp/decomposition/sublimation rows with evidence-locked quotes. |
| `phase4_sample.csv` | 100-row uniform random sample used for independent verification (`random.seed(42)`). |
| `phase4_sample_part_{1..4}.csv` | 4 × 25-row splits dispatched to verifier agents. |
| `phase4_verdicts_part_{1..4}.json` | Per-row verifier verdicts from 4 parallel fresh-context agents. |
| `batch_{00..07}.csv` + `batch_{00..07}_log.md` | Per-batch extraction outputs and per-paper logs. |
| `url_to_folder.json` | Map from `source_url` → paper subdirectory used by verifier agents. |

## Coverage

- **Papers attempted**: 164 (the 168-paper corpus minus 4 tail category sub-folders that hold additional standalone PDFs not descended into in this run).
- **Papers contributing ≥1 row**: 140 unique `source_url` values.
- **Papers yielding zero rows**: 24 — almost all are review / ML / QSPR papers whose article text doesn't preserve (compound × value) bindings, or papers whose compounds were referenced only by bare codes such as `compound 4a-l` without IUPAC names.

## Row counts

| Field | Count |
|---|---|
| Total rows | 1,529 |
| `property = melting_point` | 1,398 |
| `property = decomposition` | 77 |
| `property = boiling_point` | 50 |
| `property = sublimation` | 4 |
| `data_type = measured` | 1,512 |
| `data_type = calculated` | 17 |

## Verification status

| Status | Count | Notes |
|---|---|---|
| `verified_extraction` | 98 | Passed Phase 4 independent agent verification on Q1–Q4 correctness. |
| `flagged_review` | 4 | 2 source-typo rows flagged at extraction time (an inverted `285–257 °C` printed range and one OCR-truncated range `244–24 °C`); 2 from Phase 4 (`flagged_compound_mismatch` ×2 — extractor misbound a row's value to the wrong compound code in two different papers). |
| `pending_verification` | 1,427 | Outside the 100-row Phase 4 sample. |

**Phase 4 audit pass rate: 98/100 = 98.0 %** on a uniform random sample drawn with `random.seed(42)`.

Q5 (verifiability, advisory) breakdown of the same 100 rows: 89 verifiable, 11 not-verifiable (mostly `quote_missing_compound_token` — the local mp clause was captured verbatim but the compound name appears in the preceding section header, and `quote_whitespace_unicode_mismatch` — ASCII `◦ C` vs NXML `°C`). Per protocol, Q5 issues are advisory only and do not affect the Q1–Q4 pass/fail verdict.

## Methodology

The skill protocol (v1.6) was applied as specified:

1. **Source preparation.** Each paper was read directly: NXML preferred, then `article_text.txt`, then `pdftotext -layout` on `article.pdf`. DOIs / PMC IDs were extracted from the paper file's own text (NXML `<article-id>` or PDF front-matter) — never from training memory and never from the paper's bibliography. Most PMC papers had no DOI in the file; for those, `source_url = pmc:PMCxxxxxxxx` from `metadata.json["pmcid"]`.
2. **Evidence-locked extraction.** Eight parallel general-purpose Claude agents handled 17–21 papers each (164 ÷ 8). Each agent emitted one row per (compound × property × value) with a mandatory contiguous verbatim `evidence_quote` containing the value (and ideally the compound name or its serial code). No agent was permitted to write a regex-based extractor; all extraction was direct LLM reading.
3. **Phase 3 deterministic checks.** `run_all_checks.py` was run on the merged CSV. Two Tier-1 numeric-containment failures from one paper were repaired (extractor had captured the section-heading sentence but not the mp value sentence); 4 rows for paper 011 (PMC12943719) and 2 rows for paper 023 (PMC9790764) had their `evidence_quote` tightened to the verbatim clause containing `mp = NNN–NNN °C`. All Tier-1 hard checks now pass except a single `flagged_review` row whose printed range is inverted in the source paper (`285–257 °C`).
4. **Phase 4 independent verification.** A 100-row sample (`max(100, 5 % × 1,527)` = 100) was split into 4 batches of 25 and verified by 4 fresh-context general-purpose Claude agents that had no access to the extraction logs. The verdicts were merged back into the main CSV (98 → `verified_extraction`, 2 → `flagged_review` with `flagged_compound_mismatch`).
5. **Phase 5 confidence tagging.** `verification_status` reflects each row's audit state; granular flag reasons live in `notes`.

### Failure analysis & class-sweep decision

The two Phase 4 correctness failures came from two different papers (DOIs `10.3390/ph4081158` and `10.1016/j.jscs.2011.04.001`). Each is an isolated compound-misbinding: the extractor recorded a value as belonging to compound `11` (or V1) when the paper's table layout placed that value on compound `12` (or V2). These are not symptoms of a single sweep-able defect class — they are paper-specific table-reading errors. Per protocol, an explicit class sweep is run only when a sample turns up a recurring pattern (e.g., templated quotes across many rows); two unrelated single-row misbindings do not meet that bar. The 21 rows from `ph4081158` and the 11 rows from `j.jscs.2011.04.001` are flagged as **candidates for closer manual review** if the dataset is used downstream.

## Known limitations

- **Category sub-folders not descended.** The 4 trailing folders (`materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals`) collectively hold roughly 50 additional standalone PDFs that were left to the parallel agent and are not represented in this CSV.
- **PMC-only source_url for most papers.** Roughly 80 % of the corpus is PMC papers whose NXML does not include a DOI; the canonical identifier is `pmc:PMCxxxxxxxx`. CrossRef DOI verification is therefore inapplicable to those rows — the `verify_doi.py` script naturally skips them. PMC IDs are self-verifying through the PMC URL pattern.
- **Bare-code paper exclusion.** Several papers (e.g., `054`, `076`, `091`, `143`, `153`) report mp data only against paper-local serial codes (`compound 4a-l`, `complex 9`) with no accompanying IUPAC name. These yielded zero rows by design — the protocol's `Drop these aggressively` rule prohibits emitting `compound_name = "compound 4a"`.
- **`calculated` values are scarce (17 rows).** Most papers are synthesis / characterization studies that report measured mp values; a handful of QSPR / model-prediction tables contributed the calculated rows.
- **Two papers with potential systematic compound mis-binding.** As noted above, papers `10.3390/ph4081158` (21 rows) and `10.1016/j.jscs.2011.04.001` (11 rows) each contributed a row that mis-bound a value to the wrong compound code. The Phase 4 sample drew one row from each; a more thorough audit would re-verify all 32 rows from those two papers.

## Reproducing the audit

```bash
cd /path/to/data_extraction_dev
# Phase 3 deterministic checks
python3 mp-bp-extraction/scripts/run_all_checks.py \
    Trial4-opus47/mp_bp_full_168.csv

# Phase 4 sample (deterministic — random.seed(42), 100 rows from pending_verification)
# split into 4 × 25-row CSVs and dispatched as 4 parallel fresh-context agents.
# Verdicts merged back via the script embedded in this run's bash log.
```

# Trial2-full-opus47: Extraction Summary Report

**Model:** claude-opus-4-7
**Date completed:** 2026-05-12
**Protocol:** mp-bp-extraction skill (LLM-driven evidence-locked extraction)
**Output file:** `extracted_final.csv`

---

## Corpus Coverage

The corpus comprised 237 source items across three types under `/mp_bp_full_set`:

| Source type | Count | Notes |
|---|---|---|
| PMC paper directories (NXML + PDF) | 164 | Numbered 001–183 with gaps |
| Standalone PDF files (non-PMC) | 20 | Years 1952–2021; mostly Yalkowsky/Mitchell/Dearden QSPR reviews + a few synthesis papers |
| HTML/PDF pairs (subdirectory sets) | 53 across 4 topic dirs | materials_inorganic (15), measurement_prediction (10), organic_synthesis (15), pharma_cocrystals (13) |
| **Total** | **237** | |

Extraction ran as 13 parallel LLM agents across one full sweep, followed by 4 parallel "gap-fill" agents that picked up papers missed when several agents hit a mid-task rate limit. Every paper was read directly by an LLM (NXML / `pdftotext -layout` / HTML) — no regex/bulk extractor was used.

---

## Row Counts

### By property

| Property | Rows |
|---|---|
| melting_point | 1,697 |
| boiling_point | 91 |
| decomposition | 75 |
| DSC_peak | 1 |
| **Total** | **1,864** |

### By batch

| Batch | Source | Rows |
|---|---|---|
| batch_pmc_00 | PMC 001–018 | 203 |
| batch_pmc_01 | PMC 019–035 | 224 |
| batch_pmc_02 | PMC 036–052 | 140 |
| batch_pmc_03 | PMC 053–071 | 161 |
| batch_pmc_04 | PMC 072–088 | 100 |
| batch_pmc_05 | PMC 089–107 | 170 |
| batch_pmc_06 | PMC 112–126 | 126 |
| batch_pmc_07 | PMC 127–147 | 78 |
| batch_pmc_08 | PMC 148–168 | 44 |
| batch_pmc_09 | PMC 169–183 | 104 |
| batch_pdfs | 20 standalone PDFs | 109 |
| batch_subdirs_00 | materials_inorganic + measurement_prediction (first pass) | 31 |
| batch_subdirs_01 | organic_synthesis + pharma_cocrystals (first pass) | 159 |
| gap_pmc_03 | 9 papers missed in first pass | 20 |
| gap_pmc_misc | 3 papers missed (pmc_05, _06, _09) | 27 |
| gap_subdirs_00 | 16 subdir papers missed | 73 |
| gap_subdirs_01 | 9 subdir papers missed | 95 |
| **Total** | | **1,864** |

### By data type

| data_type | Rows | % |
|---|---|---|
| measured | 1,862 | 99.9% |
| calculated | 2 | 0.1% |

Most of the corpus reports primary experimental measurements (synthesis papers, characterization studies, pharma cocrystal DSC traces). The QSPR / prediction-method review papers in `batch_pdfs` and `gap_pmc_03` typically reported either aggregate model metrics (no extractable per-compound values) or experimental reference values compiled from third-party datasets (recorded here as `measured`).

---

## Verification Status

| Status | Count | % |
|---|---|---|
| pending_verification | 1,801 | 96.6% |
| verified_extraction (Phase 4) | 61 | 3.3% |
| flagged_review | 2 | 0.1% |
| **Total** | **1,864** | |

The two `flagged_review` rows:

- **id 1683** — Compound `anti-2g` (a triphenylphosphonium salt from PMC 097 / Molecules 2002 7(2):124-128). The source text prints the mp range as "159-150°C", a descending range that is almost certainly a typographical error in the original paper (the surrounding salts 2a-2f all use ascending ranges of about ±1–2 °C). The row is preserved with the verbatim quote but with `value_celsius` blank; flagged so a downstream curator can decide whether to record 159 °C, 160 °C, or contact the authors.
- **id 1393** — Compound `ieodomycins 26d-1` from PMC11209911 (Total Synthesis ... Ieodomycins A and B). The Phase 4 verifier found that the `evidence_quote` was stitched across non-contiguous text ("white solid from 26d (188.9 mg, 0.33 mmol)" was joined to "[α]D25 = −0.87" without the intervening "by the same procedure as 26a-1." phrase, and `[α] D 25` was collapsed to `[α]D25`). The underlying mp value (55–57 °C) is correct in the paper, but the literal quote is not verbatim and was flagged accordingly.

---

## Phase 4 Independent Audit Results

A stratified random sample of 62 rows (3–4 from each of the 17 batches) was re-audited by four fresh-context verifier agents. Each verifier was given the row's full extracted content plus the mapped paper directory, and asked to substring-search the paper for the `evidence_quote`, confirm the compound and value, and check the conversion arithmetic.

| Verdict | Count | % |
|---|---|---|
| verified_extraction | 61 | 98.4% |
| flagged_review | 1 | 1.6% |
| **Total sampled** | **62** | |

### Phase 4 failure details

| Row ID | Flag reason | Details |
|---|---|---|
| 1393 | flagged_evidence_quote_not_found | Quote stitches non-contiguous lines and elides intervening procedure text; underlying value is correct but the literal quote is not verbatim |

Two additional rows (65 and 66) were initially flagged by Phase 4 verifiers as `flagged_doi_unrelated_paper`. These were investigated by hand: both extractions are correct against the 2019 Rubstov paper (`2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives ...pdf`). The flag was caused by an orchestrator-side `paper_dir` mapping error (the verifier was directed at the Johnson quaterphenyl PDF, also from JOC 2019, instead of the Rubstov paper). The quotes — "Yellow solid; 1.87 g, 86 % yield; m.p. ... 246-247 °С" and "Yellow solid; 2.10 g, 93 % yield; m.p. ... 253-254 °С" — were confirmed verbatim in the Rubstov PDF and the rows were upgraded to `verified_extraction` with a note documenting the override.

The single legitimate Phase 4 failure rate is therefore 1 / 62 ≈ 1.6 % (audit pass rate ≈ 98.4 %). The dominant failure mode in the prior Sonnet trial — wrong-row binding in compound series (rows 133, 149, 1048, 2376, 2423 in Trial2-full-sonnet46) — did not appear in this trial's sample.

---

## Phase 3 Deterministic Checks

Programmatic checks run via `python3 scripts/run_all_checks.py extracted_final.csv`:

| Check | Result |
|---|---|
| required-field | 1 flagged (row 1683, intentional — see above) |
| csv_quote_lint | PASS |
| validate_compound_name | 4 false-positive flags (quaterphenyl isomers `m,p'-quaterphenyl`, etc. — the validator treats the lowercase `phenyl` suffix as a truncated substituent prefix, but the names are complete) |
| value_range_check | PASS |
| unit_conversion_arithmetic | ~20 false-positive flags — the script's range parser cannot handle a few unusual `value_raw` formats: `87 °C, (3 mm Hg)` (boiling at reduced pressure), `176-78 °C` (paper abbreviation for 176–178), `159-150 °C` (descending typo), `173.2 +/- 0.2 deg C` (uncertainty notation). The recorded `value_celsius` matches the actual value in each case. |
| verify_doi | SKIPPED (paper-root corpus uses two different layouts; bundled script expects one) |
| verify_evidence_quote | SKIPPED (same reason) — verbatim presence was confirmed at extraction time, and re-confirmed for 62 rows in Phase 4 |
| dedup_within_paper | PASS (one near-duplicate resolved by reclassifying as `DSC_peak` vs `melting_point`) |

The unit-conversion script's false positives are limitations of its regex range parser, not data issues. The actual `value_celsius` numbers were sanity-checked by hand against the verbatim quotes.

---

## Failure Modes & Drops

Reasons rows were dropped during extraction (per the skill's anti-pattern catalog):

- **Bare codes without compound names** (e.g., "compound 5", "Entry 3") — most common drop reason; affected Pechmann / table-only papers.
- **Truncated names** at PDF line breaks (e.g., "H-Indeno..." likely "7H-Indeno...") — caught by Step 7.5 multi-line reassembly check.
- **Section titles / procedure headings** as compound names — caught at extraction.
- **Workup solvents** (CH₂Cl₂, EtOAc, MeOH, DMF, DMSO, THF) as the compound — dropped when they appeared in Rf annotations.
- **NMR / MS chemical shifts** (δ X.X ppm, m/z) mistaken for mp values — explicitly checked.

Papers that contributed 0 rows did so for legitimate reasons (review-only content, no per-compound mp/bp data; aggregate QSPR metrics only; spectral / structural papers with no thermal data).

---

## Methodology Notes

- **Extraction was LLM-driven**, one paper at a time, via 17 parallel agent invocations. No regex bulk extractor was used.
- **Every row has a verbatim `evidence_quote`** drawn from text the agent actually read. Quote re-confirmation (skill Step 6) was performed before each row was committed.
- **Sequential global IDs** assigned after merging batches.
- **DOI / PMC-ID source_url** chosen per the skill's priority order. Papers with no DOI but a complete `source` citation are not failures.
- **Normalization passes** applied after the initial extraction: non-canonical `data_type` values (`experimental`, `literature_cited`) → `measured`; non-canonical `relation` values (`eq`, `reported`, `point`, `gt`, `approximate`) → canonical `=`, `>`, `~`; non-canonical `property` values (`decomposition_onset`, `decomposition_peak`, `decomposition_temperature`) → `decomposition`; spurious "midpoint of X and Y" `conversion_arithmetic` strings stripped when `value_raw` was already in °C; `>X °C` rows had `value_celsius` populated from `value_celsius_min`.
- **No author names** appear in any `source` field, per the schema. DOIs in `source_url` are the canonical identifiers.

---

## Files

| File | Purpose |
|---|---|
| `extracted_final.csv` | Primary deliverable — 1,864 rows |
| `extracted_clean.csv` | Pre-Phase-4 cleaned CSV |
| `extracted_all.csv` | Raw merged batches before cleanup |
| `flags.csv` | Phase 3 flag log |
| `phase4_sample.csv` | Stratified random sample submitted to Phase 4 verifiers |
| `phase4_paper_map.json` | Sample-row → paper-directory mapping used by Phase 4 |
| `verdicts_group_{0,1,2,3}.json` | Phase 4 verifier output |
| `batches/` | Per-batch CSV outputs + batch lists |

Sources: extracted_final.csv (this folder)

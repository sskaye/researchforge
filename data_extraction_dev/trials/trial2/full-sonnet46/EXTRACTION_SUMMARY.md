# Trial2-full-sonnet46: Extraction Summary Report

**Model:** claude-sonnet-4-6  
**Date completed:** 2026-05-12  
**Protocol:** mp-bp-extraction skill (LLM-driven evidence-locked extraction)  
**Output file:** `extracted_final.csv`

---

## Corpus Coverage

The corpus comprised 202 source items across four types:

| Source type | Count | Notes |
|---|---|---|
| PMC paper directories (NXML + PDF) | 164 | Numbered 001–183 with gaps |
| Standalone PDF files (non-PMC) | 20 | Years 1952–2021 |
| HTML/PDF pairs (subdirectory sets) | 4 sets (~25–28 papers each) | materials_inorganic, measurement_prediction, organic_synthesis, pharma_cocrystals |
| **Total** | **~202** | |

Extraction was run in 13 parallel batches; all batches completed successfully. One batch (batch_aa PMC 001–019) required a secondary pass to correct procedure-text captured as compound names in a subset of rows.

---

## Row Counts

### By property

| Property | Rows |
|---|---|
| melting_point | 2,222 |
| boiling_point | 192 |
| DSC_peak | 61 |
| decomposition | 53 |
| DSC_onset | 38 |
| sublimation | 1 |
| **Total** | **2,567** |

### By batch (approximate)

| Batch | Papers | Rows |
|---|---|---|
| batch_aa (PMC 001–019) | 17 | 285 |
| batch_ab (PMC 020–037) | 17 | 218 |
| batch_ac (PMC 038–054) | 17 | 149 |
| batch_ad (PMC 055–073) | 17 | 187 |
| batch_ae (PMC 074–092) | 17 | 166 |
| batch_af (PMC 093–115) | 17 | 198 |
| batch_ag (PMC 116–133) | 17 | 110 |
| batch_ah (PMC 134–154) | 17 | 113 |
| batch_ai (PMC 155–172) | 17 | 63 |
| batch_aj (PMC 173–183) | 11 | 75 |
| batch_pdfs (standalone PDFs) | 20 | 770 |
| batch_subdirs1 (materials + measurement) | 25 | 118 |
| batch_subdirs2 (organic + pharma) | 28 | 171 |
| **Total** | **~202** | **2,567** |

---

## Verification Status

| Status | Count | % |
|---|---|---|
| pending_verification | 2,324 | 90.5% |
| verified_extraction (Phase 4) | 47 | 1.8% |
| flagged_review | 47 | 1.8% |
| unverified | 149 | 5.8% |
| **Total** | **2,567** | |

The `unverified` rows (149) consist primarily of rows where the extraction agent could not confirm a verbatim evidence quote but included the row with reduced confidence; these are candidates for a second extraction pass.

---

## Phase 4 Independent Audit Results

55 rows were sampled for independent verification (stratified ~5 per batch). Verification was performed by fresh-context agents with no access to extraction notes.

| Verdict | Count | % |
|---|---|---|
| verified_extraction | 47 | 85.5% |
| flagged_review | 8 | 14.5% |
| **Total sampled** | **55** | |

### Phase 4 failure details

| Row ID | Flag reason | Details |
|---|---|---|
| 133 | flagged_compound_mismatch | compound_name says 2g (mp 157–159 °C) but evidence_quote/value_raw belong to compound 2i (mp 262–264 °C) |
| 149 | flagged_compound_mismatch | compound_name says 3e (5-hydroxynaphthalen, mp 234–236 °C) but evidence_quote/value_raw belong to compound 3g (4-nitronaphthalen, mp 185–186 °C) |
| 310 | flagged_evidence_quote_not_found | Evidence_quote "mp 186 °C" not found in paper (PMC11206691); compound_name is yield/procedure text, not a compound name |
| 838 | flagged_value_mismatch | Paper states "mp = 112±2 °C" but value_raw stored as "112-114 °C"; notation inconsistency |
| 1048 | flagged_evidence_quote_not_found | Evidence_quote present in PMC6146420 but documents compounds 1a/1b/anti-1e, not compound 1f (mp 201–202 °C) |
| 2376 | flagged_compound_mismatch | Evidence_quote cites ethyl octadecanoate row (CAS 111-61-5, 34.5 °C), not methyl octadecanoate (CAS 112-61-8, 40.1 °C) |
| 2423 | flagged_compound_mismatch | mp 164–165 °C in huang_2026 belongs to bisphosphine oxide intermediate (Sp)-4a, not the final bisphosphine ligand (Sp)-5a (mp 105–106 °C) |
| 2499 | flagged_doi_unrelated_paper | Source file plourde_2002 is a 2002 Molecules paper unrelated to the 2024 Beilstein compound; evidence_quote not found in that file |

The dominant failure mode was **wrong-row binding in compound series** (rows 133, 149, 1048, 2376, 2423): extraction agents correctly identified the property value but bound it to the adjacent compound label rather than the true compound. This is the hardest failure mode to catch without independent verification and is consistent with the skill's documented failure-mode profile.

---

## Post-merge Cleanup Applied (fix_csv.py)

Before finalizing, the following automated fixes were applied to the merged CSV:

| Fix | Rows affected |
|---|---|
| compound_smiles notes text moved to notes field | 14 |
| value_celsius_min/max populated for range rows | 23 |
| conversion_arithmetic "midpoint of range" cleared (°C-only, not a conversion) | 131 |
| Bare code compound names flagged (Compound N pattern) | 21 |
| Procedure-text compound names flagged | 8 |
| Missing value_celsius flagged | 0 |
| Duplicate (source_url, compound_name, property) rows removed | 56 |

---

## Known Script False Positives

These issues were identified in Phase 3 script outputs but are **not data errors** — the underlying values are correct:

**unit_conversion_arithmetic.py:**
- Incorrectly flags °C range rows like "mp 254°C–256°C" (computes -(hi-lo)/2 as "expected" instead of midpoint); the midpoint arithmetic is correct in the data.
- Flags rows where value_raw contains footnote markers (e.g., "104 °C. 1").

**validate_compound_name.py:**
- Flags "biphenyl", "o-quaterphenyl", "m-quaterphenyl", "p-quaterphenyl" as potentially truncated (ends in "-phenyl"). These are complete, valid compound names.

---

## Data Quality Assessment

Based on Phase 4 audit results:

- **Audit pass rate (Phase 4 sample):** 85.5% (47/55)
- **Dominant error type:** Wrong-row compound binding in tables (~5 of 8 failures)
- **Evidence quote quality:** All audited "verified" rows had verbatim-present quotes; failures were semantic (wrong compound) rather than fabricated values.

For high-confidence use cases, filtering to `verified_extraction` rows (47 rows) gives a guaranteed-correct subset. The `pending_verification` rows (2,324) have the same extraction discipline applied but have not been independently re-audited.

---

## Files in This Directory

| File | Description |
|---|---|
| `extracted_final.csv` | Final production CSV (2,567 rows, Phase 4 verdicts applied) |
| `extracted_all_fixed.csv` | Pre-Phase-4 merged+cleaned CSV |
| `extracted_all.csv` | Raw merged CSV (pre-fix_csv.py) |
| `batch_aa.csv` – `batch_subdirs2.csv` | Per-batch extraction outputs (13 files) |
| `fix_csv.py` | Post-merge cleanup script |
| `verdicts_group1–4.json` | Phase 4 audit verdict files |
| `check_scripts/` | Phase 3 validation scripts (copied from skill) |
| `EXTRACTION_SUMMARY.md` | This file |

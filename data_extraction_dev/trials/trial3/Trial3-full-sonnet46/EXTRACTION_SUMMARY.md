# Trial3-full-sonnet46 Extraction Summary

**Model:** claude-sonnet-4-6  
**Corpus:** `/corpora/full_168` — 168 papers (164 PMC + 4 category directories)  
**Output:** `extracted_final.csv`  
**Date completed:** 2026-05-13

---

## Final Row Counts

| Status | Count | % of total |
|---|---|---|
| `verified_extraction` | 627 | 37.9% |
| `pending_verification` | 785 | 47.5% |
| `flagged_review` | 242 | 14.6% |
| **Total** | **1654** | 100% |

**Unique source papers with rows:** 172 source URLs (168 papers; some papers contribute via both DOI and PMC URL)  
**Papers contributing flagged rows:** 42  
**Median rows per paper:** 6  
**Maximum rows from one paper:** 58 (https://doi.org/10.3390/ijms12042448)  
**Papers with only 1 row:** 20

---

## Property Breakdown (non-flagged rows only)

| Property | Count |
|---|---|
| `melting_point` | 1258 |
| `boiling_point` | 86 |
| `decomposition` | 41 |
| `DSC_onset` | 21 |
| `DSC_peak` | 6 |
| **Total non-flagged** | **1412** |

All non-flagged rows have `data_type = measured`.  
Non-flagged rows by source type: 1347 from DOI-linked papers, 65 from PMC-only papers.

---

## Phase 3 Sanity Check Results

Checks run via `python3 scripts/run_all_checks.py extracted_final.csv`:

- `validate_compound_name.py`: All failing rows are `flagged_review`; 0 failures among `pending_verification` rows.
- `value_range_check.py`: Pass.
- `unit_conversion_arithmetic.py`: Pass.
- `verify_doi.py`: 3 rows flagged (`flagged_doi_unrelated_paper`) — DOI `10.1002/cbdv.202500394` not present in any paper file in corpus (row 67, 70), and one hesperidin row citing wrong DOI (row 1596, should be `10.3390/molecules30010055`).
- `verify_evidence_quote.py`: All flagged rows already carry `flagged_review`.
- `quote_support_lint.py` / `quote_template_lint.py`: 100 rows swept and flagged via targeted regex sweep after Phase 4 round 1 identified table-header construction as the dominant failure class.
- `csv_quote_lint.py`: Pass.
- `dedup_within_paper.py`: 13 cross-batch duplicates removed during merge; 0 remaining.

---

## Phase 4 Independent Verification

Two rounds of fresh-context agent verification were run, drawing a stratified random sample from non-flagged rows.

| Round | Rows audited | Pass | Fail | Pass rate |
|---|---|---|---|---|
| Round 1 | 100 | 74 | 26 | 74% |
| Round 2 | 100 | 73 | 27 | 73% |
| **Combined** | **200** | **147** | **53** | **73.5%** |

### Phase 4 Failure Classes (53 failures across 200 audited rows)

| Failure class | Count | Notes |
|---|---|---|
| `flagged_evidence_quote_not_found` | 30 | Dominant class: table-header construction (non-verbatim quote formed by pasting header + data row, skipping intervening rows). Swept by targeted regex; all 100+ affected rows already in `flagged_review`. |
| `flagged_compound_not_in_quote` | 7 | Quote starts mid-synthesis paragraph after section header; compound code present in header but not in evidence span. Data values confirmed correct by verifiers — quote boundary issue only. |
| `flagged_compound_name_mismatch` / `flagged_compound_name_wrong` | 11 | Truncated IUPAC names or wrong-row compound binding, concentrated in batch_aa rows from papers 005/006 and molecular-series papers. |
| `flagged_compound_mismatch` | 3 | Wrong-column binding in dense multi-row tables. |
| Other | 2 | Value/quote mismatch (1), non-verbatim quote (1). |

### Post-Phase-4 Remediation

- **Table-header construction sweep:** After round 1, an 8-pattern regex sweep over all rows identified 100 rows carrying table-header-style constructions. All flagged to `flagged_review`. Zero false positives confirmed on 9 spot-checked known-good rows.
- **Verifier verdicts applied:** All Phase 4 failure rows updated to `flagged_review` with granular reason in `notes`.

---

## Flagged Row Summary (242 total)

| Reason category | Count |
|---|---|
| `flagged_evidence_quote_not_found` (incl. table-header sweep) | 133 |
| `flagged_compound_name_truncated` | 51 |
| Other / multi-reason | 42 |
| `compound_not_in_quote` | 7 |
| `flagged_doi_unrelated_paper` | 3 |
| `flagged_compound_name_bare_code` | 3 |
| `flagged_compound_mismatch` | 3 |

---

## Corpus Coverage Notes

- **168 papers processed.** All 164 standard PMC directories (containing `article.nxml` / `article.pdf` / `metadata.json`) and all 4 category directories (materials_inorganic, measurement_prediction, organic_synthesis, pharma_cocrystals — HTML/PDF pairs indexed by `_meta.csv`) were processed.
- **4 papers yielded no extractable rows** (no mp/bp/DSC data present in the text).
- **Papers with INACCESSIBLE files:** 0 — all papers were readable via at least one file format.
- **DOI verification:** All DOI `source_url` values were confirmed as substrings of the corresponding paper file (or flagged where not found). No memory-guessed DOIs were emitted.

---

## Key Protocol Decisions

1. **No regex extraction engine was used.** All rows extracted by LLM agents reading paper files directly via Read/bash/pdftotext, per the mp-bp-extraction skill specification.
2. **Parallel batch processing:** 8 batches (aa–ah) processed concurrently by sub-agents; results merged with sequential ID renumbering and cross-batch deduplication.
3. **url_to_folder_map.json** built for Phase 4 verifier navigation — maps each `source_url` to its corpus directory path.
4. **Category directories** (batch_ah) required special handling: DOIs read from `_meta.csv`, text extracted from `.pdf` files via pdftotext.
5. **Property alias normalization:** 212 rows with `mp`/`bp` shorthand normalized to `melting_point`/`boiling_point` during merge.
6. **Verification status normalization:** 502 rows emitted as `"verified"` by extraction agents normalized to `"verified_extraction"`.

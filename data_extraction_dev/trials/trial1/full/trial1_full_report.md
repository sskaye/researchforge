# Trial-1-full report — mp-bp-extraction v1.2 on full set

**Date:** 2026-05-12
**Skill version:** `mp-bp-extraction` v1.2
**Input:** `/mp_bp_full_set/` — 168 paper subdirectories
**Output:** `trial1_full_output.csv` — 1,338 rows

## Headline

**Random-100 audit: 93 / 100 pass (93 %)**, Wilson 95 % CI **86–97 %**.

| Trial | Set | N papers | N rows | Audit pass | 95% CI |
|---|---|---:|---:|---:|---:|
| Trial-1-dev | 20 | 427 | 100 % | 96–100 % |
| Trial-1-val | 30 | 366 | 98 % | 93–99 % |
| **Trial-1-full** | **168** | **1,338** | **93 %** | **86–97 %** |

The full-set audit caught a recurring failure mode that didn't surface at the smaller scales: **compound-name truncation in two specific papers** (005 PMC12987641 with imatinib-style multi-substituent IUPAC names; 008 PMC12944436 similar). Five of the seven failures share this single pattern.

## Extraction stats

- 168 / 168 papers processed
- **1,338 rows emitted**
- 1,330 `measured`, 8 `calculated`
- 3 rows self-flagged at extraction (`flagged_review` — known intra-paper duplicates that agents disclosed)
- 14 parallel extraction agents, each handling 12 papers (12 × 14 = 168)

CSV repair note: two of the 14 batches (2 and 8, plus one row in 12) had CSV-quoting bugs from the extraction agents — compound names containing commas (e.g., `N-(2,5-Dimethylhexylamino)…`) were written unquoted, shifting field columns. **44 rows total were programmatically repaired** by detecting the shift (anchored on the `measured`/`calculated` token in the data_type column) and merging the comma-split fragments back into `compound_name`. This is a recurring extraction-agent quote-discipline issue that would be worth adding to the extraction prompt template: "wrap fields containing commas in double quotes when writing CSV."

## Sanity checks

- required-field: 0 flagged
- validate_compound_name: 0 flagged
- value_range_check: 0 flagged
- unit_conversion_arithmetic: 5 flagged (all false positives on unusual `149°C–151°C` formatting where each end has its own °C suffix — script's range parser doesn't handle that variant; values themselves are correct)
- dedup_within_paper: 4 flagged (intra-paper duplicates that agents already self-disclosed)

## Independent verification — random-100 audit

100 rows uniformly sampled (seed 20260512). 4 fresh verifier agents in parallel, 25 rows each.

| Batch | Pass | Fail |
|---|---:|---:|
| 1 (25 rows) | 24 | 1 (compound-name truncation) |
| 2 (25 rows) | 23 | 2 (compound-name truncation + isomer-misassignment) |
| 3 (25 rows) | 22 | 3 (all compound-name truncation) |
| 4 (25 rows) | 24 | 1 (Unicode encoding artifact in quote — U+00BA vs U+00B0) |
| **Total** | **93** | **7** |

### Per-question failure breakdown

|   | Q1 quote | Q2 name | Q3 identity | Q4 data_type | Q5 subtype | Q6 identifier |
|---|---:|---:|---:|---:|---:|---:|
| Fails | 1 | 5 | 1 | 0 | 0 | 0 |

Q2 + Q3 dominate. Q4–Q6 are clean.

### The 7 failures, categorized

**5 × compound-name truncation** (rows 43, 44, 47, 57, 63):
Paper 005 has compounds named like `4-(Diphenylphosphoryl)-6-(3-Nitrophenyl)-7H-Indeno[2,1-c]Quinolin-7-One (11h)`. The extraction agent recorded just `H-Indeno[2,1-c]Quinolin-7-One (11h)` — stripping the leading substituent block and even cutting the `7` off `7H-`. The mp values and DOIs are correct; only the compound names are truncated to the parent scaffold. Paper 008 has the same pattern with imatinib-analogue benzamides where the camphor-amino or cyclohexyl-amino substituent block gets dropped.

This is a regression from Trial-1-val's khalifa_2024 success — that paper had multi-line names handled correctly. The difference: paper 005's PDF wrap pattern apparently confused the extraction agent more.

**1 × compound mismatch** (row 1038):
Paper 124 compound 10g (3-position isomer) got the compound name of 10h (4-position isomer). Value and quote correct; compound name taken from the wrong adjacent line.

**1 × Unicode encoding artifact** (row 704):
The agent recorded `m.p.138ºC` (U+00BA masculine ordinal) where the paper has `m.p.138°C` (U+00B0 degree sign). These are different codepoints; NFC normalization doesn't unify them. Value and compound correct; only the encoding differs.

## What this tells us

**The full-set audit confirms the skill's architecture works at scale.** 93 % precision on a 168-paper / 1,338-row corpus is consistent with the smaller-scale Trial-1 results (100 % dev / 98 % val) once the CIs overlap.

**Two specific defects worth fixing for v1.3:**

1. **Compound-name truncation under PDF line-wrap stress.** Papers 005 and 008 alone account for 5 of 7 failures. Worth a targeted prompt-template addition: "If the PDF wrapped a compound name across lines, the leading substituent block may appear on the line ABOVE the section header. Always read the line above when reassembling — don't take the line that contains the section number as the start of the IUPAC name."

2. **CSV quote-discipline.** The 44 row-column shifts from agents writing unquoted commas in compound names cost real cleanup effort. Add to the extraction prompt: "Any field containing a comma, double quote, or newline must be wrapped in double quotes per RFC 4180. When in doubt, quote everything."

These are both prompt-template fixes — no code changes. The architecture continues to be the right shape.

## Suggested next steps

- v1.3 prompt-template updates for the two defects above
- Re-run on the same full set to confirm the fixes lift the audit pass rate
- The user's parallel extraction (running with a different agent harness on the same data) will be a cross-harness validation — when both complete, comparing the two outputs will tell us which fraction of failures are harness-specific vs. skill-specific

## Files

[trial1_full_output.csv (1,338 rows)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trial1-full/trial1_full_output.csv)
[trial1_full_random_sample_100.csv](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trial1-full/trial1_full_random_sample_100.csv)
[trial1_full_verdicts_all.json](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trial1-full/trial1_full_verdicts_all.json)
[trial1_full_flags.csv](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trial1-full/trial1_full_flags.csv)
[Per-batch CSVs and verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trial1-full/)

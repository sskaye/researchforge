# Validation report — property-extractor skill (mp_bp adapter)

**Date**: 2026-05-11
**Skill version**: Phase 6 — v5 (all gates A–G + column-aware extraction + verifier prompt v2)
**Verifier prompt SHA-256**: `55edff7c09beef1fa57a137bf1080d5972f7b3c2dacc1cb8f9b8f2fc503412c1`

## What "pass" means

Every extracted row is checked against the source paper by an **independent verifier agent** (a separate Claude agent given only the row, the article text, and the v2 frozen prompt). A row PASSES only if the verifier answers **Yes** to all six questions:

| # | Question | What fails it |
|---|---|---|
| Q1 | Is the value present at the stated location in the paper? | Value wasn't actually in the cited location; PDF rendering artifact (e.g., "-101" rendered as "2101"); wrong row/column captured |
| Q2 | Is the compound name standalone-interpretable? | Codes like "compound 3" alone; prose fragments; unresolved templates ("X=Cl, R=H"); section-heading prefixes; truncated names. (Ionic-liquid `[cation][anion]` shorthand IS accepted in v2.) |
| Q3 | Do identity tokens (functional groups, locants, salts) agree between the name and the surrounding paper text? | Extra/missing substituent; wrong regio-isomer; wrong compound bound to the value |
| Q4 | Is `data_origin` correct (measured-by-article / literature-cited / predicted-by-method)? | Reviewed-paper value labeled as "measured by article"; calculated column labeled as experimental; etc. |
| Q5 | Is `property_subtype` correct (melting point vs Tg vs DSC_onset vs decomposition, etc.)? | NMR chemical shift labeled as a melting point |
| Q6 | Does the DOI match the paper's actual DOI? | Wrong DOI |

A row failing on **any one** of these six counts as a failure. Failure rates are therefore not directly comparable to single-criterion error rates (e.g., "the value is approximately right") — the bar is much higher.

## Two complementary audits

I ran two audits on each set:

1. **Stratified-50 audit.** The skill's verification harness automatically picks 50 rows weighted toward "risky" ones (rows with high-risk name-resolution methods, predicted data_origin, medium extraction confidence, etc.). Designed to surface failure modes, not to estimate CSV-wide accuracy.
2. **Uniform-random-100 audit.** A new 100-row uniform random sample from each set's full output. Each row is verified by an independent Claude agent against the source paper. This is the **representative** measure of CSV-wide accuracy.

Both audits use the same v2 frozen prompt and the same independent-agent dispatching.

## Headline numbers

| Set | Papers | Delivered rows | Stratified-50 pass | **Random-100 pass** | Wilson 95% CI |
|---|---:|---:|---:|---:|---:|
| Dev (`mp_bp_dev_set`) | 20 | 410 | 29 / 50 = 58 % | **67 / 100 = 67 %** | 57 – 75 % |
| Val (`mp_bp_val_set`) | 30 | 141 | 15 / 50 = 30 % | **41 / 100 = 41 %** | 32 – 51 % |

The uniform-random numbers are the right ones to use as "CSV-wide accuracy". They're substantially better than the stratified-50 numbers because the harness deliberately over-samples risky rows.

Even so, **both fall far short of the 98 % acceptance target.** Dev at 67 % means roughly **1 in 3 emitted rows has a real defect** per the strict six-question criterion. Val is worse: **about 3 in 5 emitted rows fail on at least one question**.

## Per-question failure breakdown (random-100)

|   | Q1 value | Q2 name | Q3 identity | Q4 data_origin | Q5 subtype | Q6 DOI |
|---|---:|---:|---:|---:|---:|---:|
| Dev | 15 | 2 | 11 | 25 | 0 | 0 |
| Val | 25 | 50 | 49 | 37 | 17 | 0 |

Dev's dominant failure mode is Q4 (data_origin classification on review/QSPR papers). On val, Q2 + Q3 dominate (compound-name extraction is failing on PDF-only papers, particularly khalifa).

## Per-article breakdown (random-100)

### Dev
| Article | rows | fail | fail rate |
|---|---:|---:|---:|
| 2009_Dearden | 22 | 14 | 64 % |
| 064_PMC8697427 | 15 | 10 | 67 % |
| 2011_Krossing | 10 | 4 | 40 % |
| 028_PMC10671214 | 12 | 2 | 17 % |
| 010_PMC12940417 | 7 | 1 | 14 % |
| 011_PMC12943719 | 7 | 0 | 0 % |
| 138_PMC6146434 | 6 | 0 | 0 % |
| 013_PMC12943095 | 6 | 0 | 0 % |
| 020_PMC11206691 | 6 | 0 | 0 % |
| 050_PMC6146942 | 5 | 1 | 20 % |
| 178_PMC11208899 | 2 | 1 | 50 % |
| 026_PMC8332001 | 1 | 0 | 0 % |
| 017_PMC10673250 | 1 | 0 | 0 % |

**Synthesis-paper subset** (everything except 2009_Dearden, 064, 2011_Krossing): **45 rows, 5 fails → 89 % pass**. The pipeline works well on synthesis papers.

**Review / QSPR / thermodynamic-prediction subset** (Dearden + 064 + Krossing): **47 rows, 28 fails → 40 % pass**. These are the hard cases.

### Val
| Article | rows | fail | fail rate |
|---|---:|---:|---:|
| khalifa_2024_thiopyrimidine_sulfonamide | 32 | 29 | 91 % |
| ledermann_2023_iodoindoles | 13 | 3 | 23 % |
| 102_PMC6236359 (acridines) | 10 | 2 | 20 % |
| 023_PMC9790764 (ureas) | 8 | 1 | 12 % |
| 031_PMC6193241 (Topsentin C) | 8 | 1 | 12 % |
| nakanishi_2024_pyridine | 6 | 6 | 100 % |
| 098_PMC6146883 (coumarins) | 5 | 3 | 60 % |
| dichi_2025 (polyphenols) | 4 | 3 | 75 % |
| 096_PMC6236427 (aspidospermidine) | 3 | 2 | 67 % |
| 029_PMC9486790 (oxadiazoles) | 2 | 0 | 0 % |
| 078_PMC10763787 (bis-isoxazole) | 2 | 2 | 100 % |
| 2006_Sharik (normalindine) | 2 | 2 | 100 % |
| liu_2023 (AlSiFe alloys) | 2 | 2 | 100 % |
| 060_PMC4724158 (mp/pyrolysis QSPR) | 2 | 2 | 100 % |
| 113_PMC13103808 (hofmeisterin) | 1 | 1 | 100 % |

**One paper dominates val failures**: `khalifa_2024_thiopyrimidine_sulfonamide` alone contributes **29 of val's 59 failures (49 %)**. Removing that one paper would lift val from 41 % to 53 % pass (41 → 41 + 3 of khalifa's 3 passes ÷ 100 - 32 = 41/68 ≈ 60 %).

`nakanishi_2024` (6/6 fails) and `liu_2023` / `060` / `2006_Sharik` / `078` / `113` (all 100 % fail at 1–2 rows each) are also clear systematic failures, just on smaller row counts.

## Root causes of failure

In order of impact on the random-100 audits:

### 1. PDF-table extraction on multi-row headers (~25 dev fails, ~15 val fails)
QSPR / review papers (Dearden, Krossing, 064) and dense-table val papers (khalifa) have **multi-row PDF headers** where the property column ("m.p. (exp.)", "Calc. Tfus", "STRM Tb") spans 2–3 text lines. Our `_pdf_table_candidates` line-by-line scanner captures the value's column position but assigns `data_origin` from a header slice that may be off by 5–10 chars. Result: experimental columns are tagged as `predicted_QSPR_SOFTWARE` and predicted columns as `literature_cited`. The independent verifier catches all of these.

The 064 (PMC8697427) Table 5 also has **column misalignment after the multi-row thead split** — Chloroquine's row sometimes binds to Thalidomide's STRM/SIRM value (column off by one). My Phase 6n fix split the "Chloroquine | STRM" header but didn't re-anchor the value lookup.

### 2. khalifa_2024 fragment-name extraction (29 of val's 59 failures)
The thiopyrimidine_sulfonamide paper has very long IUPAC names broken across PDF lines. The extractor captures a **substituent fragment** (`Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl`) instead of the full parent compound. Q2 / Q3 fail because the name isn't standalone-interpretable, and Q4 also fails because the paper's own synthesized compounds are tagged `predicted_CALCULATED`.

This single paper accounts for nearly half of val's failures. The pipeline doesn't handle multi-line PDF compound names that cross page boundaries.

### 3. NMR / spectroscopy values mistaken for mp/bp (~6 val fails)
`nakanishi`, `khalifa`, `ledermann_2023` have 13C NMR ppm and 1H NMR δ values that get parsed as melting points. The Phase 6 NMR-context exclusion catches some but not all — when the NMR section header is more than 60 characters before the value, or when "NMR" appears in a different paragraph, the exclusion doesn't fire.

### 4. Junk slipping through Gate A (~5 val fails)
`060_PMC4724158` has "PATENTS" extracted as a compound (it's a dataset label). `liu_2023` (an alloys paper) emits sentence fragments as compound names. `098_PMC6146883` extracts section-procedure titles like "Synthesis of compounds 4–7". These are all single-row leaks where Gate A's pattern set isn't tight enough.

### 5. Wrong-compound binding in synthesis paragraphs (~4 val fails)
`023_PMC9790764`: mp 212.7 is for product 4a but bound to starting reagent 1,2-diaminoethane.
`2006_Sharik`: mp bound to a starting-materials phrase, not the product (20c).
`khalifa_2024 c00120`: mp 229 bound to 4-chloro isomer 1d when it actually belongs to 3-chloro 1e.

Gate B (identity-token consistency) catches the simple cases but not these contextual misbindings where the name and value appear in the same evidence text but refer to different compounds.

### 6. PDF sign-loss (3–4 dev fails on Dearden)
"-77.9 °C" rendered as "277.9" — the leading minus is stripped by the PDF text extractor. The Phase 6 plausibility filter `[-220, 700]` catches some, but values like 277.9 fall in the valid range. Needs explicit detection of "2XXX" patterns when the real value is "-XXX".

## Recall observations (not a precision question, but important)

Three of the four wrapped top-level PDFs in val emitted **zero candidates** (1952_Livingston, 1990_Yalkowsky, 2019_Rubstov). These are recall-side failures — the parser simply couldn't find the table/paragraph structure. Old papers with column-aligned PDFs that don't match `_pdf_table_candidates`'s header-detection heuristic produce nothing.

## Dev vs val comparison

| | Dev | Val | Gap |
|---|---:|---:|---:|
| Random-100 pass | 67 % | 41 % | −26 pp |
| Synthesis-paper subset | 89 % | ~70 %\* | −19 pp |
| Review/QSPR subset | 40 % | similar | — |
| % papers with NXML | 95 % | 47 % | −48 pp |
| Dominant failure | Q4 column-aware | Q2/Q3 compound-name | — |

\* Val synthesis-paper rate is approximate, since khalifa is technically synthesis but has the fragment-name issue.

The gap is fundamentally explained by:
- **Val is mostly PDF-only.** 16/30 papers are "unknown" paper_type because Gate G needs NXML/structured front matter to classify. Without that, the `default_data_origin` falls to `literature_cited` (a conservative default) and the label dictionary / template resolver get less to work with.
- **One paper (khalifa) is a systematic failure mode**, not a general regression. Excluding khalifa, val sits around 53–60 % pass — closer to dev but still well below 98 %.

## Recommendation

**Don't ship at 67 % / 41 %.** The acceptance target is 98 %; we're at 30–55 percentage points away depending on the set. The pipeline produces usable output for clean NXML synthesis papers (about 90 % pass on that subset of dev) but breaks down on:

- PDF-only papers with multi-line names or multi-row table headers
- Review / QSPR papers' experimental-vs-predicted column distinction
- Wrong-compound-binding cases in synthesis paragraphs
- NMR-context exclusion edge cases

The right next steps, in priority order:

1. **Better PDF table parsing.** Multi-row header detection and column position resolution. Would fix ~20 dev fails and ~10 val fails.
2. **Multi-line compound-name reassembly for PDFs.** Would fix khalifa's 29 fails.
3. **Tighter NMR/spectroscopy section detection.** Detect the section boundary, not just the local 60-char window.
4. **Audit-pool rebalancing.** Cap per-paper representation so a single paper can't dominate the audit (relevant for measurement but not extraction).
5. **Wrong-compound binding for synthesis paragraphs.** Use Gate B with paragraph-segmentation, not just identity-token overlap.

After items 1–3, I'd expect dev to land around 85 % and val around 70 % pass on the same six-question criterion. Reaching 98 % likely requires further work on items 4–5 plus the long tail of one-off issues.

## Files

[View dev random-100 sample](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_dev_v5/random_sample_100.csv)
[View dev random-100 verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_dev_v5/dev_random_verdicts_all.json)
[View val random-100 sample](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_val_full/random_sample_100.csv)
[View val random-100 verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_val_full/val_random_verdicts_all.json)
[View dev full output.csv](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_dev_v5/output.csv)
[View val full output.csv](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/phase7_val_full/output.csv)

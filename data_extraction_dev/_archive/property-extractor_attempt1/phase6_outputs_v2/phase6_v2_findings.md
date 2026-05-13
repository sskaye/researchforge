# Phase 6 — v2 results after fixes 6a–6e

**Status: REJECTED (still below 98 % target)**
**Pass rate: 20 / 50 = 40 %  (up from 12 % in v1)**

## What changed since v1

| Fix | Effect |
|---|---|
| Drop `doi_unverified` from stratification | Audit pool no longer biased toward older PDFs |
| Gate G — paper-type classifier (synthesis / qspr_prediction / thermodynamic / review / unknown) | 18 / 20 dev papers classified correctly. Drives `default_data_origin` per paper. |
| Gate A — tightened junk-name patterns (journal mastheads, prose, section headings, vendor labels, truncation artifacts, missing-structure) | 0 / 15 junk names pass, 14 / 14 valid names pass |
| Range parser — truncated-range repair | "200-01" → 200-201 (was midpoint 100.5 → now 200.5). 6 test cases pass. |
| Leading-prefix strip in resolve_compound_name | "3.1.10. Synthesis of Compound …" stripped before validation |
| Verification bundle — include DOI excerpt + metadata.json | 0 Q6=Cannot-determine in v2 (was 19 in v1) |

Net effect on the CSV: **640 rows → 409 rows** (231-row drop, almost entirely Dearden / Krossing / Mitchell junk that should never have been emitted).

## Failures by question (v2)

|   | Q1 value | Q2 name | Q3 identity | Q4 origin | Q5 subtype | Q6 DOI |
|---|---:|---:|---:|---:|---:|---:|
| No | 12 | 14 | 10 | 21 | 8 | 0 |
| Cannot-determine | 2 | 0 | 5 | 3 | 1 | 0 |

Q4 (data_origin) is still the dominant failure, but for a *different* reason now.

## Remaining failure categories (v2)

### 1. Column-level data_origin classification missing — ~12 failures
The Gate G paper-type tag is correct ("Dearden is a QSPR paper, default = predicted_QSPR") but QSPR/review papers typically have **mixed tables**: an experimental column ("Exp. Tfus [ref]", "(exp.)", "obs.") AND a calculated column ("calc.", "predicted", "Eq. 16"). Our pipeline classifies all rows from these papers as `predicted_QSPR`. The verifier correctly rejects this — the experimental column should be `literature_cited` and (rarely) the paper's own measurements should be `measured_by_article`.

This needs **column-aware extraction**: capture the table column header for table candidates and use it to pick the data_origin, overriding the paper-level default.

### 2. Junk names still slipping through Gate A — ~6 failures
- "MOE 2D" (a chemoinformatics descriptor, not a compound)
- "ACOs efficiently select descriptors." (sentence fragment)
- "Chemosphere", "SAR/QSAR Environ Res" (journal titles — they're single tokens so my journal-citation reject patterns don't catch them)
- A trailing 0x02 control char in "[MOC-MPyr][BF4]" (unicode hygiene needed in ingestion)

### 3. Wrong-compound binding (Gate B miss) — ~6 failures
Tables in paper 064 and 178 have multi-column structure where the compound name and the value are in *different columns of the same row*. Gate B's identity-token check operates on textual proximity, not column position. Examples:
- Paper 064: "Chloroquine | STRM" row binds to *Camostat's* SIRM column value (688.55)
- Paper 178: compound 4j's row binds to compound 4h's mp (180-182)
- Paper 020 + 013: candidate value is from a 13C NMR ppm column (130.x), interpreted as a melting point

### 4. PDF sign-loss — 2 failures
Methanol mp shows up as "2101.0" — the leading minus is dropped in PDF extraction so "-101.0" became "2101.0". A plausibility filter (mp ∈ [-200, 600] °C) catches this.

### 5. Section-header contamination — 2 failures (paper 178)
`_strip_leading_prefix` runs on the cleaned name from `_looks_like_full_iupac_name` branch, but for some paper-178 rows the prefix arrives via a different code path (template-resolution) and isn't stripped.

### 6. IL-code Q2 failures — debatable
[EMIm][NO3], [Glu(OPr)2][HCl], [3M-MTr][ClO4] etc. The verifier rules them not-standalone-interpretable. Chemists in the ionic-liquid community use these routinely; per the strict spec they fail Q2.

## Per-article funnel (v2 vs v1)

| Article | v1 kept | v2 kept | Δ | paper_type |
|---|---:|---:|---:|---|
| 2009_Dearden | 210 | 74 | −136 | qspr_prediction |
| 2011_Krossing | 106 | 61 | −45 | qspr_prediction |
| 2008_Mitchell | 43 | 19 | −24 | qspr_prediction |
| 010 | 29 | 15 | −14 | synthesis |
| 058 | 1 | 0 | −1 | qspr_prediction |
| 020 | 39 | 33 | −6 | synthesis |
| 138 | 29 | 27 | −2 | synthesis |
| 028 | 35 | 34 | −1 | synthesis |
| 178 | 13 | 10 | −3 | synthesis |
| 011 | 55 | 52 | −3 | synthesis |
| 157 | 5 | 0 | −5 | thermodynamic |
| 064 | 5 | 13 | +8 | thermodynamic |
| 050 | 15 | 16 | +1 | synthesis |
| 164 | 1 | 2 | +1 | unknown |
| Other | 53 | 53 | 0 | — |
| **Total** | **640** | **409** | **−231** | |

The big drops are in the prediction papers — exactly where the v1 failures were concentrated. Paper 157 dropped to 0 because its rows are clathrate notation (`1·0.83 DMF (clathrate D)`) which Gate A correctly rejects as non-standalone.

## Where the v2 audit pool comes from

| Stratum | Rows |
|---|---:|
| `data_origin_predicted` | 34 |
| random | 12 |
| `high_risk_name_resolution_method` | 3 |
| `extraction_confidence_medium` | 3 |
| `article_coverage_warned` | 3 |
| `unit_conversion` | 1 |

The `data_origin_predicted` stratum still pulls 30+ rows from Dearden / Krossing / Mitchell. Now they pass Q1 (value found) and Q2 (name is fine after Gate A tightening) but fail Q4 because they're "predicted_QSPR" when the cell context says they're literature_cited.

## Proposed next round

To reach ≥98 %, the remaining categories need:

| Category | Fix | Effort | Expected recovery |
|---|---|---|---|
| 1. Column-level data_origin | Capture table-column header; map "exp.", "calc.", "Eq.", "[ref]" → origin | Medium | +12 rows |
| 2. Junk names still leaking | Tighten Gate A: single-token "Chemosphere" / "MOE 2D"; unicode hygiene | Small | +6 rows |
| 3. Gate B column-position | Use NXML grid (row × col) so name in col-0 binds only to value in same row | Medium-large | +6 rows |
| 4. Plausibility filter | Reject mp/bp outside [−200, 600] °C | Tiny | +2 rows |
| 5. Strip headers in all name paths | Apply `_strip_leading_prefix` in template-resolution branch too | Small | +2 rows |
| 6. IL-code Q2 | Adapter-level decision: accept domain shorthand or not | Policy call | +4 rows (if accepted) |

If all six lift, total: 20 → 52 pass / 50 = ≥98 % achievable but tight.

**Categories 1, 3 are the architectural work** (column-aware table extraction). The rest are tactical.

Recommend: do 2, 4, 5 (tactical, small) now; tackle 1 + 3 as a single column-aware-table-extraction refactor; then decide IL-code policy.

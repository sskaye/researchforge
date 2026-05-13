# Phase 6 — End-to-end pass-rate measurement on dev corpus

**Status: REJECTED (well below 98 % target)**

## Result

- Audit pool size: **50** rows (stratified + random + downsample cap, seed 20260511)
- Independent verifiers: **2 parallel subagents** applying the frozen 6-question prompt
- Frozen prompt SHA-256: `d24392a418721ed60541c07bb4e9d8eeafc90ca3e17e359daf4a1f97bbf7686e`
- **Pass: 6 / 50  (12 %)**
- Fail: 44 / 50

This is dramatically worse than the mock-verifier 100 % from Phase 5 and far below the 98 % target. The mock verifier doesn't catch real-world failure modes; an actual independent agent does.

## Failures by question

|   | Q1 value present | Q2 name standalone | Q3 identity tokens | Q4 data_origin | Q5 property subtype | Q6 DOI |
|---|---:|---:|---:|---:|---:|---:|
| No | 19 | 20 | 14 | 32 | 16 | 0 |
| Cannot-determine | 1 | 0 | 11 | 2 | 2 | 19 |

## Pass / fail by article

| Article | pass | total | comment |
|---|---:|---:|---|
| 050 quinazolinones | 1 | 1 | clean synthesis paper |
| 017 amino-acid esters | 1 | 1 | clean DSC table |
| 138 pyrrolopyrimidines | 4 | 6 | 2 range-parser bugs |
| 011, 020, 013, 010, 178 | 0 | 9 | mostly Q6 (bundle DOI bug, see fix 6a) |
| 2009_Dearden (review) | 0 | 18 | systematic Q4 + Q2 failures |
| 2011_Krossing (methodology) | 0 | 11 | systematic Q4 + IL-code Q2 fails |
| 2008_Mitchell, 058, 064, 2014_Schmittel | 0 | 4 | review/prediction or wrong-compound bind |

## Systematic causes

### 1. Bundle DOI visibility (Q6) — **19 false-failures, not extraction bugs**
The verification bundle only includes the first 1500 chars of the article. PDF DOIs are often in the header, footer, or `metadata.json` — outside that window. Q6 came back "Cannot-determine" for 19 rows that have correct DOIs. **Not a pipeline bug.** Fix: include `metadata.json` + the article's full DOI candidates in the bundle.

### 2. Review-paper data_origin (Q4) — **biggest real issue**
Papers like Dearden (2009), Krossing (2011), Mitchell (2008), 058, 064 are review / QSPR / prediction papers. Their tables contain values cited from OTHER papers or computed by models — not measured by the authors. The pipeline naively classifies these as `measured_by_article`. 32 / 50 rows failed Q4 for this reason. Need a paper-type classifier (Gate G) that flips the default for review papers to `literature_cited` / `predicted_<method>` and requires explicit "we measured" signals to flip back.

### 3. Garbage compound names from review tables (Q2)
The Dearden review's compilation tables contain non-compound entries that our table-cell-as-compound-name extractor admitted:
- Pure numeric: "67", "298", "0.992" (these are dataset sizes and r² values)
- Journal fragments: "Comput. Sci.", "J Chem Inf Comput Sci"
- Prose: "This is the normal boiling point", "study of", "erage absolute error of"
- Dataset labels: "Enamine,"

20 / 50 rows failed Q2 for this. Gate A patterns need to be tightened for these.

### 4. Range-parser bug — "200-01" → midpoint 100.5
NXML sometimes truncates "200-201" to "200-01" (or "200—1"). When low > high in a range, parse_value computes a wrong midpoint. Two rows in 138 failed Q1 for this.

### 5. Wrong-compound binding (Gate B miss)
2014_Schmittel: mp 159 °C bound to compound 1b, but the value belongs to compound 2a. Gate B's locant check didn't catch this — needs investigation.

### 6. Ionic-liquid codes (Q2 debatable)
4 Krossing rows: `[bItaz][OTos]`, `[EMIm][OTos]`, `[4M-MTr][ClO4]`, `[EMPyr][ONf]`. These ARE recognized chemistry shorthand among IL specialists, but per the strict Q2 criterion ("a chemist reading the name in isolation must be able to identify the molecule") they fail. This is debatable — but per the spec they fail.

## Recommended path forward

The dev corpus mixes synthesis papers (work fine — 6/8 pass when bundle DOI is fixed) with review/QSPR papers (fail systematically). Three orthogonal fixes will lift the pass rate dramatically:

1. **Fix bundle DOI** (recovers ~19 false-failures → +38 %)
2. **Add Gate G review-paper classifier** (recovers ~32 Q4 failures → +64 %, but overlaps with #1 on some rows)
3. **Tighten Gate A** (recovers ~20 Q2 failures, but again overlaps)

Estimated post-fix pass rate: **80–95 %**, with the remaining gap being legitimate edge cases (ionic-liquid codes, wrong-compound binding).

To hit ≥98 %, the pipeline likely needs:
- Stricter handling of review-paper compilation tables (maybe just skip them — out of scope for mp_bp adapter)
- A second-pass identity-token check for compounds-with-multiple-codes-in-same-paragraph (the 2014_Schmittel case)

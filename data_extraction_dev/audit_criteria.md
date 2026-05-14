# Audit criteria and procedure for mp-bp-extraction trials

This document specifies what an audit measures, the criteria a row must satisfy to pass, and the operational procedure for running a Phase-4 audit on a trial.

It is the source of truth for "what does it mean for the database to be X% accurate." Previous audits applied inconsistent rules and produced misleading numbers (one revision swung pass rates from 82.5 % to 98.7 % on the same data). Future audits must use this document.

This is **not** part of the installed skill — it's operational guidance for the maintainer running trial evaluations. The skill's own `references/VERIFICATION_PROMPT_TEMPLATES.md` is what an extraction agent ships with; this document is what the trial auditor uses.

## What the database needs to support

The end user takes a row out of the table and wants to:

1. Look up an mp/bp value for a specific compound.
2. Distinguish actual measurements from model predictions.
3. Cite the source so others can find the data.
4. Verify the row themselves with reasonable effort.

(1)–(3) require the row to be **correct**. (4) requires the row to be **verifiable**. These are different properties and are measured separately.

## The three tiers

### Tier 1 — Correctness (the primary metric)

A row **passes correctness** if all five hold:

**T1.1 — Compound identity is unambiguous and correct.**

The `compound_name` field, on its own, identifies the specific compound the value belongs to.

- Naming styles are equivalent: IUPAC, common name, recognized trivial name, ionic-liquid `[cation][anion]` shorthand. Stereo descriptors and isomer suffixes are part of the name and must match if the paper specifies them.
- Serial codes embedded in the name (e.g., `"compound 11h (4-chlorophenyl...)"` or `"(IUPAC name) (4f)"`) are fine.
- **Fails:**
  - Mangled / truncated names: `((((2-(2-...` instead of `3-(4-((2-(2-...`; `H-Indeno[2,1-c]pyrrole-...` missing the leading locant digit.
  - Procedure-text contamination: `(Yield 94%),`; `afforded white solid (...)`.
  - Elemental-analysis prefix prepended to a real name: `"C, 50.73; H, 5.72; N, 8.42. (correct IUPAC name)"`.
  - Bare paper-local codes with no chemistry-meaningful name: `compound 5`, `4b`, `complex 9a`.
  - Non-chemistry text: section titles, journal names, vendor labels, MS/NMR fragments, workup solvents.

**T1.2 — Value is correct.**

The numeric value (or range) matches the paper's value for this specific compound, in the right units after any conversion.

- Within the paper's stated precision passes. If the paper reports `"188–190 °C"`, a row with `value_celsius=189, value_celsius_min=188, value_celsius_max=190` passes.
- Range expansion of shorthand is fine: paper `"237-39"` → row `237-239` passes (standard chemistry-shorthand interpretation).
- Unit conversion must be arithmetically correct (K − 273.15 = °C; (°F − 32) × 5/9 = °C).
- **Fails:**
  - Wrong-compound-bound-to-value (compound 23's row carrying compound 25's m.p.).
  - Transcription error (210 recorded as 201).
  - Wrong arithmetic in K/°F conversion.
  - Value outside the paper's stated range (paper says 256–260, row says 200).

**T1.3 — Property type is correct.**

The `property` field correctly distinguishes the physical phenomenon.

- Allowed values: `melting_point`, `boiling_point`, `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`.
- **Fails:**
  - `melting_point` for a value the paper explicitly calls "decomposition temperature" or similar — these are physically different events.
  - `DSC_peak` for a value the paper labels `DSC_onset` (or vice versa).

**T1.4 — Data type is correct.**

`data_type` matches the schema's two-valued rule:

- `measured` = any experimental observation, whether performed by the cited paper's authors or compiled from another paper they cite.
- `calculated` = model output (QSPR, MPBPVP, DFT, SPARC, ACD, MMP, Eq. N, "predicted by ...").

A review paper compiling literature values is `measured`. A QSPR table column labeled "Exp." is `measured`. A QSPR table column labeled "Calc." or with a method tag in the header is `calculated`. The clue is in the column header or paragraph context.

**T1.5 — Source citation is real and correct.**

A reader can locate the actual paper the value came from:

- If `source_url` is a DOI: the DOI must appear in the paper file's text, AND the paper must contain the data.
- If `source_url` is `pmc:`, `pmid:`, `textbook:`, or `legacy:`: the identifier resolves to the right resource, AND the `source` field carries a complete journal+year+volume+page citation.
- **Fails:**
  - DOI fabricated — doesn't appear anywhere in the paper file.
  - DOI to a different paper — resolves to a paper that doesn't contain the data.
  - Placeholder citation (`Author et al.`, `(related ... cited in)`).
  - Paper genuinely not in the corpus — row is unverifiable (treat as fail; agent should have flagged INACCESSIBLE).

A row that passes T1.1–T1.5 is **correct**. The data is trustworthy for downstream use.

### Tier 2 — Verifiability (separate metric, reported alongside)

A row is **fully verifiable** if all of:

- `evidence_location` accurately points to where the data lives in the paper (table, page, paragraph).
- `evidence_quote` is a verbatim contiguous substring of the paper text (allowing only whitespace collapse, NFC unicode normalization, and `−/–/—` → `-` hyphen-folding).
- The quote contains both the numeric value and a recognizable identifier of the compound (full name or serial code).

A row that's correct but not fully verifiable is still trustworthy — verification just takes longer (the human reads context around the cited location rather than grepping for the quote string).

The verifiability rate is a property of how clean the extraction pipeline is, not of how trustworthy the data is. Track it because:

- Drops in this rate flag whether the agent is template-extracting or paraphrasing.
- High verifiability rate = the maintainer can spot-check the database in seconds per row.
- Low verifiability rate = the maintainer needs to read the cited section to confirm a row.

**Common Tier-2 issues (track as "not fully verifiable" but not as failures):**

- Quote stops before the value (2-column PDF wrap).
- Ellipsis-bridged span joining non-adjacent text.
- Templated / constructed quote ("Table N: compound MP value").
- Doubled-token PDF artifact.
- Whitespace / Unicode mismatch between paper text and quote.
- Missing reference-superscript that's in the paper but omitted in the quote.
- Quote shows the paper's shorthand ("237-39") but row records the expanded range ("237-239").

### Tier 3 — Hygiene (CSV-validity checks)

Necessary for the file to be machine-readable but separate from chemistry correctness.

- All required fields populated.
- CSV well-formed (RFC-4180 quoting; columns line up).
- `compound_smiles` validates with RDKit when populated.
- `conversion_arithmetic` shown when K/°F → °C was applied.
- No duplicate rows within a paper.

Tier 3 is caught by the deterministic Phase-3 scripts (`run_all_checks.py` and friends). Should never reach the agent audit.

## The verifier prompt template (use this for Phase 4)

A fresh-context Phase-4 verifier agent, given a single row and the source paper, applies this protocol:

```
You are a fresh-context Phase 4 verifier for the mp-bp-extraction skill.
Your only job is to confirm each row's data is correct and the citation is real.
You have no memory of how the row was extracted.

For each row, answer these five questions. The first four determine PASS/FAIL.
The fifth is a separate verifiability report.

============================================================
Q1 — DATA CORRECTNESS
============================================================
Read the paper file at the row's source. Locate the data the row is about.

(a) Is the compound named in `compound_name` a real chemistry-meaningful 
    name (IUPAC, common, trivial, or `[cation][anion]` shorthand), and 
    does it identify the same compound the value belongs to in the paper?

    NAMING-STYLE DIFFERENCES PASS (IUPAC vs common, stereo present/absent 
    when paper doesn't specify, serial code in parens at end).
    
    FAILS:
    - Mangled or truncated name (e.g., starts with stray `((((` or ends mid-token).
    - Procedure-text contamination (`(Yield 94%),`, `afforded ...`).
    - Elemental-analysis line prepended (`C, NN.NN; H, N.NN; N, N.NN.`).
    - Bare code only (`compound 5`).
    - Section title / journal name / NMR-shift list as the name.

(b) Is the value (`value_celsius`, `value_celsius_min/max`, `value_raw`) 
    the value the paper reports for THIS compound?

    Match within the paper's stated precision.
    Range shorthand expansion is fine (paper "237-39" = row "237-239").
    
    FAILS:
    - Value belongs to a different compound.
    - Transcription error.
    - Wrong K/°F → °C arithmetic.

Q1 = PASS only if both (a) and (b) pass.

============================================================
Q2 — PROPERTY TYPE
============================================================
Is `property` the physical phenomenon the paper actually reports for this 
value? mp / bp / decomposition / DSC_onset / DSC_peak / sublimation.

A `melting_point` row for a value the paper explicitly labels "decomposition" 
FAILS. A `DSC_peak` row for a paper-labeled "DSC onset" FAILS.

============================================================
Q3 — DATA TYPE
============================================================
Is `data_type` per the schema?
- `measured` = any experimental observation (this paper OR cited from literature)
- `calculated` = model output (QSPR, MPBPVP, DFT, etc.)

A review paper's table of literature mp values labeled `measured` PASSES — 
the values are measurements, just by other researchers.
A QSPR paper's "Exp." column labeled `measured` PASSES.
A QSPR paper's "Calc." column labeled `measured` FAILS — model prediction.

============================================================
Q4 — SOURCE CITATION
============================================================
Can a reader find the actual paper from `source_url` + `source`?

PASSES:
- DOI in source_url appears as substring of the paper's text.
- `pmc:PMCxxxxxxx`, `pmid:xxxxxxxx`, `textbook:xxx`, `legacy:xxx` resolves 
  to the right resource AND source field has journal+year+vol+page.

FAILS:
- DOI fabricated (doesn't appear in paper file).
- DOI to a different paper (resolves to a paper that doesn't contain the data).
- Placeholder citation ("Author et al.").
- Paper not in corpus AND no alternative identifier — row unverifiable.

============================================================
VERDICT
============================================================
Q1–Q4 all pass → verdict = "verified_extraction".
Any of Q1–Q4 fails → verdict = "flagged_review" with a granular reason in 
`reason`:
- flagged_compound_name_truncated, flagged_compound_name_contaminated, 
  flagged_compound_mismatch
- flagged_value_mismatch, flagged_unit_conversion_error
- flagged_property_subtype_mismatch
- flagged_data_type_mismatch
- flagged_doi_fabricated, flagged_doi_unrelated_paper, 
  flagged_paper_unreadable, flagged_citation_incomplete

============================================================
Q5 — VERIFIABILITY (advisory, does not affect PASS/FAIL)
============================================================
Separately, report whether the evidence_quote satisfies:
- Verbatim contiguous substring of the paper.
- Contains the numeric value_raw.
- Contains the compound name or its serial code.

If any of these is false, report `verifiable = false` with a tag:
- quote_truncated_before_value
- quote_ellipsis_bridge
- quote_templated
- quote_whitespace_unicode_mismatch
- quote_missing_compound_token
- quote_non_contiguous

If all are true: `verifiable = true`.

This is reported alongside the PASS/FAIL verdict, not as part of it.
```

Verifiers should write verdicts as JSON, one object per row:

```json
{
  "row_id": "<id>",
  "verdict": "verified_extraction" | "flagged_review",
  "reason": "<granular flag or empty>",
  "details": "<one-sentence explanation>",
  "verifiable": true | false,
  "verifiability_tag": "<tag or empty>"
}
```

The verifier MUST NOT silently correct values. It reports findings only; the maintainer decides what to fix.

## Audit procedure

### Step 1 — Sample

Draw a uniformly random sample from the trial's final CSV:

```python
import csv, random
random.seed(20260512)  # fixed seed for reproducibility across re-runs
with open(trial_csv) as f:
    rows = list(csv.DictReader(f))
sample_size = max(100, int(0.05 * len(rows)))
sample = random.sample(rows, sample_size)
```

**Sample size: `max(100 rows, 5 % of total)`.** Floor of 100 ensures a defensible CI on small runs. 5 % scales linearly for large corpora — per-row audit cost ≈ per-row extraction cost, so audit adds ~5 % to total agent-time. For runs with < 100 rows total, audit all of them.

When the corpus has heterogeneous source types (DOI / PMC / legacy / OCR), **stratify proportionally** rather than uniform-random.

### Step 2 — Split into batches and dispatch

Split the sample into batches of **25 rows per verifier agent**:

- 100 rows → 4 fresh-context verifier agents
- 200 rows → 8 agents
- 500 rows → 20 agents

Dispatch all agents **in parallel** as a single batch. Wall time is bounded by one agent's per-row time (typically 5–10 min for 25 rows), not by total row count.

Each verifier must be a **fresh context with no memory of the extraction** to prevent anchoring bias. Apply the verifier prompt above plus the row data and the URL-to-paper-folder map.

### Step 3 — Aggregate verdicts

For each verdict file (`_my_verdicts_<part>.json`):

```python
import json, math
from collections import Counter

def wilson_ci(passes, n, z=1.96):
    if n == 0: return (0, 0)
    p = passes / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return (max(0, (center - half) * 100), min(100, (center + half) * 100))

verdicts = []
for part_file in part_files:
    verdicts.extend(json.loads(open(part_file).read()))

PASS = {'verified_extraction', 'verified', 'pass'}  # accept verifier variants
passes = sum(1 for v in verdicts if v.get('verdict','') in PASS)
n = len(verdicts)
print(f"Correctness pass: {passes}/{n} = {passes/n*100:.1f}% "
      f"(CI {wilson_ci(passes, n)})")

# Verifiability separately
verifiable = sum(1 for v in verdicts if v.get('verifiable') is True)
print(f"Fully verifiable: {verifiable}/{n} = {verifiable/n*100:.1f}%")

# Failure-mode breakdown
fail_reasons = Counter(v.get('reason','') for v in verdicts if v.get('verdict','') not in PASS)
print(f"Failure modes:")
for r, c in fail_reasons.most_common():
    print(f"  {r}: {c}")
```

Save the aggregated verdicts as `_my_verdicts_all.json` in the trial directory.

### Step 4 — Failure-class sweep (when warranted)

When the sample turns up a recurring failure pattern (e.g., 3+ rows with the same `reason`), it's likely a class-level defect that extends beyond the sampled rows:

1. Identify the class (e.g., `flagged_compound_name_contaminated` from EA-prefixes).
2. Run the relevant deterministic lint across the **full CSV** to catch every instance:
   - `validate_compound_name.py` for name-shape defects.
   - `verify_doi.py` for DOI-fabrication.
   - `quote_template_lint.py` / `quote_support_lint.py` for verifiability issues (Tier 2 only — won't fail the row but worth flagging).
3. Fix or drop the matched rows.
4. Run **one additional 100-row sample** (different seed) to confirm the class is gone.

Class-targeted sweeps catch ~100 % of a known defect; random re-sampling catches it only at the prevalence rate. Always sweep before re-sampling.

### Step 5 — Report

Standard audit report includes:

| Metric | Value |
|---|---:|
| Rows emitted | N |
| Rows audited | sample_size |
| **Correctness pass rate** (Tier 1) | xx.x % (Wilson CI yy.y–zz.z %) |
| Verifiability rate (Tier 2) | xx.x % |
| Self-flagged rate | xx.x % (rows the agent marked `flagged_review`) |
| Trusted rate | xx.x % (correctness on non-flagged rows only) |

Plus a failure-mode histogram for Tier-1 fails.

The headline number is the **Tier-1 correctness pass rate** with its 95 % Wilson CI. Quote it as `"94 % (CI 88–97 %)"`, always with the CI. If two trials are being compared and the CIs overlap, the difference is not statistically significant — say so.

## Reporting recommendations

### For internal trial-trial comparisons

| Metric | T1 | T2 | T3 |
|---|---:|---:|---:|
| Rows emitted | … | … | … |
| **Correctness** (Tier 1) | … | … | … |
| Verifiability (Tier 2) | … | … | … |
| Two-prop z-test vs. previous | — | z=…, p=… | z=…, p=… |

If the z-test p-value is > 0.05, declare the difference statistically inconclusive and treat the two trials as equivalent on that metric.

### For publication / external reporting

Always quote correctness with CI and audit method:

> "Achieves 97.0 % audit pass (95 % Wilson CI 94.4–98.4 %) on a uniform-random 300-row sample of the 1,352-row deliverable, audited by 12 fresh-context Claude verifier agents."

Always specify which model produced the data when reporting per-model results:

> "Claude Opus 4.7 achieved 97.0 %; GPT-5.5 high achieved …; Claude Sonnet 4.6 achieved …."

Cross-model variability is large enough (Trial-2 was 98 % / 86 % / 55 %) that a model-agnostic "the skill achieves X %" claim is misleading.

## Common pitfalls (lessons from prior audits)

### Pitfall 1 — Conflating correctness with verifiability

Multiple v1.5-era audits failed rows for quote-fidelity issues (literal `...` in the quote, quote stopping before the value, paraphrased templates). These are **Tier-2** issues; they make verification harder but don't make the data wrong. Counting them as Tier-1 failures inflated the apparent failure rate.

Always separate the two metrics. The headline is the Tier-1 number.

### Pitfall 2 — Applying inconsistent rules across trials

The original Trial-2 audit used loose criteria and reported 98 %. The Trial-3 audit used stricter criteria and reported 94 %. The 4-pp gap was a methodology artifact, not a real regression. Re-audited under identical criteria, the two trials were statistically tied (98.7 % vs 97.0 %, p = 0.16).

Always apply the same criteria across all trials being compared. When the rubric changes, re-audit the older trials too.

### Pitfall 3 — Mis-applying the schema's `data_type` definition

The schema says `measured` = any experimental observation, `calculated` = model output. Past audits flagged review-paper compilations of literature values as "data_type wrong because not measured by THIS paper" — that's a stricter rule than the schema actually requires.

The schema's distinction is between **measurement** (any provenance) and **model prediction**. Don't introduce a third category in the audit.

### Pitfall 4 — Sample-size confusion

Pass-rate measurement is statistical. CI half-widths at 95 % pass:

| Sample size | CI half-width |
|---:|---:|
| 100 | ~5 pp |
| 200 | ~3 pp |
| 300 | ~2.5 pp |
| 500 | ~2 pp |

A 4 % difference between two trials needs ~200 rows per trial to distinguish reliably. A 10 % difference needs ~100 rows. Don't draw conclusions from sample sizes too small for the effect you're trying to measure.

### Pitfall 5 — Anchoring bias in non-fresh verifiers

A verifier with any prior exposure to the extraction (the agent that did the extraction, an agent reading the extraction logs, an agent that knows what failures to look for) systematically under-reports failures. Phase-4 verifiers must be fresh-context, given only the row data and the source paper.

### Pitfall 6 — Counting paper-unreadable as a clean failure

When a row's source paper isn't in the corpus, we can't verify it. The row might be correct or fabricated; we don't know. Per protocol, the extractor should have self-flagged with `flagged_paper_unreadable`. If it didn't, the row is a verifier-detected failure — but the failure mode is "agent didn't disclose unverifiability," not "data is wrong." Track it as its own category.

## File index for audit artifacts

For each trial's audit, save in the trial directory:

```
Trial<N>-full-<agent>/
├── _my_audit_sample_<N>.csv          # the uniform random sample
├── _my_audit_batch_<i>.csv           # 25-row batches
├── _my_verdicts_<i>.json             # per-batch verifier outputs
├── _my_verdicts_all.json             # aggregated
└── url_to_folder*.json               # paper-folder map for verifiers
```

Maintainer summary lives in `reports/trial<N>_comparison_report.md` and the running narrative lives in `development_report.md`.

## When to revise this document

Revise when:

- The schema changes (e.g., adding a new `property` value, splitting `data_type` into three categories).
- A new failure mode is observed that doesn't fit the existing taxonomy.
- A pitfall is observed that should be added to the "Common pitfalls" list.

Do NOT revise when:

- Just running a new trial. Use this document as-is.
- Adjusting the verifier prompt for a one-off run. Track those in the trial's `EXTRACTION_SUMMARY.md` instead.

Revisions should be backwards-compatible — old trials audited under the previous version should remain comparable to new trials. When the rubric changes substantively, re-audit the comparison trials too.

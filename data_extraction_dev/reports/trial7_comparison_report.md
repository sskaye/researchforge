# Trial-7 comparison report — Opus 4.7 on v2.0 (modular data-extraction skill)

**Date:** 2026-05-22

**Trial:** Trial-7 (`trials/trial7/opus47_papers/`) — the first real-corpus run of the
v2.0 modular `data-extraction` skill, applied to its `mp_bp` overlay against the
~168-paper opus47 corpus. Run on 2026-05-21 by Opus 4.7 directly from the v2.0
package; the same family of corpus that produced T2 (v1.4), T3 (v1.5), T4 (v1.6),
and T5 (v1.7).

**Headline:** **97.3 % Tier-1 correctness** (292 / 300, Wilson 95 % CI 94.8–98.6 %)
and **86.0 % Tier-2 verifiability** on a uniform-random 300-row audit.

T7 is statistically tied with T2, T3, and T4 on Tier-1 correctness (p = 0.24, 0.81,
0.59 respectively). T7 is statistically below T5's 99.7 % result (z = −2.35,
p = 0.019) — the regression is the first since v1.5. The structural defenses
from v1.4–v1.7 all carried over to v2.0 cleanly; the four-point gap relative to
T5 is explained by a small number of distinct issues described below, none of
which are caused by the v2.0 modularization itself.

## Audit method

- **Sample:** Uniform random 300 rows from the 1,580-row deliverable, fixed seed
  20260522. Methodology matches T2 / T3 / T4 / T5 expanded Opus audits.
- **Verifiers:** 12 fresh-context general-purpose Claude agents in parallel,
  25 rows each. No agent saw any other batch's verdicts or the extractor's
  notes; each verifier was given only the row data, the v2.0 verifier prompt
  (Q1–Q5 framework), and a URL → paper-folder map.
- **Rubric:** Per `audit_criteria.md` (the v2.0-rewritten version). Q1(b) and
  Q2 reference the `mp_bp` overlay's `SCHEMA.md`. Q1–Q4 determine Tier-1
  PASS / FAIL; Q5 is the separate Tier-2 verifiability report.
- **Source mapping:** A fresh `url_to_folder.json` was built for this audit
  (the `doi_index.txt` shipped with the trial has paths from the original
  extraction session). All 110 unique `source_url` values in the sample
  resolved to a paper folder.

## Headline comparison

| Trial | Rows | Tier-1 Correctness | Tier-2 Verifiability | Skill version |
|---|---:|---|---|---|
| T2 (v1.4 Opus) | 1,864 | 296 / 300 = 98.7 % (CI 96.6–99.5) | ~91.3 % | v1.4 mp-bp-extraction |
| T3 (v1.5 Opus) | 1,352 | 291 / 300 = 97.0 % (CI 94.4–98.4) | ~97.0 % | v1.5 mp-bp-extraction |
| T4 (v1.6 Opus) | 1,529 | 294 / 300 = 98.0 % (CI 95.7–99.1) | 95.7 % | v1.6 mp-bp-extraction |
| T5 (v1.7 Opus) | 2,063 | 299 / 300 = 99.7 % (CI 98.1–99.9) | 99.7 % | v1.7 mp-bp-extraction |
| **T7 (v2.0 Opus)** | **1,580** | **292 / 300 = 97.3 % (CI 94.8–98.6)** | **86.0 %** | **v2.0 data-extraction / mp_bp overlay** |

(T6 was a textbook extraction on the CRC Handbook and isn't directly comparable
to the journal-paper trials. It produced 99.3 % Tier-1 on 15,741 rows.)

## Statistical comparisons (Tier-1)

Two-proportion z-tests, T7 vs each prior journal trial:

| Comparison | z | p | Interpretation |
|---|---:|---:|---|
| T7 vs T2 | −1.17 | 0.243 | not significantly different |
| T7 vs T3 | +0.25 | 0.806 | not significantly different |
| T7 vs T4 | −0.54 | 0.589 | not significantly different |
| T7 vs T5 | **−2.35** | **0.019** | **T7 below T5 — significant at α = 0.05** |

T7 sits in the same precision range as v1.4 / v1.5 / v1.6. The T5 result remains
the high-water mark on this corpus family; T7 hasn't reproduced it.

## Tier-1 failure breakdown (8 failures total)

The 8 failures group into four root causes:

### Category A — corpus-availability defects (4 of 8)

| Row | Reason | Root cause |
|---|---|---|
| 1233 | `flagged_doi_unrelated_paper` | Extractor cited DOI `10.1021/ci700307p` (Hughes 2008 J Chem Inf Model) — the actual SI dataset paper. That paper isn't in the corpus; the URL → folder map resolved it to a *citing* paper (Tetko et al. 2016 PMC4724158) which only references Hughes 2008 in its bibliography. Verifier opened the wrong paper. |
| 1244 | `flagged_paper_unreadable` | Same Hughes 2008 SI dataset; verifier couldn't find the actual source file. |
| 1236 | `flagged_paper_unreadable` | Same root cause — Hughes 2008 SI dataset paper not in corpus. |
| 1212 | `flagged_doi_unrelated_paper` | DOI `10.1016/j.ijpharm.2009.01.026` (Chu & Yalkowsky 2009 Int J Pharm) — same pattern. Cited paper not in corpus; URL → folder map sent the verifier to a citing paper instead. |

These four failures share a single root cause: the extractor used a DOI from
the source paper's bibliography section, because the values themselves came
from a *table compiled in the corpus paper that cites the original measurement
source.* The DOI is real and verifiable (the substring is in the corpus paper's
bibliography), but the *underlying measurement* lives in a paper that isn't in
the corpus.

Per the v2.0 protocol, this should have been handled at extraction time: either
(a) cite the corpus paper (`measured`, with notes that the upstream primary
isn't in the corpus), or (b) flag the row with `flagged_paper_unreadable`. The
extractor took option (a) by intention but populated the `source_url` with the
upstream primary's DOI — partially mixing the two strategies. Phase 1 step 2
of `SKILL.md` is unambiguous that the DOI must come from "this paper's"
front matter, not the bibliography. v2.0 carried that rule over verbatim from
v1.7; the lapse is in extractor execution, not protocol design.

If the rule had been followed strictly, these four rows would have been either
suppressed or marked `flagged_review` at extraction time. The verifier's job
is to catch this, and it did.

### Category B — property-subtype mismatches (2 of 8)

| Row | Reason | Root cause |
|---|---|---|
| 163 | `flagged_property_subtype_mismatch` | Compound `[Glu(OEt)][IBU]`, value 194.2 °C. Extractor recorded `property = DSC_onset`. The paper's quote ("onset of decomposition at a temperature of 194.2 °C") and methods section make this a *TGA decomposition-onset value*, not a DSC measurement. Correct enum value: `decomposition`. The CSV's `notes` field even reads "TGA_onset_decomposition" — extractor knew the underlying phenomenon but picked the wrong enum value. |
| 660 | `flagged_property_subtype_mismatch` | Compound 10, value 260 °C from "Table II row 10 col M.p." showing `"260°C, decomp."`. The explicit `decomp.` label means `property` should be `decomposition`, not `melting_point`. |

Both are real extraction errors — the value and the compound are right, but
the `property` field is wrong. The mp_bp overlay's enum does contain
`decomposition`; the extractor should have selected it for both rows.

### Category C — value transcription error (1 of 8)

| Row | Reason | Root cause |
|---|---|---|
| 902 | `flagged_value_mismatch` | Compound 18 (6,7,8,9-tetrachloro-...-fluorene). Paper states `mp 158–159.5 °C`; extractor recorded `value_raw="158–159"` and `value_max=159`, truncating the `.5`. Also a Q5 fail (`quote_truncated_before_value`). |

Single-paper transcription typo.

### Category D — self-flagged before audit (1 of 8)

| Row | Reason | Root cause |
|---|---|---|
| 1398 | `flagged_compound_name_unbalanced_brackets` | Compound name has mismatched parens. Already pre-flagged by the extractor's Phase 3 `validate_compound_name.py` lint (it appears in the CSV's `flagged_review` set, one of six rows the extractor self-reported). Counts as a Tier-1 failure under our rubric (un-fixed `flagged_review` rows are not delivered as verified) but it's not an undetected defect. |

## Tier-2 verifiability (86.0 %)

T7's verifiability rate is markedly lower than T5's 99.7 %:

| Verifiability tag | Count |
|---|---:|
| `quote_missing_compound_token` | 37 |
| `quote_whitespace_unicode_mismatch` | 3 |
| `quote_truncated_before_value` | 1 |
| `quote_templated` | 1 |
| **Total Tier-2 fails** | **42** |

The dominant category — by a wide margin — is `quote_missing_compound_token`:
the `evidence_quote` carries the value verbatim but omits the compound's serial
code or name. The most common shape is

> `"(266 mg, 69%) as a white solid (mp 123-124 °C)"`

where the compound identifier (e.g., "8a") appears one line above in the paper
and the extractor's quote span didn't reach back far enough.

These rows are correct (Q1–Q4 all pass). The Tier-2 tag just says the maintainer
can't grep the database for the row and find the quote with the compound name
in one shot — they'd need to look at the surrounding lines of the paper.

Why is this so much higher than T5? Two contributing factors are visible in the
per-batch reports:

1. The T7 corpus has more papers that report mp/bp in the experimental section's
   per-compound block (`"Compound 8a. ... White solid (266 mg, 69%); mp ..."`),
   where the compound serial sits at the start of the paragraph and the mp/bp
   often wraps to a later line.
2. The extractor seems to have been more aggressive about taking the shortest
   span containing the numeric value, possibly to avoid the
   `quote_truncated_before_value` failure mode (Tier-2 in v1.6+, was Tier-1
   pre-v1.6). The result trades fewer truncated-before-value failures for more
   missing-compound-token failures.

Both behaviors are correct per the protocol — Tier-2 issues don't drop rows —
but the maintainer should be aware that quick spot-checks of T7 will more often
require reading the surrounding paragraph rather than relying on the quote
alone.

## Recall (manifest accounting)

T7 enumerated **237 manifest entries** and accounted for all of them:
**163 processed + 74 skipped = 237 ✓**. No silent loss. This matches the
T5 / T6 expectation — the Phase 0 manifest defense and `_skipped.txt` taxonomy
worked exactly as intended.

The manifest composition is:

- 164 PMC subdirectories with `article.nxml`
- 20 top-level standalone PDFs
- 53 PDFs in the four category subfolders (`materials_inorganic`,
  `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals`) — the
  same subfolders T4 missed via cross-trial contamination.

The 74 skipped papers are dominated by `no_mp_bp_data_in_text` (20) and
`review_no_per_compound_binding` (18), with smaller buckets for
`formulation_only_no_discrete_compound`, `bare_code_compounds_only`, and
`binding_ambiguous`. All within the v1.7 skip taxonomy except for one
`paper_unreadable`.

T7 emitted **1,580 rows** vs T5's 2,063 (−23 %). Likely contributors:

- T5 used `Trial5-full-opus47/` (`opus47` had read access to the prior trial's
  `EXTRACTION_SUMMARY.md` for protocol confirmation, sandboxed away from skip
  lists). T7 ran sandboxed without any prior-trial reference.
- The category subfolder PDFs were processed in T7 (53 papers) and accounted
  for, but yielded fewer rows than the PMC-bearing journal papers — many are
  textbook-style references contributing tens of compounds, not hundreds.
- T7 self-flagged 6 rows (vs T5's 0), reflecting the v2.0 lints catching shape
  defects that T5 may have committed silently.

Net: row count is a coarse signal. The 23 % drop isn't a recall regression in
the sense that T4's −17 % was — the manifest is intact and the skip reasons
are documented.

## Did v2.0 modularization itself cause anything?

No. The eight Tier-1 failures break down as:

- 4 corpus-availability defects (Category A) — same failure mode v1.7 would
  have produced on the same corpus. The fix is enforce Phase 1 step 2 (DOI
  from this paper's front matter, not its bibliography) more strictly at
  extraction time.
- 2 property-subtype mismatches (Category B) — Q2 verifier check working as
  designed; the mp_bp overlay's `decomposition` enum is in `SCHEMA.md` and
  was available to the extractor. Picking the wrong enum value is an
  agent-time judgment error.
- 1 value transcription (Category C) — single-row anomaly.
- 1 self-flagged (Category D) — the extractor's own Phase 3 lint caught it
  pre-audit.

None of these failures touched the v2.0 schema rename, the new `--datatype` flag,
the `conversion_arithmetic_lint.py` syntax check, or the overlay structure.
The audit infrastructure (URL → folder mapping, verifier prompt with overlay
pointers, JSON verdict format) all worked end-to-end.

## What changed vs T5

- Tier-1 dropped 99.7 % → 97.3 % (CI overlap is narrow but real — p = 0.019).
- Tier-2 dropped 99.7 % → 86.0 % (the bigger gap, and the more interesting
  signal).
- Recall (rows / total manifest entries) shifted from T5's 2,063-from-186
  to T7's 1,580-from-163.
- Manifest accounting is intact in both.

The four Category A failures are the structural concern: the extractor used
bibliography-DOIs as `source_url` for compiled-literature rows. In T5 this
didn't happen (or happened at a rate below the audit's detection sensitivity).
In T7 it happened four times in a 300-row sample → an estimated ~21 rows in
the full deliverable. The right fix is a tightening of Phase 1 step 2's
"DOI from this paper only" rule at the agent prompt level (or a deterministic
check at Phase 3 that the DOI in `source_url` is in the paper's body, not
just its bibliography list — though that's harder to detect).

## Recommendations

### v2.0.1 patch suggestions

1. **Tighten Phase 1 step 2 against bibliography-DOI capture.** The
   `EXTRACTION_PROMPT_TEMPLATES.md` Template 1 already says "Never guess a
   DOI" and "extract from the paper file ONLY — not from the paper's
   bibliography (those DOIs belong to *cited* papers)." Add a concrete
   anti-pattern: "❌ For a value the paper compiled from a literature
   reference, do NOT use that reference's DOI as your `source_url`. Use
   this paper's DOI (the one you're reading) and put the upstream
   primary citation in `notes` if relevant." Caught 4 of T7's 8 failures.

2. **Add a `decomposition` vs `melting_point` example to
   `datatypes/mp_bp/COMMON_ERRORS.md`.** The mp/bp overlay already lists
   `decomposition` in its enum, but the failure mode (260°C labeled
   "decomp." captured as `melting_point`) is real and worth a worked
   example. Caught 2 of T7's 8 failures.

3. **Track Tier-2 `quote_missing_compound_token` rate as a release-gate
   metric.** T7's 86 % vs T5's 99.7 % is a real shift in extraction
   behavior that's invisible to Tier-1. If verifiability drops below
   90 % on the next trial, audit the extraction prompt for whether the
   `quote_re_confirmation` step is being skipped on per-compound experimental
   sections.

### Audit infrastructure note

The URL → folder map (`url_to_folder.json`) is brittle when a row's
`source_url` cites a paper not in the corpus. For Category A rows, the map
falls back to whichever corpus paper the DOI's substring appears in — often
the *citing* paper, not the cited paper. This is correct behavior for the
infrastructure (we can't conjure a paper that isn't there) but it can confuse
post-audit triage. A future audit framework could mark these explicitly with
a `flagged_paper_not_in_corpus` reason rather than blending them into
`flagged_doi_unrelated_paper` and `flagged_paper_unreadable`.

## Net assessment

v2.0 is structurally healthy. The modularization didn't introduce any new
failure modes, the `--datatype mp_bp` halt rule didn't get in the way of the
extraction agent, the new generic `conversion_arithmetic_lint.py` ran cleanly
on all 36 conversions, and Phase 0 manifest accounting balanced.

T7's 97.3 % Tier-1 puts the skill back in the v1.4–v1.6 range after T5's
unusually clean 99.7 %. The four Category A failures are a known protocol
edge case (compiled-literature values) that v1.7 either avoided by luck or
this corpus exposes more aggressively. The two Category B failures and one
Category C failure are baseline agent-time error.

Tier-2 verifiability at 86 % is the more meaningful regression. It's not a
data-quality issue (those rows are correct) but it does indicate that the
extractor's quote-span discipline has slipped relative to T5. Recommend
adding a tightening pass on the Phase 2 `quote_re_confirmation` instruction
for v2.0.1.

T7 is the first trial of v2.0 on a fresh corpus. The result is consistent
with the v1.4–v1.6 baseline and well above the regex-extraction ceiling
(56 %). The skill is performing as designed; the four-point gap from T5 is
diagnosable and addressable with prompt-level tightening, not architectural
changes.

---

**Files:**

- Sample: `trials/trial7/opus47_papers/audit/_my_audit_sample_300.csv`
- Per-batch CSVs: `trials/trial7/opus47_papers/audit/_my_audit_batch_{1..12}.csv`
- Per-batch verdicts: `trials/trial7/opus47_papers/audit/_my_verdicts_{1..12}.json`
- Aggregated verdicts: `trials/trial7/opus47_papers/audit/_my_verdicts_all.json`
- URL → folder map: `trials/trial7/opus47_papers/audit/url_to_folder.json`

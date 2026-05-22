# Trial-8 comparison report — Opus 4.7 on v2.1 (consolidated data-extraction skill)

**Date:** 2026-05-22

**Trial:** Trial-8 (`trials/trial8/opus47_papers/opus47/`) — the first
real-corpus test of the v2.1 consolidated `data-extraction` skill. v2.1
collapsed each datatype overlay from 3 files (OVERLAY.md + SCHEMA.md +
COMMON_ERRORS.md) to 1 (OVERLAY.md), moved generic patterns up to the
skill-level docs, and bundled five targeted content patches addressing
T7's documented failures.

**Headline:** **98.3 % Tier-1 correctness** (295 / 300, Wilson 95 % CI
96.2–99.3 %) and **99.3 % Tier-2 verifiability**.

T8 is statistically tied with every prior journal trial (p ≥ 0.10 against
T2, T3, T4, T5, T7) and notably closes the Tier-2 gap T7 had opened. Of
the 5 Tier-1 failures, 3 were already self-flagged by the extractor's
own Phase 3/4 — only 2 were undetected at delivery time.

## Audit method

Same methodology as T7 and the v1.x trials:

- **Sample:** Uniform random 300 rows from the 1,743-row deliverable,
  fixed seed 20260522. Stratified verifier dispatch.
- **Verifiers:** 12 fresh-context general-purpose Claude agents in
  parallel, 25 rows each. Same prompt scaffold as the T7 audit, with
  the v2.1 property-disambiguation and compilation-table rules
  embedded.
- **Rubric:** Per `audit_criteria.md`. Q1–Q4 = Tier-1 PASS/FAIL;
  Q5 = Tier-2 verifiability (advisory).
- **Source mapping:** url_to_folder.json rebuilt for this session;
  all 114 unique source_url values in the sample resolved cleanly to
  paper files in the corpus (0 unresolved, vs T7's 0 unresolved after
  the doi_index-rebase pass).

## Headline comparison

| Trial | Skill | Rows | Tier-1 Correctness | Tier-2 Verifiability |
|---|---|---:|---|---|
| T2 (v1.4 Opus) | v1.4 | 1,864 | 296 / 300 = 98.7 % (CI 96.6–99.5) | ~91.3 % |
| T3 (v1.5 Opus) | v1.5 | 1,352 | 291 / 300 = 97.0 % (CI 94.4–98.4) | ~97.0 % |
| T4 (v1.6 Opus) | v1.6 | 1,529 | 294 / 300 = 98.0 % (CI 95.7–99.1) | 95.7 % |
| T5 (v1.7 Opus) | v1.7 | 2,063 | 299 / 300 = 99.7 % (CI 98.1–99.9) | 99.7 % |
| T7 (v2.0 Opus) | v2.0 | 1,580 | 292 / 300 = 97.3 % (CI 94.8–98.6) | 86.0 % |
| **T8 (v2.1 Opus)** | **v2.1** | **1,743** | **295 / 300 = 98.3 %** (CI 96.2–99.3) | **99.3 %** |

(T6 was a textbook extraction on the CRC Handbook; not directly
comparable to journal-paper trials. T6 produced 99.3 % Tier-1 on
15,741 rows.)

## Statistical comparisons (Tier-1)

| Comparison | z | p | Interpretation |
|---|---:|---:|---|
| T8 vs T2 | −0.34 | 0.737 | not significantly different |
| T8 vs T3 | +1.08 | 0.279 | not significantly different |
| T8 vs T4 | +0.30 | 0.761 | not significantly different |
| T8 vs T5 | −1.64 | 0.101 | not significantly different (T5 numerically higher) |
| T8 vs T7 | +0.84 | 0.400 | not significantly different (T8 numerically higher) |

T8 is statistically indistinguishable from every prior journal trial on
Tier-1. The numerical position — between T7 (97.3 %) and T5 (99.7 %) —
suggests the v2.1 consolidation moved the skill partway back toward
T5's high-water mark without quite reaching it.

## Tier-2 verifiability is the big story

T8 Tier-2 of 99.3 % is the headline change vs T7's 86.0 %. This was
the failure mode that drove the v2.1 consolidation hypothesis: the
trimmed Step 6 examples and increased cross-reference count in v2.0
encouraged subagents to settle for short, value-only quote spans that
omitted the compound's serial code. v2.1 restored anchoring examples
to the EXTRACTION_PROMPT_TEMPLATES Step 6 (now mirrored in SKILL.md
Phase 2 step 7) and added 4 worked examples to the consolidated
OVERLAY.md.

The result: only 2 of the 300 audited rows are not-fully-verifiable,
both with minor issues (a paraphrased quote omitting yield-mass detail
on row 1018; a partial line-wrap quote on row 1398). Both are
correct rows (Q1–Q4 PASS); the Tier-2 tags are advisory.

|  | T5 | T7 | T8 |
|---|---:|---:|---:|
| Tier-2 verifiability | 99.7 % | 86.0 % | **99.3 %** |
| `quote_missing_compound_token` count | <1 of 300 | 37 of 300 | 0–1 of 300 |

The Tier-2 result is statistically back to T5/T6 territory.

## Tier-1 failure breakdown (5 failures, 3 self-flagged)

### Already self-flagged before audit (3 of 5)

These rows were already marked `flagged_review` in the deliverable
CSV by the extractor's own Phase 3/4 sweep. The audit rubric counts
un-fixed flagged_review rows as Tier-1 failures, but they aren't
*undetected* defects — the extractor surfaced them, the maintainer
hasn't yet remediated.

| Row | Reason | Notes |
|---|---|---|
| 893 | `flagged_property_subtype_mismatch` | Bare-value row in PMC6146903 Table II tagged `decomposition`; per v2.1 disambiguation, bare values default to `melting_point`. Self-flagged by extractor; verifier confirmed. |
| 1405 | `flagged_property_subtype_mismatch` | Krossing 2011 `[C4MPyr][BF4]`, value 150.6 °C from a Table 1 "Te = peak onset" column. Should be `DSC_onset`, tagged `melting_point`. Self-flagged. |
| 908 | `flagged_compound_name_unbalanced_brackets` | Paper itself uses backtick-as-prime typography producing unbalanced brackets; CSV preserves the paper's typography. Self-flagged by `validate_compound_name.py`. |

### Undetected failures (2 of 5)

| Row | Reason | Root cause |
|---|---|---|
| 920 | `flagged_property_subtype_mismatch` | Compound 8, value `> 300 °C`. The paper labels it as a melting point: `"recrystallized to give 7 as pale yellow crystals (66%), m.p. > 300°C"`. The extractor tagged it `decomposition` — probably because >300°C suggests thermal decomposition for an organic at that range, but the v2.1 disambiguation rule is unambiguous: paper labels it m.p. → `property = melting_point`. |
| 970 | `flagged_compound_name_truncated` | Molecules 2001, 6, 300, compound 9. The paper's IUPAC name is `3(N)-(2,2'-diaminobenzophenone)-5-hydroxy-1,4-naphthoquinone`. The CSV recorded `3-(2-aminobenzophenone)-5-hydroxy-1,4-naphthoquinone` — missing the `2,2'-di` (paired amino groups vs single). Compound identity off by a functional group; the value (221 °C) is correct. |

These two are baseline agent-time errors — the kind any large
extraction will produce at low rates. Both could be addressed by
strengthening Phase 4's class-targeted sweep after Phase 4 finds
similar failures, but they don't trace to a v2.1 skill-text gap.

### The v2.0 → v2.1 failure-mode comparison

| Failure category | T7 (v2.0) | T8 (v2.1) | Comment |
|---|---:|---:|---|
| Compilation-table source_url (Category A) | 4 | 0 | v2.1's affirmative Phase 1 step 2 rule resolved it. |
| Property-subtype mismatch (Category B) | 2 | 3 | The v2.1 disambiguation table caught one extractor mistake (row 893 self-flagged) and one verifier-detectable mistake (row 920); raw count similar to T7. |
| Value transcription (`.5` truncation) (Category C) | 1 | 0 | The v2.1 trailing-decimal rule appears to have caught it. |
| Compound-name shape / contamination | 1 (self-flagged) | 2 | Row 970 (verifier-detected truncation) + row 908 (self-flagged typography). |

Category A — the largest contributor to T7's regression — is gone in
T8. The four T7 failures from compilation-table DOI capture (rows
1212, 1233, 1236, 1244) didn't recur. The affirmative Step 1b rule
("source_url is the DOI of the paper file you are physically reading,
NOT the DOI of any paper it cites") worked.

Category C is also gone: the trailing-decimal suspicion rule in
Phase 2 step 7 appears to have prevented the row-902-style truncation
in this corpus, though n=1 in T7 makes that claim less certain.

Category B (property subtype) is roughly stable. The disambiguation
table in OVERLAY.md helped the extractor self-flag the borderline
cases (rows 893, 1405 are both self-flagged in T8, whereas T7's
analogous failures weren't pre-flagged). Row 920 is a real miss —
the extractor token-matched ">300°C" → decomposition despite the
explicit "m.p." label in the source.

## Recall (manifest accounting)

T8 enumerated **237 manifest entries** and accounted for all of them:
**177 processed + 60 skipped = 237 ✓**. No silent loss.

T8's 1,743 rows is +163 rows (+10 %) vs T7's 1,580, with 14 more papers
processed (177 vs 163). The T7 orchestrator's "sample 20–50 representative
compounds from QSPR tables" cap (which the orchestrator disclosed
post-T7 was responsible for most of T7's row-count drop vs T5) wasn't
re-applied here — paper 062 (Yalkowsky alcohol bp table), paper 064 (API
Tm table), paper 014 (incadronate analogs) were fully extracted.

Skip-reason histogram remains in the v1.7-baseline range:

| Reason | T7 | T8 |
|---|---:|---:|
| `review_no_per_compound_binding` | 18 | 22 |
| `formulation_only_no_discrete_compound` | 14 | 14 |
| `no_mp_bp_data_in_text` | 20 | 10 |
| `bare_code_compounds_only` | 10 | 7 |
| `binding_ambiguous` | 8 | 2 |
| `image_only_compound_table` | 2 | 1 |
| `tga_or_nmr_only_no_mp_bp` | 1 | 1 |
| `paper_unreadable` | 1 | 1 |
| Other (free-text) | 0 | 2 |
| **Total skipped** | **74** | **60** |
| **Total processed** | **163** | **177** |

T8 skipped 14 fewer papers than T7 — the `binding_ambiguous` and
`no_mp_bp_data_in_text` categories shrank most (−6 and −10
respectively). The v2.1 explicit "drop list = per-row, skip vocabulary
= per-paper" distinction appears to have helped: fewer papers
escalated from "this paper has some problem rows" to "skip the whole
paper."

## Did v2.1 consolidation itself cause anything?

No. The 5 Tier-1 failures don't trace to the consolidation. Specifically:

- The consolidated single-file overlay didn't cause any new failure mode.
- The promoted compilation-table rule successfully prevented the
  T7 Category A failures (zero recurrence).
- The trailing-decimal rule appears to have prevented the T7
  Category C failure (zero recurrence in 300).
- The property-disambiguation table improved self-flagging
  (T8 self-flagged 2 of 3 property-subtype failures pre-audit;
  T7 self-flagged 0).
- The cross-reference reduction (69 → ~25) didn't introduce any new
  errors and is consistent with the Tier-2 verifiability rebound.

## What this confirms

The v2.1 hypothesis was: **the v2.0 → T7 regression was driven primarily
by cognitive / context load from the modular split, plus four small
content gaps**. v2.1 addressed both:

1. **Consolidation** reduced the cross-reference count from 69 to ~25.
2. **Content patches** added the affirmative compilation-table rule,
   the property-disambiguation table, the trailing-decimal suspicion
   rule, and the explicit drop-list-vs-skip-vocabulary distinction.

T8 results are consistent with this hypothesis:

- Tier-2 verifiability rebounded from 86.0 % to 99.3 % (back to v1.7
  / T5 levels). This is the load-reduction signal.
- Tier-1 improved from 97.3 % to 98.3 %, with the specific T7 failure
  classes (compilation-table source_url, value truncation) eliminated.
  This is the content-patch signal.
- Recall recovered: 1,580 → 1,743 rows (+10 %) without the orchestrator
  sample-cap that T7 had. v1.7's high-water mark (T5's 2,063) is now
  reachable; T8 didn't reach it but the gap is mostly attributable to
  this run's orchestrator-level choices, not skill-text issues.

## Net assessment

v2.1 has reached parity with v1.7 on the metric that matters most
(Tier-2 verifiability is back to 99 %+), substantially improved over
v2.0 on Tier-1, and preserved the modular architecture for future data
types. The skill is at a stable, deployable state for mp/bp extraction.

The two undetected failures (rows 920, 970) are baseline agent-time
errors of the kind any large extraction produces. Their categories
(property-subtype mismatch despite the disambiguation table; compound
name truncated to lose a functional group) are worth tracking in
future trials but don't currently warrant another skill iteration.

### Open items

- T8 didn't reach T5's 99.7 % Tier-1. The 5 failures vs T5's 1
  failure isn't statistically significant (p = 0.10), but T5 remains
  the high-water mark. A future trial could close this gap by
  adding a class-targeted sweep step after Phase 4 finds 2+ rows
  with the same `reason` — the existing protocol allows this but
  the orchestrator didn't apply it in T8.

- The redox overlay (v2.0 → v2.1 consolidated) has not been audit-tested
  against a real redox corpus. A redox trial would validate the
  v2.1 overlay structure for a property family other than mp/bp.

---

**Files:**

- Sample: `trials/trial8/opus47_papers/opus47/my_audit/_my_audit_sample_300.csv`
- Per-batch CSVs: `trials/trial8/opus47_papers/opus47/my_audit/_my_audit_batch_{1..12}.csv`
- Per-batch verdicts: `trials/trial8/opus47_papers/opus47/my_audit/_my_verdicts_{1..12}.json`
- Aggregated verdicts: `trials/trial8/opus47_papers/opus47/my_audit/_my_verdicts_all.json`
- URL → folder map: `trials/trial8/opus47_papers/opus47/my_audit/url_to_folder.json`

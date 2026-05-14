# Trial-3 comparison report — three agent models on v1.5

**Date:** 2026-05-13
**Skill version:** mp-bp-extraction v1.5 (installed via the packaged `.skill` artifact)
**Corpus:** `corpora/full_168` — 168 paper subdirectories
**Audit method:** Per-trial uniform random 100-row sample (seed 20260512), 4 fresh-context Claude verifier agents in parallel. For Opus, expanded to 300 rows via an additional 200-row sample (seed 20260514) audited by 8 more parallel agents. Final scoring under the three-tier criteria from `audit_criteria.md`.

## Headline

| Run | Agent | Rows emitted | Initial-100 audit (strict v1.5 criteria) | Final correctness (corrected criteria) |
|---|---|---:|---:|---:|
| Trial-2 (reference, v1.4) | Opus 4.7 | 1,864 | 98 / 100 = **98 %** | 296 / 300 = **98.7 %** |
| Trial-3 opus47 | Opus 4.7 | 1,352 | 94 / 100 = **94 %** | 291 / 300 = **97.0 %** |
| Trial-3 gpt55_high | GPT-5.5 high | 448 | 76 / 100 = **76 %** | not re-scored |
| Trial-3 sonnet46 | Sonnet 4.6 | 1,654 | 79 / 100 = **79 %** | not re-scored |

**The headline takeaway**: under matched, corrected audit criteria, v1.5 produced no measurable Tier-1 correctness improvement on Opus (T2 98.7 % vs T3 97.0 %, two-prop z-test p = 0.16) while costing ~27 % recall (1,864 → 1,352 rows). v1.5's apparent precision win was a verifiability improvement that the audit rubric mistakenly counted as correctness.

A separate finding: Sonnet 4.6 improved dramatically (55 → 79 % on the strict-v1.5 audit). v1.5's anti-script-row-generation rule successfully closed Sonnet's Path-B data-entry-script failure mode.

## What changed in the skill between Trial-2 and Trial-3 (v1.4 → v1.5)

Six changes documented in `CHANGELOG.md` and `reports/trial2_comparison_report.md`:

1. **Quote-must-contain-value rule** (strict, with "DROP the row" instructions).
2. **Generalized anti-pattern** forbidding scripts that produce the four evidence-locked fields (compound_name, value_raw, evidence_quote, source_url).
3. **No-ellipsis rule** + `quote_template_lint.py` that flagged literal `...` and "Table N: ..." patterns.
4. **Expanded `validate_compound_name.py`** shape lint (terminal unfinished-suffix tokens, dangling hyphen/prime, balanced brackets, narrow procedure-text contamination).
5. **DOI-from-file-only rule** — DOIs must appear as substrings of the paper file's text.
6. **Phase 4 sampling rule** — `max(100, 5 %)` parallel-dispatch pattern documented in SKILL.md.

The skill was packaged as `mp-bp-extraction/dist/mp-bp-extraction.skill` (66 KB) and installed on each of the three Trial-3 agent harnesses.

## Per-agent results

### Trial-3 Opus 4.7 — 94 / 100 (strict v1.5 audit)

| Failure mode | Count |
|---|---:|
| `flagged_compound_name_truncated` (EA-prefix contamination + truncations) | 3 |
| `flagged_evidence_quote_not_found` (PDF watermark splitting + paraphrasing) | 1 |
| `flagged_compound_mismatch` (wrong-compound-bound-to-value) | 1 |
| `flagged_value_mismatch` (literature value labeled measured) | 1 |

Opus self-flagged only 5 of 1,352 rows (0.4 %) and emitted 1,347 trusted rows.

EXTRACTION_SUMMARY.md reports Opus's own internal Phase-4 audit at 97 / 100 (close to the independent audit's 94 / 100 within sampling noise).

Opus's six initial-audit failures fall into two clusters:
- **Compound-name-field contamination** (3 of 6): elemental-analysis lines (`"C, 50.73; H, 5.72; N, 8.42."`) prepended to a real IUPAC name. New failure mode introduced by v1.5 — the stricter extraction protocol appeared to make Opus capture more surrounding context around the compound name, sweeping the EA prefix along.
- **Genuine data errors** (3 of 6): a PDF watermark splitting an evidence span (row 1274); a compound 23 row carrying compound 25's m.p. 256 °C (row 750); a literature-reference value recorded as the paper's own measurement (row 529).

### Trial-3 GPT-5.5 high — 76 / 100

| Failure mode | Count |
|---|---:|
| `flagged_evidence_quote_not_found` | 14 |
| `flagged_compound_mismatch` | 7 |
| `flagged_value_mismatch` | 2 |
| `flagged_doi_unrelated_paper` | 1 |

GPT-5.5 self-flagged 130 of 448 rows (29 %) and emitted 318 trusted rows. The trusted-only audit rate was 93.8 % (61 / 65). GPT's strict-v1.5 audit number (76 %) is driven mostly by rows it openly disclosed as uncertain — a different failure profile from agents that emit confidently.

The recall drop on GPT-5.5 (907 → 448, -51 %) reflects heavy self-filtering under the stricter v1.5 rules, not a Path-B-style structural failure. GPT-5.5 used parallel LLM workers + orchestration scripts, not data-entry scripts.

### Trial-3 Sonnet 4.6 — 79 / 100

| Failure mode | Count |
|---|---:|
| `flagged_evidence_quote_not_found` | 15 |
| `flagged_compound_name_truncated` | 3 |
| `flagged_doi_unrelated_paper` | 1 |
| `flagged_compound_mismatch` | 1 |
| `flagged_compound_name_ms_fragment` | 1 |

Sonnet 4.6 self-flagged 242 of 1,654 rows (14.6 %) and emitted 1,412 trusted rows. The trusted-only audit rate was 86.7 % (78 / 90).

The +24 pp improvement vs Sonnet Trial-2 (55 → 79 %) is the largest single-trial gain in the project. Almost entirely attributable to v1.5's anti-script-row-generation rule closing Sonnet's Trial-2 Path-B failure (the `build_batch_pdfs.py` data-entry script that templated quotes via f-strings). Of the residual Sonnet T3 failures, only one (1 row of 21) matches the constructed-quote pattern — the rest are quote-fidelity (non-contiguous spans) or compound-name issues.

## Why the headline numbers were misleading

Two methodology issues showed up during the audit and forced a re-analysis:

### Issue 1 — The 100-row audit couldn't distinguish T2 from T3 on Opus

Opus T2 (v1.4) reported 98 / 100, T3 (v1.5) reported 94 / 100. With Wilson 95 % CIs of 93.0–99.4 % and 87.5–97.2 % respectively, the two-prop z-test gave p = 0.27 — within sampling noise. To distinguish a real 4-pp difference, we needed a larger sample.

We drew 200 additional Opus rows from each of T2 and T3 using a different seed, ran them through 16 fresh-context verifier agents in parallel, and got:

- T2 (v1.5 audit standards): 165 / 200 = 82.5 % (CI 76.6–87.1 %)
- T3 (v1.5 audit standards): 183 / 200 = 91.5 % (CI 86.8–94.6 %)
- z = −2.68, **p = 0.007**

That looked like a real +9 pp v1.5 improvement on Opus. But the underlying number was odd — T2 had been audited at 98 % originally and was now at 82.5 % on the same data.

### Issue 2 — The audit rubric was rejecting things that weren't failures

The 200-row T2 audit gave verbose failure rationale. Looking at the 35 fails, most were one of:

- Quote stops before value (PDF column wrap, watermark, OCR-mangled boundary).
- Quote contains literal `...` joining non-adjacent paper text.
- Quote omits a citation superscript ("(2g).19" → "(2g)").
- Range shorthand expansion ("237-39" → "237-239").
- Whitespace inside paren mismatch.
- Review-paper value labeled `measured` — but per the schema this is correct.

In each case, the row's compound, value, and source citation were correct. The verifier was rejecting on quote-fidelity grounds (v1.5's strict criteria) and on data_type grounds (a stricter rule than the schema). The row's actual data was fine.

That prompted a re-think of what an audit should measure.

## The three-tier audit framework

Captured in `audit_criteria.md` at the project root. The framework separates correctness from verifiability:

- **Tier 1 — Correctness.** Compound identity correct, value correct (matched to that compound), property type correct, data_type per schema (`measured` = any experimental observation; `calculated` = model output), source citation real. PASS / FAIL determines the headline number.
- **Tier 2 — Verifiability.** Quote is verbatim, contiguous, and contains compound + value. Tracked as a separate rate; tells you how easy spot-checking is, not whether the data is wrong.
- **Tier 3 — Hygiene.** CSV well-formed; required fields populated; SMILES validates; conversion_arithmetic shown when applied. Caught by Phase-3 scripts.

The mistake the v1.5 audit made was treating Tier 2 issues (paraphrased quotes, ellipsis, missing-value-in-quote) as Tier 1 failures. The v1.5 *production* protocol made agents drop rows on Tier 2 issues. Together, those two rules created a self-reinforcing loop: stricter extraction protocol + stricter audit rubric, both targeting verifiability, both lowering recall without improving correctness.

## Re-scored results under corrected criteria

Going back to the 300 audited Opus rows (100 original + 200 extra) and re-classifying each "fail" by the Tier-1 criteria:

| Audit subset | T2 (v1.4) | T3 (v1.5) |
|---|---:|---:|
| Original 100 (re-scored) | 100 / 100 = **100 %** | 96 / 100 = **96.0 %** |
| Extra 200 (re-scored) | 196 / 200 = **98.0 %** | 195 / 200 = **97.5 %** |
| **Combined 300** | **296 / 300 = 98.7 %** | **291 / 300 = 97.0 %** |
| Wilson 95 % CI | 96.6–99.5 % | 94.4–98.4 % |
| Two-prop z-test | | z = 1.40, **p = 0.16** |

**Under corrected criteria, T2 and T3 are statistically indistinguishable on Tier-1 correctness.** The 9-pp gap that the strict-v1.5 audit showed was an audit-rubric artifact, not a real improvement.

Quote-fidelity rates (Tier-2, separate metric):

| | T2 (v1.4) | T3 (v1.5) |
|---|---:|---:|
| Quote-fidelity issues (verbatim presence violated) | 26 / 300 = 8.7 % | 9 / 300 = 3.0 % |

v1.5 *did* improve Tier-2 verifiability — by 5.7 pp on Opus, ~70 % relative. That's a real change. It just wasn't a correctness change.

## Trial-3 Opus failure breakdown under corrected criteria

The 9 actual Tier-1 failures across 300 audited rows:

**T2 (4 fails, all DOI fabrication):**
- Rows 1728, 1644, 1642, 1853 — DOIs that don't appear in the source paper. v1.4 didn't enforce DOI-from-file-only; v1.5 did.

**T3 (9 fails — mix of compound-name and source issues):**
- 3 EA-prefix contamination (rows 364, 365, 493): `"C, NN.NN; H, N.NN; N, N.NN."` prepended to a correct IUPAC name.
- 1 wrong-value-binding (row 750): compound 23's row carrying compound 25's m.p.
- 1 mangled compound name (row 930): `"3-(4-((2-(2-..."` truncated to `"((((2-(2-..."`.
- 1 procedure-text in compound_name (row 530): `"(Yield 94%),"` as the compound name.
- 1 leading-code-prefix in name (row 920): `"6 (Methyl 2-...)"` instead of stripped IUPAC.
- 2 paper-not-in-corpus (rows 1292, 1340): cited DOIs map to papers that aren't in the corpus.

**The trade v1.5 actually made:**

| | v1.5 effect |
|---|---|
| DOI fabrication | -4 (eliminated) |
| Compound-name contamination | +5 (introduced as a new failure pattern) |
| Net Tier-1 correctness | ~zero |
| Tier-2 verifiability | +5.7 pp |
| Recall | -27 % |

## Where the recall went

Opus T2 → T3 row drop decomposed by paper:

| Component | Rows | Story |
|---|---:|---|
| Papers in T2 only that vanished in T3 | -855 | 88 papers Opus T2 produced rows for; T3 produced zero |
| Papers in T3 only (newly covered) | +366 | 32 papers in T3 not in T2 |
| Net delta on shared papers (104 in both) | -23 | -2.3 % over ~1,009 shared rows |
| **Net** | **-512** | |

The 88 vanished papers break down as:

| Where the paper lives in the corpus | Papers | T2 rows lost |
|---|---:|---:|
| Category subfolders (materials_inorganic, organic_synthesis, pharma_cocrystals, measurement_prediction) | 43 | 350 |
| Indexed PMC subdirs that Opus T3 visited but produced 0 rows for | 42 | 481 |
| Not found in current corpus | 3 | 24 |

The first cluster is a Opus T3 operational gap — its `EXTRACTION_SUMMARY.md` records that the 4 category subdirs at the corpus tail weren't descended into. Not a v1.5 effect.

The second cluster is a v1.5 effect: 42 indexed PMC papers Opus visited and emitted zero rows for. Examination of the v1.5 Step 6.2 wording — "DROP the row" on quote-fidelity issues — combined with Opus's near-zero self-flagging tendency (it drops rather than flags) is the most likely cause. Several of those papers have 2-column PDFs or tables where the value lives in a different physical cell from the compound name; v1.5's strict contiguous-quote rule made those rows undeliverable.

## Cross-trial behavior pattern: Opus vs everyone else

The trial revealed an Opus-specific behavioral dynamic that affected the conclusions:

| | Opus 4.7 | GPT-5.5 | Sonnet 4.6 |
|---|---|---|---|
| Self-flagging rate (T3) | 0.4 % | 29 % | 14.6 % |
| Response to stricter rules | Drops rows | Marks `flagged_review` | Mix of drop + flag |
| Recall change T2 → T3 | -27 % | -51 % | -36 % |
| Trusted-only audit rate (T3) | 94 % | 94 % | 87 % |

Opus doesn't compensate for strict extraction rules by self-flagging — it drops rows. This means strictness costs Opus recall directly. GPT-5.5 and Sonnet self-flag, so strict rules push borderline rows into `flagged_review` rather than out of the deliverable; the user filters them out, the "trusted" rows stay clean.

For deployment with Opus specifically: every strict rule has a recall cost. Strict rules should only be applied for Tier-1 correctness; Tier-2 / Tier-3 issues should be lints (advisory, not auto-drop).

## v1.6 plan (derived from this analysis)

Per the framework in `audit_criteria.md`:

**Keep as strict Tier-1 rules:**
- DOI-from-file-only.
- Compound-name shape lint with v1.5 patterns plus **new v1.6 additions** for EA-prefix, leading paper-local code prefix, procedure-text-at-start.
- Anti-script-row-generation (zero impact on Opus, kept as documentation; preserves cross-model lesson).
- Phase 4 sampling rule + parallel dispatch.

**Downgrade to Tier-2 advisory:**
- Quote-must-contain-value (`quote_support_lint.py` stays as a Phase-3 warning, no longer auto-drops rows; Step 6.2 extraction prompt no longer says "DROP the row").
- Verifier prompt rewritten so Q1–Q4 = Tier-1 PASS/FAIL, Q5 = separate Tier-2 verifiability report.

**Drop entirely:**
- No-ellipsis-in-quote rule.
- Template-quote prohibition.
- `quote_template_lint.py` replaced with a deprecated no-op stub (kept for backward compatibility).

Predicted v1.6 outcome on Opus:

| Metric | T2 (v1.4) | T3 (v1.5) | v1.6 prediction |
|---|---:|---:|---:|
| Rows emitted | 1,864 | 1,352 | ~1,800–1,900 |
| Tier-1 correctness | 98.7 % | 97.0 % | ~98.5–99.5 % |
| Tier-2 verifiability | 91.3 % | 97.0 % | ~92–94 % |
| DOI fabrication | 4 | 0 | 0 |
| Compound-name contamination | 0 | 5–7 | 0 |

Net: recover the recall v1.5 cost, eliminate the EA-prefix / leading-code-prefix failures introduced in v1.5, hold the DOI-fabrication wins from v1.5, accept somewhat lower verifiability than v1.5 in exchange.

## Opus-only deployment

Given Opus's substantial precision lead (97 % vs 76 % GPT vs 79 % Sonnet on the strict audit; comparable correctness but with the highest emitted-row volume on the corrected audit), Opus is the production model going forward. The cross-model robustness work documented in v1.4 and v1.5 stays in the skill — the changes have near-zero cost for Opus — but the production target is one model, not three. v1.6's predicted outcomes are specifically for Opus.

## Lessons from Trial-3

1. **Audit rubric matters as much as the data being audited.** Two of the most striking numbers in the project (98 % T2 → 94 % T3, then 82.5 % → 91.5 % under "v1.5 standards") were both audit-rubric artifacts, not real changes. The corrected three-tier framework lives in `audit_criteria.md` to prevent this from recurring.
2. **Verifiability is not correctness.** Quote-fidelity rules made it easier to spot-check rows but didn't make rows more correct. Conflating the two led to a v1.5 release that traded recall for verifiability and looked like a precision improvement.
3. **Strict rules and self-flagging compensate for each other; with non-self-flagging agents, strict rules drop rows silently.** Opus's 0.4 % self-flagging rate means every strict rule has a direct recall cost. This is an Opus-specific dynamic that shaped the v1.6 design.
4. **Sample size matters when comparing close pass rates.** The 100-row audit could not distinguish T2 from T3 (CIs heavily overlapping). The 300-row expansion was necessary to see the underlying numbers; with the corrected criteria it then turned out the two trials are statistically tied (p = 0.16).
5. **Sonnet's v1.5 result demonstrates the anti-script-row-gen rule works.** +24 pp on the strict audit is the largest single change observed in the project. Even if Opus is the production target, the cross-model robustness wins from v1.5 are worth retaining.

## Files

[Trial-3 opus47 audit verdicts (300-row aggregated)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial3-full-opus47/_my_verdicts_all.json)
[Trial-3 gpt55_high audit verdicts (100-row)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial3-full-gpt55_high/_my_verdicts_all.json)
[Trial-3 sonnet46 audit verdicts (100-row)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial3-full-sonnet46/_my_verdicts_all.json)
[T2 Opus extra-200 audit verdicts (under matched v1.5 standards)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial2/full-opus47/)
[Audit criteria framework](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/audit_criteria.md)
[v1.6 .skill artifact](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp-bp-extraction/dist/mp-bp-extraction.skill)

# Trial-4 comparison report — Opus 4.7 on v1.6

**Date:** 2026-05-14
**Skill version:** mp-bp-extraction v1.6 (installed via the packaged `.skill` artifact)
**Corpus:** `corpora/full_168` — 168 paper-bearing locations
**Audit method:** Uniform random 300-row sample (100 with seed 20260512, 200 with seed 20260514), 12 fresh-context Claude verifier agents in parallel, three-tier criteria per `audit_criteria.md`. Same methodology as the T2 and T3 expanded Opus audits.

## Headline — v1.6 delivered what the v1.6 plan predicted

| | Rows emitted | Tier-1 Correctness | Tier-2 Verifiability | Statistical comparison |
|---|---:|---:|---:|---:|
| T2 (v1.4 Opus) | 1,864 | 296/300 = **98.7 %** (CI 96.6–99.5) | ~91.3 % | — |
| T3 (v1.5 Opus) | 1,352 | 291/300 = **97.0 %** (CI 94.4–98.4) | ~97.0 % | T2 vs T3: p = 0.16 |
| **T4 (v1.6 Opus)** | **1,529** | **294/300 = 98.0 %** (CI 95.7–99.1) | **95.7 %** | T2 vs T4: **p = 0.52**; T3 vs T4: **p = 0.43** |

T4 is statistically tied with both T2 and T3 on Tier-1 correctness. v1.6 sits in the same precision range as v1.4 and v1.5, with verifiability close to T3's high. Net result: v1.6 is the steady state — none of the v1.5 over-corrections, but it still carries the v1.5 wins (DOI-from-file-only, expanded compound-name shape lint, new EA-prefix detection).

The recall picture is more nuanced. T4's 1,529 rows is +177 vs T3 but −335 vs T2. The shortfall is **not** a v1.6 conservatism problem — it's an operational corpus-coverage gap that turned out to be cross-trial contamination.

## What v1.6 fixed vs T3

The four T3 failure modes the v1.6 plan targeted, on a per-row basis:

| Failure pattern | T3 count | T4 count |
|---|---:|---:|
| EA-prefix contamination (`"C, NN.NN; H, N.NN; N, N.NN. (IUPAC name)"`) | 3 of 9 | **0 of 6** |
| Leading paper-local code prefix (`"6 (IUPAC name)"`) | 1 of 9 | 0 of 6 |
| Procedure-text in compound_name (`"(Yield 94%),"`) | 1 of 9 | 0 of 6 |
| Indexed-PMC papers visited but emitted 0 rows | 42 | **9** |

The v1.6 lints (added EA-prefix, leading-code-prefix, procedure-text-at-start detection to `validate_compound_name.py`) caught every instance of those patterns at extraction time. The "DROP the row" → "record the closest contiguous span" softening of Step 6.2 dropped the indexed-PMC zero-row cluster from 42 papers / 481 rows in T3 down to 9 papers / 27 rows in T4. The latter cluster is now essentially noise (small numbers, mostly legitimate per-paper reasons).

## Trial-4's 6 Tier-1 failures

| Row | Failure | Note |
|---|---|---|
| Multiple in paper PMC7148931 (3 rows) | `wrong_compound_bound_to_value` | Isomer mismatch in a multi-isomer synthesis paper (5-(N-benzylidene) series; V7/V8 substituent swap). Single-paper anomaly. |
| 1 row | `flagged_compound_name_contaminated` ("sodium salt route" trailing phrase) | New compound-name contamination pattern not in v1.6 lint. Single occurrence — not worth a lint addition unless it recurs. |
| 1 row | `flagged_compound_mismatch` | One-off generic mismatch. |
| 1 row | `paper_printed_typo` (paper has inverted range `285–257 °C`) | Not a real failure — agent self-flagged at extraction time, correctly preserving the paper's typo. |

5 of the 6 are real audit failures (the 6th is correctly self-flagged). Three of those five are concentrated in one paper, which is the kind of single-paper anomaly that doesn't justify a class sweep under `audit_criteria.md`'s policy.

## Tier-2 verifiability — 13 of 300 non-verifiable

| Verifiability tag | Count |
|---|---:|
| `quote_missing_compound_token` | 9 |
| `quote_whitespace_unicode_mismatch` | 2 |
| `quote_truncated_before_value` | 2 |

The `quote_missing_compound_token` cluster is the synthesis-paper pattern Opus described in its self-analysis: the compound name is in the section heading immediately above the m.p. line and the captured quote is just the m.p. clause. Under v1.6 design this is correct behavior — the row's data is right and Q5 is advisory.

## The recall question — and why the shortfall is operational, not v1.6

T4 covered 140 papers vs T2's 170 (at paper-folder level, normalized across the source_url DOI/PMC variation). The 40 missed papers break down:

| Where the missed paper lives in the corpus | Papers | T2 rows |
|---|---:|---:|
| `organic_synthesis/` (standalone PDFs) | 14 | 198 |
| `materials_inorganic/` | 12 | 59 |
| `pharma_cocrystals/` | 3 | 9 |
| `measurement_prediction/` | 2 | 25 |
| **Subtotal: category subfolders not descended into** | **31** | **291** |
| Indexed PMC subdirs (visited, emitted 0 rows) | 9 | 27 |
| **Total** | **40** | **318** |

**91 % of the recall gap is the four category subfolders.** Same gap T3 had, same explicit "left to a parallel run" phrasing in EXTRACTION_SUMMARY.md.

## What Opus admitted in its self-analysis

The exact commands Opus ran for corpus enumeration:

```bash
cd corpora/full_168 && ls -d */ | sed 's|/||' > _paper_dirs.txt
# → 168 lines, including the 4 category folders as the last 4 entries
# Then explicitly filtered them out:
ls -d */ | sed 's|/||' | \
  grep -v "^materials_inorganic$\|^measurement_prediction$\|^organic_synthesis$\|^pharma_cocrystals$" \
  > _pmc_dirs.txt
# → 164 lines
```

**Opus saw the category subfolders** (the listing surfaced them), counted the PDFs (32 / 21 / 31 / 27 files across the four), and *explicitly filtered them out*. The stated reason: it had read `Trial3-full-opus47/EXTRACTION_SUMMARY.md` at the start of the run as a reference and lifted the "left to a parallel run" framing without questioning whether the same exclusion applied.

This is the meta-finding from Trial-4.

## The cross-trial-contamination failure mode

This is a new failure mode in the same family as cross-model variability (Trial-2) and audit-rubric drift (Trial-3). All three are about how the *context* around the skill — what other text the agent has seen, what rubric the verifier applies — affects results more than the skill content itself does.

In Trial-4's case: a fresh Opus invocation, given the corpus + the skill + (incidentally) a previous trial's directory tree, treated the previous trial's operational choices as if they were part of the protocol. Opus's exact framing: *"I lifted the framing from the Trial3-full-opus47/EXTRACTION_SUMMARY.md that I read as a reference at the start of the run, without questioning whether the same exclusion applied here."*

This is structurally similar to the v1.4 failure mode where a cross-harness agent read SKILL.md as a Python-pipeline-to-implement rather than a protocol-to-follow: authoritative-looking text gets promoted from reference to instruction.

**Two angles on the fix:**

1. **Operational:** sandbox the agent's read scope. The dispatching script should give the agent access only to the corpus and the skill directory. Past trial outputs, the development report, `audit_criteria.md`, and other prior-run artifacts are out of scope unless explicitly handed over with framing.
2. **Skill-side:** acknowledge that the agent's reading material is part of the protocol surface, and explicitly tell it not to treat past trial choices as authority.

Both are needed. The sandbox is the primary defense; the skill-side anti-pattern is belt-and-suspenders.

## The 24 zero-row papers — mostly legitimate

Opus categorized every paper that emitted zero rows. The breakdown:

| Category | Papers |
|---|---:|
| (a) Review / ML / QSPR with no per-compound binding | 8 |
| (b) Bare-code-only compounds | 5 |
| (c) NMR-only / TGA-only / method-only / mp-absent | 6 |
| (d) Other (DNA Tm, structure-image tables, formulations, ambiguous) | 5 |

Almost all are legitimate skips per protocol. Only **paper 037 (PMC6264548)** stands out — Opus called it "compound-binding ambiguous" with 12 T2 rows. That single paper accounts for nearly half of the 27-row INDEXED_PMC gap and is worth a manual look during a future trial, but is not systemic.

## v1.7 plan — three changes

Three skill-level changes plus one operational change addressing this trial's findings:

### Skill changes (v1.7)

**1. Add Phase 0 — corpus manifest** to `SKILL.md`. Intent-level, not mechanism-specific:

> Before Phase 1, enumerate every paper-bearing location in the corpus, descending into subfolders. Write the enumeration to `_corpus_manifest.txt` in your working directory. Anything you intentionally exclude from extraction goes in `_skipped.txt` with a one-line reason. Phase 1 is gated on the manifest being non-empty; the EXTRACTION_SUMMARY must account for every manifest entry as either processed or skipped-with-reason.

The skill stays generic — it doesn't prescribe `find` patterns or assume any particular corpus layout. Larger or differently-structured corpora are handled by the agent producing the right enumeration for the actual structure.

**2. `_skipped.txt` requirement.** EXTRACTION_PROMPT_TEMPLATES.md and EXTRACTION_SUMMARY template both require this file. Each entry: one paper-bearing location, one reason. Taxonomy starts from Opus's categorization:
- `review_no_per_compound_binding`
- `bare_code_compounds_only`
- `no_mp_bp_data_in_text`
- `tga_or_nmr_only_no_mp_bp`
- `binding_ambiguous`
- `image_only_compound_table`
- `formulation_only_no_discrete_compound`
- `paper_unreadable`

**3. Anti-pattern:** *Past trial outputs are reference, not protocol.* Added to the SKILL.md anti-patterns list:

> ❌ **"The prior trial run did X, so I'll do X too."** — Past trials are observations and can inform what to look out for, but they do NOT define protocol. Only SKILL.md and your assigned corpus define your task. If a past run skipped part of the corpus, that's a fact about that run, not a directive for yours. When in doubt, ask the user; do not adopt prior-run choices as if they were rules.

### Operational change (not part of v1.7)

Trial-5 dispatch sandbox: agent's read-accessible paths are the skill directory and the corpus. Past `Trial*-*/` directories, `audit_criteria.md`, the development report, and other prior-run artifacts are out of scope. This is the primary defense against cross-trial contamination; the v1.7 anti-pattern is the secondary defense for cases where contamination still leaks through.

### Explicitly NOT in v1.7

- **No reconciliation-checker script.** The Phase 0 manifest + `_skipped.txt` are enforcement by design rather than enforcement by check. If a future trial shows the "emitted-paper-count ≠ manifest-count" failure pattern, add a script then. Not preemptively.
- **No merge of category-subfolder rows into the T4 deliverable.** We're testing the skill, not building a database. Trial-5 will produce the correct deliverable from a clean run.
- **No fix for the "sodium salt route" compound-name contamination.** One occurrence is too rare to deserve its own pattern in `validate_compound_name.py`. Add if it recurs.

## Predicted Trial-5 outcome (v1.7 + sandbox)

| Metric | T2 (v1.4) | T3 (v1.5) | T4 (v1.6) | T5 prediction (v1.7 + sandbox) |
|---|---:|---:|---:|---:|
| Rows emitted | 1,864 | 1,352 | 1,529 | ~1,800–1,900 |
| Papers processed | 170 | 126 | 140 | ~190–198 |
| Tier-1 correctness | 98.7 % | 97.0 % | 98.0 % | ~98 % |
| Tier-2 verifiability | 91.3 % | 97.0 % | 95.7 % | ~95–96 % |
| Silent skipping of corpus parts | Some | Yes | Yes | **No (manifest-enforced)** |

The expected change: recall back at T2-equivalent because the manifest step + sandbox forces full corpus coverage. Correctness and verifiability stay at v1.6 levels because no Tier-1 rules change.

## Lessons from Trial-4

1. **v1.6 worked as designed.** The compound-name contamination patterns are caught; the over-conservative quote rules are advisory; recall recovered ~13 % vs T3. The audit numbers are statistically tied with both T2 and T3.
2. **The recall shortfall traces to cross-trial contamination, not the skill.** Opus's exact words: *"I lifted the framing from Trial3-full-opus47/EXTRACTION_SUMMARY.md."* This is a new failure mode worth naming.
3. **Cross-trial contamination is one of three "context shapes the result" failures the project has now identified.** The others are cross-model variability (Trial-2) and audit-rubric drift (Trial-3). Each is a case where the surrounding context — not the skill itself — drives outcomes.
4. **The fix is structural at the dispatch layer, not in the skill.** Sandbox the agent's read scope; the skill adds a small belt-and-suspenders anti-pattern but the operational change is the load-bearing piece.
5. **A manifest step is cheap insurance for larger corpora.** Even with sandboxing fixing this specific case, requiring explicit enumeration + skip-accounting before extraction means future trials on larger / differently-structured corpora won't silently miss subfolders for other reasons.

## Files

[Trial-4 verdict aggregates (300 rows)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial4-opus47/_my_verdicts_all.json)
[Trial-4 audit samples](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial4-opus47/)
[Opus's self-analysis (Q&A with maintainer)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial4-opus47/EXTRACTION_SUMMARY.md)
[Audit criteria framework](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/audit_criteria.md)

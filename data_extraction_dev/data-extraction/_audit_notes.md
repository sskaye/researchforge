# Audit notes — Step 2 of the v1.7 → v2.0 migration

Generated during migration Step 2 (per `generalization_proposal.md`). Classifies every file
and every major section in `data-extraction/` (post-Step 1 verbatim copy of `mp-bp-extraction/`)
as **generic** (property-agnostic), **mp_bp_specific** (tied to melting/boiling-point semantics),
or **both** (generic with embedded mp/bp examples or rules).

Labels in this doc:

- `[G]` — generic; stays in v2.0 generic layer with at most cosmetic edits.
- `[S]` — mp/bp-specific; moves to `datatypes/mp_bp/` overlay.
- `[B]` — both; split during Step 4 (generic skeleton stays; mp/bp examples become the overlay's worked example or move to the overlay's `COMMON_ERRORS.md`).

The proposal's Section 2 set the broad classification; this doc records the file-and-section
detail Step 4 needs.

---

## Top-level files

### `SKILL.md` (389 lines)

| Lines | Section | Label | Notes |
|---|---|---|---|
| 1–5 | YAML front matter (`name: mp-bp-extraction`, `description:`, `version: v1.7`) | [S] | Rewrite for v2.0: `name: data-extraction`; new `description:` mentioning the overlay structure; `version: v2.0`. |
| 7 | Title "# mp/bp extraction protocol" | [S] | → "# Data extraction protocol" or similar. |
| 9–36 | "How this skill is applied — MANDATORY READING" + Pre-flight checklist | [G] | Already generic in shape. Add the "identify your data type" instruction (per Step 4 in the proposal) and the halt-on-missing-overlay rule. |
| 38–40 | Goal | [B] | "melting-point and boiling-point measurements" → "the data type's measurements". Move the mp/bp specifics into the overlay's `OVERLAY.md`. |
| 42–49 | Why the discipline matters | [G] | Property-agnostic argument; keep. "30–60% extraction-error rates" is from mp/bp history but the principle is universal. |
| 51–59 | Input contract | [G] | Refers to "paper files", not "mp/bp papers". Keep. |
| 61–83 | The schema (17-column v1.7 table) | [S] | **Major rewrite.** Replace with v2.0's 18-column generic schema (per proposal Section 2): `compound_name`, `compound_smiles`, `property`, `value`, `value_min`, `value_max`, `value_raw`, `units`, `relation`, `meas_calc` (renamed from `data_type`), and the source/evidence/notes columns. Add empty-when-not-applicable conventions and standardized `conversion_arithmetic` syntax. Point at overlay's `SCHEMA.md` for the property enum, standardized unit string, and extension columns. |
| 85–103 | Verification status values | [G] | The enum is property-agnostic. Keep. The granular `flagged_*` reasons are mostly generic but a few are mp/bp-coupled (e.g., `flagged_value_out_of_range` is generic; `flagged_compound_name_truncated` is generic). No structural change needed. |
| 105–107 | "Why no author field" + "Why a single file" | [G] | Keep. |
| 109–130 | Worked example (three CSV rows) | [S] | Move to `datatypes/mp_bp/SCHEMA.md` as the worked-example row. Replace in SKILL.md with a pointer: "See your data type's `SCHEMA.md` for a worked-example row." |
| 132–157 | Phase 0 — Corpus manifest | [B] | Mostly generic; `_skipped.txt` reason taxonomy has mp/bp-specific entries (`tga_or_nmr_only_no_mp_bp`, `no_mp_bp_data_in_text`, `bare_code_compounds_only`). Split: generic Phase 0 structure stays in SKILL.md; the data-type-specific skip reasons move to the overlay's `OVERLAY.md` as a "Skip-reason vocabulary" subsection. |
| 159–175 | Phase 1 — Source preparation | [B] | Steps 1–4 are generic. Step 5 mentions "mp / bp / m.p. / Tm / Tfus / boiling point / Tb" as candidate-location tokens — those are mp/bp-specific; move to overlay. |
| 177–211 | Phase 2 — Evidence-locked extraction | [B] | The quote re-confirmation 4-step check is generic. "Drop these aggressively" (lines 204–209) is mp/bp-specific (NMR/MS, workup solvents) and moves to overlay's `OVERLAY.md` or `COMMON_ERRORS.md`. |
| 213–236 | Phase 3 — Programmatic sanity checks | [B] | The umbrella structure is generic. The check table mixes generic checks (csv_quote_lint, dedup_within_paper, verify_doi, verify_evidence_quote, quote_support_lint) with mp/bp-specific ones (validate_compound_name lists mp/bp-specific shape rules, value_range_check uses mp/bp ranges, unit_conversion_arithmetic is K/°F → °C). Rewrite the table to point at generic scripts + `datatypes/<X>/scripts/`. |
| 238–277 | Phase 4 — Independent verification | [G] | Keep verbatim. Q1–Q5 framework is property-agnostic; verifier prompts customize via overlay pointers (handled in `VERIFICATION_PROMPT_TEMPLATES.md`). |
| 279–281 | Phase 5 — Confidence tagging | [G] | Keep. |
| 283–292 | Phase 6 — Failure handling | [G] | Generic. |
| 294–327 | Anti-patterns | [B] | The four-evidence-locked-fields general rule, the regex-extractor rule, the data-entry-script rule, the past-trials rule are all [G]. Line 326 ("I'll extract this NMR shift…") is mp/bp-specific and moves to overlay's `COMMON_ERRORS.md`. |
| 329–343 | "How this protocol catches errors observed in the wild" table | [S] | All examples are mp/bp-specific (NMR ppm 130.31, PDF sign-loss for °C, TLC eluent, etc.). Move the table to `datatypes/mp_bp/COMMON_ERRORS.md` as worked examples; replace in SKILL.md with a pointer to the overlay. |
| 344–360 | Bundled scripts table | [B] | Generic scripts (crossref_lookup, verify_doi, verify_evidence_quote, quote_support_lint, csv_quote_lint, dedup_within_paper, verify_row, run_all_checks) keep their description. mp/bp-specific scripts (validate_compound_name has mp/bp shape rules, value_range_check, unit_conversion_arithmetic) move under `datatypes/mp_bp/scripts/` and the SKILL.md table gets a separate "Property-specific scripts" section pointing at the overlay. Also: add `conversion_arithmetic_lint.py` as a new generic v2.0 row. |
| 362–370 | When to apply this skill | [S] | "Building a new mp/bp database" — rewrite to "Building a new property database for a supported data type". |
| 372–376 | Reference files | [G] | Add `datatypes/<X>/OVERLAY.md`, `datatypes/<X>/SCHEMA.md`, `datatypes/<X>/COMMON_ERRORS.md` to the list. |
| 378–388 | Evals | [B] | Generic eval coverage description + mp/bp-specific examples (helium / tungsten). The eval taxonomy is structurally generic; the specific evals split per overlay. |

### `README.md` (106 lines)

| Lines | Section | Label | Notes |
|---|---|---|---|
| 1–9 | Title / "What this is" | [S] | mp/bp framing throughout. Full rewrite. |
| 11–19 | Quick start | [B] | Steps are generic; references SKILL.md and the templates. Add: "Specify which data type you are extracting (e.g., `--datatype mp_bp` or in the user prompt)." |
| 21–46 | Directory layout | [S] | Shows v1.7 layout. Replace with v2.0 layout per proposal Section 3. |
| 48–60 | Quick test | [B] | Generic concept; the fixture paths change to `datatypes/mp_bp/evals/files/`. |
| 62–70 | Architectural philosophy | [G] | "Thin scripts, fat prompts" is generic; remove the mp/bp-vs-regex framing in the last paragraph or generalize. |
| 72–94 | Schema | [S] | v1.7 schema. Replace with v2.0 generic schema + pointer to overlay's SCHEMA.md. |
| 96–106 | When to apply | [S] | mp/bp-specific. Generalize: "Building / extending / auditing a property database from a corpus of provided papers; supported data types: mp_bp, redox, etc." Add the "How to add a new data type" pointer. |

The proposal Step 4 explicitly notes the v1.7 README assumes a single mp/bp purpose and will not survive a light edit — confirmed by this audit. **Full rewrite is correct call.**

### `flags.csv`

Sample/artifact file with three columns (row_id, check, detail). Looks like leftover output from a run of `run_all_checks.py`. **Not part of the skill proper.** Remove from `data-extraction/` during Step 3 (or earlier — it shouldn't ship in the package).

---

## `references/` files

### `references/EXTRACTION_PROMPT_TEMPLATES.md` (180 lines)

| Lines | Section | Label | Notes |
|---|---|---|---|
| 1–4 | Title + intro | [S] | "mp/bp extraction" → "data extraction". Generalize. |
| 5–117 | Template 1 — Single-paper extraction | [B] | Structural skeleton is generic (Steps 1–8 are property-agnostic). mp/bp-specific bits to overlay: the v1.7 schema column listing (lines 35–55), the candidate-token list (line 32: mp/Tm/Tfus/bp/Tb), the "Drop these aggressively" list (lines 57–66, NMR/MS/workup solvents), the worked example references, mp/bp-specific Step 7.5 examples (`H-Indeno…`, `H-Pyrrolo…`). Insert pointers: "see `datatypes/<X>/OVERLAY.md` for the property enum, drop patterns, and example row." |
| 118–161 | Template 2 — Bulk-corpus extraction | [B] | Phase 0 structure is generic; the `_skipped.txt` reason list (135–143) is mp/bp-specific and moves to overlay. The accounting equation `processed + skipped == manifest` is generic. |
| 163–167 | Template 3 — Single-paper with smaller scope | [G] | Already generic ("only emit rows that match {filter clause}"). |
| 169–179 | Why these rules matter | [B] | Most failure-mode categories are generic; PDF-column-merge mentions mp/bp tables specifically — replace with property-neutral phrasing. |

### `references/VERIFICATION_PROMPT_TEMPLATES.md` (187 lines)

| Lines | Section | Label | Notes |
|---|---|---|---|
| 1–11 | Intro + Q1–Q5 framework | [G] | Property-agnostic. Keep. |
| 13–34 | Template — Single-row verification — header + Step 0 | [B] | Row fields list (`value_celsius`, `data_type`, etc.) uses v1.7 column names. Update to v2.0 (`value`, `meas_calc`, `units`, `value_min`, `value_max`). |
| 36–70 | Q1 (compound + value correctness) | [B] | Pass/fail criteria are generic but the examples are mp/bp-flavored (workup solvents, ionic-liquid shorthand). Insert pointer to overlay's `SCHEMA.md` for what counts as "the value" + property-specific examples. |
| 72–81 | Q2 (property type correctness) | [S] | Hard-codes the mp/bp property enum (lines 76). Replace with pointer to overlay's `OVERLAY.md` for the property enum + how to distinguish subtypes. |
| 83–94 | Q3 (data type correctness, measured vs calculated) | [G] | Property-agnostic. Keep. (`meas_calc` rename — update the field name.) |
| 96–109 | Q4 (source citation reality) | [G] | Generic. Keep. |
| 111–123 | Verdict block + granular flag list | [B] | Generic structure; some flag names are mp/bp-tied (`flagged_value_out_of_range`); leave as-is but document per-overlay flag extensions. |
| 125–144 | Q5 (verifiability tags) | [G] | Generic. Keep. |
| 146–163 | Output JSON schema + "do not silently correct" | [G] | Keep. |
| 165–175 | Template — Batch verification | [G] | Keep. |
| 177–186 | Anti-patterns for verifiers | [G] | All seven anti-patterns are generic. Keep. |

### `references/COMMON_ERRORS.md` (141 lines)

| Lines | Section | Label | Notes |
|---|---|---|---|
| 1–13 | Intro | [B] | "Common errors in mp/bp extraction" — generalize the title. The "intentionally minimal at v1" framing is generic. |
| 15–76 | Section "Carried-forward known patterns" (entries A–H) | [S] | Every entry is mp/bp-specific (NMR shifts as mp, PDF sign-loss for °C, TLC eluent, etc.). Move the entire block to `datatypes/mp_bp/COMMON_ERRORS.md`. |
| 79–141 | Section "Observed in this skill's trials" (entries I–N) | [B] | Entries I, J, L are mp/bp-specific (specific paper rows). Entries K, M, N are about LLM behavior in general (regex extractor, templated quotes, memory-guessed DOIs) and are property-agnostic — move those to the generic `COMMON_ERRORS.md`. |

---

## `scripts/*.py` (12 files)

Confirms the proposal Section 2 classification: 10 generic in v2.0 (one a deprecated stub), 2 mp/bp-specific moving to `datatypes/mp_bp/scripts/`.

| Script | Label | Disposition in v2.0 |
|---|---|---|
| `crossref_lookup.py` | [G] | Stays in `data-extraction/scripts/`. No changes. |
| `csv_quote_lint.py` | [G] | Stays. No changes. |
| `dedup_within_paper.py` | [G] | Stays. **One small change for the schema rename:** the script's hard-coded column names need to read `value` instead of `value_celsius` (verified by inspecting the source — it uses `value_celsius` for the dedup-key tolerance check). |
| `quote_support_lint.py` | [G] | Stays. Schema rename: reads `value_raw` (still v2.0) and `value_celsius` (now `value`). |
| `quote_template_lint.py` | [G] | Stays. Deprecated stub, no behavior change. |
| `validate_compound_name.py` | [G] in v2.0 | Stays in `data-extraction/scripts/` (per proposal G decision). Strip the mp/bp-specific shape rules — `H-Indeno…` truncated-indicated-hydrogen-locant, EA-prefix detection, "5-acetyl-" trailing-substituent. Move those to `datatypes/mp_bp/COMMON_ERRORS.md`. Keep the property-agnostic rules: bare codes (`compound 5`, `4b`), unbalanced parens, dangling hyphen/prime, terminal unfinished-suffix tokens, leading-paper-local-code prefix, procedure-text-at-start. **Confirm:** the leading-number locant exception (`1,4-benzenedicarboxylic acid`, `2,2'-bipyridine`, `4-aminobenzoic acid`) must pass. |
| `value_range_check.py` | [S] | Moves to `datatypes/mp_bp/scripts/value_range_check.py`. Hard-coded mp/bp ranges; mp/bp-specific. |
| `unit_conversion_arithmetic.py` | [S] | Moves to `datatypes/mp_bp/scripts/`. K/°F → °C only. **Note for Step 4:** also update to emit conversions in the v2.0 standardized syntax (`<input_value_with_units> <operator> <constant> = <output_value_with_units>`) rather than its current free-form output. |
| `verify_doi.py` | [G] | Stays. No changes. |
| `verify_evidence_quote.py` | [G] | Stays. No changes. |
| `verify_row.py` | [G] | Stays. Needs `--datatype <name>` flag + halt-on-missing per Step 4. Schema rename for column references. |
| `run_all_checks.py` | [G] | Stays. Needs `--datatype <name>` flag + auto-discover `datatypes/<name>/scripts/*.py` + halt-on-missing per Step 4. Schema rename. |

**New script (Step 4):** `scripts/conversion_arithmetic_lint.py` — generic syntax-shape lint for the standardized `conversion_arithmetic` column.

---

## `evals/`

### `evals/evals.json` (175 lines, 18 evals)

All 18 evals use mp/bp-specific fixtures (`clean_baseline.csv`, `seeded_errors.csv`, `v15_seeded_errors.csv`, `malformed_csv_quoting.csv`). Each entry classified:

| # | Eval name | Label | Disposition |
|---|---|---|---|
| 1 | `scripts-clean-baseline` | [S] | Tag `datatype: mp_bp`. Update fixture path. |
| 2 | `scripts-detect-seeded-errors` | [S] | Tag `datatype: mp_bp`. Expected-stdout strings depend on mp/bp-specific lints (e.g., `indicated-hydrogen locant`) — may need pruning if those lints move to the overlay. |
| 3 | `csv-quote-lint-detects-unquoted-commas` | [G] | Generic; tag `datatype: generic`. Update fixture path. |
| 4 | `validate-compound-name-detects-truncated-locant` | [S] | mp/bp-specific (`H-Indeno…` truncated-locant rule moves to overlay). Move this eval to `datatypes/mp_bp/evals/`. |
| 5 | `value-range-helium-tungsten-edge` | [S] | mp/bp-specific. Move to overlay. |
| 6 | `unit-conversion-arithmetic-K` | [S] | mp/bp-specific (K → °C). Move to overlay. |
| 7 | `unit-conversion-arithmetic-F` | [S] | mp/bp-specific (°F → °C). Move to overlay. |
| 8 | `validate-compound-name-flags-bare-code` | [G] | Bare-code rule is generic. Tag `datatype: generic`. |
| 9 | `dedup-within-paper-flags-duplicate` | [G] | Generic; tag `datatype: generic`. |
| 10 | `INACCESSIBLE-handling` | [G] | Generic agent-level behavior. Tag `datatype: generic`. |
| 11 | `extract-from-known-paper-with-provenance` | [B] | Generic eval structure but uses an mp/bp paper. Tag with both `datatype: generic` (the protocol assertion) and a known-paper-subdir per overlay. |
| 12 | `verifier-prompt-detects-fabrication` | [G] | Property-agnostic. Tag `datatype: generic`. |
| 13 | `v15-quote-support-lint-detects-missing-value-in-quote` | [G] | Quote-support is generic. Tag `datatype: generic`. |
| 14 | `v16-quote-template-lint-deprecated` | [G] | Generic. |
| 15 | `v16-compound-name-EA-prefix-detection` | [S] | EA-prefix is an mp/bp-table failure mode. Asserts behavior we're MOVING out of the generic `validate_compound_name.py` into the overlay's `COMMON_ERRORS.md`. **Expected to fail under v2.0** unless the EA-prefix detection stays in the generic script (per Step 6 framing in the proposal — "behavior-change failures from Step 3" are expected and need their assertions ported to overlay-level evals). |
| 16 | `v16-compound-name-leading-code-prefix-detection` | [G] | Leading-code prefix is property-agnostic. Keep generic. |
| 17 | `v16-compound-name-procedure-at-start-detection` | [G] | Procedure-text at start is property-agnostic. Keep generic. |
| 18 | `v15-compound-name-shape-expanded` | [G] | All shape rules tested (unfinished-suffix, dangling hyphen/prime, unbalanced parens, procedure-text token) are property-agnostic. Keep generic. |
| 19 | `v15-stereo-descriptors-not-flagged` | [G] | Stereo descriptor parsing is property-agnostic. Keep generic. |

(The JSON has 19 eval entries, not 18 — README.md mentions "10 evals" but that's outdated. **The proposal said 16 evals which was also wrong; actual count is 19.** Not a problem; the SKILL.md doesn't quote a count.)

### `evals/files/`

| File | Label | Disposition |
|---|---|---|
| `clean_baseline.csv` | [S] | Move to `datatypes/mp_bp/evals/files/`. |
| `seeded_errors.csv` | [S] | Move to `datatypes/mp_bp/evals/files/`. |
| `v15_seeded_errors.csv` | [S] | Move to `datatypes/mp_bp/evals/files/`. |
| `malformed_csv_quoting.csv` | [B] | Tests generic CSV-quoting behavior but contains mp/bp data. Could stay at generic `evals/files/` or move to mp_bp; doesn't matter functionally. Leave at top-level `evals/files/` for cleaner generic coverage. |

### `evals/check_no_stereo_false_positives.py`

Tests `validate_compound_name.py` doesn't false-positive on `(E)-`, `(S,S)-`, `(-)-`. Generic check (these are property-agnostic stereo descriptors). Stays at `evals/` top level.

---

## What's NOT in the package but referenced

`SKILL.md` references `audit_criteria.md` at the project root. The audit framework (Tier 1 / Tier 2 / Tier 3, Q1–Q5) is property-agnostic. Step 5 of the migration plan handles the de-mp-bp-ification of that file.

`SKILL.md` references the project's `_archive/example_skill_redox/redox-extraction/` as ancestor. Step 10 ports redox into `datatypes/redox/`.

---

## Summary count

- **Files surveyed:** 22 (excluding `dist/`, `.DS_Store`, `__pycache__/`).
- **Files mostly generic:** 8 (8 of 11 generic scripts + `verify_row.py` + `evals/check_no_stereo_false_positives.py`).
- **Files mostly mp/bp-specific:** 2 (`value_range_check.py`, `unit_conversion_arithmetic.py`) — move to overlay.
- **Files with both content (need splitting in Step 4):** 6 (SKILL.md, README.md, all three `references/*.md`, evals.json).
- **Stray artifact to remove:** `flags.csv` (sample output from a run; not part of the package).

No silent omissions. Every file in `data-extraction/` is accounted for above.

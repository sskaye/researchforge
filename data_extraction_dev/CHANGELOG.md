# Changelog — data-extraction skill (formerly mp-bp-extraction)

Records changes to the property-extraction skill across versions. This file lives outside the skill directory so it's not packaged with the installed skill — agents applying the skill shouldn't need (or see) historical version notes.

For the protocol itself, see `data-extraction/SKILL.md` (v2.0+) or `mp-bp-extraction/SKILL.md` (v1.x, preserved at the repo root as the historical reference). For the development arc and rationale, see `development_report.md`.

## v2.1 — 2026-05-22

Consolidation release. v2.0's modular three-files-per-overlay structure
(OVERLAY.md + SCHEMA.md + COMMON_ERRORS.md per data type) was diagnosed
as a meaningful contributor to Trial-7's regression (97.3 % Tier-1 vs
T5's 99.7 %). Cross-reference count jumped from v1.7's 6 to v2.0's 69
(an 11× increase). v2.1 reduces it by ~64 % while preserving full
modularity.

The trigger was the Trial-7 failure analysis. Four of T7's eight Tier-1
failures and the 37 Tier-2 `quote_missing_compound_token` cases traced
to rules that v1.7 had inline but v2.0 moved behind cross-references.

### Consolidated

- **Each data type's overlay collapses to a single file.**
  - `datatypes/mp_bp/{OVERLAY,SCHEMA,COMMON_ERRORS}.md` → `datatypes/mp_bp/OVERLAY.md` only.
  - `datatypes/redox/{OVERLAY,SCHEMA,COMMON_ERRORS}.md` → `datatypes/redox/OVERLAY.md` only.
  - `datatypes/redox/REFERENCE_ELECTRODES.md` kept (it's a data table consulted by the conversion script, not protocol documentation).
- **Generic patterns moved up.** All 11 cross-property failure modes
  formerly in `datatypes/mp_bp/COMMON_ERRORS.md` (NMR-as-value, PDF
  sign-loss, compound-name truncation, multi-row thead misalignment,
  workup solvents, bare codes, wrong-paper DOI, memory fabrication,
  adjacent-measurement quote, doubled-token, quote-stops-before-value)
  moved to `references/COMMON_ERRORS.md` with `**Example (mp_bp):**`
  tagged illustrations. File grew from 929 → ~2,200 words.
- **Generic skip-reason vocabulary moved up to SKILL.md.** Six
  property-agnostic reasons (`review_no_per_compound_binding`,
  `bare_code_compounds_only`, `binding_ambiguous`,
  `image_only_compound_table`, `formulation_only_no_discrete_compound`,
  `paper_unreadable`) now live in `SKILL.md` Phase 0. Overlays add
  property-specific reasons (e.g., mp_bp adds
  `no_mp_bp_data_in_text`, `tga_or_nmr_only_no_mp_bp`).
- **Property-disambiguation table added to each overlay.** mp_bp's
  table maps borderline labels ("onset of decomposition" → `decomposition`
  not `DSC_onset`; `"X °C, decomp."` → `decomposition` not
  `melting_point`). T7's two property-subtype failures (rows 163, 660)
  trace to this gap.
- **Affirmative compilation-table source_url rule.** Promoted from
  Phase 6 (failure handling) to Phase 1 step 2 (per-row decision):
  *"`source_url` is the DOI of the paper file you are physically
  reading, NOT the DOI of any paper it cites — even when the value was
  originally measured by an earlier paper and compiled into the
  paper-at-hand."* Mirrored in `EXTRACTION_PROMPT_TEMPLATES.md`. T7's
  rows 1212, 1233, 1236, 1244 (the four corpus-availability defects)
  trace to this rule being implied rather than stated.
- **Trailing-decimal / dangling-hyphen suspicion rule.** Added to Phase 2
  quote re-confirmation (step 7) and `EXTRACTION_PROMPT_TEMPLATES.md`
  Step 6: *"If `value_raw` ends at a non-token boundary (trailing
  decimal point with no digits, dangling hyphen), suspect a PDF line
  wrap and read forward to the next physical line."* T7's row 902
  (`mp 158-159.5 °C` truncated to `158-159` because `.5 °C` wrapped to
  the next physical line) is the motivating case.
- **Worked examples in each overlay.** mp_bp now includes four:
  ordinary mp from a synthesis section, K→°C conversion, decomp
  annotation → `property = decomposition`, and a compilation table
  where `source_url` is the corpus paper's DOI not the upstream
  primary's. Same shape for redox.
- **Per-row drop list vs per-paper skip vocabulary explicitly
  distinguished** in SKILL.md and the overlay. v2.0 conflated them
  adjacent on a single OVERLAY.md screen; v2.1 uses explicit
  heading-level labels. *"A paper with some bare-code rows and some
  named-compound rows is NOT a `bare_code_compounds_only` skip — emit
  the named rows and drop the bare-code rows individually per
  Phase 2 step 5."*
- **`textbook:<short-id>` source_url form** documented in SKILL.md
  Phase 1 step 2 (was implicit in v2.0, used in Trial-6).

### Removed

- `datatypes/mp_bp/SCHEMA.md` (content folded into `OVERLAY.md` and
  `SKILL.md`).
- `datatypes/mp_bp/COMMON_ERRORS.md` (generic patterns to
  `references/COMMON_ERRORS.md`; mp/bp-specific anti-patterns to
  `OVERLAY.md`).
- `datatypes/redox/SCHEMA.md` and `datatypes/redox/COMMON_ERRORS.md`
  (same consolidation pattern).

### Numeric impact

| | v1.7 | v2.0 | v2.1 |
|---|---:|---:|---:|
| Total words across files agent reads | 11,405 | 13,833 | ~12,700 |
| Files agent reads for mp/bp extraction | 4 | 8 | 6 |
| Cross-references between files | 6 | 69 | ~25 |
| Files per overlay | n/a | 3 | 1 |

The cross-reference reduction is the load-bearing change. v2.1's 25
cross-references is 4× v1.7's 6 but a substantial drop from v2.0's 69.
For an orchestrator distilling the skill into subagent prompts, this is
~64 % fewer "inline or link?" decisions.

### Migration steps for v2.0 → v2.1

No schema change. v2.0 CSVs (already v2.0-schema) work unchanged with
v2.1. The migration was 11 documentation / structure edits inside the
skill package, plus this CHANGELOG entry and a new
`development_report.md` section.

### Validation

- 17 / 17 deterministic evals pass under v2.1.
- Step-8-style regression on the migrated Trial-5 CSV produces the same
  flag list as v2.0 (no new behavior diffs introduced by the
  consolidation; the v2.0 → v2.1 changes are documentation-only).
- The Step-9 install-and-load test in a real Claude Code / Cowork
  harness is deferred until the next trial.

### Not yet validated

- A fresh extraction trial under v2.1 hasn't been run. The hypothesis
  is that the cognitive-load reduction + the explicit compilation-table
  rule + the property-disambiguation table close most of the v2.0→T7
  gap relative to v1.7→T5. The next trial will measure this.

## v2.0 — 2026-05-21

Modularization release. Generalizes the v1.7 mp/bp-specific skill so it can be applied to other measurement data types (redox potentials, viscosity, etc.) while preserving every "context shapes the result" defense from v1.4–v1.7. The skill is renamed from `mp-bp-extraction` to `data-extraction`; v1.7 stays at the repo root as `mp-bp-extraction/` until v2.0 is validated by a real trial run.

The migration was specified in `generalization_proposal.md` and executed in 11 testable steps.

### Renamed / restructured

- **Skill renamed:** `mp-bp-extraction` → `data-extraction`. The skill is property-agnostic at its core.
- **Schema generalized:**
  - `value_celsius` → `value` (generic, unit-bearing).
  - `value_celsius_min` → `value_min`.
  - `value_celsius_max` → `value_max`.
  - **New column `units`** (e.g., `°C`, `V vs SHE`, `Pa·s`) — required for numeric values; allowed empty for categorical-valued properties.
  - `data_type` → `meas_calc` (renamed to avoid clashing with "data type" used everywhere in the proposal to mean the property family).
- **Schema width 17 → 18 columns.** v2.0-canonical column order documented in `data-extraction/SKILL.md` and `data-extraction/datatypes/<X>/SCHEMA.md`.
- **Modular layout.** Property-specific content moves into `data-extraction/datatypes/<X>/{OVERLAY.md, SCHEMA.md, COMMON_ERRORS.md, scripts/, evals/files/}` overlays. Two data types ship in v2.0: `mp_bp` (the production mp/bp skill, fully migrated) and `redox` (built from the archived `_archive/example_skill_redox/`).

### Added

- **`--datatype <name>` required flag** on `run_all_checks.py` and `verify_row.py`. Both halt with exit 2 and an available-data-types listing if the flag is missing or names an overlay that doesn't exist. No implicit "generic only" mode — the agent must specify the data type up front (or halt and ask the user).
- **Halt-on-missing-overlay rule** in `SKILL.md` MANDATORY READING block.
- **Standardized `conversion_arithmetic` syntax** (v2.0): `<input_value_with_units> <operator> <constant> = <output_value_with_units>`. Both ASCII (`-`, `*`) and unicode (`−`, `×`) operators are accepted as input; new output should use unicode.
- **New generic script `scripts/conversion_arithmetic_lint.py`** verifies the syntax shape. Ships with unit tests (`evals/check_conversion_arithmetic_lint.py`) covering 6 valid and 4 invalid shape examples.
- **Empty-when-not-applicable conventions** documented in `SKILL.md`: `compound_smiles`, `value_min`/`value_max`, `units` (for categorical), `conversion_arithmetic`, and `notes` may be empty; all other generic columns required.
- **`datatypes/mp_bp/` overlay** — preserves the v1.7 production behavior: property enum, value-range checks, K/°F → °C conversion, mp/bp-specific failure-mode catalog.
- **`datatypes/redox/` overlay** — ported from `_archive/example_skill_redox/`. Adds extension columns: `reference_electrode` (required), `solvent`, `ph`, `n_electrons` (optional). Standardized unit string `V vs SHE`.
- **`migrate_v17_to_v20.py` at the repo root** — one-time migration utility (not part of the shipped skill). Renames v1.7 columns and inserts `units = "°C"`. Used in Step 7 to migrate Trial-5 and Trial-6 CSVs (`opus47_mp_bp_v20.csv`, `mp_bp_data_v20.csv`).

### Changed

- **`validate_compound_name.py` is now generic** (stays in `data-extraction/scripts/`). The only v1.7-era rule that was actually mp/bp-specific — the `mp =` / `m.p. =` tokens inside `_PROCEDURE_WORDS` — was stripped. The other rules (bare codes, truncated locants, EA-prefix, leading paper-local code, procedure-text-at-start) are all property-agnostic compound-name shape rules and apply to any chemistry data type.
- **`references/COMMON_ERRORS.md` slimmed** to keep only the property-agnostic LLM-behavior anti-patterns (entries K, M, N from v1.7: regex extractors, templated quotes, memory-guessed DOIs). The mp/bp-specific patterns (entries A–H, I, J, L) moved to `datatypes/mp_bp/COMMON_ERRORS.md`.
- **`SKILL.md` schema section rewritten** to document the 18-column generic core inline. Overlays now own their property enum, standardized unit string, and any extension columns.
- **`run_all_checks.py` auto-discovers** `datatypes/<name>/scripts/*.py` and invokes each after the generic scripts. The hard-coded `value_range_check.py` / `unit_conversion_arithmetic.py` calls are gone — they're picked up via the overlay glob.
- **`verify_row.py` rewritten** to import overlay scripts via `importlib`; calls every overlay script with a `check_row(row) -> str | None` signature.
- **`audit_criteria.md` at the project root** rewritten to be data-type-agnostic. mp/bp-specific examples are now explicitly marked `**Example (mp_bp):**`. The verifier prompt template parameterizes Q1(b)/Q2 with overlay pointers. `data_type` → `meas_calc` flag rename (`flagged_data_type_mismatch` → `flagged_meas_calc_mismatch`).
- **`csv_quote_lint.py`** updated to check the `meas_calc` column instead of `data_type`.
- **`dedup_within_paper.py`** reads `value` and `meas_calc` instead of `value_celsius` and `data_type`. Tolerance default unchanged at 0.5; documented as overridable for unit scales other than °C.
- **README.md fully rewritten** to document v2.0 usage (data-type specification, halt rule, modular layout) and include a "How to add a new data type" recipe.
- **Verifier prompt** (`references/VERIFICATION_PROMPT_TEMPLATES.md`) parameterized with `{datatype}` placeholder; Q1(b) and Q2 reference the overlay's `SCHEMA.md` and `OVERLAY.md`.

### Removed

- **`flags.csv` artifact** at the skill root (leftover from a prior `run_all_checks.py` run; not part of the package).

### Behavior diffs vs v1.7 (Step-8 regression test)

Running the v2.0 modular skill against the migrated Trial-5 (2,063 rows, full) and a uniform-random 500-row subset of migrated Trial-6 produced one intentional flag-count diff vs the v1.7 baseline:

- **`conversion_arithmetic_lint.py`** (new in v2.0) surfaces +58 syntax-shape issues in Trial-5 conversion strings and +1 in the Trial-6 subset. These weren't checked under v1.7. All other categories (value-out-of-range, conversion-math-disagrees, dedup, required-field, EA-prefix, etc.) showed +0 diff. No regressions from the schema rename or the overlay restructure.

### Migration tests run

All Step-1-through-Step-10 tests in `generalization_proposal.md` passed:

- Step 1: byte-identical copy (md5 + `diff -r`).
- Step 2: `_audit_notes.md` covers every file with no silent omissions.
- Step 3: file moves verified by checksum; new overlay docs non-empty.
- Step 4: 17 deterministic evals pass; halt rule works; new `conversion_arithmetic_lint.py` ships with unit tests.
- Step 5: `audit_criteria.md` grep shows mp/bp matches only in `Example (mp_bp):` blocks.
- Step 6: 17/17 deterministic evals pass under the new structure.
- Step 7: Trial-5 (2,063 rows) and Trial-6 (15,741 rows) migrated to `*_v20.csv` with full row-count parity, `units = °C` on every row, `meas_calc` row-for-row match with v1.7 `data_type`.
- Step 8: Regression flag counts match v1.7 except for the one intentional `conversion_arithmetic_lint` increment noted above.
- Step 9: `dist/data-extraction.skill` zip integrity passes; front matter parses to `name: data-extraction, version: v2.0`. Harness install-and-load deferred until the v2.0 package is dropped into Claude Code / Cowork.
- Step 10: `run_all_checks.py --datatype redox` runs all three redox scripts plus the generic checks without crashing on a 3-row clean baseline; halt rule lists both `mp_bp` and `redox`.

### Operational notes (not part of the .skill artifact)

- v1.7 `mp-bp-extraction/` stays at the repo root until v2.0 is validated on a fresh corpus. After that we can formally archive it.
- The redox overlay is structurally complete but hasn't been audit-tested against a real redox corpus. The existing redox fixtures from `_archive/example_skill_redox/redox-extraction/evals/files/` use the v1.7 redox-schema (`molecule`, `voltage_v_she`), not v2.0 — a separate one-off migration would be needed to use them as regression baselines.
- The harness install-and-load test (Step 9) requires dropping `dist/data-extraction.skill` into a real Claude Code or Cowork install — defer until v2.0 is being trialed for real.

## v1.7 — 2026-05-14

Motivated by Trial-4's recall analysis (see `reports/trial4_comparison_report.md`). v1.6 audited at 98.0 % Tier-1 correctness on Opus (statistically tied with both T2 and T3 under matched criteria) — that part of the skill is stable. But Trial-4 emitted 1,529 rows vs T2's 1,864, and 91 % of the gap traced to 31 papers in four category subfolders that Opus explicitly filtered out. In its self-analysis Opus admitted: *"I lifted the framing from the Trial3-full-opus47/EXTRACTION_SUMMARY.md that I read as a reference at the start of the run, without questioning whether the same exclusion applied here."*

This is a new failure mode — cross-trial contamination — where past trial outputs were treated as if they defined protocol. v1.7 adds two structural defenses in the skill plus an operational note about sandboxing future trial dispatches.

### Added

- **Phase 0 — corpus manifest (required, before Phase 1).** New section in SKILL.md and a new Step 0 in EXTRACTION_PROMPT_TEMPLATES.md Template 2. The agent must enumerate every paper-bearing location in the corpus (descending into subfolders) and write `_corpus_manifest.txt` before processing any paper. Phase 1 is gated on the manifest being non-empty. The skill stays generic — it does not prescribe a specific `find` pattern because corpora vary in layout.
- **`_skipped.txt` requirement.** Anything the agent intentionally excludes from extraction must be logged as `<location>\t<reason>` with a reason from a fixed taxonomy: `review_no_per_compound_binding`, `bare_code_compounds_only`, `no_mp_bp_data_in_text`, `tga_or_nmr_only_no_mp_bp`, `binding_ambiguous`, `image_only_compound_table`, `formulation_only_no_discrete_compound`, `paper_unreadable`. Free-text reasons require asking the user first. Taxonomy starts from Opus's Trial-4 categorization of its 24 zero-row papers.
- **EXTRACTION_SUMMARY accounting requirement.** The agent's run report must include the equation `processed + skipped == manifest`. Numbers that don't balance indicate silent loss.
- **Past-trials anti-pattern.** New entry in the SKILL.md anti-patterns list: "❌ The prior trial run did X, so I'll do X too." Codifies the lesson that past trial outputs are observations, not protocol. Names the Trial-4 example (17 % recall loss from regex-grepping out category subfolders that a prior trial had also excluded).
- **Pre-flight checklist** gains two new bullets: corpus enumeration before Phase 1, and "treat past trial outputs as reference, not protocol."

### Operational note (not part of the .skill artifact)

Future trial dispatches should sandbox the agent's read scope to the skill directory + the corpus. Past `Trial*-*/` directories, `audit_criteria.md`, `development_report.md`, and other prior-run artifacts should be out of scope unless explicitly handed over with framing. The v1.7 skill-side defenses are belt-and-suspenders; sandboxing is the primary defense.

### Unchanged from v1.6

- All Tier-1 correctness rules (DOI-from-file-only, compound-name shape lint with EA-prefix / leading-code-prefix / procedure-text-at-start, no regex extractors, no data-entry scripts).
- All Tier-2 verifiability rules (`quote_support_lint.py` advisory; `quote_template_lint.py` deprecated stub).
- Phase 4 sampling rule (`max(100, 5 %)` parallel-dispatch).
- The verifier prompt template structure (Q1–Q4 = PASS/FAIL, Q5 = separate verifiability report).

### What v1.7 did NOT add

- **No reconciliation-checker script.** The Phase 0 manifest + `_skipped.txt` are enforcement by design (the agent has to write them) rather than enforcement by check. If a future trial shows a "manifest-vs-emitted mismatch" failure pattern, add the script then.
- **No new compound-name lint patterns for Trial-4's single occurrences** (the "sodium salt route" suffix, the wrong-isomer-binding in PMC7148931). Single occurrences don't justify lint additions.
- **No corpus-specific enumeration mechanism.** The skill stays generic so it can be applied to differently-structured corpora.

### Predicted Trial-5 outcome

Same Tier-1 correctness (~98 %), same Tier-2 verifiability (~95–96 %), recall back at T2-equivalent (~1,800–1,900 rows) because the manifest step + sandbox forces full corpus coverage with explicit skip-accounting.

## v1.6 — 2026-05-13

Motivated by the Trial-3 audit re-scored under corrected criteria (`audit_criteria.md`). v1.5 produced no Tier-1 correctness improvement over v1.4 on Opus (98.7 % → 97.0 %, p = 0.16) but cost ~27 % recall. v1.5's apparent precision win was a verifiability improvement that the audit rubric had mistakenly counted as correctness. v1.6 keeps the genuine correctness wins from v1.5 and downgrades the verifiability constraints to advisory.

### Kept from v1.5 (genuine Tier-1 correctness wins)

- **DOI-from-file-only rule** — `verify_doi.py` substring-checks DOIs against the paper file; agents must not memory-guess DOIs. Eliminates the v1.4 DOI-fabrication failure mode (4/300 on Opus T2 → 0/300 on Opus T3).
- **Generalized "no scripts produce row values" anti-pattern** — preserves the lesson from cross-model validation. Zero behavioral impact on Opus (Opus doesn't write data-entry scripts) but kept as documentation.
- **Expanded `validate_compound_name.py` shape lint** — terminal unfinished-suffix, dangling hyphen/prime, balanced brackets, narrow procedure-text contamination.
- **Phase 4 sampling rule** — `max(100, 5%)` parallel verifier dispatch. Now also documented in `audit_criteria.md`.

### Added in v1.6 (new Tier-1 correctness checks)

- **EA-prefix contamination detection** — `validate_compound_name.py` flags rows where `compound_name` begins with elemental-analysis text (`C, NN.NN; H, N.NN; N, N.NN.`) prepended to a real IUPAC name. Caught 3 of T3 Opus's 4 original-audit failures and ~140 contaminated rows across the full corpus that v1.5 missed.
- **Leading paper-local code prefix detection** — flags rows where `compound_name` starts with a serial code in the form `"6 (IUPAC name)"` rather than `"IUPAC name (6)"`. Re-enables the Phase 6e leading-context-prefix rule from the regex-based predecessor.
- **Procedure-text-at-start detection** — flags `compound_name` fields that begin with appearance / yield / procedure text (`(Yield 94%),`, `White solid,`, `Yellow powder`). Caught T3 Opus row 530.

### Downgraded from Tier-1 (strict) to Tier-2 (advisory) in v1.6

- **Quote-must-contain-value rule** — `quote_support_lint.py` still flags rows where `evidence_quote` doesn't contain the numeric value, but the lint is now **advisory** (warning, not auto-fail). The umbrella `run_all_checks.py` no longer propagates this lint's exit code. The extraction prompt no longer instructs agents to "DROP the row" on quote-fidelity issues — instead, "record the closest contiguous span; lints flag, don't auto-drop." Predicted recall recovery: ~480 rows on Opus on a comparable corpus (the 42 indexed-PMC papers Opus T3 visited and emitted 0 rows for under the v1.5 strict rule).
- **Verifier prompt updated to match `audit_criteria.md`** — Q1–Q4 determine Tier-1 PASS/FAIL on (a) compound + value correctness, (b) property type, (c) data_type per schema (review-paper compilations are `measured`), (d) source citation reality. Q5 is a separate verifiability report that does NOT affect the PASS/FAIL verdict.

### Dropped entirely in v1.6

- **No-ellipsis-in-quote rule** — papers legitimately use ellipsis in their own text; section-header-then-mp patterns require an elision in the captured span. Forcing this rule cost Opus rows in T3 with no Tier-1 correctness benefit. The check has been removed from `EXTRACTION_PROMPT_TEMPLATES.md` Step 6.1 and from `VERIFICATION_PROMPT_TEMPLATES.md` Step 4. The `quote_template_lint.py` script that enforced this (along with template-quote prohibition) has been replaced with a deprecated no-op stub for backward compatibility.
- **Templated-quote prohibition** — `quote_template_lint.py`'s flagging of `"Table N: <compound> MP <value>"`-style strings is no longer enforced. The cross-model concern that originally motivated it (Sonnet's data-entry script) is addressed by the kept-from-v1.5 anti-script anti-pattern, which targets the construction mechanism rather than the resulting string shape.

### Doc / packaging

- SKILL.md schema row for `evidence_quote` reworded: "verbatim text from the source containing the value; prefer contiguous; quote fidelity is a verifiability concern, not a correctness gate."
- SKILL.md Phase 2 quote re-confirmation step rewritten: Tier-1 checks (wrong-compound-binding) cause drops; Tier-2 issues (PDF format) get flagged but not dropped.
- SKILL.md anti-patterns list trimmed (removed ellipsis-bridge anti-pattern; kept all others).
- SKILL.md Phase 3 checks table annotated with Tier-1 / Tier-2 / Tier-3 labels.
- Bundled-scripts table updated to label `quote_support_lint.py` as advisory and to remove the now-deprecated `quote_template_lint.py` from the active set (file kept as a no-op stub for back-compat).
- Front-matter `description:` rewritten (981 chars, under the 1024 limit) to reflect the v1.6 framing.
- New v1.6 evals in `evals/evals.json` for EA-prefix, leading-code-prefix, and procedure-text-at-start patterns. v1.5 `v15-quote-template-lint` eval removed.
- New seeded-error rows 16–18 in `evals/files/v15_seeded_errors.csv` exercising the new lints.
- New companion doc `audit_criteria.md` at the project root: source of truth for what an audit measures and how to run one. Not part of the installed skill.

## v1.5 — 2026-05-13

Six changes, motivated by Trial-2 audit results (Opus 98 % / GPT-5.5 86 % / Sonnet 55 %) and the three agents' self-analyses (`reports/trial2_analysis_*.md`).

- **Quote must contain the value.** New rule in `SKILL.md` (Phase 2, schema row) and `EXTRACTION_PROMPT_TEMPLATES.md` (Step 6.2): the numeric portion of `value_raw` must be a substring of `evidence_quote`. Catches the "Dark red solid;" failure mode where the quote is verbatim present but stops before the m.p. line.
- **New `scripts/quote_support_lint.py`.** Deterministic check enforcing the rule above. Reports value-not-in-quote rows as hard failures; compound-name-not-in-quote rows as advisories (synthesis papers often print the compound name in the section header above the quoted m.p. line — legitimate pattern).
- **Generalized anti-pattern: no script-generated row values.** Replaces the v1.4 regex-extractor-specific prohibition with a broader principle: scripts may not produce or transform `compound_name`, `value_raw`, `evidence_quote`, or `source_url`. Orchestration / dedup / enum-normalization scripts are still fine. Catches Sonnet 4.6's Path-B failure: a data-entry script that hardcoded values + templated quotes via f-strings produced 770 rows of paraphrased (non-verbatim) quotes.
- **No-ellipsis rule + `scripts/quote_template_lint.py`.** Step 6.1 "Do NOT allow" list gains a bullet forbidding ellipsis-bridged spans. New deterministic script flags templated patterns: `^Table\s+[IVX\d]+[:,.]`, inline `MP X BP Y`, literal `...` or `…` in the quote, column-header tokens used as field separators.
- **Expanded compound-name shape lint.** `validate_compound_name.py` extended with terminal unfinished-suffix detection (`Carboxamid$`, `Carbo$`, etc.), dangling hyphen/prime tail, balanced-bracket check, narrow procedure-text contamination check. Specifically NOT flagging legitimate stereo-descriptor opens like `(E)-`, `(-)-`, `(2E,4E)-` (false positive observed in initial v1.5 draft and corrected).
- **DOI-from-file-only rule.** SKILL.md Phase 1 Step 2 and EXTRACTION_PROMPT_TEMPLATES.md Step 1b now explicitly state: extract DOI only from NXML doi-id, PDF front matter, or metadata.json — never from the paper's reference list (those DOIs belong to *cited* papers), never from training memory. Trial-2 found 4 Sonnet rows citing DOIs that appear nowhere in the source files.
- **Phase 4 sampling rule + parallel-dispatch pattern.** SKILL.md Phase 4 section rewritten with concrete rules: sample size `max(100 rows, 5 % of total rows)`, parallel dispatch (25 rows per fresh-context agent in one batch), failure escalation by running the relevant deterministic lint across the full CSV + one confirmation sample. Per-row audit cost ≈ per-row extraction cost, so 5 % adds ~5 % wall time at any corpus size.

Wired both new scripts into `run_all_checks.py`. Updated the SKILL.md Phase 3 checks table and bundled-scripts table. Bumped version front-matter to v1.5; front-matter `description:` rewritten (908 chars, under the 1024 limit) to lead with the four-field rule and reference the 55 % vs. 98 % Trial-2 spread.

Implementation note: an earlier v1.5 draft included a "leading open-paren in compound_name = truncation" rule. Dropped because legitimate IUPAC names routinely start with parenthesized stereo descriptors. Sonnet's actual failure (missing leading "4-(4-" substituent block) is already caught by the bracket-balance check.

## v1.4 — 2026-05-12

- Added an explicit MANDATORY-READING block at the top of `SKILL.md` stating that the agent reads each paper directly and does NOT write a Python regex extractor.
- New anti-pattern entry in `SKILL.md` forbidding regex-based bulk extractors (first position in the list).
- Phase 4 (independent verification) now explicitly labeled as mandatory before declaring success.
- `scripts/run_all_checks.py` prints a warning when >90 % of rows are still `pending_verification` (i.e., Phase 4 hasn't been run).
- Strengthened the front-matter `description:` so the skill's purpose statement leads with "LLM-driven" extraction and explicitly forbids the regex approach.
- New entry K in `references/COMMON_ERRORS.md` documenting the regex-extractor misapplication observed in cross-harness validation (56 % audit pass rate vs. 93 % for the prescribed approach).

Motivated by a parallel cross-harness validation where a different agent absorbed the protocol's contract (`evidence_quote`, schema, `source_url` formats, deterministic checks) but missed the methodology — wrote a regex extractor instead of reading papers directly — and reached 56 % audit pass vs. 93 % for the protocol-intended approach.

## v1.3 — 2026-05-12

- Added multi-line compound-name reassembly step to `EXTRACTION_PROMPT_TEMPLATES.md` Template 1 (read the line above section headers; reject `H-Indeno...` indicated-hydrogen-locant truncations; resolve `pdftotext` doubled-token artifacts).
- Mandated RFC-4180 CSV quoting in the extraction prompt (use `csv.QUOTE_ALL` or wrap fields containing comma/quote/newline in double quotes).
- New `scripts/csv_quote_lint.py` to catch unquoted-comma column shifts at sanity-check time. Added to `run_all_checks.py`.
- New `_TRUNCATED_LOCANT_PREFIX` pattern in `validate_compound_name.py` detecting names that start with `[A-Z]H-[A-Z]` or `H-Pyrrolo/Indeno/Pyrazolo/...` (the indicated-hydrogen locant truncation pattern).
- Two new entries in `references/COMMON_ERRORS.md` (I: adjacent-measurement quote; J: doubled-token PDF artifact).
- Added seeded-error rows to `evals/files/seeded_errors.csv` for the new truncation pattern; added `evals/files/malformed_csv_quoting.csv` for the CSV quoting check. Two new evals in `evals/evals.json`.

Motivated by Trial-1-full audit findings: 5 of 7 audit failures were compound-name truncation; 44 rows across 3 of 14 batches had CSV-quoting bugs that required programmatic repair.

## v1.2 — 2026-05-12

- Added explicit 4-step quote re-confirmation requirement in `SKILL.md` Phase 2, fired before each row is committed:
  1. Substring-search the paper for the quote (whitespace-normalized).
  2. Reject doubled-token PDF artifacts.
  3. Confirm the value in the verified-present quote matches `value_raw`.
  4. Confirm the compound in the quote matches `compound_name`.
- `EXTRACTION_PROMPT_TEMPLATES.md` Step 6 rewritten with concrete rejection patterns (missing words, doubled tokens, adjacent-measurement quotes).
- `VERIFICATION_PROMPT_TEMPLATES.md` Step 4 rewritten to explicitly reject doubled-token PDF artifacts and adjacent-measurement quotes.

Motivated by Trial-1-val's two audit failures (rows 147 and 296): both had correct compound + value but wrong `evidence_quote` text (one captured the freezing-point line instead of the boiling-point line on an adjacent row; one transcribed a `pdftotext -layout` column-doubling artifact).

## v1.1 — 2026-05-12

- Extended `source_url` schema to support `pmc:PMCxxxxxxx`, `pmid:xxxxxxx`, `textbook:<id>`, and `legacy:<folder-name>` prefixes (in addition to DOI URLs).
- Updated `EXTRACTION_PROMPT_TEMPLATES.md`, `VERIFICATION_PROMPT_TEMPLATES.md`, and the `SKILL.md` Phase 1 step 2 / Phase 6 to document the priority order (DOI > PMC > PMID > legacy) and explicitly clarify that a missing DOI is not an error when the citation is complete.
- `scripts/verify_doi.py` and `scripts/verify_evidence_quote.py` updated to resolve PMC-keyed lookups by scanning subdirectory names for `PMC#######` patterns.
- Verifier prompt's Q6 step updated to accept any of the identifier forms.

Motivated by Trial-1-dev paper 157 (Int J Mol Sci 2007), which has no DOI in its NXML or PDF. The original v1.0 protocol required a DOI URL and flagged all 6 of paper 157's rows; v1.1 lets older / non-PMC / pre-DOI-era papers extract normally using whatever stable identifier the paper carries.

## v1.0 — 2026-05-11

Initial release. LLM-driven evidence-locked extraction protocol for melting-point and boiling-point data. Mandatory verbatim `evidence_quote` per row; refusal-to-fabricate via INACCESSIBLE; deterministic Phase 3 checks; independent Phase 4 verification.

Built after a 6,400-LOC regex-based predecessor (`property-extractor`, attempt 1) plateaued at 67 % dev / 41 % val audit pass rate. v1.0 reaches 100 % dev / 98 % val with ~1,100 LOC by inverting the architecture: LLM does the semantic extraction, scripts do only deterministic checks.

Modeled after the sibling `redox-extraction` skill, which uses the same pattern for redox-potential data.

# Changelog — mp-bp-extraction skill

Records changes to the `mp-bp-extraction` skill across versions. This file lives outside the skill directory so it's not packaged with the installed skill — agents applying the skill shouldn't need (or see) historical version notes.

For the protocol itself, see `mp-bp-extraction/SKILL.md`. For the development arc and rationale, see `development_report.md`.

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

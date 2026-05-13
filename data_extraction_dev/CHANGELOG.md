# Changelog — mp-bp-extraction skill

Records changes to the `mp-bp-extraction` skill across versions. This file lives outside the skill directory so it's not packaged with the installed skill — agents applying the skill shouldn't need (or see) historical version notes.

For the protocol itself, see `mp-bp-extraction/SKILL.md`. For the development arc and rationale, see `development_report.md`.

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

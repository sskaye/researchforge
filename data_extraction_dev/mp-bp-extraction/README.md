# mp-bp-extraction

An evidence-locked extraction protocol for melting-point and boiling-point data from a provided set of journal articles.

## What this is

A reusable skill (in the style of `redox-extraction`) that turns a directory of papers into a CSV of mp/bp values, with strict per-row provenance, automated sanity checks, and an independent verification pass.

Designed to be applied by a Claude agent. The agent does the reading + writing; the bundled scripts do the deterministic checks.

## Quick start

1. **Read `SKILL.md`.** That's the protocol — schema, six phases, anti-patterns.
2. **Apply Template 1 from `references/EXTRACTION_PROMPT_TEMPLATES.md`** for single-paper extraction or Template 2 for a corpus.
3. **Run sanity checks** on the resulting CSV:
   ```bash
   python3 scripts/run_all_checks.py output.csv --paper-root <papers_dir>
   ```
4. **Independent verification** (Phase 4): dispatch a fresh agent with the prompt in `references/VERIFICATION_PROMPT_TEMPLATES.md` for each row (or batches).

## Directory layout

```
mp-bp-extraction/
├── SKILL.md                              # The protocol (350+ lines)
├── README.md                             # This file
├── scripts/                              # 8 deterministic sanity-check scripts
│   ├── crossref_lookup.py                # DOI → authoritative metadata
│   ├── validate_compound_name.py         # name shape + SMILES validity
│   ├── value_range_check.py              # mp/bp plausible-range filter
│   ├── unit_conversion_arithmetic.py     # K/°F → °C math verifier
│   ├── verify_doi.py                     # DOI in row matches DOI in paper file
│   ├── verify_evidence_quote.py          # verbatim quote present in paper file
│   ├── dedup_within_paper.py             # collapse duplicate rows
│   ├── verify_row.py                     # per-row programmatic checks
│   └── run_all_checks.py                 # umbrella runner
├── references/
│   ├── COMMON_ERRORS.md                  # anti-pattern catalog (filled as we observe)
│   ├── EXTRACTION_PROMPT_TEMPLATES.md    # copy-paste agent prompts
│   └── VERIFICATION_PROMPT_TEMPLATES.md
└── evals/
    ├── evals.json                        # 10 evals (deterministic + agent-based)
    └── files/
        ├── clean_baseline.csv            # 5 rows that pass every check
        └── seeded_errors.csv             # 9 rows with deliberate errors
```

## Quick test

Verify the scripts work against the bundled fixtures:

```bash
# Clean fixture: zero flags expected
python3 scripts/run_all_checks.py evals/files/clean_baseline.csv
echo "exit=$?"   # → 0

# Seeded-error fixture: every deliberate error should be flagged
python3 scripts/run_all_checks.py evals/files/seeded_errors.csv
echo "exit=$?"   # → 1
```

## Architectural philosophy

This skill follows the `redox-extraction` model: **thin scripts, fat prompts**.

- The Claude agent reads the actual paper file(s) and writes rows with a verbatim `evidence_quote`. The agent does the semantic work (identifying the compound, value, units, data type).
- The scripts only do deterministic checks an LLM can't do reliably: arithmetic verification, range plausibility, SMILES validity, DOI substring presence, duplicate detection.
- An **independent verifier agent** (fresh context, no extractor notes) re-reads the source and confirms every row's evidence quote.

The previous attempt at this problem (see `../_property-extractor_attempt1/`) used regex / NXML parsing for extraction. That approach hit a ceiling around 67 % dev / 41 % val pass rate on independent audits. The redox-extraction skill achieved 96–100 % using the LLM-driven pattern — this skill applies the same pattern to mp/bp.

## Schema

A single CSV with these required columns:

| Column | Notes |
|---|---|
| `id` | Sequential integer |
| `verification_status` | `pending_verification`, `verified_extraction`, `flagged_review`, etc. |
| `compound_name` | Full IUPAC / common / trivial name; never truncated |
| `compound_smiles` | Optional; validated by RDKit when populated |
| `property` | `melting_point` / `boiling_point` / `DSC_onset` / `DSC_peak` / `decomposition` / `sublimation` |
| `value_celsius` | Numeric, canonical °C |
| `value_celsius_min`, `value_celsius_max` | When value is a range |
| `value_raw` | As printed in source, with units |
| `relation` | `=`, `>`, `<`, `~`, `≈` |
| `data_type` | `measured` or `calculated` |
| `source`, `source_url` | Citation; no author names; DOI in URL |
| `evidence_location` | Precise pointer (e.g., "Table 1 row 3") |
| `evidence_quote` | **MANDATORY** verbatim text from source |
| `conversion_arithmetic` | K → °C or °F → °C math when applied |
| `notes` | Optional |

See `SKILL.md` for full schema details and worked examples.

## When to apply

Apply this skill when:
- Building an mp/bp database from a corpus of provided papers
- Extending an existing mp/bp database
- Auditing an existing mp/bp extraction for errors

Do **not** apply this skill for one-off questions ("what's the boiling point of methanol?") — that's overkill.

This skill **does not fetch papers**. The user provides them as subdirectories on disk. If you also need to find / fetch papers from the literature, use a separate paper-discovery skill first, then apply this one.

# data-extraction

An evidence-locked extraction protocol for chemistry property data from a
provided set of journal articles or textbook compilations. Generic at its
core; the property family (mp/bp, redox, viscosity, …) is supplied as a
data-type overlay under `datatypes/<X>/`.

v2.1 (consolidated modular layout). The v1.x line shipped as
`mp-bp-extraction/` and is preserved at the repo root as the historical
reference. v2.0 (modular layout, 3 files per overlay) was superseded by
v2.1 after Trial-7 revealed that the 3-file-per-overlay structure imposed
a meaningful cognitive / context load on the extraction agent. v2.1
consolidates each overlay to a single `OVERLAY.md` file and moves the
property-agnostic patterns up to `references/COMMON_ERRORS.md`.

## What this is

A reusable skill that turns a directory of papers (or a textbook) into a
CSV of property values, with strict per-row provenance, automated sanity
checks, and an independent verification pass.

Designed to be applied by a Claude agent. The agent does the reading and
writing; the bundled scripts do the deterministic checks; an independent
verifier agent re-reads the source to confirm each row.

## Quick start

1. **Tell the skill which data type you want extracted.** This is required.
   Currently supported: `mp_bp` (melting and boiling points; six property
   values). `redox` ships in a future migration step.
2. **Read `SKILL.md`.** That's the generic protocol — schema (18 columns),
   seven phases, anti-patterns, conversion-arithmetic syntax.
3. **Read `datatypes/<datatype>/OVERLAY.md`.** That's the per-property
   specifics — value ranges, unit conversions, drop-list patterns, the
   `property` enum.
4. **Apply Template 1 from `references/EXTRACTION_PROMPT_TEMPLATES.md`**
   for single-paper extraction or Template 2 for a corpus.
5. **Run sanity checks** on the resulting CSV:

   ```bash
   python3 scripts/run_all_checks.py --datatype <name> output.csv \
       --paper-root <papers_dir>
   ```

   The `--datatype` flag is required. The umbrella halts if it's missing
   or names an overlay that doesn't exist, with a list of installed data
   types.

6. **Independent verification** (Phase 4): dispatch a fresh agent with the
   prompt in `references/VERIFICATION_PROMPT_TEMPLATES.md` for each row
   (or batches). Q1(b) and Q2 customize per overlay; the rest is generic.

## Directory layout

```
data-extraction/
├── SKILL.md                              # generic protocol
├── README.md                             # this file
├── scripts/                              # generic deterministic checks
│   ├── crossref_lookup.py                # DOI → authoritative metadata
│   ├── validate_compound_name.py         # name shape + SMILES validity
│   ├── conversion_arithmetic_lint.py     # v2.0 conversion syntax (new)
│   ├── verify_doi.py
│   ├── verify_evidence_quote.py
│   ├── quote_support_lint.py             # quote contains value (advisory)
│   ├── quote_template_lint.py            # deprecated stub
│   ├── csv_quote_lint.py
│   ├── dedup_within_paper.py
│   ├── verify_row.py                     # per-row checks (generic + overlay)
│   └── run_all_checks.py                 # umbrella; auto-discovers overlays
├── references/
│   ├── EXTRACTION_PROMPT_TEMPLATES.md    # copy-paste agent prompts
│   ├── VERIFICATION_PROMPT_TEMPLATES.md  # Q1–Q5 verifier protocol
│   └── COMMON_ERRORS.md                  # generic LLM-behavior errors only
├── datatypes/
│   ├── mp_bp/                            # supported data type
│   │   ├── OVERLAY.md                    # SINGLE file: enum, schema, examples,
│   │   │                                 # ranges, conversions, drop patterns,
│   │   │                                 # property-specific skip reasons,
│   │   │                                 # mp/bp failure-mode catalog
│   │   ├── scripts/
│   │   │   ├── value_range_check.py      # mp/bp ranges
│   │   │   └── unit_conversion_arithmetic.py
│   │   └── evals/files/                  # mp/bp fixture CSVs (v2.0 schema)
│   └── redox/                            # second supported data type
│       ├── OVERLAY.md                    # SINGLE file (same structure)
│       ├── REFERENCE_ELECTRODES.md       # electrode-offset data table
│       ├── scripts/
│       │   ├── voltage_range_check.py
│       │   ├── conversion_arithmetic.py
│       │   └── validate_smiles.py
│       └── evals/files/
└── evals/
    ├── evals.json                        # generic + per-overlay evals
    ├── check_no_stereo_false_positives.py
    ├── check_conversion_arithmetic_lint.py  # new in v2.0
    └── files/                            # generic (cross-overlay) fixtures
```

## Quick test

Verify the scripts work against the bundled fixtures:

```bash
# Clean fixture for mp_bp: zero flags expected
python3 scripts/run_all_checks.py --datatype mp_bp \
    datatypes/mp_bp/evals/files/clean_baseline.csv
echo "exit=$?"   # → 0

# Seeded-error fixture: every deliberate error should be flagged
python3 scripts/run_all_checks.py --datatype mp_bp \
    datatypes/mp_bp/evals/files/seeded_errors.csv
echo "exit=$?"   # → 1

# Generic conversion-arithmetic-syntax unit tests
python3 evals/check_conversion_arithmetic_lint.py
echo "exit=$?"   # → 0
```

## Architectural philosophy

This skill follows the `redox-extraction` model: **thin scripts, fat prompts**.

- The Claude agent reads the actual paper file(s) and writes rows with a
  verbatim `evidence_quote`. The agent does the semantic work (identifying
  the compound, value, units, data type).
- The scripts only do deterministic checks an LLM can't do reliably:
  arithmetic verification, range plausibility, SMILES validity, DOI
  substring presence, duplicate detection, CSV quoting.
- An **independent verifier agent** (fresh context, no extractor notes)
  re-reads the source and confirms every row's evidence quote.

v2.0 modularization moved ~30 % of the v1.7 skill — the property-specific
value ranges, unit-conversion math, property enum, and property-specific
failure patterns — into a `datatypes/<X>/` overlay so adding a new property
family doesn't require rewriting the generic protocol.

## Schema

A single CSV with 18 columns. The v2.0 generic schema applies across every
data type; the overlay declares the property enum, the standardized unit
string for `units`, and any extension columns.

| Column | Notes |
|---|---|
| `id` | Sequential integer |
| `verification_status` | `pending_verification`, `verified_extraction`, `verified_textbook`, `flagged_review`, etc. |
| `compound_name` | Full IUPAC / common / trivial name; never truncated |
| `compound_smiles` | Optional; validated by RDKit when populated |
| `property` | One of the values declared in the overlay's `SCHEMA.md` |
| `value` | Numeric value in the property's standardized unit (or categorical string) |
| `value_min`, `value_max` | When value is a range |
| `value_raw` | As printed in source, with units |
| `units` | The unit of `value` (e.g., `°C`, `V vs SHE`). Empty for categorical. |
| `relation` | `=`, `>`, `<`, `~`, `≈` |
| `meas_calc` | `measured` or `calculated` (renamed from v1.7's `data_type`) |
| `source`, `source_url` | Citation; no author names; DOI in URL |
| `evidence_location` | Precise pointer (e.g., "Table 1 row 3") |
| `evidence_quote` | **MANDATORY** verbatim text from source |
| `conversion_arithmetic` | Math when conversion applied; v2.0 standardized syntax |
| `notes` | Optional |

See `SKILL.md` for the full schema, empty-when-not-applicable conventions,
and conversion-arithmetic syntax. Plus the overlay's `SCHEMA.md` for the
property enum and any extension columns.

## When to apply

Apply this skill when:

- Building a property database from a corpus of provided papers (mp/bp,
  redox, …).
- Extending an existing property database with new papers.
- Auditing an existing extraction for errors.

Do **not** apply this skill for one-off conversational questions
("what's the boiling point of methanol?") — that's overkill.

This skill **does not fetch papers**. The user provides them as
subdirectories on disk. If you also need to find / fetch papers from
the literature, use a separate paper-discovery skill first, then apply
this one.

## How to add a new data type

Concrete recipe for adding (say) `viscosity`:

1. Copy `datatypes/mp_bp/` to `datatypes/viscosity/`.
2. Rewrite the single `OVERLAY.md` file. It has eight sections:
   - **Properties extracted** + a property-disambiguation table for
     borderline cases.
   - **Schema** — extension columns (e.g., `temperature_celsius` for
     viscosity), standardized unit (`Pa·s` etc.).
   - **Worked examples** — 3-4 rows showing edge cases.
   - **Value ranges** — per-property plausibility bounds.
   - **Unit conversions** — non-standard-unit → standard-unit math
     in the v2.1 standardized syntax.
   - **Skip reasons specific to this property** (additions to
     `SKILL.md`'s generic vocabulary, NOT replacements).
   - **Candidate-token list** — tokens the agent should scan for in
     Phase 1.
   - **Per-row drop patterns** — failure patterns specific to this
     property family.
   - **Property-specific anti-patterns** — concrete examples to avoid.
   - **Failure modes observed in past trials** — accumulated as you run trials.
3. Replace the overlay scripts in `datatypes/viscosity/scripts/`:
   - `value_range_check.py` with viscosity-appropriate ranges.
   - Any conversion-arithmetic script if your property has alternate units.
4. Add evals to `evals/evals.json` with `datatype: "viscosity"`; put
   fixtures under `datatypes/viscosity/evals/files/`.
5. Run `python3 scripts/run_all_checks.py --datatype viscosity <test.csv>`
   to confirm the umbrella picks up your overlay.

The generic skill machinery (Phases 0, 1, 3, 4, 5, 6; the audit framework;
the verifier prompt; the property-agnostic failure-mode catalog in
`references/COMMON_ERRORS.md`) all works unchanged for the new data type.

**One overlay file, not three.** v2.0 split each overlay across three
files (`OVERLAY.md`, `SCHEMA.md`, `COMMON_ERRORS.md`); v2.1 collapsed them.
The single-file pattern reduces the cross-reference burden on the agent
distilling the skill into a working prompt — Trial-7 showed the 3-file
split was a meaningful contributor to extraction-quality regression.

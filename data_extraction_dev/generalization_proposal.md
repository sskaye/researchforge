# Modularizing the extraction skill for multiple data types

A proposal for generalizing the current `mp-bp-extraction` skill so it can be applied to other measurement data types (redox potentials, thermal conductivity, viscosity, etc.) while preserving the v1.4–v1.7 hardening work.

---

## 1. Current skill — what's in it

The shipped `mp-bp-extraction` skill (v1.7) is a 22-file package (excluding `dist/` artifacts):

```
mp-bp-extraction/
├── SKILL.md                              # protocol (305 lines)
├── README.md                             # how to install + apply
├── references/
│   ├── EXTRACTION_PROMPT_TEMPLATES.md    # copy-paste agent prompts (3 templates)
│   ├── VERIFICATION_PROMPT_TEMPLATES.md  # Q1–Q5 audit protocol
│   └── COMMON_ERRORS.md                  # anti-pattern catalog (entries A–N)
├── scripts/                              # 11 deterministic checks (one a deprecated stub) + 1 umbrella runner
│   ├── crossref_lookup.py
│   ├── csv_quote_lint.py
│   ├── dedup_within_paper.py
│   ├── quote_support_lint.py
│   ├── quote_template_lint.py            # deprecated no-op stub
│   ├── run_all_checks.py                 # umbrella
│   ├── unit_conversion_arithmetic.py
│   ├── validate_compound_name.py
│   ├── value_range_check.py
│   ├── verify_doi.py
│   ├── verify_evidence_quote.py
│   └── verify_row.py
└── evals/
    ├── evals.json                        # 16 deterministic evals
    └── files/                            # 4 fixture CSVs
        ├── clean_baseline.csv
        ├── seeded_errors.csv
        ├── v15_seeded_errors.csv
        └── malformed_csv_quoting.csv
```

The protocol is organized into 7 phases (Phase 0 corpus manifest, Phases 1–6 from the original design). The v1.7 schema is a single CSV with 17 mp/bp-specific columns (including `value_celsius` / `value_celsius_min` / `value_celsius_max`). The audit framework lives in `audit_criteria.md` at the project root, NOT in the skill (it's maintainer-facing).

### What the v1.4 → v1.7 hardening added

Each version added "context shapes the result" defenses, all of which are property-agnostic:

| Version | Defense | What it prevents |
| --- | --- | --- |
| v1.4 | MANDATORY-READING block + anti-regex anti-pattern + Phase 4 enforcement | Cross-harness agents writing regex extractors instead of reading papers |
| v1.5 | DOI-from-file-only rule; expanded compound-name shape lint; anti-data-entry-script rule | Memory-guessed DOIs; templated quotes; truncated compound names |
| v1.6 | EA-prefix / leading-code-prefix / procedure-text-at-start lints; downgraded quote-fidelity rules to advisory | New compound-name contamination patterns; over-conservatism on borderline rows |
| v1.7 | Phase 0 corpus manifest; `_skipped.txt` requirement; past-trials anti-pattern; sandbox guidance | Silent corpus omission; cross-trial contamination |

None of these depend on the property being mp/bp. All would apply equally to redox-potential extraction, thermal-conductivity extraction, etc.

### Six trials of evidence

| Trial | Source | Rows | Tier-1 Correctness | Tier-2 Verifiability |
| --- | --- | --- | --- | --- |
| T2 (v1.4) | 168 journal papers | 1,864 | 98.7 % | 91.3 % |
| T3 (v1.5) | 168 journal papers | 1,352 | 97.0 % | 97.0 % |
| T4 (v1.6) | 168 journal papers | 1,529 | 98.0 % | 95.7 % |
| T5 (v1.7) | 168 journal papers | 2,063 | 99.7 % | 99.7 % |
| T6 (v1.7) | CRC HCP textbook | 15,741 | 99.3 % | 99.7 % |

Tier-1 = compound + value + source correctness; Tier-2 = evidence quote supports the row. See `audit_criteria.md` for the full three-tier framework. The skill is stable at \~99 % correctness; the hardening work is done.

---

## 2. What's data-type-specific vs generic

I went line-by-line through both the current `mp-bp-extraction` and the `redox-extraction` reference at `_archive/example_skill_redox/redox-extraction/`. Here's the breakdown.

### Always generic (\~70% of the skill content)

These pieces are property-agnostic and would not change for any data type. They're the load-bearing portion of the skill that produced the T5/T6 audit numbers.

**`SKILL.md` — generic sections (keep verbatim):**

- The MANDATORY READING block (agent reads papers directly, not via regex)
- The pre-flight checklist
- Phase 0 (corpus manifest + `_skipped.txt`)
- Phase 1 step 2 (DOI-from-file-only rule)
- Phase 1 step 3 (CrossRef verification when DOI present)
- Phase 2 quote re-confirmation (steps 1–6 are property-agnostic; only the `value_raw` token to search for differs)
- Phase 3 umbrella structure (run_all_checks.py)
- Phase 4 independent verification (the Q1–Q5 framework)
- Phase 5 confidence tagging (the `verification_status` enum)
- Phase 6 failure handling (paper-unreadable, DOI-mismatch, etc.)
- All anti-patterns except "I'll extract this NMR shift, it looks like an mp value" (data-type-specific)
- The "Past trial outputs are reference, not protocol" anti-pattern

**Scripts — generic in v2.0 (11 in total: 10 inherited from v1.7, all property-agnostic, plus one new):**

- `crossref_lookup.py` — DOI metadata, any chemistry property
- `verify_doi.py` — DOI substring presence in paper file
- `verify_evidence_quote.py` — verbatim quote check in paper text
- `dedup_within_paper.py` — duplicate (compound, property, value) within one paper
- `csv_quote_lint.py` — RFC-4180 quoting; column-shift detection
- `quote_support_lint.py` — <!-- fmc:1 -->quote contains numeric value<!-- /fmc:1 --> (no-op for categorical-valued properties)
- `quote_template_lint.py` — deprecated stub (kept for back-compat)
- `validate_compound_name.py` — generic compound-name shape lint (rules tuned for organic-chemistry naming, including leading-number locants like `1,4-benzenedicarboxylic acid`). Data-type-specific failure modes live in the overlay's `COMMON_ERRORS.md` — both compound-name shape errors (e.g., EA-prefix contamination in mp/bp tables) and value/property contamination (e.g., NMR shifts being captured as mp values).
- `conversion_arithmetic_lint.py` (new in v2.0) — verifies the standardized `conversion_arithmetic` syntax shape
- `verify_row.py` — single-row check bundle
- `run_all_checks.py` — umbrella runner

**References — generic:**

- `EXTRACTION_PROMPT_TEMPLATES.md` Template 1 outer structure (Steps 0–8)
- `VERIFICATION_PROMPT_TEMPLATES.md` Q1–Q5 protocol (Q1(b) and Q2 customize per data type; Q3, Q4, Q5 are generic)
- `COMMON_ERRORS.md` failure-pattern format and the cross-cutting entries (K, L, M, N about cross-harness, cross-trial, etc.)

**Schema columns — always present (generic core, 18 columns):**

All data types share the same column set, populated with property-appropriate values. This is the v2.0 proposed schema. It is broader than the v1.7 mp/bp schema (which baked the unit into the column name as `value_celsius`, `value_celsius_min`, `value_celsius_max`); v2.0 splits those into a generic `value` / `value_min` / `value_max` plus an explicit `units` column. The v1.7 `data_type` column is renamed to `meas_calc` in v2.0 to avoid clashing with "data type" used everywhere else in the proposal to mean the property family (mp_bp, redox, ...).

| Column | Generic meaning |
|---|---|
| `id` | Sequential row id |
| `verification_status` | Per the schema's enum (`pending_verification`, `verified_extraction`, `verified_textbook`, `flagged_review`, etc.) |
| `compound_name` | Compound the row is about. Standardized across data types so future joins across property families are possible. |
| `compound_smiles` | SMILES when the source provides one. Empty when not provided. |
| `property` | The specific property recorded (e.g., `melting_point`, `boiling_point`, `redox_potential`, `viscosity`). Each data-type overlay defines its enum. |
| `value` | The value in the property's standardized unit. Usually numeric; may be a categorical string for non-numeric properties (e.g., state-of-matter "solid"). Nothing in the generic schema or generic scripts blocks non-numeric strings; the first non-numeric data type to ship will define any additional handling in its overlay. |
| `value_min`, `value_max` | When the source reports a range. Empty for single values. |
| `value_raw` | As printed in the source, including original units. |
| `units` | The unit of `value` (e.g., `°C`, `V vs SHE`, `Pa·s`). Empty for categorical properties. |
| `relation` | `=`, `>`, `<`, `~`, `≈`. |
| `meas_calc` | `measured` or `calculated`. (Renamed from v1.7's `data_type`.) |
| `source` | Citation (journal + year + vol + page, or textbook + edition, or PMC subdirectory). |
| `source_url` | DOI URL, PMC/PMID, textbook, etc. |
| `evidence_location` | Pointer into the source. |
| `evidence_quote` | Verbatim text supporting the row. |
| `conversion_arithmetic` | Math when unit conversion was applied. Standardized syntax in v2.0: `<input_value_with_units> <operator> <constant> = <output_value_with_units>` (e.g., `300 K − 273.15 = 26.85 °C`). Empty when no conversion was needed. |
| `notes` | Free text. |

**Empty-when-not-applicable conventions** (v2.0): `compound_smiles` empty when the source has no SMILES; `value_min` / `value_max` empty for single values; `units` empty for categorical properties; `conversion_arithmetic` empty when no conversion was applied; `notes` empty by default. All other generic columns are required to be populated. Each overlay can declare its own empty-allowed conventions for its extension columns.

### Data-type-specific (\~30% of content)

These pieces are tied to the specific property being extracted. They're where the skill needs to differ per data type.

**Schema columns — data-type extensions (optional, declared in each overlay's `SCHEMA.md`):**

Most data types fit the generic schema with no extensions. Some properties need additional measurement-context columns:

| Data type | Required extension columns | Optional extension columns | Notes |
|---|---|---|---|
| mp/bp | (none) | (none) | mp and bp are property values (the `property` column), not separate data types. Both share schema, units (°C), and conversion math. |
| redox | `reference_electrode` | `solvent`, `ph`, `n_electrons` | Reference electrode is mandatory. Solvent and pH should be populated when present in the source; can be empty (e.g., gas-phase). |
| (future) viscosity | `temperature_celsius` | (none) | Viscosity values are meaningless without the temperature at which they were measured, so temperature is required for any viscosity row. |

The overlay's `SCHEMA.md` declares which extension columns the data type uses, which are required, and what the `property` enum is.

**Scripts — property-specific:**

| Concern | mp/bp script | redox script | What changes |
| --- | --- | --- | --- |
| Plausible value range | `value_range_check.py` (mp ∈ \[−275, 4500\] °C; bp ∈ \[−275, 6500\] °C) | `voltage_range_check.py` (per-chemical-class voltage windows) | Property family + ranges |
| Unit conversion math | `unit_conversion_arithmetic.py` (K/°F → °C) | `conversion_arithmetic.py` (reference-electrode offsets) | Conversion logic |

`validate_compound_name.py` (formerly mp/bp-specific) is generic in v2.0 — see generic-scripts list above. Property-specific shape errors (EA-prefix contamination, NMR-as-mp, methyl-viologen-couple-ambiguity) live in the overlay's `COMMON_ERRORS.md`. The redox overlay additionally ships `validate_smiles.py` for SMILES-string shape checking, which is a separate concern from compound-name validation.

**References — property-specific:**

| Doc | mp/bp | redox | What it contains |
| --- | --- | --- | --- |
| Property-specific reference table | (none needed — temperature is universal) | `REFERENCE_ELECTRODES.md` (SHE conversion table) | Domain-specific constants |
| Common errors — property-specific | EA-prefix contamination; NMR shifts as mp; workup solvents as compounds; PDF sign-loss for −77 °C | SCE-as-SHE errors; methyl viologen V²⁺/V⁺• vs V⁺•/V⁰; aprotic-vs-aqueous conflation; Ag/AgCl electrolyte ambiguity | Failure-mode catalog has both generic and property-specific entries |

**Extraction prompt — property-specific bits:**

- The valid `property` enum values (mp/bp lists `melting_point`, `boiling_point`, `DSC_onset`, etc.; redox lists `redox_potential`, `formal_potential`, etc.)
- The "drop these aggressively" list (mp/bp: NMR shifts, workup solvents; redox: SCE-without-conversion, ambiguous reference electrodes)
- The unit-conversion examples
- Required vs optional extension columns
- The example row (one fully populated example per data type)

**Verification prompt — property-specific bits:**

- Q1(b) "value matches paper's printed value" — the unit and conversion logic differs
- The granular `flagged_*` reasons specific to the property (mp/bp has `flagged_value_out_of_range`; redox has `flagged_reference_electrode_mismatch`)

---

## 3. Proposed modular structure

I'm going with the approach you suggested — data-type-specific subfolders in `references/`, `scripts/`, and `evals/` — with a small refinement: <!-- fmc:9 -->each data type gets its own folder under each, with a per-data-type<!-- /fmc:9 --> `OVERLAY.md` document that the agent reads to learn what's different from the generic protocol.

### Proposed layout

```
data-extraction/                         # renamed from mp-bp-extraction
│
├── SKILL.md                             # generic protocol (with placeholders pointing at datatype overlays)
├── README.md
│
├── references/
│   ├── EXTRACTION_PROMPT_TEMPLATES.md   # generic Template 1, with explicit "see datatypes/<X>/OVERLAY.md" markers
│   ├── VERIFICATION_PROMPT_TEMPLATES.md # generic Q1–Q5, with markers for datatype-specific Q1/Q4
│   └── COMMON_ERRORS.md                 # generic-only entries (cross-trial contamination, cross-harness regex, etc.)
│
├── scripts/                             # generic scripts (run on every datatype)
│   ├── crossref_lookup.py
│   ├── verify_doi.py
│   ├── verify_evidence_quote.py
│   ├── dedup_within_paper.py
│   ├── csv_quote_lint.py
│   ├── quote_support_lint.py
│   ├── quote_template_lint.py           # deprecated stub
│   ├── validate_compound_name.py        # generic compound-name shape lint
│   ├── conversion_arithmetic_lint.py    # new in v2.0: verifies syntax shape
│   ├── verify_row.py
│   └── run_all_checks.py                # discovers datatypes/<X>/scripts/ at runtime
│
├── datatypes/
│   ├── mp_bp/                           # the current production data type
│   │   ├── OVERLAY.md                   # what the agent reads to learn mp/bp specifics
│   │   ├── SCHEMA.md                    # extension columns (none), property enum, worked example row
│   │   ├── COMMON_ERRORS.md             # mp/bp-specific failures (EA-prefix, NMR-as-mp, etc.)
│   │   ├── scripts/
│   │   │   ├── value_range_check.py             # mp/bp ranges
│   │   │   └── unit_conversion_arithmetic.py    # K/°F → °C
│   │   └── evals/
│   │       └── files/                           # mirrors v1.7 layout
│   │           ├── clean_baseline.csv
│   │           ├── seeded_errors.csv
│   │           ├── v15_seeded_errors.csv
│   │           └── malformed_csv_quoting.csv
│   │
│   └── redox/                           # second data type (built from the archived redox-extraction skill)
│       ├── OVERLAY.md
│       ├── SCHEMA.md
│       ├── COMMON_ERRORS.md
│       ├── REFERENCE_ELECTRODES.md
│       ├── scripts/
│       │   ├── voltage_range_check.py
│       │   ├── conversion_arithmetic.py         # reference-electrode offsets
│       │   └── validate_smiles.py
│       └── evals/
│           └── files/
│               └── clean_baseline.csv
│
├── evals/
│   ├── evals.json                       # generic + per-datatype eval entries
│   └── files/                           # generic (cross-datatype) fixtures
│
└── dist/
    └── data-extraction.skill            # packaged artifact (still single zip)
```

### How the agent invokes a specific data type

When the user applies the skill, they specify a data type:

> "Extract <!-- fmc:10 -->melting-point and boiling-point<!-- /fmc:10 --> data from the papers in `corpora/full_168/`."

The agent reads `SKILL.md`, follows the generic protocol, and at the appropriate points reads:

- `datatypes/mp_bp/OVERLAY.md` — overview of what's specific to mp/bp.
- `datatypes/mp_bp/SCHEMA.md` — the column definitions and worked example row.
- `datatypes/mp_bp/COMMON_ERRORS.md` — failure modes specific to mp/bp extraction.

If the user asks for a data type that doesn't have a folder yet, the agent halts and asks the user to either pick from the available data types or write a new overlay first. This is a hard rule — no inference from corpus content, no falling back to a "generic" extraction without an overlay.

If the user asks for a subset of a data type's properties (e.g., "extract only boiling points", not melting points), the agent uses the mp/bp overlay but restricts its emitted rows to that property value. The overlay defines what's available; the user's instruction filters which to emit.

### Agent Skills standard compliance

The proposed `datatypes/<X>/scripts/` subfolders go one level deeper than the current Anthropic Agent Skills convention (which places `scripts/` flat at the skill root). I'm not aware of a hard restriction in the published skill format, and the skill is loaded by reading `SKILL.md` and any files it references — so nested subfolders should work. But this is worth verifying against the actual harness we use before commit. Two safety options:

- **Verify by installing the v2.0 package in the target harness** (Claude Code / Cowork) and confirming it loads and that nested scripts are accessible.
- **Fall back to flat layout if the harness complains**: instead of `datatypes/mp_bp/scripts/value_range_check.py`, use a naming convention like `scripts/mp_bp__value_range_check.py` with `__` as the data-type separator. Same modularity, no nesting.

I'd default to the nested layout and validate during step 6 of the migration (where the v1.7 evals are re-run against the new structure).

### What `SKILL.md` looks like in the modular version

The skill prose is almost unchanged. The only differences are:

1. **Identify the data type at the start**.The MANDATORY READING block gains a line: *"Identify which data type you are extracting (e.g.,* `mp_bp`*,* `redox`*). Read* `datatypes/<datatype>/OVERLAY.md` *for the property-specific schema, anti-patterns, value ranges, and example row before starting Phase 0."*

2. **Schema is generic; overlay declares extensions.** The schema section in `SKILL.md` documents the full 18-column generic core inline (`id`, `verification_status`, `compound_name`, `compound_smiles`, `property`, `value`, `value_min`, `value_max`, `value_raw`, `units`, `relation`, `meas_calc`, `source`, `source_url`, `evidence_location`, `evidence_quote`, `conversion_arithmetic`, `notes`) along with the empty-when-not-applicable conventions and the standardized `conversion_arithmetic` syntax. The overlay's `SCHEMA.md` only declares (a) the valid `property` enum, (b) the property's standardized unit string for the `units` column, (c) any required and optional extension columns, and (d) a worked example row.

3. **Phase 3 reads from datatypes/X/scripts/.**`run_all_checks.py` is updated to accept `--datatype <name>` and automatically include `datatypes/<name>/scripts/*.py` in the umbrella run (after the generic scripts).

4. **Anti-patterns section is split.** Generic anti-patterns (no regex extractor, no data-entry scripts, no memory-based DOI, past trials = reference) stay in `SKILL.md`. Data-type-specific anti-patterns (NMR shifts as mp; SCE-as-SHE conversion errors) move to `datatypes/<X>/COMMON_ERRORS.md`.

### What an `OVERLAY.md` looks like

A short, intent-level document the agent reads first. <!-- fmc:11 -->Concretely for mp/bp<!-- /fmc:11 -->:

```markdown
# Data type: melting-point and boiling-point (mp/bp)

This overlay tells you what's specific to mp/bp extraction. Use it alongside SKILL.md
and the generic schema documented there.

## Properties extracted

This overlay covers six property values (set in the row's `property` column):

- `melting_point`
- `boiling_point`
- `DSC_onset`
- `DSC_peak`
- `decomposition`
- `sublimation`

melting_point and boiling_point are distinct properties (not subtypes of one
"thermal transition" property). The other four are closely related thermal events.

If the user asks you to extract only one of these (e.g., "only melting points"),
restrict the rows you emit to that property value. The skill, scripts, and audit
framework all work the same — only which rows you emit differs.

## Schema

No data-type extension columns. mp/bp rows use the generic schema exactly:
- `compound_name` for the compound identity
- `property` set to one of the six values above
- `value` in °C; `value_min` / `value_max` when the source reports a range
- `value_raw` as printed in the source
- `units` is always "°C"
- `conversion_arithmetic` populated when the source's value was in K or °F

## Value ranges

- mp / DSC_onset / DSC_peak: [−275, 4500] °C (helium through highest-melting carbides)
- bp: [−275, 6500] °C (helium through rhenium)
- decomposition / sublimation: full range

Enforced by `datatypes/mp_bp/scripts/value_range_check.py`.

## Unit conversions

Conversion expressions are written into the generic `conversion_arithmetic` column using v2.0's standardized syntax (see SKILL.md). For mp/bp:

- K → °C: `<X> K − 273.15 = <Y> °C`
- °F → °C: `(<X> °F − 32) × 5/9 = <Y> °C`

Numeric correctness enforced by `datatypes/mp_bp/scripts/unit_conversion_arithmetic.py`.

## Data-type-specific anti-patterns

See `COMMON_ERRORS.md` for full catalog. Critical ones:
- NMR chemical shifts (`δ 130.31`) mistaken for mp values
- Workup solvents (CH2Cl2, EtOAc, MeOH) extracted as the compound
- EA-prefix contamination in compound_name (`"C, 50.73; H, 5.72; N, 8.42. (IUPAC name)"`)
- PDF sign-loss: `−77.9 °C` rendered as `277.9 °C`

## Worked example row

(One fully-populated mp/bp row showing every column correctly filled.)
```

For redox the same overlay would describe the reference-electrode and solvent context, the multi-couple-per-molecule rule, and so on.

### What changes in the scripts

Surprisingly little.

`run_all_checks.py` gains a required `--datatype <name>` flag. When provided, it:

1. Runs every generic script in `scripts/`.
2. Additionally discovers and runs `datatypes/<name>/scripts/*.py`.
3. Discovery is just `glob`; no special manifest needed.

When `--datatype` is **not** provided, `run_all_checks.py` halts with an error message listing the available data types (`mp_bp`, `redox`, ...). This matches the user-must-specify-data-type rule from Section 5 — there is no implicit "generic only" mode.

`verify_row.py` gains the same flag with the same halt-on-missing behavior.

**The data-type-specific scripts** for mp/bp (`value_range_check.py`, `unit_conversion_arithmetic.py`) physically move into `datatypes/mp_bp/scripts/`. Their content is unchanged; just relocated. `validate_compound_name.py` stays in the generic top-level `scripts/` (it operates on the generic `compound_name` column and applies to any data type with chemical compounds — see Section 2).

**No generic script needs to know about specific data types.** Generic scripts work on the generic columns; data-type-specific scripts work on extension columns and on data-type-specific ranges or conversions.

### Conversion-arithmetic syntax (standardized in v2.0)

`conversion_arithmetic` follows a single format across every data type:

```
<input_value_with_units> <operator> <constant_with_units_if_any> = <output_value_with_units>
```

Examples:

- mp/bp Kelvin → Celsius: `300 K − 273.15 = 26.85 °C`
- mp/bp Fahrenheit → Celsius: `(300 °F − 32) × 5/9 = 148.89 °C`
- redox SCE → SHE: `+0.40 V vs SCE + 0.241 = +0.641 V vs SHE`

The column is empty when no conversion was applied. A new generic lint, `conversion_arithmetic_lint.py`, verifies the syntax shape (input + operator + constant + `=` + output; units present where the column-table convention requires them). Added to the generic `scripts/` in migration Step 4.

### What changes in the extraction prompts

Template 1 in `references/EXTRACTION_PROMPT_TEMPLATES.md` keeps its outer structure but the per-step "specifics" sections move out:

- Step 4 ("Extract row by row") references `datatypes/<X>/SCHEMA.md` for the column list.
- Step 5 ("Drop these aggressively") points to `datatypes/<X>/COMMON_ERRORS.md` for the property-specific drop patterns.
- The unit-conversion guidance becomes a pointer: *"See* `datatypes/<X>/OVERLAY.md` *§ Unit conversions."*

The cross-cutting steps (Step 1 read + DOI identification, Step 6 quote re-confirmation, Step 7 sanity checks, Step 7.5 multi-line name reassembly, Step 8 CSV quoting) stay generic in the main template.

### What changes in the verification prompts

`VERIFICATION_PROMPT_TEMPLATES.md` Q1–Q5 protocol stays generic. The customization happens through two pointers:

- Q1(b) "value matches paper's printed value" — references `datatypes/<X>/SCHEMA.md` for what counts as "the value".
- Q2 "property type correct" — references `datatypes/<X>/OVERLAY.md` for the property enum and how to distinguish subtypes.

The verifier still emits the same JSON output schema (`verdict`, `reason`, `details`, `verifiable`, `verifiability_tag`).

---

## <!-- fmc:14 -->4. Migration plan<!-- /fmc:14 -->

Concrete steps to convert the current skill to the modular form. Each step is independently testable. The first step preserves the existing skill: I'll copy `mp-bp-extraction/` to a new `data-extraction/` folder and make all edits there, leaving the v1.7 production skill untouched as a fallback.

**Step 1 — Copy `mp-bp-extraction/` to `data-extraction/`.** Verbatim copy, no edits. The v1.7 `mp-bp-extraction/` stays as-is in the repo as the historical reference and the still-installable production skill until the modular `data-extraction/` skill is validated. All subsequent steps happen inside `data-extraction/`.

*Test:* `diff -r mp-bp-extraction/ data-extraction/` empty (modulo `.DS_Store`); all files have matching md5 checksums.

**Step 2 — Audit current files for generic vs data-type-specific content** inside `data-extraction/`. For each file in the current skill, classify every section as generic / mp-bp-specific / both. Most of the work is identifying which paragraphs of `SKILL.md`, `EXTRACTION_PROMPT_TEMPLATES.md`, etc. need to be split.

*Test:* a classification document exists (e.g., `_audit_notes.md`) covering every file in the skill, with each major section labeled. No silent omissions.

**Step 3 — <!-- fmc:13 -->Create the<!-- /fmc:13 -->** `datatypes/mp_bp/` **folder** inside `data-extraction/`. mp and bp share schema, units, unit-conversion math, and most anti-patterns, so they live together in one overlay (they're different `property` values within the same overlay's enum). Move:

- `references/COMMON_ERRORS.md` mp/bp-specific entries → `datatypes/mp_bp/COMMON_ERRORS.md`
- `scripts/value_range_check.py` → `datatypes/mp_bp/scripts/value_range_check.py`
- `scripts/unit_conversion_arithmetic.py` → `datatypes/mp_bp/scripts/unit_conversion_arithmetic.py`
- `evals/files/*.csv` (the mp/bp fixtures) → `datatypes/mp_bp/evals/files/`
- Tag each entry in the top-level `evals/evals.json` with a `datatype` key (or `generic`). The file stays in one place; the tag lets `run_all_checks.py` and the eval runner filter by data type. Update fixture-path references to point at the new `datatypes/mp_bp/evals/files/` locations.

`scripts/validate_compound_name.py` stays in the generic top-level `scripts/` (it's now generic — see Section 2). The migration here is just deleting any mp/bp-specific shape rules from it and moving those to `datatypes/mp_bp/COMMON_ERRORS.md`. Make sure the generic rules allow leading-number locants in IUPAC names (`1,4-benzenedicarboxylic acid`, `2,2'-bipyridine`, `4-aminobenzoic acid`).

Write the new files:

- `datatypes/mp_bp/OVERLAY.md` — the short overview document above.
- `datatypes/mp_bp/SCHEMA.md` — extension columns (none), property enum, units string (`°C`), worked-example row.

*Test:* moved scripts match their originals by md5 checksum; removed files no longer exist at their old paths; `OVERLAY.md` and `SCHEMA.md` exist and are non-empty; `evals.json` carries a `datatype` key on every entry and mp/bp entries point at `datatypes/mp_bp/evals/files/...`.

**Step 4 — Update generic files in `data-extraction/`.**

- `SKILL.md`: replace property-specific paragraphs with overlay pointers. Document the full 18-column generic core schema inline (with `meas_calc` renamed from v1.7's `data_type`), the empty-when-not-applicable conventions, and the standardized `conversion_arithmetic` syntax. Add the "Identify your data type" instruction to the MANDATORY READING block. Add the "halt if the user asks for a property type with no overlay" rule.
- `README.md`: rewrite to document v2.0 usage — how to specify a data type when invoking the skill, the halt rule, the modular layout, and how to add a new data type. The v1.7 README assumed a single mp/bp purpose and will not survive a light edit.
- `references/EXTRACTION_PROMPT_TEMPLATES.md`: replace property-specific steps with overlay pointers (`datatypes/<X>/OVERLAY.md`, `datatypes/<X>/SCHEMA.md`, `datatypes/<X>/COMMON_ERRORS.md`).
- `references/VERIFICATION_PROMPT_TEMPLATES.md`: parameterize Q1(b) and Q2 with overlay pointers.
- `references/COMMON_ERRORS.md`: keep only generic entries (cross-harness regex, cross-trial contamination, etc.). Remove EA-prefix and NMR-as-mp entries (they live in the overlay).
- `scripts/run_all_checks.py`: add required `--datatype <name>` flag; auto-discover `datatypes/<name>/scripts/*.py`; halt with available-data-types list when flag is missing.
- `scripts/verify_row.py`: same `--datatype` flag with the same halt-on-missing behavior.
- `scripts/validate_compound_name.py`: strip mp/bp-specific shape rules; ensure leading-number-locant compound names pass.
- `scripts/conversion_arithmetic_lint.py` (new): verify the v2.0 standardized `conversion_arithmetic` syntax (input + operator + constant + `=` + output).

*Tests:*

- `SKILL.md` contains the 18-column generic schema inline, the "identify your data type" instruction in MANDATORY READING, and the halt-on-missing-overlay rule.
- `run_all_checks.py` invoked without `--datatype` exits non-zero with an available-data-types list; invoked with `--datatype mp_bp` exits zero and runs both generic and mp_bp scripts.
- `verify_row.py` has the same halt-on-missing behavior.
- `validate_compound_name.py` passes a small fixture of leading-number-locant names (`1,4-benzenedicarboxylic acid`, `2,2'-bipyridine`, `4-aminobenzoic acid`); no longer flags the EA-prefix shapes (those moved to the overlay).
- `conversion_arithmetic_lint.py` ships with unit tests covering the three valid example shapes from Section 3 and at least four invalid shapes (missing `=`, missing input units, swapped operator/constant, extra trailing text).
- `references/COMMON_ERRORS.md`: grep finds no remaining mp/bp-specific entries.

**Step 5 — Update `audit_criteria.md` at the project root.** It stays outside the skill package, but the wording is currently mp/bp-flavored in places. Rewrite to be data-type-agnostic (replace "mp/bp" with "the data type"; replace mp/bp-specific examples in Q1(b) / Q2 with placeholder references to the overlay).

*Test:* grep for `mp`, `bp`, `melting`, `boiling`, `Celsius` — any matches must be inside clearly-marked example blocks, never in normative protocol wording.

**Step 6 — Verify the v1.7 evals under the new structure.** Run the existing eval suite. Two categories of failures are expected and need to be reconciled rather than treated as bugs:

- **Path-only failures** (most of the 16): each eval references its fixture by path, now `datatypes/mp_bp/evals/files/*.csv`. Fix by updating the fixture path in `evals.json`.
- **Behavior-change failures from Step 3**: any eval that asserts mp/bp-specific behavior in `validate_compound_name.py` (e.g., EA-prefix detection) will fail because those rules moved to the overlay's `COMMON_ERRORS.md`. Port the assertion into an overlay-level eval under `datatypes/mp_bp/evals/`.

Any failure outside these two categories is a real coupling bug to fix.

**Step 7 — One-time migration of the existing Trial-5 and Trial-6 CSVs to the v2.0 schema.** Write a small `migrate_v17_to_v20.py` script. This is a one-off migration utility, not part of the shipped skill — it lives at the project root (alongside `audit_criteria.md`), not inside `data-extraction/scripts/`. The script:

- Renames `value_celsius` → `value`, `value_celsius_min` → `value_min`, `value_celsius_max` → `value_max`.
- Inserts a new `units` column populated with `°C` (since the v1.7 schema implied this).
- Renames `data_type` → `meas_calc`.
- Leaves all other columns unchanged.

Apply to `trials/trial5/opus47/opus47_mp_bp.csv` and `trials/trial6/opus47/mp_bp_data.csv`. Save migrated copies alongside the originals (e.g., `*_v20.csv`) so the v1.7-format originals remain as historical record.

*Tests:*

- Output CSV header is exactly the v2.0 18 columns in the documented order.
- Row-count parity: input row count == output row count for both Trial-5 and Trial-6.
- `units` populated with `°C` on every output row.
- `meas_calc` matches the v1.7 `data_type` column row-for-row.
- Spot-check 5 randomly-selected rows: every non-renamed cell preserved exactly.

**Step 8 — Regression-test the modular skill against the migrated CSVs.** Run `python3 scripts/run_all_checks.py --datatype mp_bp trials/trial5/opus47/opus47_mp_bp_v20.csv` against the migrated Trial-5 output. Then run the same against a **uniform-random 500-row subset of the migrated Trial-6 CSV** (fixed seed for reproducibility — full-corpus regression on 15,741 rows would be slow).

Expected output: same flags from the still-equivalent checks (DOI verification, quote support, value-range, etc.). Intentional behavior diffs from this migration:

- `validate_compound_name.py` will produce fewer flags now that its mp/bp-specific rules moved to the overlay's `COMMON_ERRORS.md`. The newly-overlay rules (EA-prefix, NMR-as-mp) are not enforced by a script in v2.0; they're documented for the extracting agent and verifier.
- `conversion_arithmetic_lint.py` is new in v2.0 and may surface syntax-shape issues in v1.7-format conversion strings that the v1.7 lint suite never checked.

Enumerate the diffs and confirm each falls into one of the intentional buckets above. Anything that doesn't is a regression to investigate.

**Step 9 — Update front matter + repackage.**

- Update front-matter: `name: data-extraction`.
- Rewrite the `description:` to mention the data-type-overlay structure.
- Bump version to v2.0 (breaking-API change relative to v1.7 — the schema column names and the agent-must-specify-data-type requirement are real interface changes).
- Rebuild `dist/data-extraction.skill`.

*Tests:*

- `unzip -tq dist/data-extraction.skill` passes integrity check.
- `unzip -l dist/data-extraction.skill` shows `SKILL.md`, `scripts/`, `datatypes/mp_bp/`, `datatypes/redox/` at the expected paths.
- Front-matter parses: `name: data-extraction`, `version: 2.0`.
- Install the `.skill` in the target harness (Claude Code or Cowork). It loads without errors and appears as `data-extraction` in the available-skills list.

**Step 10 — Build the `redox/` data type as proof of generality.** Take the archived `_archive/example_skill_redox/redox-extraction/` and convert its property-specific content into `datatypes/redox/`. Most of the work is reformatting:

- `references/REFERENCE_ELECTRODES.md` → `datatypes/redox/REFERENCE_ELECTRODES.md`
- `references/COMMON_ERRORS.md` (redox-specific entries) → `datatypes/redox/COMMON_ERRORS.md`
- `scripts/voltage_range_check.py` → `datatypes/redox/scripts/voltage_range_check.py`
- `scripts/conversion_arithmetic.py` → `datatypes/redox/scripts/conversion_arithmetic.py`
- `scripts/validate_smiles.py` → `datatypes/redox/scripts/validate_smiles.py`
- Write `datatypes/redox/OVERLAY.md` and `datatypes/redox/SCHEMA.md`.

(`find_open_access.py` and `cross_source_consistency.py` from the redox skill are NOT carried over — this skill is extraction-only. Source discovery and cross-source consistency are out of scope.)

*Tests:*

- `run_all_checks.py --datatype redox` against the archived redox-extraction fixtures: every generic check (DOI, quote support, dedup, etc.) plus the three redox-specific scripts (`voltage_range_check.py`, `conversion_arithmetic.py`, `validate_smiles.py`) executes without crashing.
- `run_all_checks.py --datatype redox` produces the same Tier-1/Tier-2 verdicts on those fixtures as the archived redox-extraction skill did (intentional behavior diffs from porting are enumerated and accepted, same framing as Step 8).
- Same halt-on-missing-overlay rule applies: `run_all_checks.py --datatype nonexistent` exits non-zero.

**Step 11 — Document the modular pattern.** Update `README.md` (inside the skill) with a "How to add a new data type" section: copy the `datatypes/mp_bp/` folder, rewrite `OVERLAY.md` / `SCHEMA.md` / `COMMON_ERRORS.md` for the new property, write new property-specific scripts (range check, unit conversion if needed), add evals.

Update `CHANGELOG.md` and `development_report.md` at the project root (outside the skill, part of the development record) with the v2.0 changes: schema generalization, column renames, modular layout, halt-on-missing-overlay rule, conversion-arithmetic syntax standardization.

*Tests:*

- `README.md` contains a "How to add a new data type" section with a concrete file-by-file recipe.
- `CHANGELOG.md` at the project root has a v2.0 entry covering the schema rename, column-name changes, modular layout, halt-on-missing-overlay rule, and conversion-arithmetic syntax standardization.
- `development_report.md` at the project root has a v2.0 section.
- Following the "How to add a new data type" recipe produces a structurally-valid placeholder folder (`OVERLAY.md`, `SCHEMA.md`, `COMMON_ERRORS.md`, `scripts/`, `evals/files/` all present at the expected paths) — no need for the placeholder to do real extraction.

---

## 5. Decisions (resolved during review)

All six design questions from the first draft of this section have been resolved through your review. Recording the outcomes here so the migration plan in Section 4 is unambiguous.

### Skill name, version, packaging

- **Name:** `data-extraction`. The skill is property-agnostic at its core.
- **Version:** <!-- fmc:16 -->v2.0<!-- /fmc:16 -->. The schema column names and the agent-must-specify-data-type requirement are real interface changes relative to v1.7.
- **Packaging:** <!-- fmc:17 -->Single `.skill` zip containing all data types<!-- /fmc:17 -->. Simpler to maintain; users who only care about one property can still install the single package.

### Schema-column naming convention

<!-- fmc:18 -->Standardize on generic names.<!-- /fmc:18 --> `compound_name` everywhere (not "molecule"). The reasoning: future joins across property families (e.g., "for compounds where we have both mp and redox data, look at correlations") are valuable, and they're only possible if the compound column has the same name in every property's table. Same applies to `value`, `value_raw`, `value_min`, `value_max`, `units`, `relation`, and `property`. Data-type extensions (`reference_electrode` for redox, etc.) sit alongside the generic columns.

### Auto-discovery of data types

<!-- fmc:19 -->The user must specify the data type explicitly.<!-- /fmc:19 --> Papers commonly report multiple property types (e.g., a synthesis paper has both mp/bp and yield), so there's no reliable way to infer what the user wants. If the user requests a data type that doesn't have an overlay (no `datatypes/<X>/`), the agent **halts** and asks the user to either pick a supported data type or write a new overlay first. No fallback to "generic" extraction without an overlay.

### Cross-property datasets

<!-- fmc:20 -->Two separate CSVs, one per data type.<!-- /fmc:20 --> A user extracting both mp/bp and redox from the same corpus runs the skill twice. Joining the two CSVs on `compound_name` after the fact is straightforward (and the standardized compound-name column makes it trivial).

### Fate of `_archive/example_skill_redox/` and the current `mp-bp-extraction/`

<!-- fmc:21 -->Keep both as-is in `_archive/` (or in the case of `mp-bp-extraction/`, keep at the repo root until the new `data-extraction/` skill is validated).<!-- /fmc:21 --> They're the historical record of the v1.0–v1.7 evolution and the proof points for the migration. After v2.0 ships and is validated by a trial run, we can decide whether to formally archive `mp-bp-extraction/` too.

### Where `audit_criteria.md` lives

<!-- fmc:22 -->Stays at the project root, outside the skill package.<!-- /fmc:22 --> It's maintainer-facing. Verifier agents read `references/VERIFICATION_PROMPT_TEMPLATES.md` (inside the skill) for the Q1–Q5 protocol; the higher-level "what does an audit measure" framing lives in `audit_criteria.md` for the human maintainer.

---

## 6. What this does NOT change

To be explicit about preserving the v1.7 hardening work:

- **The seven phases** stay (Phase 0 manifest, Phase 1 source prep, Phase 2 evidence-locked extraction, Phase 3 deterministic checks, Phase 4 independent verification, Phase 5 confidence tagging, Phase 6 failure handling).
- **The three-tier audit framework** (`audit_criteria.md`) stays structurally identical. The migration in Step 5 only swaps mp/bp-flavored examples for property-agnostic placeholders; the Tier-1 / Tier-2 / Tier-3 definitions and the Q1–Q5 verifier protocol are unchanged.
- **The generic anti-patterns** (no regex extractor, no data-entry scripts, DOI-from-file-only, no script-generated row values, past trials = reference) stay in `SKILL.md` and apply to every data type.
- **The Phase 0 manifest +** `_skipped.txt` mechanism is unchanged.
- **The Q1–Q5 verification protocol** is unchanged at the framework level; only Q1(b) and Q2 customize per data type.
- **The cross-trial contamination defenses** (sandbox, past-trials anti-pattern) are unchanged.
- **The** `verified_textbook` **status tier** (used in T6) stays in the `verification_status` enum.
- **The audit numbers** from T2–T6 are preserved as-is in the trial reports.

The modularization is purely about *where files live* and *which content is generic vs property-specific*. The row-level extraction *decisions* on mp/bp corpora should be identical to v1.7 after migration. The *output CSV format* differs because of the schema rename (`value_celsius` → `value` + `units`, `data_type` → `meas_calc`), and `validate_compound_name.py` produces a narrower set of flags now that its mp/bp-specific rules have moved to the overlay's `COMMON_ERRORS.md`. Those are intentional and accounted for in the Step 7 migration script and Step 8 regression-baseline comparison.

---

## 7. Open questions for the next iteration (after modularization works)

Not blocking, but worth flagging:

- **Cross-data-type evals.** If the modular skill is invoked with the wrong data-type overlay (e.g., the user says "redox" but the corpus is mp/bp papers), what should happen? Currently nothing structural prevents this. A small sanity check at Phase 0 ("does the corpus contain text consistent with the chosen data type?") could be useful.

- **Mixing data types in one corpus.** Some papers report both mp/bp and redox. The current proposal handles this by running the skill twice (once per data type) on the same corpus. A future iteration could allow the skill to extract multiple data types in a single run, but the deliverable schemas would differ — probably one CSV per data type still.

- **Auto-generating a data-type overlay from a worked example.** If a user has a couple of fully-populated rows of a new data type, can the skill help bootstrap an `OVERLAY.md` for them? Could be a future "skill-creator" companion tool.

- **Cross-overlay sharing.** v2.0 promotes the obvious shared patterns (compound-name shape lint, the generic schema) into the top-level `scripts/` and `SKILL.md`. If two overlays later end up shipping near-identical scripts (e.g., both mp/bp and viscosity end up needing a temperature-range sanity check), a shared `_common/` slot under `datatypes/` could hold those. Defer until at least two overlays demonstrate duplicated content — preemptive abstraction is the bigger risk right now.

---

## TL;DR

- **Current skill is \~70 % data-type-agnostic.** All the v1.4–v1.7 hardening work (the "context shapes the result" defenses, the Phase 0 manifest, the three-tier audit framework) is property-independent and stays. The v2.0 generic schema has 18 columns: `compound_name`, `compound_smiles`, `property`, `value`, `value_min`, `value_max`, `value_raw`, `units`, `relation`, `meas_calc` (renamed from v1.7's `data_type`), and the source/evidence/notes columns. v1.7's mp/bp-specific `value_celsius` / `value_celsius_min` / `value_celsius_max` are replaced by generic `value` / `value_min` / `value_max` plus an explicit `units` column.
- **The \~30 % that's property-specific** (value-range bounds, unit-conversion math, property-specific anti-patterns, the `property` enum, and a small set of optional extension columns like `reference_electrode` for redox) moves into `datatypes/<X>/` subfolders. `validate_compound_name.py` becomes generic — compound names are universal across data types.
- **Your suggested structure works** with one refinement: each data type gets a single folder under `datatypes/<X>/` that contains its `OVERLAY.md`, `SCHEMA.md`, `COMMON_ERRORS.md`, and a `scripts/` subfolder. The generic skill reads pointers to the right overlay based on the user-specified data type.
- **Migration is 11 steps**, each independently testable. Step 1 is a verbatim copy of `mp-bp-extraction/` to a new `data-extraction/` folder so the v1.7 production skill stays intact until v2.0 is validated. Step 7 is a one-time `migrate_v17_to_v20.py` pass to bring Trial-5 and Trial-6 CSVs to the new schema; the migrated CSVs (plus a 500-row Trial-6 subset for speed) serve as regression baselines in Step 8.
- **Section 5 decisions are resolved:** <!-- fmc:15 -->`data-extraction`<!-- /fmc:15 --> as the new name; v2.0 version; single package; standardize on `compound_name` and other generic column names; user must specify data type explicitly (skill halts if no overlay); two CSVs for cross-property; keep the archived skills and current `mp-bp-extraction/` as historical reference; `audit_criteria.md` stays at the project root (and gets generic-ified in migration Step 5).

Ready to implement on your sign-off.

<!-- forgemark-comments
- id: 1
  anchor_text: "quote contains numeric value"
  context_before: "rty, value) within one paper csv_quote_lint.py — RFC-4180 quoting; column-shift detection quote_support_lint.py — "
  context_after: " quote_template_lint.py — deprecated stub (kept for back-compat) verify_row.py — single-row check bundle run_al"
  author: Steven
  timestamp: "2026-05-21T14:14:08.037Z"
  resolved: false
  body: "This will work for all properties that are numeric, but not for ones that aren’t. For example, state of matter (solid, liquid, gas) or color (blue, green, etc.)"
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Good catch. Added a note in Section 2's generic schema that `value` accepts categorical strings (e.g., "solid", "blue") for non-numeric properties, with `units` empty in those cases. The `quote_support_lint.py` numeric-token check would no-op (or become a string-containment variant) when the property is categorical. The skill's current deterministic checks were designed for numeric properties; adapting them for categorical properties would happen inside the overlay (e.g., a `datatypes/state_of_matter/` overlay could ship its own `value_string_lint.py` and skip the generic numeric quote-support check).
- id: 2
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:16:35.521Z"
  resolved: false
  body: "Compound name and smiles should be generic. All properties will be of a compound and all compounds can have a smiles."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. Moved `compound_name` and `compound_smiles` into the generic schema in Section 2. The 'Schema columns — property-specific' table that originally anchored this comment is gone — the new section is 'Schema columns — always present (generic core)' with these columns in the always-present list."
- id: 3
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:17:29.393Z"
  edited_at: "2026-05-21T14:21:34.589Z"
  resolved: false
  body: "We can keep this generic as well. All properties have a value, units, and raw. When a property has a min/max, then value_max and value_min are the right column name. Add a column, property that specifies what property is being recorded (melting point, boiling point, redox voltage, etc.)."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. Generic schema now has `value`, `value_min`, `value_max`, `value_raw`, `units`, `relation`, and `property` columns. The `property` column specifies which property is recorded per row; each data-type overlay defines its valid enum (mp/bp overlay: `melting_point`, `boiling_point`, `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`). Section 2 schema table reflects all of this."
- id: 4
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:22:41.863Z"
  resolved: false
  body: "melting point and boiling point are different properties, not subtypes, otherwise this makes sense."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. mp and bp are now distinct values of the generic `property` column, not subtypes. The mp/bp overlay enum lists them as separate properties (along with `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`). Updated the OVERLAY example accordingly."
- id: 5
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:24:26.796Z"
  resolved: false
  body: "Don’t include this, redox skill combined search and extraction, this skill is extraction only."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. Removed the source-discovery row from the property-specific scripts table. Migration plan Step 10 (build redox/) now explicitly notes that `find_open_access.py` from the archived redox skill is NOT carried over — this skill stays extraction-only."
- id: 6
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:24:31.835Z"
  resolved: false
  body: "Don’t include this, redox skill combined search and extraction, this skill is extraction only."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. Removed cross-source consistency row from the property-specific scripts table. Migration plan Step 10 explicitly notes `cross_source_consistency.py` is NOT carried over."
- id: 7
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:24:50.224Z"
  resolved: false
  body: "Don’t include this, redox skill combined search and extraction, this skill is extraction only."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Agreed and applied. Removed the `SOURCE_DISCOVERY.md` row from the property-specific references table."
- id: 8
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:29:10.458Z"
  resolved: false
  body: "Needs to have reference. Solvent and pH should exist if in the data, but ok if not (there’s gas phase)"
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Applied. The data-type extension columns table in Section 2 now lists the redox row as `reference_electrode` required, `solvent / ph / n_electrons` optional. The accompanying note clarifies: solvent and pH should be populated when present in the source, but can be empty (e.g., gas-phase)."
- id: 9
  anchor_text: "each data type gets its own folder under each, with a per-data-type"
  context_before: " approach you suggested — data-type-specific subfolders in references/, scripts/, and evals/ — with a small refinement: "
  context_after: " OVERLAY.md document that the agent reads to learn what's different from the generic protocol. Proposed layout data-ex"
  author: Steven
  timestamp: "2026-05-21T14:31:11.542Z"
  resolved: false
  body: "In the abstract, I like this organization better, but please confirm it conforms to the Agent Skills standard. If not, some harnesses might not interpret it correctly."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Added a new subsection in Section 3 ("Agent Skills standard compliance"). Short version: I'm not aware of a hard restriction in the published Anthropic Agent Skills format against nested subfolders under `scripts/` or `references/` — the skill is loaded by reading SKILL.md and the files it references, with no formal layout requirement beyond that. But this is worth verifying against the actual harness we use before we commit.

        I added a fallback option to the proposal in case a harness rejects nested directories: a flat layout with naming convention like `scripts/mp_bp__value_range_check.py` (using `__` as the data-type separator). Same modularity, no nesting. Default plan is nested, validated in migration Step 6 (run evals against the new structure).
- id: 10
  anchor_text: "melting-point and boiling-point"
  context_before: "zip) How the agent invokes a specific data type When the user applies the skill, they specify a data type: \"Extract "
  context_after: " data from the papers in corpora/full_168/.\" The agent reads SKILL.md, follows the generic protocol, and at the approp"
  author: Steven
  timestamp: "2026-05-21T14:31:55.785Z"
  resolved: false
  body: "Will this work if I want just melting point or just boiling point? If not, we may need to separate those two."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Yes — addressed in Section 3 and Section 4. Combined with comment 4 (mp and bp are different properties, not subtypes), single-property runs are natural:

        - The mp/bp overlay defines an enum of property values (mp, bp, DSC_onset, DSC_peak, decomposition, sublimation).
        - When the user asks for "only boiling points", the agent uses the mp/bp overlay but restricts emitted rows to `property = boiling_point`.
        - The overlay defines what's available; the user's instruction filters which to emit.

        So mp and bp stay in one overlay folder (they share schema, units, conversion math, and ~all anti-patterns), and the user can still extract just one of them.
- id: 11
  anchor_text: "Concretely for mp/bp"
  context_before: "datatypes/<X>/COMMON_ERRORS.md. What an OVERLAY.md looks like A short, intent-level document the agent reads first. "
  context_after: |
    : # Data type: melting-point and boiling-point (mp/bp)
    
    This overlay tells you what's specific to mp/bp extraction. Use
  author: Steven
  timestamp: "2026-05-21T14:53:52.880Z"
  resolved: false
  body: "mp/bp specific columns should be more narrow than listed here, see comments above."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Updated. The OVERLAY example now reflects the broader generic schema (per comments 2, 3, 4). The mp/bp overlay declares **zero** extension columns — all the compound/value/relation/units fields are generic, populated for mp/bp by setting `units = "°C"` and `property` to one of the six values. The example's Schema section now says: "No data-type extension columns. mp/bp rows use the generic schema exactly: `compound_name` for the compound identity, `property` set to one of the six values above, `value` in °C, ..."
- id: 12
  floating: true
  author: Steven
  timestamp: "2026-05-21T14:55:04.646Z"
  resolved: false
  body: "Don’t include this estimates. You are doing this and it doesn’t take you nearly this long."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Removed. The time estimate (\"1–2 hours of reading\") is gone from the migration plan — the steps no longer carry effort estimates."
- id: 13
  anchor_text: "Create the"
  context_before: "h. Most of the work is identifying which paragraphs of SKILL.md, EXTRACTION_PROMPT_TEMPLATES.md, etc. need to be split. Step 3 — "
  context_after: " datatypes/mp_bp/ folder inside data-extraction/. mp and bp share schema, units, unit-conversion math, and most anti-patte"
  author: Steven
  timestamp: "2026-05-21T14:55:33.660Z"
  resolved: false
  body: "Confirm that it’s ok to keep mp and bp together."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Confirmed and noted in the migration plan. Added to Step 3: "mp and bp share schema, units, unit-conversion math, and most anti-patterns, so they live together in one overlay (they're different `property` values within the same overlay's enum)."

        The single-property extraction case (the user wants only mp or only bp) is handled at extraction time by filtering on the `property` column — no need to split the overlay folder. See the reply on comment 10 for the user-filter explanation.
- id: 14
  anchor_text: "4. Migration plan"
  context_before: "s. The verifier still emits the same JSON output schema (verdict, reason, details, verifiable, verifiability_tag).   "
  context_after: " Concrete steps to convert the current skill to the modular form. Each step is independently testable. The first step pre"
  author: Steven
  timestamp: "2026-05-21T14:57:41.331Z"
  resolved: false
  body: "Instead of making edits to the existing skill, let’s preserve it. Make a complete copy of the mp-bp-extraction folder and name it data-extraction. Then, make your edits in that folder."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Applied. Migration plan now opens with a sentence stating the preservation strategy, then Step 1 is: "Copy `mp-bp-extraction/` to `data-extraction/`. Verbatim copy, no edits." All subsequent steps happen inside `data-extraction/`. The v1.7 `mp-bp-extraction/` stays untouched as the still-installable production skill until v2.0 is validated.

        I also moved the rename/repackage step (originally Step 6) to be a smaller "update front matter + repackage" step (now Step 9), since the directory rename happens in Step 1 instead of at the end.
- id: 15
  anchor_text: "`data-extraction`"
  context_before: " in the TL;DR section: \"Section 5 decisions are resolved:\" "
  context_after: " as the new name; v2.0 version; single package; standardize on compound_name and other generic column names; user must"
  author: Steven
  timestamp: "2026-05-21T14:58:39.901Z"
  resolved: false
  body: "Agreed, go with data-extraction."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. Section 5 records `data-extraction` as the final name decision. TL;DR also mentions it. The anchor moved from its original position in the old Section 5 (which I rewrote into the resolved-decisions form) to the TL;DR summary."
- id: 16
  anchor_text: "v2.0"
  context_before: "Section 5 'Skill name, version, packaging' bullet 'Version:' "
  context_after: ". The schema column names and the agent-must-specify-data-type requirement are real interface changes relative to v1.7."
  author: Steven
  timestamp: "2026-05-21T14:58:49.338Z"
  resolved: false
  body: Agreed
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. v2.0 it is. Section 5 records this and Migration plan Step 9 mentions bumping the version."
- id: 17
  anchor_text: "Single `.skill` zip containing all data types"
  context_before: "Section 5 'Skill name, version, packaging' bullet 'Packaging:' "
  context_after: ". Simpler to maintain; users who only care about one property can still install the single package."
  author: Steven
  timestamp: "2026-05-21T14:59:03.064Z"
  resolved: false
  body: "Single package."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. Single-package decision recorded in Section 5."
- id: 18
  anchor_text: "Standardize on generic names."
  context_before: "Section 5 'Schema-column naming convention' "
  context_after: " `compound_name` everywhere (not 'molecule'). The reasoning: future joins across property families (e.g., 'for compounds where we have both mp and redox data, look at correlations') are valuable"
  author: Steven
  timestamp: "2026-05-21T15:00:44.011Z"
  resolved: false
  body: "Single, generic name. Go with compound_name. The reason is that it’s valuable to be able to join tables in the future to have multiple properties per compound. This lets you look and build models involving associations between properties."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Applied throughout. Section 2's schema table now lists `compound_name`, `compound_smiles`, `property`, `value`, `value_raw`, `value_min`, `value_max`, `units`, `relation` as generic columns — same name across every data type. Redox no longer uses `molecule`; it uses `compound_name` with the multi-couple-disambiguation convention recorded in the redox overlay's notes/extension fields rather than embedded in the column name.

        Section 5 records the rationale (cross-property table joins). Section 5's "cross-property datasets" decision explicitly says joining two CSVs on `compound_name` becomes trivial because of the standardized name.

        Anchor moved from its original position in the old Section 5 (which I rewrote into the resolved-decisions form). The new anchor wraps the resolved decision in the updated Section 5.
- id: 19
  anchor_text: "The user must specify the data type explicitly."
  context_before: "Section 5 'Auto-discovery of data types' "
  context_after: " Papers commonly report multiple property types (e.g., a synthesis paper has both mp/bp and yield), so there's no reliable way to infer what the user wants. If the user requests a data type that doesn't have an overlay (no `datatypes/<X>/`), the agent halts and asks the user to either pick a supported data type or write a new overlay first."
  author: Steven
  timestamp: "2026-05-21T15:02:12.767Z"
  resolved: false
  body: "Definitely. user must specify. Papers have multiple property types, so no easy way to infer what’s desired. The skill should also halt if the user asks for a property type that it doesn’t have references and scripts for."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: |
        Applied. Section 5 records "The user must specify the data type explicitly." Section 3 now adds the hard rule: "If the user asks for a data type that doesn't have a folder yet, the agent halts and asks the user to either pick from the available data types or write a new overlay first. This is a hard rule — no inference from corpus content, no falling back to a 'generic' extraction without an overlay."

        Migration plan Step 4 also notes that SKILL.md needs to add this halt rule explicitly.
- id: 20
  anchor_text: "Two separate CSVs, one per data type."
  context_before: "Section 5 'Cross-property datasets' "
  context_after: " A user extracting both mp/bp and redox from the same corpus runs the skill twice. Joining the two CSVs on `compound_name` after the fact is straightforward (and the standardized compound-name column makes it trivial)."
  author: Steven
  timestamp: "2026-05-21T15:02:45.371Z"
  resolved: false
  body: "Agreed. It is easy to join the tables afterwards if needed."
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. Section 5 records 'Two separate CSVs, one per data type.' The joining-becomes-trivial point is tied to the standardized `compound_name` decision from comment 18."
- id: 21
  anchor_text: "Keep both as-is in `_archive/` (or in the case of `mp-bp-extraction/`, keep at the repo root until the new `data-extraction/` skill is validated)."
  context_before: "Section 5 'Fate of _archive/example_skill_redox/ and the current mp-bp-extraction/' "
  context_after: " They're the historical record of the v1.0–v1.7 evolution and the proof points for the migration."
  author: Steven
  timestamp: "2026-05-21T15:02:59.507Z"
  resolved: false
  body: Agreed.
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. Section 5 records 'Keep both as-is.' Added a note that after v2.0 ships and is validated by a real trial run, we can decide whether to formally archive `mp-bp-extraction/` too."
- id: 22
  anchor_text: "Stays at the project root, outside the skill package."
  context_before: "Section 5 'Where audit_criteria.md lives' "
  context_after: " It's maintainer-facing. Verifier agents read references/VERIFICATION_PROMPT_TEMPLATES.md (inside the skill) for the Q1–Q5 protocol; the higher-level 'what does an audit measure' framing lives in audit_criteria.md for the human maintainer."
  author: Steven
  timestamp: "2026-05-21T15:03:15.620Z"
  resolved: false
  body: Agreed.
  replies:
    - author: Claude
      timestamp: "2026-05-21T17:00:00Z"
      body: "Confirmed. `audit_criteria.md` stays at the project root. Section 5 records this."
-->

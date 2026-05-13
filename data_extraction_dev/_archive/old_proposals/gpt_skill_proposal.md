# Proposal: Modular Skill for Verifiable Scientific Property Extraction

## Executive summary

Build the skill as a conservative, evidence-first extraction pipeline. Its primary rule should be: emit a row only when the compound identity, property value, units, data origin, and source provenance can be independently verified from the paper without relying on hidden context. Missing a difficult row is acceptable; emitting an ambiguous or wrong row is not.

The main lesson from the melting point and boiling point tests is that value extraction is not the hardest part. The largest accuracy risk is compound naming: local labels, table codes, R-group templates, section headings, shorthand such as "compound 4", and generic phrases can all look like compound names but are not usable in a final table. The skill should therefore separate property detection from compound identity resolution, and it should reject rows whose compound name cannot be made standalone and verifiable.

The skill should be modular. The core skill should handle document ingestion, evidence capture, candidate tracking, compound identity resolution, row validation, deduplication, and verification. Property-specific behavior, such as melting/boiling point triggers, units, exclusions, and event terms, should live in separate adapter references or scripts.

## Target behavior

The skill should optimize for at least 98% correctness across:

- standalone compound names
- property type and value
- units and conversions
- DOI and article metadata
- evidence text or evidence location
- data-origin labels such as measured, cited experimental, predicted, calculated, or open bound

The extraction policy should default to high precision:

- Skip unresolved compound identities.
- Skip property values that cannot be tied to a specific compound.
- Skip values where the property type is ambiguous.
- Preserve uncertain but useful candidates in a skipped-candidates file rather than the final CSV.
- Prefer structured fields over overloaded text.

## Proposed skill layout

```text
scientific-property-extractor/
  SKILL.md
  references/
    core_workflow.md
    core_schema.md
    source_ingest.md
    compound_identity_resolution.md
    row_acceptance_gates.md
    verification_protocol.md
    property_adapter_contract.md
    adapters/
      melting_boiling_points.md
      example_new_property_adapter.md
  scripts/
    extract_text.py
    parse_nxml_tables.py
    build_candidate_index.py
    normalize_values.py
    validate_rows.py
    compare_extractions.py
    sample_for_verification.py
```

`SKILL.md` should stay short. It should tell the agent to run the pipeline, select a property adapter, preserve notes, and apply strict acceptance gates. The detailed logic should live in references and scripts so the skill can expand to other property types without rewriting the core.

## Core workflow

### 1. Define extraction scope

Before extracting, create a run configuration:

- target property adapter, for example `melting_boiling_points`
- accepted data origins: measured, cited experimental, predicted, calculated
- accepted relation types: exact, range, greater-than, less-than
- unit normalization rules
- whether inferred compound names are allowed
- whether graphical-only structures may be used
- required output fields

For high-precision production runs, default settings should be:

- include measured and cited experimental values
- exclude predicted/calculated values unless explicitly requested
- keep open bounds only with a structured relation field
- reject inferred compound names unless a reviewer explicitly approves them
- reject graphical-only compound identities unless OCR or structure parsing provides a verifiable name

### 2. Ingest paper text and metadata

For each article, build an article package:

- canonical article id
- DOI from NXML metadata, PDF metadata, article text, or manual metadata file
- plain text extracted from NXML when available
- table objects from NXML when available
- PDF text from more than one extractor when needed
- figure captions, scheme captions, table captions, section headings
- coordinates or table row/column locations when available

The prior tests showed several ingestion-specific risks:

- PDF minus signs can be lost or mangled, especially in QSPR/modeling papers.
- NXML tables are much safer than flattened PDF text.
- Source text windows can drift into the previous or next compound if boundaries are not respected.
- Image-cell tables can contain compound identifiers that normal text extraction misses.

The skill should prefer structured sources in this order:

1. NXML article metadata and tables
2. NXML body text with section boundaries
3. PDF text in layout mode
4. PDF text in raw mode for signs, columns, and tabular data
5. OCR or supplementary files for image-heavy tables

If no reliable text source exists, the skill should skip rather than guess.

### 3. Build a candidate index

The extractor should first enumerate candidates, not immediately emit final rows. A candidate is any local evidence that might contain a property value. Each candidate should include:

- article id and DOI
- source type: paragraph, table, caption, supplementary text
- section path
- table id, row id, column id, if applicable
- raw value text
- raw unit text
- nearby compound label or name
- property trigger that matched
- data-origin trigger, if any
- raw evidence text

This candidate-first approach prevents silent misses like the Dearden table and allows later validation to explain why rows were skipped.

### 4. Build article-level identity maps

Before resolving individual candidates, build maps for compound identifiers used in the paper:

- explicit code-to-name mappings, such as `5d = ethyl ...`
- table row labels to names
- scheme labels to captions and product names
- headings that introduce named compound series
- R-group table definitions
- ligand/complex relationships
- synonym and abbreviation definitions

The identity map should include a confidence level and evidence for each mapping. It should not assume that a local label such as `4a`, `compound 3`, or `complex 9` is itself a valid final compound name.

### 5. Resolve compound identity

For every candidate, resolve a standalone `compound_name`. The final name must be usable outside the paper. Store local labels separately.

Recommended fields:

- `compound_name`: standalone interpretable name
- `compound_label`: local label, such as `5d`, `compound 4`, or `complex 9`
- `compound_name_source`: exact evidence used to resolve the name
- `name_resolution_method`: exact_text, table_mapping, scheme_mapping, abbreviation_expansion, reviewer_approved_inference
- `name_resolution_confidence`: high, medium, low

Rows should be rejected if the name is:

- only a local label, such as `compound 4`
- a range or series, such as `2a-g`
- a section heading, such as `Result and discussion`
- a generic class, such as `benzoxanthenone derivative`
- a phrase that does not name a compound, such as `minor components in the purple`
- an unresolved template, such as `X=H, R=H`, unless the scaffold and attachment points are fully resolved
- a generic product class plus code, unless the code is mapped to a full name
- a metal complex description that omits the ligand identity, stoichiometry, counterion, or hydrate state when those are necessary to identify the compound

Local labels and method annotations should be removed from `compound_name` and stored elsewhere. Examples of text to strip or relocate:

- `(compound 3, Method 2)`
- `[4a]`
- citation markers
- method numbers
- table row numbers
- parenthetical local codes

### 6. Apply property-specific extraction adapter

The core skill should call a property adapter. The adapter defines:

- property names and aliases
- accepted units
- unit conversions
- numeric patterns
- range and inequality handling
- table-header triggers
- paragraph triggers
- exclusion terms
- data-origin classification
- method/instrument fields
- property-specific sanity checks

For melting/boiling point extraction, the adapter should define:

- accepted properties: melting point, boiling point, fusion temperature when equivalent to melting point
- optional event labels: decomposition, sublimation, glass transition, crystallization, DSC transition
- units: C, K, F when conversion is explicit and safe
- value structures: exact, range, greater-than, less-than
- exclusions: Tg, Tc, aggregate model statistics, non-compound summary values
- data origins: experimental measured, experimental cited, predicted, calculated

The adapter should not decide whether the compound name is valid. That belongs to the core identity-resolution gate.

### 7. Normalize values into structured fields

Do not flatten value semantics into a single text column. Recommended fields:

- `property_name`
- `property_type`
- `value_original_text`
- `unit_original`
- `value_celsius`
- `value_min_celsius`
- `value_max_celsius`
- `value_midpoint_celsius`
- `value_relation`: exact, range, greater_than, less_than
- `conversion_note`
- `thermal_event`
- `data_origin`
- `measurement_method`
- `instrument`

For ranges, preserve both endpoints and optionally compute midpoint. For open bounds, preserve the relation. Do not turn `>300 C` into `300 C` without a relation field.

### 8. Capture verifiable evidence

Every emitted row needs enough provenance for an independent reviewer to verify it quickly.

Recommended evidence fields:

- `evidence_text`: exact contiguous article text when available
- `evidence_location`: section/table/row/column/page
- `compound_evidence_text`: exact text used to resolve compound name
- `property_evidence_text`: exact text used to resolve value and unit
- `doi_evidence`: metadata source or text source for DOI

For tables, exact contiguous article text may be impossible or awkward. In that case, use structured provenance:

```text
Table 2, row "5d", columns "Compound", "mp C", and "Name"
```

The previous tests showed that paraphrased source text is a verification weakness. Paraphrase should be avoided in final evidence fields unless marked as `evidence_type=structured_summary`.

### 9. Validate rows before emission

The validator should enforce acceptance gates before a row enters the final CSV.

Required gates:

- DOI is present or explicitly marked unavailable after search.
- Compound name is standalone and not merely a local label.
- Compound name evidence supports the final name.
- Property value appears in the evidence or table coordinates.
- Unit is explicit or safely inherited from a table header.
- Conversion is reproducible.
- Property type is not contradicted by nearby text.
- Data origin is classified.
- The row is not a duplicate under a structured dedup key.
- The source evidence is sufficient for independent verification.

Suggested high-risk gates:

- Reject R-group names unless scaffold, substituent values, and attachment points are resolved.
- Reject generic derivative names unless code-to-full-name mapping is found.
- Reject heading-derived names unless confirmed by table/prose evidence.
- Reject manually transcribed names that differ in chemistry-bearing tokens from source text.
- Flag or reject names where tokens such as acid, nitrile, amide, ester, chloride, sulfate, hydrate, methyl, ethyl, fluoro, chloro, bromo, iodo, oxime, thione, and oxide change between source and output.

### 10. Deduplicate structurally

Deduplication should use a structured key, not raw string equality:

```text
article_id
doi
compound_name_normalized
compound_label
property_type
value_original_text
value_relation
value_min
value_max
data_origin
thermal_event
measurement_context
```

This avoids keeping duplicate rows that differ only by citation text or method annotations, while preserving genuinely distinct rows such as measured vs cited values, pure compound vs solution, or melting vs decomposition.

### 11. Produce final and diagnostic outputs

Each run should produce:

- `extracted_properties.csv`: accepted rows only
- `skipped_candidates.csv`: rejected candidates with reason codes
- `extraction_notes.md`: decisions, caveats, paper-specific issues, and commands/scripts used
- `verification.md`: independent verification results
- `run_config.json`: property adapter and scope settings

The skipped file is important. It preserves recall opportunities without contaminating the high-confidence final table.

## Verification protocol

The verification step should be part of the skill, not an optional afterthought.

### Automated verification

Run deterministic checks over every row:

- DOI format and DOI/article consistency
- evidence field present
- final value present in evidence or table coordinates
- unit conversion round-trip
- no banned compound-name patterns
- no unresolved labels in `compound_name`
- no plural series names in `compound_name`
- local labels stored outside `compound_name`
- chemistry-bearing token consistency between source and output
- duplicate-key check
- property-specific range and unit sanity checks

### Independent manual verification

For production extraction, sample rows after automated validation:

- random sample across the full table
- stratified sample by article
- targeted sample of high-risk rows
- 100% review of rows with medium confidence, inferred names, R-group resolution, metal complexes, image-table sources, PDF-only extraction, or non-Celsius conversion

A suggested acceptance gate for the 98% target:

- If a 100-row random audit finds more than 1 wrong row, fix root causes and rerun.
- If any wrong row reveals a systematic class of errors, audit all rows in that class.
- Do not release until automated checks pass and targeted high-risk review has no unresolved critical errors.

For a stricter statistical gate, use a larger sample. But in this task domain, systematic error discovery is more valuable than a single random percentage, because one bad rule can corrupt many rows.

### Verification scoring

Score each audited row independently for:

- compound name correctness
- property value correctness
- unit/conversion correctness
- property classification correctness
- DOI/article correctness
- evidence sufficiency

A row should count as wrong if any required field is wrong or unverifiable. Cleanup-only issues, such as a local label left in the name, should count as wrong when they make the final table less standalone or less useful.

## Lessons from the test runs

### Compound naming is the main failure mode

The GPT extraction frequently emitted non-standalone names such as local labels, generic derivatives, section headings, and unresolved templates. The Claude extraction had cleaner names overall but still had issues with R-group templates, generic derivative labels, and at least one chemistry-bearing transcription error.

Design response:

- make compound identity resolution mandatory
- store labels separately
- reject unresolved local/contextual names
- add chemistry-token consistency checks
- require evidence for name resolution, not just value evidence

### Scope needs explicit data-origin fields

Many apparent disagreements were not value errors. They came from different policies around calculated values, predicted values, literature-cited values, open bounds, and DSC events.

Design response:

- add `data_origin`
- add `thermal_event`
- add `value_relation`
- make extraction scope explicit in `run_config.json`
- do not collapse measured, cited, predicted, and calculated values into the same untyped property row

### Table-level extraction prevents major misses

One run missed an entire Dearden table because the extraction path did not robustly parse the experimental columns. Another missed clear rows because its regex patterns were too narrow.

Design response:

- enumerate candidate tables before extracting rows
- scan all table headers for property triggers
- record table coverage and candidate counts per article
- compare expected candidate counts against emitted and skipped rows

### Evidence windows must respect structure

Some values were correct but source snippets pointed to the wrong neighboring compound. This undermines verification.

Design response:

- use table coordinates for table evidence
- snap paragraph windows to section and sentence boundaries
- store separate compound and property evidence when needed
- avoid paraphrased evidence in final CSV

### Image-heavy papers require special handling

Papers with structure images or image-only compound cells cannot be safely handled by text extraction alone.

Design response:

- try OCR, alt text, supplementary data, or captions
- if the full name remains unavailable, skip the row
- record skipped candidates with reason `compound_identity_graphical_only`

## Property adapter contract

Each property adapter should define:

```yaml
property_family: melting_boiling_points
accepted_properties:
  - melting_point
  - boiling_point
units:
  accepted: [C, K, F]
  canonical: C
value_patterns:
  - exact_number
  - range
  - greater_than
  - less_than
table_triggers:
  - mp
  - m.p.
  - melting point
  - bp
  - b.p.
  - boiling point
paragraph_triggers:
  - melts at
  - boiling point
exclusion_triggers:
  - Tg
  - glass transition
  - crystallization temperature
data_origin_rules:
  measured:
    - experimental
    - found
    - observed
  cited_experimental:
    - lit.
    - literature
  predicted:
    - predicted
    - calculated by model
normalization:
  ranges: preserve_endpoints_and_midpoint
  inequalities: preserve_relation
```

For a new property type, the agent or developer should add a new adapter file rather than changing the core skill. For example, density, solubility, refractive index, pKa, band gap, and toxicity would each have their own triggers, units, exclusion terms, and sanity checks.

## Recommended implementation phases

### Phase 1: Core high-precision pipeline

- Implement source ingestion for NXML and PDF text.
- Implement candidate enumeration.
- Implement core CSV schema.
- Implement skip log.
- Implement strict compound-name acceptance gates.
- Implement MP/BP adapter as the first property adapter.

### Phase 2: Identity-resolution improvements

- Add article-level code-to-name mapping.
- Add R-group table handling with explicit scaffold validation.
- Add metal-complex name handling.
- Add local-label cleanup.
- Add chemistry-bearing token checks.

### Phase 3: Verification tooling

- Add deterministic row validator.
- Add random and stratified sampling script.
- Add comparison script for cross-run or cross-model audits.
- Add verification report template.

### Phase 4: Broader property support

- Add adapter contract tests.
- Add additional property adapters.
- Add per-property examples.
- Add OCR or supplementary-file handling for graphical tables.

## Proposed operating rules for the skill

1. Emit only rows that are independently verifiable.
2. Treat compound identity resolution as mandatory.
3. Keep local labels out of final compound names.
4. Preserve property semantics in structured fields.
5. Keep measured, cited, predicted, calculated, and open-bound values distinguishable.
6. Prefer exact evidence or structured table coordinates over paraphrase.
7. Use skipped-candidate logs to protect recall without polluting final data.
8. Require automated validation before final output.
9. Audit high-risk rows manually.
10. Record all extraction decisions in notes.

## What this would have prevented in the test runs

- Section headings and prose fragments would fail the standalone-name gate.
- `compound 4`, `4a`, and `complex 9` would be stored as labels, not names, unless resolved.
- `2a-g` series names would be rejected unless split into resolved individual compounds.
- R-group names would be rejected unless the scaffold and positions were fully resolved.
- Open-bound values would be retained as `value_relation=greater_than` instead of flattened.
- Predicted and calculated values would not be mixed with measured values.
- Dearden-style tables would be found by table-header scanning.
- Source snippets would be replaced by table coordinates when exact text is unreliable.
- Chemistry-bearing transcription errors such as acid vs nitrile would be flagged.

## Bottom line

The reliable skill is less like a single extractor and more like a conservative evidence pipeline:

1. Find candidates broadly.
2. Resolve compound identity rigorously.
3. Normalize property values structurally.
4. Reject anything that cannot be verified.
5. Audit the accepted rows and learn from every error class.

That design should give the best chance of reaching the 98% correctness target while remaining extensible to many scientific property types beyond melting and boiling points.

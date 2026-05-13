# Property Extraction Skill — Merged Design Proposal (v2)

A modular skill for extracting compound-level physical-property data from
scientific papers. Target: **≥ 98 % correct** on compound names, property
values, units, data origin, DOI, and evidence — **measured on a held-out
corpus, after audit-failed rows are quarantined**. **Precision over
recall** — a missed row is better than a wrong row.

The skill is **property-agnostic at the top level**. Melting-point /
boiling-point logic lives in a swappable property adapter. New properties
(log P, pKa, density, solubility, color, crystal system, …) plug in via
the same interface. Both numeric and qualitative properties are
supported by the schema.

This v2 proposal merges the original `claude_skill_proposal.md` and
`gpt_skill_proposal.md`, incorporates user feedback (Forgemark comments
#1–#3 and the follow-up review), and folds in fixes from a critical
self-review and an independent review by the GPT instance.

The accuracy target is **enforced by validation gates and audit results**,
not guaranteed by design alone. We measure against the threshold; we
don't assert it. **Any row that fails independent audit is moved to the
skip log before the pass rate is computed** — the 98 % gate is on the
delivered output, not on the original emission.

---

## 1. What the prior audits taught us

The Claude-Test and GPT-Test extractions, the two cross-checks, and the
100-row random audits surfaced **eight failure modes**. Every design
decision below maps to one of these:

| # | Failure mode | Where it bit | Fix in this skill |
|---|---|---|---|
| F1 | Wrong compound name (functional group transcribed wrong) | Claude row for paper 011 compound 5d (benzonitrile vs benzoic acid) | All names emitted by string extraction from source text, never typed by hand; bidirectional, position-aware identity-token consistency check (§ 7) |
| F2 | Section title used as compound name | GPT used `"Result and discussion"`, `"N-Hydroxypyridinedione Oximes 33-50"` | Compound-name reject list + require list (§ 6) |
| F3 | Local-label-only names (unusable without paper) | Both: `compound 3`, `Pb(II) complex of compound 4`, `benzoxanthenone derivative 4b` | Standalone-name validator; **unresolved rows go to `skipped_candidates.csv`, never to the output CSV** (no sentinel rows in delivered output) |
| F4 | Template-format names with unresolved variables | Both, paper 050: `(X=Cl, R=4-CH3)` with X position never bound | Cross-reference table headers against prose; reject `(X=…)` patterns unless resolved (§ 5 step 5) |
| F5 | Whole table or paper missed | GPT missed all 196 Dearden rows; Claude missed all 47 paper 064 rows | **Candidate-first enumeration** (every property-relevant mention enters a candidate index *before* filtering) + per-paper coverage check (§ 5 steps 3, 9) |
| F6 | Duplicate rows from inline + table appearances | GPT: paper 026 compounds 4 & 6 twice, paper 178 4h–4j twice | Strong dedup key (§ 5 Gate F) including `relation`, `data_origin`, `instrument` to prevent over-collapsing |
| F7 | Open-bound and predicted values handled inconsistently | Claude skipped `>X`; GPT included. Krossing calculated values divided the systems | Explicit `relation` + `data_origin` columns; default is consumer-filterable; `--strict` preset for conservative use (§ 10) |
| F8 | Prose-fragment provenance / paper-jargon in name field | Both: `(NMP, pure guest)`, `Method 1`, `clathrate B`, `[51]` citation marks | Separate `compound_label` and split evidence columns; name field is chemical identity only |

The audits agree on a clear remediation pattern: **resolve compound
identity to a standalone name before emitting a row**, and **reject any
row where that cannot be done**.

---

## 2. Operating rules

The skill operates under twelve standing rules. Every script and validator
is built to enforce them:

1. **Emit only rows that are independently verifiable from the paper.**
2. **Compound identity resolution is mandatory.** No final-CSV row may
   carry a local-label-only name (`compound 3`, `complex 9`, `derivative
   4a`).
3. **Local labels stay out of `compound_name`.** They live in
   `compound_label`.
4. **Preserve property semantics in structured fields.** Don't flatten
   ranges, inequalities, or units into a single text column.
5. **Keep measured, cited, predicted, and calculated values distinguishable**
   via `data_origin`. The default emission policy is to extract
   everything and tag; consumers filter on read. A `--strict` preset
   is documented for users who want measured + cited experimental
   only.
6. **Prefer exact evidence or structured table coordinates over
   paraphrase.** Paraphrased evidence is **never emitted to the final
   output**. Rows whose evidence cannot be expressed as either
   verbatim text or structured table coordinates go to
   `skipped_candidates.csv` with `skip_reason =
   paraphrase_evidence_not_allowed`. (v2 backlog item: investigate
   safe paraphrase handling.)
7. **Use a skip log** to protect recall without polluting the final
   table. Every candidate not emitted is recorded with a `skip_reason`.
8. **Require automated validation before final output**, and quarantine
   audit-failed rows before computing the pass rate. The 98 % gate is
   on the delivered output, not the original emission.
9. **Stratified-audit high-risk rows** in addition to random sampling.
   Random alone misses systematic errors at the precision we need.
10. **Record every extraction decision in `extraction_notes.md`** as
    the run proceeds. Decisions made silently are decisions that can't
    be audited.
11. **Coverage check before verification**, not after. Coverage misses
    are systematic; finding them after a failed audit is too late.
12. **The accuracy target is measured on a held-out corpus.** The
    20-paper `mp_bp_dev_set` is the training corpus the gates were tuned
    against. The held-out corpus (the user's larger paper set, from
    which `mp_bp_dev_set` was sampled) is the real precision
    measurement.

---

## 3. Schema (property-agnostic, supports numeric + qualitative)

The canonical unit and the values of `property_subtype` are defined by
the **property adapter**. The columns themselves are property-neutral.
The schema supports both numeric properties (mp, bp, log P, pKa, density)
and qualitative properties (color, phase, crystal system, morphology).

```
column                          type      description
-----------------------------------------------------------------------------
compound_name                   str       standalone, unique chemical identity
                                          (IUPAC, common, or unambiguous
                                          shorthand). Must pass the standalone-
                                          name validator. No paper-local labels.
compound_label                  str       paper-local label or compound code
                                          (e.g., "4a", "compound 3"). Optional;
                                          for traceability.
compound_evidence_text          str       exact article text snippet that
                                          supports compound identity. Required.
compound_evidence_type          str       "verbatim_text" | "structured_coordinates"
name_resolution_method          str       "exact_text" | "code_lookup" |
                                          "template_resolution" |
                                          "scheme_mapping" |
                                          "reviewer_approved_inference"
name_resolution_confidence      str       "high" | "medium" | "low"
property_name                   str       controlled vocabulary; defined by adapter
                                          (e.g., "melting_point", "boiling_point",
                                          "log_p", "pka", "color")
property_subtype                str       adapter-defined sub-classification
                                          (mp/bp: "melt", "decomp", "boil",
                                          "DSC_onset"; log_p: "octanol_water";
                                          pka: "pKa1", "pKa2"; color: "appearance")
value_type                      str       "numeric" | "qualitative" | "boolean"
                                          (a range is represented as numeric
                                          with non-null _min/_max; no separate
                                          "range" type)
value_canonical                 float|NULL value in adapter's canonical unit;
                                          midpoint for ranges; boundary value for
                                          open bounds (e.g., 50 for ">50").
                                          NULL when value_type is qualitative
                                          or boolean.
value_canonical_min             float|NULL range lower bound (NULL if not a range);
                                          presence of _min and _max indicates a
                                          range value
value_canonical_max             float|NULL range upper bound (NULL if not a range)
canonical_unit                  str|NULL  adapter's canonical unit (e.g., "°C"
                                          for mp/bp; "" for log P). NULL for
                                          qualitative properties.
value_text                      str|NULL  string content for qualitative
                                          properties (e.g., "red crystals",
                                          "amorphous", "P2_1/c"). NULL for
                                          numeric properties.
value_original                  str       printed value/text exactly as in paper
unit_original                   str       unit as printed (e.g., "°C", "C", "K",
                                          "°F", or "" for unitless properties)
relation                        str       "=" (default), ">", "<", "≥", "≤",
                                          "≈", "~"  (≈ and ~ are aliases for
                                          "approximately")
property_evidence_text          str       exact article text snippet supporting
                                          the value + unit. Required.
property_evidence_type          str       "verbatim_text" | "structured_coordinates"
evidence_location               str       hierarchical pointer to source:
                                          "Experimental > Synthesis of … > Table 2
                                          row 4a column 'Mp (°C)'"
data_origin                     str       "measured_by_article" |
                                          "literature_cited" |
                                          "predicted_<method>" |
                                          "unknown"
instrument                      str       e.g., "DSC", "capillary", "Mettler FP62",
                                          "unk". Free-form; included in dedup key.
source_section                  str       paper section path
doi                             str       verified DOI (see § 5 step 2 for
                                          verification procedure)
doi_evidence                    str       which source the DOI came from:
                                          "nxml_front_matter" | "pdf_metadata" |
                                          "pdf_text" | "publisher_lookup" |
                                          "user_metadata"
doi_verified                    bool      true if DOI was cross-validated across
                                          at least two sources
article_id                      str       stable file/folder/source identifier
extraction_confidence           str       "high" | "medium" | "low"
                                          (must be ≤ name_resolution_confidence)
```

**Notes on the schema design:**

- **Split evidence**: `compound_evidence_text` + `compound_evidence_type`
  and `property_evidence_text` + `property_evidence_type` are
  independent. When a code is resolved to a name via a different
  paragraph (the paper 020 `compound 3` case), each piece of evidence
  has its own type. A row may have verbatim prose evidence for the
  compound and structured-coordinate evidence for the value.
- **Property-neutral**: `value_canonical` + `canonical_unit` works for
  numeric properties; `value_text` works for qualitative properties.
  The adapter declares which kind it produces (or both).
- **Open bounds**: `value_canonical` always holds the numeric boundary
  even when `relation` is `>` or `<`. `>50` stores `50` with
  `relation = ">"`. Consumers filter on `relation` to opt in/out.
- **Approximate values**: `≈` and `~` are both recognized as
  "approximately" relations. `relation = "~"` is preferred for ASCII
  hygiene; `≈` is normalized to `~` on input.
- **Confidence relationship**: `extraction_confidence ≤
  name_resolution_confidence`. A row with `name_resolution_confidence
  = low` cannot have `extraction_confidence = high`. Enforced by row
  validator (§ 9a).
- **DOI verification**: `doi_verified = true` requires the DOI to
  match between at least two sources (NXML front matter, PDF metadata,
  PDF text, publisher lookup, or user-provided metadata). If only one
  source exists, `doi_verified = false` and the row's
  `extraction_confidence` is capped at `medium`.

---

## 4. Skill file layout

```
property-extractor/
├── SKILL.md                            # Top-level workflow (§ 5)
├── reference/
│   ├── schema.md                       # Column spec (§ 3)
│   ├── operating_rules.md              # The 12 rules (§ 2)
│   ├── source_ingestion.md             # NXML, PDF, text parsing recipes
│   ├── name_validators.md              # REJECT/REQUIRE patterns (§ 6)
│   ├── identity_token_check.md         # Identity-token consistency (§ 7)
│   ├── verification_protocol.md        # Audit protocol (§ 9)
│   ├── verifier_prompt.md              # Frozen prompt template (§ 9b)
│   ├── property_adapter_contract.md    # Adapter interface (§ 8)
│   ├── run_config.md                   # Run-config schema and presets
│   ├── tests_and_evals.md              # Test plan (§ 12)
│   └── todo.md                         # Maintained backlog (§ 13)
├── scripts/
│   ├── main.py                         # CLI entry point; orchestrates pipeline
│   ├── ingest_article.py               # → sections, tables, DOI, raw text
│   ├── verify_doi.py                   # → cross-source DOI validation
│   ├── build_candidate_index.py        # → candidate enumeration (F5)
│   ├── build_label_dictionary.py       # → {code: name} from article
│   ├── resolve_template_variables.py   # → X/R/etc. → position+substituent
│   ├── resolve_compound_name.py        # → final standalone name
│   ├── validate_name.py                # → standalone-name validator (§ 6)
│   ├── identity_token_check.py         # → identity-token consistency (§ 7)
│   ├── verify_substring.py             # → evidence substring check
│   ├── normalize_value.py              # → ranges, inequalities, units
│   ├── classify_data_origin.py         # → measured/cited/predicted
│   ├── dedup.py                        # → strong-key dedup (F6)
│   ├── coverage_check.py               # → per-paper sanity check (F5)
│   ├── sample_for_verification.py      # → random + stratified sampler
│   ├── audit_verifier.py               # → independent-agent dispatcher
│   ├── validate_row.py                 # → deterministic row gates
│   ├── quarantine_failed_audits.py     # → moves audit-failed rows to skip log
│   ├── emit_outputs.py                 # → CSV + audit log writer
│   └── adapter_loader.py               # → loads property adapter
├── tests/                              # see § 12 for full layout
│   ├── unit/                           # § 12.1 per-script tests
│   ├── golden/                         # § 12.2 dev-corpus expected outputs
│   ├── regression/                     # § 12.3 failure-mode regressions
│   ├── schema_integrity/               # § 12.4 column / type integrity
│   ├── held_out/                       # § 12.5 held-out corpus (user's larger set)
│   ├── modularity/                     # § 12.6 cross-property modularity
│   ├── conformance/                    # § 12.7 adapter contract
│   ├── harness/                        # § 12.8 verifier-harness self-tests
│   ├── robustness/                     # § 12.9 error handling, idempotence, edge cases
│   ├── chemical_diversity/             # § 12.10 name-validator coverage
│   ├── scope_flags/                    # § 12.11 --strict preset behavior
│   └── performance/                    # § 12.12 perf / scalability
└── properties/
    ├── mp_bp/                          # Reference property adapter
    │   ├── adapter.py                  # find_candidates, parse_value, classify
    │   ├── triggers.yaml               # property triggers, units, exclusions
    │   ├── adapter.md                  # narrative documentation
    │   └── golden_tests/               # per-paper expected extractions
    └── example_new_property/
        ├── adapter.py                  # template for new adapters
        └── adapter.md
```

Adding a new property is purely additive: create a new directory under
`properties/`, implement the adapter contract, and the shared scripts
in `scripts/` work unchanged. See § 8 and § 12.6.

---

## 5. SKILL.md — the workflow

`SKILL.md` stays short. It tells the agent to run the pipeline, select a
property adapter, preserve notes, and apply strict acceptance gates.
Detailed logic lives in `reference/` and `scripts/`.

```
Inputs:
  - input_path        : folder, file, or list of articles
  - property          : "mp_bp" | "log_p" | …
  - output_csv        : path
  - skipped_csv       : path
  - audit_log         : path
  - run_config        : path (overrides defaults; schema in reference/run_config.md)

Procedure (paper-by-paper, can be parallelized across papers):

1. LOAD ADAPTER. scripts/adapter_loader.py loads the property adapter
   from properties/{property}/. Reads triggers.yaml and imports
   adapter.py. Adapter must expose:
     - functions: find_candidates, parse_value, classify
     - constants: PROPERTY_NAMES (list), CANONICAL_UNIT,
                   PROPERTY_SUBTYPES, DATA_ORIGINS,
                   DEDUP_VALUE_TOLERANCE
     - lexicon extensions: EXTRA_EXEMPT_NAMES,
                            EXTRA_REJECT_PATTERNS,
                            EXTRA_REQUIRE_PATTERNS
   The loader validates the contract before any extraction runs;
   missing attributes raise at load time, not mid-run.

   IMPORTANT: extraction never modifies the source article files.
   All reads are read-only; any temporary annotations live in the
   skill's own scratch directory and are removed at end of run.

2. INGEST + DOI VERIFICATION. scripts/ingest_article.py returns an
   article object containing:
     - sections (with hierarchical headings)
     - tables (with column/row headers as structured cells)
     - figure/scheme captions
     - DOI candidates from each available source (NXML front matter,
       PDF metadata, PDF text, publisher lookup, user-provided
       metadata)
     - article_id
     - full plain text (concatenation of all sources)

   scripts/verify_doi.py cross-validates the DOI. The script
   distinguishes THE paper's DOI from any DOIs cited in references
   by requiring the DOI candidate to come from one of: NXML front
   matter, PDF metadata, PDF text in the first 2 pages, OR matching
   between two of those — citation DOIs (in reference lists, NXML
   <back>) are explicitly excluded.

   Source precedence (highest to lowest authority):
     1. NXML <front> article-id pub-id-type="doi"
     2. PDF /Doc metadata field "doi"
     3. PDF text matched to a DOI regex in the first 2 pages
     4. Publisher metadata lookup (if configured)
     5. User-provided metadata file

   Decision logic:
     - 2+ sources agree → doi_verified = true, use the matched DOI
     - 1 source only → doi_verified = false, use that source's value,
       cap row extraction_confidence at "medium"
     - Sources disagree → use the HIGHEST-precedence source, flag
       the conflict in audit log, doi_verified = false, cap
       extraction_confidence at "medium". Each row records which
       source won in `doi_evidence`.
     - 0 sources → article-level warning in audit log; rows from
       this article get doi = "" and doi_verified = false. The
       run may still proceed; the user decides whether to deliver
       DOI-less rows.

   Three source modes for text in preference order: NXML > article_text.txt
   > pdftotext. For PDFs, use BOTH `-layout` and `-raw` modes and merge
   — `-raw` is needed to disambiguate negative signs (the Dearden case).

3. ENUMERATE CANDIDATES. scripts/build_candidate_index.py invokes the
   adapter's find_candidates(article) to enumerate every property-
   relevant mention before any filtering. The adapter's
   exclusion_triggers (e.g., "Tg", "RMSE") are applied at this stage
   so genuinely-not-the-property mentions don't enter the index.

   A candidate is any local evidence that *might* contain a property
   value:
     - inline mp/bp/Tm/Tfus/etc. mentions in prose
     - table cells with property-keyword column headers
     - prose mentions in narrative sections

   Every candidate enters the index with:
     - candidate_id (unique within run)
     - article_id, source_section, evidence_location
     - raw value text + nearby compound label
     - property trigger that matched
     - source_type ∈ {paragraph, table, caption, supplementary}

   This candidate-first approach makes F5 (silent table miss) visible:
   the candidate index for Dearden Table 2 would have ~196 rows; if
   the downstream pipeline only emits a handful, that's a coverage
   warning.

4. BUILD ARTICLE-LEVEL IDENTITY MAPS. scripts/build_label_dictionary.py
   walks the ENTIRE article looking for code→name patterns:
     "<IUPAC name> ( <code> )"
     "<IUPAC name>, <code>"
     "Synthesis of <IUPAC name>"  (used as next-paragraph code)
     "<code>: <IUPAC name>"
     "compound <code> = <IUPAC name>"
     "The compound <IUPAC name> (<code>) was synthesized"
   Emits a {code: standalone_name} dictionary used during resolution.
   This catches the Claude paper 020 #3 case (IUPAC name in a
   different paragraph from the mp).

5. RESOLVE TEMPLATE VARIABLES. scripts/resolve_template_variables.py
   scans article prose for table-variable definitions:
     - "X = Cl at position 6"
     - "the 6-chloro derivatives (X = Cl)"
     - "R substituent at the 4-position of the phenyl"
   Builds a {variable: (substituent, position)} dictionary per table.
   This catches the paper 050 X = 6-Cl case.

6. RESOLVE COMPOUND NAMES. For each candidate,
   scripts/resolve_compound_name.py attempts (in precedence order):
     a. If the candidate has a verbatim IUPAC name in its immediate
        context → use it. (The verbatim name wins over any code.)
        The code, if present, is stored in compound_label.
     b. If only a code → look up in the label dictionary from step 4.
     c. If from a table with template variables → expand via step 5's
        dictionary.
     d. Record name_resolution_method and name_resolution_confidence.

   Unresolved candidates go to skipped_candidates.csv with
   skip_reason = compound_identity_not_resolvable_from_paper.

7. APPLY ACCEPTANCE GATES. For each resolved candidate, in order:

   Gate A — STANDALONE-NAME VALIDATOR (§ 6). Reject if the name is a
   section title, prose fragment, "compound N", "derivative N",
   "X=…, R=…" template, etc.

   Gate B — IDENTITY-TOKEN CONSISTENCY (§ 7).
     - Forward check: every chemistry-bearing token in compound_name
       must appear in the union of compound_evidence_text +
       property_evidence_text.
     - Reverse check: chemistry-bearing tokens that appear in
       compound_evidence_text **near the name occurrence** must also
       appear in compound_name. Catches the "evidence says 6-chloro
       but name omits it" case.
     - Position-aware: tokens are matched within ±60 chars of the
       compound-name occurrence in the evidence, not just anywhere.

   Gate C — EVIDENCE-SUBSTRING CHECK. Each evidence_text field must be
   verifiable per its evidence_type. Only two types are allowed in
   the final output:
     - "verbatim_text" → must be a substring of the article text
       after Unicode-normalization (NFC), whitespace collapse, and
       PDF-hyphen-line-break dehyphenation
     - "structured_coordinates" → must resolve to a real table
       cell/coordinate via the article's parsed table structure

   Any other evidence form (paraphrased / "structured_summary") is
   rejected outright with skip_reason = paraphrase_evidence_not_allowed.
   The skip log records the paraphrased text so v2 can investigate
   safe handling.

   Gate D — VALUE NORMALIZATION CHECK. The adapter's parse_value runs;
   the result must satisfy:
     - value_canonical is a real number (NULL only if value_type is
       qualitative or boolean)
     - value_original appears in property_evidence_text (or table
       coord resolves to a cell with that value)
     - unit_original is on the adapter's accepted list
     - relation is in {"=", ">", "<", "≥", "≤", "~"}

   Gate E — DATA-ORIGIN CLASSIFIED. classify() must return a non-empty
   data_origin label.

   Gate F — DEDUPLICATION. Strong-key dedup over:
     (article_id, normalized_name, property_name, property_subtype,
      value_canonical ±DEDUP_VALUE_TOLERANCE (adapter-configurable;
      default 0.5 for mp/bp), relation, data_origin, instrument)
   Within-paper duplicates from table + inline collapse to one row.
   Different `instrument` or `relation` keep rows distinct
   (a DSC measurement and a capillary measurement of the same
   compound are two genuine data points; ">300" and "=300" are
   different).

   Rows failing any gate go to skipped_candidates.csv with the failing
   gate as skip_reason. Rows passing all gates go to the emission
   queue.

8. EMIT. scripts/emit_outputs.py writes draft files:
     output_draft.csv      — accepted rows (after gates)
     skipped.csv           — rejected candidates + skip reasons
     audit_log.json        — run metadata, gate stats
     extraction_notes.md   — narrative log of decisions per paper

9. COVERAGE CHECK. scripts/coverage_check.py runs BEFORE verification.
   Compares the candidate index against emitted/skipped rows. Warns
   if any of:
     - A paper with property keywords in the abstract emitted 0 rows
       AND skipped 0 candidates (a true silent miss)
     - A table whose headers match property-keyword triggers
       contributed 0 candidates to the index
     - An "N compounds were synthesized" claim in the abstract is
       more than 50 % above the emitted+skipped count
   Warnings go to audit_log AND expand the stratified-audit pool (all
   rows from warned papers get 100 % review).

10. VERIFY (§ 9). scripts/sample_for_verification.py picks:
     - random sample: 15 % of emitted rows
     - stratified high-risk pool: 100 % of rows with:
       - name_resolution_method ∈ {template_resolution,
         scheme_mapping, reviewer_approved_inference}
       - unit_original ≠ canonical_unit (conversion happened)
       - data_origin starting with predicted_
       - extraction_confidence ∈ {medium, low}
       - doi_verified = false
       - rows from PDF-only papers
       - rows from coverage-warned papers
     - overlap between random and stratified is counted once

    scripts/audit_verifier.py dispatches each sampled row to an
    independent verifier agent (see § 9b for the frozen prompt
    template and tooling).

11. QUARANTINE FAILED AUDITS. scripts/quarantine_failed_audits.py
    moves every row that failed audit from output_draft.csv to
    skipped.csv with skip_reason = failed_independent_audit:<reason>.
    The audit log records every move.

12. RECOMPUTE PASS RATE on the post-quarantine output.

    Edge case — empty sample: if the original verification sample
    is empty (no rows reached emission, OR all sampled rows were
    quarantined), the run does NOT auto-accept. Instead it is
    flagged `no_emission` or `all_audited_failed` for human review.
    These outcomes indicate a probable upstream problem (gates too
    aggressive, candidate enumeration too narrow, or systematic
    extraction failure) rather than a real-data scarcity.

    Normal case (sample_size > 0):
      pass_rate = (sample_size - quarantined_count) / sample_size
    - ≥ 98 % → run is `accepted`; output_draft.csv is renamed to
      output.csv and delivered.
    - < 98 % → run is `verification_failed`; output.csv is NOT
      produced. Human must investigate systematic causes (likely a
      gate gap) and re-run.

Every row in `output.csv` has:
 (a) passed Gates A–F,
 (b) appeared in the verification sample at the prescribed rate, OR
     was outside the sample but covered by the strata,
 (c) for those that were audited, been confirmed correct by an
     independent agent.

Audit-failed rows are never in `output.csv`. The 98 % threshold is on
the delivered output, not the original emission.
```

---

## 6. The standalone-name validator (Gate A)

`reference/name_validators.md` defines the rules. Implementation in
`scripts/validate_name.py`. **All pattern matching uses
`re.IGNORECASE`.**

A name is **rejected** if any REJECT_PATTERN matches:

```python
import re
FLAGS = re.IGNORECASE

REJECT_PATTERNS = [
    # --- Section titles / prose fragments ---
    r"^(?:results?\s+and\s+discussion|introduction|experimental|methods?)$",
    r"^(?:synthesis|preparation|general\s+procedure)\b",
    r"^the\s+(?:precursors?|compound|product|minor|main)",
    r"^(?:halogen|aldehyde|amine|phenol)-release\s+biocides?",
    r"^(?:characterization|spectral\s+data|analytical\s+data)",

    # --- Bare codes / local labels ---
    r"^compound\s+\d+[a-z]?$",            # "compound 3"
    r"^complex\s+\d+[a-z]?$",             # "complex 9"
    r"^\d+[a-z]?$",                       # just "4a"

    # --- Generic derivative labels ---
    r"\bderivative\s*\d*[a-z]?\s*$",      # "benzoxanthenone derivative 4b"
    r"\bcomplex\s+of\s+compound\s+\d",    # "Pb(II) complex of compound 4"

    # --- Unresolved template variables ---
    r"\bX\s*=\s*[A-Za-z0-9]",             # "X=Cl", "X=H"
    r"\(\s*X\s*=",
    r"\bR\s*=\s*[A-Za-z0-9]",
    r"\(\s*R\s*=",
    r"R\d+\s*=",                          # "R1=H"

    # --- Range labels / plural series ---
    r"\bcompounds?\s+\d+\s*[-–]\s*\d+",   # "compounds 33-50"
    r"^[A-Z]\w+s\s+\d+[-–]\d+",           # "Oximes 33-50"

    # --- Empty ---
    r"^\s*$",
]
# Note: the original "^.{1,3}$" reject pattern is dropped — it would
# block valid short names ("TNT", "DDT", "MBT", "BHA"). Short-name
# safety is handled by EXEMPT_NAMES and adapter EXTRA_EXEMPT_NAMES.
```

A name passes only if **no REJECT_PATTERN matches** AND at least one of
the following holds:

```python
REQUIRE_PATTERNS = [
    # --- Chemistry-bearing tokens (organic) ---
    r"(?:yl|oxy|amine|amino|acid|ester|amide|nitrile|thione|thiol|"
    r"alcohol|phenol|phenyl|methyl|ethyl|hydroxy|naphthal|benzo|"
    r"pyrid|pyrim|thiadiazol|oxadiazol|triazol|imid|sulfanyl|"
    r"sulfonyl|sulfonate|sulfate|phosphate|nitrate|carbox|carbonyl|"
    r"piperidin|piperazin|morpholin|oxazol|furan|thiophen|indol|"
    r"quinolin|xanthen|chromen)",

    # --- IL / salt shorthand: [...][...] ---
    r"\[[^\]]+\]\[[^\]]+\]",

    # --- IUPAC stereodescriptors indicate this is a real chemical name ---
    r"\b(?:rac|cis|trans|R|S|E|Z|α|β)-",

    # --- Inorganic / coordination compound patterns ---
    r"(?:hydrate|hydrochloride|chloride|bromide|iodide|fluoride|"
    r"oxide|sulfide|nitride|carbonate)\b",
    r"\b[A-Z][a-z]?(?:O|S|N|Cl|Br|I|F)\d*\b",  # e.g. CuO, NaCl

    # --- Polymer / material patterns ---
    r"\b(?:poly|co-poly|block-poly)\w+",
]

# A common-name lexicon for compounds that don't match any pattern above
EXEMPT_NAMES = {
    # Organic small molecules
    "acetone", "acetonitrile", "methanol", "ethanol", "isopropanol",
    "water", "benzene", "toluene", "xylene", "chloroform", "ether",
    "tetrahydrofuran", "thf", "dmf", "dmso", "nmp", "dichloromethane",
    "dcm", "ethyl acetate", "hexane", "heptane", "pentane",
    # APIs / drugs from the audit corpus
    "chloroquine", "hydroxychloroquine", "dexamethasone", "thalidomide",
    "favipiravir", "fingolimod", "umifenovir", "baricitinib", "camostat",
    "ibuprofen", "acetylsalicylic acid", "aspirin",
    # Industrial / biocide names
    "glutaraldehyde", "bronopol", "dazomet", "tcmtb", "bhap", "mbt",
    "bcdmh", "dbnpa",
    # Halocarbons (common short names)
    "ddt", "ddd", "pcb", "tnt", "rdx", "hmx",
    # Natural products
    "dehydrocholic acid", "tyrindoleninone", "tyrindolinone",
}
# Adapters extend this via EXTRA_EXEMPT_NAMES.
```

A name passes only if it (a) matches no REJECT_PATTERN AND (b) matches
at least one REQUIRE_PATTERN OR is in EXEMPT_NAMES ∪
adapter.EXTRA_EXEMPT_NAMES.

Adapters can additionally specify `EXTRA_REJECT_PATTERNS` (compiled
into the same FLAGS regex set) and `EXTRA_REQUIRE_PATTERNS`. The
loader merges these with the core patterns.

Failed names get `skip_reason = name_not_standalone:<which_rule>` and
go to `skipped.csv`. They are **never** placed in the final output CSV
under a sentinel label.

---

## 7. Identity-token consistency + evidence substring (Gates B and C)

These are the most important precision gates. They catch the Claude
paper 011 #5d benzonitrile/benzoic-acid error and most of GPT's
section-title-as-name errors.

### 7a. Identity-token consistency (Gate B)

`scripts/identity_token_check.py`. Bidirectional, position-aware
identity-token consistency. Broader than just functional groups.

```python
import re

# Identity-bearing substring tokens, organized by category. Used by
# the forward and reverse checks. Locants are NOT in this dict; they
# are handled by a separate regex-based function below.
IDENTITY_TOKENS = {
    # Functional-group suffixes
    "fg": ["nitrile", "acid", "ester", "amide", "amine", "alcohol",
           "ether", "ketone", "aldehyde", "phenol", "sulfonate",
           "sulfanyl", "sulfonyl", "sulfide", "thione", "thiol",
           "oxide", "imine", "imide", "carboxyl", "carboxamide",
           "carbamate", "carbonyl"],

    # Substituent prefixes (identity-changing)
    "subst": ["fluoro", "chloro", "bromo", "iodo", "nitro", "methoxy",
              "ethoxy", "hydroxy", "amino", "cyano", "trifluoromethyl",
              "phenoxy", "methylthio", "acetyl", "carboxy",
              "methylenedioxy"],

    # Heterocycle stems
    "het": ["pyridazin", "pyrimidin", "thiadiazol", "oxadiazol",
            "triazol", "imidazol", "thiazol", "pyrrol", "furan",
            "thiophen", "naphthalen", "indol", "quinolin",
            "isoquinolin", "xanthen", "chromen", "piperidin",
            "piperazin", "morpholin", "oxazol"],

    # Salt / hydrate / coordination descriptors
    "form": ["hydrate", "hydrochloride", "sulfate", "acetate",
             "nitrate", "phosphate", "methanesulfonate", "tosylate",
             "chloride", "bromide", "iodide", "fluoride", "oxide",
             "carbonate"],

    # Stoichiometric / counterion identifiers
    "stoich": ["bis", "tris", "tetra", "penta", "hexa", "di", "tri",
               "tetrakis"],
}

# Locant + substituent pattern: a digit-(or comma-separated digits-)
# hyphenated prefix immediately followed by a known substituent or
# heterocycle token. Examples: "6-chloro", "3,5-dimethyl", "2-amino".
_LOCANT_TOKEN_RE = re.compile(
    r"\b(?P<locant>\d+(?:,\d+)*)-(?P<token>[a-z]+)",
    re.IGNORECASE,
)

def _extract_locant_pairs(text):
    """Return a set of (locant, token) tuples found in text."""
    pairs = set()
    for m in _LOCANT_TOKEN_RE.finditer(text.lower()):
        locant = m.group("locant")
        token = m.group("token")
        pairs.add((locant, token))
    return pairs

def _locant_consistency(compound_name, local_evidence_text):
    """For every (locant, token) pair in compound_name, the SAME pair
    must appear in the local evidence window. For every pair in the
    local evidence whose `token` is in any IDENTITY_TOKENS category,
    the SAME pair must appear in compound_name.

    Returns (ok: bool, mismatches: list[(direction, locant, token)]).
    """
    name_pairs = _extract_locant_pairs(compound_name)
    evid_pairs = _extract_locant_pairs(local_evidence_text)

    all_identity_tokens = {t for cat in IDENTITY_TOKENS.values() for t in cat}

    mismatches = []
    # Forward: every locant pair in name must be in evidence
    for locant, token in name_pairs:
        if (locant, token) not in evid_pairs:
            # Tolerate when the same token appears in evidence with a
            # different locant: that's the actual disagreement to flag
            matching_in_evid = [p for p in evid_pairs if p[1] == token]
            if matching_in_evid:
                mismatches.append(("forward_locant_disagrees", locant, token))
            else:
                # Token simply isn't locant-tagged in the evidence —
                # handled by the main forward identity-token check
                pass
    # Reverse: identity tokens in evidence with locants must match name
    for locant, token in evid_pairs:
        if token in all_identity_tokens and (locant, token) not in name_pairs:
            matching_in_name = [p for p in name_pairs if p[1] == token]
            if matching_in_name:
                mismatches.append(("reverse_locant_disagrees", locant, token))
            # else: the token isn't in the name at all — the main reverse
            # check flags that

    return (len(mismatches) == 0, mismatches)


def identity_token_consistency(compound_name, compound_evidence_text,
                                property_evidence_text,
                                name_position_in_compound_evidence):
    """Bidirectional + position-aware identity-token check.

    Forward: every category token in compound_name must appear in the
             evidence union.
    Reverse: every category token in compound_evidence_text within
             ±60 chars of the compound-name occurrence must also
             appear in compound_name.
    Locants:  paired (locant, token) tuples must agree between name
             and the local evidence window.

    name_position_in_compound_evidence is the integer offset where
    compound_name starts inside compound_evidence_text. It is set by
    scripts/resolve_compound_name.py when the row is built; the
    pipeline guarantees this position is non-None for every row that
    reaches Gate B.
    """
    name = compound_name.lower()
    evid_full = (compound_evidence_text + " " + property_evidence_text).lower()

    start = max(0, name_position_in_compound_evidence - 60)
    end = name_position_in_compound_evidence + len(compound_name) + 60
    local_evid = compound_evidence_text[start:end].lower()

    forward_missing = {}
    reverse_missing = {}
    for category, tokens in IDENTITY_TOKENS.items():
        name_tokens = {t for t in tokens if t in name}
        evid_tokens = {t for t in tokens if t in evid_full}
        local_evid_tokens = {t for t in tokens if t in local_evid}
        forward_gap = name_tokens - evid_tokens
        if forward_gap:
            forward_missing[category] = list(forward_gap)
        reverse_gap = local_evid_tokens - name_tokens
        if reverse_gap:
            reverse_missing[category] = list(reverse_gap)

    locant_ok, locant_mismatches = _locant_consistency(compound_name, local_evid)

    return (
        len(forward_missing) == 0 and len(reverse_missing) == 0
        and locant_ok,
        {"forward": forward_missing,
         "reverse": reverse_missing,
         "locants": locant_mismatches}
    )
```

If the check returns `False` → reject row with
`skip_reason = identity_token_mismatch:<direction>:<category>:<tokens>`.

The forward check catches the Claude 5d case: name has "nitrile"
but evidence (which contains "benzoic Acid") has "acid". Forward
gap: `{"fg": ["nitrile"]}`. Reject.

The reverse check catches the case where the evidence says
"6-chloro-…-thione" but the name omits "6-chloro": evidence local
tokens has "chloro", name does not. Reverse gap: `{"subst": ["chloro"]}`.

The locant check catches the case where positions disagree (e.g.,
name says "4-chloro", evidence says "6-chloro").

### 7b. Evidence substring check (Gate C)

`scripts/verify_substring.py`.

```python
def normalize_for_substring_match(text):
    """Apply NFC Unicode, whitespace collapse, and PDF-hyphen-line-break
    dehyphenation."""
    import unicodedata
    text = unicodedata.normalize("NFC", text)
    # Dehyphenate line breaks: "hydroxy-\nnaphthalen" → "hydroxynaphthalen"
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def evidence_is_in_article(evidence_text, evidence_type, article_full_text,
                           article_table_lookup):
    if evidence_type == "verbatim_text":
        e = normalize_for_substring_match(evidence_text)
        a = normalize_for_substring_match(article_full_text)
        return e in a
    if evidence_type == "structured_coordinates":
        return article_table_lookup.has(evidence_text)
    # No other evidence_type is allowed to reach Gate C: anything not
    # in {verbatim_text, structured_coordinates} is rejected by the
    # adapter/resolver upstream with skip_reason =
    # paraphrase_evidence_not_allowed.
    return False
```

If any required evidence text fails verification → reject row with
`skip_reason = evidence_not_in_article:<which_field>`.

---

## 8. Property adapter contract

Each property adapter is a directory under `properties/` containing
**both** a Python module (for extraction logic) and a YAML declaration
(for triggers and units). Python for logic, YAML for declarative data.

### 8a. `adapter.py` — logic

```python
# properties/{name}/adapter.py

PROPERTY_NAMES = ["melting_point", "boiling_point"]   # one or more
CANONICAL_UNIT = "°C"                                  # adapter's canonical
PROPERTY_SUBTYPES = ["melt", "decomp", "melt_or_decomp", "boil",
                     "DSC_onset", "DSC_peak", "sublimation"]
DATA_ORIGINS = ["measured_by_article", "literature_cited",
                "predicted_<method>"]
EXTRA_EXEMPT_NAMES = {"glutaraldehyde", "dehydrocholic acid",
                      "tyrindoleninone", "tyrindolinone"}
EXTRA_REJECT_PATTERNS = []  # adapter-specific name rejects
EXTRA_REQUIRE_PATTERNS = []
DEDUP_VALUE_TOLERANCE = 0.5                            # °C, adapter-defined

def find_candidates(article):
    """Enumerate all property-relevant mentions. Apply exclusion_triggers
    from triggers.yaml at this stage so Tg/RMSE/etc. don't enter.

    Yields dicts:
      {
        "candidate_id": str,
        "raw_value_text": str,
        "unit_text": str | None,
        "nearby_compound_handle": str,  # code or verbatim name
        "compound_handle_position": int,  # char offset of the handle
                                          # within the article's full text
                                          # (used downstream for position-
                                          # aware identity-token check —
                                          # see § 7a)
        "property_trigger": str,
        "source_type": "paragraph" | "table" | "caption" | "supplementary",
        "evidence_location": str,
      }
    """
    ...

def parse_value(raw_value_text, unit_text, adapter_context=None):
    """Return:
      {value_type, value_canonical, value_canonical_min, value_canonical_max,
       value_text, value_original, unit_original, relation}
    Handles °C / K / °F, ranges (123-125 → midpoint 124), inequalities
    (>250 → 250 with relation ">"), (dec.) annotations, ~/≈
    (approximately)."""
    ...

def classify(candidate, article_context):
    """Return (data_origin, property_subtype, instrument).
    For mp/bp:
      - 'mp 245 (dec.)' → property_subtype = "melt_or_decomp"
      - 'Te' from DSC subsequent cycles → "DSC_onset"
      - table column 'experimental Tfus' → "measured_by_article"
      - table column 'calculated' → "predicted_<method>"
    """
    ...
```

### 8b. `triggers.yaml` — declarative data

```yaml
property_family: melting_boiling_points
canonical_unit: "°C"
accepted_units:                # normalized unit identifiers
  - "°C"
  - "C"                        # bare 'C' is normalized to °C
  - "K"
  - "°F"
  - "F"

unit_conversion:
  K: "value - 273.15"
  "°F": "(value - 32) * 5/9"
  F: "(value - 32) * 5/9"
  C: "value"
  "°C": "value"

property_triggers:
  paragraph:
    - "mp"
    - "m.p."
    - "Mp"
    - "M.p."
    - "melting point"
    - "Tm"
    - "Tfus"
    - "T_fus"
    - "bp"
    - "b.p."
    - "Bp"
    - "B.p."
    - "boiling point"
    - "Tb"
  table_headers:
    - "Mp"
    - "M.p."
    - "Mp (°C)"
    - "Tm"
    - "Tfus"
    - "Bp"
    - "T_b"
    - "boiling point"

exclusion_triggers:    # these should NOT be extracted
  - "Tg"
  - "glass transition"
  - "Tc"
  - "crystallization temperature"
  - "RMSE"
  - "mean error"
  - "MAE"
  - "MAPE"

data_origin_patterns:
  measured_by_article:
    - "was determined on"
    - "measured by DSC"
    - "found"
    - "observed"
  literature_cited:
    - "lit."
    - "literature"
    - r"\[\d+\]"      # citation marker near value
  predicted_calculated:
    - "calculated by"
    - "predicted"
    - "estimated"
    - "STRM"
    - "SIRM"

relation_triggers:    # phrases that map to a non-default relation
  approximate:
    - "approximately"
    - "approx."
    - "ca."
    - "~"
    - "≈"
    - "about"          # only when adjacent to a numeric value
  greater_than:
    - ">"
    - "more than"
    - "above"          # only when adjacent to a value with units
  less_than:
    - "<"
    - "less than"
    - "below"

instruments:
  - "DSC"
  - "Mettler"
  - "Gallenkamp"
  - "Stuart"
  - "Büchi"
  - "Reichert"
  - "capillary"
```

### 8c. Adding a new property

1. Create `properties/<new_name>/`.
2. Copy the `example_new_property` template; fill in property-specific
   logic.
3. Write `adapter.md` documenting the property's idioms.
4. Drop 1–2 papers with known expected outputs into
   `properties/<new_name>/golden_tests/`.
5. Build a **held-out corpus for this adapter** at
   `tests/held_out/<new_name>/` — at least 10 papers with manually
   verified ground-truth annotations. This is **separate from**
   `tests/held_out/mp_bp/`; § 12.5's held-out set is mp/bp-specific.
6. Run the adapter-conformance test (§ 12.7).
7. Run the held-out validation on the adapter's own held-out corpus
   (§ 12.5 procedure, scoped to this adapter). The new adapter
   cannot be released without ≥ 98 % audit pass rate on its
   held-out set.

---

## 9. Verification protocol

### 9a. Automated row validator

`scripts/validate_row.py` runs deterministic checks on every emitted
row.

**Hard-fail checks** (row rejected, moved to skipped.csv):

| Check | Fails row if |
|---|---|
| DOI is present | empty |
| DOI matches regex `^10\.\d{4,9}/.+$` | malformed |
| compound_name passes Gate A | matches REJECT_PATTERN |
| compound_evidence_text is in article (Gate C) | not a substring / not a valid coord |
| property_evidence_text is in article (Gate C) | same |
| identity-token check passes (Gate B, bidirectional + position-aware) | any category has gaps |
| value type consistent: if value_canonical NULL, value_text non-NULL; else inverse | inconsistent |
| value_canonical, canonical_unit valid (for numeric properties) | NaN, wrong unit |
| value_original appears in property_evidence_text | not present |
| relation in allowed set | invalid value |
| data_origin classified | empty |
| extraction_confidence ≤ name_resolution_confidence | confidence inversion |
| no duplicate under Gate F key | duplicate found |

**Soft-flag checks** (row kept, added to stratified audit pool):

| Check | Adds row to audit pool if |
|---|---|
| name_resolution_method ∈ {template_resolution, scheme_mapping, reviewer_approved_inference} | true |
| doi_verified = false | true |
| unit conversion happened | unit_original ≠ canonical_unit |
| extraction_confidence ∈ {medium, low} | true |

### 9b. Random sample + stratified audit

`scripts/sample_for_verification.py`:

- **Random sample**: 15 % of emitted rows, sampled with a fixed seed
  for reproducibility.
- **Stratified high-risk pool** (100 % review):
  - Every soft-flag row from § 9a
  - All rows from coverage-warned papers (§ 5 step 9)
  - All rows from PDF-only papers
  - All rows with `data_origin` starting with `predicted_`
  - Minimum: if the stratified pool has < 10 rows total, draw an
    additional random sample to bring the total audit pool to ≥ 30

`scripts/audit_verifier.py` dispatches each sampled row to an
independent verifier agent. Tooling:
- Each row gets a fresh subprocess / agent instance.
- The verifier sees ONLY: the row being verified, the article files
  (NXML/PDF/text) **read-only**, and the **frozen prompt template**
  (`reference/verifier_prompt.md`).
- The verifier does NOT see any extraction-pipeline state, validator
  decisions, or the audit log.
- Verifier reproducibility:
    - The verifier LLM is run with `temperature = 0` and a fixed
      seed where the provider supports it.
    - The seed for each verification is derived from
      `(row_id, run_id)` so the same row→verifier pairing produces
      the same verdict.
    - Providers that don't support deterministic seeding are
      flagged in `audit_log.json`; the run can still proceed but
      stratified-audit results carry a `nondeterministic_verifier`
      marker.

**Verifier sanity check**: at the start of each verification batch,
the harness runs the verifier against a small held-out set of
known-correct AND known-wrong synthetic rows (kept in
`reference/verifier_sanity_set.json`). If the verifier doesn't
correctly classify the sanity set within tolerance (e.g., ≥ 9/10
correct), the whole batch is aborted with
`reason = verifier_unreliable`; the user investigates the verifier
configuration before any rows are quarantined. This prevents a
broken verifier from silently quarantining good rows.

**The frozen verifier prompt** (saved as `reference/verifier_prompt.md`):

```
You are an independent verifier for a property-extraction skill. You
will be given:
- One CSV row claiming a property value extracted from a paper
- The full text of the source paper

Your job: confirm or refute each claim INDEPENDENTLY. Do not trust the
row's own evidence_text — locate the value yourself in the paper.

For each row, answer six questions with Yes/No/Cannot-determine + a
one-sentence reason:

1. Does `value_original` (or its midpoint) actually appear at the
   stated source_section / evidence_location?
2. Is `compound_name` a standalone chemical identity (would a chemist
   identify it from the name alone)?
3. Do compound_name's identity-bearing tokens (functional groups,
   substituents, positions, heterocycles) match what the paper says
   about that compound — both forward (every name token in evidence)
   and reverse (no evidence token contradicting the name)?
4. Is `data_origin` correct (measured by paper, cited from literature,
   or predicted)?
5. Is `property_subtype` consistent with the paper's description
   (mp vs Tg vs DSC_onset etc.)?
6. Is the DOI correct (matches the paper's actual DOI as stated in
   front matter or DOI metadata)?

A row PASSES only if all six are Yes. Any No or Cannot-determine fails
the row.

Return JSON: {"q1": "Yes/No/Cannot-determine", "q1_reason": "...",
              "q2": ..., ..., "verdict": "pass" | "fail"}.
```

This prompt is locked. Changing it requires bumping the verifier
prompt version, which invalidates earlier audit results.

### 9c. Quarantine and re-compute

`scripts/quarantine_failed_audits.py`:
- Moves every audited row with `verdict = fail` from `output_draft.csv`
  to `skipped.csv`, with `skip_reason = failed_independent_audit:
  q<N>_<reason>`.
- The remaining `output_draft.csv` is the candidate for delivery.

The pass rate is **recomputed on the post-quarantine sample**:

```
pass_rate = (sample_size - quarantined_count) / sample_size
```

If `pass_rate ≥ 0.98` → run is `accepted`; rename `output_draft.csv`
to `output.csv`.
If `pass_rate < 0.98` → run is `verification_failed`; do not deliver
`output.csv`. Human investigates whether failures are systematic
(fix a gate) or one-off (move to skipped, re-run). The 98 % gate
applies to delivered output, not to the original emission, and is
measured on the held-out corpus (not the dev corpus the gates were
tuned against — see § 12.5).

### 9d. Scoring rules

A row counts as **wrong** (and is quarantined) if any of these are
wrong or unverifiable:
- compound name correctness (must be standalone + chemically right)
- property value correctness
- unit / conversion correctness
- property classification correctness (mp vs bp vs Tg, etc.)
- DOI / article correctness
- evidence sufficiency for independent verification

Cleanup-only issues (trailing local labels, citation marks) count as
**wrong** when they make the final table less standalone or less
useful. The 98 % threshold applies to this strict definition.

---

## 10. Scope policy

The skill resolves the four prior-extraction scope disagreements by
**always extracting and tagging**, then letting the consumer filter.
This was the user's chosen default.

| Scope question | Default policy | Run-config flag |
|---|---|---|
| Open-bound values (`>X`, `<X`) | Emit with `value_canonical = X`, `relation = ">"` or `<`. `value_original` keeps the inequality string. | **Always emitted, including in `--strict` mode.** Open bounds are real data; the `relation` field is what consumers filter on. |
| Predicted / calculated values | Emit with `data_origin = predicted_<method>`. | `--include-predicted true` (default); `--strict` turns this off |
| Literature-cited values from another paper | Emit with `data_origin = literature_cited`. | `--include-cited true` (default); `--strict` turns this off |
| Paraphrased evidence | **Always skipped.** No flag admits paraphrased evidence into the final output in v1. Recorded in skipped.csv as a v2 recall opportunity. | n/a |
| Table cell that's an image (no text) | Skip with `compound_identity_graphical_only`. | OCR fallback is a v2 TODO |
| Supplementary-information files | **Not consulted in v1.** Skipped with `data_in_supplementary_only`. | OCR / SI-parser is a v2 TODO |

**Recommended run-config presets** (`reference/run_config.md`):

```
strict   = --measured-only (turns off include-predicted and
                            include-cited; open bounds remain on)
default  = include-predicted + include-cited; open bounds emitted
review   = same as default; intended for downstream review
           workflows that consume the audit_log alongside output.csv
```

The `--strict` preset is **the recommended setting for high-
verifiability final tables**. It produces measured + cited
experimental values only, plus open bounds (which are real
measurements with a known direction). The default is permissive
because the user prefers extracting everything and filtering on
read; users who want the most conservative behavior should pass
`--strict` and ship that to downstream consumers. The emitted-vs-
skipped split is preserved in `audit_log.json` so policy decisions
are reversible without re-running the extractor.

---

## 11. Phased build plan

Each phase delivers a working, testable artifact before the next phase
depends on it. Failure-mode tags from § 1 are on the phase that
addresses them.

### Phase 1 — Source ingestion + DOI verification (no extraction yet)
- Implement `scripts/ingest_article.py` for NXML, plain text, and
  dual-mode pdftotext.
- Implement `scripts/verify_doi.py` (cross-source DOI validation).
- Define the article-object structure.
- Acceptance: parse all 20 papers in `mp_bp_dev_set`; produce
  diagnostic dumps (section count, table count, DOI sources + match
  status, text length). Manually verify on 3 papers.

### Phase 2 — Candidate enumeration (F5)
- Implement `scripts/build_candidate_index.py` and the mp/bp adapter's
  `find_candidates()` + `triggers.yaml`.
- Run on all 20 papers; produce candidate index.
- Acceptance: per-paper candidate count matches expected (golden test
  § 12.2). Dearden Table 2 contributes ~196 candidates; paper 020
  contributes ≥ 39 candidates.

### Phase 3 — Identity resolution (F2, F3, F4)
- Implement `scripts/build_label_dictionary.py`,
  `scripts/resolve_template_variables.py`,
  `scripts/resolve_compound_name.py`.
- Implement Gate A (standalone-name validator).
- Acceptance: paper 020 #3 resolves via label dictionary to
  `2-(3-Methoxybenzyloxy)isoindolin-1,3-dione`. Paper 050 resolves
  `X = 6-Cl`. Reject patterns correctly reject the GPT failures.

### Phase 4 — Acceptance gates + first full output (F1, F6, F7, F8)
- Implement Gates B (identity tokens, bidirectional + position-aware),
  C (substring; paraphrased evidence categorically rejected),
  D (value), E (origin), F (dedup with tightened key).
- Implement `scripts/normalize_value.py`,
  `scripts/classify_data_origin.py`, `scripts/dedup.py`.
- Implement `scripts/emit_outputs.py`.
- Acceptance: regression tests for the 8 failure modes (§ 12.3)
  all pass. Claude 5d benzonitrile error caught by Gate B.

### Phase 5 — Verification harness
- Implement `scripts/validate_row.py`,
  `scripts/sample_for_verification.py`,
  `scripts/audit_verifier.py`,
  `scripts/quarantine_failed_audits.py`,
  `scripts/coverage_check.py`.
- Freeze `reference/verifier_prompt.md`.
- Acceptance: harness self-tests (§ 12.7) pass. Pass rate on dev
  corpus measured.

### Phase 6 — End-to-end pass-rate on dev corpus
- Full run on all 20 papers in `mp_bp_dev_set` with all gates active.
- Random sample + stratified pool verified by independent agent.
- Acceptance: ≥ 98 % pass rate on the dev corpus. If lower → identify
  systematic causes, iterate on gates.

### Phase 6.5 — **Held-out corpus validation** (overfitting check)
- All concrete validators, FG tokens, golden tests, and regression
  tests were tuned against `mp_bp_dev_set`. To detect overfitting,
  run the full pipeline against the **user's larger paper corpus**
  (from which `mp_bp_dev_set` was sampled), using a held-out subset
  not seen during development.
- Suggested held-out size: 30+ fresh papers across the same property
  family, ideally spanning the diversity dimensions in the dev set
  (different journals, decades, table-heavy vs prose-heavy).
- Acceptance: ≥ 98 % pass rate on the held-out corpus. **This is the
  real precision measurement; the dev-corpus pass rate is a training
  metric and could be misleadingly high.**
- If held-out fails: a gate is overfit to dev. Diagnose, generalize
  the gate, re-run.

### Phase 7 — Extension validation
- Implement a second adapter (e.g., `properties/log_p/`) using the
  example template.
- Add 2 log P papers to a `log_p_dev_set/`.
- Acceptance: log P adapter runs end-to-end without changes to any
  scripts in `scripts/`. Same gates apply. Same verification
  protocol applies.

### Phase 8 — v2 / TODO backlog
- Items from `reference/todo.md` (§ 13) get prioritized and worked
  off here.

---

## 12. Tests and evals

A thorough test/eval plan in eleven layers. All tests under `tests/`,
run via `pytest`.

### 12.1 Unit tests — per script

For every script in `scripts/`, a `tests/unit/test_<script>.py` with at
minimum:

- **ingest_article.py**: parse a known-good NXML; parse a known-good
  PDF; parse a malformed NXML and fail gracefully; extract DOI from
  each available source location.
- **verify_doi.py**: two sources agree → verified; one source → not
  verified, capped confidence; sources conflict → audit-log warning.
- **build_candidate_index.py**: known input → expected candidate count
  with all required fields populated; exclusion_triggers correctly
  filter out Tg/RMSE.
- **build_label_dictionary.py**: each of the six code→name patterns
  produces a correct dictionary entry; ambiguous codes flagged.
- **resolve_template_variables.py**: paper 050's "6-chloro" prose →
  `X = (Cl, 6)`.
- **resolve_compound_name.py**: each `name_resolution_method` path
  produces the right name; verbatim-name-wins-over-code precedence
  enforced.
- **validate_name.py**: each REJECT_PATTERN unit-tested with positive
  and negative cases (with `re.IGNORECASE` confirmed); each
  REQUIRE_PATTERN same; EXEMPT_NAMES correctly admits otherwise-
  rejected short names.
- **identity_token_check.py**: forward check (name → evidence), reverse
  check (evidence → name), position-aware locant check; positive and
  negative cases; the Claude 5d case (forward miss on `nitrile`); the
  "6-chloro" reverse miss case.
- **verify_substring.py**: verbatim text in article → pass; not in
  article → fail; structured_coordinates → looked up in table; NFC
  Unicode normalization works; PDF hyphen-line-break dehyphenation
  works; any non-allowed evidence_type returns False.
- **normalize_value.py**: ranges, inequalities (`>`, `<`),
  approximate (`≈`, `~`), Kelvin / °F conversion, sign
  reconstruction (pdftotext `2141.8` from `-raw` mode → `-141.8`),
  qualitative values (`"red crystals"` → `value_type = "qualitative"`).
- **classify_data_origin.py**: measured / cited / predicted patterns
  each triggered correctly; "lit." triggers cited.
- **dedup.py**: same compound + value from table and inline collapses;
  different instrument keeps rows distinct; `>300` and `=300` kept
  distinct (different relation).
- **coverage_check.py**: known under-extracted paper triggers warning;
  warning expands the audit pool.
- **sample_for_verification.py**: same seed → same sample (random);
  stratified pool catches all soft-flag rows; overlap counted once.
- **audit_verifier.py**: verifier prompt template loaded correctly;
  verifier subprocess gets the right inputs and no extra state.
- **quarantine_failed_audits.py**: failed rows moved correctly; pass
  rate recomputed correctly.
- **validate_row.py**: hard-fail checks each unit-tested; soft-flag
  checks add to audit pool.
- **emit_outputs.py**: CSV well-formed, all required columns,
  encoding correct.
- **adapter_loader.py**: typo in `triggers.yaml` raises a clear error;
  missing function in adapter.py raises; adapter with invalid
  CANONICAL_UNIT raises.

### 12.2 Golden corpus tests — `mp_bp_dev_set`

A `tests/golden/` directory with **expected per-paper outputs** for all
20 papers. Each paper has:

- `expected_candidates.csv` — what should appear in the candidate index
- `expected_emitted.csv` — what should appear in `output.csv` after
  all gates AND audit quarantine
- `expected_skipped.csv` — what should appear in `skipped.csv` with
  which `skip_reason`

Updated paper 020 expected outputs (correcting the inconsistency from
the original v1 proposal):

```
expected_candidates:  39 rows
expected_emitted:     39 rows  (no open-bound skips —
                                 open bounds emit with relation=">")
                                 ← was incorrectly listed as 34 in v1
expected_skipped:      0 open-bound skips
                       Possibly 0–1 rows skipped for other gates;
                       per-row details in tests/golden/020_expected.csv
```

The golden tests verify the full pipeline end-to-end. Open-bound rows
appear in `expected_emitted` with `relation = ">"` (not in
`expected_skipped`), consistent with the § 10 policy.

### 12.3 Failure-mode regression tests

One test per F1–F8 mode, each based on the actual cases that bit
Claude or GPT in this study:

| Test | Description | Expected pipeline behavior |
|---|---|---|
| F1_5d_benzonitrile | Construct a synthetic row for paper 011 #5d with the wrong name "...benzonitrile" but the correct evidence "...benzoic Acid". Feed to Gate B. | Gate B (forward identity-token check) rejects with `identity_token_mismatch:forward:fg:nitrile`. |
| F2_section_title | Feed `compound_name = "Result and discussion"` | Gate A rejects with `name_not_standalone:section_title`. |
| F3_local_only | Feed paper 020 #3 candidate with raw name "compound 3" | Resolver looks up label dict; resolves to `2-(3-Methoxybenzyloxy)isoindolin-1,3-dione (3)`. Emit. |
| F4_template | Feed paper 050 candidate with raw name `(X=Cl, R=4-CH3)` | Resolver runs template-variable expansion via prose scan; finds `X = 6-Cl`; emits `6-chloro-3-(4-methylphenyl)-2-methylquinazoline-4(3H)-thione`. |
| F5_dearden_table | Run candidate enumeration on the Dearden PDF | Candidate index contains ≥ 196 entries; coverage check shows no warning. |
| F6_duplicate | Feed two rows with same compound + value, one from table, one from inline characterization, same DSC instrument | Dedup collapses to one row. |
| F6b_distinct | Feed two rows with same compound + value but one is DSC and other is capillary | Both rows kept (different `instrument`). |
| F7_open_bound | Feed `>300 °C` value | Emitted with `value_canonical = 300`, `relation = ">"`. Not skipped. |
| F8_paper_jargon | Feed `compound_name = "acetone (pure guest AC)"` | Name validator strips parenthetical; final name = "acetone" (in EXEMPT_NAMES). Local context preserved in compound_label. |

### 12.4 Schema integrity tests

- All required columns present in `output.csv`.
- No null values in required columns.
- Numeric rows: `value_canonical` parseable as float;
  `value_text` is NULL.
- Qualitative rows: `value_text` is non-empty; `value_canonical` is
  NULL.
- `canonical_unit` is consistent within a single property.
- `relation` is in the allowed set (`=`, `>`, `<`, `≥`, `≤`, `~`,
  where `≈` is normalized to `~` on input).
- `data_origin` is in the allowed set.
- `name_resolution_method` is in the allowed set.
- `extraction_confidence ≤ name_resolution_confidence`.
- DOI matches `^10\.\d{4,9}/.+$`.
- `evidence_type` values are in `{verbatim_text,
  structured_coordinates}` in delivered output (no `structured_summary`
  unless flagged).
- All emitted rows have passed all gates AND survived audit
  quarantine (no row has `skip_reason != null` AND appears in
  output.csv).

### 12.5 Held-out corpus tests (the real precision measurement)

A `tests/held_out/` directory containing **a different paper corpus**
than `mp_bp_dev_set`. Drawn from the user's larger paper set, from
which `mp_bp_dev_set` was originally sampled. Suggested size: ≥ 30
papers.

**Ground-truth source**: per-paper expected outputs in
`tests/held_out/<adapter>/<paper>.expected.csv` are produced by
**manual annotation by a qualified reviewer**. The annotation is
the gold standard the verifier compares against. (A second
independent annotator on a subset is recommended to catch
annotator disagreements; differences are resolved by adjudication
before locking the expected file.) The cost of building ground
truth is real but unavoidable — without it the 98 % target is not
operationalizable.

- The held-out papers are **never inspected during gate design or
  golden-test writing**.
- Phase 6.5 runs the full pipeline + verification harness on this
  corpus.
- Acceptance: ≥ 98 % audit pass rate on held-out (post-quarantine).
- If held-out passes but dev fails → still a problem (the dev golden
  tests are wrong).
- If dev passes but held-out fails → overfitting; a gate or pattern
  is too narrow. Diagnose, generalize, re-run.

Each adapter has its own held-out corpus under
`tests/held_out/<adapter>/`. The mp/bp corpus is the reference set;
new adapters cannot release without their own held-out corpus
(see § 8c).

This is the test that actually proves the 98 % target. The dev-corpus
tests are necessary for fast iteration but cannot stand alone.

### 12.6 Cross-property modularity tests

Add a stub `properties/log_p/` adapter with minimal triggers and
verify:

- Core scripts in `scripts/` import the adapter without modification.
- A test paper with log P data runs end-to-end.
- The `canonical_unit` is read from the adapter, not hard-coded.
- Identity-token check still works (different chemistry, same gate).
- Standalone-name validator still works.
- Verification harness still works.

Qualitative-property modularity test (stub "color" adapter):

- `PROPERTY_NAMES = ["color"]`, `CANONICAL_UNIT = None`.
- A test paper "iron(III) oxide is a red-brown solid; copper(II)
  oxide appears black" yields two rows:
  - row 1: `compound_name = "iron(III) oxide"`, `property_name =
    "color"`, `value_type = "qualitative"`, `value_text = "red-brown
    solid"`, `value_canonical = NULL`, `canonical_unit = NULL`.
  - row 2: `compound_name = "copper(II) oxide"`, `value_text =
    "black"`, …
- `compound_name` passes the standalone-name validator (via the
  inorganic REQUIRE_PATTERN `[A-Z][a-z]?(?:O|S|N|Cl|Br|I|F)\d*\b`
  matching "oxide" forms, plus EXTRA_EXEMPT_NAMES).
- Identity-token check applies normally; the qualitative value path
  does not bypass any gate.

If any script needs changing to accommodate a new property → the
modularity contract is broken; the test fails.

### 12.7 Adapter conformance tests

For each adapter under `properties/`, a contract test that verifies:

- All required functions exist: `find_candidates`, `parse_value`,
  `classify`.
- All required constants exist: `PROPERTY_NAMES`, `CANONICAL_UNIT`,
  `PROPERTY_SUBTYPES`, `DATA_ORIGINS`, `DEDUP_VALUE_TOLERANCE`.
- `find_candidates()` on a known input returns dicts with all required
  keys.
- `parse_value()` correctly handles ranges, inequalities (`>`, `<`),
  approximate (`≈`, `~`), and alternate units; produces correct
  `value_type` and `value_text` for qualitative properties.
- `classify()` returns valid values from the declared sets.
- `triggers.yaml` parses; all listed triggers actually exist as
  string keys.

### 12.8 Verification-harness self-tests

- Random sampler with the same seed produces the same sample twice.
- Stratified sampler picks up all rows in the high-risk strata.
- Minimum audit pool of 30 is enforced.
- Pass-rate calculation correct for synthetic inputs (10/10 → 100 %;
  9/10 → 90 %).
- Pass-rate calculation is post-quarantine.
- Independent verifier agent flags a known-wrong row (a synthetic row
  with deliberately wrong value); passes a known-correct row.
- Frozen verifier prompt loads correctly; cannot be silently mutated
  by a verifier agent.
- `audit_log.json` is well-formed (parses; required keys present).

### 12.9 Robustness tests

- **Error handling**: malformed NXML → script logs error and returns
  empty article object; encrypted PDF → skipped with clear reason;
  missing file → graceful exit; network failure during DOI lookup →
  use other DOI sources, mark not_verified.
- **Idempotence**: running the same input twice with the same seed
  produces byte-identical `output.csv` and identical `skipped.csv`
  (audit_log may have different timestamps).
- **Round-trip**: write CSV → read CSV → verify content unchanged
  (no character-encoding loss, no escaped-quote munging).
- **Edge cases**:
  - Paper with 0 candidates → empty emission, no crash, no false
    coverage warning if abstract has no property keywords.
  - Paper with 1000+ candidates → no performance regression.
  - Paper where every candidate is rejected → empty `output.csv`,
    full `skipped.csv`, audit pool of 0.
  - Paper with property keywords in section titles only (review
    paper) → 0 emitted, 0 skipped (no actual values to extract).
  - Verification sample empty (all rows quarantined upstream) →
    run is flagged `all_audited_failed`, not auto-accepted.
- **Lexicon evolution**: extending `EXTRA_EXEMPT_NAMES` admits
  previously-rejected rows; existing tests continue to pass.
- **Concurrency**: running the skill on 10 papers serially vs. in
  parallel (paper-level workers) produces equivalent outputs (same
  rows, same skip reasons, modulo row-id ordering). The audit log
  remains well-formed under parallel writes. No race conditions
  between adapter loader and candidate enumeration.

### 12.10 Chemical-diversity name-validator tests

The REJECT/REQUIRE patterns and EXEMPT_NAMES must handle:

- **Small molecules**: acetone, methanol, water, benzene → admitted.
- **Inorganic compounds**: NaCl, CuO, H2SO4, KMnO4 → admitted (the
  `[A-Z][a-z]?(?:O|S|N|Cl|Br|I|F)\d*\b` pattern).
- **Salts**: sodium acetate, potassium chloride, calcium carbonate
  → admitted.
- **Hydrates**: copper sulfate pentahydrate, glucose monohydrate
  → admitted.
- **Polymers**: polyethylene, polystyrene, poly(methyl methacrylate)
  → admitted.
- **Common abbreviations**: TNT, DDT, MBT, BHA, PCB → admitted via
  EXEMPT_NAMES.
- **IUPAC names with stereodescriptors**: (R)-mandelic acid,
  (E,E)-1,4-diphenyl-1,3-butadiene → admitted.
- **Ionic liquid shorthand**: [BMIm][NTf2], [N1,1,1,4][BF4] → admitted
  via REQUIRE_PATTERN bracketed pattern.
- **Coordination compounds**: [Pt(NH3)2Cl2], [Cu(en)3]2+ → admitted.

**Negative tests** (rejected as expected):
- `compound 3`, `complex 9`, `4a` → rejected (local labels)
- `Result and discussion`, `Halogen-Release Biocides` → rejected
  (section titles)
- `(X=Cl, R=H)` → rejected (template)
- `benzoxanthenone derivative 4b` → rejected (generic derivative)

### 12.11 Scope-flag behavior tests

Run the same corpus under each preset and verify the emitted output
differs as designed:

- **`--strict`**:
  - Predicted/calculated rows do NOT appear in `output.csv`.
  - Literature-cited rows do NOT appear in `output.csv`.
  - Open-bound rows (`relation = ">"` or `<`) DO appear (open
    bounds are real data).
  - All filtered rows are recorded in `skipped.csv` with explicit
    skip reasons (`scope_excluded_predicted`,
    `scope_excluded_cited`).
- **default**: all of the above are emitted with appropriate
  `data_origin` tags.
- **review**: identical to default for emission, but the audit
  workflow consumes the audit_log differently (out of scope for v1
  test).
- Switching presets without re-extraction: the same intermediate
  candidate index produces different `output.csv` files for
  `--strict` vs `default`. This verifies that scope is a presentation
  decision over the candidate index, not an extraction decision.

### 12.12 Performance / scalability + CI matrix

Optional, non-blocking but tracked:

- Run time per paper (target: < 60 s on a single CPU).
- Memory usage on a 50-paper corpus (target: < 1 GB).
- Time to verify a 100-row audit sample (target: < 10 min).

CI matrix recommendation (not normative; up to the team to wire up):

- Every commit: unit tests (12.1) + adapter conformance (12.7).
- Pull requests: regression tests (12.3) + schema integrity (12.4) +
  chemical-diversity (12.10) + scope-flag (12.11).
- Nightly: golden corpus (12.2) + robustness (12.9).
- Weekly: held-out corpus (12.5).
- Recommended merge gate: 98 % pass on held-out corpus. If the team
  adopts this gate, any change that drops the held-out pass rate
  below 98 % cannot merge until investigated.

---

## 13. TODO / v2+ backlog

Maintained list (per user comment #3). Items are added during phases
1–7 and prioritized when Phase 8 starts.

- **CAS / PubChem cross-reference** of every emitted compound name.
  Confirms molecular formula; resolves common-name ambiguity (e.g.,
  the Dearden "1-Hexane" typo). Could downgrade
  `extraction_confidence` when no match found.
- **OCR fallback** for image-cell tables (paper 056 case).
- **Supplementary-information parser**. Many papers reference outlier
  data tables in SI. When the main paper yields 0 rows but the
  abstract suggests data exists, try SI files.
- **Fuzzy compound-name dedup**. Recognize that
  `2-((Cyclopentyloxy)methyl)isoindoline-1,3-dione` and
  `2-((cyclopentyl-oxy)methyl)isoindoline-1,3-dione` are the same
  compound; likely uses InChI keys from a structure database.
- **Active-learning loop for EXEMPT_NAMES**. When a verified row's
  name fails REQUIRE_PATTERN but passes manual review, add it to
  `EXTRA_EXEMPT_NAMES` automatically. Builds the lexicon over time.
- **Per-domain adapter packs**. A "medicinal chemistry" pack with
  drug-specific exempt names; a "materials science" pack for
  inorganics and metal complexes.
- **Cross-paper coreference**. When paper A cites paper B's value,
  link the row to the original measurement paper.
- **HTML / PDF report output** alongside the CSV for human review.
- **Verifier-model A/B testing**. Test that two different verifier
  models produce the same verdict on a sample; flag divergent rows.
- **Schema-version migration tool**. When schema columns are added /
  renamed, provide a migration path from old CSVs.
- **Logging / observability**. Structured progress reporting for long
  runs; ability to resume after a crash.
- **Safe paraphrased-evidence handling**. v1 rejects paraphrased
  evidence outright. v2 could investigate whether a constrained
  paraphrase (compound name + value + unit, all required to be
  verbatim) is admissible.
- **CAS/InChI key cross-check** of every emitted name (separate
  from the existing CAS/PubChem TODO above; this one focuses on
  the InChI key for fuzzy dedup).

This list grows as the build proceeds.

---

## 14. Worked example — predicted skill behavior on `mp_bp_dev_set`

Hypothetical run on the 20-paper corpus. Counts are aspirational and
depend on Phase 3–4 implementation quality; ranges are given where
the outcome depends on resolver coverage.

| Paper | Claude actual | GPT actual | Skill prediction |
|---|---:|---:|---|
| 010 TRPA1 | 29 | 31 | 30–31 emitted; GPT duplicate collapsed; ≥1 row with `relation=">"` for `>270 °C` |
| 011 PDE4 | 55 (1 chem err) | 55 | 54 emitted; compound 5d **caught by Gate B forward check**; if name re-extracted by re-running step 6 with the corrected source span, emitted as benzoic acid |
| 013 6H-benzo[c]chromene | 34 | 34 | 34 emitted |
| 017 ibuprofen salts | 9 | 9 | 9 emitted (Tg/Tc excluded by adapter triggers) |
| 020 N-hydroxypiridinedione | 32 (2 missed) | 39 | 39 candidates enumerated; ~39 emitted (including all open bounds with `relation=">"` per § 10) |
| 026 nucleoside analogs | 8 | 11 (with dups) | 8 emitted (GPT dups collapsed); Pb-complex `>300` emitted with `relation=">"` |
| 028 dispiro spirocyclics | 31 | 35 | 31 emitted + 4 with `relation=">"` for the >300 °C entries |
| 050 quinazolines | 18 (X unresolved) | 19 | 18 emitted with proper `6-chloro-…` names after template-variable resolver runs |
| 056 AI BP prediction | 0 | 0 | 0 emitted, candidate index logs the image-cell table; skip reasons `compound_identity_graphical_only` |
| 058 drug-like MP prediction | 0 | 0 | 0 emitted; abstract has no per-compound claims; no coverage warning |
| 064 COVID API | 0 (over-skipped) | 47 (incl. predictions) | ~9 emitted as `literature_cited`; ~36 emitted as `predicted_SIRM`/`predicted_STRM`; section-title names rejected by Gate A |
| 138 triazole/tetrazole | 27 | 27 | 27 emitted |
| 141 Tyrian Purple | 4 | 3 | 4 emitted (Tyrindoleninone via EXTRA_EXEMPT_NAMES; second 6-bromoisatin lit value kept) |
| 157 dehydrocholic acid | 8 | 8 | 8 emitted; DOI updated to verified `10.3390/i8070662` (cross-checked from publisher source) |
| 164 microbiological | 11 | 10 | 11 emitted (no duplicates); biocide names cleaned |
| 178 benzoxanthenones | 10 (4a inferred) | 13 (with dups) | 4 emitted (4a + 4h/4i/4j); 6 skipped as `compound_identity_not_resolvable_from_paper` (4b–4g unnamed in paper) |
| 2009 Dearden | 196 | 0 | 196 emitted (candidate enumeration catches the full table; GPT's silent miss prevented) |
| 2011 Krossing | 40 | 92 | ~40 measured emitted + ~50 calculated emitted (tagged as `predicted_<method>`) |
| 2014 Schmittel | 5 | 5 | 5 emitted |

The skill is closer to Claude on standalone quality, closer to GPT on
coverage, and strictly better on the residual error modes — especially
the silent table miss (Dearden), the chemistry transcription bug (5d),
the section-title fallback, and the template/derivative names. **All
predicted counts are conditional on Phase 6.5 validating against the
held-out corpus**; the dev-corpus numbers above are training
expectations only.

---

## 15. Summary

The skill is built around the user's stated priority:

> *It's much more important that all data extracted be correct and
> verifiable than that no data be missed.*

Mechanism:

- **Six acceptance gates (A–F)** every row must clear, mapped
  many-to-many to the eight failure modes the prior audits surfaced
  (Gate A covers F2/F3/F4/F8; Gate B covers F1; Gate F covers F6;
  the candidate-first enumeration in step 3 covers F5; the relation
  field covers F7).
- **A two-column identity schema** (`compound_name` for standalone
  identity, `compound_label` for paper-local code) with **paired
  evidence** (`compound_evidence_text` + `property_evidence_text`,
  each with its own `evidence_type`).
- **Property-neutral schema** (`value_canonical` + `canonical_unit`
  for numeric, `value_text` for qualitative) so the same skill works
  for log P, pKa, density, color, crystal system, …
- **Candidate-first enumeration**: every property-relevant mention
  enters a candidate index *before* any filtering; emitted vs skipped
  is the primary output split.
- **Unresolved compounds go to `skipped_candidates.csv` only**,
  never to the final CSV.
- **Random + stratified verification** with a 98 % pass threshold
  enforced **after** audit-failed rows are quarantined. **The threshold
  is measured on a held-out corpus**, not on the dev corpus the
  gates were tuned against.
- **Cross-source DOI verification** as part of ingestion.
- **Phased build (1–8)** with explicit overfitting check at Phase 6.5.
- **Eleven test layers (12.1–12.11)** with unit, golden-corpus,
  regression (F1–F8), schema integrity, **held-out corpus
  validation**, cross-property modularity, adapter conformance,
  harness self-tests, robustness/edge-case, chemical-diversity
  validator tests, and performance / CI matrix.
- **A TODO backlog (§ 13)** maintained as the build proceeds.

The 98 % target on compound names, property values, units, DOIs, and
evidence is what the verification harness measures and what the held-
out merge gate enforces. The proposal is implementable; the
architecture is modular; the gaps the prior audits exposed are wired
through explicit gates and tests; and the overfitting risk is
explicitly checked rather than assumed away.

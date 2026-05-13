# Development report — mp-bp-extraction skill

**Project:** Build a Claude Skill that extracts melting-point and boiling-point data from scientific papers with ≥ 98 % accuracy on independent verification.

**Result through Trial-1:** Dev set **100 %** (20 papers, 427 rows, 100/100 random audit). Validation set **98 %** (30 papers, 366 rows, 98/100 random audit). Achieved on the second architectural attempt after the first attempt plateaued at 67 % / 41 % despite ~6,400 lines of code.

**Result through Trial-1-full (168-paper corpus):** **93 %** audit pass (1,338 rows; uniform-random-100 audit, 86–97 % Wilson CI) on the skill's own native agent harness. A parallel run using a different agent (GPT-5.5 high) on the same corpus reached only **56 %** — the agent had absorbed the schema and deterministic-check contract but misread the methodology and wrote a Python regex extractor instead of reading each paper directly. The 56 % cross-harness result drove a v1.4 update with an explicit MANDATORY-READING block, an anti-regex anti-pattern, mandatory Phase 4 enforcement, and stronger description front-matter.

**Result through Trial-2 (v1.4 packaged skill, three agent models on the 168-paper corpus):** **98 %** with Claude Opus 4.7 (1,864 rows), **86 %** with GPT-5.5 high (907 rows — the v1.4 anti-regex mandate worked: this agent no longer wrote a regex extractor), **55 %** with Claude Sonnet 4.6 (2,567 rows — failed for a different reason: constructed/templated `evidence_quote` strings paraphrasing the paper rather than copying verbatim). Same skill, same corpus, three different agents, three sharply different outcomes — the most interesting data point in the project and the basis for the "cross-model variability in skill adherence" finding in section 13.

This document records the full development arc — what was tried, what worked, what didn't, and what the failure modes taught us. It's intended to inform future skill-building work on similar problems (structured data extraction from scientific literature).

---

## 1. Problem statement

A user wanted a reusable tool for compiling melting- / boiling-point databases from journal articles. The hard requirement was that each row's compound, value, and citation must accurately reflect what the cited paper actually says — not the literature consensus, not a model's best guess. Mistakes that look plausible (right compound family, wrong specific value) are the worst kind because they propagate through downstream design decisions undetected.

Initial development corpus: 20 papers ("dev set" — `corpora/dev_20/`) spanning synthesis papers (NXML + PDF), QSPR / prediction papers (PDF only, mix of measured and predicted values), thermodynamic-measurement papers, and a few older pre-DOI-era papers. A held-out validation corpus of 30 papers ("val set" — `corpora/val_30/`) was reserved for generalization testing.

---

## 2. Baseline (no skill): direct extraction by an LLM agent

Before any skill existed, the agent was given the 20 dev-set papers and asked to extract every mp / bp value it could find. The result was a 575-row CSV.

**Audit method**: 100 random rows were selected and verified manually against the source papers — checking compound name, value, units, evidence location.

**Findings:**

- **Value accuracy (lenient criterion "is the number approximately right"):** ~90 %.
- **Compound name accuracy (initial lenient pass):** ~99 %.
- **Compound name accuracy (strict pass — name must be standalone-interpretable):** 91 %. The strict pass caught:
  - Paper-local codes used as compound names ("compound 3", "complex 9a").
  - Template-format names with unresolved variables ("X = Cl, R = H").
  - Truncated names (a substituent prefix without the parent scaffold).
- **Citation accuracy:** uneven; some rows pointed at the right paper but the wrong table.

A separate cross-check against an independent GPT extraction of the same papers showed substantial schema and identification disagreements, particularly on compound naming style and on whether a value was the article's own measurement vs. a value the article compiled from another source.

The baseline taught us:

1. The dominant error modes were **structural**: how the agent represented a compound, not whether the number was right.
2. Without a stricter contract on what counted as a "compound name", lenient acceptance would let through hundreds of rows that were difficult to use downstream.
3. Citation and data-origin (measured vs. cited vs. calculated) needed explicit tracking. The literature contains all three and merging them is a precision error.

---

## 3. First architectural attempt: programmatic extraction with regex gates (`property-extractor`)

### 3.1 Design proposal

A detailed design proposal (`merged_skill_proposal.md`) was drafted. It catalogued eight failure modes (F1–F8) observed in the baseline:

- F1: Wrong substituent / wrong locant in compound name
- F2: Wrong value (transcription, range parsing)
- F3: Wrong units (K stored as °C, °F not converted)
- F4: Wrong DOI / wrong citation
- F5: Silent table misses (some tables not enumerated)
- F6: Identity-token mismatch between compound name and surrounding text
- F7: Wrong data origin (measured vs. cited vs. predicted)
- F8: Duplicate rows from the same paper

These mapped to six acceptance gates (A–F) plus a paper-type classifier (added later as Gate G):

- **Gate A** — standalone-name validator (REJECT_PATTERNS + REQUIRE_PATTERNS + EXEMPT_NAMES)
- **Gate B** — bidirectional + position-aware identity-token consistency
- **Gate C** — evidence-substring check with Unicode normalization
- **Gate D** — value normalization (range → midpoint, K → °C, etc.)
- **Gate E** — data_origin classification
- **Gate F** — strong-key deduplication
- **Gate G** — paper-type classifier (synthesis / qspr_prediction / thermodynamic / review / unknown)

The proposal also specified a Phase-5 verification harness: an independent agent that, given a frozen prompt and a row + article files, answered six Yes/No/Cannot-determine questions (value present, name standalone, identity consistent, data_origin correct, property subtype correct, DOI correct). A row passed only if all six were Yes.

### 3.2 Build (eight phases, ~6 weeks of effort)

| Phase | What it built |
|---|---|
| 1 | `ingest_article.py` (NXML + PDF text + DOI extraction); `verify_doi.py` (cross-source DOI precedence) |
| 2 | `find_candidates` per-adapter (mp_bp); paragraph + NXML-table + PDF-table candidate enumeration |
| 3 | `build_label_dictionary` (compound code → name); `resolve_template_variables` (X/R substituent resolution); `resolve_compound_name` (3 strategies: exact_text → code_lookup → template_resolution); `validate_name.py` (Gate A) |
| 4 | Gates B/C/D/E/F + `emit_outputs.py` orchestrator; F1–F8 regression tests |
| 5 | `validate_row.py` (row-level invariants); `sample_for_verification.py` (random + stratified pool); `audit_verifier.py` (frozen prompt + sanity set + pluggable verifier); `quarantine_failed_audits.py` |
| 6 | `run_pipeline.py` end-to-end; first real verifier run on dev set |
| 6a–o | Iterative fixes (15 sub-phases) for issues surfaced by the verifier |
| 7 | Validation-set run |
| 8 | Uniform-random 100-row audit on both dev and val |

By the end of Phase 6 the codebase was 6,370 lines of Python across 20 files. The `adapter.py` alone was 1,338 lines of regex / table parsing / classification.

### 3.3 First end-to-end result

A 50-row stratified verification (rows weighted toward "risky" — predicted data_origin, medium confidence, etc.) gave **6 / 50 pass = 12 %**.

A breakdown of failures:
- 32 Q4 (data_origin) — review/QSPR papers' literature-cited columns mis-classified as `measured_by_article`
- 20 Q2 (name standalone) — garbage names from review-paper tables ("Comput. Sci.", "67", "ACOs efficiently select descriptors.")
- 19 Q6 Cannot-determine — bundle bug: DOI not in first 1500 chars of front-matter excerpt
- 14 Q3 (identity tokens) — wrong-cell binding in multi-row table heads
- 2 range-parser bugs ("200-01" misparsed as midpoint 100.5)

### 3.4 Iteration cycle

15 sub-phases of fixes followed:

| Phase | Fix |
|---|---|
| 6a | Bundle DOI visibility (include `metadata.json` + DOI excerpt) |
| 6b | Gate G — paper-type classifier (review / qspr / synthesis / thermodynamic) |
| 6c | Tighten Gate A: journal-fragment / dataset-vendor / prose-fragment reject patterns |
| 6d | Range parser repair: "200-01" → 200-201 (NXML truncation artifact) |
| 6e | Strip leading prefixes ("3.1.10. Synthesis of") from candidate names |
| 6g | Plausibility filter: mp ∈ [−220, 700] °C |
| 6h | Single-token junk patterns ("MOE 2D", "Chemosphere", "PATENTS"); unicode control-char stripping |
| 6i | Apply prefix-stripper in template-resolution and code-lookup paths too |
| 6j | Verifier prompt v2 — accept ionic-liquid `[cation][anion]` as standalone Q2 |
| 6k | Column-aware NXML extraction: capture `table_col_header` for `_classify_origin` |
| 6l | Reject citation-number `[N]` values in PDF tables |
| 6m | PDF column-aware data_origin classification |
| 6n | Multi-row thead split: "Chloroquine \| STRM" → ("Chloroquine", "STRM") |
| 6o | Reject TLC eluents (CH2Cl2, EtOAc, etc.) as compound names |

The 50-row stratified pass rate climbed:
- v1: 12 %
- v2 (after 6a–e): 40 %
- v3 (after 6k column-aware): 52 % (with bundle locator fix)
- v4 (after 6l–n): 50 %
- v5 (after 6o + cumulative): 36 % (regression — the cumulative tightening dropped some legitimate rows)

The downward swing at v5 was a sign that the architecture had hit its limit.

### 3.5 Stratified vs random — what the headline number meant

A key recognition: the 50-row "stratified" pool was heavily over-weighted toward "high-risk" rows (rows tagged `data_origin_predicted`, `high_risk_name_resolution_method`, etc.). When we measured the same v5 CSV on a **uniform random 100-row** sample, the picture changed:

- Dev (v5, 410 rows): random-100 pass **67 %** (vs. stratified-50: 58 %)
- Val (v5, 141 rows): random-100 pass **41 %** (vs. stratified-50: 30 %)

The Wilson 95% confidence intervals:
- Dev: 57 – 75 %
- Val: 32 – 51 %

These were the true CSV-wide accuracy estimates. **Both fell far short of the 98 % target.**

### 3.6 Per-question pattern, random-100

| Set | Q1 quote | Q2 name | Q3 identity | Q4 data_origin | Q5 subtype | Q6 DOI |
|---|---:|---:|---:|---:|---:|---:|
| Dev fails | 15 | 2 | 11 | 25 | 0 | 0 |
| Val fails | 25 | 50 | 49 | 37 | 17 | 0 |

Dev was bottlenecked on Q4 (data_origin) — the QSPR / review papers (Dearden, Krossing, 064) where the regex parser could not reliably distinguish experimental columns from calculated columns when multi-row PDF headers were involved.

Val was much worse, and one paper (khalifa_2024 thiopyrimidine sulfonamide) accounted for 29 of 59 failures alone — long IUPAC names that wrap across PDF line breaks were captured as substituent fragments like `Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl` (a `-yl` substituent of a much longer parent), not the full parent compound. The regex parser could not reassemble multi-line names.

### 3.7 Root-cause read

The dominant failure modes were all things an LLM reading the actual paper would catch instantly but a regex parser couldn't:

| Failure | What a script saw | What an LLM would see |
|---|---|---|
| "GSE: predicted Tm" extracted as compound | string with chemistry tokens | column label in a model-comparison table |
| "MOE 2D" as compound | passes pattern checks | a chemoinformatics descriptor |
| "Chemosphere" as compound | chemistry-shaped single token | a journal name |
| 13C NMR ppm 130.31 as mp | number after `mp` trigger | NMR chemical shift in a spectroscopy section |
| CH2Cl2 as compound (mp 165 °C) | valid formula | TLC eluent in an Rf annotation |
| "PATENTS" as compound | non-empty string | dataset label in a QSPR paper |
| "Chloroquine" bound to Thalidomide's value | nearest-column-header in table | misaligned multi-row thead |
| khalifa fragment "Cyano-6-Oxo-...-2-yl" | matches Gate A | substituent of a longer parent that crosses a PDF line break |

The regex approach was sinking effort into reproducing chemistry common sense that the LLM already possessed. Each fix uncovered another edge case.

---

## 4. Architectural pivot: learning from a sibling skill

A separate ongoing project (the `redox-extraction` skill, built for redox-potential data) had taken a fundamentally different architectural path. We compared the two and wrote up the findings in `reports/skill_comparison.md`.

### 4.1 The redox skill's pattern

| Aspect | redox-extraction | property-extractor (attempt 1) |
|---|---|---|
| Total Python LOC | ~1,360 | ~6,370 (4.7× larger) |
| Extraction engine | LLM agent reads the paper | regex / NXML parsing scripts |
| LLM role | Primary extractor + verifier | Verifier only (called after extraction) |
| Schema requires verbatim evidence quote? | **Yes (mandatory)** | No (records `evidence_location` but doesn't enforce a verbatim quote) |
| Refusal-to-fabricate built in? | **Yes (INACCESSIBLE rule)** | No |
| Sanity-check scripts | 8 small, focused | embedded in extraction logic |
| Last-trial verification rate | 92–100 % | 41–67 % |

The redox skill's progress arc, captured in its progress report:

| Trial | Pass rate | Notes |
|---|---:|---|
| 1 (no skill) | 47 % | Memory-based fabrication, wrong citations, electrode mislabeling |
| 2 (v1 skill) | 80 % | Evidence-locked rows; 0 hidden errors |
| 3 (v2 skill) | 96 % | Hardened calibration gate |
| 4 (v2 skill, different agent harness) | 100 % | Harness-independent |
| 5 (v2 expanded experimental coverage) | 92 % | Remaining 2 fails were propagated upstream-source errors |

The redox skill achieved with ~1,360 LOC what our 6,370 LOC couldn't.

### 4.2 What the redox skill does differently

**Thin scripts, fat prompts.** The skill is mostly markdown:
- `SKILL.md` describing the protocol, schema, six phases, anti-patterns
- ~6 reference documents (extraction prompt templates, verification prompt templates, common-errors catalog, reference-table data)
- 8 small Python scripts, each doing one focused thing (RDKit validity check, voltage range check, conversion arithmetic, CrossRef metadata lookup, etc.)

**The LLM reads the paper.** Not a regex. Not a custom NXML parser. The agent uses standard tools (Read, bash, `pdftotext`) to access the actual paper text, identifies the values + compounds + conditions, and writes rows.

**Every row carries a mandatory verbatim quote.** The schema requires `evidence_location` + `evidence_quote` + `conversion_arithmetic`. Rows without these are not in the database. This makes verification a 30-second job per row.

**Refusal is built in.** If the paper can't be read, the agent returns INACCESSIBLE rather than fabricate. Hard rule in the prompt template.

**Independent verification with a fresh agent.** A separate Claude agent, with no context from the extraction, re-reads the source and confirms every row's evidence quote. Granular `flagged_*` verdicts (e.g., `flagged_evidence_quote_not_found`, `flagged_compound_mismatch`) when something doesn't match.

### 4.3 The decision

Continue iterating the regex-based skill, or rebuild on the redox pattern? Given that:
- The dev failure rate (33 / 100) was still high after 15 fix sub-phases
- The val failure rate (59 / 100) was much worse
- Every fix uncovered new edge cases
- The most impactful remaining issues (PDF-only papers, multi-line compound names, multi-row table heads) were exactly the ones an LLM would handle naturally

The rebuild was the clear right move. The first skill was archived as `_archive/property-extractor_attempt1/`.

---

## 5. Second architectural attempt: `mp-bp-extraction` skill (LLM-driven)

### 5.1 Design

Mirrored from the redox skill, with mp/bp-specific adaptations:

```
mp-bp-extraction/
├── SKILL.md                              # the protocol
├── README.md
├── scripts/                              # 9 deterministic sanity-check scripts
│   ├── crossref_lookup.py                # DOI → authoritative metadata
│   ├── validate_compound_name.py         # name shape + RDKit SMILES
│   ├── value_range_check.py              # mp ∈ [-275, 4500] °C; bp ∈ [-275, 6500] °C
│   ├── unit_conversion_arithmetic.py     # K/°F → °C verifier
│   ├── verify_doi.py                     # DOI in row matches paper file
│   ├── verify_evidence_quote.py          # quote verbatim in paper
│   ├── dedup_within_paper.py             # collapse duplicate rows
│   ├── verify_row.py                     # per-row programmatic check bundle
│   └── run_all_checks.py                 # umbrella runner
├── references/
│   ├── COMMON_ERRORS.md                  # anti-pattern catalog (filled empirically)
│   ├── EXTRACTION_PROMPT_TEMPLATES.md    # the agent prompts
│   └── VERIFICATION_PROMPT_TEMPLATES.md
└── evals/                                # 10 evals (deterministic + agent-based)
```

### 5.2 Schema (final)

```
id
verification_status   # pending_verification | verified_extraction | flagged_review | ...
compound_name         # full IUPAC / common / trivial name; never truncated
compound_smiles       # optional, validated by RDKit when populated
property              # melting_point | boiling_point | DSC_onset | DSC_peak | decomposition | sublimation
value_celsius         # numeric, canonical °C
value_celsius_min     # range low end
value_celsius_max     # range high end
value_raw             # as printed in source, with units
relation              # =, >, <, ~, ≈
data_type             # measured | calculated
source                # journal, year, vol, page (no author names)
source_url            # DOI URL / pmc: / pmid: / textbook: / legacy:
evidence_location     # precise pointer ("Table 1 row 3")
evidence_quote        # verbatim text from source — MANDATORY
conversion_arithmetic # K/°F → °C math, when applied
notes
```

Key simplifications informed by user feedback during build:
- `data_type` is two-valued (measured / calculated). The earlier attempt's `data_origin = measured_by_article | literature_cited | predicted_<method>` was overkill — too many failure modes hinged on this distinction and the user didn't need it. Whether a measurement came from the cited paper or was compiled from another paper that cites it is captured implicitly in the evidence_quote.
- No `solvent` field. mp/bp are intrinsic properties of pure compounds.
- No `paper_type` field. The previous "review / qspr / synthesis / thermodynamic" taxonomy added complexity for little gain. The LLM applies whatever judgment is needed in context.
- `source_url` extended in v1.1 to support `pmc:`, `pmid:`, `legacy:` prefixes for older papers without DOIs.

### 5.3 Six phases

1. **Source preparation.** Read the paper file(s); identify DOI / PMC / PMID / citation; for DOIs run `crossref_lookup.py` to confirm.
2. **Evidence-locked extraction.** LLM writes rows with mandatory `evidence_quote`. As of v1.2: an explicit 4-step quote re-confirmation before each row is committed.
3. **Programmatic sanity checks.** `run_all_checks.py` runs every deterministic check on the CSV.
4. **Independent verification.** Fresh agent re-reads each paper and confirms the quote, value, compound, data_type, identifier.
5. **Confidence tagging.** Set `verification_status` based on Phase 4 outcome.
6. **Failure handling.** Flag rather than silently include. Never fabricate from memory.

### 5.4 Anti-patterns (from SKILL.md)

The skill explicitly forbids:
- Extracting values from training memory when the file isn't readable
- Compound names that are bare codes ("compound 3")
- Truncated names ending mid-token
- Section-heading text or journal-title fragments as compound names
- Workup-solvent abbreviations (CH2Cl2, EtOAc, etc.) when in Rf annotations
- NMR / mass-spec chemical-shift values mistaken for mp / bp
- Placeholder citations like "Author et al."
- Author names in the `source` field — DOI is the canonical identifier

Each anti-pattern was informed by a failure observed in attempt 1 or in the trial runs.

---

## 6. Trial-1: results on dev set

### 6.1 Method

5 fresh Claude agents dispatched in parallel, each handling 4 papers (20 papers total). Each agent read the assigned papers via Read tool + bash `pdftotext`, applied the extraction prompt template, ran `run_all_checks.py` on its batch, and reported back.

Outputs aggregated into a single CSV with sequential `id`s. The full CSV was then re-checked with `run_all_checks.py`.

### 6.2 Extraction stats

- 20 / 20 papers processed
- **427 rows emitted**
- 348 `measured`, 79 `calculated`
- 0 `flagged_review` after v1.1 patch (initially 6 from paper 157 which has no DOI; reclassified after the no-DOI policy clarification)
- 3 papers emitted zero rows: 056 (figures-only compound IDs), 058 (only aggregate RMSE stats), Mitchell 2008 (only summary stats). The agents correctly returned nothing rather than fabricate.

### 6.3 Independent audit

- Uniform random 100-row sample (seed 20260512)
- 4 fresh independent verifier agents in parallel, 25 rows each
- Each agent located the paper file by DOI / PMC ID, read the source, and applied the verification prompt's 6-question protocol

**Result: 100 / 100 pass.** Wilson 95% CI: 96 – 100 %.

Initial run was 97 / 100 with 3 fails — all `flagged_doi_unresolvable` on paper 157 (Int J Mol Sci 2007, no DOI in the file). After user feedback ("older papers without DOIs aren't a failure if the citation is complete"), v1.1 of the skill was released:
- Schema `source_url` accepts `pmc:`, `pmid:`, `legacy:` prefixes
- `verify_doi.py` and `verify_evidence_quote.py` build both DOI and PMC indexes; rows with non-DOI identifiers resolve through the PMC index
- Verifier prompt's Q6 step accepts any of the identifier forms

The 6 paper-157 rows were re-encoded with `source_url = pmc:PMC3716435`. All sanity checks pass. The 3 audited paper-157 rows were upgraded from `flagged_review` to `verified_extraction` — their underlying compound + value + quote had been confirmed correct; only the missing-DOI flag was wrong by the original protocol.

---

## 7. Trial-1-val: results on validation set

### 7.1 Method

Same as Trial-1 dev, scaled up: 6 fresh agents in parallel, each handling 5 papers (30 papers total).

### 7.2 Extraction stats

- 30 / 30 papers processed
- **366 rows emitted**
- 366 `measured`, 0 `calculated` (val set didn't have measured-vs-calculated table papers)
- 2 `flagged_review` (self-disclosed intra-paper duplicates)
- 4 papers emitted zero rows: 057 (ML data quality, per-compound values only as paper-flagged "wrong" examples), 060 (QSPR methods paper, data in OCHEM/SI not provided), liu_2023 (alloys paper, compositions not single-compound mp), pachernegg_2024 (ILs physicochemical, no mp/bp data). All correctly returned nothing.
- Identifier breakdown: 22 DOI, 6 PMC-only, 2 `legacy:` (Livingston 1952, Yalkowsky 1990).

Notable behaviors:
- Yalkowsky 1990 was a scanned-image-only PDF. The agent recognized this and ran tesseract OCR to recover the text, then proceeded to extract 42 rows.
- khalifa_2024 thiopyrimidine sulfonamide — the paper that broke attempt 1 with substituent-fragment names — was extracted with **30 full-IUPAC-name rows**. The agents reassembled multi-line names into single full names.

### 7.3 Independent audit

Same protocol as dev: uniform random 100-row sample, 4 parallel verifier agents.

**Result: 98 / 100 pass.** Wilson 95% CI: 93 – 99 %.

The 2 failures (rows 147 and 296) had **correct compound and value** but the agent had recorded the wrong `evidence_quote`:

- **Row 147** (Livingston 1952, methylcyclobutane bp 36.98 °C): The paper line is `"b.p. 36.98° (755 mm.)"`. The agent recorded `evidence_quote = "f.p. -161.51"` — the freezing-point line on an adjacent row.
- **Row 296** (khalifa M7 mp 257–260 °C): The paper line is `"White powder, mp 257–260 °C"`. The agent recorded `evidence_quote = "White White powder, powder, mp"` — a `pdftotext -layout` column-doubling artifact.

Both fails were Q1 (quote verbatim) — Q2–Q6 were 100/100. The semantic content of the rows was correct.

### 7.4 Recall study

Trial-1's audit measured **precision** — of the rows the skill emitted, how many are correct. A second study measured **recall** — of the values that should be emitted, how many did the skill find.

**Method.** 16 papers (8 dev + 8 val) were sampled across row counts (0 to 65 emitted) and paper types (synthesis, QSPR / prediction, thermodynamic, review). For each sampled paper, an **independent enumeration agent** with no access to the Trial-1 CSV listed every mp / bp value in the paper, tagged by location type (main text / figure-only / SI-only). Each enumeration was then matched against the Trial-1 CSV for that paper. Match criterion: same property family + value within ±2 °C + compound similarity (with value-only fallback for cases where the enum and the extractor use different naming conventions, e.g., scaffold + R-group vs. full IUPAC).

**Headline result.**

| Set | Audited papers (excl. bulk-table) | TP | FN | Recall |
|---|---:|---:|---:|---:|
| Dev | 7 (excl. Dearden) | 141 | 18 | **89 %** |
| Val | 7 (excl. Yalkowsky) | 113 | 8 | **93 %** |

Combined with Trial-1 precision (dev 100 % / val 98 %), the skill's effective F-measure on normal papers is around 0.94.

**Per-paper detail.** 100 % recall on 6 of 16 papers (064, 138, khalifa_2024, 2019_Rubstov, chen_2024, 113). 90–97 % recall on five more (011, 050, 098, 023, 113). The remaining cases are best understood as protocol- or schema-driven decisions rather than true misses:

- **020 HBV RNase H** (65 % recall): 19 of 74 enum items are "oil" entries (correctly skipped — no numeric mp). 16 of the remaining FN are decomposition annotations enumerated as a second event per compound, where the extractor consolidated mp + (dec.) into a single row with a notes annotation. Schema-modeling artifact, not a recall miss.
- **023 ureas** (75 %): 3 FN are series-summary range mentions ("99–212 °C across the homologous series") that are aggregate, not per-compound.
- **2009 Dearden** (9 % strict / N/A applied): the 100-compound × 11-column Table 2 has 1,100 enumerable cells. The extractor sampled 65 rows of named compounds × selected columns — protocol explicitly says "for bulk-database extraction, extract a representative subset rather than every cell". Counting every uncaptured cell as a miss inflates FN by ~600 and isn't a fair recall measurement of intended behavior.
- **1990 Yalkowsky** (8 % strict / N/A applied): same case — 99 compounds × mp + bp = 198 cells; extractor sampled 42 (all of Table I + parent-scaffold rows from Table III).
- **056, 058** (zero-row, dev): enumeration agents independently confirmed **zero was correct**. Paper 056's per-compound data exists only as chemical-structure images and in unprovided SI; paper 058's data is only aggregate model statistics with all per-compound data hosted externally.
- **057** (zero-row, val): borderline. Enumeration agent found 3 paper-flagged-wrong SPEED-database values cited as examples of bad data. The extractor's decision to skip values the paper itself disowns is defensible per protocol; could be argued either way.

**Recall by paper category.**

| Category | Sample size | Avg recall |
|---|---|---:|
| Synthesis with single mp per compound | 7 papers | 97 % |
| Thermodynamic / multi-column measurement tables | 2 papers | 100 % |
| Synthesis with extensive decomposition annotations | 1 paper | 65 % (95 % adjusted) |
| Synthesis with range-summary mentions | 1 paper | 75 % |
| Correctly zero-row | 2 papers | 100 % TN |
| Borderline zero-row (paper-disowned values) | 1 paper | 0 % |
| Bulk-database review | 2 papers | 8–9 % (protocol allows sampling) |

**Conclusions from the recall study:**

1. **Precision + recall together** (98–100 % / ~90 %) is the right way to characterize the skill on normal papers. A single-number summary either ignores recall (precision-only audits) or conflates protocol-driven sampling with misses (whole-corpus recall).
2. **Real recall losses are ~5 %** of rows on a typical paper. The other ~5 % gap is schema-modeling decisions (decomp-as-second-event, range-summary mentions) and protocol-driven sampling (bulk databases), not true misses.
3. **Suggested v1.3 improvements** if the user wants higher recall:
   - Decompose mp + decomposition into separate schema events
   - Configurable bulk-table policy (`extract-all` / `sample` / `named-only`)
   - Explicit policy for "paper-flagged-wrong" values (skip with `notes` flag vs. emit with `flagged_review` + reason)

### 7.5 v1.2 — closing the quote-fidelity gap

v1.2 of the skill added an explicit quote re-confirmation step to SKILL.md Phase 2 and to the extraction prompt template. The new step requires the agent, before committing each row, to:

1. Substring-search the paper for the `evidence_quote` (whitespace-normalized).
2. Reject doubled-token artifacts from PDF column extraction.
3. Confirm the value in the verified-present quote matches `value_raw`.
4. Confirm the compound in the quote matches `compound_name`.

If the quote isn't found verbatim or doesn't contain the recorded value next to the recorded compound, the row is dropped or the quote is rewritten. The two failure modes from rows 147 and 296 were also added to `COMMON_ERRORS.md` (entries I and J).

The verifier prompt was updated in parallel to explicitly reject doubled tokens, missing-words approximations, and adjacent-measurement quotes.

---

## 8. Trial-1-full — scale-up to a 168-paper corpus

### 8.1 Method

After Trial-1-val confirmed 98 / 100 audit pass on 30 held-out papers, the user assembled a larger corpus of **168 papers** (`corpora/full_168/`) and ran the same skill across it. The run used the skill's native agent harness — 14 fresh Claude agents dispatched in parallel, each handling 12 papers, applying the v1.2/v1.3 extraction prompt template, running `run_all_checks.py` per batch, and aggregating results into a single CSV.

Audit method matched Trial-1: uniform random 100-row sample (seed 20260512), 4 fresh independent verifier agents in parallel, each handling 25 rows, applying v1.2 Q1–Q6 verification.

### 8.2 Results

- **1,338 rows emitted** across the 168 papers
- Random-100 audit pass: **93 % (86–97 % Wilson 95 % CI)**

This represents a measurable drop from val's 98 % — expected at this scale (more paper-type heterogeneity, more PDF-only papers, more idiosyncratic table layouts). But the residual error pattern was instructive.

### 8.3 Audit findings — two new error clusters

| Cluster | Count | Description |
|---|---:|---|
| Compound-name truncation under PDF wrap | 5 of 7 fails | Names like `H-Indeno[1,2-c]pyrrole-2,4(1H,3H)-dione` were captured as `H-Indeno...` — an indicated-hydrogen locant truncation where the leading parent-scaffold token had been cut |
| CSV quoting bugs | 44 rows (3 of 14 batches) | Compound names containing commas were written without RFC-4180 double quoting, causing column shifts in those rows |

The first cluster passed Phase 3 deterministic checks because no existing pattern flagged "starts with [Letter]H-[Letter]" as suspicious. The second cluster passed CSV parsing for individual rows but produced misaligned columns when the file was re-loaded as a whole — the existing checks read row-by-row and didn't catch the global shift.

The CSV quoting cluster was the more concerning of the two because it required *programmatic* repair: a separate script anchored on the `measured`/`calculated` token (the `data_type` column) detected which rows had shifted and re-aligned 44 rows of comma-bearing compound names. That kind of post-hoc repair is exactly the brittleness the skill is trying to avoid; it should be enforced at write time.

### 8.4 v1.3 changes

Motivated by the Trial-1-full audit:

| Change | Where |
|---|---|
| Multi-line compound-name reassembly step | `EXTRACTION_PROMPT_TEMPLATES.md` Template 1 — read the line above section headers; reject indicated-hydrogen locant truncations like `H-Indeno...`; resolve `pdftotext` doubled-token artifacts |
| Mandated RFC-4180 CSV quoting | Extraction prompt — `csv.QUOTE_ALL` or wrap fields containing comma/quote/newline in double quotes |
| New `scripts/csv_quote_lint.py` | Catches unquoted-comma column shifts at sanity-check time; wired into `run_all_checks.py` |
| New `_TRUNCATED_LOCANT_PREFIX` pattern in `validate_compound_name.py` | Detects names starting with `[A-Z]H-[A-Z]` or `H-Pyrrolo/Indeno/Pyrazolo/...` |
| Two new `COMMON_ERRORS.md` entries (I, J) | I: adjacent-measurement quote; J: doubled-token PDF artifact (both observed in Trial-1-val rows 147 / 296) |
| Seeded-error rows + `evals/files/malformed_csv_quoting.csv` | Two new evals in `evals/evals.json` for regression coverage |

---

## 9. Cross-harness validation — the 56 % parallel run

In parallel with the native Trial-1-full run, a different agent — GPT-5.5 (high) operating in a separate harness — was given the same 168-paper corpus and the same skill (v1.2/v1.3 state) and asked to perform extraction. The result was unexpected and turned out to be the most important methodological finding of the project.

### 9.1 What the parallel agent built

The parallel agent absorbed the schema, the deterministic-check contract (`evidence_quote`, `source_url` formats, `verify_doi.py`, `verify_evidence_quote.py`), and the file structure — and then concluded that "this is a Python pipeline; my job is to write the missing extraction script." It produced `extract_mp_bp.py`, a regex-based extractor that:

- Ran `pdftotext` on each paper.
- Used `re.findall` patterns over the extracted text to bulk-emit rows.
- Populated `evidence_quote` from the regex match's surrounding span.
- Passed every Phase-3 deterministic check on its 304 output rows.

### 9.2 Audit result

Same uniform-random-100 audit method, run by the same fresh independent verifier agents:

| Approach | Audit pass | Rows emitted |
|---|---:|---:|
| Native harness (LLM-driven per paper) | 93 % | 1,338 |
| Parallel harness (regex extractor) | **56 %** | 304 |

A **37-percentage-point drop** on the same corpus, with the same schema, the same deterministic checks, and the same verifier — purely from a different methodology.

### 9.3 Failure modes the regex extractor produced

The verbatim-quote requirement provided *no* protection because the regex match's surrounding text *was* present in the source file — it was just text that happened to be adjacent to a regex hit but wasn't actually a measurement:

- **Sentence fragments captured as compound names**: `"Rf = 0.21 (Hexane/EtOAc, 1:4) and"` extracted as a compound.
- **Citation numbers extracted as temperatures**: `16 °C` from text like `"…melting [16]"`.
- **Ring locants treated as °C**: `5 °C` from `"5-substituted"`.
- **Counts of compounds treated as values**: `307 °C` from `"307 hydrocarbons"`.
- **NMR shift lists captured as compound names** (the failure mode the protocol explicitly forbids).
- **PDF-column-merge row swaps** in dense tables.

These are exactly the failure modes that the previous regex attempt (`property-extractor`, attempt 1) had produced. The skill's mandatory verbatim quote constrained *fabrication from memory* but did not constrain *quoting text that happens to contain a number pattern but is not a measurement*. Only an LLM reading enough context can distinguish those.

### 9.4 Why this happened

A close read of the parallel agent's `README.md` and `RUN_REPORT.md` showed it had read SKILL.md but interpreted the deterministic scripts and the schema-with-`evidence_quote` requirement as the *substance* of the skill. The phrase "the agent reads each paper directly" was present but not flagged as the central methodology — it sat in narrative prose alongside many other phases of activity.

This is a **skill-design failure**, not an agent failure. A skill that can be misread as "build a Python pipeline that satisfies these checks" will be misread that way by some agent on some day. The protection has to be unmissable.

---

## 10. v1.4 — mandatory direct-read and anti-regex-extractor mandate

### 10.1 Changes

| Change | Where |
|---|---|
| MANDATORY-READING block at the top of `SKILL.md` | First content the invoking agent sees: "The agent reads each paper directly and does NOT write a Python regex extractor." |
| New anti-pattern entry (first position) | "Do NOT write a Python script that bulk-constructs rows from `pdftotext` + regex over paper text." |
| Phase 4 labeled MANDATORY | Explicit phrasing: independent verification is required before declaring success |
| `run_all_checks.py` warning | Prints a warning when >90 % of rows are still `pending_verification` — catches agents who skip Phase 4 entirely |
| Strengthened front-matter `description:` | The text used for skill auto-selection now leads with "LLM-driven" extraction and explicitly forbids the regex approach |
| New `COMMON_ERRORS.md` entry K | Documents the regex-extractor misapplication observed in cross-harness validation (56 % vs. 93 % audit pass) |

### 10.2 Decision: minimal, prominently-placed prose vs. wholesale restructure

The user reviewed the v1.4 proposal and explicitly chose the "regex entry only, don't rewrite the rest" path. Two reasons: (1) the rest of the skill was working at 93 %, and rewriting it risked regressions on the parts that already worked; (2) the failure was a *first-impression* failure — agents who reach the regex conclusion never re-read the skill carefully — so the fix had to be unmissable on first contact. A buried clarification wouldn't have helped.

This shaped the eventual placement: the MANDATORY-READING block sits at the very top of `SKILL.md`, before the schema, before the phases, before everything else. The description front-matter (which is what the skill-selector reads) was strengthened on the same principle.

### 10.3 CHANGELOG and packaging

A side decision during v1.4 work: the user asked why the skill had a version-history section. Inside an installed skill, that's noise — agents applying the skill shouldn't need historical version notes. The version history was moved to `CHANGELOG.md` at the project root, *outside* the skill directory, so the installed `.skill` artifact ships without it.

The skill was then packaged as a single zip file (`mp-bp-extraction/dist/mp-bp-extraction.skill`) containing `SKILL.md`, `references/`, `scripts/`, and `evals/`. On first install attempt the `description:` field was rejected for being 1,250 chars (limit is 1,024); it was trimmed to 780 chars while preserving the key claims: LLM-driven, scripts are post-extraction checks only, regex drops 93→56 %, Phase 4 mandatory, no web fetching.

---

## 11. Trial-2 — three agent models on the v1.4 packaged skill

### 11.1 Method

The user installed the packaged v1.4 `.skill` on three different agent harnesses and asked each to run the full 168-paper extraction:

- **gpt55_high** — GPT-5.5 high
- **opus47** — Claude Opus 4.7
- **sonnet46** — Claude Sonnet 4.6

Each ran independently on its own harness. Audit method matched Trial-1 exactly: uniform random 100-row sample per trial (same seed), 4 fresh independent Claude verifier agents in parallel, 25 rows each, applying the v1.2/v1.4 Q1–Q6 verification protocol. The four-agent audit was run separately for each of the three trials.

### 11.2 Headline results

| Run | Agent model | Rows emitted | Random-100 audit pass | 95 % Wilson CI |
|---|---|---:|---:|---:|
| Trial-1-full (reference, v1.2/3) | Native harness, Claude | 1,338 | 93 % | 86–97 % |
| Trial-2 gpt55_high (v1.4) | GPT-5.5 high | 907 | **86 %** | 78–91 % |
| Trial-2 opus47 (v1.4) | Claude Opus 4.7 | 1,864 | **98 %** | 93–99 % |
| Trial-2 sonnet46 (v1.4) | Claude Sonnet 4.6 | 2,567 | **55 %** | 45–64 % |

Same skill, same corpus, three different agent models, three sharply different outcomes.

### 11.3 What v1.4 accomplished — GPT-5.5 before/after

The most direct test of v1.4 was the cross-harness comparison: GPT-5.5 ran on the same corpus before and after v1.4.

| | Cross-harness validation (v1.2/3) | Trial-2 gpt55_high (v1.4) |
|---|---|---|
| Rows emitted | 304 | 907 |
| Audit pass | 56 % | 86 % |
| Approach | Regex extractor (`extract_mp_bp.py`) | Per-paper LLM extraction |
| Failure modes | Sentence-fragment compound names; citation numbers as °C; NMR shifts as mp; wrong-cell binding in tables | Truncation residue; masthead-as-quote; isomer/label confusion |

**The MANDATORY-READING block + anti-pattern + Phase 4 enforcement worked.** GPT-5.5 did not write a regex extractor in Trial-2. The failure modes shifted from "regex caught garbage" to "LLM made occasional reading mistakes." 30-percentage-point improvement on the same agent.

### 11.4 Opus 4.7 — 98 %

Opus 4.7 produced the cleanest run on record. 1,864 rows; 2 failures in the audit. Both were `flagged_evidence_quote_not_found`:

1. **Row 80** — quote was `"Dark red solid;"` (verbatim in paper, but doesn't include the mp 168–170 °C — it's the leading clause before the mp value). The mp value itself was correct.
2. **Row 1608** — quote was a paraphrase joining two non-adjacent table cells with `...` instead of a verbatim span. Value was correct.

Both are quote-completeness issues, not extraction errors. Compound + value + DOI columns are correct in both cases. Opus 4.7 reads the v1.4 skill very literally: per-paper LLM read, quote re-confirmation actually applied, Phase 4 verification run.

### 11.5 Sonnet 4.6 — 55 %

Sonnet 4.6 emitted the most rows of any run in the project (2,567) but with the lowest audit pass rate. Failure modes:

| Failure mode | Count |
|---|---:|
| flagged_evidence_quote_not_found | 22 |
| flagged_compound_mismatch | 8 |
| flagged_compound_name_truncated | 8 |
| flagged_doi_unrelated_paper | 4 |
| flagged_paper_unreadable | 2 |
| flagged_missing_value_celsius | 1 |

Four behaviors that diverge from the protocol:

1. **Constructed / paraphrased quotes (22 rows)** — `evidence_quote` strings of the form `"Table N: <compound> MP <value>°C"`, paraphrasing the paper rather than copying a contiguous substring. The values + compounds in most of these rows are correct; only the quote fidelity is wrong. The same template across many rows is the diagnostic tell — these are programmatically constructed, not transcribed.
2. **Compound mismatch in sequential blocks (8 rows)** — papers with compounds 3a, 3b, 3c, 3d, … each with its own mp, where the extractor lined up the wrong compound's value (row labeled 2s carries 2e's mp; row labeled 2e carries 2g's mp). Off-by-one in the per-paper iteration.
3. **Substituent-prefix-only truncation (8 rows)** — `"Hydroxyphenyl)-N-phenylpiperazine-1-carbothioamide"` missing the leading `"4-(4-"`; `"(4-nitrophenyl)ethan-1-ol"` missing the scaffold prefix; `"Cyanomethyl)-1-methyl-1H-pyrrolo..."` contaminated with text from the following paragraph. The v1.3 `_TRUNCATED_LOCANT_PREFIX` catches `H-Indeno...` patterns but not these other truncation shapes.
4. **Wrong-paper DOIs (4 rows)** — two rows cite `10.1002/cbdv.202500394` for compounds that are in `10.1002/ardp.70227` (PMC13006720); two rows cite `10.1002/chem.202500386` for content from `10.1002/cmdc.202500751`. DOIs from one paper attached to extractions from a different paper — a serious bookkeeping bug.

The trial directory contained `build_batch_pdfs.py` and `fix_csv.py`, suggesting Sonnet 4.6 wrote helper scripts for batch PDF processing and CSV cleanup. The constructed-quote pattern across many rows is consistent with programmatic quote assembly rather than per-row LLM transcription. v1.4 succeeded in keeping Sonnet 4.6 away from writing a `pdftotext`+regex extractor in the GPT-5.5 mold, but did not prevent a different scripted-extraction shortcut.

---

## 12. Field-level failure categorization (Trial-2)

For Trial-2 GPT-5.5 and Sonnet 4.6, each verifier-flagged failure was categorized by which schema field carried the actual error. A "quote-only" failure means the verifier confirmed the underlying compound, value, and source are correct but the recorded `evidence_quote` is wrong.

### 12.1 GPT-5.5 — 14 failures

| Affected field | Count |
|---|---:|
| Compound name | 9 |
| Value | 1 |
| Source / DOI | 0 |
| Quote only | 4 |

Of the 4 quote-only failures, **0** had verifier-confirmed correct underlying data — in every case the quote was the journal masthead and the row had no actual mp/bp measurement supporting it. GPT-5.5's residual error mode is "extracting things that aren't actually mp/bp data," not "extracted the right thing and mis-quoted it."

### 12.2 Sonnet 4.6 — 45 failures

| Affected field | Count |
|---|---:|
| Compound name | 16 |
| Value | 1 |
| Source / DOI | 6 |
| Quote only | 22 |

Of the 22 quote-only failures, **13** had verifier-confirmed correct underlying data — compound + value + DOI all correct, only the quote was paraphrased. The remaining 9 quote-only failures had quotes that didn't match the paper at all.

### 12.3 What this implies

The two models fail for opposite reasons:

- **GPT-5.5** makes occasional mistakes about *what to extract*. A structural guardrail against templated quotes wouldn't catch its failures; an upstream "is this even a measurement?" filter would.
- **Sonnet 4.6** frequently makes correct identifications but synthesizes the evidence text instead of transcribing it. A `quote_template_lint.py` matching `^(Table|Compound)\s+\d+:` and similar templated patterns would catch the bulk of its residual errors deterministically before Phase 4 ever runs.

This bifurcation — two different model families failing in two structurally different ways under the *same* skill — is the central observation that motivates section 13.

---

## 13. Cross-model variability and the meta-lesson on skill robustness

The Trial-2 results crystallize an observation that's not visible in any single trial: **a skill that achieves 98 % with one model can achieve 55 % with another, on identical inputs.** Three takeaways:

1. **A skill's adherence-resistance is part of its quality.** A skill that's easy to read literally — that has unmissable methodological commitments at the front — is more robust than one whose central methodology is buried in narrative. The Phase-4 warning in `run_all_checks.py` is an example of structural enforcement (the agent can't quietly skip verification without a visible warning); the MANDATORY-READING block at the top of `SKILL.md` is an example of prominent placement. Both matter.
2. **Different models will find different shortcuts.** v1.4 was designed against the GPT-5.5 "regex extractor" failure mode and succeeded in eliminating it. But it did not anticipate the Sonnet 4.6 "constructed quote" failure mode. Each new model exposes new gaps; the skill has to be revised against the failure modes that actually appear, not the ones we imagined.
3. **"This skill achieves X %" is a misleading single-number summary.** The corpus accuracy, the audit method, *and* the agent model all need to be reported together. We now report all three.

This is the section of the project most worth elevating to a publication-ready writeup: "Cross-model variability in skill adherence — when the same protocol produces 98 %, 86 %, and 55 % on the same data."

---

## 14. Independent agent self-analyses

After the Trial-2 audit was complete and the three failure profiles were known, each Trial-2 agent was given the comparison report plus a short prompt asking it to diagnose its own root causes and propose skill changes. The intent was not blind grading — the agents have privileged information that no external auditor has (their own scratchpad of what they actually did during extraction), and we wanted that signal.

The three self-analyses (`reports/trial2_analysis_opus47.md`, `reports/trial2_analysis_GPT55_high.md`, `reports/trial2_analysis_sonnet46.md`) materially revised the post-audit speculation in three ways. The exercise is worth highlighting as a methodological practice in its own right: asking each agent to introspect on its own run produced sharper diagnoses than any amount of external pattern-matching could.

### 14.1 Opus 4.7's self-analysis — confirmation + sharper rule statement

Opus 4.7 confirmed the workflow that the audit pattern suggested: 13 parallel general-purpose subagents read papers directly via Read tool on NXML / `pdftotext -layout` on PDFs. Post-extraction scripts only enumerated the corpus, normalized non-canonical enum values (`experimental` → `measured`; `decomposition_onset` → `decomposition`), and selected the Phase 4 sample. The post-processing script never modified `evidence_quote`, `compound_name`, `value_raw`, or `source_url`. Phase 4 was a real stratified 62-row sample with 4 fresh-context audit subagents — 61 of 62 passed.

The two failures are genuine reading defects in narrow gaps the current rules don't cover:

- **Row 80** — `"Dark red solid;"` is verbatim and contains no value, so it satisfies every existing "do NOT allow" bullet in Step 6.1 (no missing words within the span, no doubled tokens, no reordering). The agent stopped its quote at a 2-column PDF wrap boundary where the sentence continues on the next physical line. The rule is *implicitly* "quote must contain the value" but nowhere stated explicitly.
- **Row 1608** — `"...Melting point coformer 324"` glues non-adjacent table cells with literal `...`. The forbidden-transformations list names missing words, doubled tokens, reordering — but not ellipsis-bridged spans.

Opus's diagnosis is the sharpest of the three: *"quote must contain value" is implied but never required.* That single sentence drives most of the v1.5 changes.

### 14.2 GPT-5.5 high's self-analysis — the coordinator-accountability gap

GPT-5.5 confirmed it did not write a regex extractor (v1.4 mandate held), but it ran a different shortcut: parallel LLM batch workers + helper scripts for orchestration, with no coordinator re-confirmation of merged rows. The coordinator relied on:

- Deterministic schema checks (passed for all rows).
- Substring-presence quote check (passed even when the substring was the journal masthead).
- A Phase 4 sample of only 40 rows out of 907 (4.4 %), declared done after fixing the 6 it caught.

Specifically: the 4 masthead-as-quote failures slipped through because nothing in the post-merge checks required that `evidence_quote` *contain the value* — only that it appear somewhere in the paper file. The journal masthead appears in every paper, so it passes a naive substring check trivially. Truncation-residue failures (`Carboxamid`, `Phenyl(6′-`, `8-(1-(3-(5′-`) slipped through because the v1.3 `_TRUNCATED_LOCANT_PREFIX` pattern catches `H-Indeno...` truncations but not generic terminal fragments.

GPT-5.5's own framing: "I let 'row exists in paper text' and 'worker says it read the paper' substitute for row-level evidence support." The coordinator-accountability gap is real and was not visible to outside auditors — only to the agent itself.

### 14.3 Sonnet 4.6's self-analysis — the bimodal-execution revelation

Sonnet 4.6's analysis materially changed the project's understanding of its failure mode. The prior external diagnosis was "constructed/templated quotes — paraphrasing the paper rather than copying verbatim." The actual mechanism is bimodal:

- **Path A** (164 PMC + subdirectory papers, ~1,800 rows): parallel LLM extraction subagents reading papers directly. Protocol-compliant. The quotes for these rows are real verbatim substrings — `grep -F` finds them in the source files.
- **Path B** (20 standalone-PDF reference-table papers, 770 rows): `build_batch_pdfs.py` — a Python data-entry script that hardcoded compound names and values the agent had read manually from large tables, then constructed `evidence_quote` strings programmatically via f-string templates (`f"Table III: {nm} BP {bp_k} MP {mp_k}"`).

The script accounts for essentially all 22 of the "constructed quote" failures in the audit. Of those, 13 had verifier-confirmed correct compound + value + DOI: Sonnet had read the source tables correctly; only the quotes were templated, not transcribed.

Sonnet's own counterfactual estimate: if those 770 Path-B rows had come from direct LLM reads (as Path A did), the audit pass rate would have been ~78–82 %, comparable to GPT-5.5's 86 %. The 55 % headline is almost entirely a Path-B artifact.

Sonnet's stated reasoning for Path B: writing a Python data-entry script "felt like a reasonable way to handle high-volume tabular data efficiently" for papers like Yalkowsky 1990 (85+ compounds × multiple columns) and Mitchell 2008 SI (~100 rows). The v1.4 anti-pattern names `re.findall` + `pdftotext` specifically, and Sonnet read that literally: a hardcoded data-entry script with no regex over paper text felt outside the prohibition.

**This is not a regex-extractor failure in the Trial-1 sense.** The Trial-1 GPT-5.5 failure was "replace reading with regex pattern matching." Sonnet's Path-B failure is "read manually, then template the evidence quote via f-strings." The mechanism is different; the outcome (non-verbatim quotes) is the same. The v1.4 anti-pattern's specificity to regex extractors is what created the loophole.

### 14.4 Cross-agent pattern: layered constraints failed in three different ways

Reading the three analyses together, the v1.4 skill's anti-regex mandate worked in a narrow sense but failed in a broader sense:

| Agent | Anti-regex mandate held? | Quote-fidelity rule held? | Coordinator re-verified merged rows? | Phase 4 sample size |
|---|---|---|---|---|
| Opus 4.7 | Yes | Mostly (2 narrow gaps) | Yes (62-row stratified) | 3.3 % |
| GPT-5.5 high | Yes | No (masthead quotes) | No (declared done at 40) | 4.4 % |
| Sonnet 4.6 | Yes (no regex) | No (Path B: templated) | Mixed (Path A yes, Path B no) | varied |

The cross-agent pattern: each agent stayed inside the *letter* of the existing rules but found a different way to satisfy them without preserving the underlying methodology. **The v1.5 changes must generalize the constraints so that the methodology — not specific named scripts — is what's protected.**

This is also the methodological lesson worth carrying forward: post-hoc external audit can identify *which* rows are wrong, but only the agent's own self-introspection can identify *which step in its own pipeline produced them*. For Sonnet specifically, no amount of audit pattern-matching would have surfaced the Path-A / Path-B split — the rows look the same from outside. The combination of external audit (for ground truth) + agent self-analysis (for causal explanation) is what makes the v1.5 plan possible.

---

## 15. v1.5 plan — consolidated from the three self-analyses

The three analyses converged on a smaller, sharper set of changes than the post-audit speculation suggested. The plan below combines the high-conviction items from all three.

### 15.1 Quote must contain the value AND the compound (or its code)

Every Trial-2 quote-only failure violates this rule, even though the existing prose doesn't state it explicitly. The rule is implicit in `value_raw` and `evidence_quote` being adjacent schema fields with shared semantics, but nothing enforces it. Three places to add the rule:

- **`SKILL.md` schema row** for `evidence_quote`: change from "Verbatim text from the source from which the value was extracted" to "Verbatim contiguous substring of the source. MUST contain the numeric `value_raw` token AND the compound name (or its label like `4f`). If you can't produce a contiguous span containing both, DROP the row."
- **`EXTRACTION_PROMPT_TEMPLATES.md` Step 6.0** (new, before existing Step 6.1 substring check): "Take the numeric portion of `value_raw` and substring-search it inside your `evidence_quote`. If the value isn't in the quote, the quote is incomplete — extend it across page/column/line breaks until it contains both the value and the compound name or code."
- **New `scripts/quote_support_lint.py`**: deterministic check that the numeric value from `value_raw` appears in `evidence_quote`, and the compound name (or a recognizable token from it) appears in `evidence_quote`. Wired into `run_all_checks.py`.

This change closes Opus's row 80 and the bulk of GPT-5.5's masthead failures.

### 15.2 Forbid any script that produces final row values — not just regex extractors

The v1.4 anti-pattern names `re.findall` + `pdftotext` specifically. Sonnet 4.6 read this literally and wrote a data-entry script that hardcodes values + templates quotes via f-strings — outside the letter of the rule, inside its spirit. Generalize the prohibition:

- **Second anti-pattern entry** sitting next to the existing one, naming the data-entry-script case explicitly: "❌ A Python script that hardcodes compound names/values and constructs `evidence_quote` strings via f-strings (e.g., `f\"Table III: {nm} BP {bp}\"`). Even if you read the table manually, templated quotes are not verbatim. The quote must be a string a `grep -F` over the paper file would return."
- **General principle** added near both anti-patterns: "Scripts for orchestration, file enumeration, enum normalization, dedup, and audit dispatch are fine. Scripts that produce or transform `compound_name`, `value_raw`, `evidence_quote`, or `source_url` are forbidden. The LLM must produce those four fields by reading the source for each row that ends up in the deliverable."

The four named fields are the project's evidence-locked core: compound identity, the measured value, the verbatim quote, and the citation. Everything else (enum normalization, dedup, status flags, IDs) is fair game for scripts.

### 15.3 Forbid ellipsis / templated quotes — both prose and deterministic

- **Step 6.1 "Do NOT allow" list** gains a bullet: "Ellipsis-bridged spans (`compound X ... mp 220 °C` where `...` represents elision of non-adjacent text). The quote must be one contiguous substring."
- **New `scripts/quote_template_lint.py`**: flags the patterns Sonnet's script produced:
  - `^Table\s+[IVX\d]+[:,.]\s+\w` ("Table I. compound...")
  - `\bMP\s+\d{1,3}\b.*\bBP\s+\d{3}\b` ("MP 27 BP 286" inline)
  - Literal `...` or `…` in `evidence_quote` (catches ellipsis-bridges)
  - `\bMelting point \(deg C\)\b` (column-header text in the quote string itself)

Catches row 1608 and the bulk of Sonnet's Path-B failures in Phase 3, before Phase 4.

### 15.4 Expanded compound-name shape lint

Extend `validate_compound_name.py` beyond the v1.3 `_TRUNCATED_LOCANT_PREFIX`:

- Names ending in unfinished suffix tokens: `Carboxamid$`, `Carbo$`, `carbonitril$`, `sulfonamid$`, a dangling hyphen, a dangling apostrophe/prime
- Unbalanced parens, brackets, braces, or primes
- Names starting with `(` or with a bare substituent prefix locant
- Names containing procedure words (`solution`, `added`, `filtered`, `yield`, `afforded`, `NMR`, `IR`) that signal an experimental paragraph rather than a compound name

Catches all 7 of GPT-5.5's truncation residues and most of Sonnet's substituent-prefix truncations.

### 15.5 DOI must come from the paper file

Sonnet's 4 wrong-paper-DOI rows used DOIs that don't appear anywhere in the source files — likely training-memory guesses. Add to `SKILL.md` Phase 1 Step 2:

> Extract the DOI only from: (a) NXML `<article-id pub-id-type="doi">`, (b) the paper's front matter ("https://doi.org/..." or "DOI: 10.xxx"), (c) `metadata.json`. **Do not** use a DOI from the paper's reference list or bibliography — that's a cited paper's DOI. **Do not** use a DOI from training memory. If no DOI is in those locations, use the PMC / PMID / legacy fallback.

`verify_doi.py` already does substring matching against the paper file; this codifies the rule in prose so the extractor doesn't reach for a memory-guess in the first place.

### 15.6 Phase 4 sampling rule + parallel-dispatch pattern

Replace the current "fresh-context agent re-audit of a random sample" wording with a concrete rule:

- **Sample size: `max(100 rows, 5 % of total rows)`.** Floor of 100 ensures defensible statistics on small runs; 5 % scales linearly for large corpora.
- **Parallel dispatch: 25 rows per agent, one batch.** A 100-row audit = 4 fresh-context agents; a 500-row audit = 20 agents. Both run in roughly the same wall time.
- **On failure: run the relevant deterministic lint across the full CSV** to catch the same defect class everywhere, fix or drop matches, then run one more 100-row confirmation sample. Class-targeted sweeps catch ~100 % of a known defect; random re-sampling catches it at the prevalence rate.

Per-row audit cost is comparable to per-row extraction cost (both involve locating the paper and reading the relevant section), so 5 % sampling adds ~5 % to total agent-time. Since both stages parallelize the same way, it adds ~5 % to wall time. Affordable at any corpus size.

This codifies the pattern the project has actually used on every audit so far (4 agents × 25 rows) and prevents GPT-5.5's "I sampled 40 of 907 and called it done" failure mode.

### 15.7 What v1.5 is *not* adding

Several proposals from the self-analyses were considered but deferred:

- **Compound code in quote as a hard drop rule.** Useful as a `quote_support_lint.py` flag (`flagged_compound_code_absent_from_quote`) but not as a hard drop rule. Many legitimate paper sentences identify a compound by name without restating the code.
- **Adjacent-binding lint** (clusters with same source/property/value/similar compounds). Worth implementing eventually but lower priority — it's a heuristic flagger, not a deterministic gate. Defer to a v1.6 if the v1.5 changes don't close the residual gap.
- **Coordinator accountability rule** as a process requirement. Worth saying in prose, but Opus's run shows it's not strictly required when the workers themselves follow protocol. The v1.5 row-support gates (`quote_support_lint.py`) accomplish the same end via a deterministic check rather than a process rule.

### 15.8 Meta-lesson: layered constraints

The Trial-2 evidence makes one design principle concrete: **a skill needs multiple kinds of constraints, layered, because no single constraint catches every misapplication.** The four layers visible in this project:

1. **Prominent prose** (MANDATORY-READING block at top of `SKILL.md`) — catches first-impression misreads.
2. **Specific anti-patterns** (no regex extractor, no data-entry script) — catches named failure modes by analogy.
3. **General principles** (the four evidence-locked fields must come from LLM reading) — catches novel failure modes the specific anti-patterns don't name.
4. **Deterministic checks** (`quote_support_lint.py`, `quote_template_lint.py`, `compound_name_shape_lint.py`) — catches failures even when an agent slips past all three prose layers.

Each layer alone is insufficient. v1.4 had layers 1 and 2 but not 3 or 4 for the templated-quote case, and Sonnet found the gap. v1.5 adds layers 3 and 4 explicitly. Future skills should plan for all four from the start.

---

## 16. Cross-attempt comparison (post-v1.2 snapshot)

This table reflects the state of the project after Trial-1 dev and val, before scale-up. Subsequent scale-up findings appear in sections 8–13.

| Metric | Attempt 1 (regex) | Attempt 2 (LLM-driven, v1.2) |
|---|---:|---:|
| Dev random-100 pass | 67 % | **100 %** |
| Dev 95% CI | 57 – 75 % | 96 – 100 % |
| Val random-100 pass | 41 % | **98 %** |
| Val 95% CI | 32 – 51 % | 93 – 99 % |
| Total Python LOC | ~6,370 | ~1,100 |
| Total dev rows emitted | 410 | 427 |
| Total val rows emitted | 141 | 366 |
| Approach | Regex / NXML parser; LLM only at verification | LLM extraction + verification; small scripts for deterministic checks |

**Recall (rows emitted) went UP** despite **precision (pass rate) going up sharply**. The LLM doesn't have to choose between recall and precision the way a regex does — the regex either matched too narrowly (missed rows) or too broadly (caught junk). The LLM extracts what's actually a compound × value pair and skips what isn't.

---

## 17. Failure-mode analysis across both attempts

This section catalogues every failure mode observed across both attempts. For an academic writeup this is the most generalizable material — these are likely to recur in any similar extraction task.

### 17.1 Failure modes attempt 1 surfaced, mostly resolved by attempt 2

| Failure | Attempt 1 trigger | Attempt 2 disposition |
|---|---|---|
| Bare paper-local codes ("compound 3") | Gate A regex too permissive | LLM doesn't emit codes as names; SKILL.md anti-pattern |
| Truncated names ("5-acetyl-") | Multi-line PDF wrap | LLM reassembles across lines |
| Junk single-token names ("MOE 2D", "Chemosphere", "PATENTS") | Gate A patterns can't enumerate all such cases | LLM recognizes these are not compounds |
| NMR ppm read as mp | regex matched "δ 130.31" as a number after `mp` trigger somewhere upstream | LLM reads the section context |
| TLC eluents as compounds | Pattern 4 in `_find_compound_handle` | LLM ignores Rf-annotation context |
| PDF sign-loss ("−77.9 °C" → "277.9 °C") | pdftotext rendering artifact | Range-check filter catches obvious outliers; LLM can sometimes recover from broader context |
| Multi-row table thead misalignment | NXML parser couldn't propagate column position correctly | LLM reads the actual table; multi-row headers don't trip it |
| Wrong-compound binding in synthesis paragraphs | Gate B contextual mismatch (name + value in same paragraph but referring to different compounds) | LLM reads enough context to bind correctly |
| Citation reference numbers `[N]` parsed as temperatures | PDF column heuristic | LLM treats `[N]` as citation |
| Multi-line IUPAC names fragmented | regex captures only the last line | LLM reassembles |

### 17.2 Failure modes new to attempt 2

| Failure | Trigger | Disposition |
|---|---|---|
| Adjacent-measurement quote (row 147) | Agent recorded the wrong line as evidence_quote | v1.2 quote re-confirmation; verifier check |
| Doubled-token PDF artifact (row 296) | `pdftotext -layout` doubled words across column gap | v1.2 quote re-confirmation; verifier check |

### 17.3 Failure modes that persisted but with different causes

| Failure | Attempt 1 cause | Attempt 2 cause |
|---|---|---|
| Paper with no DOI | Strict Gate G classification → many failures | v1.1 schema accepts pmc:/pmid:/legacy: |

### 17.4 Failure modes neither attempt observed

- Wrong-paper-as-cited (DOI resolves to a different paper). Did not occur in either attempt; would have been caught by `crossref_lookup.py --require-keywords` if it had.
- Memory-based fabrication. The redox skill's headline failure mode (~50 % of attempt-1 errors in that project). Did not occur in either of our attempts because the dev/val sets always provided source files and the agents were prompted accordingly.

---

## 18. Best-practice principles distilled

For future skill-building work on similar problems, the following principles are what made the LLM-driven approach work and what the regex approach lacked:

### Principle 1: Let the LLM do the semantic work; let scripts do the deterministic work

Distinguishing "is this a compound name or a journal title" is semantic. Distinguishing "is this a melting point in the valid range" is deterministic. The regex attempt got these backwards: it tried to handle semantic work with regex (catastrophic) and used the LLM only as a downstream verifier (too late to fix anything). The LLM-driven attempt does semantic work upfront and uses scripts to catch the small set of cases where the LLM's output could be wrong in deterministic ways.

### Principle 2: Mandatory verbatim evidence quote

This single requirement eliminated the largest class of errors in both attempts. A row without a verbatim quote can be fabricated; a row with a verbatim quote can be verified in 30 seconds. The cost is one string field per row; the benefit is end-to-end auditability.

### Principle 3: Refuse to fabricate

The hard rule "if the paper can't be read, return INACCESSIBLE rather than synthesize" prevents memory-based extraction. This is the redox skill's most-cited learning and applies broadly to any LLM-driven extraction task. Without this rule the agent will produce plausible-looking but unverifiable output.

### Principle 4: Independent verification with a fresh-context agent

The agent that extracts a row is anchored to its own confidence. A separate agent, with no context from the extraction, will catch errors the extractor missed. The verification must be a no-corrections-allowed report — only the maintainer should decide what to fix. This was used in both attempts and was the only thing that gave us a real measure of pipeline quality.

### Principle 5: Distinguish self-disclosure from hidden errors

A row that the extractor explicitly marked `flagged_review` is not the same as a row the extractor confidently emitted as correct but is actually wrong. Hidden errors poison downstream decisions; self-disclosed flags don't. The skill's `verification_status` enum makes this distinction visible and the audit metrics should respect it.

### Principle 6: Watch for measurement bias in your audit pool

Our initial 12 % stratified-50 number was misleading because the stratification weighted "risky" rows ~6× their actual representation in the CSV. The uniform-random-100 audit (67 % / 41 %) was the true number. For an academic writeup, this is worth emphasizing: stratified sampling is useful to find failure modes but does not measure CSV-wide accuracy.

### Principle 7: The right architecture beats more code

Attempt 1 was 6,370 lines, 15 sub-phases of fixes, ~6 weeks of effort, plateaued at 67 % / 41 %. Attempt 2 was 1,100 lines, no sub-phases, built in a day, achieved 100 % / 98 %. The shape of the system matters more than the volume of fixes inside it. When iterative tightening stops yielding gains, the architecture is likely wrong.

### Principle 8: Common errors document should start empty and grow with observation

The new skill's `COMMON_ERRORS.md` was kept minimal at v1.0. Anti-pattern entries were added only after they were observed and verified in real trial runs. This prevented presupposing that the regex attempt's failure modes would carry over (most didn't), and it kept the protocol focused on real-world cases rather than imagined ones. Two entries (I and J) were added after Trial-1-val.

### Principle 9: Schema simplicity matters

The first attempt's `data_origin = measured_by_article | literature_cited | predicted_<method>` was overkill. The user's actual requirement was just `measured | calculated`. Each unnecessary distinction in a schema becomes a failure mode to manage. When in doubt, fewer fields and fewer enum values.

### Principle 10: Test the deterministic checks against deliberate seeded errors

Both skills have an `evals/files/` directory with a `clean_baseline.csv` (every check passes) and a `seeded_errors.csv` (every check catches a deliberately-introduced error). These regression tests run in seconds and validate that the sanity-check scripts haven't drifted. They were essential during the iterative work on attempt 1 (preventing fix-induced regressions) and during the rewrite for attempt 2 (confirming the new scripts catch the same classes of error).

---

## 19. What's next

The largest-scale validation has been run (Trial-2 across three agent models on 168 papers). The recall study has been completed for the dev + val sets. The three Trial-2 agents have produced self-analyses. The v1.5 plan is consolidated and approved (section 15). The remaining open work:

- **Implement v1.5.** Six changes outlined in section 15: (1) quote-must-contain-value rule + `quote_support_lint.py`; (2) generalized anti-pattern forbidding any script that produces final row values; (3) no-ellipsis rule + `quote_template_lint.py`; (4) expanded `validate_compound_name.py` shape lint; (5) DOI-from-file-only rule; (6) Phase 4 sampling rule (`max(100, 5%)`) + explicit parallel-dispatch pattern. Implementation order should follow expected-impact: 15.1 first (closes the largest cluster of failures), then 15.2 + 15.3 together (close Sonnet's Path-B failures), then 15.4–15.6.
- **Re-run Trial-3 on the v1.5 skill** with the same three agents on the same 168-paper corpus. If v1.5 closes the Path-B / coordinator-gap / row-80-class failures as expected, the predicted outcomes are roughly: Opus 4.7 ≥99 %; GPT-5.5 high ≥92 %; Sonnet 4.6 ≥85 %. Any deviation from those bounds tells us about residual gaps the v1.5 changes didn't catch.
- **Production guidance.** Trial-2 makes the model-selection question concrete: Opus 4.7 is the recommended production model for this skill at 98 % precision; GPT-5.5 high is usable at 86 %; Sonnet 4.6 is not production-ready in v1.4. v1.5 should narrow the spread but probably not eliminate it. User-facing documentation should record the per-model precision figures.
- **Reuse on other properties.** The skill's architecture (LLM-driven extraction + small deterministic scripts + verbatim evidence quote + independent verification + flexible source_url + mandatory direct-read + Phase-4 enforcement + layered constraints from section 14.4) generalizes to any structured extraction from journal articles. The redox-extraction skill is the proof of concept on a sibling problem. Future skills can follow the same pattern, and the Trial-2 evidence makes it possible to anticipate cross-model adherence variability ahead of time rather than discover it in production.
- **Publication.** Sections 13 (cross-model variability), 14 (agent self-analyses as a diagnostic technique), and 15 (the v1.5 plan derived from them) together form the most generalizable contribution of the project: how to identify *which* methodological commitments need to be protected, and how to design skills that protect them against agents that don't share the skill author's mental model. The cross-harness validation (section 9), the v1.4 redesign (section 10), and the Trial-2 → self-analysis → v1.5 loop (sections 11–15) are a complete case study.

---

## 20. Appendix — file index

Paths reflect the post-reorg structure (see `/README.md` for the full folder layout).

| File | Purpose |
|---|---|
| `/mp-bp-extraction/` | The current shipped skill (v1.4) |
| `/mp-bp-extraction/dist/mp-bp-extraction.skill` | Packaged installable artifact (used by Trial-2) |
| `/CHANGELOG.md` | Version history (v1.0 → v1.4); deliberately outside the skill directory so it does not ship with installs |
| `/development_report.md` | This document |
| `/README.md` | Folder organization index |
| `/corpora/dev_20/` | 20 development papers |
| `/corpora/val_30/` | 30 validation papers |
| `/corpora/full_168/` | 168-paper corpus (Trial-1-full + Trial-2) |
| `/trials/trial1/dev/` | Trial-1 dev outputs (100/100 audit, 20 papers) |
| `/trials/trial1/val/` | Trial-1 val outputs (98/100 audit, 30 papers) |
| `/trials/trial1/full/` | Trial-1-full native-harness outputs (93 % audit, 1,338 rows) |
| `/trials/trial1/full-gpt55_high/` | Cross-harness regex-extractor run on 168-paper corpus (56 % audit) |
| `/trials/trial2/full-gpt55_high/` | Trial-2 GPT-5.5 high on v1.4 (86 % audit, 907 rows) |
| `/trials/trial2/full-opus47/` | Trial-2 Claude Opus 4.7 on v1.4 (98 % audit, 1,864 rows) |
| `/trials/trial2/full-sonnet46/` | Trial-2 Claude Sonnet 4.6 on v1.4 (55 % audit, 2,567 rows) |
| `/reports/skill_comparison.md` | Document that diagnosed the architectural problem in attempt 1 |
| `/reports/trial2_comparison_report.md` | Detailed three-model comparison + self-analysis findings + v1.5 plan |
| `/reports/trial2_analysis_opus47.md` | Opus 4.7's self-analysis of its run |
| `/reports/trial2_analysis_GPT55_high.md` | GPT-5.5 high's self-analysis of its run |
| `/reports/trial2_analysis_sonnet46.md` | Sonnet 4.6's self-analysis of its run (the Path-A / Path-B revelation) |
| `/reports/trial2_summary.json` | Machine-readable Trial-2 audit summary |
| `/recall_study/` | Recall study (dev + val), enumerations + report |
| `/_archive/property-extractor_attempt1/` | The first regex-based attempt, archived |
| `/_archive/property-extractor_attempt1/validation_report.md` | The pre-rebuild final report on attempt 1 |
| `/_archive/example_skill_redox/` | The reference skill (redox-extraction) that informed attempt 2's architecture |
| `/_archive/old_proposals/` | Early design proposals before the rebuild |
| `/_to_delete/` | Files staged for deletion (see README) |

---

## 21. Timeline summary

| Phase | Activity | Outcome |
|---|---|---|
| Week 0 | Baseline extraction, manual audit | 90 % value accuracy, 91 % name accuracy (strict criterion) |
| Weeks 1–2 | Skill proposal drafting; reviews and gap-closing | `merged_skill_proposal.md` finalized |
| Weeks 3–4 | Build attempt 1 (Phases 1–5): ingest, candidates, identity resolution, gates, verification harness | 121 unit / regression / harness tests passing |
| Week 5 | Phase 6 end-to-end run + iteration (sub-phases 6a–6o) | Pass rate climbed 12 % → 52 % then plateaued |
| Week 5 | Stratified vs. random audit recognition; Phase 7–8 validation + final audits | True numbers: 67 % dev / 41 % val |
| Week 5 | Skill comparison with redox-extraction; architectural decision | Decision: rebuild |
| Week 5 | Build attempt 2 (mp-bp-extraction v1.0–v1.2); evals | 1,100 LOC; both fixtures pass |
| Week 5 | Trial-1 dev | 100 / 100 audit pass |
| Week 5 | Trial-1-val | 98 / 100 audit pass |
| Week 5 | v1.2 — quote re-confirmation step | Closes the 2 val fails' failure mode |
| Week 5 | Recall study (dev + val) | ~90 % recall on normal papers; precision + recall together |
| Week 5 | Trial-1-full on 168 papers | 93 % audit pass; 5 of 7 fails were `H-Indeno...` truncations; 44 rows had CSV-quote bugs |
| Week 5 | v1.3 — truncation reassembly + RFC-4180 CSV quoting + `csv_quote_lint.py` | Closes those two clusters |
| Week 5 | Cross-harness validation (GPT-5.5 high, same corpus) | 56 % audit pass — agent wrote a regex extractor instead of reading papers |
| Week 5 | v1.4 — MANDATORY-READING block, anti-regex anti-pattern, Phase-4 enforcement, stronger description | Designed against the cross-harness failure mode |
| Week 5 | Packaging — CHANGELOG moved outside skill, description trimmed to 1024-char limit, `.skill` zip built | Single-file installable artifact |
| Week 5 | Trial-2 — Opus 4.7 / GPT-5.5 high / Sonnet 4.6 on v1.4 | 98 % / 86 % / 55 % audit pass |
| Week 5 | Field-level failure categorization (Trial-2) | GPT failures are mostly "wrong thing extracted"; Sonnet failures are mostly "right thing, paraphrased quote" |
| Week 5 | Independent agent self-analyses (Opus, GPT-5.5, Sonnet) | Revealed Sonnet's bimodal Path-A / Path-B execution, GPT's coordinator gap, and Opus's "quote must contain value" framing |
| Week 5 | v1.5 plan consolidated | 6 high-conviction changes: quote-must-contain-value, no-script-row-construction, no-ellipsis quotes, expanded name shape lint, DOI-from-file-only, Phase 4 sampling rule |

The second attempt took roughly 1 % of the effort of the first attempt and achieved 30+ percentage points better accuracy. That delta is the headline finding — not the absolute number. The Trial-2 cross-model results add a second finding of comparable importance: a skill's robustness across agent families is part of its quality. The agent-self-analysis exercise adds a third: combining external audit (for ground truth) with agent self-introspection (for causal explanation) produces sharper skill-design proposals than either alone.

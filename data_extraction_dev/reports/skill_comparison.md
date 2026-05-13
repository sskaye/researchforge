# Skill comparison — redox-extraction vs. property-extractor (mp_bp)

**Date:** 2026-05-11

## Summary

The redox-extraction skill achieved **96–100 %** on independent spot-checks over five trials. Our property-extractor skill is at **67 % dev / 41 % val** on a comparable random-sample audit.

The two skills tackle similar problems (extract numeric measurements + provenance from scientific papers), and the verification protocols are nearly identical. The performance gap is almost entirely **architectural**:

|  | Redox skill | Property-extractor (mine) |
| --- | --- | --- |
| Total Python LOC | \~1,360 | \~6,370 (4.7× larger) |
| Extraction engine | LLM agent reading the paper | Regex / NXML parsing scripts |
| LLM role | Primary extractor + verifier | Verifier only |
| Schema requires evidence quote? | **Yes (mandatory)** | No (we record evidence_location but don't enforce verbatim quote) |
| Refusal-to-fabricate built in? | **Yes (INACCESSIBLE rule)** | No |
| Sanity-check scripts | 8 small, focused | embedded in extraction logic |
| Last-trial verification rate | 92–100 % | 41–67 % |

I think we built the wrong shape of skill. The redox approach — small reusable scripts + reference docs + prompt templates that put the LLM in the driver's seat — would have produced a much better outcome with much less code.

## 1. Accuracy comparison, apples-to-apples

Both skills measure pass rates via independent verification (a fresh agent re-fetches the source and confirms each row). But the success criteria differ in important ways.

### Redox success criterion ("verified-among-accessible")

A row passes if all of these hold:

- DOI resolves to a real paper whose title is on-topic.
- `evidence_quote` is verbatim present at `evidence_location` in the cited paper.
- The molecule and value in the quote match what the row reports.
- The conversion arithmetic (if any) is correct.

This is essentially: **"can the reviewer reproduce the row's value from the cited source in 30 seconds?"**

### My MP/BP success criterion (six Yes/No/Cannot-determine questions)

- Q1 value present at location
- Q2 compound name standalone-interpretable
- Q3 identity tokens consistent
- Q4 `data_origin` correctly classified (measured / cited / predicted)
- Q5 `property_subtype` correctly classified
- Q6 DOI correct

PASS requires **all six** = Yes. Failing **any one** fails the row.

### Normalizing

Mapping my questions onto the redox criterion:

- Q1, Q3, Q6 are direct equivalents of redox's "evidence quote verbatim", "molecule-value match", and "DOI correct".
- Q2 is roughly equivalent to redox's "molecule field is not truncated / not a placeholder".
- **Q4 and Q5 don't have a direct redox equivalent.** The redox skill captures these via explicit schema fields (`data_type`, `value_directness`) but doesn't run a verification check on them.

If I drop Q4 and Q5 from my pass criterion (to match the redox criterion), my random-100 numbers become:

| Set | Strict (6Q) | Q1+Q2+Q3+Q6 only |
| --- | --- | --- |
| Dev | 67 % | \~80 % (estimated)\* |
| Val | 41 % | \~55 % (estimated)\* |

\* Estimated by subtracting Q4 / Q5 sole-failure cases. Dev has 25 Q4-No and 0 Q5-No rows; if \~10 of those failed ONLY on Q4 the relaxed rate would be \~77 %.

Even normalized, the gap is still **\~20 percentage points on dev and \~40 percentage points on val**, vs. redox's 96–100 %. The redox skill is fundamentally more accurate.

A few caveats on the comparison:

- Redox spot-checks are 15–31 rows; mine is 100 rows. Smaller samples → wider CIs (redox's 31/31 = 100 % has a Wilson 95 % CI of about 88–100 %).
- Redox has more rows per database (\~16k–24k) but only a few hundred are non-bulk-computational and audited. The 100 % verified rate applies to the audited slice, not all 16,098 rows.
- Redox trial 5's 92 % includes 2 propagated upstream-source errors that the protocol "couldn't have caught". By that standard, my val's khalifa failures are arguably "the source PDF text was the problem". But I think that excuse doesn't actually hold — most of my failures are extraction-pipeline bugs (NMR → mp, fragment names, column misalignment), not faithful transcription of bad source data.

## 2. Script vs. agent — primary architectural differences

### Redox skill: thin scripts, fat prompts

The redox skill is mostly **prose**:

- `SKILL.md` (this file is the brain): 350 lines describing the protocol, schema, the six phases, anti-patterns.
- 6 reference docs: REFERENCE_ELECTRODES.md (conversion table), COMMON_ERRORS.md (anti-pattern catalog with real examples), EXTRACTION_PROMPT_TEMPLATES.md (copy-paste agent prompts), VERIFICATION_PROMPT_TEMPLATES.md (the verifier prompt), SOURCE_DISCOVERY.md, SANITY_CHECK_SCRIPTS.md.
- 8 Python scripts totaling 1,360 lines. Each does one focused thing:
  - `find_open_access.py` — given a DOI, query Unpaywall / OpenAlex / Semantic Scholar / Europe PMC / CORE / Wayback, return URLs.
  - `crossref_lookup.py` — authoritative paper metadata; relevance keyword check.
  - `validate_smiles.py` — RDKit + chemistry plausibility.
  - `voltage_range_check.py` — flag voltages outside the plausible range for the chemical class.
  - `conversion_arithmetic.py` — verify the SHE-conversion math and the offset value.
  - `cross_source_consistency.py` — same molecule × same conditions across multiple sources should agree.
  - `verify_row.py` — per-row programmatic checks.
  - `run_all_checks.py` — umbrella runner that produces `flags.csv`.

**What the LLM does:** Reads the actual paper. Identifies values, molecules, references, conditions. Writes evidence-locked rows. Calls scripts as tools (not as the engine).

**What scripts do:** Discover open-access URLs. Validate fields. Catch a small set of known sanity failures. Nothing tries to *do* the extraction.

### Property-extractor (mine): fat scripts, no LLM in the loop until the end

My skill is mostly **code**:

- 20 Python files totaling 6,370 lines.
- `ingest_article.py` (643 lines): NXML parsing, PDF text scraping, DOI extraction.
- `adapter.py` (1,338 lines): regex trigger patterns, table parsing (NXML + PDF), compound-handle extraction with 4 fallback patterns, range parser, template-variable expansion, scaffold parsing, value normalization, data-origin classification, instrument detection.
- `validate_name.py` (327 lines): regex REJECT + REQUIRE + EXEMPT patterns. Tries to decide "is this string a valid compound name" via lexical rules.
- `resolve_compound_name.py` (345 lines): three-strategy resolver (exact text → code lookup → template expansion).
- `paper_type_classifier.py` (328 lines): regex-based classifier for synthesis / qspr / thermodynamic / review / unknown.
- Plus identity_token_check, dedup, verify_doi, verify_substring, audit_verifier, sample_for_verification, quarantine_failed_audits, build_label_dictionary, resolve_template_variables, build_candidate_index, emit_outputs, run_pipeline, validate_row, coverage_check, build_verification_bundle.

The LLM only appears at the END, as an independent verifier of the extraction pipeline's output. The actual extraction is entirely programmatic.

### What the LLM does well that scripts struggle with

Going down my random-100 failure list, the dominant failure modes are exactly the things an LLM would have caught instantly:

| My failure | What a script saw | What an LLM would see |
| --- | --- | --- |
| "GSE: predicted Tm" extracted as compound name | string with chemistry tokens | column label in a model-comparison table |
| "MOE 2D" as compound | passes pattern checks | a chemoinformatics descriptor name |
| "Chemosphere" as compound | single token with chemistry suffix | a journal name |
| 13C NMR ppm 130.31 as melting point | number after mp trigger | NMR chemical shift in spectroscopy section |
| CH2Cl2 as compound at mp 165 | valid formula | TLC eluent in Rf annotation |
| "PATENTS" as compound | non-empty string | dataset label in a QSPR paper |
| "PDF artifact 277.9" (real -77.9) | number in valid mp range | sign-loss in PDF text extraction |
| "Chloroquine" bound to Thalidomide's value | nearest-column-header in table | misaligned multi-row thead |
| khalifa fragment "Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl" | matches Gate A | substituent of a longer parent compound that crosses PDF line boundary |
| Compound 4d's mp 76 not in evidence excerpt | searches the wrong window | reads the synthesis section and finds the correct paragraph |

The redox skill bypasses all of these by letting the LLM read the actual paper and write a row with the evidence quote attached. The script never has to "guess" what the compound name is — the LLM puts it there directly, and a verifier later confirms it.

### What scripts do well that LLMs don't

- **Deterministic sanity checks**: RDKit SMILES validation, voltage-range-by-class, conversion-arithmetic verification. These run in milliseconds and never hallucinate.
- **Authoritative metadata lookup**: CrossRef DOI → paper title. The LLM is much worse at remembering paper metadata than CrossRef is at returning it.
- **Reproducible numeric processing**: deduplication, unit conversion, range midpoint calculations. Easy to test.
- **Cross-source consistency**: comparing the same molecule × conditions across multiple cited sources.

The redox skill uses scripts for exactly these things and nothing else.

## 3. Best overall approach

For an extraction task like mp/bp from primary literature, the redox skill's pattern is clearly better. Concretely, I would rebuild the property-extractor as:

### `mp-bp-extraction/` <!-- fmc:1 -->skeleton (proposed)<!-- /fmc:1 -->

```
mp-bp-extraction/
├── SKILL.md                              # Protocol, schema, phases, anti-patterns
├── scripts/
│   ├── find_open_access.py               # (shared from redox)
│   ├── crossref_lookup.py                # (shared from redox)
│   ├── validate_compound_name.py         # RDKit InChI / SMILES sanity; reject TLC eluents
│   ├── value_range_check.py              # mp ∈ [-220, 700] °C; bp ∈ [-220, 1000] °C
│   ├── unit_conversion_arithmetic.py     # K → °C, °F → °C; arithmetic verifier
│   ├── verify_evidence_quote.py          # confirm the verbatim quote is in the cited PDF
│   ├── dedup_within_paper.py             # (small — collapse duplicate rows from one paper)
│   ├── run_all_checks.py                 # umbrella runner
│   └── verify_row.py                     # per-row programmatic checks
├── references/
│   ├── COMMON_ERRORS.md                  # NMR-as-mp, fragment names, sign-loss, etc.
│   ├── EXTRACTION_PROMPT_TEMPLATES.md    # the agent prompts
│   ├── VERIFICATION_PROMPT_TEMPLATES.md
│   ├── PAPER_TYPE_GUIDE.md               # how to recognize synthesis vs review vs QSPR papers
│   └── DATA_ORIGIN_RULES.md              # how to set data_origin from paper context
└── evals/
    ├── evals.json
    └── files/                            # seeded-error fixtures
```

### <!-- fmc:2 -->Schema (required fields)<!-- /fmc:2 -->

```
id
verification_status
compound_name              # full IUPAC or common name; never truncated
property                   # melting_point | boiling_point | DSC_onset | etc.
value_celsius              # numeric, canonical °C
value_raw                  # as printed in source (e.g., "188-190 °C", "−77.9 °C")
relation                   # =, >, <, ~, ≈
data_origin                # measured_by_article | literature_cited | predicted_<method>
solvent                    # if mp/bp depends on a solvent system (rare for mp)
source                     # journal, year, vol, page (no authors)
source_url                 # DOI URL
evidence_location          # "Table 1 row 3", "p.6469 col 2 ¶ 3"
evidence_quote             # verbatim from source ← REQUIRED, MANDATORY
conversion_arithmetic      # when K/°F converted to °C, show the math; otherwise blank
notes
```

The `evidence_quote` requirement alone would have caught \~80 % of my failures, because the LLM either produces a quote that's actually in the paper (correct row) or can't (rejected before emission).

### The six phases

Mirroring the redox skill:

1. **<!-- fmc:3 -->Source preparation.<!-- /fmc:3 -->**<!-- fmc:3 --> Fetch via OA URLs; verify it's the right paper; identify mp/bp-bearing tables and paragraphs.<!-- /fmc:3 -->
2. **Evidence-locked extraction.** LLM reads the paper and writes one row per compound × property event with mandatory evidence_quote.
3. **Programmatic sanity checks.** SMILES validity, value-range plausibility, unit-conversion arithmetic, duplicate detection, paper-type-vs-data_origin consistency.
4. **Independent verification.** Fresh agent <!-- fmc:4 -->re-fetches the sourc<!-- /fmc:4 -->e and confirms each row's evidence_quote.
5. **Confidence tagging.** Use the same `verification_status` enum.
6. **Failure handling.** INACCESSIBLE &gt; fabrication. Flag rather than silently include.

### What we keep from the current implementation

A few pieces of my current pipeline are worth retaining:

- <!-- fmc:5 -->The paper-type classifier idea (synthesis / qspr / thermodynamic / review) — but enforced via an LLM prompt, not a regex classifier. The classifier exists in the redox skill as prose in COMMON_ERRORS, not as a script.<!-- /fmc:5 -->
- <!-- fmc:6 -->The value-range plausibility filter (\[-220, 700\] °C).<!-- /fmc:6 -->
- The unit-conversion-arithmetic check (K → °C, °F → °C).
- The duplicate-within-paper check.
- The DOI verification flow.

### What we drop

- `ingest_article.py` (643 lines of NXML/PDF parsing) — the LLM reads the paper directly via web_fetch / Read.
- `adapter.py` (1,338 lines of regex extraction) — the LLM identifies values + compounds.
- `validate_name.py`'s big REJECT/REQUIRE pattern list — the LLM's chemistry training is far better at "is this a compound name?" than any regex set. Keep only a small RDKit-based check for clearly invalid strings.
- `resolve_compound_name.py`'s three-strategy resolver — the LLM writes the compound name directly.
- `paper_type_classifier.py` — replace with prose in reference docs that the LLM applies as judgment.
- The whole "Gates A–G" framework — replaced by a single evidence_quote requirement + per-row independent verification.

The result is a smaller skill (\~1,500 LOC vs 6,370), with one big architectural change: **the LLM does the semantic work, and scripts only do the deterministic checks the LLM can't do reliably**.

### Trade-offs of the LLM-first approach

| Pro | Con |
| --- | --- |
| Much better recall on compound names, units, NMR vs mp distinctions | Higher per-paper token cost (one full read per extraction) |
| Robust to PDF format variation (NXML, columnar PDF, scanned PDF with OCR) | Requires good source-fetching infra (OA URL discovery, paywall handling) |
| Smaller codebase, less brittle maintenance | Less reproducible across LLM versions — same paper might extract differently in 6 months |
| Schema with evidence_quote is auditable end-to-end | Requires actual web access at extraction time |
| Refusal-to-fabricate prevents the worst failure mode | Doesn't help when the LLM hallucinates anyway (mitigated by Phase 4 verification) |

The trade-offs land on the LLM-first side for our use case. We're not extracting from millions of papers — we're extracting from corpora of 20–30 at a time. Tokens are cheap relative to engineering time and to the cost of a 30 %–60 % failure rate on the current approach.

## My recommendation

**Stop iterating on the current property-extractor and rebuild it in the redox-skill mold.** Specifically:

1. Take the redox skill as a starting template. Many components (`find_open_access.py`, `crossref_lookup.py`, the [SKILL.md](http://SKILL.md) structure, the prompt templates, the COMMON_ERRORS pattern) are property-agnostic and can be reused directly.
2. Replace the chemistry-specific bits (REFERENCE_ELECTRODES, voltage_range_check, conversion_arithmetic with electrode-specific tables) with mp/bp equivalents (value_range_check with K/°C/°F arithmetic; PAPER_TYPE_GUIDE; DATA_ORIGIN_RULES for synthesis vs review).
3. Write the extraction prompt template that emphasizes evidence_quote as mandatory.
4. Re-run on the same 20 + 30 papers and audit with the same 100-row random sample protocol.

I'd expect the rebuild to land around **90 %+ on both dev and val** based on what the redox skill achieved on a comparable problem. The remaining \~10 % would be the same long tail that redox sees: legitimate disagreements (multi-couple labeling, ambiguous solvent context, paywall-only SI), not algorithmic failures.

The current property-extractor produced useful learnings — the failure-mode catalog (F1–F8), the data_origin classification scheme, the audit-pool stratification critique — but the underlying architecture is the wrong shape for this task. Better to recognize that and pivot than to keep grinding on regex pattern lists.

<!-- forgemark-comments
- id: 1
  anchor_text: "skeleton (proposed)"
  context_before: " the redox skill's pattern is clearly better. Concretely, I would rebuild the property-extractor as: mp-bp-extraction/ "
  context_after: |
     mp-bp-extraction/
    ├── SKILL.md                              # Protocol, schema, phases, anti-patterns
    ├── scripts/
    │  
  author: Steven
  timestamp: "2026-05-12T02:05:33.096Z"
  edited_at: "2026-05-12T02:09:58.810Z"
  resolved: false
  body: |
    1. find_open_access.py is not needed. The redox skill searched for papers and then extracted data from them. We’re now separating those into two separate skills and this is the one for extracting data from already provided papers.
    
    2. cross_ref_lookup.py - is this needed if the skill is only extracting data from already provided papers?
    
    3. value_range_check.py - mp and bp ranges are wider than this. Make sure you’re not excluding valid values.
    
    4. COMMON_ERRORS.md - Don’t assume that the errors of the current skill will be common in the new one. Leave this blank to start and only add to it once we find and verify errors.
    
    5. PAPER_TYPE_GUIDE.md - I’m concerned that trying to distinguish synthesis vs. review vs. QSPR is too complicated for little gain. It’s important to distinguish measured from calculated, but that’s it. Look at how this is done in the redox skill and copy that.
- id: 2
  anchor_text: "Schema (required fields)"
  context_before: |
    gin from paper context
    └── evals/
        ├── evals.json
        └── files/                            # seeded-error fixtures 
  context_after: |
     id
    verification_status
    compound_name              # full IUPAC or common name; never truncated
    property               
  author: Steven
  timestamp: "2026-05-12T02:10:09.351Z"
  edited_at: "2026-05-12T02:12:39.477Z"
  resolved: false
  body: |
    1. data_origin - see comment above regarding not needed to distinguish measured from cited.
    
    2. solvent - melting point and boiling point are properties of compounds. Have you seen examples where there’s a molecule and a solvent?
    
    3. Does the redox skill have conversion_arithmetic? If not, remove.
- id: 3
  anchor_text: "Source preparation. Fetch via OA URLs; verify it's the right paper; identify mp/bp-bearing tables and paragraphs."
  context_before: "actually in the paper (correct row) or can't (rejected before emission). The six phases Mirroring the redox skill: "
  context_after: " Evidence-locked extraction. LLM reads the paper and writes one row per compound × property event with mandatory evid"
  author: Steven
  timestamp: "2026-05-12T02:13:04.403Z"
  resolved: false
  body: "This skill will be provided the papers, not search for them."
- id: 4
  anchor_text: "re-fetches the sourc"
  context_before: "ersion arithmetic, duplicate detection, paper-type-vs-data_origin consistency. Independent verification. Fresh agent "
  context_after: "e and confirms each row's evidence_quote. Confidence tagging. Use the same verification_status enum. Failure handl"
  author: Steven
  timestamp: "2026-05-12T02:13:29.753Z"
  resolved: false
  body: "Yes, but from the provided files."
- id: 5
  anchor_text: "The paper-type classifier idea (synthesis / qspr / thermodynamic / review) — but enforced via an LLM prompt, not a regex classifier. The classifier exists in the redox skill as prose in COMMON_ERRORS, not as a script."
  context_before: "y include. What we keep from the current implementation A few pieces of my current pipeline are worth retaining: "
  context_after: " The value-range plausibility filter ([-220, 700] °C). The unit-conversion-arithmetic check (K → °C, °F → °C). "
  author: Steven
  timestamp: "2026-05-12T02:14:15.493Z"
  resolved: false
  body: "No. See above. We need to know measured vs. predicted, but the rest adds unnecessart complication."
- id: 6
  anchor_text: "The value-range plausibility filter ([-220, 700] °C)."
  context_before: "prompt, not a regex classifier. The classifier exists in the redox skill as prose in COMMON_ERRORS, not as a script. "
  context_after: " The unit-conversion-arithmetic check (K → °C, °F → °C). The duplicate-within-paper check. The DOI verification"
  author: Steven
  timestamp: "2026-05-12T02:14:41.297Z"
  resolved: false
  body: "Yes, but you need to broaden your ranges. What about helium or Tungsten?"
-->

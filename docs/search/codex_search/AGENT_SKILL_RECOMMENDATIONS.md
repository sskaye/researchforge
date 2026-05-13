# Literature Search Corpus Build: Melting and Boiling Point Data

This note summarizes the workflow used to build and verify the open-access test corpus in this
directory, the main opportunities for improving it, and a recommended path for turning the approach
into a repeatable Codex agent skill.

## Final Corpus State

- Verified corpus: 164 open-access article records.
- Expansion records manually reviewed: 116.
- Expansion records kept after manual verification: 102.
- Expansion records moved to review: 14.
- Expansion manual-verification pass rate: 87.9%.
- Current category mix:
  - `synthetic_organic`: 148
  - `measurement_or_data`: 9
  - `boiling_point`: 7
- File completeness: 164 PDFs, 164 NXML files, 164 extracted text files, and 164 metadata files.
- Redundant source tarballs retained: 0.

Key locations:

- `articles/`: verified papers, one directory per article.
- `manifest.csv` and `manifest.jsonl`: verified corpus index.
- `review_no_mp_bp_data/`: manually rejected records and review manifests.
- `scripts/`: corpus building, targeted append, and expansion scripts.

## What Worked

### 1. Search was deliberately redundant

The most effective strategy was not one broad query. It was a bank of overlapping queries aimed at
different ways melting and boiling point data appears in papers:

- Synthetic organic chemistry patterns: `m.p.`, `mp:`, `mp =`, `mp C`, `M.p.`, `1H NMR`, `13C NMR`,
  `IR`, `synthesis`, `yield`, `solid`.
- Journal-targeted queries for chemistry-heavy open-access sources, including `Molecules`,
  `Beilstein J Org Chem`, `Marine Drugs`, `RSC Adv`, and related PMC-indexed journals.
- Measurement/property-style queries for papers specifically about melting point, boiling point,
  thermophysical data, or property prediction.
- Boiling point specific queries, which were lower yield but useful for diversity.

This redundancy mattered because article text is inconsistent: the same concept appears as
`melting point`, `mp`, `m.p.`, `Mp:`, `m.p. (degrees C)`, and occasionally only in experimental
paragraphs.

### 2. The official PMC OA package route was more reliable than ad hoc PDF scraping

The workflow relied primarily on:

- Europe PMC search for candidate discovery.
- PMC OA package service for article package metadata and download URLs.
- PMC FTP packages for PDF, NXML, figures, and license metadata.

That gave each article a stable bundle with `article.pdf`, `article.nxml`, extracted text, and
metadata. It also made cleanup simple: after extraction, source tarballs could be deleted without
losing the usable corpus.

### 3. Evidence snippets were captured before accepting records

Each accepted record has fields such as:

- `melting_point_mentions`
- `boiling_point_mentions`
- `mp_numeric_contexts`
- `bp_numeric_contexts`
- `manual_verification_evidence`

The useful rule was not just "contains the phrase melting point." Records were accepted only when
there was a nearby numeric value that looked like a property value, usually with `C`, `degrees C`,
or a range like `171-173`.

Good evidence looked like:

- `mp: 171-173 degrees C; 1H NMR...`
- `mp = 180-182 degrees C`
- `mp 246 degrees C (decomp.)`
- `boiling point ... 78.3 degrees C`

### 4. Manual verification caught important false-positive classes

Manual review was essential. The main false-positive patterns were:

- Conference abstract books and poster volumes with many author initials like `M.P.`
- Biomedical and clinical papers where `MP`, `Tm`, `BP`, or `CAM` meant something unrelated.
- Articles with apparatus statements only, such as "melting points were measured using..." but no
  actual numeric melting point values.
- Polymer/materials papers with temperatures for synthesis, drying, degradation, or testing, but no
  melting or boiling point data.
- False matches from `MPa`, protein names, microscope/microscopy text, pumps, lamps, or abbreviations.

Moving these into `review_no_mp_bp_data/` rather than deleting them preserved an audit trail and
created useful negative examples for future classifier tuning.

### 5. Cleanup and consistency checks prevented corpus drift

After each build or verification pass, the workflow checked:

- Manifest rows match article directories.
- Every verified record has PDF, NXML, text, and metadata.
- No verified article directory is missing from the manifest.
- No extra verified article directory is outside the manifest.
- Review manifests contain moved records.
- Tarballs have been removed.
- Summary files agree with manifest counts.

This caught count mismatches after manual moves and kept the corpus usable for downstream tests.

## Opportunities For Further Improvement

### 1. Add a stronger evidence classifier

The current approach is good regex-driven screening plus manual review. The next version should add a
small scoring classifier that distinguishes property values from unrelated temperatures.

High-confidence positive signals:

- `mp`, `m.p.`, `melting point`, or `boiling point` within 80-160 characters of a numeric temperature.
- Nearby chemistry characterization markers: `1H NMR`, `13C NMR`, `IR`, `HRMS`, `yield`, `solid`,
  `crystals`, `decomp`, `lit.`.
- Experimental section headings such as `Synthesis`, `General procedure`, `Characterization`,
  `Compound`, or numbered compound labels.

High-confidence negative signals:

- `MPa`, `mPa`, `M.P.` initials, `PMCID`, `pump`, `lamp`, `microscopy`.
- `Tm` unless the surrounding text clearly says melting temperature of a chemical/material.
- Abstract-book titles, poster presentations, conference proceedings, `Abstracts from`, `UEG Week`,
  `World Congress`, or similar volume-level records.
- Sentences that only describe equipment or methods and contain no nearby property value.

The classifier does not need to be fancy at first. A weighted rule score with a few negative
overrides would probably remove most manual rejects.

### 2. Treat article type as a first-class filter

Many false positives were not normal research articles. The build script should inspect NXML metadata
and title/citation strings before download or before final acceptance.

Recommended exclusions by default:

- Abstract books.
- Conference poster collections.
- Meeting proceedings made of many short abstracts.
- Records without a PDF when `require_pdf=true`.
- Records with only metadata-like or reference-only text.

Keep an option such as `--allow-review-articles` because reviews can contain useful property tables,
but route review articles through stricter evidence checks.

### 3. Use section-aware extraction

PMC NXML preserves section labels. The next version should parse NXML structurally and record where
evidence came from:

- table
- caption
- abstract
- main text
- experimental section
- supplementary-material pointer

For this task, evidence in experimental sections and tables is more valuable than evidence in
references or general discussion. A section-aware extractor could down-rank references and captions
that merely cite another source.

### 4. Add table extraction

Some valuable property data appears only in tables. The current text extraction can surface table
text from NXML, but a better skill should emit structured table candidates:

- table label and caption
- row text
- column headers
- property column name
- numeric value and unit
- compound identifier

This would make the corpus more useful for evaluating table extraction agents, not just text-span
extractors.

### 5. Preserve negative examples deliberately

The review folder is useful. Future runs should write a negative manifest with:

- rejection reason
- false-positive trigger
- matched snippet
- article type
- whether the record had PDF/XML/text

These rejected records can become a test set for precision, especially for avoiding `M.P.` initials,
abstract-book records, method-only mentions, and unrelated `Tm`/`BP` uses.

### 6. Add resumability and source accounting

The scripts already dedupe against the manifest, but the repeatable skill should make resumability
explicit:

- maintain `seen_pmcids.json`
- maintain `download_failures.csv`
- maintain `screening_rejections.csv`
- record query, rank, and source service for each candidate
- record why each candidate was accepted or rejected

This would make long runs less fragile and make it easier to top up a corpus after manual rejects.

### 7. Improve boiling point coverage

Boiling point papers were much lower yield than melting point synthetic chemistry papers. To improve
coverage, add targeted query families for:

- vapor-liquid equilibrium
- distillation
- azeotrope
- ebulliometry
- Antoine constants
- normal boiling point
- thermophysical properties
- ionic liquids
- solvents and fuel components

These may need different acceptance logic from organic synthesis papers, since boiling points often
appear in property tables rather than compound characterization paragraphs.

## Recommended Agent Skill Design

### Skill purpose

Create a skill for repeatable open-access literature corpus construction where the agent:

1. Searches literature sources for papers likely to contain numeric property data.
2. Downloads open-access article packages.
3. Extracts text and metadata.
4. Screens for numeric evidence.
5. Builds a verified corpus with manifests.
6. Moves rejects into review folders with reasons.
7. Produces a final audit summary.

The skill should support melting/boiling point first, but the design should allow other numeric
properties later.

### Proposed skill name

`literature-property-corpus`

### Proposed trigger description

Use this skill when the user asks Codex to search for, download, verify, or build an open-access
literature corpus containing numeric scientific property data from academic papers, especially
melting points, boiling points, experimental characterization data, thermophysical tables, or
chemistry property measurements.

### Recommended skill structure

```text
literature-property-corpus/
|-- SKILL.md
|-- scripts/
|   |-- build_corpus.py
|   |-- expand_corpus.py
|   |-- verify_corpus.py
|   |-- move_rejects.py
|   `-- summarize_corpus.py
`-- references/
    |-- query_patterns.md
    |-- evidence_rules.md
    `-- false_positive_patterns.md
```

Keep `SKILL.md` short. Put the fragile details in scripts and the tunable domain knowledge in
references.

### What should live in SKILL.md

The skill body should contain only the workflow and decision points:

1. Confirm target property, target count, output directory, and whether PDFs are required.
2. Search using query patterns from `references/query_patterns.md`.
3. Download through official OA routes first.
4. Extract PDF, NXML, plain text, and metadata.
5. Screen with `scripts/verify_corpus.py`.
6. Manually inspect borderline accepted records.
7. Move rejects with `scripts/move_rejects.py`.
8. Run `scripts/summarize_corpus.py`.
9. Report counts, pass rate, files created, and residual risks.

The `SKILL.md` should also state default acceptance criteria:

- A kept paper must contain a numeric melting or boiling point value, not just a methods statement.
- A kept paper should have a PDF unless the user opts out.
- Every kept paper must have a manifest row and article directory.
- Rejected papers should be moved, not silently deleted, unless the user explicitly asks for deletion.

### What should live in scripts

The scripts should do the deterministic work:

- `build_corpus.py`: start a new corpus from search queries.
- `expand_corpus.py`: add new records without duplicating existing PMCID/DOI values.
- `verify_corpus.py`: score evidence snippets and emit accepted, borderline, and rejected reports.
- `move_rejects.py`: move rejected article directories and update both main and review manifests.
- `summarize_corpus.py`: check file completeness and write summary JSON/README-style output.

Suggested common CLI flags:

```text
--property melting_point,boiling_point
--target 100
--output ./codex_search
--require-pdf
--remove-packages-after-extraction
--discard-reject-artifacts
--max-package-mb 250
--manual-review-borderline
--source pmc
```

### What should live in references

`query_patterns.md`:

- PMC/Europe PMC query templates.
- Synthetic chemistry query families.
- Boiling point and thermophysical query families.
- Journal-targeted query families.

`evidence_rules.md`:

- Positive regexes.
- Negative regexes.
- Scoring weights.
- Examples of accepted snippets.
- Examples of method-only mentions that should be rejected.

`false_positive_patterns.md`:

- Abstract-book and conference-volume patterns.
- Abbreviation traps.
- Biomedical uses of `MP`, `BP`, and `Tm`.
- Unit traps like `MPa`.
- Non-property temperature contexts.

### Recommended acceptance workflow

Use three buckets instead of binary accept/reject:

- `accepted`: strong numeric evidence, article package complete.
- `borderline`: some evidence but needs manual inspection.
- `rejected`: no numeric property data, wrong article type, missing required files, or false-positive
  abbreviation pattern.

For a high-quality corpus, the agent should manually inspect all `borderline` records and a sample of
`accepted` records. For small corpora, manually inspect every accepted record.

### Recommended output layout

```text
codex_search/
|-- articles/
|-- review_no_property_data/
|   |-- articles/
|   |-- manifest.csv
|   `-- manifest.jsonl
|-- reports/
|   |-- screening_report.csv
|   |-- manual_verification_report.csv
|   `-- summary.json
|-- packages/
|-- manifest.csv
|-- manifest.jsonl
`-- README.md
```

For disk-constrained runs, `packages/` should be empty after extraction and the manifest should record
the package URL plus `package=removed_after_extraction_to_save_space`.

### Recommended validation checks

Every run should end with a validation command equivalent to:

```text
- manifest row count equals verified article directory count
- every manifest row has exactly one article directory
- every kept article has PDF, NXML, extracted text, and metadata
- review manifest rows match moved review directories
- no source tarballs remain when cleanup is requested
- summary JSON counts match the manifests
```

### Recommended final response from the skill

The agent should always report:

- verified corpus size
- newly added count
- reviewed count
- kept count
- rejected/moved count
- pass rate
- file completeness
- output paths
- any unresolved caveats

## Suggested Next Implementation Step

Turn the current scripts into the skill's bundled scripts with a small refactor:

1. Merge shared PMC search/download/extract code into a reusable helper module.
2. Parameterize property targets, query sets, package size limits, and PDF requirements.
3. Add structured rejection reasons and a borderline bucket.
4. Add section-aware NXML extraction.
5. Write a lean `SKILL.md` that invokes the scripts instead of explaining all internals.

That would convert this one-off successful workflow into a repeatable corpus-building agent skill
without forcing future agents to rediscover the same query patterns and false-positive traps.

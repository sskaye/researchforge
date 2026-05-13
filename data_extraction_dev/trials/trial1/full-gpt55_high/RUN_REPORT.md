# Trial1-full-gpt55_high extraction report

## Scope

I used the `mp-bp-extraction` protocol on the supplied corpus at:

`/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp_bp_full_set`

I wrote all outputs only to:

`/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial1-full-gpt55_high`

I avoided reading or using other workspace-root trial/result folders, per the contamination warning.

## Outputs

- `mp_bp_extracted.csv`: final extracted rows.
- `skipped_sources.csv`: readable source files where no conservative row was emitted.
- `phase3_flags.csv`: empty flag report from the final Phase 3 run.
- `extract_mp_bp.py`: local extraction script used for this run.
- `README.md`: short summary counts.

## Extraction Result

The final CSV contains 304 rows from 65 source files.

Property counts:

- `melting_point`: 292
- `boiling_point`: 9
- `decomposition`: 3

Data type counts:

- `measured`: 295
- `calculated`: 9

Source identifier counts:

- DOI-backed rows: 166
- PMC-backed rows: 4
- Local `legacy:` source rows: 134

All rows are still marked `pending_verification`. I ran deterministic Phase 3 checks, but I did not run a fresh-context independent Phase 4 verifier.

## Method And Decisions

I followed an evidence-first extraction policy. Every emitted row had to include a source-local `evidence_quote`, and that quote had to be found again in the extracted source text after whitespace and hyphen normalization.

For PMC-style article folders, I preferred `article_text.txt` and metadata, using `article.nxml` only to recover article-level DOI information when needed. I did not separately process each PMC folder's PDF when an `article_text.txt` was already available, because the text file is the cleaner canonical text representation for these packages.

For category folders and root-level PDFs/HTML files, I extracted text from HTML directly and from PDFs using the bundled Python runtime's `pypdf` package. Several PDFs produced parser warnings, but rows were only kept when an exact quote could still be anchored in extracted text.

I added a `source_file` column beyond the required schema. This is deliberate: many non-PMC files have `legacy:` source URLs, and `source_file` makes local verification unambiguous.

I treated local PDF/HTML files without reliable DOI/PMC/PMID metadata as `legacy:<relative-path>`. I did not guess DOIs.

I normalized abbreviated ranges only when the source quote made the abbreviation clear. For example, a printed range such as `175-6oC` was stored as `175-176 °C`, while the evidence quote preserves the printed abbreviation and the note records the normalization.

I aggressively dropped candidate rows when the compound name looked procedural, generic, or mis-bound to surrounding prose. Examples of dropped patterns included address fragments containing `BP 17`, instrument mentions like `MP-500D`, generic text such as `After filtration...`, and predicted-vs-observed plot captions without a specific compound-value pair.

## Phase 3 Checks

The final CSV passed the bundled checks:

- required fields
- compound-name validation
- value range check
- unit conversion arithmetic
- DOI verification
- evidence quote verification
- within-paper duplicate detection

The final `phase3_flags.csv` has 0 rows.

## Data Not Extracted

`skipped_sources.csv` contains 225 readable sources where no row was emitted by the conservative extractor.

Skipped source categories:

- PMC article-text folders: 120
- `organic_synthesis`: 26
- `pharma_cocrystals`: 26
- `materials_inorganic`: 24
- `measurement_prediction`: 17
- root-level files: 12

All final skipped entries have the same recorded reason:

`no inline mp/bp/decomposition/sublimation values matched conservative extractor`

That reason means the file was readable, but I did not find a compound-specific value that passed the evidence rules. In practice, sources fell into several cases:

- The paper did not appear to report extractable mp/bp/decomposition values in the readable text.
- Candidate values appeared only in broad discussion, plots, model-performance text, or general-property examples rather than as a compound-specific measurement.
- Values appeared in tables or layouts where the compound-value binding was not reliable from flattened text.
- The source contained synthesis procedures, but the text around the value did not preserve a trustworthy full compound name.
- PDF extraction produced enough text to scan, but not enough structure to safely bind rows.
- Candidate strings were clearly false positives, such as institutional addresses with `BP`, instrument names with `MP`, reaction temperatures, assay temperatures, or chromatography/procedure fragments.

I chose not to emit uncertain rows as `flagged_review` in the final CSV. Instead, I left non-extracted sources in `skipped_sources.csv`, because including weak rows would make the main CSV harder to use and would mix defensible evidence with known-uncertain candidates.

## Known Limitations

This was a conservative automated extraction, not a full human/manual pass through every table and supplemental file. It likely misses valid data where the value is table-only, image-only, split across PDF columns, or described with unusual notation.

The final rows have deterministic quote and sanity-check coverage, but not independent semantic Phase 4 verification. A fresh verifier should still spot-check that each compound name is semantically the one associated with the quoted value.

The CSV favors precision over recall. The most important decision was to leave possible-but-uncertain data out rather than fabricate or weakly infer a compound-value pair.

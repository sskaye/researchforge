# MP/BP Open-Access Corpus Search Report

Date: 2026-05-15

Workspace root: `/Users/skaye/Claude/Skills/ResearchForge/test_data`

Main output directory: `codex_search/`

This report documents the workflow used to find, download, audit, and filter open-access sources likely to contain melting-point or boiling-point data. It also records recommendations for turning this workflow into a reusable, general-purpose literature/data-source discovery skill.

## Executive Summary

I built a broad open-access corpus for testing numeric-data extraction from papers and books, then audited and filtered it to reduce wasted extraction runs.

Final paper corpus:

- Downloaded open-access article XML/text records: 6,488
- Filtered accepted documents: 3,816
- Accepted article-body/XML documents: 3,640
- Accepted supplementary-information documents: 176
- Rejected or unresolved: 2,672
- Accepted SI files retained on disk: 176

Audit results:

- Initial random audit of unfiltered corpus: 204/300 valid, or 68.0%
- Calibration estimate after applying filter to that audit: 156 TP, 12 FP, 48 FN, 84 TN; precision 92.9%, recall 76.5%
- Actual post-filter random audit of 300 accepted records: 277 valid, 23 invalid; observed precision 92.3%
- Approximate Wilson 95% CI for post-filter precision: 88.8% to 94.8%

The filter clears the requested 90% validity target, but the margin is close. If extraction token cost is very high, a stricter second-pass cleanup would be reasonable.

## Directory Map

Important files and directories:

- `codex_search/articles/`
  Initial Europe PMC article batch, 1,497 downloaded article records.
- `codex_search/articles_additional_5k/`
  Additional Europe PMC article batch, 4,991 downloaded article records.
- `codex_search/books/`
  Downloaded open-access or public-domain books/lab manuals.
- `codex_search/dense_tables/`
  Data-rich sources and manifests for large tables/datasets.
- `codex_search/manifests/`
  Search query manifests, article manifests, corpus summary, and book manifest.
- `codex_search/audits/random_300/`
  Initial random sample and manual audit of 300 unfiltered papers.
- `codex_search/filtered_mp_bp_high_precision/`
  Final filtered accepted set, rejected/unresolved manifests, accepted SI files, and post-filter audit.
- `codex_search/scripts/collect_open_access_mp_bp_corpus.py`
  Europe PMC search and XML download script.
- `codex_search/scripts/build_audit_sample.py`
  Script to create reproducible random audit samples and context packs.
- `codex_search/scripts/audit_mp_bp_presence.py`
  Lightweight script-assisted presence triage for audit samples.
- `codex_search/scripts/filter_high_precision_mp_bp.py`
  Final high-precision paper/SI filter.
- `codex_search/filtered_mp_bp_high_precision/filter_report.md`
  Compact filter-only report.

## Source Discovery

### Article Sources

The article corpus came from Europe PMC open-access full-text search, using Europe PMC search and full-text XML APIs:

- Search endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/search`
- Full-text XML endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML`

The search script records each returned PMCID, source query names/categories, hit counts, Europe PMC URL, PMC URL, DOI, title, authors, journal, license text, and local XML/text paths.

Two batches were collected.

Initial batch:

- Target: 1,500 candidates
- Downloaded: 1,497
- Failed: 3, all HTTP 404
- Query manifest: `codex_search/manifests/search_queries.json`
- Article manifest: `codex_search/manifests/articles_manifest.jsonl`
- Summary: `codex_search/manifests/summary.json`

Additional broad batch:

- Target: 5,000 candidates
- Downloaded: 4,991
- Failed: 9, all HTTP 404
- Query manifest: `codex_search/manifests/additional_5k_search_queries.json`
- Article manifest: `codex_search/manifests/additional_5k_articles_manifest.jsonl`
- Summary: `codex_search/manifests/additional_5k_summary.json`

Combined article corpus:

- Downloaded records: 6,488
- Unique downloaded PMCIDs: 6,488
- Duplicate downloaded PMCIDs: 0
- Corpus summary: `codex_search/manifests/corpus_summary.json`

Before selecting additional records, existing PMCIDs found in `mp_bp_full_set`, `mp_bp_dev_set`, `mp_bp_val_set`, and earlier `codex_search` article folders were skipped.

### Article Query Sets

Initial query set:

- `"melting point" OPEN_ACCESS:y HAS_FT:y`
- `"boiling point" OPEN_ACCESS:y HAS_FT:y`
- `("melting point" OR "melting points") AND (synthesis OR synthesized OR derivatives OR compounds OR analogues) OPEN_ACCESS:y HAS_FT:y`
- `("boiling point" OR "boiling points") AND (synthesis OR synthesized OR derivatives OR compounds OR analogues) OPEN_ACCESS:y HAS_FT:y`
- `("differential scanning calorimetry" OR DSC OR "phase transition") AND ("melting point" OR "melting temperature") OPEN_ACCESS:y HAS_FT:y`
- `("normal boiling point" OR "boiling temperature" OR "vapor pressure") AND (organic OR compound OR compounds) OPEN_ACCESS:y HAS_FT:y`

Additional broad query set:

- `"melting point" OPEN_ACCESS:y HAS_FT:y`
- `"boiling point" OPEN_ACCESS:y HAS_FT:y`
- `("melting point" OR "melting points" OR "melting range") AND (synthesis OR synthesized OR derivatives OR compounds OR analogues OR characterization) OPEN_ACCESS:y HAS_FT:y`
- `("boiling point" OR "boiling points" OR "boiling range") AND (synthesis OR synthesized OR derivatives OR compounds OR analogues OR characterization) OPEN_ACCESS:y HAS_FT:y`
- `("melting temperature" OR "melting temperatures" OR "fusion temperature") OPEN_ACCESS:y HAS_FT:y`
- `("boiling temperature" OR "boiling temperatures" OR "normal boiling temperature") OPEN_ACCESS:y HAS_FT:y`
- `("differential scanning calorimetry" OR DSC OR "phase transition" OR thermogravimetric) AND ("melting point" OR "melting temperature" OR "melting range") OPEN_ACCESS:y HAS_FT:y`
- `("normal boiling point" OR "boiling temperature" OR "vapor pressure" OR "vaporisation" OR "vaporization") AND (organic OR compound OR compounds OR solvent OR solvents) OPEN_ACCESS:y HAS_FT:y`
- `("decomposition temperature" OR "decomposition point" OR "thermal decomposition") AND ("melting point" OR "DSC" OR compound OR compounds) OPEN_ACCESS:y HAS_FT:y`

The broad query set had 8,721 candidate PMCIDs after de-duplication and after skipping already known sources. The top 5,000 were selected, prioritizing organic-synthesis hits, multi-query overlap, publication year, and title.

### Book Sources

Downloaded books are listed in `codex_search/manifests/books_manifest.jsonl`.

Downloaded book/manual sources:

- Organic Chemistry Lab Techniques, Lisa Nichols
  - Source: LibreTexts PDF export / Open Textbook Library
  - Local file: `codex_search/books/libretexts_organic_chemistry_lab_techniques/book.pdf`
  - License note: Open Textbook Library lists the work as CC BY-NC-ND.
- A text-book of organic chemistry for students of medicine and biology, Elmer Verner McCollum
  - Source: National Library of Medicine Digital Collections
  - Local file: `codex_search/books/nlm_04720270R_textbook_organic_chemistry/book.pdf`
  - License note: NLM catalog states that NLM believes this item to be in the public domain.
- A laboratory manual of organic chemistry for medical students, Matthew Steel
  - Source: National Library of Medicine Digital Collections
  - Local file: `codex_search/books/nlm_04720530R_laboratory_manual_organic_chemistry/book.pdf`
  - License note: NLM catalog states that NLM believes this item to be in the public domain.
- A laboratory manual of medical chemistry, Ira Carleton Chase
  - Source: National Library of Medicine Digital Collections
  - Local file: `codex_search/books/nlm_61510470R_laboratory_manual_medical_chemistry/book.pdf`
  - License note: NLM catalog states that NLM believes this item to be in the public domain.

These were included as useful older/open lab technique sources, but the high-precision paper filter described below was applied to the article corpus, not to the books.

### Dense Tables and Databases

Data-rich sources are listed in `codex_search/dense_tables/manifests/dense_tables_manifest.jsonl`.

The manifest contains 17 entries, including:

- Jean-Claude Bradley Open Melting Point Dataset
  - 28,645 rows
  - Local file: `codex_search/dense_tables/datasets/figshare_1031637_bradley_open_melting_point_dataset.xlsx`
- ONS Open Melting Point Collection
  - 7,413 rows
  - Local file: `codex_search/dense_tables/pdfs/nature_precedings_2011_ONS_open_melting_point_collection.pdf`
- Boiling point dataset curated and enriched using Enalos tools
  - 5,432 rows
  - Local file: `codex_search/dense_tables/datasets/zenodo_14392754_BP.csv`
- Ionic liquid melting point and decomposition tables from Zenodo record 3251643
  - 2,212 melting point rows
  - 1,236 decomposition rows
  - 2,631 cation/anion SMILES rows
- ILGen-ion general melting point database
  - 5,848 rows
- ILGen-ion Venkatraman ionic-liquid melting point database
  - 2,206 rows
- CalebBell `chemicals` library data
  - Organic physical constants: 10,867 rows
  - Inorganic physical constants: 2,438 rows
  - NIST WebBook constants: 13,779 rows
  - Common Chemistry data: 79,291 rows
- NIST Critical Constants of Organic Compounds
  - 850 rows
- LibreTexts source pages for melting points and flash/boiling point data

The corpus summary reports approximately 154,585 known dataset rows across dense-table sources.

## Download Workflow

The Europe PMC downloader is `codex_search/scripts/collect_open_access_mp_bp_corpus.py`.

Important behavior:

- Uses Europe PMC cursor pagination.
- Requires `OPEN_ACCESS:y` and `HAS_FT:y` in query strings.
- Normalizes and deduplicates PMCIDs.
- Can skip PMCIDs already present in earlier corpora.
- Downloads full-text JATS XML from Europe PMC.
- Converts XML to flattened text for fast grep/audit workflows.
- Stores each record as:
  - `article.nxml`
  - `article_text.txt`
  - `metadata.json`
- Writes JSON query summaries and JSONL manifests.

Representative commands:

```bash
python3 codex_search/scripts/collect_open_access_mp_bp_corpus.py \
  --root codex_search \
  --target 1500 \
  --workers 8 \
  --articles-subdir articles \
  --query-set baseline
```

```bash
python3 codex_search/scripts/collect_open_access_mp_bp_corpus.py \
  --root codex_search \
  --target 5000 \
  --workers 8 \
  --articles-subdir articles_additional_5k \
  --manifest-prefix additional_5k \
  --query-set broad \
  --start-index 1
```

The script supports `--insecure-ssl` as a fallback if the local Python certificate store is broken.

## Initial Random Audit of Unfiltered Corpus

The first audit asked whether a paper has at least one extractable numeric melting-point, boiling-point, melting-temperature, boiling-temperature, `Tm`, or `Tb` datum tied to a compound, material, sample, or table row. This was intentionally a document-level presence audit, not a full extraction pass.

Audit files:

- `codex_search/audits/random_300/sample_index.csv`
- `codex_search/audits/random_300/sample_contexts.jsonl`
- `codex_search/audits/random_300/presence_audit_initial.csv`
- `codex_search/audits/random_300/presence_audit_tight.csv`
- `codex_search/audits/random_300/presence_audit_enhanced_triage.csv`
- `codex_search/audits/random_300/presence_audit_manual.csv`
- `codex_search/audits/random_300/audit_report.md`

Sample construction:

```bash
python3 codex_search/scripts/build_audit_sample.py \
  --root codex_search \
  --sample-size 300 \
  --seed 20260514 \
  --max-snippets 10 \
  --out-dir codex_search/audits/random_300
```

Script-assisted triage:

```bash
python3 codex_search/scripts/audit_mp_bp_presence.py \
  --root codex_search \
  --sample codex_search/audits/random_300/sample_contexts.jsonl \
  --out codex_search/audits/random_300/presence_audit_initial.csv
```

Manual audit result:

- Sample frame: 6,488 downloaded PMC article XML/text records
- Sample seed: 20260514
- Sample size: 300
- Valid: 204
- Invalid / not worth sending to extractor: 96
- Valid fraction: 68.0%

Invalid reason breakdown:

- Process/reaction temperature, not property data: 40
- No extractable numeric MP/BP value found: 36
- Bioassay or biopolymer melting context: 11
- Method-only or supporting-information-only values: 9

Conclusion: the unfiltered search set was too noisy for a token-intensive extractor.

## Why the Original Search Produced False Positives

The original Europe PMC queries intentionally favored recall. That brought in many documents where the target words appeared but did not represent extractable property data.

Common false positives:

- Method-only synthesis papers
  - Example pattern: "melting points were determined on..." with actual product values absent or in SI.
- Process temperatures
  - "boiling water", "heated to reflux", "below the boiling temperature", "boiling point separation", "reached boiling temperature".
- Reaction or processing temperatures
  - "heated at", "stirred at", drying, calcination, sintering, annealing, pyrolysis, combustion.
- Bioassay or biopolymer melting
  - PCR/HRM/DNA/RNA/protein `Tm`, melting curves, thermal-shift assays.
- Dataset/model papers
  - Papers about predicting melting points, where the accepted article discusses data/model performance but does not print useful rows.
- Abbreviation collisions
  - `Tb` as terbium or table labels; `mp` inside unrelated text; `BP` as "blood pressure" or other abbreviation.
- Generic review prose
  - "high boiling point solvent" or "lower melting point mixture" without a local numeric property value.

## SI Retrieval and Filtering

The user asked not to discard papers just because the data is in SI. The final filter therefore has an SI route.

SI logic is implemented in `codex_search/scripts/filter_high_precision_mp_bp.py`.

High-level SI workflow:

1. Parse article JATS XML.
2. Extract SI/media/ext-link references from:
   - `supplementary-material`
   - `inline-supplementary-material`
   - `media`
   - relevant `ext-link` elements
3. If article body has weak/no accepted evidence but looks like chemistry/materials work with SI, mark it as an SI candidate.
4. For each SI candidate:
   - scan existing SI cache first;
   - try direct SI/media URLs;
   - fall back to the NCBI OA package API;
   - extract SI-like files from OA tarballs;
   - scan PDF, DOCX, XLSX/XLSM, ZIP, CSV/TSV/TXT/XML/HTML/CIF/SDF/MOL files;
   - accept the SI file only if it contains direct mp/bp/melting/boiling/Tm/Tb value evidence.
5. Prune rejected SI directories automatically so disk usage stays bounded.

NCBI OA package note:

- OA API endpoint: `https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=<PMCID>`
- The OA API can return old FTP-style URLs under `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...`.
- The script converts these to HTTPS and maps the legacy path to:
  `https://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_package/...`

This fallback recovered SI files that direct publisher links could not fetch.

Implementation details added during the run:

- HTML/DOCTYPE responses are rejected before PDF parsing.
- PDF parsing is capped to 30 pages for presence filtering.
- `pypdf` logging is suppressed to avoid huge warning output from malformed PDFs.
- SI work is parallelized with `--si-workers`.
- Rejected SI files are pruned unless `--keep-unmatched-si` is explicitly passed.

Final filter command:

```bash
python3 codex_search/scripts/filter_high_precision_mp_bp.py \
  --root codex_search \
  --out-dir codex_search/filtered_mp_bp_high_precision \
  --download-si \
  --si-workers 24 \
  --sleep 0
```

## High-Precision Filter Design

The final filter is document-level presence filtering. It does not extract all rows. It accepts a document if there is strong evidence that at least one extractable target datum exists.

Accepted evidence patterns include:

- `melting point`, `melting range`, `melting temperature`
- `boiling point`, `boiling range`, `boiling temperature`
- `mp`, `m.p.`, `bp`, `b.p.`
- `Tm`, `Tb`
- numeric temperature values in the same local context
- table/caption/section evidence where headers and row values indicate target data
- chemistry/material context such as compound, product, derivative, material, polymer, solvent, salt, ionic liquid, alloy, wax, lipid, etc.

Rejected or downweighted contexts include:

- PCR, qPCR, RT-PCR, HRM, amplicon, primer, DNA/RNA/oligonucleotide/protein, thermal shift assay, melting curve
- boiling water, heated until boiling, reflux, reaction temperature, stirred at, drying, pyrolysis, combustion, calcination, sintering, annealing
- laser remelting, welding, cladding, melting infiltration, hot-water extraction, deparaffinization, antigen retrieval
- method-only statements such as "melting points were determined", "melting point apparatus", "uncorrected", "calibrated using indium" unless a local value is present
- broad model/dataset text without local rows

Important regex fix:

- Early versions allowed `m\s*\.?\s*p`, which could match ordinary `m ... p` word boundaries. This was tightened to require contiguous `mp` or dotted `m.p.`.

## Filter Results

Output directory:

- `codex_search/filtered_mp_bp_high_precision/`

Files:

- `filtered_manifest.jsonl`
- `rejected_or_unresolved_manifest.jsonl`
- `si_candidates_manifest.jsonl`
- `summary.json`
- `filter_report.md`
- `si/`
- `post_filter_audit_300/`

Final counts:

- Records scanned: 6,488
- Accepted article body/XML: 3,640
- SI candidates considered: 1,542
- Accepted supplementary: 176
- Accepted total: 3,816
- Rejected or unresolved: 2,672

Output size:

- Filtered output directory: about 1.0 GB
- Accepted SI directory: about 996 MB
- Accepted SI file count: 176

## Post-Filter Manual Audit

After creating the filtered set, I performed an actual post-filter manual audit.

Audit directory:

- `codex_search/filtered_mp_bp_high_precision/post_filter_audit_300/`

Audit files:

- `post_filter_audit_sample.csv`
- `post_filter_audit_manual.csv`
- `review_chunk_001_050.md` through `review_chunk_251_300.md`
- `risk_review.txt`

Sampling:

- Source: `codex_search/filtered_mp_bp_high_precision/filtered_manifest.jsonl`
- Random seed: 20260515
- Sample size: 300 accepted records

Manual-check rule:

- Valid if the accepted document itself contains at least one extractable numeric MP/BP/Tm/Tb value tied to a compound, material, mixture, polymer, sample, solvent, or property table.
- Invalid if the hit is only a process/method temperature, protein/DNA bio melting context, qualitative phrase, derived difference, abbreviation collision, or dataset/model discussion without local extractable rows.

Post-filter audit result:

- Valid: 277
- Invalid: 23
- Observed filtered-set precision: 92.3%
- Approximate Wilson 95% CI: 88.8% to 94.8%
- Article-body sample: 283 records, 260 valid, 23 invalid
- SI sample: 17 records, 17 valid, 0 invalid

Invalid categories:

- Bio/protein melting context: 6
- No extractable numeric property value in the accepted document: 4
- Process temperature only: 3
- Method/instrument context: 2
- Qualitative/no-value boiling or melting wording: 2
- Derived difference only: 1
- No target property data: 1
- Abbreviation false positive: 1
- Relative value only: 1
- Method-only/general background: 1
- Dataset discussion without local rows: 1

## Reproducibility Checklist

To reproduce the workflow from scratch:

1. Create the output root:

```bash
mkdir -p codex_search
```

2. Run the baseline Europe PMC collection:

```bash
python3 codex_search/scripts/collect_open_access_mp_bp_corpus.py \
  --root codex_search \
  --target 1500 \
  --workers 8 \
  --articles-subdir articles \
  --query-set baseline
```

3. Run the broad additional collection:

```bash
python3 codex_search/scripts/collect_open_access_mp_bp_corpus.py \
  --root codex_search \
  --target 5000 \
  --workers 8 \
  --articles-subdir articles_additional_5k \
  --manifest-prefix additional_5k \
  --query-set broad
```

4. Add or refresh book and dense-table sources.

The current workflow does not have a single consolidated downloader script for every dense-table/book source. Reproduce from:

- `codex_search/manifests/books_manifest.jsonl`
- `codex_search/dense_tables/manifests/dense_tables_manifest.jsonl`

For a reusable skill, this should be converted into source-specific download adapters.

5. Build an initial random audit sample:

```bash
python3 codex_search/scripts/build_audit_sample.py \
  --root codex_search \
  --sample-size 300 \
  --seed 20260514 \
  --max-snippets 10 \
  --out-dir codex_search/audits/random_300
```

6. Run script-assisted triage:

```bash
python3 codex_search/scripts/audit_mp_bp_presence.py \
  --root codex_search \
  --sample codex_search/audits/random_300/sample_contexts.jsonl \
  --out codex_search/audits/random_300/presence_audit_initial.csv
```

7. Manually review the sample and write `presence_audit_manual.csv`.

8. Run the high-precision filter with SI:

```bash
python3 codex_search/scripts/filter_high_precision_mp_bp.py \
  --root codex_search \
  --out-dir codex_search/filtered_mp_bp_high_precision \
  --download-si \
  --si-workers 24 \
  --sleep 0
```

9. Create a post-filter accepted-set audit:

Sample generation can be done with a small script:

```bash
python3 - <<'PY'
import csv, json, random
from pathlib import Path
root = Path("codex_search/filtered_mp_bp_high_precision")
out = root / "post_filter_audit_300"
out.mkdir(exist_ok=True)
rows = [json.loads(line) for line in (root / "filtered_manifest.jsonl").open(encoding="utf-8")]
sample = random.Random(20260515).sample(rows, 300)
with (out / "post_filter_audit_sample.csv").open("w", newline="", encoding="utf-8") as f:
    fields = ["audit_id", "pmcid", "doi", "document_kind", "document_path", "title",
              "evidence_score", "decision_reason", "evidence_snippet",
              "manual_verdict", "reason_category", "notes"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for i, r in enumerate(sample, 1):
        w.writerow({
            "audit_id": i,
            "pmcid": r.get("pmcid", ""),
            "doi": r.get("doi", ""),
            "document_kind": r.get("document_kind", ""),
            "document_path": r.get("document_path", ""),
            "title": r.get("title", ""),
            "evidence_score": r.get("evidence_score", ""),
            "decision_reason": r.get("decision_reason", ""),
            "evidence_snippet": r.get("evidence_snippet", ""),
            "manual_verdict": "",
            "reason_category": "",
            "notes": "",
        })
PY
```

Then manually label the sample into `post_filter_audit_manual.csv`.

## Recommendations for a General-Purpose Search Skill

This workflow should become a reusable "open corpus search and validation" skill, parameterized by target property/domain rather than hard-coded to MP/BP.

### Skill Inputs

The skill should accept a config file like:

```yaml
task_name: melting_boiling_point
output_root: codex_search
target_count: 5000
source_types:
  - europe_pmc_full_text
  - books
  - dense_tables
target_terms:
  - melting point
  - boiling point
  - melting temperature
  - boiling temperature
abbreviations:
  - mp
  - m.p.
  - bp
  - b.p.
  - Tm
  - Tb
value_patterns:
  - numeric_temperature
positive_context:
  - compound
  - material
  - polymer
  - product
  - table
negative_context:
  - process_temperature
  - method_only
  - bioassay_melting
audit:
  sample_size: 300
  seed: 20260515
precision_target: 0.90
```

For other searches, replace the term/value/context blocks. Examples:

- pKa extraction:
  - terms: `pKa`, `acid dissociation`, `dissociation constant`
  - values: dimensionless numeric, pH context
  - negative contexts: unrelated `PKA` acronyms, kinase/protein names
- solubility extraction:
  - terms: `solubility`, `soluble in`, `aqueous solubility`
  - values: mg/mL, mol/L, g/L, logS
  - negative contexts: qualitative-only soluble/insoluble without values
- toxicity/IC50 extraction:
  - terms: `IC50`, `EC50`, `LC50`, `GI50`
  - values: nM/uM/mg/L
  - context: assay/cell line/species
  - negative contexts: method-only assay descriptions without results
- reaction yield extraction:
  - terms: `yield`, `% yield`, `isolated yield`
  - values: percent, mg/mmol
  - context: product/reaction/table rows
  - negative contexts: crop yield, quantum yield, signal yield

### Recommended Skill Architecture

Use a modular pipeline:

1. Query planner
   - Expands target terms into exact phrase, synonym, abbreviation, and context-rich query families.
   - Separates broad recall queries from precision queries.
   - Records all hit counts and query provenance.

2. Source adapters
   - Europe PMC full text adapter.
   - PubMed Central OA package adapter.
   - Crossref/Unpaywall adapter for OA PDFs where allowed.
   - Zenodo/Figshare/Dataverse adapter for datasets.
   - GitHub release/raw-data adapter.
   - Open textbook/public-domain book adapter.

3. Downloader and normalizer
   - Stores raw artifacts unchanged.
   - Creates normalized text representations.
   - Extracts metadata, license, DOI, source URL, and local path.
   - Deduplicates by DOI, PMCID, title, and content hash.

4. Candidate context builder
   - Parses XML/HTML/PDF/DOCX/XLSX/CSV.
   - Preserves paragraph, section, caption, and table-row boundaries.
   - Emits compact context windows for audit and classifier development.

5. Presence filter
   - Config-driven positive and negative patterns.
   - Table-aware header/row matching.
   - Domain-specific false-positive rules.
   - SI/supplement downloader route.
   - Produces accepted, rejected, and unresolved manifests.

6. Audit harness
   - Creates reproducible random samples from both unfiltered and filtered sets.
   - Generates review chunks.
   - Stores manual labels with reason categories.
   - Computes precision, recall where possible, confidence intervals, and invalid reason breakdowns.

7. Iteration loop
   - If filtered precision is below target, propose stricter rules.
   - If recall is too low, propose additional source queries or SI/dataset routes.
   - Keep every iteration manifest and audit result versioned.

8. Reporting
   - Always write a final report with sources, counts, queries, commands, audit results, caveats, and next recommendations.

### General Skill Output Contract

Each run should produce:

- `raw_sources/` or source-specific directories
- `manifests/search_queries.json`
- `manifests/source_manifest.jsonl`
- `manifests/download_summary.json`
- `audits/pre_filter_sample.csv`
- `audits/pre_filter_manual.csv`
- `filtered/accepted_manifest.jsonl`
- `filtered/rejected_manifest.jsonl`
- `filtered/unresolved_manifest.jsonl`
- `filtered/supplementary/`
- `audits/post_filter_sample.csv`
- `audits/post_filter_manual.csv`
- `search_report.md`

Each accepted manifest row should include:

- stable document ID
- source IDs: DOI, PMCID, PMID, URL as available
- title, authors, journal/source, year
- license/reuse note if available
- original artifact path
- normalized text path
- accepted document path
- document kind: article, supplementary, book, dataset
- query provenance
- decision reason
- evidence snippet
- evidence score
- parser type
- timestamp

### Lessons Learned

- Query hit counts can look excellent while validity is mediocre. Always audit early.
- Search terms for scientific properties are highly ambiguous; process/method contexts dominate false positives.
- SI matters. Some chemistry articles have method statements in the article and actual product characterization only in supplementary files.
- Direct SI links often fail or return HTML challenge pages. OA package fallback is important.
- Rejected SI downloads can consume many GB; prune or quarantine aggressively.
- Table-aware parsing is essential. Many true positives are numeric-only table cells whose units live in a header.
- Abbreviations require strict boundaries. Loose `m p` or `b p` matching creates false positives.
- Post-filter auditing must sample accepted records, not only reuse an original corpus sample.

### Suggested Next Improvements

For this MP/BP corpus specifically:

- Add a stricter second-pass filter for the remaining false-positive classes:
  - protein/bio `Tm`
  - GC/chromatographic "boiling point separation"
  - process/cooking/boiling water
  - prediction/dataset discussion without local rows
  - relative-only statements such as "10 C lower"
- Add explicit book/dense-table filtering and audit, separate from article filtering.
- Add content hashes to all downloaded artifacts.
- Build a single source-acquisition script that also recreates the book and dense-table downloads, not only Europe PMC.
- Store filter version and git diff/hash in every manifest.
- Add a lightweight HTML/PDF validation step before writing SI files to disk.
- Consider a two-tier output:
  - high-precision extraction queue, estimated >95%
  - broad recall queue, lower precision but useful for expanding coverage later.


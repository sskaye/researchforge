# Extraction prompt templates

Copy-paste these prompts when delegating property-data extraction to a
Claude agent. The wording is calibrated to enforce the protocol's hard
rules (no memory-based extraction, mandatory evidence_quote,
drop-rather-than-guess, explicit data type).

The templates are **data-type-agnostic at the outer level**; the
property-specific bits (the `property` enum, candidate-token list,
aggressive-drop list, unit-conversion examples, worked example row) live
in each overlay's single `OVERLAY.md` file (v2.1 consolidated `OVERLAY.md`,
`SCHEMA.md`, and `COMMON_ERRORS.md` into one). Where this file says "see
overlay", insert the corresponding section from `datatypes/<datatype>/OVERLAY.md`
when copying the prompt.

## Template 1 — Single-paper extraction

> You have access to the Read and bash tools. **Do not extract values from training memory under any circumstances.** If you cannot read the paper file, return INACCESSIBLE for that paper and move on.
>
> **Data type:** `{datatype}` (e.g., `mp_bp`, `redox`). Before you start, read `datatypes/{datatype}/OVERLAY.md` end-to-end — this single file contains the property enum, schema (extension columns + standardized unit), worked examples, value ranges, unit conversions, candidate tokens, per-row drop patterns, per-paper skip-reason additions, and the property-specific failure-mode catalog. Also read `references/COMMON_ERRORS.md` for property-agnostic failure modes. If the overlay folder doesn't exist, stop and ask the user — do not infer the data type from the corpus.
>
> **Task:** Extract every measurement of the chosen property family from the paper located at `{paper_dir}`. The paper subdirectory contains some combination of `article.nxml`, `article.pdf`, `article_text.txt`, and `metadata.json`.
>
> **Mandatory steps:**
>
> **Step 1 — Read and identify the paper.**
> 1a. Read whichever of (`article.nxml`, `article_text.txt`) is present. If only `article.pdf` exists, use bash `pdftotext -layout article.pdf -` to get readable text.
> 1b. Find the paper's canonical identifier. **Extract it from the paper file ONLY** — not from the paper's bibliography (those DOIs belong to *cited* papers), not from your training memory. The identifier must appear as a substring of the paper file's text. Look in this order:
>     - **DOI**: NXML `<article-id pub-id-type="doi">`, PDF front matter ("https://doi.org/..." or "DOI: 10.xxxx/..."), or `metadata.json`. Set `source_url = https://doi.org/<DOI>`.
>     - **PMC ID** (if no DOI): NXML `<article-id pub-id-type="pmc">`, or "PMC########" in text/metadata. Set `source_url = pmc:PMC########`.
>     - **PMID** (if no DOI/PMC): NXML `<article-id pub-id-type="pmid">`, or "PMID: ########". Set `source_url = pmid:########`.
>     - **Citation only** (older papers): if none of the above are present, ensure `source` carries journal + year + vol + page. Set `source_url` to any stable URL the paper provides or `legacy:<paper-folder-name>` as a last resort.
>
>     **Never guess a DOI** — if none of these locations has one, use the next available identifier.
>
>     **`source_url` is the DOI of the paper file you are physically reading, NOT the DOI of any paper it cites.** When the value you're extracting is tabulated inside the paper-at-hand (a QSPR / compilation / review / textbook table that lists literature values), `source_url` is still the DOI of the paper-at-hand. The upstream primary measurement's DOI is irrelevant to `source_url`. If you want to credit it, mention it in `notes`. Compiled-literature values still belong to the compilation paper for citation purposes.
> 1c. **Only if you found a DOI**, run `python3 scripts/crossref_lookup.py <DOI>` to confirm the DOI resolves and the returned title matches the paper file. If they don't match, emit a single `flagged_review` row for the paper with reason `flagged_doi_unrelated_paper` and stop processing this paper.
>
> A paper with no DOI is NOT an error. Pre-DOI-era papers sometimes never had one.
>
> **Step 2 — Note the paper's reporting conventions.**
> For every value you'll later extract, you'll need to decide:
> - Is the value `measured` (real experimental measurement, including compiled-from-literature) or `calculated` (model output)? The clue is usually in the immediate column header or paragraph context.
> - What units are used? Compare against the standardized unit declared in `datatypes/{datatype}/OVERLAY.md` § Schema.
>
> **Step 3 — Find candidate locations.**
> Scan for the candidate tokens listed in `datatypes/{datatype}/OVERLAY.md` (e.g., for mp_bp: `mp`, `m.p.`, `melting point`, `Tm`, `Tfus`, `bp`, `b.p.`, `boiling point`, `Tb`, `DSC onset`, `DSC peak`, `decomposition`, `sublimation`). Note page / table / figure numbers per region.
>
> **Step 4 — Extract row by row.**
> For each (compound × property × value) instance, produce a CSV row with the 18-column generic schema declared in `SKILL.md`:
>
> Required:
> - `id`: sequential integer
> - `verification_status`: `pending_verification`
> - `compound_name`: full IUPAC, common, or trivial name as printed. **Never truncated.** For multi-line PDF names that wrap, reassemble them. For ionic-liquid `[cation][anion]` shorthand, the shorthand is acceptable.
> - `property`: one of the enum values in `datatypes/{datatype}/OVERLAY.md` § Properties — pick the most specific applicable. See the property-disambiguation table in the overlay for borderline cases.
> - `value`: numeric value in the property's standardized unit (the overlay declares it under § Schema).
> - `value_raw`: as printed in the source, including original units.
> - `units`: the standardized unit string from the overlay (e.g., `°C` for mp_bp).
> - `relation`: `=` (default), `>`, `<`, `~`, `≈`.
> - `meas_calc`: `measured` or `calculated`.
> - `source`: journal / year / vol / page (NO author names).
> - `source_url`: DOI URL (preferred), `pmc:`, `pmid:`, `textbook:`, or `legacy:` per Step 1.
> - `evidence_location`: precise pointer (e.g., "Table 1 row 3", "p. 6469 col 2 ¶ 3", "SI Table S4 row 12").
> - `evidence_quote`: **verbatim text from the paper** containing the value. Allow only minor whitespace differences. **MANDATORY — if you can't produce a verbatim quote, DROP the row.**
>
> Conditional / optional:
> - `value_min`, `value_max`: when `value_raw` is a range.
> - `compound_smiles`: if the source provides a SMILES.
> - `conversion_arithmetic`: when you converted from a non-standard unit, use the v2.0 standardized syntax `<input value+units> <op> <constant> = <output value+units>`. See SKILL.md for the syntax + `datatypes/{datatype}/OVERLAY.md` for the property-specific conversion examples. Blank when `value_raw` is already in the standardized unit.
> - Any extension columns declared in the overlay's § Schema (e.g., `reference_electrode` for redox).
> - `notes`: chemical family, audit history, flag-reason details.
>
> **Step 5 — Drop these aggressively (per-row, NOT paper-level)** — see `datatypes/{datatype}/OVERLAY.md` § "drop patterns" for the data-type-specific patterns. These are per-row decisions: a paper containing one of these does not become a whole-paper skip. (Whole-paper skips use the Phase 0 vocabulary in `SKILL.md` + any property-specific additions in the overlay.) Always-drop generic patterns:
> - Bare code names without a real compound name ("compound 3", "complex 9a", "compound 4b").
> - Truncated names — anything ending mid-token, e.g., `-yl` fragment without the parent, `5-acetyl-` (a substituent without the scaffold).
> - Names that are actually section-heading or procedure-title text ("Synthesis of compounds 4–7").
> - Names that are clearly journal titles, vendor labels, dataset descriptors, or non-chemistry prose.
>
> When in doubt, emit the row with `verification_status = flagged_review` and a granular reason in `notes`. Do **not** silently drop.
>
> **Step 6 — Quote re-confirmation. THIS IS MANDATORY AND NON-NEGOTIABLE.**
>
> Before adding a row to the output, re-open the paper file and run this 5-step check:
>
> 1. **Try to capture a verbatim contiguous span** that contains both the compound (or its serial code) and the value. Verifiable by `grep -F` in 5 seconds. Permitted normalizations: whitespace collapsing, NFC unicode, ASCII hyphen folding (`−` / `–` / `—` → `-`). Avoid extra/missing words and avoid doubled-token PDF artifacts ("White White powder, powder").
>
> 2. **If you can't capture a single contiguous span containing both** (common cases: 2-column PDF wrap, table cells separated by spacing, watermark splitting a sentence), record the closest contiguous span that supports the row — typically the local clause containing the value. Phase 3 lints will flag quote-fidelity issues for maintainer review, but they do NOT auto-drop the row.
>
> 3. **Confirm the value matches `value_raw`.** If the quote points at a different measurement on a nearby line (e.g., quoted the freezing point while recording the boiling point), fix the quote to capture the correct line. This is a Tier-1 correctness check — wrong value attached to a compound is the failure mode the protocol exists to prevent.
>
> 4. **Confirm the compound name (or its label) is correct.** Multi-row PDF tables can put a value on the row of a different compound than the agent assumed. Re-read the row label.
>
> 5. **Confirm `conversion_arithmetic`** (if present) is mathematically correct AND uses v2.0 standardized syntax (`<input value+units> <op> <constant> = <output value+units>`).
>
> 6. **Suspect a PDF line wrap when `value_raw` ends at a non-token boundary.** If your recorded `value_raw` ends in a trailing decimal point with no following digit (e.g., `"158-159."` or `"158-159"` when the source might continue with `.5`), a dangling hyphen (e.g., `"36.98-"`), or a dangling unit character (e.g., `"−77.9 °"`), the actual value is almost certainly continued on the next physical line of the `pdftotext` output. Re-read the next line and reconstruct the full `value_raw`. Trial-7 row 902 was a `mp 158–159.5 °C` where the `.5 °C` wrapped to the next physical line; recording `value_raw = "158-159"` truncated the decimal.
>
> Drop any row that fails this check.
>
> **Step 7 — Run sanity checks.**
> ```bash
> python3 scripts/run_all_checks.py --datatype {datatype} <your-output.csv>
> ```
> The `--datatype` flag is required. If any rows flag, fix them. Do **not** deliver a CSV with mixed verified + flagged rows where the flags weren't already disclosed.
>
> **Step 7.5 — Multi-line compound name reassembly** (mandatory when source is a wrapped PDF).
>
> Long IUPAC names routinely wrap across PDF line breaks. When you encounter a compound name that LOOKS like it might be incomplete, do these checks:
>
> 1. **Read the line above the section header.** Many PDFs put the leading substituent block on the previous line, then "Synthesis of …" / a section number / a code on the new line, then the rest of the name. Always read at least one line above the section header before deciding where the name starts.
> 2. **Reject names starting with a single capital letter + dash.** Patterns like `H-Indeno...`, `H-Pyrrolo...`, `O-Benzyl...`, `N-Methyl...` are almost always truncated — the original was `7H-Indeno...`, `1H-Pyrrolo...`, etc. with a leading numeric locant.
> 3. **Reject names that are clearly a parent scaffold when the compound code is part of a substituted series.** If compounds 11a–11p appear as a numbered series (each with a different aryl substituent), 11h's name MUST include that substituent.
> 4. **Resolve `pdftotext` artifacts.** `pdftotext -layout` on 2-column PDFs sometimes produces doubled tokens ("White White powder, powder"). If you see this, switch to `pdftotext` (no `-layout`) and cross-reference, or use the NXML if available.
>
> When you're not sure, **drop the row rather than commit a truncated name**.
>
> **Step 8 — Output: CSV quoting discipline (mandatory per RFC 4180).**
>
> When writing the CSV, **any field that contains a comma, double quote, or newline MUST be wrapped in double quotes**. Compound names like `N-(2,5-Dimethylhexylamino)methylenebisphosphonic acid` MUST be written `"N-(2,5-Dimethylhexylamino)methylenebisphosphonic acid"`. If a quoted field contains an embedded double quote, the embedded quote must be doubled (`She said "hi"` → `"She said ""hi"""`).
>
> Easiest practice: **wrap every field in double quotes for every row**, regardless of content. Use Python's `csv.writer` with `quoting=csv.QUOTE_ALL`.
>
> Write the CSV to the path you've been told to write to. Report a short summary: `<N rows emitted, M flagged_review>`.
>
> **What NOT to do:**
> - Do not extract from training memory.
> - Do not include author names in the source field.
> - Do not use placeholder citations.
> - Do not truncate compound names.
> - Do not guess at the DOI.
> - Do not extract context numbers (NMR shifts, mass-spec values, citation numbers) as property values — see `datatypes/{datatype}/OVERLAY.md` § "drop patterns" for property-specific patterns and `references/COMMON_ERRORS.md` for generic ones.
> - Do not invent values that aren't supported by an `evidence_quote`.

## Template 2 — Bulk-corpus extraction (multiple papers)

For a directory containing many papers (in any layout — indexed
subdirectories, standalone PDFs, category subfolders with PDFs inside,
mixed):

> **Data type:** `{datatype}` (specified by the user; do not infer).
>
> **Step 0 — Build the corpus manifest before extraction.**
>
> Enumerate every paper-bearing location in `{input_dir}`. A paper-bearing location is anything that contains an article body. **Descend into subfolders** — past trials have silently missed papers in category subfolders by enumerating only the top level.
>
> Use whatever enumeration mechanism is appropriate for the corpus layout (`ls`, `find`, `glob`).
>
> Write `_corpus_manifest.txt` with one paper-bearing location per line. Verify the count is plausible.
>
> **Step 0a — Skip-list with reasons.**
>
> Anything you intentionally exclude from extraction goes in `_skipped.txt`, one line per location:
> `<location>\t<reason>`
>
> Use the most specific reason from the generic skip-vocabulary in `SKILL.md` Phase 0 (six categories: `review_no_per_compound_binding`, `bare_code_compounds_only`, `binding_ambiguous`, `image_only_compound_table`, `formulation_only_no_discrete_compound`, `paper_unreadable`) or the property-specific additions in `datatypes/{datatype}/OVERLAY.md` § "Skip reasons specific to ..." (e.g., for mp_bp: `no_mp_bp_data_in_text`, `tga_or_nmr_only_no_mp_bp`). Free-text reasons are permitted but ask the user before using one. **Do not skip a location because a prior trial skipped it** — past trials are reference, not protocol. **Whole-paper skip vs per-row drop:** these reasons are for excluding a *whole paper* from extraction. A paper that has some good rows and some bad ones does NOT belong here — emit the good rows and drop the bad ones individually per Step 5.
>
> **Step 1+ — Per-paper extraction (Template 1).**
>
> For each location in the manifest that is NOT in `_skipped.txt`, apply Template 1 with the same `{datatype}`. Process each paper independently and append rows to a single CSV. Use a sequential `id` counter across the whole corpus.
>
> **Step N — Sanity checks.**
>
> After all papers are processed, run:
>
> ```bash
> python3 scripts/run_all_checks.py --datatype {datatype} <output.csv>
> ```
>
> **Step N+1 — Account for every manifest entry.**
>
> Your EXTRACTION_SUMMARY.md must include the accounting equation `processed + skipped == manifest`. Report the per-paper summary (rows emitted, rows flagged, INACCESSIBLE entries) AND the per-skip-reason histogram from `_skipped.txt`. Numbers that don't balance indicate silent loss; investigate before declaring the run complete.

## Template 3 — Single-paper extraction with smaller scope

For when you only want a subset (e.g., only one specific property value
within the overlay's enum, or only experimental measurements):

> Apply Template 1 with the same `{datatype}`, but only emit rows that match `{filter clause}` (e.g., `property = melting_point` only, or `meas_calc = measured` only). All other rules stay the same — evidence_quote mandatory, no memory extraction, etc.

## Why these rules matter

Past versions of property-data extraction produced 30–60 % error rates
when independently spot-checked. The dominant error categories were:

- **Memory-based fabrication.** Without a verbatim evidence quote
  requirement, agents fill in plausible-sounding values for well-known
  compounds.
- **Wrong-paper citations.** Agents guess at "the most likely primary
  source" and end up with DOIs pointing at unrelated papers.
- **PDF text artifacts misread as data.** NMR chemical shifts, mass-spec
  m/z values, PDF sign-loss artifacts all look numerically like property
  values and end up in the database.
- **Truncated / fragmented compound names.** Long IUPAC names split across
  PDF line breaks get captured as substituent fragments.
- **Wrong-column / wrong-row binding in dense tables.** Multi-row table
  headers trip up programmatic extractors. An LLM reading the actual table
  layout doesn't make this mistake.

Every rule in these templates exists because at least one of those failure
modes was observed in real prior runs. The data-type overlay catalogs
additional property-specific failure modes (e.g., for mp_bp: NMR shifts
falling in mp range, TLC eluents extracted as compounds, PDF sign-loss).

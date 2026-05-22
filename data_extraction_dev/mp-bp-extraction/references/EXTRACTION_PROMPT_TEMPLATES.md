# Extraction prompt templates

Copy-paste these prompts when delegating mp/bp extraction to a Claude agent. The wording is calibrated to enforce the protocol's hard rules (no memory-based extraction, mandatory evidence_quote, drop-rather-than-guess).

## Template 1 — Single-paper extraction

> You have access to the Read and bash tools. **Do not extract values from training memory under any circumstances.** If you cannot read the paper file, return INACCESSIBLE for that paper and move on.
>
> **Task:** Extract every melting-point and boiling-point measurement from the paper located at `{paper_dir}`. The paper subdirectory contains some combination of `article.nxml`, `article.pdf`, `article_text.txt`, and `metadata.json`.
>
> **Mandatory steps:**
>
> **Step 1 — Read and identify the paper.**
> 1a. Read whichever of (`article.nxml`, `article_text.txt`) is present. If only `article.pdf` exists, use bash `pdftotext -layout article.pdf -` to get readable text.
> 1b. Find the paper's canonical identifier. **Extract it from the paper file ONLY** — not from the paper's bibliography (those DOIs belong to *cited* papers), not from your training memory (you may know a similar-sounding DOI for a different paper). The identifier must appear as a substring of the paper file's text. Look in this order:
>     - **DOI**: NXML `<article-id pub-id-type="doi">`, PDF front matter ("https://doi.org/..." or "DOI: 10.xxxx/..."), or `metadata.json`. Set `source_url = https://doi.org/<DOI>`.
>     - **PMC ID** (if no DOI): NXML `<article-id pub-id-type="pmc">`, or "PMC########" in text/metadata. Set `source_url = pmc:PMC########`.
>     - **PMID** (if no DOI/PMC): NXML `<article-id pub-id-type="pmid">`, or "PMID: ########". Set `source_url = pmid:########`.
>     - **Citation only** (older papers): If none of the above are present, that's fine — older papers predate DOIs. Make sure `source` carries journal + year + vol + page. Set `source_url` to any stable URL the paper provides, or `legacy:<paper-folder-name>` as a last resort.
>
>     **Never guess a DOI** — if none of these locations has one, use the next available identifier. A wrong DOI is worse than no DOI.
> 1c. **Only if you found a DOI**, run `python3 scripts/crossref_lookup.py <DOI>` to confirm the DOI resolves and the returned title matches the paper file. If they don't match, the DOI is wrong — emit a single `flagged_review` row for the paper with reason `flagged_doi_unrelated_paper` and stop processing this paper.
>
> **A paper with no DOI is NOT an error**. Pre-DOI-era papers (typically pre-2000) sometimes never had one. As long as you have a complete citation in `source` and a stable identifier in `source_url`, proceed to extraction normally.
>
> **Step 2 — Note the paper's reporting conventions.**
> Read the abstract / experimental section. For every value you'll later extract, you'll need to decide:
> - Is the value `measured` (real experimental measurement, including compiled-from-literature) or `calculated` (model output — QSPR / MPBPVP / DFT / SPARC / etc.)? The clue is usually in the immediate column header or paragraph context.
> - What are the units (°C, K, °F)?
>
> **Step 3 — Find candidate locations.**
> Scan for tables, figures, and paragraphs mentioning: `mp`, `m.p.`, `M.p.`, `melting point`, `Tm`, `Tfus`, `bp`, `b.p.`, `boiling point`, `Tb`, `DSC onset`, `DSC peak`, `decomposition`, `sublimation`. Note page / table / figure numbers per region.
>
> **Step 4 — Extract row by row.**
> For each (compound × property × value) instance, produce a CSV row with these fields (see SKILL.md for the full schema):
>
> Required:
> - `id`: sequential integer
> - `verification_status`: `pending_verification`
> - `compound_name`: full IUPAC, common, or trivial name as printed. **Never truncated.** For multi-line PDF names that wrap, reassemble them into a single string. For ionic-liquid `[cation][anion]` shorthand, the shorthand is acceptable as-is.
> - `property`: one of `melting_point`, `boiling_point`, `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`
> - `value_celsius`: numeric, in °C (midpoint of range if a range)
> - `value_raw`: as printed in the source, including original units
> - `relation`: `=` (default), `>`, `<`, `~`, `≈`
> - `data_type`: `measured` or `calculated`
> - `source`: journal / year / vol / page (NO author names)
> - `source_url`: DOI URL (preferred) or `textbook:<short-id>`
> - `evidence_location`: precise pointer (e.g., "Table 1 row 3", "p. 6469 col 2 ¶ 3", "SI Table S4 row 12")
> - `evidence_quote`: **verbatim text from the paper** containing the value. Allow only minor whitespace differences. **This is mandatory — if you can't produce a verbatim quote, DROP the row.**
>
> Conditional / optional:
> - `value_celsius_min`, `value_celsius_max`: when value_raw is a range
> - `compound_smiles`: if the source provides a SMILES
> - `conversion_arithmetic`: when you converted K → °C or °F → °C, show the math (e.g., "492.478 K − 273.15 = 219.328 °C"). Blank when value_raw is already °C.
> - `notes`: chemical family, audit history, flag-reason details
>
> **Step 5 — Drop these aggressively** (they are known failure modes; flag rather than emit):
> - Bare code names without a real compound name ("compound 3", "complex 9a", "compound 4b").
> - Truncated names — anything ending mid-token, e.g., "Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl" (a `-yl` fragment without the parent), "5-acetyl-" (a substituent without the scaffold).
> - Names that are actually section-heading or procedure-title text ("Synthesis of compounds 4–7", "3.1.10. Synthesis of compound").
> - Names that are clearly journal titles, vendor labels, dataset descriptors, or non-chemistry prose ("Chemosphere", "MOE 2D", "PATENTS", "study of", "This is the normal boiling point").
> - Workup-solvent abbreviations as the compound (CH2Cl2, EtOAc, MeOH, DMSO, DMF, THF) — particularly when they appear inside `Rf:` annotations or column eluent lists.
> - Values that come from NMR / mass-spec context (`δ X.X ppm`, `m/z`, `[M+H]+`, `13C NMR`, `1H NMR`) and just happen to fall in a plausible mp/bp range.
> - PDF sign-loss artifacts ("277.9 °C" when the original was "−77.9 °C"; you'll spot these because they're far outside the expected range for that class of compound). If suspected, flag with reason `flagged_value_out_of_range`.
>
> When in doubt, emit the row with `verification_status = flagged_review` and a granular reason in `notes`. Do **not** silently drop.
>
> **Step 6 — Quote re-confirmation. THIS IS MANDATORY AND NON-NEGOTIABLE.**
>
> Before adding a row to the output, re-open the paper file and run this 4-step check:
>
> 1. **Try to capture a verbatim contiguous span that contains both the compound (or its serial code) and the value.** This is the ideal quote — verifiable by `grep -F` in 5 seconds. Permitted normalizations: whitespace collapsing, NFC unicode, ASCII hyphen folding (− / – / — → -). Avoid extra/missing words and avoid doubled-token PDF artifacts ("White White powder, powder").
>
> 2. **If you can't capture a single contiguous span containing both** (common cases: 2-column PDF wrap where the value lands on a separate physical output line; table cells separated by spacing; watermark splitting a sentence), record the closest contiguous span that supports the row — typically the local clause containing the value. Phase 3 lints will flag quote-fidelity issues for maintainer review, but they do NOT auto-drop the row. The bar for emitting a row is: compound is identifiable, value matches the paper, source citation is real.
>
> 3. **Confirm the value matches `value_raw`.** If the quote says "f.p. -161.51 °C" but your `value_raw` says "36.98 °C" (because you read a boiling-point value from an adjacent line but quoted the freezing-point line), fix the quote to capture the bp line specifically. This is a Tier-1 correctness check — wrong value attached to a compound is the failure mode the protocol is designed to prevent.
>
> 4. **Confirm the compound name (or its label) is correct.** Multi-row PDF tables can put a value on the row of a different compound than the agent assumed. Re-read the row label. If the row claims `compound_name="compound 4f"` but the m.p. you've captured is for compound 4g, that's a Tier-1 failure — fix the compound name or fix the value, do not commit a wrong binding.
>
> 5. **Confirm `conversion_arithmetic`** (if present) is mathematically correct.
>
> Drop any row that fails this check. Past trials caught a recurring failure where steps 1-2 weren't done carefully enough — the agent quoted an adjacent measurement or a doubled-token PDF artifact, and the row passed every other check but still pointed at non-verbatim text. Step 6 IS the last defense against this.
>
> **Step 7 — Run sanity checks.**
> ```bash
> python3 scripts/run_all_checks.py <your-output.csv>
> ```
> If any rows flag, fix them. Do **not** deliver a CSV with mixed verified + flagged rows where the flags weren't already disclosed.
>
> **Step 7.5 — Multi-line compound name reassembly (mandatory when source is a wrapped PDF).**
>
> Long IUPAC names routinely wrap across PDF line breaks. When you encounter a compound name that LOOKS like it might be incomplete, do these checks:
>
> 1. **Read the line above the section header.** Many PDFs put the leading substituent block on the previous line, then "Synthesis of …" / a section number / a code on the new line, then the rest of the name. Always read at least one line above the section header before deciding where the name starts.
> 2. **Reject names starting with a single capital letter + dash.** Patterns like `H-Indeno...`, `H-Pyrrolo...`, `O-Benzyl...`, `N-Methyl...` are almost always truncated — the original was `7H-Indeno...`, `1H-Pyrrolo...`, etc. with a leading numeric locant that got dropped. If you see this pattern, look backward in the paper text for the missing prefix.
> 3. **Reject names that are clearly a parent scaffold when the compound code is part of a substituted series.** If compounds 11a–11p appear in a numbered series (each with a different aryl substituent), then 11h's name MUST include that substituent. A bare "11h: 7H-Indeno[2,1-c]Quinolin-7-One" is missing what makes 11h different from 11a.
> 4. **Resolve `pdftotext` artifacts.** `pdftotext -layout` on 2-column PDFs sometimes produces doubled tokens ("White White powder, powder"). If you see this, switch to `pdftotext` (no -layout) and cross-reference, or use the NXML if available.
>
> When you're not sure, **drop the row rather than commit a truncated name**.
>
> **Step 8 — Output: CSV quoting discipline (mandatory per RFC 4180).**
>
> When writing the CSV, **any field that contains a comma, double quote, or newline MUST be wrapped in double quotes**. Compound names like `N-(2,5-Dimethylhexylamino)methylenebisphosphonic acid` MUST be written `"N-(2,5-Dimethylhexylamino)methylenebisphosphonic acid"`. If a quoted field contains an embedded double quote, the embedded quote must be doubled (e.g., `She said "hi"` → `"She said ""hi"""`).
>
> Easiest practice: **wrap every field in double quotes for every row**, regardless of content. Use Python's `csv.writer` with `quoting=csv.QUOTE_ALL`. Spot-check the output CSV by opening it and confirming compound names containing commas (like `2,5-`, `1,2,3-`, `(R,S)-`) appear properly quoted.
>
> Write the CSV to the path you've been told to write to. Report a short summary: `<N rows emitted, M flagged_review>`.
>
> **What NOT to do:**
> - Do not extract from training memory.
> - Do not include author names in the source field.
> - Do not use placeholder citations.
> - Do not truncate compound names.
> - Do not guess at the DOI.
> - Do not extract NMR / MS values as mp / bp.
> - Do not invent values that aren't supported by an `evidence_quote`.

## Template 2 — Bulk-corpus extraction (multiple papers)

For a directory containing many papers (in any layout — indexed subdirectories, standalone PDFs, category subfolders with PDFs inside, mixed):

> **Step 0 — Build the corpus manifest before extraction.**
>
> Enumerate every paper-bearing location in `{input_dir}`. A paper-bearing location is anything that contains an article body: an indexed subdirectory with `article.nxml` / `article.pdf` / `article_text.txt`, a standalone `.pdf` at the corpus root, a `.pdf` inside a category subfolder, an `article.html` companion, or any other layout the corpus uses. **Descend into subfolders** — past trials have silently missed papers in category subfolders by enumerating only the top level.
>
> Use whatever enumeration mechanism is appropriate for the corpus layout (`ls`, `find`, `glob`). The skill does not prescribe a command because corpora vary.
>
> Write `_corpus_manifest.txt` with one paper-bearing location per line. Verify the count is plausible for the corpus you've been given — if you got 10 lines and expected 200, the enumeration is broken.
>
> **Step 0a — Skip-list with reasons.**
>
> Anything you intentionally exclude from extraction goes in `_skipped.txt`, one line per location:
> `<location>\t<reason>`
>
> Use the most specific reason from this list:
> - `review_no_per_compound_binding`
> - `bare_code_compounds_only`
> - `no_mp_bp_data_in_text`
> - `tga_or_nmr_only_no_mp_bp`
> - `binding_ambiguous`
> - `image_only_compound_table`
> - `formulation_only_no_discrete_compound`
> - `paper_unreadable`
>
> Free-text reasons are permitted but ask the user before using one. **Do not skip a location because a prior trial skipped it** — past trials are reference, not protocol.
>
> **Step 1+ — Per-paper extraction (Template 1).**
>
> For each location in the manifest that is NOT in `_skipped.txt`, apply Template 1. Process each paper independently and append rows to a single CSV. Use a sequential `id` counter across the whole corpus.
>
> **Step N — Sanity checks.**
>
> After all papers are processed, run:
>
> ```bash
> python3 scripts/run_all_checks.py <output.csv>
> ```
>
> **Step N+1 — Account for every manifest entry.**
>
> Your EXTRACTION_SUMMARY.md must include the accounting equation `processed + skipped == manifest`. Report the per-paper summary (rows emitted, rows flagged, INACCESSIBLE entries) AND the per-skip-reason histogram from `_skipped.txt`. Numbers that don't balance indicate silent loss; you must investigate before declaring the run complete.

## Template 3 — Single-paper extraction with smaller scope

For when you only want a subset (e.g., only the values for one named compound, or only experimental measurements):

> Apply Template 1, but only emit rows that match `{filter clause}`. All other rules stay the same — evidence_quote mandatory, no memory extraction, etc.

## Why these rules matter

Past versions of this extraction problem produced 30–60 % error rates when independently spot-checked. The dominant error categories were:

- **Memory-based fabrication.** Without a verbatim evidence quote requirement, agents fill in plausible-sounding values for well-known compounds. Specific decimals are often wrong by 50–200 °C.
- **Wrong-paper citations.** Agents guess at "the most likely primary source" and end up with DOIs pointing at unrelated papers.
- **PDF text artifacts misread as data.** NMR chemical shifts, mass-spec m/z values, and PDF sign-loss artifacts all look numerically like mp/bp values and end up in the database.
- **Truncated / fragmented compound names.** Long IUPAC names split across PDF line breaks get captured as substituent fragments rather than full molecules.
- **Wrong-column / wrong-row binding in dense tables.** Multi-row table headers with `Compound | exp. | calc. | predicted` patterns trip up programmatic extractors. An LLM reading the actual table layout doesn't make this mistake.

Every rule in this template exists because at least one of those failure modes was observed in real prior runs.

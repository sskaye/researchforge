# Extraction prompt templates

Copy-paste these prompts when delegating extraction to a Claude agent. The wording is calibrated to enforce the protocol's hard rules (no memory-based extraction, evidence-locked rows, programmatic sanity checks).

## Template 1: Single-paper extraction

> You have web_fetch, WebSearch, and bash tools — USE THEM. **Do not extract values from training memory under any circumstances.** If you cannot fetch the source, return INACCESSIBLE and stop.
>
> **Task:** Extract every redox-potential measurement from {paper title and citation}. DOI: {DOI}.
>
> **Mandatory steps:**
>
> **Step 1: Fetch and verify.** Run `python scripts/find_open_access.py {DOI}` to discover open-access URLs. Fetch the paper from the first working URL. Verify you have the actual paper (open it, check title and DOI match). If you cannot retrieve the source after trying all URLs, **stop and return INACCESSIBLE — do not synthesize values from memory**.
>
> **Step 2: Confirm metadata.** Run `python scripts/crossref_lookup.py {DOI}` to confirm the paper's title is about redox/electrochemistry/flow batteries (or whatever chemistry the paper is in). If the title is unrelated, the DOI is wrong — flag and stop.
>
> **Step 3: Identify reference-electrode convention.** Read the experimental section. Note exactly which reference electrode the authors used and in what electrolyte. Common patterns:
> - "vs SCE in 0.1 M H₂SO₄"
> - "vs Ag/AgCl (3 M KCl)"
> - "vs Fc/Fc⁺ in 0.1 M TBAPF₆/MeCN"
>
> **Step 4: Locate measurement-bearing tables/figures.** Identify by table number, figure number, or paragraph location. For each, you'll need page or table numbers as evidence_location.
>
> **Step 5: Extract row by row.** For each compound × redox event, produce a row with the schema in SKILL.md. Required per row:
>
> - `id`: integer row identifier
> - `verification_status`: set to `pending_verification` for newly extracted rows. The Phase-4 verifier will upgrade this to `verified_extraction` after passing checks.
> - `molecule`: full name as printed in the source. **Do not abbreviate or truncate.** SMILES allowed if no name available. For multi-couple molecules, include the couple identifier (e.g., "methyl viologen V²⁺/V⁺•").
> - `voltage_v_she`: numeric, in V vs SHE
> - `voltage_raw`: as printed, including original units AND electrolyte (e.g., "−0.47 V vs Ag/AgCl(3M KCl)" — never just "Ag/AgCl" since the electrolyte changes the offset)
> - `reference_electrode`: as the source reports it
> - `evidence_location`: where in the paper this came from (e.g., "Table 1 row 3", "Fig 2 caption", "p. 6469 col 2 ¶ 3")
> - `evidence_quote`: the verbatim text from which the value was extracted
> - `conversion_arithmetic`: if you converted, show the math (e.g., "−0.47 V vs Ag/AgCl(3M KCl) + 0.21 = −0.26 V vs SHE"). Blank if no conversion. Always include the electrolyte spec in the reference name so the offset is unambiguous.
> - `value_directness`: "direct" (measured CV/RDE), "derived" (cell-voltage minus catholyte, range midpoint, figure-position estimate), or "computed"
> - `solvent`, `ph`, `n_electrons` from the source (leave `n_electrons` blank if not stated; never guess)
> - `data_type`: "experimental" or "computational"
> - `source`: journal, year, vol, page (NO author names; the DOI in source_url is canonical). For textbook references (Bard/CRC/Pope), use the title + edition.
> - `source_url`: the DOI URL (preferred) OR `textbook:<short-id>` for textbook entries (e.g., `textbook:CRC-Handbook-102nd`). Must be present.
>
> **Step 6: Self-verify each row.** After extraction, for each row, re-open the source and confirm the evidence_quote is at the stated evidence_location. Drop any row that fails this check.
>
> **Step 7: Run sanity checks.** `python scripts/run_all_checks.py <your-output.csv> --check-dois`. If any rows are flagged, fix them before submitting. Do not submit flagged rows.
>
> **Output:** CSV with the standard schema. Include only rows that pass self-verification AND sanity checks.
>
> **What NOT to do:**
> - Do not generate rows from training memory.
> - Do not include author names in the source field.
> - Do not use placeholder citations like "Author et al."
> - Do not infer values from cell-voltage differences and call them "direct measurements" — set `value_directness = derived`.
> - Do not guess at the reference electrode.
> - Do not extract from figures without OCR; if you must, mark `value_directness = derived` with a note explaining "figure OCR".
>
> If anything in the source is ambiguous (e.g., reference electrode unclear, multiple redox events conflated, unit conversion uncertain), **flag the row** rather than guessing.

## Template 2: Bulk-database extraction

For any structured CSV/XLSX/relational dump of computational data:

> You have web_fetch, WebSearch, bash tools.
>
> **Task:** Extract rows from {dataset citation} where voltage_v_she is in range [{low}, {high}] V vs SHE.
>
> **Mandatory steps:**
>
> 1. Download the dataset via curl. Verify it's the expected file (size, schema). Save locally.
> 2. **Read the dataset's documentation carefully.** Find:
>    - What reference electrode the values are against (often non-SHE).
>    - What conversion the database author claims to apply (and verify if they actually did — past compilations have been incorrect about this).
>    - What solvent / electrolyte assumption applies.
> 3. **Identify the calibration formula** (e.g., "E°_SHE = a × ΔE_rxn + b") and apply it explicitly in `conversion_arithmetic`. For non-trivial conversions (especially absolute-scale or vacuum-referenced storage), **read the dataset's API/schema source code** — paper prose alone is often ambiguous about field semantics.
> 4. **Calibration spot-check, when possible.** If the dataset contains canonical molecules whose redox potentials are known from textbook or canonical primary references (parent quinones like 9,10-anthraquinone, methyl viologen, ferrocyanide, TEMPO, ferrocene, etc.), apply the planned conversion to ≥3 of them and compare to known literature within ±150 mV.
>    - **If any canonical molecule is off by >300 mV after conversion: STOP.** Do not extract any rows under that conversion until you've confirmed the convention against the dataset's API/schema source. The conversion is wrong.
>    - **If the dataset contains no canonical-molecule overlap** (e.g., a screen of novel scaffolds with no overlap with well-studied molecules): proceed with extraction, but explicitly mark all rows as `unverified_computational` and add a note in each row's `notes` field that the calibration could not be externally spot-checked (e.g., "calibration not verifiable; no canonical-molecule overlap with this dataset").
>    - This step is a soft gate, not a hard refusal: it only fires when the gate is testable. Don't invent canonical molecules where there are none in the dataset.
> 5. Extract rows with full evidence:
>    - `evidence_location`: dataset row index
>    - `evidence_quote`: copy of the original row data verbatim (or, for SMILES-only datasets, the SMILES)
>    - `conversion_arithmetic`: the math from raw value to vs-SHE value
>    - `value_directness`: "computed"
>    - `data_type`: "computational"
>    - `source`: the dataset's primary citation (journal, year, vol, page); DOI in source_url
> 6. Run `python scripts/run_all_checks.py <output> --check-dois`.
>
> Output as CSV. `verification_status` is `unverified_computational` for these rows.

## Template 3: Audit-existing-rows pass

For verifying rows already in a database:

> You have web_fetch, WebSearch, bash tools. **Do not generate or correct any values from training memory.**
>
> **Task:** Verify each row in {input_csv} by directly inspecting the cited source.
>
> For each row:
> 1. `python scripts/verify_row.py {input_csv} {row_id}` — runs the programmatic checks.
> 2. If programmatic checks pass, fetch the source via `find_open_access.py`, navigate to `evidence_location`, confirm `evidence_quote` is verbatim present.
> 3. Confirm molecule and value match the quote.
>
> Verdict per row: `verified`, or `flagged_<reason>` (specific check failed), or `inaccessible_source`.
>
> **Critical: do NOT silently make corrections.** Report the discrepancy and let the maintainer decide. If you "correct" a value to match what you think the source should say, you risk introducing the same kind of error you're trying to catch.
>
> **Output:** CSV with `id, verdict, evidence_quote_found?, value_match?, citation_match?, notes`.

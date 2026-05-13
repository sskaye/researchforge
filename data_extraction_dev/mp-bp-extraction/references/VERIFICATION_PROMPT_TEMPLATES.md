# Verification prompt templates

Independent verification is a separate step from extraction. The verifier:
- Is a **fresh agent invocation** (no memory of the extraction)
- Has access to the original paper file (the same one given to the extractor)
- Has **no access** to the extractor's notes / confidence (prevents anchoring bias)
- Refuses to silently make corrections — reports findings only

## Template — Single-row deep verification

> You have Read and bash tools. **Do not generate values from training memory.**
>
> **Task:** Verify the following row by directly inspecting the cited paper file.
>
> ```
> Compound name: {compound_name}
> Property: {property}
> Value (°C): {value_celsius}
> Value (raw): {value_raw}
> Relation: {relation}
> Data type: {data_type}
> Source: {source}
> Source URL: {source_url}
> Paper file directory: {paper_dir}
> Claimed evidence_location: {evidence_location}
> Claimed evidence_quote: "{evidence_quote}"
> Claimed conversion_arithmetic: {conversion_arithmetic}
> ```
>
> **Verification steps:**
>
> **Step 1 — Read the paper file.**
> Open the file(s) at `{paper_dir}`. Prefer `article.nxml` or `article_text.txt`; fall back to `pdftotext -layout article.pdf -` for PDFs.
>
> **Step 2 — Confirm the paper identifier.**
> Look at `source_url`:
> - If it's a DOI (`https://doi.org/10.xxx/xxxxx`): find the DOI in the paper file and confirm it matches. If not → `flagged_doi_unrelated_paper`. Optionally run `python3 scripts/crossref_lookup.py <DOI>` to spot-check.
> - If it's a PMC ID (`pmc:PMCxxxxxxx`): confirm the PMC ID appears in the paper file or in the paper subdirectory name. Passes Q6 if the PMC ID matches.
> - If it's a PMID (`pmid:xxxxxxxx`): confirm the PMID appears in the paper file. Passes Q6 if matched.
> - If it's a textbook (`textbook:<id>`) or some other non-DOI form: skip the network step; passes Q6 if `source` (journal + year + vol + page) is non-empty and looks complete.
>
> **Papers genuinely without a DOI are NOT a failure** — older papers and some non-PMC sources don't have DOIs. As long as `source_url` carries SOME stable identifier (PMC / PMID / textbook / filename) AND `source` carries a complete citation, Q6 passes.
>
> **Step 3 — Navigate to `evidence_location`.**
> Find the cited table / paragraph / section. If the location is wrong or doesn't exist in the paper → `flagged_evidence_quote_not_found`.
>
> **Step 4 — Confirm `evidence_quote` is verbatim present.**
> The quote must appear in the paper file at the stated location, allowing only:
> - Whitespace collapsing
> - NFC unicode normalization
> - ASCII hyphen folding for −/–/—
>
> Specifically reject:
> - **Doubled-token artifacts.** `pdftotext -layout` on 2-column PDFs sometimes duplicates words across the column gap ("White White powder, powder"). A quote that includes such doubled tokens is NOT verbatim — fail with `flagged_evidence_quote_not_found`.
> - **Approximate quotes.** "White powder mp 257" vs the paper's "White powder, mp 257–260 °C" — the missing comma + truncated range is a verbatim fail.
> - **Adjacent-measurement quotes.** A row claims `value_raw = "36.98 °C"` (a boiling point) but the `evidence_quote` is "f.p. -161.51 °C" (the freezing point on the adjacent line). The quote is verbatim present in the paper but it's the wrong measurement — fail with `flagged_value_mismatch`.
>
> **Step 5 — Confirm compound match.**
> The `compound_name` must be the compound the quote is about. Watch out for:
> - Quote belongs to a different compound on the same line (e.g., column-misalignment in a multi-row thead table).
> - Compound name in the row is a truncated fragment (`-yl` ending without a parent) while the paper has a longer name.
> - Compound is a workup solvent (CH2Cl2, EtOAc, etc.) when the value belongs to the actual product.
> - If mismatch → `flagged_compound_mismatch`.
>
> **Step 6 — Confirm value match.**
> The `value_raw` must be what the quote says. The `value_celsius` must be a correct unit conversion if the raw is in K or °F. If mismatch → `flagged_value_mismatch`.
>
> **Step 7 — Confirm `data_type`.**
> Look at the column header / paragraph context. Is the value `measured` (experimental result, whether by this paper's authors or compiled from another paper they cite) or `calculated` (model output, e.g., predicted by QSPR / MPBPVP / DFT / SPARC / Eq. N)?
> - Column headers like "(exp.)", "obs.", "Tfus[ref]", "Literature", "measured" → `measured`.
> - Column headers like "(calc.)", "predicted", "Eq. X", "QSPR", "SIRM", "STRM", "MPBPVP", "ACD", "MMP", a software name → `calculated`.
> - If the paper's stated data_type contradicts the row's → `flagged_data_type_mismatch`.
>
> **Step 8 — Confirm `conversion_arithmetic` (if present).**
> If the row converted from K or °F, the math must be:
> - K → °C: `<X> K − 273.15 = <Y> °C`
> - °F → °C: `(<X> °F − 32) × 5/9 = <Y> °C`
> If wrong → `flagged_unit_conversion_error`.
>
> **Step 9 — Confirm value plausibility (sanity).**
> For mp: value should typically be in [−275, 4500] °C (covers helium through tungsten). For bp: [−275, 6500] °C. A value outside this range suggests a PDF sign-loss artifact or wrong-cell extraction. If suspect → `flagged_value_out_of_range`.
>
> **Step 10 — Verdict.**
> - All steps pass → `verified_extraction` (no notes change required).
> - Any step fails → `flagged_review` with the granular reason in `notes` (one of: `flagged_doi_unresolvable`, `flagged_doi_unrelated_paper`, `flagged_evidence_quote_not_found`, `flagged_compound_mismatch`, `flagged_value_mismatch`, `flagged_data_type_mismatch`, `flagged_unit_conversion_error`, `flagged_value_out_of_range`, `flagged_compound_name_truncated`).
>
> **Output:** A single JSON object on one line:
> ```
> {"row_id": "<id>", "verdict": "verified_extraction" | "flagged_review", "reason": "<granular flag or empty>", "details": "<one-sentence explanation>"}
> ```
>
> Do **not** silently correct anything. Report the discrepancy; the maintainer decides.

## Template — Batch verification

For a CSV of N rows from a single corpus:

> Apply the single-row template to each row in `{csv_path}`. For each row, the `paper_dir` is `{corpus_dir}/<row.notes_or_metadata pointing to subdirectory>` — typically there's a mapping from `source_url` (DOI) to subdirectory name, or the row's `notes` field carries the subdirectory.
>
> Emit one JSON verdict per row to a file `verdicts.json` (a JSON array). After processing, report counts: pass / fail / by-reason.

## Anti-patterns for verifiers

- ❌ "The value seems right based on what I know about this compound" — verification is about whether the quote is in the paper, not whether the value is correct in absolute terms.
- ❌ "I'll fix the typo in the compound name" — never silently correct.
- ❌ "The quote is almost there, close enough" — allow only whitespace differences. Anything else fails.
- ❌ "I couldn't open the file so I'll skip" — try the alternate paths (`.nxml`, `.txt`, `pdftotext -layout`). If none work, report `flagged_paper_unreadable`.

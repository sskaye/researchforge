# Verification prompt templates

Independent verification is a separate step from extraction. The verifier:
- Is a **fresh agent invocation** (no memory of the extraction)
- Has access to the original paper file (the same one given to the extractor)
- Has **no access** to the extractor's notes / confidence (prevents anchoring bias)
- Refuses to silently make corrections — reports findings only

The verification protocol implements the three-tier audit framework. **Q1–Q4 determine PASS/FAIL on correctness (Tier 1).** Q5 is a separate verifiability report (Tier 2) that does NOT affect the PASS/FAIL decision.

For the framing and rationale, see `audit_criteria.md` at the project root.

## Template — Single-row verification

> You have Read and bash tools. **Do not generate values from training memory.** Your only job is to confirm whether the row's claims hold up against the source paper.
>
> **Row to verify:**
>
> ```
> compound_name: {compound_name}
> property: {property}
> value_celsius: {value_celsius}
> value_raw: {value_raw}
> data_type: {data_type}
> source: {source}
> source_url: {source_url}
> evidence_location: {evidence_location}
> evidence_quote: "{evidence_quote}"
> conversion_arithmetic: {conversion_arithmetic}
> paper file directory: {paper_dir}
> ```
>
> **Step 0 — Read the paper file.**
> Open the file(s) at `{paper_dir}`. Prefer `article.nxml` → `article_text.txt` → bash `pdftotext -layout article.pdf -` for PDFs. If you cannot read any source file, the row is unverifiable — return `flagged_review` with reason `flagged_paper_unreadable`.
>
> ---
>
> ## Q1 — Compound + value correctness (Tier 1)
>
> Locate the data this row is about in the paper.
>
> **(a) Is `compound_name` a real chemistry-meaningful name and does it identify the same compound the value belongs to in the paper?**
>
> Pass:
> - Naming style variations (IUPAC vs common, with or without stereo descriptors when paper doesn't specify, serial-code suffix in parens at end).
> - Ionic-liquid `[cation][anion]` shorthand.
>
> Fail (`flagged_compound_name_*`):
> - Mangled / truncated name (`((((2-(2-...` instead of `3-(4-((2-(2-...`; `H-Indeno...` missing leading locant digit).
> - Procedure-text contamination (`(Yield 94%),`, `afforded white solid`).
> - Elemental-analysis line prepended (`C, NN.NN; H, N.NN; N, N.NN.` then the IUPAC).
> - Leading paper-local code prefix (`5 (IUPAC name)` instead of `IUPAC name (5)`).
> - Bare code only (`compound 5`, `4b`).
> - Workup solvent (CH2Cl2, EtOAc, etc.) when the value belongs to the actual product.
> - Section title / journal name / NMR-shift list / vendor label as the name.
>
> **(b) Is the value (`value_celsius`, `value_celsius_min/max`, `value_raw`) the value the paper reports for THIS compound?**
>
> Pass:
> - Within the paper's stated precision.
> - Range shorthand expansion is fine (paper "237-39" = row "237-239").
> - Unit conversion arithmetically correct (K − 273.15 = °C; (°F − 32) × 5/9 = °C).
>
> Fail (`flagged_value_mismatch`, `flagged_compound_mismatch`, `flagged_unit_conversion_error`):
> - Value belongs to a different compound (the "compound 23 with compound 25's m.p." case).
> - Transcription error.
> - Wrong K/°F → °C arithmetic.
> - Value outside the paper's stated range.
>
> Q1 = PASS only if both (a) and (b) pass.
>
> ---
>
> ## Q2 — Property type correctness (Tier 1)
>
> Is `property` the physical phenomenon the paper actually reports for this value? Allowed values: `melting_point`, `boiling_point`, `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`.
>
> Fail (`flagged_property_subtype_mismatch`):
> - `melting_point` for a value the paper explicitly labels "decomposition" or similar.
> - `DSC_peak` for a paper-labeled "DSC onset" (or vice versa).
>
> ---
>
> ## Q3 — Data type correctness (Tier 1, per schema)
>
> The schema has two values: `measured` and `calculated`.
>
> - `measured` = any experimental observation, regardless of who measured it. This includes: the cited paper's own work, values compiled from another paper they cite, review-paper Table 1 of literature values, QSPR-paper "Exp." columns.
> - `calculated` = model output. QSPR, MPBPVP, DFT, SPARC, ACD, MMP, "predicted by ...", "Eq. N".
>
> A review-paper compilation of literature m.p. values labeled `measured` PASSES. A QSPR "Exp." column labeled `measured` PASSES. A QSPR "Calc." column labeled `measured` FAILS (`flagged_data_type_mismatch`).
>
> The clue is the immediate column header or paragraph context, not the paper's nature.
>
> ---
>
> ## Q4 — Source citation reality (Tier 1)
>
> Can a reader reach the actual paper from `source_url` + `source`?
>
> Pass:
> - DOI in `source_url` appears as a substring of the paper file's text.
> - `pmc:PMCxxxxxxx`, `pmid:xxxxxxxx`, `textbook:xxx`, or `legacy:xxx` resolves to the right resource AND `source` carries a complete journal+year+volume+page citation.
>
> Fail:
> - DOI fabricated (doesn't appear in paper file) → `flagged_doi_fabricated`.
> - DOI resolves to a different paper that doesn't contain the data → `flagged_doi_unrelated_paper`.
> - Placeholder citation (`Author et al.`) → `flagged_citation_incomplete`.
> - Paper genuinely not in the corpus and no alternative identifier → `flagged_paper_unreadable`.
>
> ---
>
> ## VERDICT (Q1–Q4 determine this)
>
> All four pass → `verified_extraction`.
>
> Any of Q1–Q4 fails → `flagged_review`. Set `reason` to the most-specific granular flag:
> - `flagged_compound_name_truncated`, `flagged_compound_name_contaminated`, `flagged_compound_mismatch`
> - `flagged_value_mismatch`, `flagged_unit_conversion_error`, `flagged_value_out_of_range`
> - `flagged_property_subtype_mismatch`
> - `flagged_data_type_mismatch`
> - `flagged_doi_fabricated`, `flagged_doi_unrelated_paper`, `flagged_paper_unreadable`, `flagged_citation_incomplete`
>
> ---
>
> ## Q5 — Verifiability (advisory, Tier 2)
>
> Separately, report whether the `evidence_quote` satisfies all of:
> - Verbatim contiguous substring of the paper.
> - Contains the numeric value from `value_raw`.
> - Contains the compound name or its serial code.
>
> If all are true: `verifiable: true`.
>
> If any is false: `verifiable: false` with a tag in `verifiability_tag`:
> - `quote_truncated_before_value` (verbatim but stops before the value, e.g., "Dark red solid;" with the m.p. on the next physical line)
> - `quote_ellipsis_bridge` (`...` joining non-adjacent text in the quote)
> - `quote_templated` (looks constructed: `"Table N: <compound> MP <value>"`)
> - `quote_whitespace_unicode_mismatch` (paper has "(Sp )-", quote has "(Sp)-")
> - `quote_missing_compound_token` (quote contains value but not the compound)
> - `quote_non_contiguous` (PDF column wrap; the quote splices two columns)
> - `quote_paraphrased` (quote is a summary, not a substring)
>
> **Q5 does NOT affect the PASS/FAIL verdict.** A row with `verdict = verified_extraction` and `verifiable = false` is a row whose data is correct but whose evidence quote is harder to spot-check. That's a known and acceptable state.
>
> ---
>
> ## Output
>
> Emit one JSON object per row:
>
> ```json
> {
>   "row_id": "<id>",
>   "verdict": "verified_extraction" | "flagged_review",
>   "reason": "<granular flag or empty>",
>   "details": "<one-sentence explanation>",
>   "verifiable": true | false,
>   "verifiability_tag": "<tag or empty>"
> }
> ```
>
> **Do not silently correct anything.** Report the discrepancy and let the maintainer decide.

## Template — Batch verification

For a CSV of N rows from a single corpus:

> Apply the single-row template to each row in `{csv_path}`. For each row, the `paper_dir` is `{corpus_dir}/<paper_subdir>` — typically there's a mapping from `source_url` to subdirectory (provided as `url_to_folder_map.json`), or you search `corpora/` for a folder containing the DOI/PMC identifier.
>
> Emit one JSON verdict per row to a single file `verdicts.json` (a JSON array). After processing, report counts:
>
> - PASS / FAIL on Q1–Q4 (Tier 1 correctness).
> - Verifiable / not-verifiable on Q5 (Tier 2 verifiability) — independent of PASS/FAIL.
> - Breakdown by `reason` for fails, and by `verifiability_tag` for not-verifiable rows.

## Anti-patterns for verifiers

- ❌ "The value seems right based on what I know about this compound" — verification is against the paper, not against your training knowledge.
- ❌ "I'll fix the typo in the compound name" — never silently correct. Flag and report.
- ❌ "The quote is almost there, close enough" — for Q5 verifiability, only whitespace / NFC / hyphen-fold differences pass. Anything else marks the row as not-verifiable. But this is independent of the PASS/FAIL verdict.
- ❌ "The quote contains a literal `...`, that's forbidden" — **NO. v1.6 removed the ellipsis prohibition entirely.** Ellipsis in the quote affects Q5 (verifiability tag = `quote_ellipsis_bridge`) but does not affect Q1–Q4 (correctness PASS/FAIL).
- ❌ "The quote is `Table N: <compound> MP <value>`, that's templated, fail it" — **NO. v1.6 removed the template-quote prohibition.** Templated quotes affect Q5 only.
- ❌ "The quote stops before the value, fail it" — Affects Q5 (`quote_truncated_before_value`), NOT Q1–Q4. As long as the value the row records IS the paper's value for this compound, Q1 passes.
- ❌ "The paper is a review and labels this `measured`, fail it as wrong data_type" — **NO.** The schema's `measured` = any experimental observation, including literature compilations. Pass Q3.
- ❌ "I couldn't open the file so I'll skip" — try the alternate paths (`.nxml`, `.txt`, `pdftotext -layout`). If none work, report `flagged_paper_unreadable` rather than silently dropping the row.

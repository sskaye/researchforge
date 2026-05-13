# Verification prompt templates

Independent verification is a separate step from extraction. The verifier:
- Should be a **fresh agent invocation** (no memory of the extraction)
- Has access to the original source
- Has **no access** to the extraction agent's confidence/notes (prevents anchoring bias)
- Refuses to make corrections silently — only reports findings

## Template: Single-row deep verification

> You have web_fetch, WebSearch, bash tools. **Do not generate values from training memory.**
>
> **Task:** Verify the following row by directly inspecting the cited source.
>
> ```
> Molecule: {molecule_name}
> Value: {voltage_v_she} V vs SHE
> Raw: {voltage_raw}
> Reference electrode: {reference_electrode}
> Solvent: {solvent}
> pH: {ph}
> Source: {source}
> Source URL: {source_url}
> Claimed evidence location: {evidence_location}
> Claimed evidence quote: "{evidence_quote}"
> Claimed conversion: {conversion_arithmetic}
> ```
>
> **Verification steps:**
>
> 1. Run `python scripts/crossref_lookup.py <DOI>`. Confirm the title is consistent with redox/electrochemistry — if the title is about something completely unrelated (like a tropical-forest paper), report `flagged_doi_unrelated_paper`.
>
> 2. Run `python scripts/find_open_access.py <DOI>` to get an OA copy. Fetch it.
>
> 3. Navigate to the claimed `evidence_location`. Confirm the `evidence_quote` is verbatim present (allow minor whitespace differences only). If absent → `flagged_evidence_quote_not_found`.
>
> 4. Confirm the molecule_name appears in or adjacent to the quote. If not → `flagged_molecule_mismatch`.
>
> 5. Confirm the raw value in the quote matches `voltage_raw`. If not → `flagged_value_mismatch`.
>
> 6. Apply the `conversion_arithmetic`. Check that the result equals `voltage_v_she`. (Or run `python scripts/verify_row.py` for the math.) If not → `flagged_conversion_arithmetic_error`.
>
> 7. Confirm the `reference_electrode`, `solvent`, `ph` match what the source actually states.
>
> **Verdict:**
>
> The verifier returns one of these granular verdicts. When writing back to the
> CSV, set `verification_status = verified_extraction` (or `verified_primary`)
> on pass; set `verification_status = flagged_review` on fail and put the
> specific verdict in `notes` so it's preserved.
>
> - `verified` — all 6 checks pass. Upgrade verification_status.
> - `flagged_doi_unresolvable` — DOI doesn't resolve on CrossRef.
> - `flagged_doi_unrelated_paper` — DOI resolves but to a different paper than the citation claims.
> - `flagged_evidence_quote_not_found` — quote not at the stated location (or anywhere in the source).
> - `flagged_value_mismatch` — quote found but the numeric value differs from voltage_v_she.
> - `flagged_molecule_mismatch` — value found but for a different molecule than claimed.
> - `flagged_reference_electrode_mismatch` — source uses a different reference than claimed.
> - `flagged_conversion_arithmetic_error` — conversion math doesn't check out.
> - `flagged_metadata_mismatch` — solvent, pH, or n_electrons don't match source.
> - `inaccessible_source` — couldn't retrieve the source after trying open-access mirrors.
>
> **Output:**
>
> ```
> Verdict: <one of the above>
> Source confirmed: <yes/no, with title>
> Evidence quote found at stated location: <yes/no, with what was actually found if no>
> Molecule confirmed: <yes/no>
> Value confirmed: <yes/no, with stated and observed values>
> Reference electrode confirmed: <yes/no>
> Conversion arithmetic confirmed: <yes/no>
> Notes: <brief explanation of any failure>
> ```
>
> **Critical: do NOT silently make corrections.** Report the discrepancy. Do not return a "fixed" version of the row.

## Template: Bulk verification pass

For verifying many rows at once:

> You have web_fetch, WebSearch, bash tools. No memory-based corrections allowed.
>
> **Task:** Verify each row in `{input_csv}` against its cited source.
>
> For each row, run the 6-check verification (see "Single-row deep verification"). Record results in an output CSV.
>
> **Optimization for bulk:** group rows by source. For each source, fetch it once via `find_open_access.py`, then verify all rows from that source in one pass. This avoids re-downloading.
>
> **Output:** `{output_csv}` with columns:
> `#, verdict, source_confirmed, quote_found, molecule_confirmed, value_confirmed, ref_electrode_confirmed, conversion_confirmed, notes`
>
> Aim to verify at least 10-20 rows per minute.
>
> If a source becomes inaccessible mid-batch, mark all its rows as `inaccessible_source` and continue with other sources.

## Template: Random spot-check audit

> You have web_fetch, WebSearch, bash tools.
>
> **Task:** Audit the redox database `{input_csv}` by spot-checking a random sample of N={N} rows.
>
> 1. Use Python with a fixed random seed to sample N rows (stratified across `verification_status` tiers if possible: 50% `verified_*`, 30% `spot_checked`, 20% `flagged_*` to test that flags are real).
>
> 2. For each sampled row, run the single-row deep verification.
>
> 3. Tally verdicts. **If the verified-row failure rate exceeds 5%, escalate**: the database needs deeper audit.
>
> 4. **Independent check on systematic issues:** for each "verified" row that fails, look at the neighbors in the source (other rows from the same source). Determine whether the failure is row-specific or systemic across the source.
>
> Output the sample, the verdicts, and a short diagnostic on any systematic issues found.

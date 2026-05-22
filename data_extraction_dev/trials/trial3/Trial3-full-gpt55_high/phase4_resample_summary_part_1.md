# Phase 4 Resample Verification Summary - Part 1

Input: `Trial3-full-gpt55_high/phase4_resample_clean_part_1.csv`

Output: `Trial3-full-gpt55_high/phase4_resample_verdicts_part_1.json`

Rows checked: 25

- Verified: 22
- Flagged for review: 3

Flagged rows:

- Row 183: `flagged_value_mismatch` - quote is present, but the source prints `Mp = 174-76°C`; row `value_raw` is `174-176°C`.
- Row 343: `flagged_metadata_mismatch` - PDF text contains DOI `10.3762/bjoc.10.317`, but `source_url` is `legacy:manifest_178`.
- Row 419: `flagged_evidence_quote_not_found` - compound/value are in the HTML, but the submitted quote is not present in raw HTML under whitespace/hyphen normalization.

No CSV files were edited.

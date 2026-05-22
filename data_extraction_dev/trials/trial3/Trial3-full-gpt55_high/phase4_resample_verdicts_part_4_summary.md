# Phase 4 Resample Verification - Part 4

Input CSV: `phase4_resample_clean_part_4.csv`

Rows audited: 25

Verdicts:
- `verified_extraction`: 19
- `flagged_review`: 6

Flagged rows:
- Row 389: `flagged_evidence_quote_not_found` - HTML source supports the value, but the CSV quote is rendered text rather than a contiguous raw HTML source substring.
- Row 350: `flagged_evidence_quote_not_found` - PDF source supports the value, but the CSV quote is reconstructed/dehyphenated rather than a normalized contiguous source substring; source_url also uses `legacy:manifest_181` despite a DOI appearing in the paper.
- Row 393: `flagged_evidence_quote_not_found` - HTML source supports the value, but the CSV quote is rendered text rather than a contiguous raw HTML source substring.
- Row 131: `flagged_value_mismatch` - cited quote says `112+-2 deg C`, while the row records `112-114 deg C` and midpoint `113.0`.
- Row 427: `flagged_evidence_quote_not_found` - HTML source supports the value, but the quote joins a heading and paragraph across intervening markup/image content.
- Row 413: `flagged_evidence_quote_not_found` - HTML source supports the value, but the quote joins a heading and paragraph across intervening markup/image content.

No CSV files were edited.

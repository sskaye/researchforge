# Phase 4 Verification Summary - Part 3

Verified only rows from `phase4_sample_part_3.csv` against source files identified by each row's `notes` `paper_path=` field.

- Rows checked: 25
- Verified extractions: 22
- Flagged for review: 3

## Flagged rows

- `372`: `flagged_evidence_quote_not_found` - table value is supported, but the claimed quote is non-contiguous across omitted table rows.
- `395`: `flagged_compound_mismatch` - quoted raw HTML is for compound 2, while the row claims bis(1,2,3-triazole) derivative 10.
- `409`: `flagged_evidence_quote_not_found` - HTML supports the value, but the claimed plain-text quote is not present verbatim under allowed normalization because markup separates heading and paragraph text.

## Reason counts

- `flagged_compound_mismatch`: 1
- `flagged_evidence_quote_not_found`: 2

# Phase 4 Verification Summary - Part 1

Verified `phase4_sample_part_1.csv` against the supplied local paper files using the row `notes` `paper_path=...` value as the source path.

## Counts

- Total rows checked: 25
- Verified extractions: 19
- Flagged for review: 6

## Flagged Rows

- Row 294: `flagged_compound_mismatch` - source has compound 26b as `(2R,4R,E)`, while the row/quote state `(2S,4S,E)`.
- Row 355: `flagged_evidence_quote_not_found` - PDF supports the compound/value, but the asserted quote is not present under the allowed normalization.
- Row 366: `flagged_evidence_quote_not_found` - the specified `paper_path` HTML file is only a Europe PMC shell and does not contain the asserted quote/value.
- Row 206: `flagged_value_mismatch` - source prints `mp: 220-22°C`; row expands `value_raw` to `220-222 °C`.
- Row 214: `flagged_value_mismatch` - source prints `mp: 154- 55°C`; row expands `value_raw` to `154-155 °C`.
- Row 135: `flagged_compound_mismatch` - source identifies compound 10 as `1-(2,4-Difluorophenyl)-2-(1H-1,2,4-triazol-1-yl)ethanol`, while the row uses a generic compound name and the quote lacks the row compound identity.

The final CSV was not edited.

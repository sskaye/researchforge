# Phase 4 Verification Summary - Part 2

Verified only rows in `phase4_sample_part_2.csv` against source files under `corpora/full_168` and the Trial3 output directory. The final CSV was not edited.

- Rows checked: 25
- Verified extractions: 24
- Flagged for review: 1

Flagged row:

- Row 138: `flagged_evidence_quote_not_found` - the quote is present near the Ia synthesis and contains the value, but the quoted span itself does not contain the compound name or `Ia` label required by the evidence-quote rule.

Notes:

- Legacy source URLs were accepted where the supplied file lacked the DOI but the citation and row notes identified the source.
- For row 368, the article HTML was not useful for article-body verification, but the PDF named in the row notes contained the supporting Table 3 text.

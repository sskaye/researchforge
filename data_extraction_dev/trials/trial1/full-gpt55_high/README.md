# Trial1-full-gpt55_high mp/bp extraction

Input root: `/Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/mp_bp_full_set`

Output CSV: `mp_bp_extracted.csv`

Rows extracted: 304

Property counts:
- melting_point: 292
- boiling_point: 9
- decomposition: 3

Data-type counts:
- measured: 295
- calculated: 9

Verification status:
- pending_verification: 304

Coverage:
- source files with extracted rows: 65
- DOI rows: 166
- PMC rows: 4
- legacy local-source rows: 134

Phase 3 checks:
- required-field check: pass
- validate_compound_name.py: pass
- value_range_check.py: pass
- unit_conversion_arithmetic.py: pass
- verify_doi.py: pass
- verify_evidence_quote.py: pass
- dedup_within_paper.py: pass

Notes:
- The extractor was deliberately conservative and only emitted rows with exact source-file evidence quotes.
- `skipped_sources.csv` lists readable sources where no conservative inline mp/bp/decomposition/sublimation value was emitted.
- `source_file` is included as an extra provenance column for local verification, especially for PDF/HTML sources represented with `legacy:` source URLs.
- Rows remain `pending_verification` because no independent fresh-agent Phase 4 verification pass was run in this thread.

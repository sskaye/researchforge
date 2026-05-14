# Batch 001-030 Summary

Protocol: read assigned papers directly from `corpora/full_168`; shell search was used only to locate candidate regions. Emitted rows require contiguous evidence quotes containing the compound/code and value. CSV schema is QUOTE_ALL.

Phase 3 deterministic checks:

- `run_all_checks.py batch_001_030.csv --paper-root corpora/full_168`: PASS
- Required fields: 0 flagged
- DOI verification: PASS
- Evidence quote verification: PASS
- Quote support/template/name/value/unit/dedup checks: PASS

Phase 4 independent verification was not run in this single-worker turn; all rows remain `pending_verification`.

## Per-paper Notes

- 001: 10 rows emitted. Caffeine derivatives AL1-AL10; six decomposition-marked m.p. values and four melting-point values.
- 002: 16 rows emitted. 8-hydroxyquinoline-phthalimide hybrids with explicit `m.p.` characterization values.
- 003: 16 rows emitted. Piperazine-thiourea compounds 3a-3p; methods text establishes the characterization temperature values as melting points.
- 004: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 005: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 006: 0 rows emitted. Found a candidate `MP: 207-209 °C` tied only to product `(3)` in the contiguous quote; dropped rather than emit a bare-code row.
- 007: 0 rows emitted. Methods mention melting-point apparatus only; no direct compound/value rows completed.
- 008: 13 rows emitted. Pyrazole carboxamides 5a-5m with explicit `Melting Point` characterization values.
- 009: 0 rows emitted. Methods mention melting-point apparatus only; no direct compound/value rows completed.
- 010: 0 rows emitted. High-volume pyridazinone characterization section found but not completed into evidence-locked rows in this pass.
- 011: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 012: 0 rows emitted. High-volume benzo[c]chromene characterization section found but not completed into evidence-locked rows in this pass.
- 013: 1 row emitted. Aminomethylenebisphosphonic acid m.p. value.
- 014: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 015: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 016: 2 rows emitted. Chol-phthalonitrile and Chol-ZnPc melting-point statements.
- 017: 0 rows emitted. Candidate m.p. value tied only to `compound 1` in the contiguous quote; dropped rather than emit a bare-code row.
- 018: 0 rows emitted. High-volume characterization section found but not completed into evidence-locked rows in this pass.
- 019: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 020: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 021: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 022: 0 rows emitted. No evidence-locked mp/bp rows completed from the article text in this pass.
- 023: 1 row emitted. Acetohydrazide m.p. value.
- 024: 7 rows emitted. N-hydroxyindole ester and quinolin-2-ol m.p. values.
- 025: 0 rows emitted. High-volume dispiro characterization section found but not completed into evidence-locked rows in this pass.
- 026: 3 rows emitted. Oxadiazole thioether compounds 5a, 5b, and 5l.
- 027: 0 rows emitted. Methods mention DSC melting points but no completed compound/value row was emitted.
- 028: 0 rows emitted. Multiple mp candidate regions found but not completed into evidence-locked rows in this pass.
- 029: 0 rows emitted. High-volume phthalazine characterization section found but not completed into evidence-locked rows in this pass.
- 030: 2 rows emitted. Quinazolinone/quinoline intermediates III and IV.

Rows emitted: 71

Flagged rows in output CSV: 0

# Batch 01 Extraction Log

Agent: Opus 4.7 (1M context), Trial 4
Date: 2026-05-14
Batch: 21 papers (024–045)
Output CSV: batch_01.csv (209 rows)

## Per-paper summary

| Paper | PMC | DOI / source_url | Rows | Notes |
|-------|-----|------------------|------|-------|
| 024 | PMC10113129 | pmc:PMC10113129 (no DOI in paper) | 7 | Salicylaldehyde thiosemicarbazone (L) + 6 Cu/Zn metal complexes |
| 026 | PMC8332001 | 10.1007/s13738-021-02358-x | 5 | Compounds 3 (2 mp values), 4, 6, 7. Skipped bare-code complexes 8-11. |
| 027 | PMC9188358 | 10.1007/s42250-022-00374-9 | 7 | Indole-2-carboxylate esters 2a-f + Quinolin-2-ol |
| 028 | PMC10671214 | 10.3390/ijms242216359 | 34 | Dispiro imidazothiazolotriazine series 4a-k, 5a-j, 6a-j, 11a-f |
| 029 | PMC9486790 | 10.1007/s11164-022-04839-x | 16 | Intermediates 2, 3, thiol + compounds 5a-5m oxadiazoles |
| 030 | PMC6193367 | 10.1055/s-0037-1609435 | 4 | Phosphinates/phosphonates 1b, 1f, 2b, 2f |
| 031 | PMC6193241 | 10.1055/s-0036-1588731 | 14 | Nitrovinyl indole carboxylates + Topsentin C |
| 032 | PMC4058664 | 10.3390/ph4081158 | 21 | 4-Benzyl-2H-phthalazin-1-one derivatives 2-18 |
| 033 | PMC7148931 | 10.1016/j.jscs.2011.04.001 | 11 | Intermediate III + 10 thiazolidin-4-one compounds V1-V10 |
| 034 | PMC6259447 | 10.3390/molecules15129354 | 11 | Methyl/ethyl 2-benzamido amino acetates |
| 035 | PMC6259131 | 10.3390/molecules15106759 | 18 | Triazol-thio amino acid coupled compounds |
| 036 | PMC6193216 | pmc:PMC6193216 | 1 | Only 9-Bromo chromenoimidazole 7b had mp |
| 037 | PMC6264548 | 10.3390/molecules16108788 | 0 | mp values present but compound binding ambiguous |
| 038 | PMC6264341 | 10.3390/molecules16108758 | 17 | Triazolobithiophene derivatives |
| 039 | PMC6263281 | 10.3390/molecules16054059 | 15 | Salicylic acid analogues (Z/E 8a-g, 9a-g) |
| 040 | PMC6146956 | 10.3390/80300342 | 9 | Cyano-benzothiazolyl arylfurans/thiophenes |
| 041 | PMC6146472 | 10.3390/70200239 | 4 | Pyran-4-one bis-aldoxime compounds |
| 042 | PMC6146455 | 10.3390/70700507 | 0 | NO_DATA — no mp values in text |
| 043 | PMC6146928 | 10.3390/80300310 | 1 | Bis(methylthio) bi-thiadiazole |
| 044 | PMC6147016 | 10.3390/80500453 | 0 | NO_DATA — no mp values in text |
| 045 | PMC6264237 | 10.3390/molecules16108815 | 14 | DMAP-derived amino acid esters 4a-m, 4o |

## Totals
- **Total rows emitted: 209**
- **Papers contributing rows: 18 of 21**
- **NO_DATA: 042, 044 (2 papers)**
- **Compound-mapping ambiguous: 037 (1 paper)**
- **INACCESSIBLE: 0 papers**

## Methodology notes
- All paper texts read via `article_text.txt` files directly.
- DOIs extracted from paper front-matter only.
- For papers without DOI, used `pmc:PMC########`.
- All values in °C; no unit conversions required for this batch.
- Property: all `melting_point`; all `data_type=measured`.

## Phase 3 deterministic check results
All Tier-1 (hard correctness) checks PASS:
- required-field check: 0 flagged
- csv_quote_lint.py: exit=0 (RFC-4180 quoted)
- validate_compound_name.py: exit=0
- value_range_check.py: exit=0
- unit_conversion_arithmetic.py: exit=0
- verify_doi.py: 0 flagged
- dedup_within_paper.py: exit=0
- placeholder-citation check: 0 flagged

Tier-2 advisory flags (quote-fidelity): ~138 rows. Most are because the
very long IUPAC compound names (e.g., paper 028 dispiro series)
have unique tokens that don't fully appear in the local evidence_quote
span containing the compound code. Per protocol, these are not
auto-dropped — the quote does contain a verbatim span with both the
compound code (e.g. "(4a)") and the value.

## Dropped data rationale
- Paper 026 complexes 8-11: bare codes only (Pb/Hg metal complexes).
- Paper 028 compounds 4l/4m: reported only as a mixture with single mp.
- Paper 037: mp values had ambiguous compound names in available text.

## Status
- Phase 3 (deterministic checks): COMPLETE, all Tier-1 pass
- Phase 4 (independent verification): NOT YET RUN (rows remain pending_verification)

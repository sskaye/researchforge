# batch_00 extraction log

| # | Paper | rows | notes |
|---|---|---|---|
| 1 | 001 PMC12938810 (caffeine xanthine hydrazides) | 10 | AL1-AL10; mostly dec. values |
| 2 | 003 PMC12943044 (Mannich 8-HQ-phthalimide) | 16 | compounds 2-5, 6a-9c |
| 3 | 004 PMC13084458 (piperazine-thiourea) | 16 | 3a-3p, single values |
| 4 | 005 PMC12987641 (indenoquinolinyl phosphine oxide) | 24 | 9a-9m,10e,11a-11m |
| 5 | 006 PMC13006720 (nitrofuryl thiadiazole) | 14 | compounds 7-20 |
| 6 | 007 PMC13093257 (imidazopyridine PIM) | 1 | only compound 3 (intermediate) |
| 7 | 008 PMC12944436 (terpene-imatinib) | 9 | 6a-6i |
| 8 | 009 PMC12943507 (arylazo pyrazole carboxamide) | 13 | 5a-5m |
| 9 | 010 PMC12940417 (TRPA1 modulators) | 28 | mixed compounds 1,6,10-25,27-36 |
| 10 | 011 PMC12943719 (PDE4 pyridazinone) | 0 | mp's not reported in main text |
| 11 | 012 PMC12987640 (sigma1R/HDAC dual) | 8 | 2a-4b |
| 12 | 013 PMC12943095 (benzo[c]chromene) | 34 | 1a-5s |
| 13 | 014 PMC12943640 (bisphosphonates) | 35 | compounds 1-35 incl. three >300°C |
| 14 | 015 PMC12943364 (PB2/JAK2 dual) | 5 | PB01-PB05 |
| 15 | 017 PMC10673250 (ibuprofen amino acid salts) | 9 | DSC Tm from Table 2 |
| 16 | 018 PMC10672206 (Chol-ZnPc) | 2 | one >300, one =186 |
| 17 | 019 PMC11203683 (phosphacoumarin) | 10 | compounds 1,2a-2l,3 |
| 18 | 020 PMC11206691 (HBV RNase H) | 32 | compounds 1-13,33-57 (drop A,B – bare codes) |
| 19 | 021 PMC10673159 (pyrylium terphenyl) | 15 | 10a-10o |
| 20 | 022 PMC9764318 (Ca(IO3)2 nano) | 0 | mp values in tables but no IUPAC names |
| 21 | 023 PMC9790764 (1,3-disubstituted ureas) | 9 | 4a-4i |
| 22 | 024 PMC10113129 (thiosemicarbazone Cu/Zn complexes) | 7 | ligand L + 6 metal complexes |
| 23 | 026 PMC8332001 (oxadiazole/triazole thiones) | 4 | compounds 3,4,6,7 |
| 24 | 027 PMC9188358 (1-hydroxyindole-2-carboxylate) | 7 | 2a-2f + quinolin-2-ol |
| 25 | 028 PMC10671214 (dispiro imidazothiazolotriazine) | 30 | 4a-11f (dropped 4l/4m mixture) |
| 26 | 029 PMC9486790 (oxadiazole thioether pesticide) | 13 | 5a-5m |

**Summary**
- Papers processed: 26
- Papers with rows: 24 (papers 011 and 022 yielded zero rows)
- Total rows emitted: 352
- All Phase 3 deterministic checks pass (exit=0): required-field, csv_quote_lint, quote_template_lint, quote_support_lint, validate_compound_name, value_range_check, unit_conversion_arithmetic, dedup_within_paper, placeholder-citation
- 9 advisory warnings (quote-support): rows 006-7, 007-3, 015-PB01..PB05, 019-1 — evidence_quote contains compound code (e.g. "PB01", "(3)", "compound 1") rather than full IUPAC name. Per spec, code/label is acceptable when it appears with the value in a contiguous verbatim substring.
- Notable drops:
  - paper 011: paper says "Melting points were determined" but no mp values reported in main text (likely supplementary)
  - paper 022: table values used only generic codes (4a-l, 3m-q) without IUPAC names — dropped per "bare codes" rule
  - paper 020: A, B intermediates dropped (only labeled "compound A" / "compound B", no IUPAC name)
  - paper 028: 4l/4m diastereomeric mixture skipped (entry uses "and" joining names)
- Property mix: mostly melting_point; ~25 decomposition (papers 001, 003, 020); 17 DSC Tm rows from paper 017 Table 2
- All `verification_status = pending_verification` awaiting Phase 4

# Batch 07 extraction log

Source corpus: `/sessions/sweet-laughing-turing/mnt/data_extraction_dev/corpora/full_168/`
Output CSV: `/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_07.csv`
Total rows emitted: 102
Rows flagged: 0

## Per-paper summary

| # | Paper dir | Rows | Notes |
|---|-----------|------|-------|
| 167 | PMC3002819 Posters PDD/PMS/PNM/PPAT/POT | 0 | NO_DATA — only formulation mp (NLC 45.1°C, not a discrete compound); skipped |
| 168 | PMC3756327 Quality not Quantity Marine NP | 1 | Sulfolane mp 28°C |
| 169 | PMC11843341 Triazole-Indole-Pyrazolone | 15 | Compounds 5a–5o, all full IUPAC names + mp ranges |
| 170 | PMC11843339 Mycophenolic Acid Analogues | 9 | DOI 10.1021/acsbiomedchemau.4c00079; compounds 2a, 2c, 2d, 2e, 3a, 3c, 4b, 4c, 6a |
| 171 | PMC11206658 1,2-Dihydroisoquinolines (Pd) | 6 | Compounds 2e, 4af, 4ag/4da, 4ah, 4ba, 4ca (wide mp ranges as printed) |
| 172 | PMC11209911 Ieodomycins A and B | 8 | Stereoisomers 26a–26d (mp 104–106°C) + 26a-1–26d-1 (mp 55–57°C) |
| 173 | PMC10914095 Mechanically interlocked / Rh | 0 | NO_DATA after dropping: compound names ("HC≡C(CH₂)6...", "PNP-14·2S", "compound 3") all bare codes / shorthand failing protocol drop criteria |
| 174 | PMC11203676 Coumarin-Sulfonamide-Triazole | 12 | Compounds 2, 10a, 11a–c, 12a, 13a–c, 14a–c |
| 175 | PMC11206905 Naphtho[2,3-d]thiazole-4,9-Diones | 8 | Compounds 2, 3, 5a–5e, PNT |
| 176 | PMC11206253 4,5-Dihydro-1,2,4-Triazoline + carbohydrate | 10 | Compounds 8a–8j |
| 177 | PMC11206731 β-Carbonyl Selenides Ester | 2 | Compounds 12, 13 |
| 178 | PMC11208899 Cu-Vit B3 MOF benzoxanthenones | 3 | DOI 10.1039/d4ra03468f; compounds 4h, 4i, 4j (the new derivatives) |
| 179 | PMC10763744 BODIPY Au(III) probe | 0 | NO_DATA — only "BOD-AP" (compound shorthand/bare code) |
| 180 | PMC12943207 PEGylation Next-Generation Polymers Review | 0 | NO_DATA — Tg / Tcp values only; mp values are for polymeric mixtures (PG3-C16/C18, PG2-C18), not discrete compounds |
| 181 | PMC10806150 Geranylacetone derivatives | 11 | Compounds 1a–1l (no 1k — duplicate of 1j name in source) |
| 182 | PMC10804403 Amodiaquine process development | 6 | Compounds 9, 10, 5, 12, 14, 3 (Amodiaquine itself) |
| 183 | PMC9007260 Isatin Imidazole derivatives | 11 | Compounds 1a–1c, 2a–2b, 3a–3d, 4a–4b (mostly decomposition points) |

## Phase 3 deterministic checks

All Tier-1 checks PASS:
- required-field check: 0 flagged
- csv_quote_lint.py: exit=0
- validate_compound_name.py: exit=0
- value_range_check.py: exit=0
- unit_conversion_arithmetic.py: exit=0
- dedup_within_paper.py: exit=0
- placeholder-citation check: 0 flagged

Tier-2 advisory flags (quote_support_lint): ~33 rows where evidence_quote captures the local clause containing the mp value but the IUPAC compound_name appears just before (separated by HRMS / EA / synthesis label / α[D] data). These are quote-fidelity concerns only and do not affect correctness per protocol. Per SKILL.md these "flag for maintainer review; they do NOT auto-drop the row."

## Status

- INACCESSIBLE papers: 0
- NO_DATA papers: 4 (167, 173, 179, 180)
- Papers contributing rows: 13
- All rows `verification_status=pending_verification`, awaiting Phase 4 audit.

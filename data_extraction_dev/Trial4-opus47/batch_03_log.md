# Batch 03 Extraction Log

Total rows emitted: 190
Papers contributing rows: 14
Papers with no extractable mp/bp data: 7

## Per-paper summary

| Paper | Rows emitted | Status / Notes |
|---|---|---|
| 069_PMC12984852 (Tricyclic Pyrrole / Zika) | 27 | mp data for compounds 11-14 and 1a-1k, 2a-2l |
| 070_PMC12985466 (PCNA Inhibitor AOH1996) | 18 | mp data for compounds 1a-1g, 2a-2c, 2e-2g, 3a-3b, 3d-3f (2d, 3c skipped: oils) |
| 071_PMC12943180 (PdII complexes/Aldol Mori) | 10 | mp data for (S)-3, (S)-4, 5a-5d, 6a-6d. Decompositions for (S)-3, (S)-4 |
| 072_PMC12943595 (Quinolone Carboxamides) | 0 | NO mp/bp data — only describes melting-point method |
| 073_PMC13085778 (Schiff bases) | 0 | NO explicit mp values reported for compounds I-V |
| 074_PMC12941172 (NHC Au/Pt Complexes) | 6 | mp data for compounds 5, 6, 8, 11, 12, 13 (4 of 6 are decompositions) |
| 075_PMC12937307 (Pyrazole) | 15 | mp data for compounds 4a-4d, 5a-5d, 6a-6g |
| 076_PMC11152677 (CdS/CeO2/Ag3PO4) | 0 | NO direct compound names — Table products are structure images only |
| 078_PMC10763787 (bis-isoxazole) | 2 | mp data from Table 2 compounds 2 and 3 |
| 079_PMC10672842 (Anti-Trypanosoma cruzi) | 6 | mp data for compounds 4-9 |
| 080_PMC9903363 (dibenzofulvene) | 3 | All 3 compounds have mp >300 °C |
| 081_PMC8540882 (microporous polymers/CO2) | 0 | NO mp/bp data — TGA only |
| 082_PMC7332229 (Azaphenantherene/SARS-CoV-2) | 0 | NO mp/bp data |
| 083_PMC4058676 (2-Ethoxybenzoxazinone) | 30 | mp data for compounds 2, 3, 4a-4e, 5a-5e, 6a-6d, 7-13, 14a-14c, 15, 16a-16c |
| 084_PMC5445742 (Aryliron Complexes) | 7 | mp data for 2f, 2h, 2i, 2j, 2k, 2o, 2u |
| 086_PMC6146888 (α-Aminophosphonates) | 16 | mp data for compounds 4a-4p |
| 087_PMC6146877 (2-Arylhydrazonopropanals) | 24 | mp data for compounds 1c, 3a-3g, 6, 8a-8d, 9a-9d, 13-15, 16a-16b, 17a, 18 |
| 088_PMC6146868 (Pentafluorophenyl-pyrrole) | 7 | mp data for compounds 1, 2a-2c, 3a-3c |
| 089_PMC6147034 (Dichlorocarbene/CCl4) | 0 | NO direct compound names — Table products are structure images only |
| 090_PMC6146422 (Triazolothiadiazoles) | 18 | mp data for compounds 2a-2r |
| 091_PMC3685385 (Sulfonium Ionic Liquids) | 1 | Only one solid compound ([C2Allylsul]Br, mp 145°C). Other 8 are liquids with Tg only — declined Tg/Tm column-attribution ambiguity from text |

## INACCESSIBLE papers
None — all 21 papers had readable PDF/NXML.

## Phase 3 check result
All Tier-1 checks PASS (exit=0):
- required-field check: 0 flagged
- csv_quote_lint.py: exit=0
- validate_compound_name.py: exit=0
- value_range_check.py: exit=0
- unit_conversion_arithmetic.py: exit=0
- dedup_within_paper.py: exit=0
- placeholder-citation check: 0 flagged

Tier-2 (advisory) quote-fidelity flags: Many rows lack a recognizable compound-name token in the quote span because the paper's compound name typically appears on the line above the quoted "Yield/m.p." line in section-by-section format. These are documented as advisory and do not auto-drop per protocol.

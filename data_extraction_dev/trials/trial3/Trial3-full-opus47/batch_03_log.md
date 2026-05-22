# Batch 03 extraction log

26 papers processed, 25 yielded rows, 1 dropped (p089).

## Per-paper row counts
- p086 (10.3390/80100186): 16 rows (16 aminophosphonates 4a-4p)
- p087 (10.3390/81200910): 24 rows (1c, 3a-3g, 6, 8a-8d, 9a-9d, 13, 14, 15, 16a-16b, 17a, 18)
- p088 (10.3390/80700536): 7 rows (1, 2a-2c, 3a-3c)
- p089: SKIPPED — Table 1 listed only entry letters a-k for bp/mp; chemical names appear separately in experimental section without their mp/bp, so quote rule (must contain both compound name and value) cannot be satisfied verbatim.
- p090 (10.3390/70800681): 18 rows (2a-2r triazolothiadiazoles)
- p091 (Int J Mol Sci 2007 8:304): 2 rows (compound 1 mp 145°C, compound 3 Tm from Table 1)
- p092 (10.3390/60900784): 24 rows (7a-d, 8a-d, 9a-d as base+HCl pairs). Intermediates 12-23 in table omitted: table contains only "Comp. No." with no chemical name in contiguous text.
- p093 (10.3390/80800622): 9 rows (compounds 5, 6, 7, 8, 14, 15, 16, 17, 18). Table II compounds 9-12,19-26 omitted (table lacks chemical names alongside mp).
- p094 (10.3390/70100096): 7 rows (7, 8, 9, 10a-10c, 11)
- p095 (10.3390/60300267): 22 rows (2a-2f, 3a-3f, 4, 5a-5c, 6a, 6b, 7 (alt), 9, 10)
- p096 (10.3390/61000803): 7 rows (6a, 7a, 1a, 3, 4, vincadifformine N-oxide, 16-oxoaspidospermidine)
- p097 (10.3390/70200124): 13 rows (1a-1g amides + 4a-g pyridinone/quinolinone from Table 1; 4f oil dropped; 4b reported as decomposition)
- p098 (10.3390/80700541): 22 rows (compounds 2, 7, 10, 12, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34) — chemical names from section titles bridged to "Compound N obtained ... mp X" sentences.
- p099 (10.3390/60300194): 9 rows (3, syn-4 DNPH, syn-6 DNB, anti-9, syn-7, anti-10, syn-4 tosylhydrazone, 12, 13)
- p102 (10.3390/60400300): 16 rows (4a, 4b, 5a, 5b, 6a, 6b, 8, 9, 10, 11, 14, 17a, 17b, 20, 24, 25)
- p103 (10.3390/71000756): 18 rows (compounds 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17a, 17b, 18)
- p104 (10.3390/80200243): 2 rows (Tet A precursor and naphthylmethyl-Tet A)
- p105 (10.3390/60500481): 3 rows (36, 18, 7)
- p106 (10.3390/60800683): 7 rows (6, 7, 17, 18, 12, 19, 20)
- p107 (10.3390/60100052): 9 rows (1, ChoTs, 2, DCA, LF, 1a, 1b-α, 1b-β, recovered 2)
- p112 (10.1016/j.jobcr.2024.01.008): 1 row (title pyrazole-carbothioamide)
- p113 (10.1021/acsomega.6c01037): 12 rows (5, 6a, 6b, 7a, 7b, 8a, 8b, 9a, 9b, 11, 12, 1). Compound 10 dropped — text said "50 mg of 11" although section header was for 10 (likely typo).
- p114 (10.1039/d5ra09311b): 19 rows (12a-12s coumarin-triazole hybrids)
- p115 (10.3389/fchem.2026.1758992): 1 row (compound 4c, mp 85-95°C)
- p116 (10.3390/molecules31050796): 12 rows (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
- p117 (10.3390/molecules31040595): 16 rows (15a-15h, 16a-16b, 17a-17d, 18a-18b)

## Total rows: 296

## Phase 3 deterministic check results
All checks pass (after fixes):
- csv_quote_lint.py: PASS
- quote_template_lint.py: PASS (ellipses removed, contiguous quotes restored for p102 6a/8/9/10/14 and p103 18)
- quote_support_lint.py: PASS (advisory warnings only — quotes contain compound code rather than full name token; allowed under rules)
- validate_compound_name.py: PASS (p087_3d name re-balanced)
- value_range_check.py: PASS
- unit_conversion_arithmetic.py: PASS (value_raw normalized from "oC" → "°C")
- dedup_within_paper.py: PASS
- required-field check: 0 flagged
- placeholder-citation check: 0 flagged

## Notes / drop reasons
- p089 dropped entirely.
- p092 omits intermediates 12-23 (table lacks chemical names in contiguous span).
- p093 omits Table II rows 9-12, 19-26 (table lacks names in contiguous span).
- p097 4f dropped (oil — no mp).
- p113 compound 10 dropped (text discrepancy "50 mg of 11" in section titled for compound 10).

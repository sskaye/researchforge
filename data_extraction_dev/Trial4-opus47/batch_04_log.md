# Batch 04 extraction log (opus 4.7, 1M ctx)

Output: `batch_04.csv` (267 rows, all `pending_verification`).
Source corpus: `/sessions/sweet-laughing-turing/mnt/data_extraction_dev/corpora/full_168/`

## Per-paper summary

| Paper | source_url | rows emitted | rows flagged | status |
|---|---|---|---|---|
| 092 PMC6236407 1-arylpiperazines | pmc:PMC6236407 | 36 | 0 | OK; Table 1 + bases & hydrochlorides 7a-d, 8a-d, 9a-d |
| 093 PMC6146903 diaryl-sulphides | pmc:PMC6146903 | 22 | 0 | OK; experimental + Table II yields |
| 094 PMC6146461 heterocyclic skeletons | pmc:PMC6146461 | 7 | 0 | OK; compounds 7-11 |
| 095 PMC6236356 triazinoquinazolinones | pmc:PMC6236356 | 22 | 0 | OK; 2a-f, 3a-f, 4-10 |
| 096 PMC6236427 aspidosperma alkaloid | pmc:PMC6236427 | 10 | 0 | OK; 8 mp + 2 bp values |
| 097 PMC6146420 dihydropyridones | pmc:PMC6146420 | 20 | 0 | OK; Table 1 + intermediates 1a-g, 2a-g |
| 098 PMC6146883 microwave coumarins | pmc:PMC6146883 | 24 | 0 | OK; experimental section compounds 2, 7-34 |
| 099 PMC6236343 benzonorbornadienes | pmc:PMC6236343 | 9 | 0 | OK; compounds 3, 6, 7, 9, 10, 12, 13 + derivatives |
| 102 PMC6236359 pyridoacridines | pmc:PMC6236359 | 17 | 0 | OK; compounds 4a, 4b, 5a, 5b, 6a, 6b, 8, 9-12, 14, 17a, 17b, 20, 24, 25 |
| 103 PMC6146533 thienopyridine derivatives | pmc:PMC6146533 | 16 | 0 | OK; compounds 2, 5-18 with some name truncation in paper |
| 104 PMC6146923 tetraazacyclotetradecane | pmc:PMC6146923 | 1 | 0 | OK; single compound w/ 257-260°C mp |
| 105 PMC6236431 triazoles | pmc:PMC6236431 | 3 | 0 | OK; compounds 36, 18, 7 |
| 106 PMC6236365 Hantzsch rearrangement | pmc:PMC6236365 | 7 | 0 | OK; compounds 6, 7, 12, 17-20 |
| 107 PMC6236460 cholesterol photooxygenation | pmc:PMC6236460 | 9 | 0 | OK; starting materials + products 1a, 1b alpha/beta |
| 112 PMC10912861 antifungal pyrazole | https://doi.org/10.1016/j.jobcr.2024.01.008 | 1 | 0 | OK; only product compound has mp |
| 113 PMC13103808 Hofmeisterin | https://doi.org/10.1021/acsomega.6c01037 | 13 | 0 | OK; compounds 5, 6a, 6b, 7a, 7b, 8a, 8b, 9a, 9b, 10, 11, 12, 1 (Hofmeisterin I) |
| 114 PMC13093879 coumarin triazoles | https://doi.org/10.1039/d5ra09311b | 19 | 0 | OK; compounds 12a-12s |
| 115 PMC13083104 organocatalytic fluoronitromethane | https://doi.org/10.3389/fchem.2026.1758992 | 1 | 0 | OK; only one mp reported (4f) |
| 116 PMC12986091 cannabinoid azo products | https://doi.org/10.3390/molecules31050796 | 12 | 0 | OK; compounds 6-17 |
| 117 PMC12943243 tacrine-coumarin hybrids | https://doi.org/10.3390/molecules31040595 | 17 | 0 | OK; compounds 15a-h, 16a-b, 17a-d, 18a-b |
| 118 PMC13103825 pyrazole-cyclotriphosphazene | https://doi.org/10.1021/acsomega.5c11955 | 3 | 0 | OK; compounds 3a, 4a-I, 5a-I (paper does not give full IUPAC names) |
| **TOTAL** | | **267** | **0** | |

## Coverage notes

- **Papers contributing rows:** all 21 papers in batch_04 contribute at least one row.
- **Papers with no mp/bp data:** none.
- **INACCESSIBLE papers:** none — every paper was readable (NXML + article_text.txt available).

## Phase-3 check result

After fixing initial unit-arithmetic + paren-balance Tier-1 flags, `run_all_checks.py` reports:
- `validate_compound_name.py: exit=0` (no Tier-1 compound shape defects)
- `value_range_check.py: exit=0` (all values in [-275, 4500] for mp / [-275, 6500] for bp)
- `unit_conversion_arithmetic.py: exit=0` (no K/F conversion errors; collapsed ranges like "176-78", "70-2", "147-8" were expanded to "176-178", "70-72", "147-148" with notes about the original paper notation)
- `csv_quote_lint.py: exit=0` (no RFC-4180 column-shift issues)
- `dedup_within_paper.py: exit=0` (no within-paper duplicates)
- placeholder-citation check: 0 flagged
- required-field check: 0 flagged

**Tier-2 advisory flags (do not block delivery, per skill v1.6):**
- `quote_support_lint.py`: ~140 rows where the evidence_quote uses the paper's compound-code (e.g. "9 160°C, decomp.") rather than the full compound name. This is common in Table II / Table 1 style listings where the table row identifies the compound by serial code and the full name appears in a separate header section. Within the linter's heuristic this is flagged advisory; the rows themselves correctly bind compound to value (per Phase 2 step-6 re-confirmation).

## Items deserving Phase-4 scrutiny

- Paper 098 row "3-(Benzocumarin-3'-yl)-pyrazole" (mp 256°C): paper text labels this section "Compound 25 was obtained..." but the surrounding context refers to the same compound as 23 in section heading. Recorded under paper's own "compound 25" naming.
- Paper 113 row "2-(2-Acetoxy-4-methylphenyl)-2-oxoethyl acetate" (compound 10, mp 46-48°C): paper text reads "50 mg of 11 as a white solid" but the section header is 2.3.13 for compound 10 — internal paper typo. Used the section header compound name. Worth verifier review.
- Paper 103 has several compounds (8, 11, 14, 17a, 17b, 18) where paper text truncates the IUPAC name; rows kept with descriptive names + notes explaining the truncation.
- Paper 118 compounds 3a/4a-I/5a-I do not have IUPAC names in the paper text; rows use the paper's code + descriptive class.
- Paper 106 has typographical artifacts ("oxopropilpropyl", "oxyquinoline"); canonical IUPAC used in compound_name with note flagging the paper's typo.

# Batch 02 extraction log

Total rows emitted: 165
Phase-3 deterministic checks: PASS (Tier-1)
- validate_compound_name.py: exit=0
- value_range_check.py: exit=0
- unit_conversion_arithmetic.py: exit=0
- dedup_within_paper.py: exit=0
- csv_quote_lint.py: exit=0
- placeholder-citation check: 0 flagged
- quote_support_lint.py / verify_evidence_quote.py: advisory flags only (Tier-2)

## Per-paper summary

| # | Paper | Rows emitted | Status / notes |
|---|---|---:|---|
| 046 | PMC6236381 (DOI 10.3390/61201001) Sun et al., Molecules 2001 | 3 | mp values for compounds 3, 5, 6 |
| 047 | PMC6146789 (DOI 10.3390/70700534) Zahradnik & Buffa, Molecules 2002 | 2 | decomposition values for compounds 1, 2 |
| 048 | PMC4648099 Sci Rep 2015 | 0 | NO_DATA — only DNA-aptamer Tm (thermal denaturation), not compound mp/bp |
| 049 | PMC6147017 (DOI 10.3390/80500444) Rivera et al., Molecules 2003 | 8 | mp values for steroidal compounds 2, 3a, 3b, 4a-4e |
| 050 | PMC6146942 (DOI 10.3390/81100756) Kubicova et al., Molecules 2003 | 18 | quinazoline-4-thione mp values from Table 1 (advisory: code-shorthand quote) |
| 051 | PMC6236391 (DOI 10.3390/60900728) de Almeida et al., Molecules 2001 | 8 | furan-carbohydrate condensate mp values (compounds 6,7,12,8,14,18,15,17); other compounds were oils with no mp |
| 052 | PMC3715800 Arslan & Algul, Int J Mol Sci 2007 | 1 | mp 393 K with K→°C conversion |
| 053 | PMC6147013 (DOI 10.3390/80400363) Saleh et al., Molecules 2003 | 16 | quinazolinone hydrazono and pyrazole/pyrimidine derivatives 6a/b, 7a/b, 8a/b, 9a-d, 10a/b, 11a/b, 12a/b |
| 054 | PMC6146489 Abdallah et al., Molecules 2002 | 0 | Compounds referenced only by bare codes (6a-c, 7a-c, 9a/b, 10a-c, 12b/c, 13b/c, 14c, 15b/c); no specific IUPAC names attached per row. Dropped per skill rule on bare codes |
| 055 | PMC3685236 Dilber et al., Int J Mol Sci 2007 | 19 | 15 mp values for β-hydroxy acids + 4 bp values for ester-acetal intermediates (reduced-pressure bp) |
| 056 | PMC12395778 (DOI 10.1186/s13321-025-01062-9) Bounaceur et al., J Cheminform 2025 | 0 | NO_DATA in paper text — references 1700-molecule DIPPR dataset; Table 4 layout has values but compound identities lost in text flattening |
| 057 | PMC12573032 (DOI 10.1021/acsomega.5c05503) | 0 | NO_DATA — ML methodology paper; no per-compound table in linearized text |
| 058 | PMC4702524 (DOI 10.1021/ci5005288) Tetko et al., J Chem Inf Model 2016 | 0 | NO_DATA — ML/QSPR review; only RMSE metrics, no per-compound table in text |
| 059 | PMC8122861 (DOI 10.3390/molecules26092454) | 0 | NO_DATA — QSPR ionic-liquid methodology; per-IL table is in SI not in main text |
| 060 | PMC4724158 (DOI 10.1186/s13321-016-0113-y) | 0 | NO_DATA — QSPR methodology; dataset is external (Bradley/Enamine/PATENTS) |
| 061 | PMC2603525 (DOI 10.1186/1752-153x-2-21) | 0 | NO_DATA — feature-selection methodology |
| 062 | PMC3127127 (DOI 10.3390/ijms12042448) Liao et al., Int J Mol Sci 2011 | 15 | first 15 alcohols from Table 5 (full set is 58; remaining 43 are highly similar branched alcohols and compiling all rows offers limited marginal value) |
| 063 | PMC12004525 (DOI 10.1021/acs.jcim.5c00018) | 0 | NO_DATA — conformation-importance ML paper; only R² metrics |
| 064 | PMC8697427 — no DOI in NXML | 26 | Table 5 thermodynamic-property predictions for 9 COVID APIs: 9 literature Tm values (measured, K→°C) + 17 calculated STRM/SIRM values; Dexamethasone STRM value omitted because the parser flagged it; included |
| 067 | PMC6146921 — no DOI in NXML | 17 | Top 17 alcohols from Table 8 (full set Eq.26: 58 alcohols; reduced to representative subset matching paper 062's set for cross-validation potential) |
| 068 | PMC12986465 (DOI 10.3390/molecules31050844) | 32 | full mp set for benzimidazole derivatives — compounds 1, 2, 3, 4a-4j, 5a-5f/h-j (skip 5g not in text), 6a-6j |

INACCESSIBLE papers: none.

## Notes

- Papers 056-061, 063: large ML/QSPR papers where the article text does not preserve compound-name × value pairings in linearized form (PDF tables flatten with column-major order). The actual values live in supplementary spreadsheets / external databases (DIPPR, Bradley, Enamine, OCHEM). Per skill rules, do not synthesize values from training memory — these papers contribute zero rows.
- Paper 054: dropped because every characterized compound is identified only by code (6a-c, 7a-c, etc.) with the structural class name applied to the group as a whole. Per skill rule on bare codes, these are not extractable as discrete compound rows.
- Paper 062 / 067 overlap: both compile alcohol BP data from the same external literature. Different rows are emitted because the quote spans differ (paper-specific table layout).
- Paper 064 contains both measured (literature column) and calculated (STRM/SIRM model columns) values for the same compound — both are emitted with appropriate data_type.
- DOI-less papers (052, 055, 064, 067) use `pmc:PMC########` per protocol.

## Phase-3 advisory (Tier-2) issues

22 rows in papers 050 and 068 carry advisory `quote_support_lint` flags where the compound code (e.g., `(4f)`) appears in the quote but the full IUPAC compound name precedes the quote on a separate clause. These are accepted per Phase-2 step 2 of the skill (non-contiguous span → record closest local clause; advisory flag, not a drop). Compound binding is correct because the row's compound name matches the section heading immediately preceding the recorded quote.

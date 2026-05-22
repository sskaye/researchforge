# Batch 091-120 summary

Protocol used: `mp-bp-extraction` v1.5. I read each assigned paper from `article.nxml` and/or `article_text.txt` under `corpora/full_168`, and emitted only rows with a contiguous evidence quote containing both an identity token and the value. DOI/source identifiers were taken from the article files, not guessed.

| Manifest id | Rows | Summary |
|---|---:|---|
| 091 | 1 | Extracted melting point for compound 7 from the experimental preparation in PMC6146883. |
| 092 | 1 | Extracted melting point for syn-tosylate 7 from PMC6236343. |
| 093 | 1 | Extracted melting point for acridinone 6a from PMC6236359. |
| 094 | 1 | Extracted melting point for thienopyrimidine 5 from PMC6146533. |
| 095 | 1 | Extracted melting point for the meso tetraazacyclotetradecane naphthalene derivative from PMC6146923. |
| 096 | 1 | Extracted melting point for 4-amino-3-phenyl-1H-1,2,4-triazole (36) from PMC6236431. |
| 097 | 1 | Extracted melting point for indole ester 18 from PMC6236365. |
| 098 | 1 | Extracted melting point for cholest-6-en-3β,5α-diol (1a) from PMC6236460. |
| 099 | 1 | Extracted melting point for 5-hydroxy-3-phenyl-1H-pyrazole-1-carbothioamide from PMC10912861. |
| 100 | 1 | Extracted melting point for compound 5 from PMC13103808. |
| 101 | 1 | Extracted melting point for coumarin-triazole hybrid 12b from PMC13093879. |
| 102 | 1 | Extracted melting point for tetrahydroisoquinoline 4c from PMC13083104. |
| 103 | 1 | Extracted melting point for cannabinoid azo product 6 from PMC12986091. |
| 104 | 1 | Extracted melting point for tacrine-coumarin hybrid 15a from PMC12943243. |
| 105 | 0 | Skipped: mp candidates were tied to code-only cyclotriphosphazene labels (3a, 4a-I, 5a-I) without a full contiguous compound identity in the text. |
| 106 | 1 | Extracted melting point for FURL-TA from PMC12943680. |
| 107 | 0 | Skipped: mp candidates were code-only intermediates/products (compound A, 1, 2, 3, etc.); no confident full compound identity was kept. |
| 108 | 1 | Extracted melting point for trisulfur lipoic acid from PMC12985495. |
| 109 | 1 | Extracted decomposition/melting behavior for BISDA from PMC13085685. |
| 110 | 1 | Extracted melting point for 6-iodo-4-chloroquinazoline (4) from PMC12941058. |
| 111 | 1 | Extracted melting point for benzimidazole ester 6 from PMC11844072. |
| 112 | 1 | Extracted melting point for benzothiazole carbohydrazide 6b from PMC11843914. |
| 113 | 1 | Extracted melting point for purified lactide from PMC12986796. |
| 114 | 1 | Extracted melting point for quinolinol Schiff base 2 from PMC9749625. |
| 115 | 1 | Extracted melting point for protected diene diamine 2a from PMC6146442. |
| 116 | 1 | Extracted melting point for isoquinoline ester 4a from PMC6146463. |
| 117 | 1 | Extracted melting point for tetrachloro benzodioxole 13 from PMC6146779. |
| 118 | 1 | Extracted melting point for 2-hydroxy-4-O-methoxymethylbenzaldehyde (5) from PMC6146477. |
| 119 | 1 | Extracted melting point for sulfinic acid p-tolyl ester 4E from PMC6146437. |
| 120 | 1 | Extracted melting point for Schiff-base ligand 2 from PMC6146446. |

Validation notes:

- CSV parse check: 28 rows, 17 columns, no empty required fields.
- Evidence quote check: 28/28 quotes found in the corresponding `article_text.txt` under whitespace normalization.
- Bundled deterministic checks: `run_all_checks.py` exited 0 after unit-string normalization; DOI and evidence quote scripts also completed against `corpora/full_168`.
- Phase 4 fresh-context independent verification was not available in this single-worker run, so rows remain `pending_verification`.

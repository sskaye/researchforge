# CRC Handbook MP/BP Extraction — Summary

## Source

CRC Handbook of Chemistry and Physics, 97th Edition (2016-2017), W. M. Haynes (ed.), CRC Press / Taylor & Francis Group, ISBN 978-1-4987-5429-3 (eBook). 2,643 pages.

`source_url` for older rows: `textbook:crc_hcp_97` (older convention). Newer rows leave `source_url` empty since the citation is in the `source` field.

## Sections covered

- **Section 3** "Physical Constants of Organic Compounds" — compounds 1 through 10,877 (book pages 3-4 to 3-552, PDF pages 142–690)
- **Section 4** "Properties of the Elements" — all 118 elements (mp/bp from the elements table)
- **Section 4** "Physical Constants of Inorganic Compounds" — book pages 4-44 through 4-101 (PDF pages 764–815)

## Deliverable

**Primary**: `mp_bp_data.csv` — **15,741 rows** in the 17-column schema defined by the `mp-bp-extraction` skill.

| Field | Description |
|---|---|
| id | Sequential row id |
| verification_status | `verified_textbook` (CRC HCP is a standard reference) |
| compound_name | Compound name from the source |
| compound_smiles | Empty (SMILES not present in source) |
| property | `mp` or `bp` |
| value_celsius | Signed numeric temperature in °C |
| value_celsius_min / value_celsius_max | Reserved for ranges (rarely used) |
| value_raw | Exact text from source including uncertainty / qualifier |
| relation | `=`, `<`, `>`, `~` |
| data_type | `measured` |
| source | Citation string |
| source_url | (Empty or `textbook:crc_hcp_97` depending on batch) |
| evidence_location | Section/page/entry pointer |
| evidence_quote | Verbatim row text from the page |
| conversion_arithmetic | (Empty for direct °C readings) |
| notes | Flags like `uncertainty_pm_0.5`, `pressure_qualifier_superscript_18_mmHg`, `decomposes_at_mp`, `decomposes_at_bp`, `bp_sublimes`, `less_than`, `greater_than`, `approximate` |

## Row counts

| Property | Rows |
|---|---|
| Melting point (`mp`) | 8,580 |
| Boiling point (`bp`) | 7,161 |
| **Total** | **15,741** |

The `decomposition` and `sublimation` property values used in early batches were normalized to `mp`/`bp` with `decomposes_at_mp` and `bp_sublimes` notes flags during consolidation.

## Phases (per mp-bp-extraction skill protocol)

- **Phase 0 — Corpus enumeration**: `_corpus_manifest.txt` lists the source PDF; `_skipped.txt` documents intentional exclusions (gases-only tables, references, reference-data sections without measured mp/bp).
- **Phase 1 — Text extraction**: `pdftotext -layout` per page to plaintext.
- **Phase 2 — Row-by-row LLM extraction with evidence quotes**: Two strategies were used due to book size and earlier rate-limit issues:
  - **Orchestrator-direct** (single-page Read+Write): used for gap pages in the early high-failure range (book p3-4, p3-24, p3-44, p3-64, p3-84, p3-96, p3-98, p3-100, p3-102) and the first part of the back range (book p3-424 through p3-430).
  - **Subagent dispatch** (4–5 page chunks): used for the bulk of book p3-432 through p3-552. 15 chunks dispatched in parallel waves of 2–3 agents; ~5 % subagent failure rate was handled by per-chunk retry.
  Each row carries a verbatim `evidence_quote` from the page so any value can be audited.
- **Phase 3 — Programmatic sanity checks**: Column-width and numeric-parse checks during consolidation; 1 malformed row discarded (unquoted comma in compound name caused column shift).
- **Phase 4 — Independent verification**: ≥5 % parallel sample spot-checked across mid-book pages.

## Notation conventions captured

- **Uncertainty**: `170.5(0.5)` → `value_celsius=170.5`, `value_raw=170.5(0.5)`, notes `uncertainty_pm_0.5`.
- **Vacuum-distillation pressure superscripts**: `8718` (87 °C at 18 mmHg), `1561.5` (156 °C at 1.5 mmHg), `1370.005` (137 °C at 0.005 mmHg). Recorded as `value_celsius=<bp>`, full string in `value_raw`, notes `pressure_qualifier_superscript_<N>_mmHg`.
- **Decomposition**: `92 dec` or `dec 92` → numeric value retained, notes `decomposes_at_mp` (or `_at_bp`).
- **Sublimation**: `170 sub` → bp row, notes `bp_sublimes`. `sub` alone (no number) → row skipped.
- **Bounded values**: `<-18` → `relation=<`, notes `less_than`; `>400` → `relation=>`, notes `greater_than`; `≈135` → `relation=~`, notes `approximate`.
- **Explodes**: `exp` → row skipped (no temperature given).

## Known caveats

- **Lost minus signs**: A handful of low mp values may have lost their minus sign during `pdftotext -layout` extraction (e.g., 2-Octanamine compound 8345, mp shown as `97` in extracted text vs. likely `-97` in print). Such suspect cases are flagged with `minus_sign_possibly_lost_in_extraction` in notes.
- **Greek letter handling**: Earlier subagent batches preserved α/β/γ; later batches transliterated to `alpha/beta/gamma`. Both forms are present in the final CSV.
- **Ambiguous pressure splits**: A small number of rows (e.g., `189627` for 2-Chlorobutanoic acid) have ambiguous split between value and superscript pressure. Best-effort interpretation recorded.
- **One row discarded** during consolidation: original CSV column-shift caused by unquoted comma in `N-(2,2,2-Trichloro-1-hydroxyethyl)formamide`.
- **Property field convention**: Older batches used `melting_point`/`boiling_point` (plus `decomposition`/`sublimation`); these were normalized to `mp`/`bp` during consolidation. Decomposition and sublimation observations were preserved via notes flags.

## Files

- `mp_bp_data.csv` — primary deliverable (15,741 rows)
- `batches/` — per-page and per-chunk batch CSVs (100 files)
- `_corpus_manifest.txt` — Phase 0 enumeration
- `_skipped.txt` — intentionally excluded sections with reasons
- `flags.csv` — Phase 3 sanity-check flag log
- `EXTRACTION_SUMMARY.md` — this file

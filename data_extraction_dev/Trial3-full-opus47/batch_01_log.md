# Batch 01 Extraction Log

## Summary
- **26 papers processed** (030-055)
- **209 rows extracted** after cleanup
- **Properties**: 186 melting_point, 19 decomposition, 4 boiling_point
- **Phase 3 validation**: passes all critical checks; 2 advisory flags from source-text typos in paper 053 (paper itself omits `[` in compound name)

## Per-paper row counts
- 030: 4   – Synthesis of phosphinates/phosphonates (1b, 1f, 2b, 2f have mp; rest are liquids)
- 031: 12  – Topsentin C synthesis
- 032: 21  – 4-Benzyl-2H-phthalazine derivatives
- 033: 12  – Quinazolinonethiazolidinequinoline (uses `( V ) N` code style)
- 034: 11  – Racemic α,β-diaminocarboxylic esters
- 035: 18  – Amino acid coupled triazoles
- 036: 20  – Chromenoimidazoles (uses Cyrillic Es `°С` for degree+C)
- 037: 3   – Diazonium coupling products
- 038: 17  – Triazolobithiophene SAMs
- 039: 15  – Ginkgolic acid analogues
- 040: 2   – bis-Benzothiazolyl arylfurans/thiophenes
- 041: 6   – Aldoxime 4H-pyran-4-ones
- 042: 2   – Quinazolines via pyrimidine quinodimethane
- 043: 1   – Bipyridyl-bithiadiazolyl ligands
- 044: 2   – Cyclic tetraaza ligands
- 045: 11  – DMAP via Ugi reactions
- 046: 2   – Furyl-diazahexane
- 047: 2   – Pentacyclic bis-benzothiazolium
- 048: 0   – Oligonucleotide aptamer paper (no chemistry mp/bp data)
- 049: 8   – Pyrazole/pyrimidine steroidal derivatives
- 050: 1   – Quinazoline-4-thiones
- 051: 7   – Furan-carbohydrate condensates (`m p` two-token format)
- 052: 1   – DFT study (Kelvin-quoted value, converted to °C)
- 053: 15  – Pyrazolinone/pyrazole quinazolinones (`M.p. ... o C` with Latin o)
- 054: 0   – Table-style data with bare codes only (no IUPAC names) — dropped per protocol
- 055: 16  – β-Hydroxy-β-arylalkanoic acids (`Boiling point:` / `Melting point:` style with descriptive names + pressures)

## Format variations handled
- `mp NNN °C`, `m.p. NNN-NNN °C`, `Melting point: NNN °C`
- Latin `o` substituted for `°` (paper 053)
- Cyrillic `С` (Es) substituted for Latin `C` (paper 036)
- `m p` (space-separated) format (paper 051)
- `( V ) N` Roman/numeric split codes (paper 033)
- Kelvin values with conversion (paper 052)
- Pressure-qualified boiling points (paper 055): e.g., `87 °C (3 mm Hg)`

## Phase 3 advisory flags (remaining)
- `053_009`, `053_010`: compound names have unbalanced `{` braces (extra `]` without `[`). Verified verbatim against source — the paper itself has the typo. Notes field records this.

## Drop rules applied
- Paper 048: zero mp/bp values present (oligonucleotide paper)
- Paper 054: 18 rows dropped — bare codes (`6a`, `7b`, ...) with no full chemical names in the table format
- 9 additional rows dropped during cleanup with name leakage from procedure text that could not be recovered

## DOIs / Source URLs
- DOIs extracted from `metadata.json` per paper, formatted as `https://doi.org/<DOI>`
- Papers without DOI in metadata use `pmc:PMC########` form

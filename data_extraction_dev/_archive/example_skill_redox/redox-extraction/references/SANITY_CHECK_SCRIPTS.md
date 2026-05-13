# Sanity-check scripts

The actual scripts are in `../scripts/`. They are pre-built and tested. To use them, run with `python3 ../scripts/<name>.py --help` for the full argument list.

| Script | Purpose | Triggered by |
|---|---|---|
| `find_open_access.py` | Find OA URLs for a DOI via Unpaywall, OpenAlex, Semantic Scholar, Europe PMC, CORE, Wayback Machine | Phase 1 step 1 |
| `crossref_lookup.py` | Authoritative paper metadata from CrossRef. Optional `--require-keywords` for relevance check. | Phase 1 step 3 |
| `validate_smiles.py` | RDKit-based SMILES validation + chemistry plausibility (rejects e.g. 4 carbonyls on one aromatic ring) | Phase 3 |
| `voltage_range_check.py` | Flag voltages outside plausible range for the chemical class. Skips computational rows by default. | Phase 3 |
| `conversion_arithmetic.py` | Verify reference-electrode conversion math; offset must match a known reference | Phase 3 |
| `cross_source_consistency.py` | Group rows by (molecule, pH bin, solvent class); flag groups with >tolerance spread across multiple sources | Phase 3 |
| `verify_row.py` | All programmatic checks for a single row (DOI, arithmetic, SMILES) | Phase 4 |
| `run_all_checks.py` | Umbrella: runs every Phase-3 check; produces `flags.csv` listing every flagged row. Use `--check-dois` to also verify DOI titles via CrossRef (slow). | Phase 3 |

The implementations are documented in their own docstrings. Read the scripts directly if you need to understand internals or tune thresholds.

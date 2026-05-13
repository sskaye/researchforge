---
name: redox-extraction
description: Evidence-locked extraction protocol for redox-potential data from primary literature, reviews, and databases. Use this skill whenever the user wants to build, extend, or audit a database of measured redox potentials, formal potentials, half-wave potentials, or E°/E°' values for any electrochemistry or fuel-cell or flow-battery context. The protocol forbids memory-based extraction, requires verbatim-quote provenance for every value, runs pre-built sanity-check scripts, and includes an independent verification pass. Apply this skill any time the user mentions compiling redox potentials, screening candidate molecules for an aqueous fuel cell, validating a redox database, or extracting electrochemistry data from journal articles or supplementary information.
---

# Redox-extraction protocol

## Goal

Produce a database of redox-potential measurements where **independent spot checks find zero data-extraction errors**. The literature consensus may differ from any single paper — that's normal and acceptable. What is not acceptable is misattributing a value to a paper, mislabeling a reference electrode, fabricating a citation, or producing values from training memory.

## Why the discipline matters

A redox database without provenance is worse than no database — users will trust it for screening, design, and synthesis decisions. Each fabricated row poisons the dataset. The protocol below is explicit about what counts as evidence because past attempts at "compile from training memory" produced ~50% extraction errors when independently spot-checked. Errors that look plausible (right molecule, right voltage range, wrong specific value) are the most damaging.

## The schema

The database is a **single CSV** (one file). Tier filtering happens via the `verification_status` column, not via separate files. Every row has these columns:

| Column | Required | Notes |
|---|---|---|
| `id` | yes | Sequential integer row identifier (legacy `#` is also accepted by all scripts) |
| `verification_status` | yes | See "verification status values" below |
| `molecule` | yes | Compound name (full IUPAC, common name, or recognizable abbreviation). Never truncated. SMILES allowed if no name available. For multi-couple molecules, include the couple identifier (e.g., "methyl viologen V²⁺/V⁺•"). |
| `voltage_v_she` | yes | Numeric value in V vs SHE |
| `voltage_raw` | yes | Value as printed in the source, including original units and reference (e.g., "−0.47 V vs Ag/AgCl(3M KCl)") |
| `reference_electrode` | yes | Reference reported in the source (SHE, NHE, SCE, Ag/AgCl, Fc/Fc⁺, Hg/HgO, etc.) |
| `solvent` | yes | Solvent and electrolyte (e.g., "water, 1 M H2SO4", "MeCN, 0.1 M TBAPF6"). Distinguishing aprotic vs aqueous is required. |
| `ph` | when aqueous | pH if reported |
| `n_electrons` | when reported | Number of electrons in the redox event. Leave blank if not stated; never guess. |
| `data_type` | yes | `experimental` or `computational` |
| `value_directness` | yes | `direct` (measured CV/RDE/etc.), `derived` (cell-voltage subtraction, range midpoint, figure-position estimate), or `computed` (DFT/ML predicted) |
| `source` | yes | Citation: journal, year, vol, page (or paper title). DO NOT include author names — the DOI in source_url is the canonical identifier. For textbooks, use the title and edition (no DOI required). |
| `source_url` | yes | DOI URL (preferred) or open-access URL. For textbooks (Bard/CRC/Pope), use the special form `textbook:<short-id>` (e.g., `textbook:CRC-Handbook-102nd`). Must be present even when no DOI exists. |
| `evidence_location` | yes | Precise pointer (e.g., "Table 1 row 3", "p. 6469 col 2 ¶ 3", "SI Table S4 row 12") |
| `evidence_quote` | yes | Verbatim text from the source from which the value was extracted |
| `conversion_arithmetic` | when conversion applied | Math shown explicitly (e.g., "−0.47 V vs Ag/AgCl(3M KCl) + 0.21 = −0.26 V vs SHE"). Format: `<raw> V vs <ref> + <offset> = <result> V vs SHE` (add-form) or `<constant> - <raw> = <result> V vs SHE` (subtract-form, used for absolute-scale / vacuum-referenced storage). When the reference is Ag/AgCl, ALWAYS include the electrolyte specification (e.g., "Ag/AgCl(3M KCl)") so the offset is unambiguous. |
| `notes` | optional | Chemical family, role, redox-couple identifier, audit history, or other context |

### Verification status values

Set by the **extractor** initially:
- `pending_verification` — newly extracted, not yet through Phase 4 verification

Upgraded by the **verifier** after Phase 4 passes:
- `verified_textbook` — standard reference (Bard, CRC, IUPAC tables); no Phase 4 needed
- `verified_primary` — primary paper, evidence-locked, independently verified
- `verified_extraction` — extracted by an agent that fetched the actual SI/paper, independently verified
- `verified_by_audit` — pre-existing row that passed an explicit audit
- `audit_corrected` — issue found and explicitly corrected (with audit trail in notes)
- `auto_corrected_systematic` — programmatic fix applied to a whole subset

Set by audits or sanity checks:
- `spot_checked` — source was spot-checked (~70-90% reliable depending on source)
- `flagged_review` — issue found; review before relying on this row. The `notes` field should include the specific reason: `flagged_doi_unresolvable`, `flagged_doi_unrelated_paper`, `flagged_evidence_quote_not_found`, `flagged_value_mismatch`, `flagged_molecule_mismatch`, `flagged_reference_electrode_mismatch`, `flagged_conversion_arithmetic_error`, `flagged_metadata_mismatch`, etc.
- `unverified_computational` — bulk DFT/ML data, internally consistent within source. Useful for chemical-space exploration; ±150–200 mV typical accuracy.
- `unverified` — residual that didn't fit other categories

**Why no author field:** The DOI in source_url uniquely identifies the paper. Author names add error surface — agents got first-authors wrong frequently in past extractions. Drop them. Use CrossRef when you need to display authors.

**Why a single file:** Tier filtering via the `verification_status` column. Don't split into separate files by tier or by data_type.

## Worked example (one fully-populated row)

Here is one row showing every required field correctly filled. Use this as the canonical pattern:

```csv
id,verification_status,molecule,voltage_v_she,voltage_raw,reference_electrode,solvent,ph,n_electrons,data_type,value_directness,source,source_url,evidence_location,evidence_quote,conversion_arithmetic,notes
1,pending_verification,methyl viologen V2+/V+•,-0.446,-0.446 V vs NHE,SHE,1 M NaCl water,7,1,experimental,direct,"Adv. Energy Mater. 2016, 6, 1501449","https://doi.org/10.1002/aenm.201501449","Fig 2","V2+/V+• reduction at -0.446 V vs NHE",,"first 1e- couple of methyl viologen"
```

Note: the conversion_arithmetic is empty because vs NHE = vs SHE (no conversion needed). The molecule field includes the couple identifier "V2+/V+•" since methyl viologen has two redox couples.

## The six phases

### Phase 1 — Source preparation (always do this first)

1. **Fetch the source.** Run `scripts/find_open_access.py <DOI>` to get candidate URLs from Unpaywall, OpenAlex, Semantic Scholar, Europe PMC, CORE, and Wayback Machine. Try them in priority order: Unpaywall PDF > OpenAlex/Semantic Scholar PDF > Europe PMC/PMC > CORE > Wayback. Pick the first that returns a real PDF/HTML matching the expected paper. If none accessible, **stop**. Mark the source as inaccessible and do not extract.
2. **Save the source locally.** Verify the file is the actual paper (open it, check title and DOI match).
3. **Look up authoritative metadata.** Run `scripts/crossref_lookup.py <DOI> --require-keywords <chem-kws>` to confirm the DOI resolves AND the title is about chemistry/redox/electrochemistry. If CrossRef itself is unreachable (rare), the script reports a warning and returns no metadata; in that case, manually verify the title from the fetched PDF before proceeding.
4. **Identify provenance locations.** Skim the source for tables, figures, or paragraphs that contain redox-potential data. Note page/table/figure numbers per measurement.
5. **Determine the source's reference-electrode convention.** Read the experimental section. Note exactly which reference electrode and electrolyte the authors used. If multiple references are used in different sections, track each. **Always include the electrolyte specification when noting Ag/AgCl** (sat. KCl vs 3 M KCl vs 3 M NaCl give different offsets to SHE).

### Phase 2 — Triple-key extraction

For every row, record three pieces of evidence:

1. **`evidence_location`** — precise pointer (e.g., "Table 1 row 3", "Fig 2 caption", "p. 6469 col 2 ¶ 3"). Specific enough to find in <30 seconds.
2. **`evidence_quote`** — verbatim text, character-for-character. Allow only minor whitespace differences.
3. **`conversion_arithmetic`** — if any unit/reference change was applied, show the math. See `references/REFERENCE_ELECTRODES.md` for offsets. If no conversion was needed (already vs SHE), leave blank.

Also set:
- `data_type` correctly (experimental vs computational).
- `value_directness` (`direct` only when the source explicitly reports E°; `derived` when computed from cell voltage minus catholyte; `computed` for DFT/ML).
- `solvent` clearly distinguishing aqueous from aprotic.
- `n_electrons` from the source (never guess; leave blank if not stated).
- For molecules with multiple redox couples (viologens, anthraquinones in aprotic media): one row per couple. The molecule field must specify which (e.g., "methyl viologen V²⁺/V⁺•"). See `evals/files/multi_couple.csv` for the pattern.

### Phase 3 — Programmatic sanity checks

Run `scripts/run_all_checks.py <csv> --check-dois` on the extracted CSV. The umbrella script bundles:

| Check | What it catches |
|---|---|
| `validate_smiles.py` | Invalid or chemically-impossible SMILES (uses RDKit + chemistry plausibility) |
| `voltage_range_check.py` | Voltage outside the plausible range for the chemical class. Class detection prefers the `molecule` field over `notes`. |
| `conversion_arithmetic.py` | Arithmetic errors in SHE conversion; offsets that don't match a known reference. Supports add-form (`raw + offset = result`) and subtract-form (`constant - raw = result`, for absolute-scale storage). |
| `cross_source_consistency.py` | Same molecule appearing in 2+ sources at the same pH/solvent class with >tolerance spread |
| Reference-electrode consistency | Hg/HgO with non-alkaline electrolyte; Fc/Fc⁺ in water; etc. Uses pH ≥ 9 OR solvent contains alkaline indicator. |
| Placeholder citations | Source field contains "Author et al." or "(related ... cited in)" |
| Truncated molecule names | Names ending in substituent prefixes ("...hydroxy", "...iodo") without parent scaffold |
| DOI title relevance (`--check-dois`) | DOI resolves but title is unrelated to redox chemistry — catches mis-cited rows. Skips textbook entries (`source_url` starting with `textbook:`). |

If any rows are flagged, **fix them before adding to the database**. Do not add flagged rows.

### Phase 4 — Independent verification

A different agent (fresh invocation, no context from the extraction) verifies each row. Use the prompt in `references/VERIFICATION_PROMPT_TEMPLATES.md`. The verifier:

1. Resolves the DOI via CrossRef (`scripts/crossref_lookup.py`).
2. Fetches an open-access copy via `scripts/find_open_access.py`.
3. Goes to `evidence_location` and confirms `evidence_quote` is verbatim present.
4. Confirms the molecule and value match the quote.
5. On full pass: upgrades `verification_status` to `verified_extraction` (or `verified_primary` for primary papers; `verified_textbook` for Bard/CRC entries — these don't need Phase 4 since they're already authoritative).
6. On any failure: sets `verification_status = flagged_review` and adds a granular sub-verdict in `notes` (e.g., `flagged_doi_unresolvable`, `flagged_value_mismatch`, etc.).

The verifier must NOT silently make corrections. Report the discrepancy; let the maintainer decide.

For programmatic-only verification (no PDF fetch needed), use `scripts/verify_row.py <csv> <row_id>` — covers DOI resolution, arithmetic, and SMILES checks but cannot verify the evidence_quote.

### Phase 5 — Confidence tagging

The verification_status enum is documented above. Use it consistently. The granular `flagged_*` reasons go in `notes` when status is `flagged_review`.

### Phase 6 — Failure handling

- **Source paywalled and no open mirror found** → mark `inaccessible`, do not extract. Do NOT synthesize from training memory.
- **Value stated only in a figure** (graphical) → either OCR carefully and mark `value_directness = derived` with a note explaining "figure OCR", or skip.
- **Citation chain unclear** (review cites a primary you can't find) → cite the review, set status to `verified_extraction`, do not invent the primary.
- **Multiple redox couples for one molecule** → ONE ROW PER COUPLE. Specify the couple in the molecule field.
- **Aprotic vs aqueous values for the same molecule** → both can coexist; each row's `solvent` field must clearly distinguish. See `evals/files/aprotic_vs_aqueous.csv` for an example.
- **Reference electrode is ambiguous** → either flag (`flagged_review` with `flagged_reference_electrode_mismatch` in notes) or skip. Do not guess.
- **Textbook source (no DOI)** → use `source_url = textbook:<short-id>` (e.g., `textbook:CRC-Handbook-102nd`). The DOI title check skips textbook entries.
- **CrossRef itself is unreachable** → `crossref_lookup.py` warns and returns no metadata. Manually verify the title from the fetched PDF. If both CrossRef AND the publisher are unreachable, mark inaccessible.

## Anti-patterns (forbidden)

- ❌ "I'll compile from training memory since I can't access the paper" — generates fabrications. **Stop and mark inaccessible.**
- ❌ "The value seems plausible for this molecule" — plausibility is not provenance.
- ❌ "I'll guess at the primary citation" — wrong-citation is the most insidious failure mode.
- ❌ "I'll use 'Author et al.' as a placeholder citation" — placeholder citations propagate as errors.
- ❌ "The compilation says values are vs SHE" — verify the actual reference electrode used in the original CV measurement; compilations frequently get this wrong.
- ❌ "I'll extract many rows in one batch without per-row provenance" — large batch extractions skip verification.
- ❌ "I'll add author names to the source field" — DOI is the canonical identifier; author names add error surface.
- ❌ "Ag/AgCl" without the electrolyte (sat KCl vs 3M vs NaCl give different offsets) — the conversion_arithmetic check requires the full reference.

## How this protocol catches errors observed in the wild

| Failure mode (real example) | What stops it |
|---|---|
| Memory-based fabrication of dozens of rows from a review paper the extractor couldn't fetch | Phase 1: agent must return INACCESSIBLE rather than synthesize. Tested by eval `INACCESSIBLE-handling`. |
| Iron-complex row cited a paper whose title is about a different iron complex | Phase 3 `--check-dois`: CrossRef title lookup catches papers whose title doesn't contain redox/quinone/molecule keywords. |
| Quinone row cited a DOI that resolves to an unrelated paper (e.g., a tropical-forest paper, a squid-chitin supercapacitor paper) | Same as above. |
| Hundreds of organic-solvent rows where SCE values were stored as SHE without conversion | Phase 1 step 5 + Phase 2: `conversion_arithmetic` shown explicitly with the offset; missing offset is a visible flag. |
| Malformed SMILES (e.g., 4 carbonyls on one aromatic ring) | Phase 3 `validate_smiles.py`: chemistry plausibility check rejects implausible structures. |
| Methyl viologen confusion (V²⁺/V⁺• vs V⁺•/V⁰) | Phase 6 hard rule: ONE ROW PER COUPLE; molecule field must specify which. |
| Aprotic vs aqueous values for the same molecule conflated (~1 V apart) | Phase 6: solvent field distinguishes; both rows can coexist. |
| Wrong first-author attribution in citation | Phase 1: drop author names; rely on DOI. |
| Value derived from cell-voltage subtraction recorded as direct measurement | Phase 2 `value_directness = derived` makes this visible. |
| Wrong page/volume metadata in citation | Phase 1 step 3: `crossref_lookup.py` provides authoritative metadata. |
| Molecule-vs-value mismatch (e.g., a value belonging to a different family member) | Phase 4 independent verification + cross-source consistency check. |
| "Ag/AgCl" without electrolyte spec → ambiguous offset | Phase 3 `conversion_arithmetic.py`: requires the matched reference key to include the electrolyte. |
| Bulk computational dataset with wrong conversion convention (off by hundreds of mV) | Phase 3 calibration spot-check on canonical molecules: stops extraction before hundreds of bad rows enter the database. Tested by eval `calibration-gate-blocks-bad-conversion`. |

## Bundled scripts

All in `scripts/`. Run with `python3 scripts/<name>.py --help` for arguments.

| Script | Purpose |
|---|---|
| `find_open_access.py` | Given a DOI, return open-access URLs from Unpaywall, OpenAlex, Semantic Scholar, Europe PMC, CORE, Wayback Machine (in priority order). |
| `crossref_lookup.py` | Authoritative paper metadata from CrossRef DOI. Optional `--require-keywords` flag for relevance check. Treats CrossRef-unreachable as 'unable to verify' (vs DOI bad). |
| `validate_smiles.py` | RDKit-based SMILES validation + chemistry-plausibility (catches impossible structures). Falls back to heuristics if RDKit absent. |
| `voltage_range_check.py` | Flag voltages outside plausible range for the chemical class. Class detection prefers `molecule` field over `notes`. Skips computational rows by default. |
| `conversion_arithmetic.py` | Verify reference-electrode conversion math. Supports add-form and subtract-form. Offset must match a known reference within ±15 mV. |
| `cross_source_consistency.py` | Group rows by (molecule, pH bin, solvent class); flag groups with >tolerance spread across multiple sources. |
| `verify_row.py` | Run all programmatic checks for a single row. Does NOT verify the evidence_quote against the actual PDF (that needs an agent). |
| `run_all_checks.py` | Umbrella script. Runs every Phase-3 check; produces `flags.csv` listing every flagged row. Pass `--check-dois` for CrossRef title checks. |

## When to apply this skill

Apply this skill any time you are:
- Building a new redox-potential database
- Extending an existing one with new sources
- Auditing an existing database for errors
- Verifying a candidate molecule before commitment to synthesis or experiment
- Compiling redox potentials for any electrochemistry, fuel-cell, or flow-battery design context

For one-off conversational questions about a single redox potential, this protocol is overkill — a quick web fetch + read suffices. Apply the protocol when the data will be used as a basis for downstream experimental decisions.

## Reference files

- `references/REFERENCE_ELECTRODES.md` — full conversion table, kept in sync with `conversion_arithmetic.py`'s KNOWN_OFFSETS
- `references/COMMON_ERRORS.md` — anti-pattern catalog with real examples from prior failures
- `references/SOURCE_DISCOVERY.md` — how to find open-access copies; URL ranking
- `references/EXTRACTION_PROMPT_TEMPLATES.md` — copy-paste agent prompts that bake in the protocol
- `references/VERIFICATION_PROMPT_TEMPLATES.md` — independent-verification agent prompt with granular flagged_* verdicts

## Evals

Test cases in `evals/evals.json` and fixture CSVs in `evals/files/`. Coverage:

- **scripts-clean-baseline**: 5 evidence-locked rows that should pass all checks.
- **scripts-detect-seeded-errors**: 7 rows with 5 deliberate errors of distinct types; checks that the sanity scripts catch each.
- **find-open-access-known-OA**: discover OA copies for a known-OA paper.
- **extract-from-Wedege-2016-with-provenance**: extract from a specific paper with full provenance; verify zero flags.
- **verify-row-on-self-contained-fixture**: programmatic verification of a row.
- **cross-source-disagreement-detection**: cross-source check catches a deliberately deviant row.
- **truncated-name-detection**: truncated-name check catches a substituent-prefix-only molecule field.
- **INACCESSIBLE-handling**: agent given a fake DOI must return INACCESSIBLE rather than fabricate.
- **multi-couple-schema-compliance**: one row per redox couple is the canonical pattern.
- **aprotic-vs-aqueous-coexistence**: same molecule in two solvents → two rows OK.
- **value-directness-derived-flagging**: derived values must be marked as such.
- **verifier-prompt-finds-mismatch**: verifier correctly flags a fake-DOI row.

### Running the evals

The skill is testable via the **skill-creator** skill. From the skill-creator directory:

```
# Run all evals; produces with-skill vs without-skill comparisons
python -m scripts.run_eval --skill-path /path/to/redox-extraction --eval-set evals/evals.json
```

For just the programmatic-script tests (evals 1, 2, 3, 6, 7, 9, 10, 11) you can run them directly without the skill-creator workflow — they are deterministic shell-script invocations and don't require a baseline. Evals 4, 5, 8, 12 are agent-based and need the skill-creator workflow to produce useful with-skill/baseline comparisons.

Quick local sanity check (validates that the scripts catch the seeded errors and don't false-flag the baselines):

```bash
cd protocols/redox-extraction
# Should report 0 flags
python3 scripts/run_all_checks.py evals/files/clean_baseline.csv
# Should report 5 flagged rows (with --check-dois) / 4 flagged (without)
python3 scripts/run_all_checks.py evals/files/seeded_errors.csv --check-dois
```

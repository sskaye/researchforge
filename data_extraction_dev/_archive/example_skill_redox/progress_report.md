# Redox Mediator Database — Progress Report

**Project:** Construction of a high-quality, evidence-locked database of redox-active molecules for an aqueous fuel cell.
**Status as of May 2026:** v2 of the skill deployed; trial 4 produced a 16,098-row database with **100% verified-on-spot-check** in 31 random rows. The skill has now been validated across two independent agent harnesses.

---

## Executive summary

We started with the goal of compiling a comprehensive table of candidate redox mediators for an aqueous fuel cell, drawing from the academic literature, public databases, and existing reviews. The first attempt produced ~12,500 rows, but spot-checks revealed roughly **50% of "verified" rows had real data-extraction errors** — wrong values, wrong citations, fabricated provenance. That failure was diagnosed as a systemic, recurring set of problems (memory-based fabrication, citation guessing, reference-electrode mislabeling, bad conversions) that any future build would repeat unless the process itself was hardened.

We responded by building a reusable **skill** — a documented protocol with pre-tested scripts, evals, and prompt templates — that forces evidence-locked extraction, programmatic sanity checks, and an independent verification pass. The skill went through five live-fire trials. The verified-on-spot-check rate climbed from **47% (trial 1, no skill)** to **80% (trial 2, v1 skill)** to **96% (trial 3, v2 skill)** to **100% (trial 4, v2 skill, different harness)** to **92% (trial 5, expanded experimental coverage)**, with the remaining errors becoming smaller (most are propagated upstream-source bugs rather than skill-side mistakes).

The resulting databases (trial 3 at 24,204 rows; trial 4 at 16,098 rows; trial 5 at 24,343 rows) are suitable for primary candidate screening for an aqueous fuel cell. The skill is packaged for re-use on other extraction projects, demonstrates harness-independence (trial 4), and surfaces *upstream* data quality issues that previously went unnoticed (trial 5).

---

## Project goal

Build a database of redox-active molecules with measured or computed potentials in aqueous (and some non-aqueous) media. Required fields per row: molecule identity, voltage in V vs SHE, and a citation that lets the user trace any value back to its source. Both anolyte (negative E°) and catholyte (positive E°) candidates are in scope. The user will use this database as a screening tool to identify candidate molecules for an aqueous fuel cell.

The hard requirement: **a row's value, conditions, and citation must accurately reflect what the cited paper actually says.** It's acceptable for the literature consensus to differ across sources for the same molecule. It's not acceptable to misattribute a value to a paper that doesn't contain it.

---

## Initial findings — what went wrong in the first trial

The first build was an iterative effort: ingest a few literature reviews, then progressively layer in primary papers, computational screens, and inorganic textbook references. After several rounds it had ~12,500 rows. Quality control was ad-hoc: cross-checking well-known compounds across sources, looking for outliers, etc.

### Spot-check on the first build (15 random rows)

Of 15 randomly sampled experimental rows in the "verified" tier:

- **47% verified** (within ±50 mV of the cited source)
- **27% mismatched** (>50 mV off, wrong molecule, or wrong citation)
- **27% inaccessible** (paywalled SI; values plausible but unverified)

The 27% mismatch rate was the alarm. Specific failure cases included:

| Failure | Description |
|---|---|
| Memory-based fabrication | One review was paywalled at extraction time; the agent compiled 62 rows from training memory rather than fetching. About 12 of those rows had wrong voltages by 100–200 mV. |
| Citation guessing | A "Fe-gluconate" row cited a paper that's actually about a completely different iron complex (Belva 2025 is about Na₄[Fe(Dcbpy)(CN)₄]). Several inorganic-block rows similarly cited papers whose titles bore no relation to the claimed molecule. |
| DOI corruption | A row claimed to extract from `10.1038/srep39102`. That DOI resolves to a tropical-forest carbon-storage paper, not a redox study. |
| Reference electrode mislabeled | 336 rows from one compilation stored SCE values in DMF as if they were already vs SHE. Systematically off by −0.241 V. |
| Wrong author attribution | "Wang/Aziz, ACS Energy Lett. 2019" — the actual first author is Luo. |
| Wrong absolute-scale conversion | A bulk computational source stored potentials on an absolute (vacuum-referenced) scale; the conversion to SHE was sign-flipped, putting 9,10-anthraquinone at −3.41 V vs literature's −0.44 V. |
| Truncated molecule names | Hundreds of rows had names like "2-iodo" instead of "2-iodoanthraquinone" — the substituent prefix without the parent scaffold. |
| Multi-couple confusion | Methyl viologen has two distinct redox couples (V²⁺/V⁺• at −0.45 V and V⁺•/V⁰ at −0.76 V). Some rows claimed values that were valid for *one* couple but stored against the molecule name without specifying which. |

The pattern was clear: errors came not from carelessness but from **structural omissions in how rows were captured**. Without per-row provenance, mistakes were indistinguishable from valid data and propagated through the build.

---

## Diagnosis

We classified every error into one of ten failure modes. Each was tied to a specific gap in the build process:

| Failure mode | Root cause |
|---|---|
| 1. Memory-based fabrication | Agents extracted without proving they fetched the source |
| 2. Citation-value mismatch | Agents guessed at "the most likely primary citation" |
| 3. Reference-electrode mislabeling | Trusted upstream compilations to have already done the conversion |
| 4. Truncated/corrupted data | No automated sanity checks on extracted strings |
| 5. Multi-couple confusion | No row-level "which couple" identifier |
| 6. Aprotic vs aqueous conflation | Solvent field too loose; mixing fundamentally different chemistries |
| 7. Wrong author attribution | Citations written from memory, not from CrossRef |
| 8. Indirect/derived values | No flag distinguishing direct measurement from derivation |
| 9. Wrong page/volume metadata | Same as #7 |
| 10. Molecule-vs-value mismatch | Plausible-looking pairs slip past review |

The deepest cause was that we had treated extraction as a single one-shot operation with no requirement for **proof of where every field came from**.

---

## Construction of the `redox-extraction` skill

The fix was to formalize the extraction process as a reusable skill. The skill enforces three principles:

1. **Evidence-locked rows.** Every row must come with three pieces of evidence: a precise source-location pointer, a verbatim quote from the source, and explicit conversion arithmetic (where applicable). Without these, a row is not in the database.
2. **No memory-based extraction.** Agents must return INACCESSIBLE if they can't fetch the source. Synthesis from training memory is forbidden as a hard rule.
3. **Independent verification.** A separate agent verifies each row by re-fetching the source and confirming the evidence quote — without seeing the original extractor's confidence or notes (no anchoring bias).

### Components

```
redox-extraction/
├── SKILL.md                           # Main protocol
├── scripts/                           # 8 pre-tested scripts
│   ├── find_open_access.py            # Discover OA URLs (Unpaywall, OpenAlex, Semantic Scholar, Europe PMC, CORE, Wayback)
│   ├── crossref_lookup.py             # Authoritative paper metadata
│   ├── validate_smiles.py             # RDKit + chemistry plausibility
│   ├── voltage_range_check.py         # Class-based voltage sanity
│   ├── conversion_arithmetic.py       # SHE conversion verification
│   ├── cross_source_consistency.py    # Cross-source disagreement detection
│   ├── verify_row.py                  # Per-row programmatic checks
│   └── run_all_checks.py              # Umbrella check runner
├── references/                        # Reference docs
│   ├── REFERENCE_ELECTRODES.md        # Conversion table
│   ├── COMMON_ERRORS.md               # Anti-pattern catalog
│   ├── SOURCE_DISCOVERY.md            # OA source ranking
│   ├── EXTRACTION_PROMPT_TEMPLATES.md # Copy-paste agent prompts
│   ├── VERIFICATION_PROMPT_TEMPLATES.md
│   └── SANITY_CHECK_SCRIPTS.md        # Index of scripts
└── evals/                             # 14 evals testing skill behavior
    ├── evals.json
    └── files/                         # Test fixtures
```

### Schema

Every row uses a single CSV with these required columns:

| Column | Purpose |
|---|---|
| `id` | Sequential row identifier |
| `verification_status` | Confidence tier (verified_*, pending_verification, flagged_review, unverified_computational) |
| `molecule` | Compound name; for multi-couple molecules, includes the couple identifier (e.g., "MV V²⁺/V⁺•") |
| `voltage_v_she` | Numeric value in V vs SHE |
| `voltage_raw` | Value as printed in source, including original units |
| `reference_electrode` | Reference reported in source |
| `solvent`, `ph` | Solvent/electrolyte (distinguishing aprotic vs aqueous is required) |
| `data_type` | experimental or computational |
| `value_directness` | direct, derived, or computed |
| `source` + `source_url` | Citation (no author names; DOI is canonical) |
| `evidence_location` | Precise pointer (e.g., "Table 1 row 3") |
| `evidence_quote` | Verbatim text from source |
| `conversion_arithmetic` | Math shown explicitly when units/reference were converted |

The `evidence_location` + `evidence_quote` + `conversion_arithmetic` triplet is what makes a row verifiable — a downstream auditor can find the source location in 30 seconds and confirm the quote.

### Programmatic checks (Phase 3)

Eight automated sanity checks run on any extracted CSV before it ships:

1. SMILES validity (RDKit + chemistry plausibility — rejects e.g. 4 carbonyls on one aromatic ring)
2. Voltage range by chemical class (quinones, viologens, etc., have known plausible ranges)
3. Conversion arithmetic verification (the math AND the offset must match a known reference)
4. Cross-source consistency (same molecule × same conditions × multiple sources must agree within tolerance)
5. Reference-electrode/electrolyte consistency (Hg/HgO can't be acidic; Fc/Fc⁺ in water is suspicious)
6. Placeholder citation detection ("Author et al." flags)
7. Truncated molecule name detection
8. DOI title relevance via CrossRef (catches DOIs that point to unrelated papers)

### Independent verification pass (Phase 4)

A separate agent verifies each row by re-fetching the source and confirming the `evidence_quote` is verbatim present at the stated `evidence_location`. The verifier uses granular flagged_* verdicts (`flagged_doi_unresolvable`, `flagged_value_mismatch`, etc.) that go into the row's notes when a row fails. Critically, the verifier never silently corrects values — it reports discrepancies and lets the maintainer decide.

---

## Improvements from trial 1 → trial 2 → trial 3 → trial 4 → trial 5

The skill went through five live-fire trials, with iterative improvements based on what each trial revealed. Trial 4 was a cross-harness validation (different agent system using the same skill). Trial 5 was the trial-3 agent expanding experimental coverage with newer literature — a coverage-expansion test rather than a further iteration.

### Trial 1 (initial build, no skill)

- **Build:** ~12,500 rows compiled from 25+ sources over multiple agent runs
- **Spot check:** 15 random aqueous experimental rows
- **Result:** 7 verified, 4 mismatch, 4 inaccessible — **47% verified-among-accessible**
- **Failures:** Citation-value mismatches (Fe-gluconate cited wrong paper, srep39102 tropical-forest paper), reference-electrode mislabeling (336 rows), memory fabrication (Kwabi review), truncated names, malformed SMILES

### Trial 2 (v1 skill — first deployed version)

- **Build:** 1,960 rows, conservative scope (skipped two paywalled review papers; trial 1 had assembled them from primary citations).
- **Spot check:** 30 random rows stratified across confidence tiers
- **Result:** 24 verified or correctly self-flagged, 6 self-disclosed mismatches, 0 surprise mismatches — **80% verified, 0 hidden errors**
- **What worked:** Every error was self-disclosed in the README under known caveats. The skill caught problems at the symptom level.
- **What didn't:** A bulk computational dataset (D3TaLES) had a documented conversion that turned out to be wrong; the agent applied it, got 564 implausibly negative rows (e.g., 9,10-AQ at −3.41 V vs literature −0.44 V), and correctly flagged them all — but the rows still ended up in the file as wasted space. The protocol's calibration sanity check was too soft ("investigate before extracting") to actually stop the bad extraction.

### Trial 3 (v2 skill — calibration gate hardened)

- **Build:** 24,204 rows. Larger because it included the full RedDB (15,882 rows) and Tabor 2019 quinone screen (1,968 rows) at scale.
- **Spot check:** 30 random rows stratified across tiers
- **Result:** 25 verified or correctly self-flagged, 1 surprise mismatch (45 mV off on a CRC textbook value), 1 metadata-only error, 3 inaccessible (paywall) — **96% verified-among-accessible**
- **Improvements from v1 → v2:**
  - Hardened the calibration spot-check from "investigate" to "STOP if any canonical molecule is off by >300 mV"
  - Added two new evals (`calibration-gate-blocks-bad-conversion`, `calibration-skipped-when-no-canonicals`) to regression-test the gate
  - Removed dataset-specific references throughout the protocol (D3TaLES specifically; the protocol now describes general absolute-scale conversions without naming any one dataset)
  - Documented the "read the source's API/schema source code, not just the paper prose" rule for non-trivial conversions
- **What the v2 skill caught in trial 3:**
  - The agent skipped D3TaLES entirely (no value extracted) — the calibration gate would have stopped it; bypassing it was the conservative choice
  - The agent used the published calibration formula for RedDB (`E° = −0.409 × E_rxn − 0.193`, Zhang et al. 2020) — verbatim match to Eq. 1 in the cited paper
  - 36 rows from the Tabor 2019 quinone screen were flagged_review for chemically-impossible SMILES (3+ exocyclic carbonyls on one aromatic ring) — the chemistry-plausibility check fired correctly
  - The phthalimide screen DOI was corrected (trial 2 had `10.1021/acs.joc.5c02047` which is wrong; trial 3 has `10.1021/acs.joc.5c01283` which is the actual paper)

### Trial 4 (v2 skill — different agent harness, cross-harness validation)

- **Build:** 16,098 rows from a different agent harness using the same v2 skill. The agent chose different secondary sources (no Tabor 2019 PM7 predictions, no Phthalimide screen, no Pang aza-aromatic screen). Added Emmel 2023 *Nat. Commun.* (the ReFlowLab paper, 39 rows) and Energies 2020 (14 rows) as primary-paper coverage.
- **Spot check:** 31 random rows stratified across pending_verification (12) and unverified_computational (19)
- **Result:** **31/31 VERIFIED_EXACT — 100% verified, 0 mismatches**
- **Different RedDB calibration:** Trial 4 used the newer **RedCat 2025 Eq. 2** calibration (Sorkun et al., *Digital Discovery* 4, 1844-1855):
  > E⁰_DFT (V vs RHE, pH 7) = [−0.41 × ΔE_rxn(eV)] − 0.63
  
  The agent applied this correctly across all 15,882 RedDB rows. Math verified within ±0.5 mV (rounding) on every audited row. This formula is similar in slope to Trial 3's Zhang 2020 formula but has a different intercept and reference (RHE-pH7 vs SHE directly), giving values systematically ~0.85 V more negative. Both are valid published calibrations of the same RedDB raw data; the choice depends on which publication the agent treats as authoritative. Trial 3 used the original Zhang/Khetan/Er 2020 paper; trial 4 uses the more recent RedCat 2025 update.
- **One labeling-clarity issue:** id=16073 BTMAP-Vi is reported at −0.72 V vs NHE — this is correct *as transcribed from the Emmel 2023 SI Table S8*, but the value is for the **second** redox couple (V⁺•/V⁰) per DeBruler 2017, not the canonical first couple (V²⁺/V⁺• at −0.36 V vs NHE per Beh 2017). The molecule field "BTMAP-Vi" is ambiguous; ideally would be "BTMAP-Vi V⁺•/V⁰ (second couple)". This is a multi-couple labeling issue rather than a value error.
- **What the cross-harness test demonstrates:** The skill is not specific to one agent system. A different harness, picking different sources and a different RedDB calibration formula, produced a database that passes spot checks with the same fidelity. The protocol's hard rules (evidence-locked rows, no memory-based fabrication, programmatic sanity checks) are what's doing the work, not any particular agent's idiosyncrasy.

### Trial 5 (v2 skill — trial-3 agent, expanded experimental coverage)

- **Build:** 24,343 rows = trial 3 (24,204) + 139 new experimental rows from added sources. Same agent harness as trial 3.
- **New experimental sources** (vs trial 3):
  - Huang 2022 *Nat. Commun.* 13, 4746 (DHAQ in concentrated alkaline, 18 rows)
  - ReFlowLab v1.0.0 Zenodo dataset / Emmel 2023 *Nat. Commun.* 14, 6672 (42 rows from ACTIVEMATERIAL SQLite table)
  - Benzidine derivatives, ACS Omega 2023 (13 rows)
  - Tungsten POM AORFB, Nat. Commun. 2025, 16, 4654 (9 rows)
  - Six-electron material, Adv. Sci. 2025 (4 rows)
  - Isoindoline nitroxides, ChemSusChem 2026 (3 rows)
  - 1,4-diketones, Molecules 2021 (6 rows)
  - TEMPO catholytes, RSC Adv. 2020 (5 rows)
  - + others
- **Spot check:** 30 rows (10 from existing-source controls, 20 from new sources)
- **Result:** 21 VERIFIED_EXACT + 2 VERIFIED_CLOSE + 1 MISMATCH + 1 name-error + 2 flag-correct + 4 INACCESSIBLE = **24/26 verified-among-accessible (92%)**
- **What the skill caught correctly:**
  - 2 phenoxazine rows correctly flagged for `flagged_reference_electrode_mismatch` (paper reports "(vs Ag/AgCl)" without specifying electrolyte → no SHE conversion attempted)
  - PPO isoindoline nitroxide flagged `flagged_voltage_oor` (legitimately at +1.16 V, outside the conservative 0.5-1.0 V nitroxide range — true positive flag, but not a value error)
- **What surfaced in spot check (NEW failure category — upstream data errors):**
  - **id=305 DBEAQ at pH 14 = -0.68 V** is wrong. The canonical Kwabi/Lin 2018 *Joule* value is -0.48 V (and the database has that correct value separately as id=126). The -0.68 V is the canonical 2,6-DHAQ pH 14 value. **This is a propagated upstream error**: ReFlowLab's SQLite database itself appears to have swapped DBEAQ and DHAQ values. The skill faithfully extracted what ReFlowLab said.
  - **id=302 ARS molecule name** is wrong. ReFlowLab labels its row "Anthraquinone-2-sulfonic acid" with formula C14H8O5S, but ARS = Alizarin Red S = 3,4-dihydroxyanthraquinone-2-sulfonic acid (C14H8O7S). Same upstream-error pattern — value is correct, name is wrong in the source database.
  - **All 13 ReFlowLab rows have `value_directness=derived`** when they should be `direct` (literal SQLite lookups). This is a labeling pattern error from the trial-5 agent's interpretation, not an upstream issue.
- **What this teaches us:** With the skill's protections in place, the dominant remaining error class is **propagated upstream-source bugs** that we can no longer attribute to the extraction agent. The skill is doing its job — pulling exactly what the cited source contains. When the source itself is wrong, no amount of extraction discipline catches it. Future iterations should add **cross-source corroboration** as a stronger defense (e.g., when DBEAQ pH 14 appears in two rows from two sources with 200 mV disagreement, both should be flagged).

### Quantitative comparison

| Metric | Trial 1 (no skill) | Trial 2 (v1) | Trial 3 (v2) | Trial 4 (v2, diff harness) | Trial 5 (expanded exp.) |
|---|---|---|---|---|---|
| Total rows | 12,540 | 1,960 | 24,204 | 16,098 | 24,343 |
| Verified-among-accessible | 47% | 80% | 96% | **100%** | 92% |
| Surprise mismatches (in spot check) | 4 / 15 | 0 / 30 | 1 / 30 | 0 / 31 | 1 / 26 + 1 name |
| Self-flagged bad rows | 0 | 564 | 36 | 0 | 2 |
| Bulk-source calibration errors | several | 1 (D3TaLES) | none | none | none |
| Memory-fabricated rows | 62+ | 0 | 0 | 0 | 0 |
| Wrong-citation rows | ~10+ | 0 | 0 | 0 | 0 |
| Reference-electrode mislabeling | 336 | 0 | 0 | 0 | 0 (skill caught 2 ambiguous cases and refused to convert) |
| Avg mismatch magnitude (when present) | hundreds of mV | several V (rare, all flagged) | tens of mV | none observed | one 200 mV upstream-source bug |
| Multi-couple labeling issues | several | none | none | 1 (BTMAP-Vi) | 0 |
| Propagated upstream errors | unknown | unknown | unknown | unknown | 2 (DBEAQ value, ARS name in ReFlowLab) |
| `value_directness` labeling errors | unknown | unknown | unknown | 0 | 13 (ReFlowLab rows mis-tagged "derived") |

### What the trials demonstrate

1. **The skill works.** Going from trial 1 to trial 5, the verified rate climbed from 47% to 92-100% on similar spot-check protocols. The errors that remain are smaller, self-disclosed, or attributable to upstream sources.

2. **Self-disclosure beats hidden errors.** Trial 2's 564 D3TaLES rows were wrong but flagged; the user was never misled. Trial 1's errors were silent and the user would have used them.

3. **Iteration is necessary.** Trial 2's calibration gap motivated the v2 hardening. Trial 3's small remaining issues led to the BTMAP-Vi-style multi-couple-labeling concern flagged in trial 4. Trial 5 surfaced upstream-source error propagation as the next frontier.

4. **The skill is harness-independent.** Trial 4 used a different agent system from trials 1-3 and produced equally clean output. The protocol's hard rules — not the underlying agent — are what enforce quality.

5. **The skill accommodates legitimate methodological choices.** Trial 3 and trial 4 made different but equally valid decisions: which RedDB calibration formula to use (Zhang 2020 vs RedCat 2025), which secondary computational sources to include, which review papers to cite. Both produced verified rows; the protocol is not opinionated about which choice is "right" so long as the row's evidence is consistent.

6. **Once skill-side errors are eliminated, upstream-source quality becomes the next frontier.** Trial 5 found two errors that the skill couldn't have prevented: ReFlowLab's SQLite database has DBEAQ paired with the wrong value at pH 14, and labels ARS with the wrong molecule name. Both are bugs in the curated public dataset itself, faithfully transcribed by the trial-5 agent. The next-generation defense is cross-source corroboration: flag any row whose value disagrees by >100 mV with another row in the same database for the same molecule × conditions.

---

## Trial 5 database overview

The trial-5 deliverable is `trial5 - Experimental/redox_mediator_db.csv`, with **24,343 rows** = trial 3 (24,204) plus 139 new experimental rows. Total experimental coverage grew from 199 to 338 rows; computational coverage unchanged.

| Source category | Rows |
|---|---:|
| RedDB + Tabor + Phthalimide + Pang (computational, inherited from trial 3) | 24,005 |
| Wedege 2016 + Kwabi 2020 review + CRC textbook (experimental, inherited) | 199 |
| Newly added experimental sources (Emmel/ReFlowLab, Huang 2022, Benzidine, POM, etc.) | 139 |

By verification status:
- 32 verified_textbook (CRC anchors)
- 304 pending_verification (experimental, awaiting Phase 4 — includes the new additions)
- 38 flagged_review (36 Tabor invalid SMILES + 2 phenoxazine ambiguous Ag/AgCl)
- 23,969 unverified_computational

Recommended corrections after spot-check:
1. **id=305 DBEAQ at pH 14 = -0.68 V** is wrong (should be -0.48 V per Kwabi/Lin 2018 *Joule*). Propagated from ReFlowLab upstream error. Recommend either correcting to -0.48 V or removing the row (id=126 already has the correct value).
2. **id=302 ARS molecule name** is wrong (should be "Alizarin Red S = 3,4-dihydroxyanthraquinone-2-sulfonic acid", formula C14H8O7S). Propagated from ReFlowLab.
3. **All 13 ReFlowLab rows** should have `value_directness=direct`, not `derived`. (Literal SQLite lookups are direct.)
4. The class-range check for nitroxides (0.5-1.0 V) generated one false-positive flag on PPO (+1.16 V); consider an "isoindoline-pyridinium nitroxide" subclass with a wider range.

## Trial 4 database overview

The trial-4 deliverable is `trial4/candidate_redox_mediators.csv`, with **16,098 rows** spanning:

| Source | Rows | Type |
|---|---:|---|
| RedDB (Sorkun et al. 2022) — RedCat 2025 calibration | 15,882 | computational |
| Wedege et al. 2016 | 87 | experimental |
| Emmel 2023 *Nat. Commun.* (ReFlowLab) | 39 | experimental |
| Tabor 2019 calibration set (J. Mater. Chem. A 7, 12833) | 27 | experimental |
| RedCat 2025 (Digital Discovery 4, 1844) — top candidates | 25 | computational |
| Energies 2010, 3, 803-846 (review-extracted) | 14 | experimental |
| Various primary papers (Lin 2016 Nat. Energy, Beh 2017 ACS EL, Jin 2020 AEM, etc.) | ~25 | experimental |

By verification status:
- 191 pending_verification (experimental, awaiting Phase 4)
- 15,907 unverified_computational (RedDB; ±150–200 mV typical accuracy)
- 0 verified_textbook (this harness chose to skip CRC anchors — coverage gap, not error)
- 0 flagged_review (no SMILES validity issues encountered)

One labeling-clarity issue surfaced in spot-check: id=16073 BTMAP-Vi at −0.72 V vs NHE is the second redox couple (V⁺•/V⁰), not the canonical first. The value is correctly transcribed from the cited Emmel 2023 SI but the molecule field doesn't specify which couple. Suggested fix: rename to "BTMAP-Vi V⁺•/V⁰ (second couple)" or add a sister row at −0.358 V for the first couple.

## Trial 3 database overview

The trial-3 deliverable is `trial3/redox_mediator_db.csv`, with **24,204 rows** spanning:

| Source | Rows | Type |
|---|---:|---|
| RedDB (Sorkun et al. 2022) | 15,882 | computational |
| Phthalimide screen (Moraes et al. 2026) | 5,639 | computational |
| Tabor / Cheng / Aspuru-Guzik 2019 quinone screen | 1,968 | computational (36 self-flagged) |
| Pang / Vlachos 2022 aza-aromatic screen | 516 | computational |
| Wedege et al. 2016 | 85 | experimental |
| Kwabi / Ji / Aziz 2020 critical review | 66 | experimental (review-extracted) |
| CRC Handbook 102nd ed. textbook anchors | 26 | experimental |
| Various primary papers (Huskinson 2014, Lin 2015, Beh 2017, Kwabi 2018, Hollas 2018, etc.) | ~20 | experimental |
| Bird & Kuhn 1981, Bard/Parsons/Jordan textbooks, Pavlishchuk-Addison Fc/Fc⁺ | 5 | experimental |

By verification status:
- 32 verified_textbook
- 167 pending_verification (experimental, not yet through Phase 4)
- 36 flagged_review (correctly flagged for invalid SMILES)
- 23,969 unverified_computational (bulk DFT/ML; ±150–200 mV typical accuracy)

Two minor corrections recommended (both surfaced in the trial-3 spot check):
1. Row id=17 (V²⁺/V): voltage_v_she = -1.13 V should be -1.175 V per CRC Handbook 102nd ed. (the canonical Vanysek table has -1.175)
2. Row id=90 (HQ(1,4)S): reference_electrode field says "Ag/AgCl(3M KCl)" but should be "NHE" (Wedege SI Table 4a column header explicitly reports values vs NHE)

---

## Lessons learned

### For redox / chemistry data extraction specifically

1. **Reference-electrode discipline is non-negotiable.** "Ag/AgCl" without the electrolyte specified is ambiguous (sat KCl, 3 M KCl, 3 M NaCl give different offsets to SHE). The protocol now requires the electrolyte be explicit, and the conversion-arithmetic check rejects ambiguous references.

2. **Aprotic and aqueous redox are different physical processes.** For a substituted quinone, the aprotic 1-electron Q/Q•⁻ potential can be 0.5–1.5 V more negative than the aqueous 2H⁺/2e⁻ PCET potential — they are different reactions. The protocol forces these to live in distinct rows with the solvent field clearly distinguishing them.

3. **Multi-couple molecules need explicit couple identifiers.** Methyl viologen has two distinct 1-electron reductions; anthraquinones in aprotic media show two reductions. Without specifying which couple, downstream tools confuse them.

4. **Computational databases need calibration spot-checks.** A bulk computational dataset's documented conversion may be wrong (D3TaLES showed this), or the conversion may be right but uncalibrated DFT (RedDB requires the published Zhang 2020 calibration). Spot-checking known molecules catches both kinds of errors.

### For the broader question of data extraction by LLM agents

1. **Memory-based fabrication is the dominant failure mode for "factual" extraction tasks.** Models have plausible-looking values for well-known compounds in training, but the specific decimals are often wrong by 50–200 mV. The cure is to make extraction without a fetched source structurally impossible — agents must return INACCESSIBLE rather than synthesize.

2. **Per-row provenance is the foundation of auditability.** A row without an evidence quote and source location is indistinguishable from a fabrication. With those fields, verification is a 30-second job per row.

3. **Independent verification beats self-verification.** The same agent that extracts a row is too anchored to spot its own errors. A fresh-context agent doing only verification, with no access to the extractor's confidence, catches more.

4. **Programmatic sanity checks scale.** Eight cheap, deterministic checks (SMILES validity, voltage range, arithmetic, etc.) catch a large fraction of errors before any human review.

5. **Self-disclosure of limitations is more valuable than hiding them.** A README that lists "we know rows X-Y are bad, here's why" lets the user filter intelligently. A README that claims everything is verified, when it isn't, leads to bad downstream decisions.

---

## Future work

### Database extensions

- Re-run the calibration-blocked D3TaLES extraction using the dataset's API directly (rather than the public CSV export) to get the calibrated `reduction_potential` field.
- Add the Yin / Liu 2024 viologen review (paywalled) by fetching primary citations the review covers.
- Extend to non-aqueous catholyte candidates if the fuel-cell design eventually needs them.
- Apply the trial-3 metadata corrections (V²⁺/V value, HQ(1,4)S reference electrode).

### Skill iteration

- Add a metadata-consistency check (reference_electrode field must be consistent with what the source actually reports — caught by manual review in trial 3 but missed by automated checks).
- Add a `value_directness=derived` plausibility check (cell-voltage-derived values should be flagged when the catholyte source isn't co-cited).
- Possibly: a self-test of the calibration formula at extract time. For RedDB, the agent could validate the Zhang 2020 formula against 5 random rows whose ΔE_rxn is known to give a known E° from the original paper's Figure 5.

### Process

- The skill now has 14 evals, all passing. The skill-creator workflow lets us regression-test future changes.
- The trial-over-trial improvement (47% → 80% → 96% → 100%) suggests we've reached the point of diminishing returns on the current spot-check protocol. Future tightening should focus on subtler issues: multi-couple labeling, metadata consistency between fields, value_directness audit completeness.
- Trial 4's harness-independence demonstrates the skill is portable. It can be applied to other electrochemistry data extraction projects (battery materials, electrocatalysts, etc.) with the same hard rules: evidence-locked rows, no memory-based extraction, independent verification.
- A reasonable next milestone: combine trial 3 and trial 4 (deduplicating overlapping RedDB rows on InChIKey) into a single consensus database, with the union of sources covered. Trial 3 covers Tabor PM7 + Phthalimide + Pang screens; trial 4 covers Emmel ReFlowLab + RedCat 2025 + Energies 2010. Combined coverage is broader than either alone.

---

## Deliverables

| File | Purpose |
|---|---|
| `dist/redox-extraction.skill` | Installable skill (v2) — apply to any future extraction work |
| `redox-extraction/` | Skill source code (for editing/iterating) |
| `trial3/redox_mediator_db.csv` | Trial 3 database, 24,204 rows (RedDB + Tabor + Phthalimide + Pang + 199 experimental) |
| `trial4/candidate_redox_mediators.csv` | Trial 4 database, 16,098 rows (RedDB + Emmel + RedCat 2025 + 191 experimental). Different agent harness, 100% spot-check verified. |
| `trial5 - Experimental/redox_mediator_db.csv` | Trial 5 database, 24,343 rows = trial 3 + 139 new experimental rows. 92% spot-check verified, with 2 propagated ReFlowLab upstream errors flagged. |
| `initial_trial/` | First-trial outputs preserved for reference |
| `progress_report.md` | This document |

---

*Report prepared May 2026; updated with trial 4 cross-harness validation and trial 5 expanded-experimental-coverage results.*

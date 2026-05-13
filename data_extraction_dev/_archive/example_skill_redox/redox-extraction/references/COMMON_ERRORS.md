# Common errors in redox-potential extraction

A catalog of error patterns observed in real extraction work, with real examples from prior failed attempts. Each entry lists the failure mode, an example, the root cause, and how the protocol prevents it.

## 1. Memory-based fabrication

**Pattern:** Agent without web access generates plausible-sounding but unverifiable rows.

**Real example:** Kwabi/Aziz Chem. Rev. 2020 first extraction attempt. Agent reported NMe-TEMPO at +0.79 V vs SHE; actual paper reports +1.00 V. Eleven other rows had similar errors.

**Root cause:** Models default to coherent-looking output when they can't verify. Plausible values for well-known molecules are encoded in training, but specific decimals and conditions are often wrong.

**Prevention:** Phase 1 of the protocol explicitly forbids extracting without a fetched source. Agents must return INACCESSIBLE rather than fabricate. The extraction prompts state this as a hard rule.

## 2. Citation-value mismatch

**Pattern:** The DOI in the source field does not point to a paper containing the cited compound or value.

**Real examples:**
- Fe-gluconate cited Belva & Aziz 2025 *Energy Storage* (DOI 10.1002/est2.70198). The Belva paper is about Na₄[Fe(Dcbpy)(CN)₄], a completely different iron complex. Correct primary: Tang 2022 *J. Energy Chem.* 73, 445.
- 1,8-DHAQ cited DOI 10.1038/srep39102. That DOI resolves to "Diversity and carbon storage across the tropical forest biome" — unrelated to redox chemistry.
- Fe-DTPA cited DOI 10.1016/j.jpowsour.2018.03.038, which resolves to a squid-chitin supercapacitor paper.

**Root cause:** Agent guessed at "the most likely primary citation for this molecule's redox potential" rather than starting from a real paper.

**Prevention:** Phase 1 step 2 requires `crossref_lookup.py --require-keywords` to confirm the DOI's title is on-topic. Phase 3 includes `--check-dois` for bulk verification. The skill's `run_all_checks.py --check-dois` flag catches this class of error.

## 3. Reference-electrode mislabeling

**Pattern:** Values reported in one electrode reference are stored as if they were already vs SHE.

**Real examples:**
- 336 Gao 2025 organic-solvent rows: SCE-in-DMF values stored as "vs SHE". The Gao 2025 paper claimed values were "already converted to SHE" but they hadn't been. All values were systematically -0.241 V too negative.
- Row #12526 (SPr)₃₄TpyTz: -0.47 V vs Ag/AgCl(3M KCl) stored as -0.45 V vs SHE.
- Fe-NTMPA2: "near -0.30 V vs Ag/AgCl" stored as -0.30 V vs SHE.

**Root cause:** Compilations and reviews often say "values vs SHE" without fully tracking back to the original measurement reference. Agents trust the compilation.

**Prevention:** Phase 1 step 5 requires the agent to record the source's actual reference convention. Phase 2 requires `conversion_arithmetic` shown explicitly — if no offset was applied, that's a visible flag. `conversion_arithmetic.py` verifies the math.

## 4. Truncated or corrupted molecule data

**Pattern:** Names cut off, SMILES malformed, or substituent prefix kept without the parent scaffold.

**Real examples:**
- 250 truncated names in Gao 2025 organic subset: "2-iodo" instead of "2-iodoanthraquinone"; "2,6-dihydroxy" instead of "2,6-dihydroxyanthraquinone".
- Row #115: SMILES that RDKit parses syntactically but with chemistry-impossible features.

**Root cause:** Source files (especially docx-converted SI files) sometimes have truncations. Agents don't programmatically validate molecule fields.

**Prevention:** `validate_smiles.py` uses RDKit + chemistry-plausibility checks (rejects 4 carbonyls on one aromatic ring). `run_all_checks.py` flags names ending in substituent prefixes ("...hydroxy", "...iodo") without parent scaffold.

## 5. Multi-couple confusion

**Pattern:** A molecule with multiple distinct redox events captured as a single "the" potential.

**Real examples:**
- Methyl viologen has TWO sequential 1-electron reductions: V²⁺/V⁺• at ~ -0.45 V and V⁺•/V⁰ at ~ -0.76 V. Some rows listed only one without specifying which.
- Anthraquinones in aprotic media show two 1-electron reductions (Q/Q•⁻ and Q•⁻/Q²⁻). Mixing these without annotation produces apparent "disagreement" between sources.
- Pan 2023 NMe-TEMPO at +0.81 V and 4-OH-TEMPO at +0.95 V — appear to have been swapped during figure-extraction.

**Root cause:** Agents pull "a redox potential" from a paper without considering that multiple may be reported.

**Prevention:** Phase 6 hard rule: ONE ROW PER COUPLE. Molecule field or notes must specify the couple (e.g., "methyl viologen V²⁺/V⁺•" vs "methyl viologen V⁺•/V⁰"). `cross_source_consistency.py` flags multi-source disagreements that often indicate this.

## 6. Aprotic vs aqueous conflation

**Pattern:** The same molecule has very different potentials in aprotic vs aqueous media, but the row doesn't make this clear.

**Real example:** 1,4,5,8-tetraamino-9,10-anthraquinone (Disperse Blue 1):
- DMF, 1-electron Q/Q•⁻: -1.080 V vs SHE
- Water pH 6.5, 2H⁺/2e⁻ PCET: +0.168 V vs SHE
- Difference: ~1.25 V, but both are correct measurements of the same molecule.

**Root cause:** Aprotic and aqueous redox are fundamentally different reactions. Aqueous PCET potentials are typically 0.5-1.5 V more positive than aprotic Q/Q•⁻ for the same molecule.

**Prevention:** Phase 6 rule: solvent field must clearly distinguish aprotic from aqueous. For aqueous fuel-cell screening, filter on `solvent` containing "water".

## 7. Wrong author attribution (HISTORICAL — no longer tracked)

**Pattern (historical):** Citation listed wrong first author.

**Real examples:**
- "Wang/Aziz, ACS Energy Lett. 2019" should have been Luo, Hu, Hu, Zhao, Liu (Liu lab USU).
- "Garrido-Barros et al." should have been Barros, A.

**Root cause:** Agent inferred author from title context or memory rather than looking up the DOI.

**Prevention:** **The protocol no longer tracks author names.** The DOI in `source_url` is the canonical identifier. CrossRef can look up authors at any time if needed for display. Removing the `author` field from the schema eliminates this error class entirely.

## 8. Indirect/derived values masquerading as direct measurements

**Pattern:** Value calculated from a cell voltage minus the catholyte E°, or read from a figure axis position, but recorded as if it were a direct CV measurement.

**Real example:** Original Fe-gluconate row had E° = -1.05 V derived as "1.19 V cell voltage − 0.36 V Fe-CN catholyte" — but this implicitly used an alkaline ferrocyanide value that was itself uncertain. Net error: +0.22 V.

**Root cause:** Reviews and perspective papers often quote cell voltages, and agents convert these to half-cell potentials assuming a counter electrode value.

**Prevention:** Phase 2 `value_directness` field. `direct` only for explicitly measured E°. Anything inferred → `derived` with the inference explained.

## 9. Wrong page/volume metadata

**Pattern:** Citation has correct paper title and DOI but wrong page number, volume, or year.

**Real examples:** Multiple inorganic-block rows had wrong pages (e.g., Mn(CN)₆ cited page 4385, actual is 3702-3709).

**Root cause:** Agent wrote citation strings from memory, not from the actual paper's metadata.

**Prevention:** Phase 1 step 3: `crossref_lookup.py` provides authoritative metadata. The source field should be filled from CrossRef output, not from memory.

## 10. Molecule-name vs value mismatch

**Pattern:** The molecule name and the value both look reasonable for the chemistry family, but they belong to different molecules.

**Real examples:**
- Row #26: -0.62 V is the potential for **alloxazine 7-carboxylic acid (ACA)**, not 7,8-dimethyl-alloxazine (which is ≤ -0.73 V vs SHE).
- Pan 2023 row 1232: labeled "DPivOHAQ" but the structure shown was a different compound.

**Root cause:** Plausible-looking pairs slip past review because each half looks chemically reasonable. Detection requires checking against the *specific* molecule's known potentials.

**Prevention:** Phase 4 independent verification by a different agent without anchoring; `cross_source_consistency.py` catches values that disagree with consensus for that specific molecule.

## Detection priorities

If you can only run a subset of checks, prioritize:

1. **DOI title check** (`run_all_checks.py --check-dois`) — catches the most damaging error class (wrong-citation).
2. **Conversion arithmetic verification** (`conversion_arithmetic.py`) — catches reference-electrode mislabeling.
3. **SMILES validity** (`validate_smiles.py`) — catches malformed structures.
4. **Cross-source consistency** (`cross_source_consistency.py`) — catches molecule-vs-value mismatches.
5. **Placeholder citation pattern** (built into `run_all_checks.py`) — catches "Author et al." gaps.

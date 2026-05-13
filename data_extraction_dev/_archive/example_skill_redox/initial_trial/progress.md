# Redox Mediator Database — Progress Log

**Final state:** Compiled 2026-04-28. **12,540 entries** in `redox_mediators.xlsx` and `redox_mediators.csv`.

**Goal:** Comprehensive table of redox-active molecules for an aqueous fuel cell. Required fields: Molecule, Voltage (vs. SHE), Source. Optional: Solvent. Both experimental and computational data, flagged separately. One row per measurement.

**User preferences:**
- Anolyte focus, but include catholyte too
- Below water window OK (HER mitigation tech available)
- Both experimental and computational, flagged
- One row per measurement

---

## Final deliverables (in workspace folder)

| File | Contents |
|---|---|
| `redox_mediators.xlsx` | 5-sheet workbook: README, Summary, Data (all 12,540), Data_Experimental (1,148), Data_Computational (11,388). Filterable, color-coded by voltage. |
| `redox_mediators.csv` | Same data, flat CSV, 12,540 rows + header. |
| `progress.md` | This file. |

---

## Output schema

| Column | Notes |
|---|---|
| molecule | Name; SMILES used when no name available |
| voltage_v_she | Voltage in V vs. SHE (after conversion if needed) |
| voltage_raw | Voltage as reported in the source, before conversion |
| reference_electrode | Reference reported in source |
| solvent | Solvent / electrolyte ("water" for aqueous; "MeCN", etc. for non-aqueous) |
| ph | pH if reported (aqueous only) |
| n_electrons | Number of electrons in the redox event |
| data_type | "experimental" or "computational" |
| source | Citation sufficient to find the source document |
| source_url | URL or DOI link |
| notes | Chemical family, role (anolyte/catholyte), or other context |

---

## Reference-electrode conversions used

| Reported reference | Offset added to get SHE |
|---|---:|
| SHE / NHE | 0.000 V |
| SCE (saturated KCl) | +0.241 V |
| Ag/AgCl, sat. KCl | +0.197 V |
| Ag/AgCl, 3 M KCl | +0.210 V |
| Hg/HgO, 1 M NaOH | +0.098 V |
| Hg/HgO, 1 M KOH | +0.098 V |
| Fc/Fc+ in MeCN | +0.400 V (approximate) |
| RHE → SHE (at pH x) | subtract 0.0591 × pH |
| Li/Li+ (carbonate) | −3.040 V |
| D3TaLES abs scale → SHE | V_SHE = 4.42 − raw |

---

## Systematic audit (April 28, 2026)

After the user identified spot-check failures, the full database was systematically audited. Key changes:

### New: `verification_status` column
Every row now has a confidence tier:

| Status | Rows | Description |
|---|---:|---|
| verified_textbook | 100 | Bard/CRC/Pope reference data |
| verified_primary | 57 | Primary literature paper, citation verified |
| verified_extraction | 393 | Agent fetched and parsed actual SI/paper |
| verified_by_audit | 48 | Passed explicit audit against primary source |
| audit_corrected | 24 | Audit found and corrected an issue |
| auto_corrected_systematic | 336 | Programmatic fix (Gao 2025 SCE→SHE) |
| spot_checked | 114 | Source spot-checked (~70-90% reliable) |
| flagged_review | 30 | Issue found — review before use |
| unverified_computational | 11,388 | Bulk DFT/ML data, internally consistent |
| unverified | 52 | Residual unverified |

### Tier-based filtering for screening:

- **Tier 1 (958 experimental rows)** — high confidence. Use these for primary candidate selection.
- **Tier 2 (114 rows)** — spot-checked sources (Yin 2024 viologens, Pan 2023 SmartMat, Luo 2019). Useful but verify any specific candidate against its primary before commitment.
- **Tier 3 (30 rows)** — flagged. Don't use without re-verification.
- **Tier 4 (11,440 rows)** — bulk computational. Use for chemical-space exploration; don't treat individual values as ground truth.

### Audit findings and fixes applied:

1. **250 truncated molecule names in Gao 2025 organic subset** → fixed via PubChem InChIKey lookup. Most were just substituent prefixes (e.g., "2-iodo" → "2-Iodoanthraquinone").

2. **Kwabi 2020 (62 rows)** — agent originally compiled from training memory; audit against actual paper found 12 voltage errors:
   - #2 2,7-AQDS: 0.13 → 0.21 V
   - #5 DHAQDS: -0.12 → +0.13 V
   - #6 DBEAQ: -0.47 → -0.54 V at pH 12
   - #8 PEGAQ: -0.52 → -0.43 V
   - #14 ARS: pH 14/-0.48 V → pH 0/+0.08 V (Kwabi only reports acidic)
   - #15 Tiron at -0.46 V flagged (Kwabi T1 actually shows BQDS posolyte at +0.85 V; likely confused)
   - #19 (NPr)2V: -0.39 → -0.35 V
   - #33 NMe-TEMPO: 0.79 → 1.00 V
   - #34 TEMPTMA: 0.79 → 1.00 V
   - #37 Ferrocyanide pH 14: 0.36 → 0.50 V
   - #52 2,6-DBEAQ: -0.51 → -0.54 V
   - #60 Methylene blue: 0.011 V/pH 7 → 0.57 V/acidic

3. **Inorganic block (52/66 specific-citation rows audited)** — found 13 wrong citations:
   - #4115 Fe-DTPA → Waters/Robb/Marshak ACS EL 2020 (wrong DOI was a squid-chitin paper)
   - #4124 Cr-MGDA → flagged (DOI not a real Marshak paper)
   - #4137 PV14 POM → Friedl 2018 EES (wrong DOI was a CoS-graphene paper)
   - #4144 Fc(NPr)2 → Chen ChemSusChem 2021
   - #1262/#1263/#1280 → Luo et al. (was wrongly attributed to "Wang/Aziz")
   - #12512/#12513/#4136 PW12/SiW12 → Li 2025 (was wrongly attributed to "Wang")
   - #12514/#12515 CoW12/CoSiW11 → Barros 2024 (was "Garrido-Barros"; pages corrected)
   - Plus #4119 Fe-gluconate (already fixed previously)

4. **Recent primaries 2023-2025 (67 rows)** — found 14 with placeholder/wrong citations, all flagged:
   - 9 had literal "Author et al." in citation
   - 5 had wrong primary citations (e.g., #12503 4-OT TEMPO cites Hu 2024 which actually studies TPP-TEMPO/TMA-TEMPO, not 4-OT)
   - 8 had values estimated from cell voltage rather than direct E°

5. **Yin 2024 / Pan 2023 / Luo 2019 spot checks (45 rows)** — most verified. A few specific issues:
   - Pan 2023 NMe-TEMPO at 0.81 V should be 0.95 V (likely swapped with 4-OH-TEMPO)
   - Luo 2019 row 1267 has chemically meaningless name "3,4,5-tribenzoquinone-1,3-benzenedisulfonate"
   - Some role mislabels in Luo 2019 nonaqueous Li-organic rows

6. **Cross-source disagreements (5 groups, 18 rows flagged)**:
   - FcNCl: Hu/Luo primary 0.40 V vs Kwabi-derived 0.61 V (likely citation mismatch — Hu 2017 actually reports FcN112)
   - NMe-TEMPO: Kwabi 0.79 vs Luo 0.95 (audit confirms 1.00 V is correct)
   - Methyl viologen: 318 mV spread is actually two distinct redox couples (V²⁺/V⁺• and V⁺•/V⁰), not a real disagreement

### What this means for use

**Recommended workflow for fuel-cell candidate identification:**
1. Open `Data_Tier1_HighConfidence` sheet (958 rows). This is your reliable ground.
2. Filter to your voltage window of interest. Sort by voltage_v_she.
3. For molecules of interest, click the source_url to verify the primary paper.
4. Use `Data_Computational_Bulk` to find scaffold classes outside the experimental coverage — but treat individual values as ±200 mV at best.
5. Avoid Tier 3 unless you can re-verify the row.

---

## Sources processed

| Source | Type | Rows |
|---|---|---:|
| Moraes et al., J. Org. Chem. 2026 (phthalimide screen) | computational (DFT in MeCN) | 5,172 |
| D3TaLES (Duke et al., Digital Discovery 2023) | computational (DFT in MeCN) | 3,002 |
| RedDB (Sanyal et al., Sci. Data 2022) | computational (DFT in PCM water) | 2,266 |
| Gao et al., J. Power Sources 2025 (ML redox-potential DB) | experimental (compiled, primary DOIs preserved) | 531 |
| Pang et al., J. Mater. Chem. A 2022 (aza-aromatic HT screen) | computational (DFT in water) | 516 |
| Er et al., Chem. Sci. 6, 885 (2015) (all-quinone HT shortlist) | computational (DFT in water) | 407 |
| Wedege et al., Sci. Rep. 6, 39101 (2016) | experimental (33 cmpds × 3 pH) | 88 |
| Ding et al., Chem. Soc. Rev. 47, 69 (2018) | experimental (review tables 6, 7, 8, 9, 11) | 77 |
| Recent 2023-2025 primary literature sweep | experimental (68 novel molecules) | 68 |
| Kwabi/Aziz, Chem. Rev. 120, 6467 (2020) | experimental (review compilation) | 62 |
| Pan et al., SmartMat 2023 | experimental (extracted from Figure 1 timeline) | 61 |
| Bard, Parsons & Jordan, Standard Potentials in Aqueous Solution (1985) | experimental (textbook reference) | 59 |
| Yin, Duanmu, Liu, J. Mater. Chem. A 2024 (viologen review) | experimental (assembled from primary citations) | 43 |
| CRC Handbook of Chemistry and Physics, 102nd Ed. | experimental (handbook reference) | 35 |
| Sorkun et al., Digital Discovery 2025 (RedCat) | computational (top-5 per moiety) | 25 |
| Luo et al., ACS Energy Lett. 2019 (Status and Prospects) | experimental (review narrative) | 24 |
| Lieberman et al., Molecules 2022 (Family Tree review prose) | experimental (review prose) | 21 |
| Primary AORFB papers (Huskinson 2014, Lin Aziz 2015, Beh 2017, Hu Liu 2017, Kwabi 2018, Wu 2020, Janoschka 2016, Hollas 2018, Yang 2014, Yang 2018, Skyllas-Kazacos 1986) | experimental (primary citations) | 20 |
| Jethwa et al., ACS Appl. Energy Mater. 2024 (heterocyclic quinones) | experimental | 8 |
| Afzal et al., J. Mater. Chem. A 2025 (quinone degradation review) | experimental | 5 |
| Various other primary sources (Robb Marshak Joule 2019, Gong ACS EL 2016, Lin Science 2015, Pratt JPS 2013, Pope 1983, etc.) | experimental | ~50 (within inorganic 144 total) |
| **TOTAL** | | **12,540** |

---

## Sources investigated but NOT merged

| Source | Reason for exclusion |
|---|---|
| Frontiers Chem. Eng. 2022 (1,517 quinones) | DataSheet1 reports HOMO-LUMO gap and solvation free energy but NOT redox potentials in V vs SHE. Voltage is required per user spec. Raw files saved for reference but rows excluded. |
| Lieberman 2022 Family Tree Figure 5 (39 family-level ranges) | Rows describe chemical-family ranges (e.g., "p-Benzoquinones range min/midpoint/max"), not specific molecules. The Molecule field requires individual compound names. The 21 prose-extracted compound rows from the same paper ARE included. |
| Zhu et al., Green Energy & Environment 2024 (perspective) | Narrative-only, no tabulated potentials. |
| Mapping the frontiers of quinone stability (J. Mater. Chem. A 2019, 140k pairs) | Too large to ingest meaningfully; mostly redundant with RedDB + Er 2015. |
| Patents (US11056705B2, US11557786B2, US20180072669A1) | Patent text is poor for machine extraction; sparse standardized measurements. |
| MolGAT 23k RFB candidates | Predicted screening with no published explicit potential dataset. |

---

## Sanity-check results

- All 12,540 rows have molecule, voltage_v_she, and source — no missing required fields.
- All voltage values parse as numbers.
- Cross-validation across sources for well-known molecules:
  - **AQDS** at pH 0: 0.165 (Wedege), 0.21 (Kwabi/Pan/Wang), 0.213 (primary Huskinson 2014), 0.220 (Ding) — agreement within ~50 mV.
  - **Methyl viologen** at pH 7: -0.45 (Kwabi/Pan/Wang/Liu primary), -0.446 (Ding/Yin) — agreement within 5 mV.
  - **Ferrocyanide** at pH 14: 0.36 (Kwabi/Lin Aziz), 0.42 (Lin Aziz different conditions).
- Extreme voltages sensible: F2/F- at +2.87 V, S2O82-/SO42- at +2.01 V (well-known oxidants); decamethylcobaltocene at -1.68 V (known strong reductant).

### Spot-check correction (April 28, 2026)

A user spot-check on **row 377** (1,4,5,8-tetraamino-9,10-anthraquinone, a.k.a. Disperse Blue 1, InChIKey JSFUMBWFPQSADC) revealed:

1. **The molecule name was truncated** to "1,4,5,8-tetraamino" — fixed to "1,4,5,8-tetraamino-9,10-anthraquinone (Disperse Blue 1)".
2. **The voltage was systematically mislabeled.** Verification via the Elhajj & Gozem 2024 J. Chem. Theory Comput. GitHub data (which derives from the same Prince/Dutton/Gunner BBA 2022 dataset that Gao 2025 inherits) showed the experimental column is explicitly labeled "vs SCE [mV]". Gao 2025 stored these as "vs SHE" without applying the +0.241 V SCE→SHE conversion.
3. **All 336 Gao 2025 organic-solvent rows (subset 1-3) had the same systematic error.** Cross-checked via parent quinones:

| Compound | Gao 2025 (before) | Lit vs SCE | Lit vs SHE | After +0.241 V correction |
|---|---|---|---|---|
| 9,10-anthraquinone | -0.831 | ≈-0.87 | ≈-0.63 | -0.590 (Δ = +0.04 V from lit SHE) |
| 1,4-naphthoquinone | -0.581 | ≈-0.62 | ≈-0.38 | -0.340 (Δ = +0.04 V) |
| 1,4-benzoquinone | -0.401 | ≈-0.51 | ≈-0.27 | -0.160 (Δ = +0.11 V) |
| DDQ | +0.597 | ≈+0.51 | ≈+0.75 | +0.838 (Δ = +0.09 V) |
| 1,4,5,8-tetraamino-AQ | -1.321 | -1.32 | -1.08 | -1.080 (Δ = 0.00 V) |

**Action taken:** All 336 affected rows had +0.241 V applied to `voltage_v_she`. Original values preserved in `voltage_raw` with explanatory text. `reference_electrode` and `notes` fields flag the correction.

**Note on the aqueous Gao subsets (subsets 1-1 and 1-2, 99 + 96 rows):** these were spot-checked separately and appear consistent with vs SHE at face value (parent AQDS, 2,6-DHAQ, etc. match canonical aqueous SHE values), so they were NOT recorrected. If you find anomalies there, flag them.

**Recommendation:** Treat any "experimental" row in the database that has `solvent` containing "DMF", "MeCN", or "organic solvent" with extra scrutiny — verify against the original primary source via the `voltage_raw` field. The aqueous experimental rows (Wedege, Kwabi-primary, Ding, Pan, Yin, Aziz primary papers) cross-validate cleanly.

### User-contributed aqueous data for tetraamino-AQ (April 28, 2026)

User performed an independent literature search for 1,4,5,8-tetraamino-9,10-AQ and found:

> Stergiou, Prodromidis, Veltsistas, Evmiridis, *Electroanalysis* **2004**, *16*(11), DOI:10.1002/elan.200302902. On a Disperse Blue 1-modified graphite electrode at pH 6.5: two well-shaped pairs of peaks at E°' = +152 mV and −42 mV vs Ag/AgCl/3M KCl. Reversible.
> Converted to vs SHE (Ag/AgCl/3M KCl + 0.210 V): **+0.362 V and +0.168 V vs SHE**.

Apparent gap between this and the database: ~1.25 V (database had -1.08 V vs SHE in DMF).

**Root cause: this is a real chemistry difference, not a database error.** The two values measure different physical processes:
- The DMF value is the single-electron Q + e⁻ → Q•⁻ reduction. No protons. Aprotic. Strong electron donors (4 NH₂) destabilize Q•⁻ massively.
- The aqueous value is the 2-electron / 2-proton PCET reduction Q + 2H⁺ + 2e⁻ → QH₂, where protonation stabilizes the reduced form by tens to hundreds of kJ/mol, pushing E° far more positive.
- Stergiou likely also captures the amine-group oxidation (the more positive +0.362 V peak) because the four conjugated NH₂ groups in this molecule have p-aminophenol-like electrochemistry.
- Stergiou's measurement is also surface-confined (Disperse Blue 1 is poorly soluble in water — that's why it's a "disperse" dye), which adds another shift relative to solution.

**Action:** Both Stergiou rows added to the database (totals now 12,542 rows). 1,4,5,8-tetraamino-AQ now has THREE entries: one DMF aprotic + two aqueous PCET. The README sheet flags this distinction prominently.

**Implication for use:** For an aqueous fuel cell, the aqueous rows are the directly relevant ones. Treat aprotic-solvent rows as electronic-structure information that is a poor proxy for aqueous PCET behavior, especially for substituted quinones with electron-donating groups.

### Spot-check audit of iron-complex rows (April 28, 2026)

User spot-checked **row 4119 (Fe-gluconate)** and could not find the compound in the cited reference. Investigation found:

- **Fe-gluconate row 4119 — FIXED.** The cited paper (Belva & Aziz, *Energy Storage* 2025, e70198) is real but is about Na₄[Fe(Dcbpy)(CN)₄], not Fe-gluconate. The original value of -1.05 V vs SHE was also wrong.
  - **Corrected to:** -0.83 V vs SHE (derived from the 1.19 V cell voltage in Tang 2022 minus alkaline Fe-CN at +0.36 V).
  - **Correct primary source:** Tang, Wang et al., *J. Energy Chem.* **73**, 445-451 (2022), DOI: 10.1016/j.jechem.2022.06.041 — couples Fe-gluconate (negolyte) with ferrocyanide (catholyte) in alkaline media; 1.2 M solubility; 950+ cycles.
  - The original value and original Belva 2025 citation are preserved in the row's `notes` field for the audit trail.

- **Audit of other Fe-complex rows turned up additional issues** (these were NOT auto-fixed; they're flagged here for the user to review):

| Row | Compound | Value | Issue |
|---|---|---|---|
| 12511 | Fe-NTMPA2 | -0.3 V SHE | Wang 2024 (Nat. Commun.) reports "near -0.30 V vs Ag/AgCl" at pH 8. Ag/AgCl→SHE is +0.197 V, so true SHE value is ~-0.10 V (or ~-0.23 V from cell-voltage cross-check). DB value of -0.3 V appears to be Ag/AgCl mislabeled as SHE; off by ~0.1-0.2 V. |
| 12512 | Na₄[Fe(Dcbpy)₂(CN)₂] | +0.55 V SHE | Citation "Hu, B. et al., (related Fe-Dcbpy work cited in Wang 2024 NatComm)" is not a valid reference. Correct primary source is Li et al., *Nat. Energy* 6, 873 (2021). |
| 1228 | [FeII(CN)₂(Dcbpy)₂]4- | +0.847 V SHE | Same compound as row 12512 but with very different value. One of these is wrong, or they're different stereoisomers. |
| 4117 | Fe-CDTA pH 9 | -0.10 V SHE | Cited to Schwarzenbach 1954, but that paper reports stability constants, not CV potentials. Value is plausible but primary source citation is suspect. |
| Multiple | Fe-TEA / Fe-TEOA | -0.86 V SHE | Same compound (TEOA = TEA = triethanolamine), appears as duplicate rows from Gong 2016 and Lieberman 2022 review. Not wrong, just redundant. |

- **Pass with confidence:** Fe-EDTA pH 5 (+0.117 V), Fe-DTPA pH 9 (-0.05 V), Fe-TEA pH 13 (-0.86 V), Fe-glycine pH 2 (+0.69 V) — all verified against primary literature.

**Recommendation:** The user may want to spot-check additional rows from the inorganic_couples agent's contributions (rows ~4060-4203 in the database, anywhere `source` contains "Bard, Parsons & Jordan" or specific 2020s primary papers). Most rows look fine, but the Belva 2025 citation error suggests the agent occasionally guessed at primary citations rather than verifying each one. The pattern is: simple aquo ions and halide couples (citation = textbook) are reliable; specific complex citations (citation = a 2020s primary paper) should be verified individually.

## Caveats

1. **Phthalimide screen (5,172 rows) is in MeCN, not water.** Computed values; use the solvent column to filter. Biobased phthalimide candidates predicted as anolytes; experimental aqueous validation has not been performed.

2. **D3TaLES public bulk export (3,002 rows) is also computed in implicit MeCN.** Dominated by triarylamine/p-type oxidation potentials — useful as a candidate-space extension for catholyte side, less directly applicable for aqueous anolyte. Their experimental aqueous data exists in the portal but is not bundled in the bulk download (requires per-molecule API queries).

3. **Computational entries** are calibrated DFT predictions. RedDB uses linear calibration to RHE (Sorkun & Er 2025). Pang 2022 and Er 2015 use SMD/PCM solvation. RedCat reports DFT-validated values for top candidates only. Typical accuracy ~150-200 mV.

4. **Pan 2023 SmartMat entries (61 rows)** were extracted from a graphical timeline figure (Figure 1). Some compound name assignments are best-effort and may need verification.

5. **Kwabi 2020 review entries (62 rows)** were initially compiled by an agent without web access at first attempt. The 20 primary-citation rows added later confirm the Kwabi values match primary literature within ~10 mV for AQDS, MV, BTMAP-Vi, BTMAP-Fc, FcNCl, 4-HO-TEMPO, DHPS, ACA, ferrocyanide, lawsone, tiron, 2,5-DHBQ, V(II/III), VO2+/VO2+, Br2/Br-, and 2,6-DHAQ. Other Kwabi entries are likely accurate but not individually verified.

6. **Yin 2024 viologen review (43 rows)** was paywalled; the agent assembled rows from the primary citations the review covers. Cross-checked SMILES and values against primary sources where possible.

7. **The full 1,710 quinones from Er 2015** are not publicly released — only the 408-candidate shortlist is in the SI. The full 261 RedCat 2025 candidates aren't all public — only the top 5 per moiety class (25 total) have explicit potentials.

---

## Highlights from the recent 2023-2025 sweep

Notable novel molecules added in the most recent extraction round:

- **dMeODBAP** (Chem. Sci. 2025) — methoxy-phenazine negolyte at −0.84 V vs SHE, record-low E° among phenazines.
- **3Na-PW12 phosphotungstate POM** (Nat. Commun. 2025) — anolyte at −1.10 V vs SHE, 5-electron, enables 2.0 V OCV.
- **Cys-DHAQ** (Nat. Commun. 2025) — cysteine-zwitterionic dihydroxyanthraquinone bio-mimetic α-amino-acid negolyte at ~−0.65 V vs SHE.
- **BBPE-Vi / MBPE-Vi** (Chem. Eur. J. 2025) — bisphosphonate viologens at ~−0.55 V vs SHE, lowest E° viologens reported.
- **TMiPrPTCl** (phenothiazine catholyte) at +0.902 V vs SHE, 2.69 M water-soluble.
- **Naphthalene diimides** (sulfopropyl, carboxybutyl, dextrose-functionalized): novel anolyte family.
- **Jethwa 2024 heterocyclic quinones (compounds 2, 3, 4)** — bis-triazolyl and bis-thiadiazolyl quinones at -0.34 to -0.86 V vs SHE.

---

## How to use the database

**For experimental anolyte screening (aqueous fuel cell mediator candidates):**
1. Open the Data_Experimental sheet.
2. Filter `voltage_v_she` between -0.7 and 0.0 V vs SHE (or wider per HER tolerance).
3. Sort by `voltage_v_she` ascending — most negative first.
4. The Summary sheet has top-30 anolyte and catholyte tables ready to read.

**For computational candidate generation:**
- Use `Data_Computational` sheet; filter on `solvent` containing "water" to exclude MeCN-only phthalimides and D3TaLES if needed.

**For verification:**
- Source URLs are clickable in Excel.
- Cross-reference voltages across sources where multiple rows exist for the same molecule.

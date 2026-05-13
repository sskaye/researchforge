# Redox Mediator Database — Aqueous Fuel Cell Candidates

Built using the `redox-extraction` skill protocol (evidence-locked, verbatim provenance per row, programmatic sanity checks, independent verification on a sample).

## File: `redox_mediators.csv`

**1,960 rows** spanning candidate redox mediators, anolytes, catholytes, and redox-targeting mediators for aqueous fuel cells. Schema follows the redox-extraction protocol: each row carries DOI provenance, a verbatim `evidence_quote` from the source, and the conversion arithmetic when units/electrodes were converted.

### Voltage coverage (V vs SHE)

| Range            | Rows | Comment |
|------------------|-----:|---------|
| < −2.0           |  357 | D3TaLES reduction-column rows; conversion under review (see Caveats) |
| −2.0 to −1.5     |   91 | Phthalimides (Moraes 2026), some D3TaLES |
| −1.5 to −1.0     |  198 | Deep-anolyte candidates the user requested; phthalimides, some quinones, viologen second-reduction (MV⁺•/MV⁰) |
| −1.0 to −0.5     |  482 | Heart of the deep-anolyte regime; aza-aromatic anolytes (alloxazines, phenazines), DHAQ family, RedDB / Pang / Er computational hits |
| −0.5 to 0        |  179 | Standard anolyte regime; classic AQDS / viologen first-reduction, V³⁺/V²⁺ |
| 0 to +0.5        |  144 | Mid-range; bromine-free aqueous catholytes |
| +0.5 to +1.0     |  105 | Catholyte regime; ferrocyanide, TEMPO derivatives, Fe³⁺/Fe²⁺ |
| +1.0 to +1.5     |   95 | High-potential catholytes; Br₂/Br⁻, VO₂⁺/VO²⁺, O₂/H₂O |
| > +1.5           |  309 | Very high; computational tail of D3TaLES oxidation, Mn³⁺/Mn²⁺, Ce⁴⁺/Ce³⁺ |

### Tier breakdown (`verification_status`)

| Tier                       | Rows | Notes |
|----------------------------|-----:|-------|
| `verified_textbook`        |   32 | CRC Handbook 102nd ed., Bard/Parsons/Jordan IUPAC, Pavlishchuk-Addison, Bird-Kuhn — anchor couples |
| `verified_extraction`      |   14 | Phase-4 independently verified against source PDFs by a separate agent (sample stratified across Wedege 2016, Kwabi 2020, Molecules 2022, Afzal 2025) |
| `pending_verification`     |  171 | Experimental rows from primary papers / reviews; verbatim quotes locked, ready for further Phase-4 sweeps |
| `unverified_computational` | 1,179 | Bulk DFT/ML predictions from RedDB (757), Pang aza-aromatic (76), Er-Cheng quinone (82), Moraes phthalimide (158), and D3TaLES oxidation (106). ±150–200 mV typical accuracy. |
| `flagged_review`           |  564 | D3TaLES reduction-column rows — see Caveat 1 below |

### Sources covered

| Source | DOI | Rows | Type |
|---|---|---:|---|
| RedDB (Sorkun et al. 2022) | 10.1038/s41597-022-01832-2 | 757 | computational |
| D3TaLES (Bhat et al. 2023) | 10.1039/D3DD00081H | 670 | computational |
| Moraes et al. 2026 phthalimide screen | 10.1021/acs.joc.5c02047 | 158 | computational |
| Wedege et al. 2016 | 10.1038/srep39101 | 88 | experimental |
| Er / Cheng / Aspuru-Guzik 2015 quinone screen | 10.1039/C4SC03030C | 82 | computational |
| Pang / Vlachos 2022 aza-aromatic screen | 10.1039/D2TA05674G | 76 | computational |
| Kwabi / Ji / Aziz 2020 critical review | 10.1021/acs.chemrev.9b00599 | 69 | experimental (review-cited) |
| CRC Handbook 102nd ed. textbook anchors | textbook | 26 | experimental |
| Family-tree review (Fischer 2022) | 10.3390/molecules27020560 | 21 | experimental (review-cited) |
| Afzal 2025 quinone degradation review | 10.1039/D5TA03034J | 7 | experimental (review-cited) |
| Bird & Kuhn viologen review (1981) | 10.1039/CS9811000049 | 2 | experimental |
| Bard / Parsons / Jordan IUPAC textbook | textbook | 2 | experimental |
| Pavlishchuk & Addison Fc/Fc⁺ ref | 10.1016/S0020-1693(99)00407-7 | 1 | experimental |
| Pope / Stille nitroxide review | textbook | 1 | experimental |

## Caveats — read before using

1. **D3TaLES reduction column (564 rows, `flagged_review`).** The protocol's documented "subtract-form" conversion (E_SHE = 4.42 V − E_raw) was applied to D3TaLES's `solv_reduction_potential` column, but it produces 9,10-anthraquinone at −3.41 V vs SHE (literature value ≈ −0.44 V vs SHE). The conversion is likely wrong for the reduction column — D3TaLES may store this quantity on a different scale (vacuum-referenced including additional energy terms, or the second/third reduction rather than the first). The 564 affected rows are tagged `flagged_review` with `flagged_conversion_arithmetic_error` in notes. Use them for chemical-space topology only until the conversion convention is confirmed against D3TaLES documentation. The 106 D3TaLES *oxidation* rows agree well with literature (TEMPO, DBMMB, anthracene all within 100–150 mV) and remain `unverified_computational`.

2. **Two paywalled sources skipped.** Pan SmartMat 2023 (10.1002/smm2.1198) and Yin / Liu viologen review J. Mater. Chem. A 2024 (10.1039/D4TA00753K) were behind Cloudflare/RSC paywalls during extraction. They likely contain ~30–80 additional viologen and TEMPO rows. If you can fetch them through institutional access, you can extend the database from there.

3. **Computational rows have ±150–200 mV typical accuracy.** RedDB and D3TaLES were spot-checked against canonical molecules (phenazine, substituted AQs, ferrocene, TEMPO) — RedDB systematically reports values ~200–300 mV more positive than experiment for 2H⁺/2e⁻ couples (consistent with uncalibrated PBE/LACVP+ DFT). This is expected behavior for `unverified_computational` rows and is documented in row notes.

4. **Class-range "voltage out of range" flags (5 rows).** Five rows triggered the chemistry-class voltage-range sanity check — all reflect either Pourbaix shifts (phenazine at pH 0 has a 2H⁺/2e⁻ shift up to +0.4 V, expected behavior) or class-detection conservatism (sulfonated ferrocenes can be 100–200 mV higher than parent ferrocene). Values match the source verbatim; no extraction error.

5. **Cross-source spread (3 rows).** Methyl viologen MV⁺•/MV⁰ shows ~180 mV spread between Bird-Kuhn 1981 textbook (−0.880 V) and Kwabi 2020 (−0.700 V) — both values are real and reflect electrolyte differences (KCl vs phosphate buffer) and different couples being measured. The protocol records the spread rather than picking one.

## Top deep-anolyte candidates (E° < −0.7 V vs SHE)

The user expressed particular interest in candidates between −0.9 and −1.5 V. The strongest leads in the database for that window:

- **DHPS** (7,8-dihydroxy-phenazine sulfonate): E°′ = −0.81 V at pH 14 (Kwabi 2020)
- **Quinoxaline**: E°′ = −0.78 V at pH 14 (Kwabi 2020)
- **Methyl viologen MV⁺•/MV⁰** second couple: E°′ ≈ −0.78 to −0.88 V at pH 7 (Bird/Kuhn 1981, Kwabi 2020)
- **N-substituted phthalimides** (Moraes 2026): 158 candidates, predicted E° spanning −0.70 to −1.82 V vs SHE in MeCN — these would shift more positive in water and need experimental confirmation
- **2,6-DHAQ in alkaline**: E°′ = −0.701 V at pH 13 (Wedege 2016, verified)
- **Aza-aromatic predictions** (Pang 2022, 76 rows): the deepest predicted anolytes are at E° ≈ −0.82 V vs SHE
- **Zn(OH)₄²⁻/Zn alkaline**: E° = −1.199 V (CRC textbook)
- **Various metal couples** (V²⁺/V, Cr²⁺/Cr, Mn²⁺/Mn, Al³⁺/Al, Ti³⁺/Ti²⁺): textbook anchors below −0.9 V; not practical for aqueous fuel cells due to HER kinetics but useful as scale anchors

Many additional bulk-computational candidates from RedDB, Pang, Moraes are flagged with `notes` describing their predicted scaffold. Filter `redox_mediators.csv` by `voltage_v_she` to surface them.

## How to use the database

```bash
# Filter by voltage range (e.g., target deep anolyte regime)
python3 -c "
import csv
with open('redox_mediators.csv') as f:
    for r in csv.DictReader(f):
        try:
            v = float(r['voltage_v_she'])
        except: continue
        if -1.5 <= v <= -0.9 and r['data_type'] == 'experimental':
            print(r['molecule'], r['voltage_v_she'], r['source'])
"

# Filter by tier (e.g., only verified rows)
# verification_status in {'verified_textbook', 'verified_extraction'}
```

## Re-running sanity checks

```bash
python3 /var/folders/n1/n9588ctd6c715_wlm89c534m0000gn/T/claude-hostloop-plugins/e0ad1e2f473d8162/skills/redox-extraction/scripts/run_all_checks.py redox_mediators.csv --check-dois
```

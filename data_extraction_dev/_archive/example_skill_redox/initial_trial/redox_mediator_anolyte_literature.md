# Redox Mediators & Anolytes for Flow Batteries — Literature with Large Compound Tables

A curated set of literature reviews, benchmark papers, and computational databases that contain large tables of redox-active compounds with voltage and stability information. Organized by table size and data type.

---

## 1. Large computational databases (thousands+ of compounds)

### RedDB — Sanyal et al., *Scientific Data* (2022)
- **Size:** 31,618 molecules (quinones + aza-aromatics)
- **Properties:** DFT-derived redox potentials, HOMO/LUMO, ML-predicted aqueous solubility, multiple battery-relevant descriptors
- **Notes:** The largest dedicated RFB database. Open data, FAIR-formatted, downloadable.
- **Link:** https://www.nature.com/articles/s41597-022-01832-2

### SOMAS — Sorkun et al.
- **Size:** 11,696 organic compounds
- **Properties:** Experimental aqueous solubility + eight DFT-derived quantum descriptors per molecule
- **Notes:** Solubility-focused but explicitly built for RFB screening; complements RedDB.
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9715657/

### MolGAT — ACS Omega (2023)
- **Size:** 581,014 molecules screened (OMDB, QM9, ZINC, CHEMBL, DELANEY) → 23,467 RFB candidates
- **Properties:** Graph-neural-network predicted redox activity
- **Notes:** Useful as a pre-filtered "RFB-relevant" subset of the major public chemical databases.
- **Link:** https://pubs.acs.org/doi/10.1021/acsomega.3c01295

### All-quinone HT screen — Er et al.
- **Size:** ~33,000 DFT simulations across a virtual quinone library
- **Properties:** Predicted E°, solvation free energies (ΔG⁰_solv as solubility proxy)
- **Notes:** Older but well-cited; quinone chemistry only.
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5811157/

### Phthalimide screen — Moraes et al., *J. Org. Chem.* (2026)
- **Size:** 5,705 phthalimide derivatives, including biobased subset
- **Properties:** DFT-screened reduction potentials and stability descriptors
- **Notes:** Anolyte-focused (low reduction potentials). Useful for non-quinone anolyte design.
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12814552/

---

## 2. Experimental review / benchmark papers with curated tables

### Wedege et al., *Sci. Reports* (2016) — "Organic Redox Species in Aqueous Flow Batteries"
- **Size:** 33 mostly quinone-based compounds
- **Properties:** pH-dependent redox potential, solubility, chemical stability; single-cell RFB tests on selected pairs
- **Notes:** The classic experimental compilation. Probably the single most-cited "E°/S/stability table" paper in the AORFB field.
- **Link:** https://www.nature.com/articles/srep39101

### Emmel et al., *Nat. Commun.* (2023) — "Benchmarking organic active materials…lifetime and cost"
- **Size:** 38 organic active materials + vanadium reference
- **Properties:** Capacity-fade rates, projected lifetimes, capital cost models
- **Notes:** Underlying tool released as **ReFlowLab** (Zenodo DOI: 10.5281/ZENODO.8363030) — a structured dataset you can query directly.
- **Link:** https://www.nature.com/articles/s41467-023-42450-9

### "Family Tree for Aqueous Organic Redox Couples" — Lieberman et al., *Molecules* (2022)
- **Properties:** Comparative tables of E°, solubility, demonstrated cycle life, organized by chemical family
- **Notes:** Conceptual review; functions as a navigational map of the AORFB literature.
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8778144/

### Pan et al., *SmartMat* (2023)
- **Properties:** Tables for viologens, TEMPOs, phenazines, anthraquinones — potential, solubility, capacity retention, cycle data
- **Notes:** Strong on molecular-engineering strategies (functional-group effects on E°, S, stability).
- **Link:** https://onlinelibrary.wiley.com/doi/full/10.1002/smm2.1198

### "Status and Prospects of Organic Redox Flow Batteries" — *ACS Energy Lett.* (2019)
- **Properties:** Comprehensive performance tables broken out by anolyte vs. catholyte
- **Notes:** From the Kwabi/Aziz lineage; strong on side-reaction / capacity-fade mechanisms.
- **Link:** https://pubs.acs.org/doi/10.1021/acsenergylett.9b01332

---

## 3. Class-specific reviews (tighter, deeper tables)

### Heterocyclic quinones — Robertson et al., *ACS* (2024)
- **Scope:** Pyridoquinones, naphthoquinones, fused-ring heterocyclic quinones beyond standard AQs
- **Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10806605/

### Organic electroactive molecules (aqueous + non-aqueous) — Ding et al., *Front. Chem.* (2020)
- **Scope:** Both aqueous and non-aqueous systems; useful if anolyte work spans both regimes
- **Link:** https://www.frontiersin.org/journals/chemistry/articles/10.3389/fchem.2020.00451/full

---

## Recommended starting points

| Goal | Pair to use |
|---|---|
| Broadest computational coverage | **RedDB** (31k molecules) |
| Experimentally validated reference | **Wedege 2016** (33 compounds, pH-dependent) |
| Cost & lifetime axis | **Emmel 2023 + ReFlowLab repo** (38 materials) |
| Solubility-focused screening | **SOMAS** (11.7k compounds) |
| Anolyte-only design | **Phthalimide screen** (5,705) + **RedDB aza-aromatics subset** |

**Suggested workflow:** RedDB to filter ~30k computed candidates by E° and predicted solubility → Wedege 2016 to anchor/calibrate against experimental data → Emmel 2023 (via ReFlowLab) to overlay cost and lifetime constraints.

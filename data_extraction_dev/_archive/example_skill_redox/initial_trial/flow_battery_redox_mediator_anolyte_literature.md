# Literature Sources for Redox Mediators and Anolytes in Flow Batteries

**Focus:** literature reviews, journal articles, and databases that contain large tables or datasets of redox mediators, anolytes, or related organic redox-active compounds for flow batteries, especially sources with **redox voltage** and **stability** information.

**Prepared:** April 28, 2026

---

## Executive Summary

The best sources divide into two broad categories:

1. **Large computational databases and high-throughput screens**  
   These contain thousands to millions of compounds and usually provide computed or predicted redox potentials, solubility, and stability proxies.

2. **Experimental review and benchmarking papers**  
   These contain fewer compounds but are more likely to report cycling behavior, capacity fade, chemical stability, solubility, reference electrodes, pH, and full-cell performance.

For **large searchable tables**, start with **RedCat**, **D3TaLES**, **RedDB**, the **quinone stability frontier** paper, and the **aza-aromatic high-throughput anolyte screen**. For **experimental voltage and degradation**, start with **Wedege 2016**, **Kwabi 2020**, **Gao 2025**, and **Fell & Aziz 2023**.

---

## Best Matches: Large Compound Databases and High-Throughput Screens

| Source | Size / Scope | Voltage Information | Stability Information | Why It Is Useful |
|---|---:|---|---|---|
| [**RedCat: automated discovery workflow for aqueous organic electrolytes**](https://pubs.rsc.org/en/content/articlehtml/2025/dd/d5dd00111k), *Digital Discovery*, 2025 | Screens **112 million PubChem molecules** and reports **261 promising anolyte candidates** | Reaction-energy proxy for redox potential, followed by DFT validation for selected molecules | Molecular-dynamics structural stability filtering; not equivalent to measured cycling fade | Probably the most directly relevant new anolyte-discovery paper/database for aqueous organics. It explicitly targets low-cost, soluble, stable anolytes. |
| [**D3TaLES: data infrastructure for non-aqueous redox flow battery redox-active molecules**](https://pubs.rsc.org/en/content/articlehtml/2023/dd/d3dd00081h), *Digital Discovery*, 2023 | **43,168 redox-active organic molecules**, with web/API access | Oxidation and reduction profiles; redox potential calculators | Includes stability-related quantities such as radical-cation stability scores | Best option for a large searchable/API-accessible **non-aqueous** redox-mediator/electrolyte dataset. |
| [**RedDB: computational database for aqueous redox flow battery molecules**](https://www.nature.com/articles/s41597-022-01832-2), *Scientific Data*, 2022 | **31,618 molecules**, including quinones and aza-aromatics; downloadable CSV/XLSX via Harvard Dataverse | Reaction/property tables from quantum chemistry; useful for estimating redox behavior | Thermodynamic/electronic descriptors and solubility predictions; not direct long-term fade data | One of the best starting points for a downloadable aqueous organic RFB dataset. The paper describes 15 database tables and 15,882 redox reactions. |
| [**Mapping the frontiers of quinone stability in aqueous media**](https://pubs.rsc.org/en/content/articlehtml/2019/ta/c9ta03219c), *Journal of Materials Chemistry A*, 2019 | About **140,000 quinone pairs** and over **1 million calculations** | Reduction-potential relationships for quinones | Explicit computational decomposition/stability analysis, especially water-addition instability | A must-use source if the target space includes quinone anolytes/catholytes and both voltage and chemical degradation matter. |
| [**Discovery of aza-aromatic anolytes for aqueous redox flow batteries via high-throughput screening**](https://pubs.rsc.org/en/content/articlelanding/2022/ta/d2ta05674g), *Journal of Materials Chemistry A*, 2022 | **13,406 aza-aromatic redox pairs** based on alloxazine, phenazine, and indigo scaffolds | Predicted redox potentials | Decomposition likelihood from hydration/tautomerization analysis | Very relevant for aqueous anolytes: screens for low redox potential, solubility, and decomposition resistance, then identifies **516 anolyte candidates**. |
| [**Computational design of molecules for an all-quinone redox flow battery**](https://pubs.rsc.org/en/content/articlehtml/2015/sc/c4sc03030c), *Chemical Science*, 2015 | **1,710 quinone/hydroquinone redox couples** | Computed redox potentials / redox tuning | Mainly solvation and design descriptors, not a deep degradation dataset | Older but foundational high-throughput quinone table; useful as a clean voltage/structure dataset. |
| [**Machine learning for redox-potential prediction of molecules in organic redox flow batteries**](https://www.sciencedirect.com/science/article/pii/S0378775324019876), *Journal of Power Sources*, 2025 | Experimental database with **more than 500 redox-potential measurements** | Experimental redox potentials with pH, solvent, molecule identifiers, and references | Mostly voltage-focused; limited direct stability information | Best hit for an experimental redox-potential table spanning aqueous and organic solvents. Pair it with a stability/fade review. |
| [**Multi-objective optimization of stable organic radicals for aqueous redox flow batteries**](https://www.nature.com/articles/s42256-022-00506-3), *Nature Machine Intelligence*, 2022 | ML workflow trained with nearly **100,000 quantum-chemistry simulations** | Predicts oxidation/reduction potentials | Optimizes radical persistence/stability and synthesizability | Useful if considering organic radical mediators or radical-type anolytes, though it is more of a design/optimization dataset than a conventional review table. |

---

## Best Sources for Experimental Stability, Fade, and Benchmark Tables

| Source | Size / Scope | What to Extract |
|---|---:|---|
| [**Organic redox species in aqueous flow batteries: redox potentials, chemical stability and solubility**](https://www.nature.com/articles/srep39101), Wedege et al., *Scientific Reports*, 2016 | **33 mainly quinone-based compounds** | Excellent compact table source: pH-dependent redox potentials, solubility, chemical stability, and selected RFB tests. |
| [**Electrolyte lifetime in aqueous organic redox flow batteries: a critical review**](https://www.osti.gov/biblio/1799071), Kwabi, Ji & Aziz, *Chemical Reviews*, 2020 | Review across quinones, viologens, aza-aromatics, metal complexes, nitroxides | Probably the best review for capacity-fade rates, lifetime, degradation mechanisms, demonstrated concentrations, and redox potentials across known aqueous organic systems. |
| [**Benchmarking organic active materials for aqueous redox flow batteries in terms of lifetime and cost**](https://www.nature.com/articles/s41467-023-42450-9.pdf), *Nature Communications*, 2023 | **38 organic active materials** plus vanadium benchmark | Useful comparative table/model for lifetime-cost tradeoffs; the associated ReFlowLab tool is intended for updating benchmark comparisons. |
| [**High-throughput electrochemical characterization of aqueous organic redox flow battery active material**](https://www.osti.gov/biblio/2008379), Fell & Aziz, *Journal of The Electrochemical Society*, 2023 | Common aqueous organic negolytes; over **50 flow-cell experiments** | Strong source for practical cycling/fade-rate benchmarking methodology and measured behavior, rather than just CV potentials. |
| [**Molecular engineering of organic electroactive materials for redox flow batteries**](https://pubs.rsc.org/en/content/articlelanding/2018/cs/c7cs00569e), Ding et al., *Chemical Society Reviews*, 2018 | Broad review by molecular family | Contains large review tables; for example, Table 6 summarizes solubility and redox potentials of carbonyl compounds, and Table 9 covers polymeric active materials. |

---

## Redox-Mediated / Redox-Targeting Flow Battery Reviews

These are especially relevant if **redox mediators** means mediators for **solid boosters**, **solid-liquid redox targeting**, or mediated charge/discharge of solid storage materials, rather than simply soluble active materials.

| Source | Usefulness |
|---|---|
| [**Aqueous organic and redox-mediated redox flow batteries: a review**](https://www.sciencedirect.com/science/article/pii/S245191032030003X), Gentil, Reynard & Girault, *Current Opinion in Electrochemistry*, 2020 | Good entry point for aqueous organic RFBs plus redox-mediated/solid-booster systems; useful for identifying mediator families and representative systems, but not a giant compound database. |
| [**Material selection and system optimization for redox flow batteries based on solid-liquid redox-targeting reactions**](https://www.sciencedirect.com/science/article/pii/S2352152X24046000), 2024 mini-review | Useful for mediator-selection principles in redox-targeting systems: mediator potential matching, solubility, stability, and system constraints. |
| [**Beyond conventional batteries: semi-solid and redox-targeting flow batteries -- LiFePO4 case study**](https://www.osti.gov/biblio/2482275), *Sustainable Energy & Fuels*, 2024 | Good for redox-targeting context and design constraints, especially where the mediator couples to solid storage materials. |

---

## Adjacent Database Worth Pairing with Redox Tables

| Source | Why It Matters |
|---|---|
| [**SOMAS: Solubility of Organic Molecules in Aqueous Solution**](https://www.nature.com/articles/s41597-022-01814-4), *Scientific Data*, 2022 | Not a voltage/stability database, but useful for filtering RFB candidates. It contains about **12,000 aqueous-solubility records** and descriptors, which pairs well with RedDB, D3TaLES, and RedCat voltage datasets. |

---

## Recommended Starting Order

### For aqueous anolytes

1. **RedCat**  
   Best for very large-scale anolyte discovery from PubChem.

2. **RedDB**  
   Best downloadable aqueous organic RFB dataset.

3. **Discovery of aza-aromatic anolytes via high-throughput screening**  
   Best focused screen for phenazine/alloxazine/indigo-type anolyte scaffolds.

4. **Mapping the frontiers of quinone stability in aqueous media**  
   Best large quinone-specific stability dataset.

### For experimental voltage and degradation

1. **Wedege et al. 2016**  
   Compact, experimentally grounded table with redox potential, solubility, and chemical stability.

2. **Kwabi, Ji & Aziz 2020**  
   Best broad review for electrolyte lifetime and degradation mechanisms in aqueous organic RFBs.

3. **Gao et al. 2025**  
   Useful experimental redox-potential database across solvents and conditions.

4. **Fell & Aziz 2023**  
   Strong practical source for flow-cell cycling and fade benchmarking.

### For non-aqueous redox mediators or active molecules

1. **D3TaLES**  
   Best large non-aqueous redox-active-molecule data infrastructure with searchable/API access.

### For redox-targeting mediators

1. **Gentil, Reynard & Girault 2020**  
   Best review entry point for aqueous organic and redox-mediated RFBs.

2. **Material selection and system optimization for redox-targeting reactions, 2024**  
   Useful for mediator selection rules and system constraints.

3. **Sustainable Energy & Fuels 2024 LiFePO4 redox-targeting case study**  
   Useful for understanding mediator-solid interactions and system-level design.

---

## Suggested Extraction Columns

When building a spreadsheet from these papers, keep computed and experimental stability fields separate. Suggested columns:

| Column | Notes |
|---|---|
| Compound name | Include common name and systematic name where available. |
| SMILES / InChI / CAS | Essential for deduplication across databases. |
| Molecular family | Quinone, phenazine, viologen, nitroxide, alloxazine, indigo, organometallic, radical, etc. |
| Battery role | Anolyte, catholyte, mediator, redox-targeting mediator, bifunctional, unknown. |
| Solvent / supporting electrolyte | Aqueous, non-aqueous, pH, salt, acid/base, concentration. |
| Redox potential | Preserve reported reference electrode. |
| Converted potential vs SHE or NHE | Add only after careful conversion. |
| Number of electrons | 1e-, 2e-, proton-coupled, multi-step, etc. |
| pH | Especially important for aqueous organic molecules. |
| Solubility | Include units and measurement conditions. |
| CV reversibility | Peak separation, reversibility description, diffusion behavior. |
| Chemical stability | Calendar stability, decomposition pathway, half-life, or qualitative descriptor. |
| Electrochemical stability | Cycling fade, Coulombic efficiency, voltage efficiency, energy efficiency. |
| Capacity fade rate | Preserve units: percent/day, percent/cycle, percent/hour, or mAh/L/day. |
| Computed stability metric | Radical stability, hydration energy, decomposition free energy, HOMO/LUMO, etc. |
| Experimental vs computed flag | Prevents mixing measurements with predictions. |
| Data source | Paper/database name, DOI/link, table/figure number. |
| Notes | Degradation mechanism, crossover comments, membrane compatibility, synthetic accessibility, cost. |

---

## Normalization Notes

Redox-potential tables require careful normalization because papers report values against different reference electrodes and under different conditions. For aqueous systems, pH is especially important because many organic redox couples are proton-coupled. For non-aqueous systems, solvent, supporting electrolyte, and reference calibration can strongly affect apparent potential.

Stability should not be collapsed into a single number unless the underlying metric is the same. In this literature, **stability** can mean any of the following:

- computed thermodynamic instability,
- predicted decomposition route,
- radical persistence,
- cyclic-voltammetry reversibility,
- calendar decomposition rate,
- full-cell capacity fade,
- membrane crossover resistance,
- air/water stability,
- or long-term cycling lifetime.

A useful database should therefore keep separate fields for **computed stability**, **chemical stability**, **electrochemical stability**, and **full-cell cycling stability**.

---

## Most Important Sources to Download First

1. RedDB dataset files from Harvard Dataverse, linked from the *Scientific Data* article.
2. D3TaLES data/API resources from the *Digital Discovery* paper.
3. Supporting information for the quinone stability frontier paper.
4. Supporting information for the aza-aromatic anolyte screening paper.
5. Tables and supplementary information from Wedege et al. 2016.
6. Tables and cited primary studies in Kwabi, Ji & Aziz 2020.
7. The experimental redox-potential database associated with Gao et al. 2025, if available through the article or supplementary information.


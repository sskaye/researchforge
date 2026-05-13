# Prior Work on Structured Data Extraction from Scientific Literature

A focused review of approaches, benchmarks, metrics, test sets, and reported performance for extracting structured data — numeric and categorical — from scientific papers. The intent is to make every design decision in the ResearchForge data-extraction skill traceable to evidence about what works and what fails.

---

## Contents

1. [Executive summary](#1-executive-summary)
2. [What makes scientific extraction hard](#2-what-makes-scientific-extraction-hard)
3. [Approaches tried, by generation](#3-approaches-tried-by-generation)
4. [Benchmarks and test sets](#4-benchmarks-and-test-sets)
5. [Metrics](#5-metrics)
6. [Performance comparison across benchmarks](#6-performance-comparison-across-benchmarks)
7. [Failure modes and what causes them](#7-failure-modes-and-what-causes-them)
8. [Verification, grounding, and reliability patterns](#8-verification-grounding-and-reliability-patterns)
9. [Domain case studies (materials, chemistry, polymers, batteries)](#9-domain-case-studies)
10. [Design implications for the ResearchForge extraction skill](#10-design-implications)
11. [Sources](#11-sources)

---

## 1. Executive summary

Three high-level findings drive the skill design.

**The state of the art is a multi-stage pipeline, not a single model call.** Every reproducibly successful system in the literature combines (a) a document-parsing front end that produces clean text, table structure, and figure references, with (b) an LLM-based extraction stage operating on that structured input, and (c) a verification stage that catches errors before they enter the dataset. Single-shot "ask GPT-4 to extract X" workflows underperform pipelines on every published benchmark we found.

**Frontier closed-source LLMs are now strong enough to be the extraction engine — but only inside a verification harness.** ChatExtract (Polak & Morgan, *Nature Communications* 2024) reaches ~90% precision/recall on materials data with GPT-4 *because* of follow-up verification prompts; without them, the same model is meaningfully worse. ChemDataExtractor 2.1's BERT-based NER (88–90% F1) is still competitive with much larger LLMs for narrow NER tasks at much lower cost. Multi-agent verification frameworks like SLM-MATRIX (92.85% on BulkModulus) and KARMA show further gains. The pattern is consistent: the model matters less than the harness around it.

**Tables are where most scientific data lives, and tables are where most extractors break.** 85% of compositions and properties in materials-science papers are reported only in tables (Gupta et al., *Communications Materials* 2024). Yet on OmniDocBench (CVPR 2025), even pipeline tools like MinerU and Mathpix outperform general VLMs on academic-paper tables, and frontier VLMs hit only ~30% on some structured visual reasoning tasks. Specialized parsers (Nougat, Mathpix, MinerU, Docling) substantially outperform general LLM/VLM approaches on table structure recognition. The skill must treat tables as a first-class input type with dedicated handling, not as text.

A key practical implication: the design space is well-mapped, and the right answer for ResearchForge is a *composed* system — domain-aware document parsing → structured chunking → schema-driven LLM extraction with verification → cell-level provenance — rather than novel research on any single component.

---

## 2. What makes scientific extraction hard

Five characteristics distinguish scientific data extraction from generic information extraction and explain why off-the-shelf approaches underperform.

**Heterogeneous data carriers.** Numeric and categorical data are distributed across body text, tables, figures, captions, supplementary information, and footnotes. Studies of polymer literature show that 85% of property data lives only in tables (Gupta et al., 2024); battery and synthesis papers heavily use experimental procedures that read more like recipes than prose. A skill that only reads body text will miss most of the data.

**Notation density and irregularity.** Subscripts, superscripts, Greek letters, units in non-standard forms (J g⁻¹ K⁻¹, mol/L, M, kPa·s), scientific notation, mixed formats (5.0(2) for value with uncertainty), and chemical formulas embedded in cell values. The Materials Science Tables study (Gupta et al., *IMMI* 2024) found accuracy on tables with long molecule names, hyphens, and sub/superscripts dropped to 46%.

**Implicit semantics.** A column header "Eg" in a semiconductor paper is the band gap; in a biology paper it is something else. "5.0" without a unit is meaningless. "—" in one paper means "not measured" and in another means "zero." The data is only as useful as the metadata around it, and that metadata is frequently buried in the surrounding paragraph or in the methods section.

**Quantitative reporting conventions.** Uncertainties are sometimes parenthetical (5.0(2) eV), sometimes explicit (5.0 ± 0.2 eV), sometimes one-sided, sometimes implicit ("≤ 5.0"). Detection limits and measurement floors are reported inconsistently. Derived quantities (ratios, normalized values) require parsing the formula or definition.

**Document-level reasoning is required.** SciREX (Allen AI) explicitly highlighted that the 4-ary tuple (Dataset, Metric, Task, Method) typically spans multiple sections. The same is true in the physical sciences: a measured value in a table requires the system, conditions, and method described elsewhere in the paper. A row's correctness is not local.

These are not edge cases; they are the modal case. Any extractor that handles only easy tables will fail on most real papers.

---

## 3. Approaches tried, by generation

### 3.1 Rule-based and dictionary-driven (pre-2018)

Domain-specific parsers using hand-crafted regex, dictionaries, and grammar rules. Examples: OPSIN (chemistry name → structure), early ChemDataExtractor releases. Strong precision on the narrow patterns they covered, near-zero recall on anything outside the rule set. Maintenance cost made these unscalable.

### 3.2 Domain-pretrained BERT and NER pipelines (2019–2022)

The dominant production approach for scientific extraction before LLMs hit. Domain-pretrained encoders fine-tuned for token-level NER, sometimes with downstream relation-extraction heads.

- **ChemDataExtractor** — toolkit for chemical entity, property, and relation extraction (Swain & Cole, 2016 and subsequent versions). v2.1's BERT-based single-model NER reached 89.7% F1 on CHEMDNER (organic) and 88.0% F1 on Matscholar (inorganic) simultaneously.
- **MaterialsBERT / MatSciBERT** — domain-pretrained BERT variants on materials science corpora. Used in the polymer general-purpose extraction pipeline (Gupta et al., *npj Computational Materials* 2023) that processed 2.4M articles, identified 681K polymer-relevant ones, and extracted >1M property records covering 24 properties of 106K unique polymers.
- **MatScholar** — Berkeley/LBNL materials science extraction system; trained NER for inorganic materials, sample descriptors, phase labels, properties, applications, synthesis and characterization methods.
- **BatteryBERT** — battery-domain pretrained model (Huang & Cole, *JCIM* 2022). Auto-generated a battery-materials database (*Scientific Data* 2020) using the ChemDataExtractor backbone.
- **ChemRxnExtractor / ChEMU** — reaction-specific NER with two-stage transformer pipelines: product extraction followed by reaction-role labeling, with the schema (reactants, type, catalyst, solvent, temperature, time, yield) treated as slots to fill.

Strengths: cheap inference, narrow tasks done well, good for high-volume mining over millions of papers. Weaknesses: every new schema or domain needed retraining, document-level reasoning was weak, table handling was an afterthought.

### 3.3 Document understanding models (2020–2023)

Models that jointly process text, layout, and visual signals — a different design from text-first NER.

- **LayoutLM (v1/v2/v3)** — joint text + 2-D layout + image embeddings; competitive on document classification and form understanding.
- **Donut** — OCR-free encoder-decoder (Swin encoder, BART decoder). Trained to read documents end-to-end as image-to-structured-text. Comparable accuracy to LayoutLM on classification with much lower inference cost on rendered documents.
- **TableNet, CascadeTabNet, TableFormer** — table-specific models; TableFormer is the table structure-recognition backbone of IBM's Docling.
- **Microsoft Table Transformer (TATR)** — released alongside PubTables-1M; targets detection + structure recognition jointly.

These are foundational components in modern pipelines (Docling, MinerU all use derivatives) rather than end-to-end extractors on their own.

### 3.4 Specialized scientific PDF parsers (2022–2025)

PDF → structured text with table, equation, and figure handling. Critical front-end for any modern extraction pipeline.

- **GROBID** — long-running tool for header, citation, and reference extraction; weaker on tables and equations.
- **Nougat (Meta, 2023)** — VLM ("Neural Optical Understanding for Academic Documents") trained on arXiv and PMC. Strong on math and academic paper structure. On OmniDocBench, scored 0.734–1.000 across metrics, well ahead of Marker (0.074–0.651) and Mathpix (0.131–0.690) on academic documents.
- **Marker (Datalab)** — open-source pipeline targeting markdown/JSON output; reported to benchmark favorably against Llamaparse and Mathpix on general documents.
- **Mathpix** — commercial, strong formula recognition (86.6% on formula extraction in OmniDocBench, comparable to GPT-4o at 86.8%).
- **MinerU (OpenDataLab)** — open-source pipeline for Chinese, scientific, and financial documents; 97.5 mAP on layout detection (top of OmniDocBench), excellent rotated-table handling. CUDA-accelerated 0.21 s/page on Nvidia L4.
- **Docling (IBM)** — open-source framework using DocLayNet for layout and TableFormer for table structure. Reported 97.9% accuracy on complex table extraction in a 2025 evaluation. CPU performance: 3.1 s/page on x86. Janurary 2025 OmniDocBench addition.

The key empirical finding from OmniDocBench (CVPR 2025): on academic papers, **pipeline tools beat general VLMs at table extraction** (MinerU edit ≈ 0.025 vs. general VLMs ≈ 0.146). General VLMs are more robust to visual noise but less precise on fine structure (cell borders, strict LaTeX).

### 3.5 LLM-based extraction with prompting (2023–present)

The current dominant approach for new extraction tasks. Several distinct patterns.

**Zero-shot prompting with structured outputs.** Provide the schema (JSON or otherwise), ask the LLM to fill it. Cleanlab's Structured Output Benchmark (2024) and the SOB benchmark (2025) measure this directly. Notable findings:
- JSON pass rates are very high (97%+ for most frontier models).
- Value accuracy lags 15–30 points behind: top model on SOB (Gemini 3.1-Pro) at 82.0%, GLM-5.1 at 80.6%, Qwen3.5-35B at 80.1%.
- The implication: the model usually produces *valid-looking* JSON, but the values inside are wrong far more often than the structure is.

**Few-shot prompting.** Adding 2–5 in-context examples lifts performance on narrow extraction tasks substantially; for materials data, few-shot can close most of the gap to fine-tuned models.

**ChatExtract (Polak & Morgan, *Nature Communications* 2024).** A specific prompting protocol that lifted GPT-4 to ~90% precision/recall on materials data extraction. The recipe:
1. First-pass identification of sentences that contain target data.
2. Structured extraction with explicit schema.
3. Follow-up verification turns: "Is this correct?", "Did you miss any?" — exploiting the conversational model's information retention.
4. Purposeful redundancy and uncertainty-introducing prompts.

The ChatExtract result is now widely cited as the canonical demonstration that *verification scaffolding matters more than model size* for this task class.

**LLM-NERRE (Dagdelen, Dunn et al., *Nature Communications* 2024).** Fine-tuned GPT-3 and Llama-2 for joint NER + relation extraction in materials science (dopants/host materials, MOFs, composition/phase/morphology/application). Demonstrated that fine-tuning frontier-class LLMs is a feasible path; output is JSON or English-sentence form. Code and data on `lbnlp/NERRE`.

**OpenChemIE.** Multimodal information-extraction toolkit for chemistry, integrating extractions from text, tables, and figures, including chemical structures.

### 3.6 Vision-language models for tables and figures (2023–present)

End-to-end VLM extraction (image of paper page → structured output) has become viable but is still narrowly competitive.

- **GPT-4V / GPT-4o.** Strong on body text and well-formed tables; struggles with academic notation, dense math, and complex layouts. 86.8% on formula recognition (OmniDocBench), comparable to specialized tools.
- **Claude 3.5 Sonnet / Claude 4.x.** Vision is competitive on tables and schematics, especially with the 200K context. Reported strength on nested tables with footnote associations.
- **Gemini 2.5/3 Pro.** Strong on full-page parsing; Gemini-3-Flash leads OmniDocBench at 90.1% on full-page parsing including tables. Only Gemini 3.1 Pro and GPT-5.4 consistently handle sparse tables (>87% accuracy).
- **Qwen2.5-VL.** Open-source, scoring 70% on MMMU-Pro multi-hop visual reasoning; closes much of the closed/open gap.

Caveats: on certain structured-visual reasoning tasks, top models still hit <30% accuracy (per the multimodal reasoning evaluations cited in the GPT-4V/Claude 2025 comparisons). VLMs underperform pipeline tools (MinerU, Mathpix, Docling) on table-structure tasks specifically.

### 3.7 Multi-agent / verification frameworks (2024–present)

The current research frontier — explicit multi-agent setups for cross-checking, debate, and iterative refinement.

- **SLM-MATRIX (npj Computational Materials, 2025).** Three reasoning paths: multi-agent collaborative, generator-discriminator, and dual cross-verification. **92.85% accuracy on BulkModulus** dataset, 77.68% on MatSynTriplet.
- **KARMA.** Multi-agent framework for knowledge graph enrichment with Relationship Extraction Agents, Schema Alignment, and Conflict Resolution Agents using LLM-based debate.
- **ComProScanner (RSC Digital Discovery, 2026).** Multi-agent composition-property extraction.
- **Polymer hybrid pipeline (ACL WaSP 2025).** Two-stage pipeline that first uses an LLM for table-to-text linearization, then end-to-end extraction. With Claude Sonnet 4.5 in the linearization stage, reached **67.92% F1@PoLyInfo**, significantly outperforming direct end-to-end LLM extraction.
- **otto-SR.** End-to-end systematic-review automation with **93.1% data-extraction accuracy** versus human-baseline 79.7%; 96.7%/97.9% screening sensitivity/specificity.
- **Hybrid LLM-Judge harness.** A pattern in agentic extraction pipelines: a separate LLM call verifies schema-level consistency and surface-level plausibility ("does the unit make sense for this property?", "does the value fall in the reported range elsewhere?") before the row enters the dataset.

The central pattern across these systems: explicit verification by *another* LLM call (or another agent role) catches errors that an extractor agent will not catch alone. This generalizes ChatExtract's follow-up-prompt insight to multi-agent designs.

---

## 4. Benchmarks and test sets

The benchmark landscape splits into four mostly-distinct families. The skill design needs to evaluate against multiple, because each family targets a different failure mode.

### 4.1 Table structure recognition (TSR)

These measure how well a system reconstructs the row/column/cell structure of a table image into a structured representation, regardless of what's inside the cells.

| Benchmark | Size | Source | What it measures | Notes |
|---|---|---|---|---|
| **PubTabNet** | 568K table images | PMC scientific articles | HTML structure + cell content | Introduced TEDS metric. |
| **PubTables-1M** | ~1M tables | PubMed Central scientific articles | Detailed structure incl. headers/locations | Microsoft. Addresses ground-truth oversegmentation. Subset on Kaggle. |
| **PubTables-v2** | (new, 2025) | Multi-page tables | Full-page and multi-page extraction | Late-2025 release. |
| **FinTabNet** | 113K tables | Annual reports | Row/column spanning, text-line bboxes | Financial domain. |
| **TableBank** | 417K tables | Word + LaTeX | Detection + recognition with weak supervision | 4-gram BLEU as evaluation metric. |
| **SciTSR** | 15K tables (12K train / 3K test) | Scientific PDF + LaTeX source | Cell adjacency relationship | SciTSR-COMP subset (716 complex tables) for harder evaluation. |
| **SynthTabNet** | 600K synthetic tables | Synthetic | Augmentation training | Companion data. |

### 4.2 Document parsing

These measure the full-page or full-document conversion task, including layout, text, tables, and equations.

| Benchmark | Size | Source | What it measures |
|---|---|---|---|
| **OmniDocBench (CVPR 2025)** | 1,651 PDF pages, 10 doc types, 5 layout types, 5 languages | Mixed academic + non-academic | Full-page parsing: text edit distance, table TEDS, formula CDM, layout |
| **OmniDocBench v1.5** | Updated leaderboard | Same | Same. Live leaderboard at idp-leaderboard.org |
| **DocBench** | (KnowledgeNLP 2025) | Mixed | LLM-based document QA + extraction |

OmniDocBench's overall score is `((1 − Text Edit) × 100 + Table TEDS + Formula CDM) / 3`. Top performers as of mid-2025: pipeline tools (MinerU, Docling) lead on academic papers and tables; Gemini-3-Flash leads at 90.1% full-page; only Gemini 3.1 Pro and GPT-5.4 handle sparse tables well.

### 4.3 Scientific information extraction (entity + relation)

Document-level extraction: salient entities, relations, and document-spanning n-ary tuples.

| Benchmark | Size | Domain | Task |
|---|---|---|---|
| **SciREX** (Allen AI 2020) | 438 full-text papers | Machine learning | NER (Method/Dataset/Task/Metric), salient entity ID, coreference, n-ary relation extraction (4-ary tuples) |
| **SciERC** | Abstracts only | Scientific | NER + binary relation (predates SciREX, narrower) |
| **SciER** (EMNLP 2024) | Scientific | Datasets, methods, tasks | Entity + relation extraction, full-document |
| **SciNLP** | NLP papers | Full text | Domain-specific entity + relation |
| **POLYIE** (NAACL 2024) | Polymer literature | Polymers | 5-ary tuple extraction (POLYMER, PROP_NAME, PROP_VALUE, CONDITION, CHAR_METHOD) |
| **CHEMDNER** | — | Chemistry | Chemical NER (organic) — ChemDataExtractor 2.1 reaches 89.7% F1 |
| **Matscholar NER** | — | Materials | Inorganic NER — ChemDataExtractor 2.1 reaches 88.0% F1 |

### 4.4 Long-context scientific reasoning + extraction

These specifically test full-paper reasoning rather than sentence- or paragraph-level.

| Benchmark | Size | Domain | Task |
|---|---|---|---|
| **CURIE (ICLR 2025)** | 580 problem/solution pairs across 10 tasks, 6 disciplines (materials science, condensed matter physics, quantum computing, geo-spatial, biodiversity, proteins) | Multi-domain | Information extraction, reasoning, concept tracking, aggregation, algebraic manipulation, multimodal, cross-domain |
| **TableEval (EMNLP 2025)** | Tables from finance, industry, academic, government | Mixed | Complex heterogeneous table QA |
| **VLDB 2025 TaDA — fine-grained scientific claims** | Curated benchmark | Scientific tables | Claim-level extraction from heterogeneous tables |

Best CURIE result reported: ~32% — *with frontier models*. This is a sobering data point: long-context cross-section extraction is far from solved.

### 4.5 Structured-output / JSON-schema benchmarks

Generic but useful: how reliably does the model produce schema-valid JSON with correct values?

| Benchmark | Size | What it measures |
|---|---|---|
| **Cleanlab Structured Output Benchmark** | — | Field accuracy + Output accuracy on JSON-schema-driven extraction |
| **SOB (Structured Output Benchmark, 2025)** | Multi-source | JSON Pass + Value Accuracy across many models |
| **JSONSchemaBench** | ~10K real-world JSON schemas | Efficiency (speed), Coverage (feature support), Quality (task accuracy) |
| **StructEval** | 18 formats, 44 task types | Renderable + non-renderable structured output |

### 4.6 Charts and figures

Often overlooked but essential for physical-science extraction.

| Benchmark | Size | What it measures |
|---|---|---|
| **ChartQA** | 9,608 human + 23,111 auto questions | Visual + logical reasoning over charts |
| **PlotQA** | Open-vocabulary | Reasoning over scientific plots, including math operations |
| **FigureQA / DVQA** | Synthetic charts | Structured chart QA |
| **LEAF-QA / LEAF-QA++** | Real-world data | Open-vocabulary chart QA |

Notable element: ChartQA and PlotQA define detection of 15 chart objects (Legend, yAxisTitle, ChartTitle, xAxisTitle, LegendPreview, PlotArea, yAxisLabel, xAxisLabel, LegendLabel, PieLabel, bar, pie, pieSlice, line, dotLine) — a useful reference schema for scientific-figure extraction.

---

## 5. Metrics

Five families of metrics matter. Choosing the right metric for each extraction sub-task is more important than choosing the right model.

### 5.1 Table structure metrics

- **TEDS (Tree-Edit-Distance-based Similarity).** Introduced with PubTabNet. Treats the predicted and ground-truth tables as HTML/XML trees and computes a normalized tree edit distance. Captures multi-hop cell misalignment and OCR errors better than older sequence-level metrics. Standard for table structure recognition.
- **GriTS (Grid Table Similarity, Microsoft).** A family of three: GriTS-Topology (which rows and columns each cell spans), GriTS-Content (textual content per cell), and GriTS-Location (rectangular pixel span per cell). Released with PubTables-1M. More fine-grained than TEDS for diagnostic use.
- **Cell adjacency relationship score (SciTSR).** Treats each cell pair's adjacency as the unit of evaluation; useful for diagnosing layout-only failures.
- **4-gram BLEU.** Used for TableBank — appropriate when output is an HTML/sequence, less informative when structure is what matters.

### 5.2 Field- and value-level metrics

- **Field accuracy.** Per-field correctness across many records. Fine-grained; lets you see which fields are bottlenecks.
- **Output accuracy.** All fields correct on a record. Strict; appropriate when downstream use requires every field.
- **Value accuracy.** Leaf-value correctness (e.g., the SOB metric). Distinguishes from "JSON parses successfully."
- **JSON Pass.** Schema validity only. Almost always 97%+ with modern models — this metric on its own is misleading.

### 5.3 Entity and relation extraction metrics

- **Precision / Recall / F1** on entity mentions, with strict (exact span match) and partial (overlap) variants. Standard for NER.
- **Document-level F1.** SciREX uses this for n-ary relations; relation is correct only if all entities in the tuple are.
- **Salient-entity F1.** Distinguishes core entities from incidentally mentioned ones.

### 5.4 Document parsing metrics

- **Text edit distance (normalized).** For the body text portion. Used as one of the three components in OmniDocBench.
- **Formula CDM (Character Diff Metric).** Component-level scoring for math formulas.
- **Composite scores.** OmniDocBench composes the three components into an overall score: `((1 − Text Edit) × 100 + Table TEDS + Formula CDM) / 3`.

### 5.5 Pragmatic / downstream-utility metrics

These rarely appear in benchmarks but matter for a real extraction skill.

- **Cell-level provenance recall.** Fraction of extracted cells that carry an exact source span.
- **Unit-correctness rate.** Fraction of numeric extractions with a correct, normalized unit.
- **Uncertainty handling rate.** Fraction of extractions that correctly captured ± / parenthetical / one-sided uncertainty.
- **"Not reported" vs. "zero" disambiguation rate.** Fraction of empty fields correctly classified.
- **Recall against gold-standard tables.** What fraction of the actual data in a paper made it into the output table.

A practical critique noted by Cleanlab: many published structured-output benchmarks contain ground-truth errors — re-checking the gold standard before trusting accuracy numbers is itself part of evaluation hygiene.

---

## 6. Performance comparison across benchmarks

### 6.1 Table structure recognition (PubTabNet / PubTables-1M / FinTabNet)

Microsoft's Table Transformer (TATR) is the canonical baseline; modern open-source models like DocLayout-YOLO, RobusTabNet, and Docling's TableFormer trade blows in the high-90s on TEDS for clean PMC tables. Performance on real-world heterogeneous tables (TableEval, fine-grained scientific claims benchmark) is materially lower — published numbers commonly drop 10–20 points compared to PubTabNet.

### 6.2 Document parsing (OmniDocBench)

Selected reported results (mid-2025, paraphrased from OmniDocBench leaderboards and published comparisons):

| System | Class | Strength on academic papers |
|---|---|---|
| **MinerU** | Pipeline | Edit ≈ 0.025 on academic papers (best in class) |
| **Docling** | Pipeline | 97.9% complex table extraction (2025 eval) |
| **Mathpix** | Pipeline (commercial) | Formula 86.6%, table mid-tier |
| **Nougat** | Specialized VLM | 0.734–1.000 across metrics on academic |
| **Marker** | Pipeline | 0.074–0.651 on OmniDocBench (variable by sub-task) |
| **GPT-4o** | General VLM | Formula 86.8%, table mid-tier on academic |
| **Gemini-3-Flash** | General VLM | 90.1% on full-page (top general VLM) |
| **GPT-5.4** | General VLM | 73.1 → 94.8 on table extraction (notable late-2025 jump); 87% on sparse tables |
| **Gemini 3.1 Pro** | General VLM | 94% on sparse tables |

Headline takeaway: **specialized pipelines lead on academic-paper tables; general VLMs are catching up but not yet ahead.** The best practical setup for our skill is to use a pipeline parser as the front end and a frontier LLM/VLM as the extraction layer, rather than relying on either alone.

### 6.3 Materials / chemistry data extraction

| System / Method | Task | Reported result |
|---|---|---|
| **ChatExtract (GPT-4)** | Materials data | ~90% precision, ~90% recall |
| **ChemDataExtractor 2.1 (BERT)** | Organic NER (CHEMDNER) | 89.7% F1 |
| **ChemDataExtractor 2.1 (BERT)** | Inorganic NER (Matscholar) | 88.0% F1 |
| **NERRE (fine-tuned GPT-3 / Llama-2)** | Materials joint NER+RE | Comparable or better than fine-tuned BERT pipelines |
| **MaterialsBERT pipeline (polymers)** | 24 properties on 2.4M articles | 1M+ records on 106K polymers |
| **Polymer hybrid pipeline (Claude Sonnet 4.5)** | 5-ary polymer tuples | 67.92% F1 @ PoLyInfo |
| **SLM-MATRIX (multi-agent)** | BulkModulus extraction | 92.85% accuracy |
| **SLM-MATRIX (multi-agent)** | MatSynTriplet | 77.68% accuracy |
| **Battery NER (transformer)** | Battery composition + cycling | 88.18% / 94.61% F1 |
| **LLMB agent (battery)** | Battery cell extraction | 15,398 cells extracted; integrates Material Graph Digitizer |

### 6.4 Generic structured output (SOB, JSONSchemaBench)

JSON Pass: 97%+ for almost all frontier models (Gemini, GPT-4/5, Claude, GLM, Qwen).
Value Accuracy: top models ~80–82%; gap of 15–30 points below the JSON-Pass score is the typical pattern.

### 6.5 Long-context scientific (CURIE)

Best result on full benchmark: **~32%**. Gemini Flash 2.0 and Claude-3 show consistent comprehension across domains; GPT-4o and command-R+ fail dramatically on protein sequencing. Even the best models leave most of the benchmark on the table.

### 6.6 Generic systematic-review extraction

- **otto-SR.** Data extraction 93.1% accuracy vs. human 79.7%. Screening 96.7%/97.9% sensitivity/specificity vs. human dual-reviewer 81.7%/98.1%.
- **Cross-LLM consistency** (Gemini 1.5 Flash / Pro / Mistral Large 2): 71.17%, 72.14%, 62.43% consistency with human coding — meaning humans are still needed in the loop for high-stakes extraction.
- **PICOs F1: 0.74**; study-type accuracy 74%, location 78%, size 91% (from the ISPOR multi-model HIL system).

### 6.7 Cross-benchmark synthesis

- **Easy tabular extraction with verification ≈ 90%+**; this is essentially solved for clean tables in well-formatted papers.
- **Hard tabular / heterogeneous extraction ≈ 67–85%**; requires multi-agent or hybrid pipelines.
- **Long-context multi-section extraction ≈ 32%**; still an active research problem, especially across disciplines.
- **Open-source VLMs are 10–30 points behind frontier closed-source** on most extraction tasks — but the gap is narrowing fast (Qwen2.5-VL closes much of it on visual reasoning).

---

## 7. Failure modes and what causes them

A consolidated catalog of documented failure modes, drawn from the materials-science table study (Gupta et al., *IMMI* 2024), the seven-failure-points RAG paper (Barnett et al., 2024), the OmniDocBench analysis, and the ChatExtract paper.

**Layout / parsing failures.**
- Multi-row sample tables (>5 samples). Late samples are often dropped silently.
- Unconventional notation (scientific notation, mixed formats, fractional cells). Accuracy drops sharply.
- Long molecule names with hyphens, sub/superscripts, complex chemical symbols. Worst-case accuracy ~46%.
- Merged cells, nested headers, hierarchical column groupings. Most parsers handle two levels; many fail at three.
- Footnotes and table-cell footnote markers. Frequently lost or attached to the wrong cell.
- Sparse tables (many empty cells). Only top-tier models (Gemini 3.1 Pro, GPT-5.4) handle these well.
- Rotated or sideways tables. MinerU explicitly handles these; many tools fail.

**Semantic / extraction failures.**
- Implicit units (column header "Eg" with no unit specified; convention buried in caption or methods).
- Implicit context ("at room temperature" from earlier sentence; sample naming from a separate definition table).
- Conflated species or systems (one paper uses "α-Al₂O₃" and "alumina" interchangeably; extractor treats them as different).
- "Not reported" misclassified as zero, missing, or random plausible value (hallucination).
- Derived values (ratios, normalizations) extracted as raw without the derivation context.

**LLM-specific failure modes (RAG / agentic context).**
- *Missing content* — the document does have the answer but retrieval missed the relevant passage.
- *Ranking errors* — relevant passage retrieved but not surfaced to the extractor.
- *Incomplete answers* — context contained the answer; extractor used only part of it.
- *Long-text degradation* — extraction quality drops on very long contexts despite the answer being in scope.
- *Retrieval thrash* — agent re-queries itself in circles.
- *Tool storms* — unbounded tool calls.
- *Context bloat* — agent's intermediate state crowds out evidence.
- *Hallucinated values* — model invents plausible numbers when uncertain. Documented in CURIE and structured-output benchmarks.
- *Schema overfitting* — model fills required fields at all costs, even when the document does not contain them.

**Quantitative failures.**
- Unit conversion errors (mol/L vs M; eV vs J; °C vs K offsets).
- Order-of-magnitude errors (10³ scaling missed in scientific notation).
- Sign errors (free energy conventions, negative indicators).
- Uncertainty stripping (5.0(2) becomes "5.0", losing the uncertainty).
- Mis-applied uncertainty (one-sided vs. two-sided; standard deviation vs. standard error not distinguished).

The pattern: **most failures are not "the model is bad" but "the system handed the model the wrong context, or didn't ask the model to verify."** Verification scaffolding addresses the second; pipeline parsing addresses the first.

---

## 8. Verification, grounding, and reliability patterns

The most important common pattern across high-performing systems: **a separate verification step, often a separate model invocation or agent, that catches errors before they enter the dataset.**

### 8.1 ChatExtract-style follow-up verification

The simplest, cheapest, and most consistently effective pattern.
- After extraction, ask the conversational model: "Is this value correct?" / "Did you miss any?"
- Exploit the conversation's information retention.
- ~10% absolute lift on materials-science tables; the technique is the difference between 80% and 90% accuracy in the published study.

### 8.2 Cross-LLM consensus / cross-critique

- Run extraction with two models (e.g., GPT-4o and Claude). Where they agree, accept; where they disagree, flag for human review or third-model adjudication.
- Used in otto-SR and the collaborative-LLM systematic-review pipeline (Khraisha et al., RSM 2024). Concordant outputs are highly accurate; discordant outputs are where the errors concentrate, so flagging them captures most of the value.

### 8.3 Schema-level LLM-Judge

- A separate model call with the schema definition + extracted record.
- Checks: schema validity, type consistency, plausible value ranges, unit-and-property compatibility ("is this a plausible band gap?", "is this a plausible bulk modulus?").
- Used in modern multi-agent extraction frameworks (KARMA, SLM-MATRIX, ComProScanner).

### 8.4 Cell-level provenance

- Every extracted value carries: source ID, page/section/table reference, exact text span, model + prompt version, confidence flag.
- Mandatory in PRISMA-trAIce-compatible reporting and in all serious systematic-review tools.
- Enables three things: human spot-check, programmatic re-extraction, and downstream filtering by confidence.

### 8.5 Document-level grounding (LAQuer, Attribution Gradients)

- Output spans attributed back to specific source spans.
- Enables interactive verification: "show me where this came from" with highlighted span.
- LAQuer (ACL 2025) and Attribution Gradients (2025) frame this as a first-class problem.

### 8.6 Citation-grounded extraction

- For metadata fields (paper authors, year, DOI) — verify against authoritative sources (Crossref, OpenAlex) before output.
- Eliminates the "GPT-4o hallucinates citations 78–90% of the time" failure mode (OpenScholar, *Nature* 2025) for the metadata fields specifically.

### 8.7 Domain tools as ground-truth oracle

- Unit converter, formula parser, materials-database lookups (Materials Project, NIST, AFLOW).
- The ChemCrow / Coscientist pattern: tool-augmented agents outperform model-only on domain tasks.
- For an extraction skill: when a value is extracted, ask a domain tool whether the value is plausible. E.g., extracted band gap = 87 eV → tool flags as implausible.

### 8.8 Human-in-the-loop checkpoints

- The published consensus from systematic-review automation (otto-SR, AutoLit, ISPOR HIL system, multi-model HIL): full automation is not yet appropriate for high-stakes extraction. Human spot-check on a sample, full review on flagged-low-confidence rows, full automation only where downstream use is forgiving.
- Emerging consensus: don't measure inter-LLM agreement and call it ground truth; treat low inter-rater agreement as a *signal of difficulty*, not a problem to be eliminated. Soft labels are sometimes more honest than hard ones.

---

## 9. Domain case studies

These are the best-documented physical-science extraction case studies and the most directly relevant to ResearchForge's intended user base.

### 9.1 Materials science

- **General-purpose polymer pipeline** (Gupta et al., *npj Computational Materials* 2023). 2.4M articles → 681K polymer-relevant → 1M+ property records on 106K unique polymers across 24 properties. MaterialsBERT + relation extraction. The reference for high-volume extraction.
- **Tables in materials science** (Gupta et al., *IMMI* 2024). 85% of compositions and properties only in tables. GPT-4o / Claude 3.5 ~84% accuracy; open-source models 43–56%. Scientific-notation and complex-symbol tables drop to 46%.
- **NERRE / LLM-NERRE** (Dagdelen, Dunn et al., *Nature Communications* 2024). Joint NER + RE for dopants/host materials, MOFs, composition/phase/morphology/application.
- **ChatExtract** (Polak & Morgan, *Nature Communications* 2024). The canonical verification-prompt method.
- **From text to insight** (Schilling-Wilhelmi et al., *Chem Soc Rev* 2025). Tutorial review covering the end-to-end LLM extraction workflow for chemistry/materials. Companion practical guide at matextract.pub.
- **Optimizing data extraction from materials science literature** (RSC *Digital Discovery*, 2025). Compared ChemDataExtractor, BERT-PSIE, ChatExtract, LangChain, Kimi on band-gap extraction from 200 papers. Encouraging precision and noise-rejection results, but extraction integrity below expectations — concrete evidence that none of the off-the-shelf tools is yet "good enough" alone.
- **SLM-MATRIX** (npj Computational Materials, 2025). Multi-agent verification reaching 92.85% on bulk-modulus extraction.

### 9.2 Chemistry

- **OpenChemIE.** Multimodal text + table + figure extraction with chemistry-aware algorithms.
- **Open Reaction Database (ORD)** schema as the structured target for reaction extraction (PMC11322921, 2024).
- **ChemRxnExtractor** (MIT). Two-stage product extraction + role labeling, transformer-based.
- **Automated extraction of synthesis actions** (Vaucher et al., *Nature Communications* 2020). Sequence-to-sequence transformer mapping experimental procedures to action sequences.
- **From text to insight** (Schilling-Wilhelmi et al., 2025). Already cited; the canonical chemistry-domain LLM extraction review.

### 9.3 Polymers

- **Polymer Scholar** — public corpus and database from the general-purpose polymer pipeline.
- **POLYIE** (NAACL 2024). 5-ary polymer tuple extraction dataset.
- **Polymer hybrid pipeline** (ACL WaSP 2025). Two-stage table linearization + extraction; 67.92% F1 with Claude Sonnet 4.5.
- **Polymer property data extraction** (Communications Materials 2024). LLM-driven extraction comparing extracted vs. PoLyInfo gold standard.

### 9.4 Batteries

- **A database of battery materials auto-generated using ChemDataExtractor** (*Scientific Data* 2020). The reference end-to-end extraction case.
- **BatteryBERT** (Huang & Cole, *JCIM* 2022). Domain-pretrained BERT for battery literature.
- **End-to-end battery recipe knowledge base** (Communications Materials 2025). Transformer-based mining; deep-learning NER reached 88.18% / 94.61% F1; structured 165 end-to-end recipes from 5,800+ paragraphs.
- **LLMB** (ACS Central Science). LLM agent integrated with Material Graph Digitizer; extracted 15,398 battery cells across composition and operating conditions.

### 9.5 Biomedical (relevant by analogy)

- **otto-SR.** End-to-end systematic review with state-of-the-art screening (96.7%/97.9%) and extraction (93.1%) accuracy. This is the most automated, end-to-end published system — useful as a target architecture even though the domain differs.
- **AutoLit Review.** Human-in-the-loop AI for systematic literature review.
- **Khraisha et al. (RSM 2024).** Cross-language and grey-literature systematic review with GPT-4.
- **Collaborative LLMs for living systematic reviews** (PMC 2024). Two-LLM cross-critique pattern.

The cross-domain pattern is consistent: domain-specialized parsing + LLM extraction + verification + cell-level provenance. The variable is which schema and which domain tools.

---

## 10. Design implications

A direct mapping from findings to design decisions for the ResearchForge data-extraction skill.

### 10.1 Architecture: composed pipeline, not monolithic prompt

**Decision.** A four-stage pipeline:
1. **Document parsing** (front end): convert PDF/HTML to clean structured text + table cells + figure references + section identifiers.
2. **Chunking and routing**: route prose to text-extraction; tables to table-extraction; figures to figure-extraction; supplementary info to its own pass.
3. **Schema-driven LLM extraction** with domain context (full paper available for cross-reference, but the prompt operates on a focused chunk).
4. **Verification**: ChatExtract-style follow-up + LLM-Judge schema check + (when budget allows) cross-LLM critique on flagged rows.

**Justification.** Every reproducibly successful system in the literature is a pipeline. Single-prompt extraction is consistently ~10–30 points behind on every published benchmark.

### 10.2 Document-parsing front end

**Decision.** Default to a pipeline parser (Docling, MinerU, or a hybrid) for PDFs; treat full-page VLM extraction as a fallback for documents the pipeline parser fails on. Use Nougat or Mathpix specifically for math-heavy papers.

**Justification.** OmniDocBench shows pipeline parsers beat general VLMs on academic papers, especially on tables. Full-page VLMs are catching up but not yet ahead. Math handling is uneven; specialized formula extraction (Mathpix, Nougat) is non-negotiable for physics-heavy papers.

**Open question.** How much custom parsing is needed for arXiv preprints with LaTeX source available — direct LaTeX parsing may beat any PDF pipeline when source is accessible.

### 10.3 Table handling as a first-class case

**Decision.** A dedicated table-extraction code path:
- Pipeline parser produces normalized cell-level representation (rows × cols × content + structural metadata: header rows, span info, footnote refs).
- LLM operates on the structured representation, not on rendered tables.
- Schema-aware prompts: tell the LLM what fields the table is supposed to contribute to.
- Multi-row table chunking: never let a table exceed the model's effective context for fine-grained extraction; chunk and stitch.
- Footnote attachment is recovered explicitly (footnote markers are matched to cells before LLM sees the table).

**Justification.** 85% of the data is in tables (polymer literature). Multi-row, sparse, and complex-notation tables are the dominant failure mode in every published evaluation.

### 10.4 LLM choice and verification scaffolding

**Decision.** Frontier closed-source model by default for extraction (Claude Sonnet/Opus or GPT-4-class); ChatExtract-style follow-up verification mandatory; LLM-Judge schema/plausibility check mandatory; cross-LLM critique escalation on disagreement or low confidence.

**Configuration parameters:**
- `model_extract`: primary extraction model (default: frontier closed-source).
- `model_verify`: verification model (default: frontier; can differ for cross-critique).
- `model_judge`: LLM-Judge model (can be a smaller/cheaper model; the judge task is bounded).
- `verification_passes`: 1 (ChatExtract follow-up) | 2 (+ LLM-Judge) | 3 (+ cross-LLM critique on flagged rows).

**Justification.** ChatExtract's ~10% lift is the canonical evidence. SLM-MATRIX, KARMA, and ComProScanner generalize the pattern with multi-agent verification reaching 90%+. Open-source models are 10–30 points behind on extraction; not appropriate as the default for the user's high-stakes engineering use case.

### 10.5 Schema-driven extraction with strong defaults

**Decision.** Three layers of schema:
1. **Universal fields** present in every record: source_id, page_or_section, span_text, span_offset, model, prompt_version, confidence, status (`extracted` / `derived` / `not_reported` / `missing` / `flagged`).
2. **Domain-default schemas** for the most common physical-science extraction targets: experimental measurement (system, method, conditions, value, unit, uncertainty, reference); composition (component, fraction, basis); physical property (property, value, unit, conditions, technique); reaction (reactants, conditions, yield, byproducts).
3. **User-specified custom schemas** layered on top.

**Justification.** POLYIE's 5-ary tuples and ORD's reaction schema show that domain-aware schemas dramatically improve extraction accuracy. Schema overfitting (the model fills required fields even when they aren't in the document) is mitigated by the explicit `not_reported` and `missing` distinction.

### 10.6 Units, uncertainty, and "not reported"

**Decision.** Three explicit fields per numeric extraction:
- `value`: the numeric value (or null).
- `unit`: normalized unit (the skill includes a unit-normalizer tool that maps J g⁻¹ K⁻¹, J/(g·K), etc. to a canonical form).
- `uncertainty`: structured representation `{kind: 'parenthetical' | 'symmetric' | 'asymmetric' | 'one_sided' | 'detection_limit', value: ..., basis: '1σ' | '2σ' | '95%CI' | ...}`.
- `status`: distinguishes `extracted`, `derived` (and stores the derivation), `not_reported`, `missing` (extractor failed), `flagged` (low confidence).

**Justification.** Documented failure modes (Gupta et al., 2024; ChatExtract): unit-stripping, uncertainty-loss, and "not reported"-vs-zero confusion are among the largest sources of downstream error. Making them schema-mandatory forces the pipeline to address them rather than papering over them.

### 10.7 Cell-level provenance

**Decision.** Every extracted value carries an immutable provenance record:
- `source_doi` (or arXiv ID, or local identifier).
- `location`: `{page, section, table_id, row, col, paragraph, sentence}`.
- `span_text`: the exact text the value was extracted from.
- `span_offset`: byte or character offsets for re-grounding.
- `extractor`: model + prompt-version + retrieval parameters.
- `verifications_passed`: list of which verification stages passed.
- `confidence`: numeric, with the calibration method documented.

**Justification.** This is the PRISMA-trAIce / LAQuer / Attribution Gradients consensus for grounded extraction. It is also a prerequisite for the human-in-the-loop and reproducibility requirements stated in the project goals.

### 10.8 Domain tools

**Decision.** Optional domain tools the skill calls during extraction or verification:
- Unit converter / unit normalizer.
- Chemical-formula parser (OPSIN-style) for chemistry tables.
- Property-range plausibility lookup (e.g., MaterialsProject / NIST APIs) — flag implausible extractions.
- Chemical-name disambiguation (PubChem / ChemSpider).
- Crossref / OpenAlex metadata verification for citation fields.

**Justification.** ChemCrow / Coscientist evidence: tool-augmented LLMs outperform un-augmented LLMs on domain tasks. Domain tools also serve as cheap, deterministic verification — a domain-tool flag is more reliable than an LLM "is this correct?" turn for many quantitative fields.

### 10.9 Charts and figures

**Decision.** Out of scope for v1 except as a flagged-source channel: when a paper's data is only in a figure, the skill records this as a coverage gap rather than attempting figure extraction.

**v2 path.** Integrate a chart-data-extraction tool (PlotDigitizer-style + VLM to read axes/legends) and a figure-data round-trip. Evaluate against ChartQA and PlotQA.

**Justification.** Figure extraction quality is uneven across all current systems; doing it badly in v1 would inject the worst-quality data into otherwise clean datasets. The honest move is to flag the gap.

### 10.10 Evaluation harness for the skill itself

**Decision.** The skill ships with an evaluation harness that runs against:
- A small set of papers with hand-curated gold standards (the team's own dogfooding set).
- A held-out subset of POLYIE for polymer extraction.
- A held-out subset of the materials-table study for table-heavy materials extraction.
- A subset of CURIE for long-context multi-section extraction.
- A subset of OmniDocBench for parsing front-end accuracy.
- Internally-defined regression tests for unit handling, uncertainty handling, and "not reported" classification.

**Metrics reported per run:**
- Field accuracy and Output accuracy (cleanlab-style).
- Cell-level provenance recall.
- Unit-correctness rate.
- Uncertainty-handling rate.
- "Not reported" classification rate.
- Recall against gold-standard tables.

**Justification.** Without an evaluation harness, the skill is unfalsifiable. The failure-mode catalog is too well-documented to design a skill that doesn't address it explicitly.

### 10.11 What this skill should *not* do

- **Compete on TSR benchmarks.** Use Docling or MinerU; don't reinvent the front end.
- **Train a new model.** All evidence points to verification-scaffolded prompting + tool augmentation as the high-leverage research; novel training is high-effort and low-return for this skill.
- **Aim for full automation.** Every published high-stakes extraction system uses human-in-the-loop. Surface low-confidence rows for review; default to that mode.
- **Promise figure/chart extraction in v1.** Flag the gap; come back to it.
- **Treat all papers identically.** Domain-specific schemas and domain tools matter — let the user (or upstream skills) tag the paper's domain so the right tools are loaded.

---

## 11. Sources

### Approaches and methods

- [ChemDataExtractor (Swain & Cole, JCIM 2016)](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.6b00207)
- [Single Model for Organic and Inorganic Chemical NER in ChemDataExtractor 2.1](https://pubs.acs.org/doi/10.1021/acs.jcim.1c01199)
- [NER Applied to Materials Science Information Extraction (MatScholar)](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00470)
- [Snowball 2.0: Generic Material Data Parser for ChemDataExtractor](https://pubs.acs.org/doi/10.1021/acs.jcim.3c01281)
- [Extracting accurate materials data with conversational LMs and prompt engineering — ChatExtract (Nature Communications 2024)](https://www.nature.com/articles/s41467-024-45914-8)
- [Structured information extraction from scientific text with LLMs — NERRE (Nature Communications 2024)](https://www.nature.com/articles/s41467-024-45563-x)
- [NERRE GitHub](https://github.com/lbnlp/NERRE)
- [How Well Do LLMs Understand Tables in Materials Science? (IMMI 2024)](https://link.springer.com/article/10.1007/s40192-024-00362-6)
- [From text to insight: LLMs for chemical data extraction (Chemical Society Reviews 2025)](https://pubs.rsc.org/en/content/articlelanding/2025/cs/d4cs00913d)
- [matextract.pub — companion practical guide](https://matextract.pub/)
- [Optimizing data extraction from materials science literature (RSC Digital Discovery 2025)](https://pubs.rsc.org/en/content/articlehtml/2026/dd/d5dd00482a)
- [OpenChemIE](https://arxiv.org/html/2404.01462v1)
- [Automated Chemical Reaction Extraction (JCIM 2021)](https://pubs.acs.org/doi/10.1021/acs.jcim.1c00284)
- [Automated extraction of synthesis actions (Nature Communications 2020)](https://www.nature.com/articles/s41467-020-17266-6)
- [Extracting structured organic synthesis with fine-tuned LLM (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11322921/)
- [SLM-MATRIX multi-agent extraction (npj Computational Materials 2025)](https://www.nature.com/articles/s41524-025-01719-x)
- [KARMA multi-agent KG enrichment](https://openreview.net/pdf?id=k0wyi4cOGy)
- [ComProScanner multi-agent (RSC Digital Discovery 2026)](https://pubs.rsc.org/en/content/articlehtml/2026/dd/d5dd00521c)
- [Polymer general-purpose extraction pipeline (npj Computational Materials 2023)](https://www.nature.com/articles/s41524-023-01003-w)
- [Polymer hybrid pipeline ACL WaSP 2025](https://aclanthology.org/2025.wasp-main.11/)
- [Data extraction from polymer literature (Communications Materials 2024)](https://www.nature.com/articles/s43246-024-00708-9)
- [Battery materials database via ChemDataExtractor (Scientific Data 2020)](https://www.nature.com/articles/s41597-020-00602-2)
- [BatteryBERT (JCIM 2022)](https://pubs.acs.org/doi/10.1021/acs.jcim.2c00035)
- [End-to-end battery recipe knowledge base (Communications Materials 2025)](https://www.nature.com/articles/s43246-025-00825-z)
- [LLMB battery agent (ACS Central Science)](https://pubs.acs.org/doi/10.1021/acscentsci.5c02433)
- [Mining experimental data from materials science literature (Tandfonline 2024)](https://www.tandfonline.com/doi/full/10.1080/27660400.2024.2356506)

### Document parsing

- [Nougat (Meta)](https://github.com/facebookresearch/nougat)
- [Marker — datalab](https://github.com/datalab-to/marker)
- [MinerU (OpenDataLab)](https://github.com/opendatalab/mineru)
- [Docling (IBM Research)](https://arxiv.org/html/2501.17887v1)
- [LayoutLM (paper)](https://arxiv.org/pdf/1912.13318)
- [Donut OCR-free document understanding (ECCV 2022)](https://github.com/clovaai/donut)
- [Microsoft Table Transformer (TATR)](https://github.com/microsoft/table-transformer)
- [PDF Data Extraction Benchmark 2025 — Docling, Unstructured, LlamaParse](https://procycons.com/en/blogs/pdf-data-extraction-benchmark/)
- [Comparative Study of PDF Parsing Tools (arXiv 2410.09871)](https://arxiv.org/pdf/2410.09871)

### Benchmarks and test sets

- [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet)
- [PubTables-1M (CVPR 2022)](https://arxiv.org/abs/2110.00061)
- [PubTables-v2 (arXiv 2512.10888, 2025)](https://arxiv.org/html/2512.10888v1)
- [SciTSR](https://github.com/Academic-Hammer/SciTSR)
- [TableBank](https://github.com/doc-analysis/TableBank)
- [Aligning Benchmark Datasets for TSR (arXiv 2303.00716)](https://arxiv.org/abs/2303.00716)
- [SciREX (Allen AI 2020)](https://github.com/allenai/SciREX)
- [SciER (EMNLP 2024)](https://aclanthology.org/2024.emnlp-main.726.pdf)
- [SciNLP (arXiv 2509.07801)](https://arxiv.org/html/2509.07801)
- [POLYIE (NAACL 2024)](https://aclanthology.org/2024.naacl-long.131.pdf)
- [OmniDocBench (CVPR 2025)](https://github.com/opendatalab/OmniDocBench)
- [OmniDocBench paper](https://openaccess.thecvf.com/content/CVPR2025/papers/Ouyang_OmniDocBench_Benchmarking_Diverse_PDF_Document_Parsing_with_Comprehensive_Annotations_CVPR_2025_paper.pdf)
- [OmniDocBench v1.5 leaderboard](https://www.idp-leaderboard.org/benchmarks/omnidocbench)
- [CURIE (ICLR 2025) — Google](https://github.com/google/curie)
- [CURIE paper](https://arxiv.org/abs/2503.13517)
- [TableEval (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.363.pdf)
- [Fine-grained scientific claims from heterogeneous tables (VLDB 2025 TaDA)](https://www.vldb.org/2025/Workshops/VLDB-Workshops-2025/TaDA/TaDA25_16.pdf)
- [DOCBENCH (KnowledgeNLP 2025)](https://aclanthology.org/2025.knowledgenlp-1.29.pdf)
- [Cleanlab Structured Output Benchmark](https://cleanlab.ai/blog/structured-output-benchmark/)
- [SOB Multi-Source Structured Output Benchmark](https://arxiv.org/html/2604.25359)
- [JSONSchemaBench](https://github.com/guidance-ai/jsonschemabench)
- [StructEval (arXiv 2505.20139)](https://arxiv.org/html/2505.20139v1)
- [ChartQA](https://github.com/vis-nlp/ChartQA)
- [ChartQA-X (arXiv 2504.13275)](https://arxiv.org/html/2504.13275v1)

### Methods, metrics, grounding

- [LAQuer: Localized Attribution Queries (ACL 2025)](https://aclanthology.org/2025.acl-long.746.pdf)
- [Attribution Gradients (arXiv 2510.00361)](https://arxiv.org/html/2510.00361v1)
- [Attribution, Citation, and Quotation: A Survey (arXiv 2508.15396)](https://arxiv.org/html/2508.15396v1)
- [CiteME: Can LMs Accurately Cite Scientific Claims? (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/0ef47f7b768e1a012e3d995ac8d8fac7-Paper-Datasets_and_Benchmarks_Track.pdf)
- [Seven Failure Points When Engineering a RAG System (arXiv 2401.05856)](https://arxiv.org/abs/2401.05856)
- [Cited text span identification for scientific summarization (Scientometrics 2020)](https://link.springer.com/article/10.1007/s11192-020-03455-z)

### Human-in-the-loop / systematic review

- [Human-in-the-Loop AI for Systematic Literature Review — AutoLit (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12552804/)
- [LLMs with HIL Validation for Systematic Review Data Extraction (arXiv 2501.11840)](https://arxiv.org/abs/2501.11840)
- [Repeatable Auto-extraction Frameworks (ISPOR 2025)](https://www.ispor.org/heor-resources/presentations-database/presentation-cti/ispor-2025/poster-session-5/)
- [Just Put a Human in the Loop? Subjective Tasks (arXiv 2507.15821)](https://arxiv.org/html/2507.15821v1)
- [Inter-annotator Agreement Metrics for NLP (arXiv 2603.06865)](https://arxiv.org/html/2603.06865)
- [Automation of Systematic Reviews with LLMs (medRxiv 2025)](https://www.medrxiv.org/content/10.1101/2025.06.13.25329541v2.full.pdf)
- [Collaborative LLMs for Living Systematic Reviews (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11469465/)
- [Khraisha et al., Can LLMs Replace Humans in Systematic Reviews? (RSM 2024)](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1715)

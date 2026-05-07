# Prior Work on AI-Assisted Literature Review, Synthesis, and Scientific Question Answering

A survey of what has been built, benchmarked, and published — commercial products, open-source agent frameworks, and academic literature — directly informing the design of a skill suite for literature search, summarization, structured extraction, and report generation in the physical sciences and engineering.

---

## Contents

1. Executive summary
2. Commercial tools and platforms
3. Open-source agent frameworks
4. Academic literature: benchmarks and findings
5. Cross-cutting methodology lessons
6. Architectural patterns from production agents
7. Design implications for our skill suite
8. Sources

---

## 1. Executive summary

The space has matured rapidly between 2022 and mid-2026, but in lopsided ways.

**What is largely solved.**
- Citation-grounded question answering on a small-to-medium corpus (PaperQA2 surpassed PhD-level researchers on retrieval and synthesis questions in the LitQA2 benchmark; OpenScholar reached citation accuracy on par with human experts and was preferred over expert-written answers in 70% of pairings).
- Title/abstract screening at near-human sensitivity and specificity (otto-SR reported 96.7% / 97.9% versus human dual-reviewer 81.7% / 98.1%).
- Tabular and unstructured numeric extraction on materials-science papers, when paired with explicit verification prompts (ChatExtract reached ~90% precision/recall with GPT-4-class models).

**What is partially solved.**
- End-to-end deep research (OpenAI Deep Research, Anthropic Claude Research, Gemini Deep Research, FutureHouse Falcon/Crow). These produce useful long-form briefs but cannot yet be trusted blindly — citation hallucination, coverage gaps, and reasoning errors persist.
- Search recall in narrow systematic-review settings. A Cochrane evaluation of Elicit found average sensitivity of 39.5% versus 94.5% in original human reviews, even as Elicit performed well on broader question-answering.
- Multi-paper synthesis with conflicting evidence — most tools collapse rather than expose the disagreement.

**What is still open.**
- Genuine end-to-end scientific discovery. A multi-framework evaluation (Agent Laboratory, AutoGen, BabyAGI, GPT Researcher, MOOSE-Chem2, SciAgents, SciMON, Virtual Lab) found that *no* framework completed a full cycle from literature understanding through computational execution to validated results and paper writing.
- Reproducibility and audit trails sufficient for systematic-review reporting standards. The PRISMA-trAIce checklist (2025) was developed precisely because existing AI-assisted review reporting was inconsistent and inadequate.
- Reliable structured extraction on heterogeneous physical-science tables, especially with unconventional notation, multi-row sample tables, and unit handling.

**The practical implication for our skill suite.** The pieces exist. The work is not in inventing new techniques but in *composing* the well-validated components — agentic RAG, screening, structured extraction, citation grounding, gap detection — into a workflow with auditable artifacts, explicit failure surfacing, and reproducibility built in from the start.

---

## 2. Commercial tools and platforms

### 2.1 Elicit

Elicit is the most mature general-purpose research assistant on the market, indexing ~138 million papers (sourced primarily from Semantic Scholar) and supporting search, screening, summarization, and structured extraction with PRISMA-style reporting.

**Strengths.** Sentence-level citations on every claim. Strong data extraction from text and tables (independently rated as best-in-class). Title/abstract screening reportedly saves >80% of manual time. Built-in mini-PRISMA diagram generation and study-type frequency tables.

**Weaknesses.** A 2025 Cochrane evaluation across four case studies found Elicit's search sensitivity at 39.5% versus 94.5% in original human reviews — meaning it misses many relevant studies. Searches are not reproducible (a hard requirement for systematic reviews). Single-database reliance (Semantic Scholar) limits coverage in fields not well-represented there. Screening is capped at 500 papers per project. Offers no manuscript-writing support.

**Lesson for us.** Elicit demonstrates that a clean *pipeline* of search → screen → extract → table is genuinely valuable, but its limitations on recall and reproducibility map to specific opportunities: query multi-source (OpenAlex, arXiv, Crossref, Semantic Scholar in parallel), record every search verbatim, and let the user inspect/edit at every stage.

### 2.2 Consensus

Consensus indexes ~250 million peer-reviewed papers and emphasizes a "Consensus Meter" that visualizes agreement/disagreement among studies for yes/no questions. Its Deep Search runs multi-step iterative literature reviews.

**Strengths.** Best-in-class for the narrow case of "what does the literature *agree* on?" — useful for clinical and policy questions. No-hallucination claim is supported by traceable evidence linking. Used by 5,000+ universities.

**Weaknesses.** Strongest on yes/no questions and biomedical/clinical topics; coverage of physical sciences, engineering, social science, and humanities is uneven. No published benchmarks of recall or precision against traditional databases. Best when questions are tightly scoped.

**Lesson for us.** The Consensus Meter is a strong UX pattern for *evidence-strength* signaling; replicating it as part of our analysis skill (a clear "supports / contradicts / mixed / silent" tag for each claim) would directly address one of the weakest points in most existing tools.

### 2.3 scite.ai (Smart Citations)

scite classifies 1.6B+ citations across 280M+ sources into "supporting," "contrasting," or "mentioning" using a deep-learning model on the surrounding citation context. Now part of Research Solutions; integrates via MCP with Claude and ChatGPT.

**Strengths.** A unique data layer for evaluating *how* prior work has been received, not just whether it was cited. Useful for identifying papers that are widely cited but whose claims have been substantially contested. Browser extension and MCP make it composable.

**Weaknesses.** Misclassification of citation intent has been documented; the labels are approximate, not authoritative. The supporting/contrasting/mentioning ontology is also coarser than what a careful systematic review would want.

**Lesson for us.** scite is the cleanest example of *contextual citation analysis* in production. A skill that consumes scite-style signals (or computes them locally for a small corpus) is a meaningful differentiator over tools that treat all citations as equal.

### 2.4 Undermind

Undermind is an agent-style search tool that iteratively reads and analyzes papers. Their public benchmark (whitepaper) reports a ~10× higher concentration of relevant results in the top hits versus Google Scholar; classification accuracy of ~96% on highly relevant papers; coverage of 30–80% of gold-standard papers from systematic reviews.

**Strengths.** Optimized for high-recall searches where Google Scholar produces nothing. Iterative, agent-driven query refinement is a clear architectural win.

**Weaknesses.** Coverage still depends on the underlying index. The benchmark is internal and uses ~400 manually graded papers — informative but not standardized.

**Lesson for us.** Undermind's published methodology (iterate, classify, rank) is well-aligned with how a search-and-compile skill should behave. Their benchmark approach (gold-standard recovery against systematic-review reference sets) is also worth borrowing.

### 2.5 FutureHouse platform: Crow, Falcon, Owl, Phoenix (and Robin)

FutureHouse is the most academically credentialed of the commercial offerings. Their agents are deployed versions of open-source code (PaperQA2 → Crow), with public benchmarks and a free API.

- **Crow.** Production version of PaperQA2; general-purpose Q&A over the literature with concise, scholarly answers. API-first.
- **Falcon.** Specialized for deep literature reviews with access to additional databases (e.g., OpenTargets). The flagship for review-style outputs.
- **Owl** (formerly HasAnyone). Specialized for "has anyone done X before?" — explicitly framed as a prior-art / novelty check. Architecturally interesting because it changes the success criterion: comprehensive *coverage* of similar prior work.
- **Phoenix** (experimental). FutureHouse's deployment of ChemCrow with chemistry-specific tools.
- **Robin.** A multi-agent orchestrator that combines Crow + Falcon + Finch (data analysis) for end-to-end discovery. Used to identify ripasudil as a candidate for dry AMD, including proposing and analyzing follow-up RNA-seq experiments. End-to-end conceptualization to paper submission in 2.5 months. Open-sourced.

**Strengths.** Published, peer-reviewed benchmarks (LitQA2, ScholarQABench, RAG-QA Arena science benchmark). Honest about limitations. Open-source upstream (PaperQA, Aviary).

**Weaknesses.** Strong biomedical bias in benchmarks; physical-sciences coverage is less proven. Closed proprietary deployments (Falcon, Owl) offer less transparency than the underlying open code.

**Lesson for us.** The *separation of agents by use-case* (general Q&A vs. deep review vs. prior-art search vs. domain-specific) is the single most important architectural insight from FutureHouse. Our skill suite should mirror this: skills with sharply different success criteria should be different skills, not modes of one skill. Robin is also a model for an orchestration / planning skill.

### 2.6 SciSpace

End-to-end research workspace combining discovery, AI-powered reading (Copilot), and writing assistance.

**Strengths.** The "PDF Copilot" — chat-with-the-paper interaction grounded in the actual PDF — is a paradigm worth replicating for our extraction skill.

**Weaknesses.** Less rigorous evidence on extraction accuracy than Elicit; broader "workspace" framing means less focus on any one task.

### 2.7 ResearchRabbit and Litmaps

Both are citation-based discovery tools that visualize the citation graph around a seed set of papers. As of October 2025, ResearchRabbit and Litmaps have partnered, combining their indices and features.

**Strengths.** Strong for *expansion* of an existing seed corpus through citation neighborhoods (citing-by, references-of, similar-papers). Litmaps' time/citation axis visualization is unique.

**Weaknesses.** Pure citation-graph traversal misses semantically similar work that does not cite the seed papers (the perennial problem with citation-based search).

**Lesson for us.** Citation-graph expansion should be one ingestion mode for our search skill, complementing semantic search. Treating the two as alternatives is a false dichotomy.

### 2.8 Connected Papers, Iris.ai, Petal, Scinapse, AnswerThis

Smaller players, each occupying a niche: Connected Papers for fast citation-graph visualization from a single seed paper; Iris.ai for concept-mapped exploration; Petal for individual-document chat; AnswerThis for explicit "research gap finder" framing. None are dominant, but each is informative for design ideas.

### 2.9 Deep Research products (OpenAI, Anthropic, Google)

OpenAI's Deep Research, Anthropic's Claude Research, and Gemini Deep Research all offer agent-style multi-step research with cited reports.

**Strengths.** Generalist agents that work across domains. Anthropic's Research surfaces multi-perspective reasoning and emphasizes verifiable citations. OpenAI's tool can synthesize from "dozens or hundreds of websites."

**Weaknesses (per Nature's evaluation of OpenAI Deep Research).** Useful for orienting non-experts; experts find errors and missing nuance. Citation hallucinations and over-confident synthesis remain.

**Architectural insight.** All three abandoned rigid "planner → tool → writer" pipelines in favor of integrated "model-as-agent" designs trained end-to-end with reinforcement learning to decompose tasks, browse, and assemble citations inside one model. This is a strong signal for our orchestration approach: less rigid pipelining, more iterative agent-driven planning.

### Comparative summary

| Tool | Primary strength | Primary weakness | Most relevant to our skill |
|---|---|---|---|
| Elicit | Pipeline depth, sentence-level citations | Search recall, reproducibility | Summarize + extract |
| Consensus | Evidence-strength visualization | Topic coverage, no public benchmarks | Analyze (consensus meter) |
| scite | Citation-context labels | Misclassification, coarse labels | Analyze (citation context) |
| Undermind | Iterative agent search recall | Limited transparency | Search + compile |
| FutureHouse Crow/Falcon | Open-source roots, benchmarked | Biomedical bias | All four |
| FutureHouse Owl | Prior-art / novelty framing | Niche use case | Search + compile (variant) |
| SciSpace | Chat-with-PDF UX | Less benchmarked extraction | Summarize + extract |
| ResearchRabbit / Litmaps | Citation-graph expansion | Pure citation-graph blind spots | Search + compile |
| Deep Research (OAI/Anthropic/Google) | Generalist multi-step research | Hallucination, coverage | Analysis + report |

---

## 3. Open-source agent frameworks

### 3.1 PaperQA and PaperQA2 (FutureHouse)

PaperQA2 is the open-source base of FutureHouse Crow. It is the single most important reference for our search and Q&A skills.

**Architecture.**
- Decomposes RAG into *tools* the agent calls (search, gather evidence, generate answer).
- The agent can iteratively refine search queries and re-search if a candidate answer is insufficient.
- Uses LLM-based re-ranking and contextual summarization (RCS) — a two-phase relevance check on candidate chunks.
- Supports document metadata-awareness in embeddings.

**Performance on LitQA2.** 85.2% precision and 66.0% accuracy (mean ± SD). Surpassed PhD/postdoc-level biology researchers. State-of-the-art on RAG-QA Arena's science benchmark.

**Lesson for us.** This is the reference architecture for our search-and-Q&A path. The decomposition (gather candidates → re-rank → contextual summarize → generate → verify → re-search if needed) should be the default loop in our search skill.

### 3.2 OpenScholar (Allen Institute / UW)

Published in *Nature* (2025). The first fully open retrieval-augmented LM for scientific synthesis. 45M open-access papers indexed.

**Performance.** OpenScholar-8B beat GPT-4o by 6.1% and PaperQA2 by 5.5% on multi-paper synthesis. While GPT-4o hallucinated citations 78–90% of the time, OpenScholar achieved citation accuracy on par with human experts. In blind expert pairwise judgments, OpenScholar-8B was preferred over expert-written answers 51% of the time; OpenScholar-GPT-4o 70%.

**Benchmark.** ScholarQABench: 2,967 expert queries, 208 long-form answers across CS, physics, neuroscience, biomedicine.

**Lesson for us.** Two takeaways. First, citation hallucination at 78–90% is the *default* failure rate for general-purpose LLMs without proper grounding. Any skill we build that emits citations *must* enforce retrieval-grounded, span-checked citations or it will inherit this failure mode. Second, OpenScholar's data store and code are open; we can use ScholarQABench for our own evaluation.

### 3.3 The AI Scientist v1 / v2 (Sakana AI)

The first system to produce an entirely AI-generated paper accepted at a peer-reviewed workshop (ICLR workshop, score 6.33, top ~45%). v2 eliminated v1's reliance on human-authored code templates and uses a progressive agentic tree-search methodology. Cost: $6–$15 per paper.

**Strengths.** Demonstrates end-to-end is *possible* at the workshop level for ML topics with clean experimental protocols.

**Weaknesses.** Independent evaluations (Schmidgall et al., "Evaluating Sakana's AI Scientist") describe "bold claims, mixed results." Most outputs are not publication-ready. Domain-bound to ML.

**Lesson for us.** End-to-end paper generation is *not* our goal — but the tree-search planning approach is interesting for the analysis-and-report skill, and the failure modes (over-confident novelty claims, weak experimental design critique) are exactly what our skill suite should explicitly guard against.

### 3.4 STORM (Stanford OVAL)

"Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking." Generates Wikipedia-like long-form articles from a topic.

**Architecture.** Two-stage. Pre-writing: discover perspectives by surveying related articles, simulate conversations between a writer and a topic expert grounded in retrieved sources, build a hierarchical outline. Writing: populate the outline section by section.

**Reception.** Wikipedia editors found STORM helpful for *pre-writing* (outline + source list) but said outputs need significant editing before publication.

**Lesson for us.** Outline-first is the right structure for our reporting skills. The *perspective-guided question asking* idea is also valuable: rather than generating one set of queries, force the agent to imagine multiple stakeholder/sub-topic perspectives and search for each.

### 3.5 AutoSurvey, AutoSurvey2, Agentic AutoSurvey, SurveyGen-I

A family of LLM-driven survey-paper generation systems. All target the specific genre of "long, structured, citation-heavy review paper."

- **AutoSurvey.** Initial retrieval → outline → subsection drafts by specialized LLMs → integration → multi-LLM-as-judge evaluation.
- **AutoSurvey2** (Oct 2025). Multi-stage pipeline with retrieval-augmented synthesis and structured evaluation.
- **Agentic AutoSurvey.** Four-agent system: Paper Search Specialist, Topic Mining & Clustering, Academic Survey Writer, Quality Evaluator.
- **SurveyGen-I.** Adds evolving plans and memory-guided writing for consistency in long surveys.

**Lesson for us.** The four-agent split in Agentic AutoSurvey is almost identical to the user's original four-skill plan (search → cluster/summarize → write → evaluate). This is convergent design — strong evidence the decomposition is correct. Borrow the *Quality Evaluator* idea explicitly: a critic skill or step that grades the report against rubric criteria before output.

### 3.6 ChemCrow and Coscientist

- **ChemCrow.** GPT-4 + 18 expert-designed chemistry tools. Autonomously planned syntheses of an insect repellent, three organocatalysts, and guided discovery of a novel chromophore.
- **Coscientist.** Multi-LLM system that browses the web, reads documentation, calls robotic experimentation APIs, optimizes Pd-catalyzed cross-couplings.

**Lesson for us.** Tool-augmented agents in chemistry routinely outperform un-augmented LLMs on domain tasks. For our extraction skill, this implies: domain-specific *tools* (unit converter, formula parser, materials-database lookup, equation solver) are likely to give larger quality gains than larger models alone.

### 3.7 SciAgents, SciAgent, SciMON, ResearchAgent, GPT Researcher, Robin, Aviary

- **SciAgents.** Multi-agent intelligent graph reasoning for scientific discovery.
- **SciAgent.** Coordinator + specialized worker subagents (symbolic, conceptual, numerical, verification).
- **SciMON.** Compares novel ideas against literature and revises until they no longer resemble prior work — good model for novelty-checking.
- **ResearchAgent.** Iterative dialogue between proposer and reviewer agents (peer-review simulation).
- **GPT Researcher.** Open-source, autonomous, multi-source research with inline citations. Heavily used baseline.
- **Robin** (FutureHouse). Orchestrates Crow + Falcon + Finch for end-to-end discovery — the biomedical case study (ripasudil for dry AMD) is a strong existence proof for orchestration.
- **Aviary** (FutureHouse). The training gym FutureHouse uses: language decision processes, environments for literature, protein engineering, molecular cloning. Trained agents on Aviary match/exceed frontier LLMs at up to 100× lower inference cost.

**Cold reality check.** A 2026 evaluation (bioRxiv) of eight open-source frameworks (Agent Laboratory, AutoGen, BabyAGI, GPT Researcher, MOOSE-Chem2, SciAgents, SciMON, Virtual Lab) found that *no* framework completed a full research cycle from literature understanding through computational execution to validated results to paper writing. End-to-end remains a research problem.

**Lesson for us.** Don't over-promise end-to-end. Stop at well-defined intermediate artifacts that the user can inspect and act on. The orchestration skill (if we build one) should focus on *chaining well-validated steps*, not on autonomous discovery.

---

## 4. Academic literature: benchmarks and findings

### 4.1 Benchmarks

| Benchmark | Domain | What it measures | Why it matters for us |
|---|---|---|---|
| **LitQA2** (FutureHouse) | Biomed | Multi-paper Q&A from full text | Best-known retrieval+synthesis benchmark; PaperQA2 surpassed PhD-level here. |
| **ScholarQABench** (Ai2) | CS, physics, neuro, biomed | Long-form citation-grounded answers | Multi-domain, includes physics — directly relevant to our scope. |
| **BixBench** | Computational biology | Real analytical scenarios with file inputs | Tests agentic data analysis end-to-end. |
| **SciCode** | Math, physics, chem, bio, materials | Coding scientific algorithms | The closest benchmark to physical-sciences capability. 338 subproblems from 80 main problems, scientist-curated. |
| **DeepResearch Bench** | Generalist research | Whole-pipeline deep research | Useful for our reporting skills' final evaluation. |
| **CiteAudit** / clibib | Citation hallucination | Detection across 9 fields | Reference for how to evaluate our citation grounding. |
| **HalluLens, HalluHard** | LLM hallucination | Multi-turn, grounded | Useful for stress-testing extraction accuracy. |

### 4.2 Screening and extraction performance

- **otto-SR (2025).** End-to-end systematic-review automation. Screening: 96.7% sensitivity, 97.9% specificity vs. human dual-reviewer 81.7% / 98.1%. Data extraction: 93.1% accuracy vs. human 79.7%. With AI-assisted extraction, median extraction time reduced by 41 minutes per study at 91.0% accuracy.
- **JMIR (2024).** Median recall 85% for fully automated zero-shot screening; 97% for semi-automated, 51% workload reduction.
- **Cross-study median for data extraction: ~66% correctly extracted** — wide variance by tool, model, and field. The high-end results above are the ceiling, not the average.
- **Khraisha et al. (2024, RSM).** GPT-4 efficacy in screening and extraction across multiple languages and grey literature; significant variation by task.
- **Materials science table extraction (Nature Comms 2024).** GPT-4 + ChatExtract method (engineered prompts with follow-up verification questions): ~90% precision and recall. Closed-source models (Claude-3.5-Sonnet, GPT-4o) ~84% accuracy; open-source 43–56%. Failure modes: tables with >5 samples, unconventional notation (scientific notation, mixed formats), complex content (long molecule names, hyphens, sub/superscripts) — accuracy on the worst tables fell to 46%.

### 4.3 Gap detection

- **GAPMAP (Oct 2025).** Categorizes gaps as **explicit** (signaled by lexical cues like "unknown," "further research is needed") versus **implicit** (inferred from missing links in chains of claims, scope-limited generalizations, unreconciled conflicting findings).
- **Performance.** Both open- and closed-weight LLMs are robust at identifying both gap types. In human evaluation, 83.3% of identified gaps were judged factually true; 56% fully agreed they remain open, 25.9% partially agreed.

**Lesson for us.** The explicit/implicit gap distinction is the right ontology for our summarization skill's gap-detection feature. Explicit gaps are easy and high-precision; implicit gaps require multi-paper reasoning and are where we can add the most value.

### 4.4 Reporting and reproducibility: PRISMA-trAIce

PRISMA 2020 governs systematic-review reporting; PRISMA-AI (2022, Nature Medicine) covers AI as a *subject* of review; PRISMA-trAIce (2025) covers AI as a *tool in* the review process. The latter exists because existing AI-assisted reviews were reporting prompts, model versions, human-AI interaction, and oversight inconsistently.

**Lesson for us.** We should produce, by default, a machine-readable run record that satisfies PRISMA-trAIce-style fields: model and version, prompts, retrieval parameters, dedup logic, screening decisions with rationale, extraction prompts, human override events. This is the *reproducibility audit trail* that distinguishes a serious tool from a chatbot wrapper.

### 4.5 Galactica — what not to do

Meta released Galactica (Nov 2022) as a 120B-parameter LM trained on scientific text. It was withdrawn within three days. Failure modes: confabulated papers (sometimes attributing to real authors), authoritative-voiced misinformation in subtle technical claims that even experts could miss, no separation between training corpus knowledge and external grounding.

**Lesson for us.** This is the negative example. Every output our skills produce should be either (a) a direct quote from a retrieved source with span attribution, or (b) clearly labeled synthesis with each contributing source listed. *No content should originate from the model's parametric memory without grounding.*

---

## 5. Cross-cutting methodology lessons

### 5.1 Search and compilation

- **Multi-source is non-negotiable.** OpenAlex (~209M works), Semantic Scholar, arXiv, Crossref, PubMed, Unpaywall, OpenCitations — combining them is standard practice. No single source covers everything; cross-referencing is also how you sanity-check metadata.
- **Iterative agent-driven search beats one-shot keyword search.** Undermind, PaperQA2, OpenScholar all iterate.
- **Citation-graph expansion complements semantic search; neither subsumes the other.** Citation-only misses semantically similar non-citing work; semantic-only misses obvious chains of intellectual lineage.
- **Reproducibility is a first-class requirement.** Searches must be re-runnable, query-by-query, with timestamps. Elicit's lack of this is a real limitation.
- **Recall vs. precision is task-dependent.** A "has anyone done X" search (Owl-style) optimizes for recall on prior art. A "best evidence on Y" search optimizes for precision on top hits. They are different skills with different success criteria, even if they share retrieval primitives.

### 5.2 Summarization and corpus mapping

- **Schema-driven summaries scale.** Free-form summaries are inconsistent across a corpus; an explicit per-source schema (objective, methods, cohort/system, key results, limitations, etc.) enables tabular comparison and downstream extraction.
- **Coverage gaps must be made explicit.** GAPMAP's explicit/implicit dichotomy is a clean ontology. Implicit gaps (missing links in claim chains) are where multi-paper LLM reasoning genuinely adds value.
- **Multi-paper synthesis remains the hardest step.** OpenScholar's gain over PaperQA2 was specifically on multi-paper synthesis tasks.
- **STORM-style perspective generation** before summarization improves coverage.

### 5.3 Structured data extraction

- **Verification prompts are the single most effective intervention.** The ChatExtract approach (extract → ask follow-up "is this correct?" / "did you miss any?") raised accuracy to ~100% on most tables. This is cheap and should be the default.
- **Two-LLM cross-critique is also effective.** When two models agree, accuracy is high; when they disagree, surface for human review (otto-SR and "Collaborative LLMs for Living Systematic Reviews" both validate this).
- **Tables are the dominant failure mode.** Many samples per table, unconventional notation, complex symbols/subscripts. Pre-processing (parse the table to a normalized cell representation) before LLM extraction is essential, not optional.
- **Units, uncertainty, and "not reported" require explicit handling.** Numbers without units are useless. "Not reported" must be distinguishable from "zero" or "missing extraction."
- **Provenance must be cell-level.** Every extracted value should carry: source ID, page/figure/table reference, exact text span, model+prompt version, confidence flag.
- **Closed-source frontier models (Claude-3.5+/GPT-4-class) substantially outperform open-source on accuracy.** This is consistent across studies. For a skill suite, this argues for model-agnostic design with the ability to escalate to a stronger model on hard fields.

### 5.4 Citation grounding and hallucination

- **GPT-4o hallucinates citations 78–90% of the time without grounding.** This is the OpenScholar-published baseline. Our skills must operate in a regime that rules this out.
- **CiteAudit, BibAgent, CheckIfExist** all reduce fabrication by grounding citations in authoritative databases. This is the right pattern: *every* citation our skills emit should be verified against an authoritative metadata source (DOI lookup, OpenAlex, Crossref) before output.
- **Field-level errors compound.** A citation can have the right author and wrong year, the right paper and wrong page; treat each metadata field as independently verifiable.
- **Inline-citation requirements at generation time** (HalluHard's design) substantially improve grounding compared to post-hoc citation insertion.

### 5.5 RAG vs. long-context

- **No silver bullet** (LaRA benchmark). Long-context wins on self-contained, coherent documents; RAG wins on fragmented, multi-source contexts and on cost.
- **For our use case — many papers, structured extraction across them — RAG is the right primary architecture**, with long-context as a fallback for single-paper deep-extraction tasks.
- **Summarization-based retrieval is competitive with long-context** and meaningfully better than raw chunk retrieval. PaperQA2's contextual summarization is exactly this pattern.

### 5.6 RAG engineering failure modes

From "Seven Failure Points When Engineering a RAG System" (2024) and the agentic-RAG follow-ups: missing content, ranking errors, incomplete answers despite available context, long-text extraction degradation, retrieval thrash (the agent re-querying itself in circles), tool storms (unbounded tool calls), context bloat (the agent's own intermediate state crowds out evidence).

**Lesson for us.** Validation is only feasible during operation, not in design — so we need built-in observability: log every retrieval, every re-rank score, every tool call, every prompt and response. Without this, debugging is guesswork.

---

## 6. Architectural patterns from production agents

### 6.1 Anthropic's multi-agent research system

Anthropic's Research feature uses an **orchestrator-worker pattern**: a lead agent analyzes the query, develops a strategy, saves a plan to memory, and spawns parallel subagents to explore different aspects. Subagents act as intelligent filters, iteratively searching and returning findings. The lead agent compiles the final answer.

- Multi-agent (Opus 4 lead + Sonnet 4 subagents) outperformed single-agent Opus 4 by **90.2%** on internal research evals.
- Production transition revealed prompt engineering becomes much harder in multi-agent setups: agents spawned excessive subagents on simple queries, ran redundant searches, and failed to coordinate.
- Mitigations: explicit budget/scope guidance to subagents, structured returns from subagents, deduplication at the orchestrator level.

### 6.2 Deep Research products' shift to model-as-agent

OpenAI Deep Research, Anthropic Claude Research, and Gemini Deep Research have shifted from rigid "planner → tool → writer" pipelines to integrated model-as-agent designs (often trained end-to-end with RL). The interpretation: brittle hand-coded pipelines are being replaced by agents that *learn* when to plan, search, browse, summarize, and cite.

**Implication for skill design.** Skills should not over-prescribe the inner loop. The skill's job is to define inputs, outputs, tools, and constraints — and let the model orchestrate. Heavy procedural prompting works against modern agent training.

### 6.3 The Robin pattern: small orchestrator, specialized workers

Robin orchestrates Crow, Falcon, and Finch — three specialized agents — and produces end-to-end discovery. This is the cleanest validation of the user's original four-skill plan with an optional fifth orchestration skill.

---

## 7. Design implications for our skill suite

A direct mapping from the findings above to specific design decisions for the four planned skills (and a possible fifth orchestration skill).

### 7.1 Skill 1 — Source search and compilation

**Design choices justified by prior work.**
- **Multi-source by default.** Query OpenAlex, arXiv, Semantic Scholar, and Crossref in parallel; deduplicate via DOI / arXiv ID / title-similarity. Optionally PubMed for biomed adjacencies. Driven by the consistent finding that single-source recall is too low.
- **Iterative agent loop.** PaperQA2 / Undermind / OpenScholar pattern: query → fetch candidates → LLM re-rank → assess sufficiency → reformulate query if not. Stop conditions: gold-standard recovery threshold (when a known seed set is provided), saturation in relevant-rate, or budget cap.
- **Citation-graph expansion as a complementary mode.** Litmaps/ResearchRabbit-style; one-hop and two-hop citation neighborhood with semantic re-ranking.
- **Mode parameter.** Distinct modes for *prior-art* (high recall, Owl-style), *evidence on a question* (high precision, top-k), and *full corpus for review* (high recall + completeness within scope). The success criteria differ.
- **Reproducibility artifacts.** Every query (provider, full query string, parameters, timestamp) and every dedup decision logged.
- **Coverage report.** End each run with an explicit "what we did not search" — sources unindexed, paywalled, language-filtered, date-bounded.

### 7.2 Skill 2 — Summarization and corpus mapping

**Design choices justified by prior work.**
- **Schema-driven summaries.** A user-configurable schema (with strong defaults for empirical, computational, and theoretical paper types in physical sciences). Each field is independently grounded to a span in the source.
- **Two-pass summarization.** PaperQA2's contextual summarization beats raw chunk retrieval: first extract relevant chunks against the schema, then summarize.
- **STORM-style perspective generation** for the corpus-level outline: surface multiple sub-topic perspectives before populating the corpus map.
- **Explicit + implicit gap detection** (GAPMAP ontology). Explicit gaps from lexical cues are cheap; implicit gaps from claim-chain analysis require multi-paper reasoning.
- **Trigger search expansion** when the gap detector finds an addressable gap (a specific sub-question with no coverage in the current corpus).
- **Quality evaluator step** (Agentic AutoSurvey pattern). Before emitting the corpus table, a critic check that verifies each row's grounding and surfaces low-confidence cells.

### 7.3 Skill 3 — Structured data extraction

**Design choices justified by prior work.**
- **Verification by default** (ChatExtract pattern). Every extracted value gets a follow-up verification turn ("is this correct? did you miss any?"). Cheap, ~10% accuracy lift on materials tables.
- **Two-LLM cross-critique** for high-stakes extractions. When models agree, take the value; when they disagree, surface for review.
- **Pre-process tables before LLM ingestion.** Parse PDFs/HTML to a normalized cell-level representation; the LLM extracts from structured cells, not from raw rendered tables.
- **Cell-level provenance.** Every output cell carries source ID, location, exact span, model+prompt version, confidence flag. This is the *non-negotiable* output shape.
- **Explicit unit, uncertainty, and "not reported" handling.** Three distinct fields: value, unit, status (∈ {extracted, derived, not reported, missing}). Derived values include the derivation expression.
- **Domain-aware tools.** Unit converter, formula parser, lookup against authoritative materials databases (Materials Project, NIST, NASA Polymers, etc.) where appropriate. Tool augmentation outperforms model-only on domain tasks (ChemCrow, Coscientist).
- **Closed-source frontier model by default**, with the ability to specify a cheaper model for low-stakes fields. Open-source models alone underperform on extraction (~43–56% accuracy) and are not appropriate as the default.

### 7.4 Skill 4 — Analysis and report generation

**Design choices justified by prior work.**
- **Three sub-skills, not one.** *Narrative review*, *meta-analysis support*, *direct question answering* — they have different success criteria (coverage, statistical synthesis, decisive answer).
- **Outline-first authoring** (STORM, AutoSurvey). Generate structure → review with the user → populate. Don't generate from scratch in one pass.
- **Evidence-strength signaling** (Consensus Meter pattern). For every claim, surface a tag: strong support / moderate support / mixed / contested / no direct evidence. This is the highest-value differentiator over chatty summaries.
- **Inline-citation enforcement at generation time** (HalluHard). The model must emit a citation token at every factual claim, validated against the corpus before output.
- **Citation metadata cross-check.** Before writing, every cited source's metadata (authors, year, venue, DOI) is verified via OpenAlex/Crossref. This eliminates the entire class of GPT-4o-style 78–90% citation hallucinations.
- **Critic step** (peer-review-style). A separate evaluation pass (or a different model) rates the draft against rubric criteria — coverage, citation grounding, uncertainty acknowledgment, gap surfacing — and surfaces issues for revision.
- **Explicit "unknowns" section** in every direct-answer output. Forces the model to say what it does not know rather than smoothing over uncertainty.

### 7.5 Possible Skill 5 — Orchestration / planning

**Design choices justified by prior work.**
- **Lead-orchestrator + parallel-subagent pattern** (Anthropic Research, Robin). The orchestrator decomposes the user's high-level question into sub-tasks, dispatches them to skills 1–4, and assembles the final output.
- **Memory as planning artifact.** The orchestrator's plan is persisted (Anthropic's pattern), so long-running runs survive context shifts and can be resumed/audited.
- **Budget and scope per subagent.** Without explicit budgets, agents over-spawn (Anthropic's reported failure mode). Each invocation of skills 1–4 should carry an explicit scope and stop condition.
- **Don't promise end-to-end discovery.** The user-controlled checkpoints between skills are a feature, not a bug; the 2026 multi-framework evaluation showed end-to-end is still unsolved.

### 7.6 Cross-cutting infrastructure

- **Observability built in.** Log every retrieval, re-rank score, tool call, and prompt/response. Required for debugging and required for PRISMA-trAIce-style reporting.
- **Reproducibility artifact per run.** A machine-readable JSON record with model versions, prompts, queries, decisions, and human overrides. Re-runnable.
- **Failure-aware outputs.** Every skill emits a "what I could not do" section: sources I could not access, fields I could not extract confidently, gaps I could not fill in the corpus.
- **Human-in-the-loop checkpoints between skills.** Default on; full-auto is a flag.
- **Model-agnostic with hot-swappable model choice.** Frontier closed-source by default for extraction and citation work; cheaper models acceptable for summarization and routine tasks. Skills should accept a model parameter and fall back gracefully.

---

## 8. Sources

### Commercial tools and platforms

- [Elicit: AI for scientific research](https://elicit.com/)
- [Comparison of Elicit AI and Traditional Literature Searching in Evidence Syntheses (Cochrane, 2025)](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70050)
- [Evaluating Elicit as a Semi-Automated Second Reviewer for Data Extraction (SAGE, 2025)](https://journals.sagepub.com/doi/10.1177/08944393251404052)
- [Consensus: AI for Research](https://consensus.app/)
- [Use of Generative AI in Academic Research: Review of the Consensus App (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12318603/)
- [scite.ai](https://scite.ai/)
- [scite: A smart citation index that displays the context of citations (QSS / MIT Press)](https://direct.mit.edu/qss/article/2/3/882/102990/scite-A-smart-citation-index-that-displays-the)
- [Undermind](https://www.undermind.ai/)
- [Benchmarking the Undermind Search Assistant (whitepaper)](https://www.undermind.ai/whitepaper.pdf)
- [FutureHouse Platform: Crow, Falcon, Owl, Phoenix](https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents)
- [FutureHouse Tools page](https://www.futurehouse.org/tools)
- [Demonstrating end-to-end scientific discovery with Robin (FutureHouse)](https://www.futurehouse.org/research-announcements/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system)
- [Robin: A multi-agent system for automating scientific discovery (arXiv 2505.13400)](https://arxiv.org/abs/2505.13400)
- [Litmaps vs ResearchRabbit vs Connected Papers comparison](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/)
- [ResearchRabbit 2025 release announcement](https://www.researchrabbit.ai/announcement-researchrabbit-release-2025)
- [OpenAI's deep research tool: is it useful for scientists? (Nature, 2025)](https://www.nature.com/articles/d41586-025-00377-9)

### Open-source agent frameworks

- [PaperQA GitHub](https://github.com/Future-House/paper-qa)
- [Language agents achieve superhuman synthesis of scientific knowledge (PaperQA2 paper)](https://arxiv.org/html/2409.13740v2)
- [PaperQA2 achieves SOTA on RAG-QA Arena science benchmark (FutureHouse)](https://www.futurehouse.org/research-announcements/paperqa2-achieves-sota-performance-on-rag-qa-arena-science-benchmark)
- [OpenScholar (Ai2)](https://allenai.org/blog/openscilm)
- [OpenScholar in Nature (2025)](https://www.nature.com/articles/s41586-025-10072-4)
- [OpenScholar GitHub](https://github.com/AkariAsai/OpenScholar)
- [The AI Scientist (Sakana)](https://sakana.ai/ai-scientist/)
- [The AI Scientist-v2: Workshop-Level Automated Scientific Discovery (arXiv 2504.08066)](https://arxiv.org/abs/2504.08066)
- [Evaluating Sakana's AI Scientist (arXiv 2502.14297)](https://arxiv.org/abs/2502.14297)
- [Stanford STORM](https://github.com/stanford-oval/storm)
- [Assisting in Writing Wikipedia-like Articles From Scratch with LLMs (arXiv 2402.14207)](https://arxiv.org/abs/2402.14207)
- [AutoSurvey (arXiv 2406.10252)](https://arxiv.org/abs/2406.10252)
- [AutoSurvey2 (arXiv 2510.26012)](https://arxiv.org/pdf/2510.26012)
- [Agentic AutoSurvey (arXiv 2509.18661)](https://arxiv.org/abs/2509.18661)
- [ChemCrow (arXiv 2304.05376)](https://arxiv.org/abs/2304.05376)
- [Coscientist: Autonomous chemical research with LLMs (Nature 2023)](https://www.nature.com/articles/s41586-023-06792-0)
- [SciAgents (arXiv 2409.05556)](https://arxiv.org/abs/2409.05556)
- [SciAgent: A Unified Multi-Agent System for Generalistic Scientific Reasoning (arXiv 2511.08151)](https://arxiv.org/abs/2511.08151)
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher)
- [Aviary (FutureHouse)](https://www.futurehouse.org/research-announcements/aviary)
- [Aviary paper (arXiv 2412.21154)](https://arxiv.org/abs/2412.21154)
- [Can AI Conduct Autonomous Scientific Research? (bioRxiv 2026)](https://www.biorxiv.org/content/10.64898/2026.01.05.697809v1.full)
- [Agentic AI for Scientific Discovery: A Survey (arXiv 2503.08979)](https://arxiv.org/html/2503.08979v1)

### Academic literature and benchmarks

- [Automation of Systematic Reviews with Large Language Models (medRxiv 2025)](https://www.medrxiv.org/content/10.1101/2025.06.13.25329541v2.full.pdf)
- [Artificial Intelligence-Assisted Data Extraction with an LLM (Annals of Internal Medicine)](https://www.acpjournals.org/doi/10.7326/ANNALS-25-00739)
- [Collaborative LLMs for Automated Data Extraction in Living Systematic Reviews (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11469465/)
- [Can LLMs Replace Humans in Systematic Reviews? Khraisha et al. (RSM 2024)](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1715)
- [Automated Paper Screening for Clinical Reviews Using LLMs (JMIR 2024)](https://www.jmir.org/2024/1/e48996)
- [SciCode benchmark (arXiv 2407.13168)](https://arxiv.org/abs/2407.13168)
- [BixBench (arXiv 2503.00096)](https://arxiv.org/abs/2503.00096)
- [DeepResearch Bench (arXiv 2506.11763)](https://arxiv.org/abs/2506.11763)
- [GAPMAP: Mapping Scientific Knowledge Gaps (arXiv 2510.25055)](https://arxiv.org/abs/2510.25055)
- [Extracting accurate materials data with conversational LMs and prompt engineering (Nature Communications 2024)](https://www.nature.com/articles/s41467-024-45914-8)
- [Structured information extraction from scientific text with LLMs (Nature Communications 2024)](https://www.nature.com/articles/s41467-024-45563-x)
- [How Well Do LLMs Understand Tables in Materials Science?](https://link.springer.com/article/10.1007/s40192-024-00362-6)
- [34 Examples of LLM Applications in Materials Science and Chemistry (arXiv 2505.03049)](https://arxiv.org/html/2505.03049)
- [PRISMA-trAIce checklist (JMIR AI 2025)](https://ai.jmir.org/2025/1/e80247)
- [AI to Automate Network Meta-Analyses (PharmacoEconomics-Open)](https://link.springer.com/article/10.1007/s41669-024-00476-9)
- [Meta-Mar: AI-assisted meta-analysis](https://www.meta-mar.com/)

### Methodology, hallucination, RAG

- [Long Context vs. RAG for LLMs: An Evaluation and Revisits (arXiv 2501.01880)](https://arxiv.org/abs/2501.01880)
- [LaRA: Benchmarking RAG and Long-Context LLMs (OpenReview)](https://openreview.net/forum?id=CLF25dahgA)
- [RAG or Long-Context LLMs? A Comprehensive Study and Hybrid Approach (arXiv 2407.16833)](https://arxiv.org/abs/2407.16833)
- [Seven Failure Points When Engineering a Retrieval Augmented Generation System (arXiv 2401.05856)](https://arxiv.org/abs/2401.05856)
- [Mitigating Hallucination in LLMs: Survey on RAG, Reasoning, and Agentic Systems (arXiv 2510.24476)](https://arxiv.org/html/2510.24476v1)
- [Why Meta's Galactica only survived three days online (MIT Tech Review)](https://www.technologyreview.com/2022/11/18/1063487/meta-large-language-model-ai-only-survived-three-days-gpt-3-science/)
- [Galactica: A Large Language Model for Science (arXiv 2211.09085)](https://arxiv.org/abs/2211.09085)
- [OpenAlex (arXiv 2205.01833)](https://arxiv.org/abs/2205.01833)
- [Research Paper APIs for Scientific Literature in 2026 (IntuitionLabs)](https://intuitionlabs.ai/articles/research-paper-apis-scientific-literature)

### Architectural patterns

- [How we built our multi-agent research system (Anthropic Engineering)](https://www.anthropic.com/engineering/multi-agent-research-system)
- [When to use multi-agent systems (Claude blog)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- [Top 10 Deep Research Agents in 2025](https://alici.ai/blog/top-deep-research-agents-2025)

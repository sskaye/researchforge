# Tool Fit for ResearchForge Use Cases

Companion to [`literature_search_methods_review.md`](literature_search_methods_review.md). The main review surveyed the landscape of literature-search methods, tools, and methodology in general. This document is the practical follow-on: how well do existing tools fit the specific use cases ResearchForge is being designed to support, and what does that imply for the source-search-and-compilation skill?

Four use cases are considered:

1. Building a persistent on-disk corpus for downstream extraction and analysis.
2. Property-database construction: high-recall corpora of papers measuring a specific physical/chemical property, narrow enough to feed a slow extraction tool without waste.
3. Extrapolative feasibility questions: synthesizing across adjacent literatures to address a question that no single paper answers directly.
4. Reproducible benchmark evaluation of tools and of any skill we build.

The cross-cutting observation is that existing AI search products are well-fit to a fifth use case — answering a question from the literature — that ResearchForge does not principally need, while none of them is well-fit to the four use cases above.

---

## 1. Persistent corpus building: do existing tools download papers?

### Finding

Most existing AI search tools are search-and-answer tools, not corpus-acquisition tools. They return ranked papers with metadata, sometimes deliver an answer with citations, and rely on the user or a reference manager to handle persistence. None of them autonomously assembles a downloadable on-disk corpus of full-text papers.

**[PaperQA2](https://github.com/Future-House/paper-qa) is BYO-corpus.** It operates on a local directory of PDFs the user provides — the `pqa` CLI parses and caches them into a full-text search index, fetches metadata from Crossref and Semantic Scholar, and answers against the indexed library ([Future-House/paper-qa "Where do I get papers"](https://github.com/Future-House/paper-qa/blob/main/docs/tutorials/where_do_I_get_papers.md)). A Zotero integration pulls papers from a configured Zotero library into the `Docs` object. An unofficial `paper-scraper` companion exists but is explicitly flagged as gray-area-legal scraping. PaperQA2 does not autonomously acquire new full-text PDFs from publishers.

**Elicit, Consensus, Undermind, FutureHouse Crow/Falcon/Owl, OpenAI/Anthropic/Gemini/Perplexity Deep Research, SciSpace Deep Review, OpenRead, AnswerThis** all return answers and citations, sometimes with linked PDFs, but none of them delivers a persistent on-disk corpus.

**[OpenScholar](https://github.com/AkariAsai/OpenScholar) is different in kind:** it queries a fixed 45M-paper datastore that Ai2 built and hosts. The datastore is not a corpus you can re-use locally — you can pull individual papers' metadata via the open-source code, but the canonical workflow is "use OpenScholar to answer; don't take the corpus home."

**Reference managers** (Zotero, EndNote, Mendeley) persist papers when configured, but they're triggered by user action, not by search.

**Citation-graph tools** (ResearchRabbit, Litmaps, Connected Papers) integrate with Zotero, which is the closest the AI-search ecosystem comes to corpus building — but the actual download path is still the user's reference manager, not the tool itself.

### What is closest to the right pattern

The existing `codex_search/` workflow in this repository (built for the MP/BP corpus) is closer to the right pattern than any commercial tool: Europe PMC `fullTextXML` and PMC OA package APIs to fetch full XML, plus SI download fallbacks via the NCBI OA Package service, plus a manifest with DOIs and provenance for everything. The publisher-OA equivalents — arXiv bulk, Crossref + Unpaywall resolution, [Springer Nature OA API](https://dev.springernature.com/), [OSF API](https://developer.osf.io/), DOE OSTI, NASA NTRS, IAEA INIS, Zenodo — would extend the same pattern to non-biomedical and non-journal sources.

### Implication

The skill should treat "downloaded full text on disk" and "metadata record only, with a resolvable URL" as a first-class output distinction. Downstream extraction and summarization skills need full text; downstream report skills can work from metadata for citation purposes. The output manifest should make the distinction explicit and recoverable.

---

## 2. Citation export from existing tools as a corpus seed

Many AI search tools do produce a citation/DOI list that can be used as input to a separate download step, even if they don't download papers themselves.

### Tools with structured DOI exports

- **[Elicit](https://support.elicit.com/en/articles/1153857)** — CSV / RIS / BibTeX export from Find Papers and Extract Data screens. CSV includes title, authors, DOI, and DOI link. Capped at 500 papers per project.
- **[Consensus](https://help.consensus.app/en/articles/9922811-how-to-export-consensus-results-to-reference-managers-endnote-zotero-paperpile)** — CSV / RIS export from search results and from saved Library/Collections.
- **Undermind** — BibTeX / RIS export; Pro tier can push directly to reference managers and screening platforms.
- **PaperQA2 (open source)** — every citation in the answer object carries the DOI; the `gather_evidence` intermediate step is programmatically accessible, so you can extract the full retrieved set (~12 candidates per search call by default), not just the cited subset.
- **FutureHouse Crow / Falcon / Owl API** — built on PaperQA2; responses are structured with DOI-bearing citations.
- **OpenScholar** — fully open source; structured citation outputs.
- **SciSpace, R Discovery, AnswerThis, Scinapse, OpenRead** — RIS / BibTeX export from results.
- **ResearchRabbit, Litmaps, Connected Papers** — Zotero / RIS / BibTeX export of citation-graph expansions; particularly useful because they surface papers keyword tools miss.

### Tools where it's messier

- **Perplexity Deep Research, OpenAI Deep Research, Anthropic Claude Research, Gemini Deep Research** — cite web URLs inline, not always DOIs. Extraction is possible but requires a normalization pass (URL → DOI via Crossref content negotiation or Unpaywall) before the list is useful.
- **NotebookLM** — closed-corpus only; not relevant.

### Three caveats

**Cited set ≠ retrieved set.** Most tools export only the cited papers (the small subset that survived re-ranking). For corpus building you want the wider retrieved pool. PaperQA2 and FutureHouse Crow are the only ones where the wider set is programmatically exposed.

**A DOI list is not a corpus.** Each DOI still has to be resolved to full text. The realistic pipeline is DOI → [Unpaywall](https://unpaywall.org/products/api) (OA status and best OA URL) → if OA, fetch via Europe PMC `fullTextXML`, arXiv ID, publisher OA API, or PDF; if not OA, record the DOI with `access: paywalled` and stop. The existing `codex_search` workflow already does most of this for Europe PMC; generalizing it to handle arXiv, OSF, OSTI, NTRS, Zenodo, and the publisher OA APIs is a finite amount of adapter code.

**Delegating to AI tools may not beat calling the underlying APIs.** Elicit and Consensus run on Semantic Scholar + OpenAlex; PaperQA2/FutureHouse run on Crossref + Semantic Scholar. For a given Boolean or topic query you can usually get a longer and more controllable list by hitting OpenAlex or Semantic Scholar directly. AI tools add value when their re-ranking or iterative agentic loop is what you want — Undermind's saturation-driven recall is hard to replicate without an agent.

### Implication

Treat AI-tool exports as one input modality among several (alongside OpenAlex/Crossref/Semantic Scholar direct queries and citation-graph expansion). Normalize all of them to a unified DOI-plus-metadata schema, deduplicate, then run a single OA-resolution + download pass against the merged list.

---

## 3. Property-database construction

### The use case

The MP/BP corpus build (the existing `codex_search/` workflow plus the working `mp-bp-extraction` skill) is the prototype. The general form: given a measurable property of small molecules (oxidation potential, redox potential, pKa, solubility, vapor pressure, thermal conductivity, heat capacity, etc.), assemble a corpus of papers that *measure that property*, high recall against the universe of measurement-bearing papers, with enough precision that the slow extractor does not get bogged down processing tons of papers that lack the data. The corpus is the input to extraction, not the deliverable.

The success criterion is sharply different from any AI-search product's design point. AI search products optimize *precision-at-top-k on a question*; this task optimizes *recall over a content type*, where the content is a measured numeric value tied to a compound, almost always buried in body text, tables, captions, or supplementary information.

### Why existing AI tools don't fit

- **Elicit** caps at 500 papers per project; a single property would burn the cap with no headroom for the long tail. Sensitivity is also weak — the Lau et al. 2025 Cochrane number (39.5% average sensitivity) was on a question, an easier task than this.
- **Consensus** is yes/no oriented and aggressively truncates to top-20. Wrong framing.
- **Undermind** is the closest in spirit — its iterative classifier with a saturation stop condition is the right shape — but its published gold-standard recovery is 30–80%. Even at the top of that range you would be missing 20% of the corpus, and you cannot inspect or audit the gaps.
- **PaperQA2 / FutureHouse Crow** return at most ~12 candidates per search call by design. The agent stops once it can answer, not when it has covered the literature.
- **FutureHouse Owl** is the closest single product — framed for prior-art recall — but it is recall on a question, not recall on a content type.
- **Deep Research products** are brief-writers, not corpus-builders.

The deeper issue is that property data is rarely in the title or abstract. It is in body text, tables, captions, and very often only in supplementary information. Most AI search tools index abstracts only, or query indexes (Semantic Scholar, OpenAlex) that don't expose full text in the search field. They systematically miss papers where the property is in the SI — which the MP/BP audit showed is a substantial fraction of MP/BP positives.

### Why `codex_search` is the right architecture

The MP/BP work shows that the right architecture is:

1. **Multi-source API-driven candidate discovery** with full-text-searchable open APIs — Europe PMC `OPEN_ACCESS:y HAS_FT:y` queries with multiple complementary query families biased toward recall.
2. **Bulk download** of full text (JATS XML, PDF, normalized text).
3. **Property-specific presence filtering** — positive patterns, negative patterns, table-aware matching, SI fallback route — to prune the recall-biased candidate set to a ≥90%-precision accepted set.
4. **Reproducible audit harness** to measure precision and (where possible) recall on labeled samples.

The MP/BP run hit 92.3% post-filter precision on a 300-paper audit — exactly the kind of guarantee an expensive downstream extractor needs. The architecture is sound. What is missing is parameterization for arbitrary properties.

### Generalizing the codex_search pattern across properties

Three changes turn the MP/BP pipeline into a general property-corpus tool.

**Source coverage broader than Europe PMC.** For MP/BP, Europe PMC's OA chemistry coverage was adequate. For oxidation potential and electrochemistry the same Europe PMC core plus arXiv (cond-mat, physics.chem-ph), ChemRxiv, the Semantic Scholar full-text bulk index, and — where license allows — the Springer Nature OA API, Wiley TDM (with institutional auth), and Elsevier TDM. For some properties, NIST WebBook, PubChem, ChEMBL, Materials Project, OQMD, and NOMAD are worth a separate "data-repository-first" pass because querying them directly is more efficient than extracting from papers for compounds the databases already cover.

**Property-specific configuration as the unit of variation.** The recommendations in `AGENT_SKILL_RECOMMENDATIONS.md` already sketch this — a per-property YAML with `target_terms`, `abbreviations`, `value_patterns`, `positive_context`, `negative_context`, `audit.sample_size`, `precision_target`. The skill itself stays the same; what varies is the property configuration. For oxidation potential a starter config would be `target_terms` = `oxidation potential`, `redox potential`, `half-wave potential`, `E_1/2`, `E_ox`, `anodic peak potential`, `formal potential`, `redox couple`; `positive_context` = `cyclic voltammetry`, `CV`, `electrode`, `vs Ag/AgCl`, `vs Fc/Fc+`, `vs SHE`, `vs NHE`, `vs SCE`, where reference-electrode mentions are a high-signal positive marker; `negative_context` = `membrane potential`, `action potential`, `oxidation state`, `oxidation reaction`. The redox-extraction skill in the archive supplies a controlled vocabulary for free.

**LLM-assisted config generation and refinement.** First-pass configs are human-written. Subsequent ones can be LLM-bootstrapped from a small seed corpus of known-positive papers (the same word-frequency-harvesting pattern as SR-Accelerator's Word Frequency Analyser, but parameterized for the property). An audit cycle refines the config.

### Where existing tools genuinely help, as supplements

- **Undermind in saturation mode as a recall-augmenter** after the keyword pipeline runs. Feed it the property description, harvest its DOI list, dedup against the keyword corpus, send new DOIs through the same download-and-filter pipeline. Catches papers where the terminology shifted ("regenerative fuel cell" vs. "redox flow battery") that keyword search misses.
- **Citation-graph expansion** via OpenAlex `referenced_works` / `cited_by` and Semantic Scholar `/references` and `/citations` from a confirmed-positive seed set. Adds papers no keyword query would have surfaced because the property is not in the title/abstract but the paper inherits its lineage from one that does.
- **LLM-driven false-positive class enumeration.** Show the LLM a labeled-invalid sample from a property's first audit; ask it to enumerate the false-positive patterns and propose negative-context regexes. Faster than enumerating by hand; the audit catches it if the LLM over-prunes.

### Structural problems that remain

**Chemistry literature is heavily paywalled.** JACS, Angew Chem, J Org Chem, J Electrochem Soc, J Phys Chem — most canonical electrochemistry venues require TDM agreements for full text. The OA-only pipeline will systematically under-cover these. For a "comprehensive" database the skill should flag this explicitly so the user knows what fraction of likely positives is unreachable, and provide a path to ingest individual papers the user supplies as PDFs from their institutional access. The `codex_search` pattern of returning a `rejected_or_unresolved_manifest` is exactly right — the user can see what is missing.

**Books and handbooks are the elephant in the room.** The CRC Handbook, Lange's Handbook, NIST tables, and the various Knovel-hosted reference works contain larger curated property databases than any plausible paper-extraction run will assemble for properties they cover. For some properties the smart move is to query those data repositories first (Materials Project, NIST WebBook, PubChem, ChEMBL, OQMD, NOMAD) and use paper extraction as the complementary route for compounds the databases miss. Two parallel intake paths, not alternatives.

### Recommendation

Don't try to make any of the AI tools serve this purpose. Generalize `codex_search`. The skill spec is roughly: per-property config → multi-source full-text-aware candidate discovery → bulk download → property-specific presence filter with SI fallback → audit harness → outputs (accepted corpus, rejected manifest, audit report, coverage report flagging paywalled-likely-positives). Use Undermind-style agentic recall augmentation and citation-graph expansion as add-on modes for property terms that don't keyword-search well. Query domain databases (NIST, PubChem, Materials Project, ChEMBL) as a parallel intake path where they exist.

---

## 4. Extrapolative research questions: synthesizing across adjacent literatures

### The use case

The example from the user: assess the feasibility of an aluminum-air fuel cell using small aluminum pellets. Unpacked, the question requires drawing on three (or more) adjacent literatures:

- Pellet anode geometry has been studied for **zinc-air** systems. The lessons there — particulate-electrode kinetics, current collection, dendrite/passivation behavior, electrolyte management — partially transfer.
- **Aluminum anodes** have been studied in foil, slurry, and dispersed-particulate forms. The lessons there — passivation by Al₂O₃, parasitic corrosion, hydrogen evolution, alloy additives (In, Ga, Sn, Mg, Bi) — are about aluminum's electrochemistry independent of geometry.
- **Air electrodes** have been studied across a wide range of anode chemistries (Zn, Li, Mg, Fe). Mass transport, ORR catalysts, water management, flooding/drying behavior generalize across anodes.

No single paper answers the target question. The literature *can* answer it — by combining the three threads and reasoning explicitly about transferability of each lesson to the Al-pellet case.

This is fundamentally different from:

- A direct factual question ("what is the oxidation potential of X").
- A systematic review on a single specified topic.
- A prior-art search on a specific claim ("has anyone built an Al-air pellet cell").

It is a *speculative feasibility synthesis* that requires:

1. **Decomposition** — identify the adjacent threads relevant to the question.
2. **Per-thread retrieval** — gather the relevant literature in each thread.
3. **Cross-thread synthesis** — pull the constraints and learnings from each thread.
4. **Transferability reasoning** — for each lesson, articulate whether and how it transfers to the target case.
5. **Unknowns surfacing** — make explicit what would have to be established to bridge each thread to the target.

`docs/goals.md` already names this exact use case (the aluminum-vs-zinc fuel example) as the target for the planned **question-driven assessment** sub-skill of the analysis-and-report skill. So the synthesis side is in scope by design. The question is whether the *search* side can support it, and whether any existing tool already does.

### How well do existing tools do this?

**Deep Research products (OpenAI, Anthropic, Gemini, Perplexity Deep Research)** are the only commercial products *built* for this kind of synthesis question. They produce long-form briefs that draw on multiple sources and can handle "compare aluminum to zinc" or "what would it take to build X" framings. But they have specific failure modes for this use case:

- *Citation quality is suspect.* The OpenScholar Nature paper documented GPT-4o-class hallucination at 78–90% of citations without grounding. The Deep Research products improve on this by grounding in real searches, but citation accuracy is still demonstrably below open-source citation-grounded RAG (PaperQA2, OpenScholar) by published benchmarks.
- *No explicit thread decomposition.* They tend to fuse the threads into a single synthesized brief without naming the adjacencies. For an expert reader the value is precisely in seeing the threads, the transferability arguments, and where they fail.
- *Bias toward over-confident synthesis.* They are RL-trained to produce decisive briefs, not to surface gaps. The "unknowns" section, if any, tends to be perfunctory.
- *No corpus deliverable.* They produce a brief, not a thread-organized reading list the user can read themselves to form their own judgment.
- *Web-search, not scholarly-search.* They search the open web. Coverage of scholarly literature is incidental to their pipeline.

**FutureHouse Falcon** is the most academically-credentialed of the deep-review products, with access to specialized databases (e.g., OpenTargets) on top of the Crow PaperQA2 core. It is designed for *deep reviews on a topic*, not for extrapolative feasibility. It would produce a strong review of, say, aluminum-air fuel cells in general — but not a structured analysis of which adjacencies do and don't transfer to a pellet-fed variant. The architecture is closer to a STORM-like generator than a thread decomposer.

**[STORM and Co-STORM](https://storm-project.stanford.edu/research/storm/) (Stanford OVAL)** have the closest *architectural* fit. STORM's pre-search step explicitly imagines multiple perspectives by surveying related articles and simulating writer↔expert conversations, then drives retrieval per perspective. For the Al-air pellet question this would naturally yield perspectives corresponding to the Zn-pellet expert, the Al-anode chemist, and the air-electrode specialist, and run a query family per perspective. STORM is not a polished consumer product, but the pattern it implements is the right one for the search layer of this use case. Co-STORM's human-in-the-loop turn protocol over a dynamic mind map is the right control surface for an expert who wants to inspect and edit the threads before retrieval runs.

**[Undermind](https://www.undermind.ai/)** can be made to work if you decompose the question by hand and run it three times — once per thread. Saturation-driven recall is well-suited to each thread, and the union of three runs would produce a defensible thread-organized reading list. The decomposition is not automatic; the user (or a wrapper skill) has to identify the threads. Output is a per-thread paper list, not a synthesis.

**[PaperQA2](https://github.com/Future-House/paper-qa) / FutureHouse Crow** answer well-specified questions with citation-grounded synthesis, but their default candidate budget per search call (~12) and their tendency to stop once they can answer make them poor at the recall side of an extrapolative search. They can be invoked per thread, but each invocation will short-circuit on the first answerable framing.

**[AnswerThis](https://answerthis.io/)** explicitly frames itself around research-gap finding. For the Al-air pellet question it would likely surface the gap honestly ("no published work combining Al + pellets + air cathode"), which is half the answer. It does not do the cross-thread transferability reasoning. Useful as a sanity check.

**Citation-graph tools (ResearchRabbit, Litmaps, Inciteful, Connected Papers)** are valuable here in a specific way: from a seed paper on Zn-pellet you can find neighborhoods that include Al variants or pellet-on-other-chemistries variants that pure keyword search would miss. Treat them as a thread-completion tool, not as the primary search.

**Specialized chemistry agents (ChemCrow, Coscientist)** are about experimental planning and execution, not literature synthesis. Not relevant to this use case as currently designed.

**Conventional indexes** (Web of Science, Scopus, Engineering Village) handle each thread well via Boolean queries with thread-specific concept blocks (e.g., `(aluminum air OR Al-air) AND (anode OR pellet OR particulate)`). They have the controlled vocabularies (INSPEC for electrochemistry/EE; CAS for chemistry; Compendex for engineering) that AI-only tools lack. For an extrapolative question, querying each thread in WoS/Scopus and unioning the results is a defensible baseline — what you lose is the iterative agentic refinement and the cross-thread synthesis. Both are skill-level adds.

### Honest verdict for this use case

**No single existing tool does the full workflow.** The tools cluster into three groups, each of which addresses a different sub-step:

- *Brief writers* (Deep Research products, FutureHouse Falcon) produce synthesized text but obscure the thread decomposition and have weak citation quality.
- *Multi-perspective searchers* (STORM/Co-STORM) decompose well at the search layer but stop short of the transferability synthesis.
- *Per-thread recall engines* (Undermind, citation-graph tools, conventional indexes) produce strong per-thread reading lists when the user supplies the thread decomposition.

The closest thing to a working end-to-end product is "use Co-STORM to decompose and search; use Undermind to deepen recall per thread; use Falcon or Claude Research to draft the synthesis from the union." That pipeline is not packaged anywhere. It is also not a substitute for an expert reading the per-thread reading lists themselves — the value of this use case is precisely in the reader's judgment about which adjacencies transfer.

### Implication for ResearchForge

The source search and compilation skill needs an explicit **research-question mode** in addition to the prior-art, evidence-on-question, and full-corpus-review modes already discussed in the main review. The research-question mode is characterized by:

- **Thread-first decomposition.** Before running any queries, the skill helps the user articulate the adjacent threads relevant to the question. This is the STORM-perspective-generation step lifted to the search layer. A first pass can be LLM-generated and presented for user edit; the user's domain expertise is what makes the thread set right.
- **Per-thread query families.** Each thread gets its own query family across the same multi-source backbone (OpenAlex + Semantic Scholar + arXiv + relevant domain repositories). Threads are searched independently with their own saturation criteria.
- **Thread-tagged corpus output.** The output corpus carries thread tags on every paper, not just a flat list. The downstream report skill consumes this structure for thread-organized synthesis.
- **Explicit unknowns surfacing.** For each thread, the skill should flag what was *not* found — the bridge papers that would have made the adjacency direct rather than analogical. AnswerThis's gap-finding framing is the right shape for this.
- **No premature synthesis.** The search skill stops at thread-tagged corpus + per-thread retrieval reports. Synthesis is a separate skill (question-driven assessment) so the user can read each thread before accepting any synthesis.

This use case is also the one that most directly justifies the **possible fifth orchestration skill** mentioned in `goals.md`. The natural Robin-style pattern would be a lead orchestrator that takes the user's question, decomposes into threads, dispatches a search-skill invocation per thread, runs the summarization skill on each per-thread corpus, and then invokes the question-driven assessment report skill with the per-thread summaries plus the explicit transferability reasoning. The four skills (search, summarize, extract, report) plus the orchestrator together address this use case in a way no single existing product does.

### A practical first test

A useful concrete test for this use case once the skill exists: take a feasibility question the user already has a strong prior on (the aluminum-vs-zinc-pellet question is well-suited, since the user has domain expertise and could rate the output), run a Deep Research product alongside the skill, and compare on three axes: thread decomposition quality (did each tool identify the right adjacencies?), per-thread retrieval quality (did the reading lists feel comprehensive to a domain expert?), and synthesis quality with explicit unknowns (did the output flag what would need to be established to bridge each thread?). This is a small but defensible bake-off and would give the project an early empirical signal on whether the architecture pays off.

---

## 5. Benchmark reproducibility

The main review listed the benchmarks. The practical question is which can be run today against existing tools and any skill we build.

### Open and runnable today

- **[LitQA2](https://github.com/Future-House/LitQA)** — multiple-choice scientific questions answerable only from full-text papers. The dataset and evaluation are open and straightforward to run.
- **[ScholarQABench](https://github.com/AkariAsai/ScholarQABench)** — 2,967 expert queries and 208 long-form answers across CS, physics, neuroscience, biomedicine, with a published evaluation pipeline (Prometheus rubric eval, citation precision/recall F1, multi-aspect rubric scoring). Most directly relevant to ResearchForge's physical-sciences scope.
- **[RAG-QA Arena](https://github.com/awslabs/rag-qa-arena)** (AWS Labs) — reproducibility code published, results downloadable, human-judgment-correlation code shipped.
- **[BixBench](https://arxiv.org/abs/2503.00096)** — agentic computational biology benchmark; less directly relevant to physical-sciences scope, but available.
- **MisciteBench** (BibAgent, [arXiv 2601.16993](https://arxiv.org/abs/2601.16993)) — 6,350 miscitation samples across 254 fields; targets citation verification.

### Hard or impossible to reproduce as packaged

- **The Lau et al. 2025 Cochrane evaluation of Elicit** ([Wiley DOI](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70050)) is a methodology, not a packaged benchmark. Reproducing the experiment requires picking new systematic-review reference sets and re-running the methodology. Significant work, but doable, and arguably the most informative thing the project could do for a search-and-compile skill.
- **The Undermind whitepaper benchmark** is internal — the ~400 manually graded papers are not released.
- **Engineering-domain gold-standard reference sets** essentially do not exist as packaged benchmarks. The published evaluations are biomedical.

### A two-tier evaluation harness

A reasonable evaluation harness for ResearchForge would have two tiers.

**Tier A — direct benchmark runs.** Pull LitQA2 + ScholarQABench + the science split of RAG-QA Arena. For each, run (i) the ResearchForge skill, (ii) any existing tool with an API (PaperQA2 / FutureHouse Crow free-tier API; OpenScholar open-source; Perplexity API), and (iii) compare on retrieval precision/recall, citation accuracy, and rubric scores. Direct comparability against the strongest published numbers and against PaperQA2 specifically.

**Tier B — a Cochrane-style recall evaluation built in-house.** Pick five to ten published systematic reviews in physical sciences and engineering with public reference lists (PRISMA flow diagrams generally publish the included-studies set). Run the skill in full-corpus-review mode against the same research question. Compute gold-standard recovery against the SR's included set. Directly comparable to the Lau 39.5% Elicit number and to Undermind's 30–80%, but on engineering corpora where these numbers don't currently exist.

Tier A is a few days of wiring against open evaluation code with caching for re-runs. Tier B is roughly a week of corpus curation per SR pulled in. Tier B is where the differentiating evidence will come from — Tier A lets the project match the field, Tier B lets it claim something the field has not measured.

### Implication

Build the evaluation harness alongside the skill, not after. The harness is itself a deliverable, and the published Tier-B numbers on engineering corpora would be a meaningful methodological contribution independent of the skill.

---

## 6. Cross-cutting observations

A few patterns visible across the four use cases.

**The AI-search product category is monoculture-ish on success criterion.** Almost every commercial AI search product is optimized for the same task: precision-at-top-k on a user question, with a synthesized answer. The four use cases above all want something different — corpus building, content-type recall, cross-thread synthesis, recall-against-gold-standard evaluation. The market gap is real because the dominant product framing has converged on a different problem.

**Open infrastructure is the lever.** OpenAlex, Crossref, Semantic Scholar, Europe PMC, arXiv, DataCite, plus the public-domain APIs of the government technical-report services (DOE OSTI, NASA NTRS, IAEA INIS, USGS, EPA) and the open data repositories (Materials Project, NIST WebBook, PubChem, ChEMBL) together cover most of what the use cases need without depending on any commercial AI product. The compositional layer — the skill — is where the work lives. The infrastructure is in place.

**Audit harnesses are not optional.** Three of the four use cases need an audit step to be credible — property corpora need precision and recall numbers, extrapolative searches need to know whether the threads were covered, benchmark evaluation is *itself* an audit. The MP/BP work has the right pattern: a reproducible random sample, manual labels with reason categories, computed precision, Wilson confidence intervals, invalid-category breakdowns. Generalize this and reuse it everywhere.

**Mode parameters do real work.** The same retrieval primitives (multi-source candidate discovery, hybrid retrieval, cross-encoder rerank, citation-graph expansion) compose into very different products depending on the budget, the stop condition, and what counts as success. FutureHouse demonstrates this externally (Crow vs. Falcon vs. Owl). ResearchForge should do the same internally — one search skill with explicit modes (prior-art, evidence-on-question, full-corpus-review, property-corpus, research-question), each with its own defaults.

---

## 7. Implications for the source search and compilation skill

Synthesizing this discussion plus the main review:

1. **Five modes**, not one: *prior-art* (Owl-style, recall-favoring, saturation stop); *evidence-on-question* (Consensus-style, top-k precision); *full-corpus-review* (Falcon-style, completeness within scope, PRISMA-S-grade audit); *property-corpus* (codex_search-style, content-type recall with property-specific config); *research-question* (STORM-style thread decomposition).

2. **Open-infrastructure spine**: OpenAlex + Crossref + Semantic Scholar + arXiv as the cross-cutting default; add Europe PMC for biomed adjacencies; add domain repositories (NASA ADS, INSPIRE-HEP, IEEE Xplore where licensed, DOE OSTI, NASA NTRS, IAEA INIS, Materials Project, NIST WebBook, PubChem, ChEMBL) by query type.

3. **Download is a first-class output stage.** Resolve every DOI via Unpaywall; fetch full text via Europe PMC, arXiv, OSF, OSTI, Zenodo, publisher OA APIs, and other OA routes; emit a manifest that distinguishes downloaded full text from metadata-only records with paywalled-likely-positive flagging. The codex_search pattern of `accepted_manifest`, `rejected_or_unresolved_manifest`, and an SI fallback route is the right starting shape.

4. **Property-corpus mode generalizes `codex_search`.** Per-property YAML config; reuse the audit harness; treat the property's domain database (NIST/PubChem/Materials Project/ChEMBL etc.) as a parallel intake path where one exists.

5. **Research-question mode is the differentiated use case.** STORM-style thread decomposition with user-edit checkpoint; per-thread retrieval with thread tags on output; explicit unknowns surfacing per thread; no premature synthesis — that is a separate skill.

6. **Citation export from AI tools is one input modality.** Treat Elicit/Consensus/Undermind/PaperQA2/FutureHouse exports as ingestion sources, normalize to the unified DOI-plus-metadata schema, dedupe and re-rank with the rest of the corpus. Useful especially for recall augmentation in property-corpus mode and for thread completion in research-question mode.

7. **Audit harness from day one.** Reproducible random sampling, manual-label support with reason categories, precision + (where possible) recall + Wilson CIs, invalid-category breakdowns. The MP/BP audit logic is reusable as-is; package it as part of the skill rather than as ad-hoc scripts.

8. **Two-tier evaluation harness, scoped as a deliverable.** Tier A against open benchmarks (LitQA2, ScholarQABench, RAG-QA Arena science split); Tier B against curated physical-sciences and engineering systematic-review gold-standard reference sets. Tier B is the differentiating piece — those numbers don't currently exist in the literature.

9. **Coverage report on every run.** Explicit "what we did not search" — paywalled sources skipped, language/date filters, TDM agreements not granted, books and standards behind closed paywalls. The user should know the shape of the gap.

10. **Zotero as the durable persistence store.** Output CSL-JSON via the Zotero Web API or translation-server; tag with search provenance; the user can open the library in any Zotero client. Avoids re-inventing the reference-management layer.

The headline implication is that ResearchForge's source-search-and-compilation skill is not a single search agent — it is a *compositional infrastructure* with mode-specific defaults, sitting on top of an open scholarly metadata layer, with first-class download, audit, and coverage-reporting outputs. The pieces all exist. The work is in the composition, the property-config generalization of `codex_search`, the thread-decomposition for research-question mode, and the two-tier evaluation harness.

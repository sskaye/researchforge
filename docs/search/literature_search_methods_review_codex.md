# Literature Search and Source Compilation Methods Review

Date: 2026-05-17

Purpose: review methods, tools, and agentic workflows that can inform a ResearchForge source-compilation skill. The intended skill should find and document scientific sources broadly: journal articles, preprints, books, theses, datasets, patents, standards, government and institutional reports, clinical/regulatory records, and discipline-specific databases.

## Executive summary

Literature searching has two overlapping traditions that should both inform ResearchForge.

The first is conventional systematic searching: a protocol-driven, reproducible process using structured search strings, controlled vocabularies, multiple bibliographic databases, search peer review, de-duplication, transparent screening, and final reporting. The strongest anchors are the Cochrane Handbook, PRISMA-S, PRISMA 2020, PRESS, JBI, Campbell, and grey-literature guidance such as CADTH Grey Matters. These methods are designed for defensibility, not speed.

The second is exploratory discovery: citation chasing, "pearl growing", semantic search, recommendation systems, literature maps, expert consultation, web search, and AI-assisted query expansion. These methods often find material missed by database Boolean queries, especially interdisciplinary, older, non-journal, or poorly indexed material. They are useful but harder to audit unless every search, model suggestion, source decision, and candidate record is logged.

The source-compilation skill should combine both traditions:

- Start with an explicit source protocol and inclusion criteria.
- Use conventional database/API searches as the recall backbone.
- Use AI and graph methods for term expansion, citation expansion, gap detection, and triage, but never as an unlogged black box.
- Search outside journal repositories by default when the research question could depend on books, datasets, patents, standards, government reports, regulatory documents, theses, preprints, or domain databases.
- Validate each run against seed sources, duplicate independent routes, and a documented audit sample.

The existing `docs/search/codex_search` workflow already demonstrates several valuable behaviors: redundant query families, official API/package routes, evidence snippets before acceptance, manual verification, rejection manifests, and final consistency checks. The next source-compilation skill should generalize these into a source-agnostic search protocol with provenance-rich manifests.

## Review method

This review used targeted web searches and source checks on 2026-05-17. Priority was given to primary or authoritative sources: official guidelines, official tool documentation, open-source repositories, APIs, and peer-reviewed articles. AI tools and commercial platforms are included as examples, not endorsements.

Key source classes reviewed:

- Search conduct and reporting guidelines: Cochrane, PRISMA-S, PRISMA 2020, PRESS, JBI, CADTH, Campbell.
- Programmable scholarly indexes: PubMed/NCBI E-utilities, Europe PMC, Crossref, OpenAlex, Semantic Scholar, DataCite.
- Conventional databases and search platforms: PubMed, Embase, Scopus, Web of Science, IEEE Xplore, ACM Digital Library, ProQuest, Google Scholar, Google Books, WorldCat, library catalogs.
- AI-assisted discovery and mapping tools: Elicit, Consensus, Semantic Scholar, ResearchRabbit, Connected Papers, Litmaps, scite, Inciteful.
- Review automation tools: ASReview, Rayyan, Covidence, EPPI-Reviewer, RobotReviewer-style classifiers.
- Agentic/open-source systems: PaperQA2, OpenScholar, STORM, ScholarQA-style literature question answering.
- Non-journal source routes: books, theses, grey literature, trial registries, patents, standards, datasets, chemical/property databases, regulatory records, and institutional repositories.

## Method families

### 1. Protocol-driven systematic search

The conventional high-reliability pattern is:

1. Define the question, scope, source types, date/language limits, inclusion/exclusion criteria, and stopping rules.
2. Select databases and non-database sources.
3. Build search concepts and synonyms, including controlled vocabulary where available.
4. Test search strings against known relevant seed records.
5. Peer review the search strategy.
6. Run searches, export records, and save exact query strings, dates, platforms, result counts, and filters.
7. De-duplicate.
8. Screen titles/abstracts, then full texts.
9. Report the process using a flow diagram and search-strategy appendix.

Useful references:

- The [Cochrane Handbook chapter on searching](https://training.cochrane.org/handbook/current/chapter-04) emphasizes searching multiple information sources, documenting methods, and combining database searching with other methods.
- [PRISMA 2020](https://www.prisma-statement.org/prisma-2020) gives the overall reporting structure for systematic reviews, including flow diagrams.
- [PRISMA-S](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-020-01542-z) extends PRISMA for literature-search reporting: database names, platforms, full strategies, limits, dates, and deduplication.
- [PRESS](https://www.cadth.ca/press-peer-review-electronic-search-strategies-2015-guideline-statement) formalizes peer review of electronic search strategies, including translation of the question, Boolean/proximity syntax, subject headings, spelling, limits, and overall structure.
- The [JBI Manual for Evidence Synthesis](https://jbi-global-wiki.refined.site/space/MANUAL) and [Campbell Collaboration guidance](https://www.campbellcollaboration.org/research-resources/research-for-resources.html) provide parallel guidance for evidence synthesis outside narrowly biomedical use cases.

Design implication: ResearchForge should represent the search plan as data, not prose only. A skill should emit a protocol object before running searches and should fail validation if exact search strings, source names, result counts, and timestamps are missing.

### 2. Boolean, controlled vocabulary, and fielded search

Classical database searching is still the most defensible recall backbone. Core tactics include:

- Concept blocks combined with `AND`; synonyms within blocks combined with `OR`.
- Controlled vocabulary: MeSH in PubMed, Emtree in Embase, thesauri in PsycINFO/ERIC/CINAHL, classification codes in patent and engineering databases.
- Field restrictions: title, abstract, keyword, author, affiliation, journal, DOI, MeSH/subject heading, grant number, registry ID.
- Proximity operators: useful for phrases with variable wording, for example `melting NEAR/3 point`.
- Truncation and wildcards, with explicit safeguards against noisy stems.
- Validated search filters, for example study-design filters, if appropriate.
- Search-string translation between databases, because syntax and vocabularies differ.

Design implication: a source-compilation skill needs per-source query adapters. It should not assume one universal query string. It should keep both the source-neutral concept plan and the source-specific compiled queries.

### 3. Pearl growing, citation chasing, and snowballing

Exploratory search often starts from seed papers or "pearls" and expands through:

- Backward citation chasing: references cited by seed records.
- Forward citation chasing: later works that cite seed records.
- Related-record recommendations.
- Co-citation and bibliographic coupling.
- Author, institution, grant, method, dataset, and instrument trails.
- Hand-searching key journals, conference proceedings, edited volumes, and annual review series.

Citation chasing is especially valuable when terminology is inconsistent, concepts are interdisciplinary, or older sources predate modern indexing. It is also essential for books, datasets, standards, and patents, where journal database indexing can be incomplete.

Tools commonly used for this family include Web of Science cited-reference search, Scopus citation search, Google Scholar cited-by, Semantic Scholar, OpenAlex, ResearchRabbit, Connected Papers, Litmaps, Inciteful, and scite.

Design implication: every seed should have an expansion log: route, depth, source index, candidate IDs, and reason for inclusion. Citation expansion should be bounded by depth, result caps, and stopping rules.

### 4. Grey literature and web searching

Grey literature includes material not controlled by commercial academic publishers: government reports, technical reports, policy documents, white papers, theses, conference materials, clinical/regulatory records, standards, preprints, working papers, institutional repository items, and web pages.

Common methods:

- Targeted site searches of known organizations.
- Government and intergovernmental portals.
- Institutional repositories and thesis indexes.
- Trial registries and regulatory databases.
- Conference websites and proceedings.
- Standards organizations and technical committees.
- Web search engines with saved query strings and result windows.
- Expert consultation and cited-source follow-up.

Useful references and examples:

- [CADTH Grey Matters](https://www.cda-amc.ca/grey-matters-practical-tool-searching-health-related-grey-literature) provides a practical checklist-style approach to grey literature searching.
- [ClinicalTrials.gov](https://clinicaltrials.gov/) and the [WHO ICTRP](https://trialsearch.who.int/) support trial registry searching.
- [ProQuest Dissertations & Theses](https://about.proquest.com/en/products-services/pqdtglobal/) is a major dissertations route.
- [OpenGrey](http://www.opengrey.eu/) is no longer maintained, which is a useful warning: grey literature sources age, disappear, and need periodic source-registry review.

Design implication: web/grey searches need stronger provenance than bibliographic APIs because results are unstable. Store the query, search engine, date, result count when visible, inspected result window, title, URL, snippet, access date, and archived copy or checksum when allowed.

### 5. Books, monographs, handbooks, and older literature

Books and handbooks matter for scientific research when data or methods are older, canonical, proprietary-adjacent, pedagogical, or compiled into reference works. Journal-only search misses a lot here.

Useful routes:

- Library catalogs: [WorldCat](https://search.worldcat.org/), national libraries, university catalogs.
- Open books: [Directory of Open Access Books](https://www.doabooks.org/), [Open Textbook Library](https://open.umn.edu/opentextbooks), publisher OA collections.
- Digitized books: [HathiTrust](https://www.hathitrust.org/), [Internet Archive](https://archive.org/), [Google Books](https://books.google.com/), national library digital collections.
- Specialist handbooks and encyclopedias: CRC, SpringerMaterials, Kirk-Othmer, Ullmann's, Landolt-Bornstein, NIST collections, domain handbooks.
- Bibliographic APIs: [Library of Congress APIs](https://www.loc.gov/apis/), [Open Library APIs](https://openlibrary.org/developers/api), [Internet Archive APIs](https://archive.org/developers/), and [DOAB metadata/API access](https://www.doabooks.org/en/librarians/metadata).

Design implication: book search needs edition-aware records. A manifest should distinguish work, edition, volume, chapter, page span, scan source, OCR quality, and rights/access status.

### 6. Datasets, databases, and structured repositories

For scientific questions that ask about numeric properties, measurements, specimens, spectra, sequences, structures, or benchmarks, datasets may be more important than papers.

Important routes:

- DOI-linked data: [DataCite Commons](https://commons.datacite.org/) and the [DataCite REST API](https://support.datacite.org/docs/api).
- Repository registries: [re3data](https://www.re3data.org/).
- General repositories: [Zenodo](https://zenodo.org/), [Figshare](https://figshare.com/), Dryad, OSF.
- Scholarly metadata indexes that include datasets: OpenAlex, Crossref, DataCite, Dimensions.
- Domain repositories: NCBI, EMBL-EBI, PDB, PubChem, ChemSpider, NIST Chemistry WebBook, Materials Project, ICSD/COD, ENCODE, GEO, ProteomeXchange, NASA ADS/HEASARC, USGS, NOAA, EPA, OECD, World Bank, FAOSTAT.

Design implication: a source-compilation skill should not collapse papers and datasets into one flat "citation" type. Dataset records need version, DOI/accession, repository, file formats, license, variable-level metadata, and whether the dataset is primary, derived, supplemental, or benchmark.

### 7. Patents, standards, regulations, and technical documents

Some scientific and engineering questions are answered in patents, standards, regulatory submissions, safety dossiers, or technical datasheets rather than articles.

Useful routes:

- Patents: [Google Patents](https://patents.google.com/), [The Lens](https://www.lens.org/), [PatentsView API](https://patentsview.org/apis/purpose), Espacenet, WIPO PATENTSCOPE, USPTO Patent Center.
- Standards: ISO, IEC, ASTM, IEEE Standards, NIST, SAE, ASME, regulatory standards portals.
- Regulatory and safety records: FDA, EMA, EPA, ECHA, EFSA, REACH dossiers, PubChem safety links, SDS repositories where licensing permits.
- Technical documents: manufacturer application notes, instrument manuals, materials datasheets, government laboratory reports.

Design implication: patents and standards require different metadata: jurisdiction, application/publication number, assignee, claims, family, priority date, standard number, version, committee, status, and rights/access constraints.

### 8. Alerts and living searches

For current or living reviews, literature searching becomes a monitoring workflow:

- Saved alerts in PubMed, Web of Science, Scopus, Google Scholar, Crossref, Semantic Scholar, arXiv, bioRxiv/medRxiv, trial registries, patent databases, and relevant repositories.
- Scheduled API searches with deduplication against a persistent source registry.
- Change detection for key web pages.
- Periodic revalidation of source availability, licenses, and metadata.

Design implication: ResearchForge should separate one-time corpus compilation from a living-search mode. The latter needs stable IDs, last-seen timestamps, and "new since last run" reporting.

## Source and tool landscape

### Bibliographic databases and scholarly indexes

| Source type | Examples | Strengths | Weaknesses | Programmatic route |
|---|---|---|---|---|
| Biomedical bibliographic databases | PubMed/MEDLINE, Embase, CINAHL, PsycINFO | Controlled vocabulary, strong biomedical coverage | Subscription limits for some; full text often elsewhere | [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25499/), vendor APIs |
| Full-text OA biomedical sources | Europe PMC, PubMed Central OA | Full-text XML, licenses, PMCID route | Biomedical/OA skew | [Europe PMC REST API](https://europepmc.org/RestfulWebService), [PMC OA service](https://www.ncbi.nlm.nih.gov/pmc/tools/oa-service/) |
| Multidisciplinary citation indexes | Scopus, Web of Science, Dimensions | Broad coverage, citation links | Often subscription; API restrictions | Vendor APIs |
| Open scholarly metadata | OpenAlex, Crossref, Semantic Scholar | Large-scale API access, citation/metadata graphs | Metadata errors, uneven abstracts/full text | [OpenAlex API](https://docs.openalex.org/), [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), [Semantic Scholar API](https://api.semanticscholar.org/api-docs/) |
| Computer science/engineering | IEEE Xplore, ACM Digital Library, DBLP, arXiv | Strong CS/engineering coverage | Publisher boundaries; preprint/published duplication | Publisher APIs, [arXiv API](https://info.arxiv.org/help/api/index.html), DBLP API |
| Social science/economics | SSRN, RePEc, EconLit, SocArXiv | Working papers and preprints | Versioning and publication matching can be hard | Mixed APIs/search exports |
| Chemistry/materials | SciFinder-n, Reaxys, PubChem, ChemRxiv, Materials Project, NIST Chemistry WebBook | Substance/property focused | Important sources are proprietary; licenses matter | Mixed APIs, downloads, vendor systems |

### Review management and screening platforms

| Tool family | Examples | Useful for source compilation | Cautions |
|---|---|---|---|
| Reference managers | Zotero, EndNote, Mendeley | Import/export, deduplication, PDF management, citation keys | Dedup logic is not always transparent enough for audit by itself |
| Systematic-review platforms | Covidence, EPPI-Reviewer, DistillerSR, CADIMA | Screening workflow, conflicts, PRISMA-style tracking | Commercial lock-in; exports vary |
| Screening acceleration | ASReview, Rayyan, Abstrackr, RobotReviewer-derived classifiers | Active learning and prioritization | Needs held-out validation and transparent stopping rules |
| Citation/literature maps | ResearchRabbit, Connected Papers, Litmaps, Inciteful, VOSviewer, Bibliometrix | Network expansion and gap finding | Not a substitute for database search; algorithms are not fully transparent |

Official examples:

- [ASReview](https://asreview.nl/) is an open-source active-learning tool for systematic review screening.
- [Rayyan](https://www.rayyan.ai/) provides collaborative screening and AI-assisted features.
- [Covidence](https://www.covidence.org/) and [EPPI-Reviewer](https://eppi.ioe.ac.uk/cms/Default.aspx?alias=eppi.ioe.ac.uk/cms/er4) support end-to-end review workflows.
- The [Systematic Review Toolbox](https://systematicreviewtools.com/) is useful for discovering specialized review tools, though individual entries still need independent evaluation.

## AI-assisted and agentic methods

### AI search and synthesis tools

Current AI-assisted literature tools cluster around four tasks:

- Semantic retrieval from natural-language questions.
- Summarization and claim extraction.
- Paper recommendations and map-based discovery.
- Screening prioritization and evidence tables.

Examples:

- [Elicit](https://elicit.com/) supports literature search, paper summaries, extraction tables, and systematic-review-style workflows.
- [Consensus](https://consensus.app/) searches scientific literature and generates answers with cited papers.
- [Semantic Scholar](https://www.semanticscholar.org/) combines scholarly search, recommendations, TLDR-style summaries, influential citations, and API access.
- [scite](https://scite.ai/) uses citation contexts to classify supporting, contrasting, and mentioning citations.
- [ResearchRabbit](https://www.researchrabbit.ai/), [Connected Papers](https://www.connectedpapers.com/), [Litmaps](https://www.litmaps.com/), and [Inciteful](https://inciteful.xyz/) support citation-network exploration.

Observed strengths:

- Fast query expansion and seed discovery.
- Good at surfacing semantically related material when exact terms differ.
- Useful for interdisciplinary topics where controlled vocabularies lag.
- Useful for classifying and clustering large candidate sets before manual review.

Observed weaknesses:

- Coverage and ranking are often opaque.
- Generated summaries can overstate evidence or hide retrieval misses.
- Some tools lack stable export/provenance.
- Natural-language search is hard to reproduce unless prompts, model versions, returned records, and result windows are logged.

Design implication: AI tools should be treated as candidate generators and triage aids. The final source manifest should cite verifiable source records, not the AI answer.

### Open-source and agentic literature systems

Representative systems:

- [PaperQA2](https://github.com/Future-House/paper-qa) is an agentic retrieval-augmented question-answering system over scientific papers. Its papers and repository emphasize citation-grounded answers over user-supplied or retrieved paper corpora.
- [OpenScholar](https://arxiv.org/abs/2411.14199) is an open retrieval-augmented literature synthesis system that answers scientific queries with citation-backed responses over a large open-access paper datastore.
- [STORM](https://storm.genie.stanford.edu/) demonstrates multi-perspective retrieval and article generation with citations.
- [ScholarQA](https://allenai.org/blog/scholarqa) from AI2 is an example of scholarly question answering over large academic corpora with citations and evidence presentation.
- LLM-based "research agents" in general-purpose environments can search APIs, browse web pages, inspect PDFs, and build manifests, but defensibility depends entirely on explicit logging and validation.

Skill-style examples are also emerging:

- [`agent-research-skills`](https://github.com/lingzhi227/agent-research-skills) packages Claude Code skills for a research-paper lifecycle. Its `literature-search` skill searches Semantic Scholar, arXiv, OpenAlex, and Crossref; adjacent skills handle deep research, literature review, citation management, and report compilation.
- [`yorkeccak/scientific-skills` literature-search](https://agent-skills.md/skills/yorkeccak/scientific-skills/literature-search) is a natural-language literature-search skill using Valyu over PubMed, arXiv, bioRxiv, and medRxiv.
- The emerging "agent skills" ecosystem itself is still immature. A 2026 arXiv analysis of public skills describes skills as reusable modules with triggers, procedural logic, and tool interactions, and notes heavy redundancy and safety concerns across the ecosystem.

These examples are useful primarily as implementation patterns: small `SKILL.md` files, script-backed searches, API-key setup flows, JSON outputs, and command-oriented reproducibility. They generally do not yet implement PRISMA-S/PRESS-style reporting, broad non-journal source coverage, or validation audits at the level ResearchForge should target.

### Detailed look: `agent-research-skills`

`agent-research-skills` is a public Claude Code skills repository owned by `lingzhi227`. The repository describes itself as a suite of skills for the academic research-paper lifecycle, spanning literature discovery, research planning, experiment design, paper writing, citation management, LaTeX compilation, self-review, and slide generation. The GitHub README says the current suite has 31 skills; the repository's `SKILLS_IMPLEMENTED.md` says 30 deployed skills, so the implementation record appears to lag the README by one skill, probably the later-added `github-research` skill.

Public identity:

- The repository owner is `lingzhi227`.
- A Hugging Face profile for `lingzhi227` lists the name Lingzhi Yang.
- A LinkedIn post by Lingzhi Yang links to the repository and describes "30 Agent skills that turn Claude Code into a full research paper engine."
- Based on those public profiles, Lingzhi Yang appears to be the creator/maintainer. This is an inference from public account linkage, not an independently verified biographical claim.

Repository architecture:

- Skills follow a common package shape: `SKILL.md`, optional `scripts/`, and optional `references/`.
- The README says scripts are stdlib-only where possible, each script should expose `--help`, and skills are cross-linked via related-skill sections.
- Installation is via `npx skills add lingzhi227/agent-research-skills -g -a claude-code`, followed by an optional `install.sh` that installs slash commands and verifies script syntax.
- Optional dependencies include Python 3, PyMuPDF for PDF parsing, and numpy/scipy for statistical analysis.
- A Semantic Scholar API key can be supplied for higher-rate literature search.

The skill set is organized as a research pipeline:

| Phase | Skills in README | Notes |
|---|---|---|
| Research discovery and planning | `github-research`, `deep-research`, `literature-search`, `literature-review`, `idea-generation`, `novelty-assessment`, `research-planning` | Most relevant to ResearchForge source compilation. |
| Method design | `atomic-decomposition`, `algorithm-design`, `math-reasoning`, `symbolic-equation` | Mostly prompt-driven scientific reasoning and method design. |
| Experiment pipeline | `experiment-design`, `experiment-code`, `code-debugging`, `data-analysis` | Mixes prompt workflows with small helper scripts. |
| Paper writing | `paper-writing-section`, `related-work-writing`, `survey-generation`, `paper-to-code` | Focused on manuscript drafting, citation-grounded writing, and paper-to-code workflows. |
| Figures, tables, citations | `figure-generation`, `table-generation`, `citation-management`, `backward-traceability` | Useful design patterns for verifiable generated artifacts. |
| LaTeX and compilation | `latex-formatting`, `paper-compilation`, `excalidraw-skill` | Publication artifact production and checking. |
| Review and polish | `self-review`, `paper-revision`, `rebuttal-writing`, `slide-generation`, `paper-assembly` | End-stage review, revision, presentation, and pipeline completeness. |

Most relevant skills for source compilation:

- `literature-search`: expands a user query into 2-4 complementary searches, runs at least three APIs, merges/deduplicates results, and ranks by a weighted combination of citation count, recency, venue quality, and relevance. Its own scripts include Crossref, OpenAlex, and arXiv-source utilities; it also reuses Semantic Scholar, arXiv, paper database, and BibTeX scripts from `deep-research`.
- `deep-research`: a six-phase literature-survey workflow: frontier scan, broader survey, deep dive into 8-15 full papers, code/tool ecosystem scan, synthesis, and final report. It has strong phase gates requiring files to exist before proceeding, which is a useful anti-shortcut pattern.
- `literature-review`: uses multi-perspective dialogue simulation inspired by STORM-style workflows, grounded by shared search scripts.
- `novelty-assessment`: runs up to ten literature-search/evaluation rounds to judge whether an idea is novel.
- `citation-management`: harvests and validates BibTeX entries and can scan drafts for uncited claims.
- `github-research`: expands discovery beyond papers into code repositories, Papers With Code, and implementation metadata.

What looks strong:

- It turns common research-paper workflows into reusable procedural packages.
- It separates deterministic tasks into scripts and leaves synthesis/decision tasks to the agent.
- It includes phase gates, file outputs, and JSONL/BibTeX-style intermediate data.
- It explicitly pushes deep reading before synthesis in `deep-research`.
- It includes code/repository discovery, which many literature-review tools omit.

Limitations relative to a ResearchForge source-compilation skill:

- Search coverage is mainly paper/preprint/code oriented. It does not appear to treat books, datasets, patents, standards, regulatory records, or grey literature as first-class source classes.
- Its search stack emphasizes Semantic Scholar, arXiv, OpenAlex, and Crossref; that is useful but not enough for systematic source compilation in many scientific domains.
- The ranking formula in `literature-search` is plausible but not validated in the public docs.
- It does not appear to implement PRISMA-S or PRESS-style search reporting.
- It does not appear to require seed-set recall tests, relative recall benchmarking, accepted/rejected precision audits, or source-class coverage audits.
- It is optimized for producing a research report or paper-support workflow, not for producing a defensible source corpus that can be handed to downstream extraction.

Public performance evidence:

- I found repository documentation, skill marketplace mirrors, a LinkedIn announcement, and general papers about the emerging agent-skills ecosystem.
- I did not find a peer-reviewed paper, benchmark report, or public evaluation specifically measuring `agent-research-skills` retrieval recall, precision, citation accuracy, source diversity, or report quality.
- Marketplace statistics such as stars, forks, installs, or ranking are adoption indicators, not evidence of search performance.
- General papers on agent skills discuss ecosystem structure, validation, safety, and security, but they do not appear to benchmark this repository's research skills specifically.

ResearchForge takeaway:

`agent-research-skills` is a useful reference implementation for packaging, phase gating, script-backed skills, and paper-oriented research workflows. It should not be used as a methodological benchmark for source compilation quality. ResearchForge can borrow its modular skill structure and phase-gate discipline while adding the missing pieces: source-class registry, non-journal coverage, PRISMA-S/PRESS reporting, seed recovery, relative recall, precision audits, and manifest-level provenance.

Agentic patterns worth borrowing:

- Iterative query refinement: ask what sources are missing, then search targeted gaps.
- Multi-route retrieval: combine lexical, semantic, citation, and web routes.
- Source-grounded intermediate artifacts: each candidate has a route, rationale, and evidence snippet.
- Critic/checker roles: have a second pass check whether the search plan would recover known seed sources and whether any source classes were skipped.
- Structured outputs: candidate manifests, query logs, source registries, and screening decisions are more valuable than prose answers.

Agentic patterns to avoid:

- Letting an LLM decide that a search is "comprehensive" without measurable recall checks.
- Accepting citations from model memory.
- Mixing source discovery, summarization, and conclusions without a preserved candidate list.
- Treating high-level AI answers as sources.

## What "thorough" means

A thorough source-compilation process should optimize for recall first, then use auditable screening to recover precision. Thoroughness is not just "many search results." It should be evaluated by:

- Seed recovery: did the search find known relevant sources?
- Route diversity: were articles, books, datasets, patents, standards, grey literature, and domain repositories considered when relevant?
- Query diversity: were controlled vocabulary, synonyms, spelling variants, acronyms, property names, method names, instrument names, and named datasets considered?
- Source diversity: were at least two independent indexes used for important source classes?
- Citation expansion: were forward/backward citations explored from high-value seeds?
- Negative-space checks: did the process document source classes searched and found empty or intentionally excluded?
- Auditability: can a reviewer rerun or inspect every query, filter, candidate decision, and deduplication step?
- Precision audit: what fraction of accepted candidates are actually relevant?
- Miss audit: what kinds of relevant sources were found only by late-stage expansion, and can those patterns feed back into query design?

## Benchmarking search skills and software

Search skills and search software should be benchmarked at three levels:

1. Search-strategy quality: did the generated search plan and source selection make methodological sense?
2. Retrieval quality: did the system find the relevant sources?
3. Workflow quality: did it do so reproducibly, efficiently, and with auditable provenance?

The benchmark should evaluate both recall and conduct. A skill can retrieve many good papers and still fail as a scientific-search tool if the search cannot be reproduced, if it omits whole source classes, or if it accepts model-invented citations.

### Benchmark task types

Known-item recovery:

- Provide a research question and a hidden set of known relevant sources.
- Score whether the tool recovers each seed source through normal search, not by exact DOI/title lookup unless exact lookup is part of the task.
- Useful for quick regression tests of query generation and source adapters.

Published-review reconstruction:

- Use completed systematic/scoping reviews as quasi-gold standards.
- Give the tool the review question and inclusion criteria, then compare retrieved records against the review's included studies.
- This is imperfect because published reviews are not a true complete universe, but it is practical and common.

Relative recall benchmarking:

- Build a benchmark set of relevant studies from diverse routes: earlier reviews, expert suggestions, citation chasing, hand search, and similarity search.
- Test whether a candidate search strategy retrieves those indexed benchmark studies.
- This is useful when an absolute gold standard is impossible, which is the normal case in broad literature search.

Pooled judgment benchmarking:

- Run multiple systems/search routes, pool candidates, have humans judge relevance, then evaluate each system against the pooled judgments.
- This is the TREC/CLEF-style information retrieval model.
- It is stronger than one-system evaluation but still vulnerable to missed relevant sources outside the pool.

Technology-assisted review benchmarking:

- Evaluate ranking, active learning, and screening acceleration on fixed datasets with known inclusion labels.
- CLEF eHealth TAR and TREC Total Recall are key precedents.
- Metrics should include high-recall workload measures, not just ranking quality.

Deep-research/report benchmarking:

- Give agents complex research tasks requiring multi-step search and synthesis.
- Score report quality, information recall, source support, citation accuracy, and presentation.
- DeepResearch Bench, DeepResearch Bench II, BrowseComp, GAIA-style tasks, and LitSearch are relevant examples, but they test different things. BrowseComp emphasizes finding hard-to-locate factual answers; LitSearch emphasizes scientific retrieval; DeepResearch Bench emphasizes report generation and citation-grounded synthesis.

Source-class coverage benchmarking:

- Construct tasks where the answer requires non-journal material: a book chapter, dataset, standard, patent, government report, thesis, or regulatory document.
- Score whether the system searches the right source class and retrieves the correct object.
- This is especially important for ResearchForge because journal-only benchmarks would train the wrong behavior.

### Metrics

Core retrieval metrics:

- Recall/sensitivity: relevant sources retrieved divided by relevant sources in the benchmark set.
- Precision: relevant sources retrieved divided by all retrieved sources.
- Specificity and accuracy: sometimes useful in fixed labeled corpora, but less informative for open-ended literature search.
- Yield: number of relevant sources found by a route or source class.
- Number needed to read or screen: total retrieved divided by relevant retrieved.
- Recall@k and precision@k: useful when a tool returns ranked candidates.
- nDCG, MAP, and MRR: useful for search-engine style ranked retrieval, especially when relevance is graded.

High-recall workflow metrics:

- Work saved over sampling at target recall, for example WSS@95.
- Records screened to reach 95%, 99%, or 100% recall.
- Last relevant found: rank position at which the final relevant record appears.
- Stopping-rule reliability: whether the system can safely stop without missing relevant records.
- Budgeted recall: recall achieved after a fixed screening budget.

Scientific-source quality metrics:

- Seed recovery rate.
- Source-class coverage: articles, preprints, datasets, books, patents, standards, grey literature, regulatory records, code, and domain databases.
- Unique-source contribution by route: how many accepted sources were found only by citation chasing, semantic search, web search, or a specific database.
- Metadata correctness: DOI, PMID, PMCID, ISBN, patent number, dataset accession, title, authors, year, venue, license, and URL.
- Deduplication quality: false merges and missed duplicates.
- Full-text acquisition rate and extraction success.
- Citation accuracy: whether cited sources exist and match the claims made about them.
- Evidence support: whether snippets or quoted passages actually support inclusion decisions.

Reproducibility and audit metrics:

- Exact query capture rate.
- Source-run completeness: query, source, platform, timestamp, filters, result count, and retrieved window all recorded.
- Prompt/model/tool version capture for AI-assisted steps.
- Rerun stability: overlap between repeated runs at different times.
- Decision auditability: proportion of accept/reject decisions with reason codes and evidence.
- Human-review agreement: inter-reviewer agreement on sampled screening decisions.

Cost and usability metrics:

- Wall-clock time.
- API calls and rate-limit failures.
- Token cost.
- Human review time.
- Number of manual corrections needed.
- Failure recovery: whether partial results and logs survive interrupted runs.

### Benchmark construction recommendations for ResearchForge

ResearchForge should maintain several benchmark suites rather than one omnibus leaderboard:

- `known_item_micro`: small, fast regression tests with 5-20 expected sources per task.
- `published_review_replay`: tasks derived from completed systematic/scoping reviews with known included sources.
- `non_journal_retrieval`: tasks requiring books, datasets, patents, standards, theses, or grey literature.
- `property_corpus_search`: tasks like the melting/boiling-point corpus where success means finding sources with extractable data, not merely topical relevance.
- `screening_tarbeds`: fixed candidate pools for ranking and active-learning evaluation.
- `end_to_end_research`: longer tasks where the output is a source manifest plus validation report, not just a ranked list.

Recommended benchmark artifact structure:

```text
benchmark_task/
|-- task.md
|-- inclusion_criteria.md
|-- expected_source_classes.json
|-- seed_sources_private.jsonl
|-- public_seed_sources.jsonl
|-- gold_or_quasi_gold_sources.jsonl
|-- allowed_sources.json
|-- evaluation_config.json
|-- human_judgments.jsonl
`-- notes.md
```

Recommended scoring bundle:

- `recall_report.md`: seed recovery, relative recall, recall by source class.
- `precision_report.md`: accepted-candidate audit and confidence interval where possible.
- `provenance_report.md`: query/log completeness, rerunability, evidence support.
- `coverage_report.md`: sources searched, source classes skipped, and rationale.
- `cost_report.md`: time, tokens, API calls, manual review minutes.
- `failure_analysis.md`: missed-source patterns and false-positive classes.

### Benchmark cautions

- Published reviews are not perfect gold standards; they can miss sources.
- Search engines and live APIs change, so reruns should store dates and raw records.
- Web search benchmarks are vulnerable to leakage if gold answers are public and searchable.
- LLM-as-judge scores can be useful for triage but should not be the sole metric for source relevance or citation support.
- Benchmarking only papers will systematically under-measure source-compilation skill for books, datasets, patents, standards, and grey literature.
- High report quality can mask poor retrieval. Source compilation should score the manifest before scoring the prose.

## Recommended ResearchForge source-compilation skill

### Skill purpose

Build a reproducible, auditable source corpus for a scientific or engineering question. The skill should discover candidate sources broadly, screen them against the user's scope, and produce a manifest ready for downstream summarization, extraction, or report generation.

### Default phases

#### Phase 0: scope and source protocol

Inputs:

- Research question.
- Target domains and source classes.
- Inclusion/exclusion criteria.
- Date/language/geography constraints, if any.
- Required source types: articles, books, datasets, patents, standards, regulatory records, grey literature.
- Access constraints: open access only, metadata only, institutional access allowed, downloadable full text required, etc.
- Known seed sources, if available.
- Target recall/precision posture: exhaustive, balanced, or fast exploratory.

Outputs:

- `search_protocol.md`
- `source_registry.json`
- `seed_sources.jsonl`
- `concept_blocks.json`

The skill should warn when the requested scope is too narrow. For example, a physical-property question should usually include datasets, handbooks, patents, and regulatory/property databases, not only journal articles.

#### Phase 1: concept and query expansion

Actions:

- Extract core concepts, entities, synonyms, acronyms, spellings, broader/narrower terms, methods, instruments, materials, and property names.
- Add controlled vocabulary terms where available.
- Ask an LLM for candidate terms, then verify terms against source-specific thesauri or seed records.
- Build query families rather than one giant query.
- Create source-specific query translations.

Outputs:

- `query_plan.md`
- `queries.jsonl`

Required fields for each query:

- `query_id`
- `source_id`
- `source_type`
- `route`: lexical, controlled_vocab, semantic, citation, grey_web, book_catalog, dataset, patent, standard
- `query_string`
- `compiled_syntax`
- `filters`
- `expected_signal`
- `seed_sources_expected`

#### Phase 2: execute searches

Actions:

- Run API searches where available.
- Use official exports for commercial or UI-only systems when APIs are unavailable.
- For web searches, capture query, engine, result window, and inspected URLs.
- Store raw records before screening.
- Respect robots, API rate limits, terms of use, and licensing.

Outputs:

- `raw_records/source_id/*.jsonl` or exported RIS/BibTeX/CSV
- `search_runs.jsonl`

Required fields for each run:

- `run_id`
- `query_id`
- `source_id`
- `platform`
- `run_datetime`
- `result_count_reported`
- `records_retrieved`
- `result_window`
- `api_endpoint_or_export_method`
- `notes`

#### Phase 3: normalize and deduplicate

Actions:

- Normalize identifiers: DOI, PMID, PMCID, arXiv ID, ISBN, ISSN, patent number, dataset DOI/accession, standard number, URL.
- Merge duplicate records while preserving all discovery routes.
- Distinguish duplicate records from duplicate studies, reports, datasets, editions, and versions.

Outputs:

- `candidates_raw.jsonl`
- `candidates_deduped.jsonl`
- `dedup_report.md`

Each candidate should preserve:

- All source routes that found it.
- Original source metadata.
- Normalized metadata.
- Match confidence and merge rationale.

#### Phase 4: recall expansion

Actions:

- Backward citation expansion from seed and high-confidence candidates.
- Forward citation expansion via OpenAlex, Semantic Scholar, Crossref, Scopus/Web of Science where available.
- Semantic-neighbor expansion using Elicit/Semantic Scholar/OpenAlex embeddings or local embeddings if available.
- Book/dataset/patent/standard follow-up from cited references and metadata.
- Expert-web route: search named projects, datasets, organizations, instruments, compounds, software packages, or standards discovered in candidates.

Outputs:

- `expansion_runs.jsonl`
- Updated `candidates_deduped.jsonl`
- `gap_checks.md`

Stopping criteria should be explicit. Examples: no new included records after two expansion rounds, all seed sources recovered, capped graph depth reached, or user-specified budget reached.

#### Phase 5: screen and classify

Actions:

- Title/abstract/metadata screening.
- Full-text or landing-page screening when needed.
- AI-assisted triage with conservative thresholds.
- Manual review for borderline or high-impact candidates.
- Reject with structured reasons, not silent deletion.

Outputs:

- `screening_decisions.jsonl`
- `accepted_sources.jsonl`
- `borderline_sources.jsonl`
- `rejected_sources.jsonl`
- `screening_report.md`

Suggested decision fields:

- `candidate_id`
- `decision`: accepted, borderline, rejected
- `reason_code`
- `rationale`
- `evidence_snippet`
- `reviewer`: human, agent, classifier, mixed
- `confidence`
- `needs_full_text`
- `downstream_use`: summarize, extract_data, background, exclude_from_analysis, citation_context

#### Phase 6: validate

Actions:

- Check seed recovery.
- Randomly audit accepted candidates.
- Randomly audit rejected candidates if budget allows.
- Review all borderline candidates for small corpora.
- Compare source-class coverage against the protocol.
- Run dedup and manifest consistency checks.

Outputs:

- `validation_report.md`
- `audit_sample.csv`
- `audit_decisions.jsonl`

Recommended minimum validation:

- Seed recovery table.
- Source-class coverage table.
- Accepted precision sample with confidence interval if sample is large enough.
- Late-discovery analysis: sources found only via citation/semantic/grey expansion.
- Miss analysis: any known relevant source not recovered and why.

#### Phase 7: package for downstream work

Outputs:

- `accepted_sources.jsonl`
- `accepted_sources.csv`
- `search_protocol.md`
- `query_log.md`
- `source_coverage.md`
- `validation_report.md`
- `README.md`

If full text is downloaded:

- Store license/access status.
- Store original file, extracted text, metadata, and checksum.
- Record whether extraction came from PDF, XML, HTML, OCR, API, or manual export.

### Recommended output layout

```text
search_run/
|-- README.md
|-- search_protocol.md
|-- source_registry.json
|-- concept_blocks.json
|-- queries.jsonl
|-- search_runs.jsonl
|-- raw_records/
|   |-- pubmed/
|   |-- openalex/
|   |-- crossref/
|   |-- worldcat/
|   |-- datacite/
|   `-- grey_web/
|-- candidates_raw.jsonl
|-- candidates_deduped.jsonl
|-- expansion_runs.jsonl
|-- screening_decisions.jsonl
|-- accepted_sources.jsonl
|-- borderline_sources.jsonl
|-- rejected_sources.jsonl
|-- reports/
|   |-- query_log.md
|   |-- dedup_report.md
|   |-- source_coverage.md
|   |-- screening_report.md
|   `-- validation_report.md
`-- full_text/
    |-- articles/
    |-- books/
    |-- datasets/
    |-- patents/
    `-- grey_literature/
```

### Source registry schema sketch

```json
{
  "source_id": "openalex",
  "name": "OpenAlex",
  "source_class": "scholarly_metadata",
  "coverage_notes": "Multidisciplinary scholarly metadata graph; includes works, authors, institutions, sources, concepts, funders.",
  "access": "open_api",
  "api_docs": "https://docs.openalex.org/",
  "supports": ["keyword_search", "field_filters", "citation_graph", "doi_lookup"],
  "limits": ["metadata quality varies", "full text usually external"],
  "recommended_use": ["broad discovery", "citation expansion", "dedup identifiers"]
}
```

### Candidate schema sketch

```json
{
  "candidate_id": "src_000001",
  "source_type": "journal_article",
  "title": "...",
  "normalized_identifiers": {
    "doi": "...",
    "pmid": "...",
    "pmcid": "..."
  },
  "publication_year": 2024,
  "creators": ["..."],
  "containers": ["..."],
  "discovery_routes": [
    {
      "run_id": "run_pubmed_001",
      "query_id": "q_pubmed_003",
      "rank": 12,
      "matched_terms": ["..."]
    }
  ],
  "access": {
    "landing_page": "...",
    "full_text_url": "...",
    "license": "...",
    "downloaded": false
  },
  "screening": {
    "decision": "borderline",
    "reason_code": "needs_full_text",
    "rationale": "Abstract matches property and method terms but no extractable data visible."
  }
}
```

## Validation patterns worth adopting

### Seed recovery

Ask the user for known relevant sources or derive seeds from prior work. Before accepting a search plan, run each query family against the seeds:

- Did exact DOI/title searches recover them?
- Did concept queries recover them?
- Which source found each seed first?
- Which seed was missed and why?

Seed recovery is the fastest way to catch query translations that look elegant but fail in practice.

### Dual-route confirmation

For high-value accepted sources, prefer at least two independent discovery routes, such as:

- PubMed plus citation expansion.
- OpenAlex plus Crossref DOI lookup.
- Google Books plus WorldCat.
- DataCite plus repository API.
- Patent number from Google Patents plus Lens/PatentsView.

This does not prove relevance, but it improves metadata reliability and reduces dependence on one index.

### Precision and miss audits

For accepted sources, randomly audit a sample and report observed precision. For rejected sources, sample enough to estimate whether the screening rules are over-aggressive. For source classes with few records, inspect all.

For AI-assisted screening, maintain a held-out manual sample. Do not use a model's confidence score as a validation metric.

### Late-source analysis

Track sources found only after citation/semantic/grey expansion. These are design gold: they reveal missing terms, missing databases, or source classes that the initial protocol underweighted.

## Risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Black-box AI retrieval | Hard to reproduce; hidden coverage gaps | Log prompts, model/tool version, returned records, result window, and rerun date |
| Search-engine instability | Web rankings and snippets change | Store inspected URLs, access dates, snippets, and archived/checksummed copies where allowed |
| Database syntax drift | Search strings do not translate cleanly | Compile source-specific queries and record platform/version notes |
| Subscription bias | Available APIs may skew toward open sources | Record access constraints and missing subscription sources |
| Journal-only bias | Books, datasets, patents, standards, and reports may be omitted | Require source-class checklist during protocol phase |
| Identifier errors | DOI/ISBN/patent merges can be wrong | Preserve original records and merge confidence |
| Duplicate study vs duplicate record | Same evidence may appear in preprint, article, report, dataset, and patent | Model "work", "manifestation", and "evidence item" separately when needed |
| AI hallucinated citations | Models may invent or misremember sources | Accept only records verified through source indexes or documents |
| Overly broad query noise | High recall can overwhelm screening | Use staged search, classifiers, active learning, and rejection manifests |
| Hidden full-text limits | Metadata match may not contain usable evidence | Track full-text availability and extraction route |

## Near-term implementation recommendations

1. Create a `source-compilation` skill whose first deliverable is a protocol plus source registry, not search results.
2. Implement adapters for open APIs first: OpenAlex, Crossref, Semantic Scholar, Europe PMC, PubMed E-utilities, arXiv, DataCite, Zenodo, Open Library/Internet Archive, and PatentsView.
3. Add manual-import paths for subscription/UI-only sources: Web of Science, Scopus, Embase, SciFinder/Reaxys, Google Scholar, WorldCat, standards portals.
4. Use AI for query expansion, citation-route prioritization, and screening rationale drafts, but require source-record verification before acceptance.
5. Require a seed-source test. If no seeds are available, the skill should create provisional seeds from highly relevant records found by exact phrase/domain searches, then use them for subsequent validation.
6. Preserve rejected and borderline records with reason codes.
7. Emit a final `validation_report.md` every time, even for exploratory runs.
8. Design the manifest to hand off directly to the existing structured extraction skill: stable source IDs, local file paths, source URLs, licenses, and evidence-location hints.

## Suggested reason-code taxonomy

Accepted:

- `directly_relevant_primary_source`
- `directly_relevant_dataset`
- `directly_relevant_reference_work`
- `background_or_method_source`
- `citation_context_only`

Borderline:

- `needs_full_text`
- `unclear_scope_match`
- `metadata_only`
- `possible_duplicate`
- `access_limited`
- `needs_domain_expert_review`

Rejected:

- `wrong_domain`
- `wrong_source_type`
- `no_relevant_data`
- `method_only_no_data`
- `duplicate_record`
- `superseded_version`
- `non_scientific_source`
- `unverifiable_citation`
- `unavailable_or_dead_link`
- `license_or_terms_block`

## Sources consulted

Guidelines and methods:

- Cochrane Handbook, Chapter 4, "Searching for and selecting studies": https://training.cochrane.org/handbook/current/chapter-04
- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- PRISMA-S extension: https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-020-01542-z
- PRESS guideline statement: https://www.cadth.ca/press-peer-review-electronic-search-strategies-2015-guideline-statement
- CADTH Grey Matters: https://www.cda-amc.ca/grey-matters-practical-tool-searching-health-related-grey-literature
- JBI Manual for Evidence Synthesis: https://jbi-global-wiki.refined.site/space/MANUAL
- Campbell Collaboration research resources: https://www.campbellcollaboration.org/research-resources/research-for-resources.html
- Practical guide to evaluating literature-search sensitivity using relative recall: https://www.cambridge.org/core/journals/research-synthesis-methods/article/practical-guide-to-evaluating-sensitivity-of-literature-search-strings-for-systematic-reviews-using-relative-recall/BC6A8387DAB7539D7F96EBD5965ECC32
- Search-effectiveness metrics review: https://www.sciencedirect.com/science/article/abs/pii/S0895435617313318
- Database coverage/recall/precision comparison for 120 systematic reviews: https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-016-0215-7
- Supplementary search techniques methodological review: https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-017-0625-1
- CLEF eHealth TAR 2019 task page: https://clefehealth.imag.fr/clefehealth.imag.fr/index1833.html?page_id=173
- CLEF eHealth TAR budget-aware analysis: https://www.mdpi.com/2504-4990/7/3/104

Search APIs and broad indexes:

- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- Europe PMC REST API: https://europepmc.org/RestfulWebService
- PMC OA service: https://www.ncbi.nlm.nih.gov/pmc/tools/oa-service/
- OpenAlex API: https://docs.openalex.org/
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Semantic Scholar API: https://api.semanticscholar.org/api-docs/
- arXiv API: https://info.arxiv.org/help/api/index.html
- DataCite API: https://support.datacite.org/docs/api
- re3data: https://www.re3data.org/
- PatentsView APIs: https://patentsview.org/apis/purpose

Books and non-journal sources:

- WorldCat: https://search.worldcat.org/
- Directory of Open Access Books metadata: https://www.doabooks.org/en/librarians/metadata
- Library of Congress APIs: https://www.loc.gov/apis/
- Open Library APIs: https://openlibrary.org/developers/api
- Internet Archive APIs: https://archive.org/developers/
- ClinicalTrials.gov: https://clinicaltrials.gov/
- WHO ICTRP: https://trialsearch.who.int/

AI-assisted and review tools:

- Elicit: https://elicit.com/
- Consensus: https://consensus.app/
- Semantic Scholar: https://www.semanticscholar.org/
- scite: https://scite.ai/
- ResearchRabbit: https://www.researchrabbit.ai/
- Connected Papers: https://www.connectedpapers.com/
- Litmaps: https://www.litmaps.com/
- Inciteful: https://inciteful.xyz/
- ASReview: https://asreview.nl/
- Rayyan: https://www.rayyan.ai/
- Covidence: https://www.covidence.org/
- EPPI-Reviewer: https://eppi.ioe.ac.uk/cms/Default.aspx?alias=eppi.ioe.ac.uk/cms/er4
- Systematic Review Toolbox: https://systematicreviewtools.com/
- PaperQA2: https://github.com/Future-House/paper-qa
- OpenScholar: https://arxiv.org/abs/2411.14199
- STORM: https://storm.genie.stanford.edu/
- AI2 ScholarQA overview: https://allenai.org/blog/scholarqa
- LitSearch retrieval benchmark: https://arxiv.org/abs/2407.18940
- BrowseComp browsing-agent benchmark: https://openai.com/index/browsecomp/
- DeepResearch Bench: https://arxiv.org/abs/2506.11763
- DeepResearch Bench II: https://arxiv.org/abs/2601.08536
- Agent research skills for Claude Code: https://github.com/lingzhi227/agent-research-skills
- Agent research skills implementation record: https://github.com/lingzhi227/agent-research-skills/blob/main/SKILLS_IMPLEMENTED.md
- Agent research skills `literature-search` skill: https://github.com/lingzhi227/agent-research-skills/tree/main/skills/literature-search
- `lingzhi227` Hugging Face profile: https://huggingface.co/lingzhi227
- Lingzhi Yang LinkedIn post announcing research skills: https://www.linkedin.com/posts/lingzhi-yang-72b960267_github-lingzhi227claude-research-skills-activity-7430518091425497088-dTDJ
- Example literature-search agent skill: https://agent-skills.md/skills/yorkeccak/scientific-skills/literature-search
- Agent Skills ecosystem analysis: https://arxiv.org/abs/2602.08004

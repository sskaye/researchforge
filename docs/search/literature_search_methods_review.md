# Literature-Search Methods: A Review for ResearchForge

A standalone survey of methods, tools, infrastructure, and methodology for discovering scientific and engineering literature — covering conventional bibliographic indexes, open metadata APIs, domain-specific repositories, sources beyond journals (books, grey literature, patents, standards, data, code), citation-network discovery, AI-assisted search agents, search-strategy methodology, reference management and systematic-review software, and bibliometric discovery aids. The review ends with design implications for the planned ResearchForge **source search and compilation** skill.

Companion to [`prior-work.md`](../reviews/prior-work.md), which surveyed AI-assisted literature review more broadly; this document is the search-specific deep dive, and where the two overlap on AI search agents, this document goes a layer deeper into the *search* mechanics.

---

## Contents

1. Executive summary
2. Open scholarly infrastructure: the metadata spine
3. Premium bibliographic indexes
4. Web-style discovery engines
5. Domain-specific repositories with public APIs
6. Sources beyond journal articles
7. Citation-network and federated discovery
8. AI-assisted search agents: search mechanics
9. AI search techniques and evaluation
10. Methodology and reporting standards
11. Search-strategy building blocks
12. Citation chasing and text-mining-assisted search construction
13. Reference management and systematic-review software
14. Deduplication
15. Bibliometric tools as discovery aids
16. Cross-cutting findings
17. Design implications for the source search and compilation skill
18. Sources

---

## 1. Executive summary

**The infrastructure has consolidated.** Five open services now form a credible spine for any cross-source bibliographic workflow: [OpenAlex](https://openalex.org/) (~250M works, CC0 metadata, full citation graph), [Crossref](https://www.crossref.org/) (~180M registered DOIs with deposited references), [Semantic Scholar](https://www.semanticscholar.org/) (~200M papers + embeddings + recommendations + TLDRs), [OpenCitations](https://opencitations.net/) (2.2B+ open citations), and [DataCite](https://datacite.org/) (DOIs for data, software, samples). Together with [Unpaywall](https://unpaywall.org/) for OA-status resolution, [ORCID](https://orcid.org/) for authors, and [ROR](https://ror.org/) for institutions, they cover most of what subscription indexes used to cover — though with looser curation and weaker controlled-vocabulary support.

**Premium indexes still matter** for specific tasks: [Web of Science](https://clarivate.com/) and [Scopus](https://www.elsevier.com/products/scopus) remain canonical for bibliometric provenance and tenure-style analyses; [Engineering Village/Compendex](https://www.elsevier.com/products/engineering-village/databases/compendex) and [INSPEC](https://www.theiet.org/publishing/inspec) for conference-heavy engineering disciplines; [CAS SciFinder](https://www.cas.org/solutions/cas-scifinder-discovery-platform/cas-scifinder) and [Reaxys](https://www.elsevier.com/products/reaxys) for chemistry/materials substance-and-reaction queries. They are paywalled and API-restricted, which makes them poor primary integrations for a portable skill but useful escalation targets.

**Domain repositories are heterogeneous in quality of programmatic access.** [arXiv](https://arxiv.org/), [PubMed](https://pubmed.ncbi.nlm.nih.gov/)/[Europe PMC](https://europepmc.org/), [NASA ADS](https://ui.adsabs.harvard.edu/), [INSPIRE-HEP](https://inspirehep.net/), and [Springer Nature's Open Access API](https://dev.springernature.com/) are well-documented and open. [IEEE Xplore](https://developer.ieee.org/) is gated. [ACM DL](https://dl.acm.org/), most large commercial publishers, and most engineering reference works are not realistically scriptable without an institutional TDM agreement.

**Sources beyond journals dominate engineering practice.** Government technical reports ([DOE OSTI](https://www.osti.gov/), [NASA NTRS](https://ntrs.nasa.gov/), [DTIC](https://discover.dtic.mil/), [IAEA INIS](https://www.iaea.org/resources/databases/inis), [USGS](https://pubs.usgs.gov/), [EPA](https://www.epa.gov/research-reports)), data repositories ([Materials Project](https://materialsproject.org/), [NIST WebBook](https://webbook.nist.gov/chemistry/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [NOMAD](https://nomad-lab.eu/), [AFLOW](http://www.aflowlib.org/)), patents ([USPTO PatentsView](https://patentsview.org/), [EPO OPS](https://developers.epo.org/), [Google Patents BigQuery](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data), [Lens.org](https://www.lens.org/)), and books ([HathiTrust](https://www.hathitrust.org/), [OAPEN/DOAB](https://www.oapen.org/), [LibreTexts](https://libretexts.org/)) are all programmatically accessible. Standards (ASTM, ISO, IEEE SA) are mostly paywalled and represent a real coverage gap. Engineering reference handbooks ([Knovel](https://app.knovel.com/), [CRC](https://hbcp.chemnetbase.com/), AccessEngineering) are similarly closed.

**AI-assisted search is uneven.** On *citation-grounded question answering*, the open-source frontier (PaperQA2, OpenScholar) now matches or exceeds PhD-level domain experts on the published benchmarks. On *recall against a systematic-review gold standard*, the best published numbers are still 30–80% (Undermind whitepaper) and a 2025 Cochrane evaluation found [Elicit](https://elicit.com/) averaged 39.5% sensitivity vs. 94.5% for original human searches ([Lau et al. 2025](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70050)). The frontier on comprehensive search is not closed.

**Methodology is mature where it has been formalized.** [PRISMA-S](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8074898/), [PRESS](https://www.jclinepi.com/article/S0895-4356(16)00058-5/fulltext), the Cochrane Handbook, and PROSPERO together specify how to design, document, and audit a search strategy. [PRISMA-trAIce (2025)](https://www.equator-network.org/) extends this to AI-tool use. These standards are the right backbone for a reproducible-audit-trail design.

**Reference and screening software has consolidated around four engines.** [Zotero](https://www.zotero.org/) for reference management with a usable open API; [Rayyan](https://www.rayyan.ai/) and [Covidence](https://www.covidence.org/) for screening (free and commercial respectively); [EPPI-Reviewer](https://eppi.ioe.ac.uk/eppireviewer-web/) for ML-assisted screening at scale; [ASReview](https://asreview.nl/) for open-source active-learning screening. [SR-Accelerator](https://sr-accelerator.com/) bundles the most-used point tools (Polyglot, Word Frequency Analyser, Deduplicator, Spider Citation Search).

**The practical implication for ResearchForge.** A defensible source-search-and-compilation skill is a *composition* of well-validated components rather than a novel agent: a multi-source first-stage retrieval (OpenAlex + Crossref + Semantic Scholar + arXiv + the domain-specific APIs above), agentic iteration with explicit stop conditions, hybrid retrieval + cross-encoder rerank, and a PRISMA-S-grade audit trail. The unsolved problems — comprehensive recall against gold standards, reproducible search reports, deduplication across heterogeneous sources, coverage of engineering grey literature — are exactly where a careful integration adds the most value.

---

## 2. Open scholarly infrastructure: the metadata spine

These services are the backbone of any modern multi-source search workflow. They are open, well-documented, and increasingly the *de facto* primary surface for cross-source discovery.

**[OpenAlex](https://openalex.org/)** (OurResearch). Reached ~250M works in late 2025, bootstrapped from the discontinued Microsoft Academic Graph plus Crossref, ORCID, ROR, and direct preprint feeds. CC0 metadata, free [REST API](https://developers.openalex.org/), nightly snapshot dumps. **Important 2026 change:** as of Feb 13 2026, OpenAlex deprecated the historical "polite pool" (user-agent email) and now requires API keys; default quota 100k calls/day at up to 10 req/s ([rate limits](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication)). First-class entities for works, authors, sources, institutions, concepts, and topics; full citation graph. Author and institution disambiguation is improving but remains error-prone for common names.

**[Crossref](https://www.crossref.org/)**. The 2025 Public Data File contains nearly 180M records — essentially every DOI registered by a Crossref member ([REST API docs](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)). Free, no sign-up; polite pool requires `mailto`. Authoritative for titles, authors, references, funders, and licences. Reference coverage varies (older publishers often did not deposit references); abstracts often missing; no rich subject indexing.

**[Semantic Scholar](https://www.semanticscholar.org/)** (Allen Institute for AI). ~200M+ papers, with SPECTER2 embeddings, TLDR summaries, an influential-citation flag, and a [Recommendations API](https://api.semanticscholar.org/api-docs/) for "papers similar to these". Free with API key. Default unauthenticated rate ~5,000 requests / 5 minutes (shared); authenticated baseline 1 req/s. Author disambiguation and venue normalization are still imperfect; some papers lack OA links. Underpins many AI search products (Elicit, Consensus, Connected Papers, Litmaps, ResearchRabbit).

**[OpenCitations](https://opencitations.net/)**. The Index crossed 2.2 billion citation records in July 2025; the February 2026 dataset incorporates the September 2025 Crossref dump and DataCite ([OpenCitations Indexes blog](https://opencitations.hypotheses.org/category/opencitations-indexes)). CC0; REST API at `api.opencitations.net`, SPARQL endpoint, and bulk dumps. Provides an open reproducible substitute for proprietary citation graphs.

**[Unpaywall](https://unpaywall.org/)**. Tracks OA status for ~30M articles from 50,000+ journals and 5,000+ repositories. Free with email; daily limit ~100k calls. Since the 2025 OpenAlex rewrite, Unpaywall runs as a subroutine of the OpenAlex codebase, ensuring consistent OA-location resolution. Powers most library link resolvers and browser extensions.

**[DataCite](https://datacite.org/)**. DOIs for datasets, software, samples, and non-article research outputs. Public [REST API](https://support.datacite.org/docs/api), OAI-PMH, and annual Public Data File. Best route for discovering data, software, and grey-literature outputs with persistent identifiers.

**[ORCID](https://orcid.org/)**. ~22M researcher iDs; free [Public API](https://info.orcid.org/documentation/api-tutorials/); supports ROR identifiers for affiliations as of October 2021. Coverage depends on author self-curation and is non-uniform across fields.

**[ROR](https://ror.org/)**. Open registry of ~110K research organizations. CC0, free [API](https://ror.readme.io/), bulk dumps. The de-facto open institution identifier; reconciles institution names across multiple databases. Integrated into Crossref, DataCite, ORCID, and OpenAlex.

**[CORE](https://core.ac.uk/)**. ~431M metadata records, ~323M free-to-read full-text links, ~46M full texts hosted directly. CC-BY non-commercial. The CORE [REST API](https://core.ac.uk/services/api) is one of the few open systems delivering full text via API; bulk dumps available. Metadata heterogeneous (harvested from institutional repositories); no curated citation graph.

**Practical layering.** OpenAlex is the highest-leverage primary surface; Crossref is the authoritative cross-check for metadata; Semantic Scholar adds embeddings/recommendations; OpenCitations gives a citation graph independent of any single vendor; Unpaywall resolves OA copies; DataCite covers non-article artifacts; ORCID/ROR provide author/institution disambiguation. For most search workflows these eight services together are a credible replacement for a Web of Science / Scopus combination on coverage, at the cost of weaker controlled vocabulary and softer curation.

---

## 3. Premium bibliographic indexes

Subscription-paywalled. Share three features: editorial selection of journals, controlled-vocabulary or classification systems, and a vendor-maintained citation graph.

**[Web of Science](https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/) (Clarivate).** Full platform indexes >271M records; the Core Collection covers >97M records linked by 2.4B cited references. The Core Collection includes SCI-Expanded (>9,200 journals, 178 disciplines, back to 1900), SSCI (>3,400 journals), AHCI (>1,800 journals from 1975), and the Emerging Sources Citation Index (>7,800 journals). 128 journals were de-listed in 2025 — a reminder that the index is continuously curated ([Clarivate librarian resources](https://clarivate.libguides.com/librarianresources/coverage)). Web of Science Starter, Expanded, and Lite APIs are negotiated per-subscription. Distinctive features include KeyWords Plus controlled vocabulary, Highly Cited Papers, Author Records, and the Journal Citation Reports lineage. Known to be biased toward English-language and North-American/European journals.

**[Scopus](https://www.elsevier.com/products/scopus) (Elsevier).** ~78M records as of July 2025, ~217K books, >2M preprint records, ~16M author profiles, ~70K institutional profiles ([Scopus content](https://www.elsevier.com/products/scopus/content)). Scopus Search, Abstract Retrieval, Author Retrieval, and Citation Overview APIs via the [Elsevier Developer Portal](https://dev.elsevier.com/sc_apis.html); free for non-commercial academic use, license required for commercial. Larger journal coverage than WoS, ASJC subject codes. Bramer et al. (2017, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5718002/)) flagged that Scopus lacks full thesaurus features, so its recall on structured queries is materially lower than MEDLINE/Embase even with larger raw coverage.

**[Dimensions](https://www.digital-science.com/products/dimensions/) (Digital Science).** Links publications, conference abstracts, grants, patents, clinical trials, datasets, and policy documents in a single graph; >70% of publications have full-text indexing. Free web access for publication discovery; premium tiers for analytics, grants, and full API access. The Dimensions Analytics API uses its own DSL (Dimensions Search Language). New specialty APIs as of 2025: Author Check (July 2025) and Research Security (Sept 2025) ([Frontiers paper on the Dimensions API](https://www.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2025.1514938/full)). Distinctive in linking the full research lifecycle.

**[Engineering Village / Compendex](https://www.elsevier.com/products/engineering-village/databases/compendex) (Elsevier).** Compendex covers engineering since 1884 (with the backfile); the Engineering Village platform packages it with [INSPEC](https://www.theiet.org/publishing/inspec), GeoRef, and GEOBASE. Strong conference-proceedings coverage. Ei Thesaurus is the indexing backbone. Limited programmatic access.

**[INSPEC](https://www.theiet.org/publishing/inspec) (IET).** >22M records in physics, EE, communications, CS, control, IT, manufacturing/mechanical engineering, OR, materials, oceanography, nuclear engineering, environmental science, geophysics, nanotechnology, biomedical technology, biophysics. The INSPEC Thesaurus is the gold-standard controlled vocabulary for physics and EE indexing. Subscription via Engineering Village, EBSCO, or Ovid; programmatic access vendor-dependent.

**[CAS SciFinder](https://www.cas.org/solutions/cas-scifinder-discovery-platform/cas-scifinder).** CAS Registry holds 165M substances; CAS References indexes >52M documents (journals, patents, conference proceedings, technical reports) from 1907 to present. Distinctive: structure/substructure/reaction search, CAS Registry Numbers, expert chemistry curation. Closed ecosystem; very limited programmatic access ([CAS Common Chemistry](https://commonchemistry.cas.org/) has an open subset).

**[Reaxys](https://www.elsevier.com/products/reaxys) (Elsevier).** 353M substances, 72M reactions, 125M documents, 48M patents, 51M bioactivity data points. Reaction-centric — captures yields, solvents, conditions; integrates with retrosynthesis tools. Reaxys API and flat-file feeds (refreshed twice weekly); new Predictive Retrosynthesis and Synthetic Accessibility APIs as of 2025.

**Recall evidence for premium indexes.** Bramer et al. (2017) found Embase had the highest individual-database recall (85.9%) for SR queries; Embase + MEDLINE (± Cochrane CENTRAL) reached ≥95% recall in 48% of reviews; adding Web of Science + Google Scholar reached 100% recall in 72% ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5718002/)). No single index is sufficient.

---

## 4. Web-style discovery engines

**[Google Scholar](https://scholar.google.com/).** Coverage estimated at 100M+ ([Khabsa & Giles 2014](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0093949)) to ~176M ([Orduña-Malea et al. 2015](https://link.springer.com/article/10.1007/s11192-014-1455-8)). No official API; scraping is throttled with CAPTCHAs and explicit ToS prohibition. Distinguishing strengths: broad coverage of grey literature, theses, and technical reports; full-text indexing of OCR'd PDFs. As Gusenbauer & Haddaway ([2020, Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/jrsm.1378)) documented, Scholar is unsuitable as a primary system for evidence synthesis because of opaque ranking, a 1,000-result hard cap, inability to perform precise Boolean queries, and unstable result orderings that prevent reproducible searches.

**[BASE (Bielefeld Academic Search Engine)](https://www.base-search.net/).** >400M documents from 12,000+ providers; ~60% offer full-text OA. Free OAI-PMH and a search API for registered organizations. Strong on grey literature, theses, and institutional repository content. Metadata quality varies by source.

**[CORE](https://core.ac.uk/).** See §2 — the same service that anchors the open metadata spine also functions as a web-style discovery engine over harvested full text.

**[Lens.org](https://www.lens.org/).** ~200M+ scholarly records and ~458M patent/innovation records. Free at the web interface; API and bulk data via subscription. Uniquely integrates patents with scholarly literature in a queryable graph — strongest open option for innovation/IP analyses.

---

## 5. Domain-specific repositories with public APIs

### Preprint servers

- **[arXiv](https://arxiv.org/)** (physics, math, CS, EE, stats, q-bio, q-fin). ~2.4M articles, ~28k submissions/month by late 2025. [arXiv API](https://info.arxiv.org/help/api/user-manual.html) (Atom/XML), OAI-PMH, S3 bulk dumps. In October 2025 arXiv blocked AI-generated survey papers because of submission flooding ([arXiv blog 2025](https://blog.arxiv.org/2025/)).
- **[bioRxiv](https://www.biorxiv.org/) / [medRxiv](https://www.medrxiv.org/)**. ~268k+ preprints as of Feb 2026, ~4k/month. Moved to the new independent nonprofit **openRxiv** in March 2025 with a $16M CZI grant — the largest governance change since 2013. REST API `api.biorxiv.org`; full text also via Europe PMC.
- **[ChemRxiv](https://chemrxiv.org/)**. ACS/RSC/GDCh/CCS/CSJ-hosted. Figshare-backed API.
- **[EarthArXiv](https://eartharxiv.org/)**, **[engrXiv](https://engrxiv.org/)**, **OSF Preprints**. All on the [Center for Open Science platform](https://osf.io/preprints/) with a common [OSF API](https://developer.osf.io/).
- **[TechRxiv](https://www.techrxiv.org/)** (IEEE). API provided.
- **[Research Square](https://www.researchsquare.com/)** (Springer Nature). Harvestable through Crossref.
- **[SSRN](https://www.ssrn.com/)** (Elsevier). No first-class public API; ToS-restricted.
- **[RePEc/IDEAS](https://ideas.repec.org/)** and **[EconStor](https://www.econstor.eu/)**. OAI-PMH endpoints; well-documented bulk access.

Crossref and OpenAlex index most preprint servers, so cross-server discovery is usually easier through the aggregators than per-server APIs.

### Biomedicine

- **[PubMed](https://pubmed.ncbi.nlm.nih.gov/)**. 40M+ citations (March 2025); MEDLINE alone 38M+ records from 5,200+ publications. [E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/) (ESearch, EFetch, ELink, EPost, ESummary). PubMed is migrating ESearch/EPost to updated infrastructure in February 2026.
- **[PubMed Central](https://pmc.ncbi.nlm.nih.gov/)**. ~10M+ full-text articles; substantial OA subset. OAI-PMH service. [PMC for Developers](https://pmc.ncbi.nlm.nih.gov/tools/developers/).
- **[Europe PMC](https://europepmc.org/)**. ~42M+ abstracts, ~10.2M full-text articles, ~6.5M OA. Includes preprints (bioRxiv/medRxiv), patents, NIH grants, clinical guidelines, and structured annotations. [RESTful Web Service](https://europepmc.org/RestfulWebService) with JATS XML download for OA papers.
- **[S2ORC](https://github.com/allenai/s2orc)** (Allen Institute for AI). ~81M papers with metadata and resolved references; structured full text for ~8.1M OA papers. Served via Semantic Scholar Datasets API. Core training data for modern academic-LLM systems.

### Physical sciences

- **[NASA ADS](https://ui.adsabs.harvard.edu/)**. 15M+ records in astronomy, astrophysics, planetary, and adjacent physics. Solr-backed [REST API](https://ui.adsabs.harvard.edu/help/api/) with rich field queries. The original model for citation-rich domain search.
- **[INSPIRE-HEP](https://inspirehep.net/)**. ~1.7M records for high-energy physics — particle, theoretical, astroparticle, accelerator. [REST API](https://github.com/inspirehep/rest-api-doc) returning JSON/MARCXML; 15 req / 5s rate limit. Distinctive author disambiguation through INSPIRE BAI; references auto-extracted.

### Engineering and computer science

- **[IEEE Xplore](https://ieeexplore.ieee.org/)**. ~6M+ documents — journals, conferences, books, courses, standards. Metadata API and full-text API now available via the [IEEE Developer Portal](https://developer.ieee.org/); text-and-data mining permitted for non-commercial research with active subscription. Restrictive per-record license.
- **[ACM Digital Library](https://dl.acm.org/)**. CS-focused. No first-class public API; metadata reaches downstream via Crossref.
- **[DBLP](https://dblp.org/)**. Comprehensive CS bibliography. Free [API](https://dblp.org/faq/13501473.html), well-suited for proceedings discovery.
- **[OpenReview](https://openreview.net/)**. Hosts NeurIPS, ICLR, COLM, AISTATS and most ML venues with reviews, rebuttals, and decisions. [API](https://docs.openreview.net/getting-started/using-the-api) essential for ML literature work.

### Publisher full-text APIs

- **Elsevier ScienceDirect.** Multiple APIs on the [Developer Portal](https://dev.elsevier.com/). Free non-commercial keys; full-text TDM requires institutional subscription.
- **Springer Nature.** Four APIs on the [dev portal](https://dev.springernature.com/), three free upon registration including the [Open Access API](https://dev.springernature.com/oa-api) for full text of OA publications; the TDM API supports up to 150 req/min with additional costs.
- **Wiley TDM.** The [Wiley TDM Client](https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining) Python package shipped June 2025; academic subscribers get ORCID-based tokens.
- **APS, AIP Scitation, RSC, ACS, IOP, Taylor & Francis, Oxford.** Metadata via Crossref; full-text TDM negotiated per institution.

For physical sciences and engineering, full-text programmatic access at scale is available only via OA repositories (Europe PMC, arXiv, CORE), the publisher APIs above where licensed, or institutional TDM agreements.

---

## 6. Sources beyond journal articles

Engineering practice in particular leans heavily on non-journal sources: technical reports, standards, patents, reference handbooks, and design data tables. The coverage and access posture of each category differs substantially.

### 6.1 Books and reference works

**Open and public-domain books.** [Project Gutenberg](https://www.gutenberg.org/) (full-text bulk via [Gutendex API](https://gutendex.com/)), [HathiTrust](https://www.hathitrust.org/) (~18M digitized volumes, ~6M public domain, with the [HathiTrust Bibliographic API](https://www.hathitrust.org/bib_api), [HathiFiles bulk metadata](https://www.hathitrust.org/hathifiles), and non-consumptive TDM via the [HathiTrust Research Center](https://www.hathitrust.org/htrc) — its Extracted Features dataset is CC0), [Internet Archive](https://archive.org/) (with [Internet Archive Scholar](https://scholar.archive.org/)), [Library of Congress Digital Collections](https://www.loc.gov/collections/) ([loc.gov JSON API](https://libraryofcongress.github.io/data-exploration/)), [NLM Digital Collections](https://collections.nlm.nih.gov/), [Open Library](https://openlibrary.org/) ([API](https://openlibrary.org/developers/api)), [Europeana](https://www.europeana.eu/) ([APIs](https://pro.europeana.eu/page/apis)), and [Google Books](https://books.google.com/) ([Books API](https://developers.google.com/books) for metadata/snippets only).

**Open textbooks and OER.** [Open Textbook Library](https://open.umn.edu/opentextbooks), [LibreTexts](https://libretexts.org/), [OER Commons](https://www.oercommons.org/) (OAI-PMH), [OAPEN](https://www.oapen.org/) and [DOAB](https://www.doabooks.org/) (combined ~80k+ peer-reviewed open monographs, both OAI-PMH), and [MIT OCW](https://ocw.mit.edu/).

**Commercial reference works — the engineering critical mass.** [SpringerLink books](https://link.springer.com/) (via the Springer Nature TDM API with institutional auth), [Wiley Online Library books](https://onlinelibrary.wiley.com/), [ScienceDirect](https://www.sciencedirect.com/) book chapters (via the Elsevier Text Mining API), and the four practically irreplaceable engineering references: [Knovel](https://app.knovel.com/) (aggregates Perry's, Roark's, Smithells, etc.), [CRC Handbook](https://hbcp.chemnetbase.com/), AccessEngineering, and IHS Engineering Workbench. All are firmly paywalled with no public API. The commercial reference set typically dominates authoritative coverage of practical engineering correlations and design data.

### 6.2 Theses and dissertations

[ProQuest Dissertations & Theses Global](https://about.proquest.com/en/products-services/pqdtglobal/) is the most comprehensive but paywalled. [EThOS](https://ethos.bl.uk/) (British Library) has been intermittently offline since the [late 2023 cyber incident](https://blogs.bl.ac.uk/living-knowledge/2023/12/). [OATD](https://oatd.org/) aggregates >7M open theses (no formal API). [DART-Europe](https://www.dart-europe.eu/) and [NDLTD](https://ndltd.org/) federate national/institutional repositories. [BASE](https://www.base-search.net/) and [CORE](https://core.ac.uk/) jointly cover most open theses with programmatic APIs.

### 6.3 Government and agency reports (grey literature)

Highest under-utilized class of engineering literature, and almost all of it is public domain with documented APIs.

**US Federal.** [DOE OSTI](https://www.osti.gov/) ([OSTI.GOV API](https://www.osti.gov/api/v1/docs), critical for energy/materials/nuclear), [NASA NTRS](https://ntrs.nasa.gov/) ([NTRS API](https://ntrs.nasa.gov/api/openapi.json), critical for aerospace and propulsion), [DTIC](https://discover.dtic.mil/) (defense; limited public API), [USGS Publications Warehouse](https://pubs.usgs.gov/) ([REST API](https://pubs.er.usgs.gov/documentation/web_service_documentation)), [EPA reports](https://www.epa.gov/research-reports) via [NEPIS](https://nepis.epa.gov/), [GovInfo](https://www.govinfo.gov/) ([API](https://api.govinfo.gov/docs/)).

**International.** [World Bank Open Knowledge Repository](https://openknowledge.worldbank.org/) ([DSpace OAI-PMH](https://openknowledge.worldbank.org/server/oai/request)), [OECD iLibrary](https://www.oecd-ilibrary.org/) ([Data API](https://data.oecd.org/api/)), [IMF eLibrary](https://www.elibrary.imf.org/) ([SDMX API](https://data.imf.org/api)), [EU JRC Publications](https://publications.jrc.ec.europa.eu/repository/), [IAEA INIS](https://www.iaea.org/resources/databases/inis) (critical for nuclear), [UN Digital Library](https://digitallibrary.un.org/). [IEA](https://www.iea.org/) is mostly paywalled.

**Aggregators.** [OpenGrey](http://www.opengrey.eu/) closed in 2020 (historical archive at [DANS](https://easy.dans.knaw.nl/)). [GreyNet International](http://www.greynet.org/) maintains a back-catalog.

### 6.4 Standards

Standards are where normative engineering knowledge lives and are uniquely difficult to access programmatically. [ASTM](https://www.astm.org/), [ISO](https://www.iso.org/standards.html), [IEC](https://www.iec.ch/), [ASME](https://www.asme.org/codes-standards), [SAE](https://www.sae.org/standards), [ASHRAE](https://www.ashrae.org/technical-resources/standards-and-guidelines), [API](https://www.api.org/), and [ANSI](https://webstore.ansi.org/) are all paywalled with no usable APIs. [IEEE SA](https://standards.ieee.org/) has a paywall but a subset is free under the [IEEE GET Program](https://standards.ieee.org/products-programs/ieee-get-program/). [ITU](https://www.itu.int/en/publications/) makes many ITU-T recommendations free. [NIST publications](https://www.nist.gov/publications) (SP, TN, NISTIR, FIPS) are the only fully open large-scale standards corpus and have a usable [NIST PDR API](https://data.nist.gov/sdp/); the [SP 800 series](https://csrc.nist.gov/publications/sp800) and FIPS standards are fully open. For all other standards bodies, the business model depends on the paywall, so only bibliographic metadata is realistically retrievable.

### 6.5 Patents

Patents are first-class engineering prior art and exceptionally well-structured for programmatic discovery.

- **US — USPTO.** The legacy PatFT/AppFT is replaced by [Patent Public Search](https://ppubs.uspto.gov/pubwebapp/) (web UI only). [PatentsView API](https://patentsview.org/apis/api-endpoints) is the strongest US-only programmatic interface — free, clean JSON, supports CPC/IPC, inventor/assignee disambiguation, citations. [USPTO Open Data Portal](https://developer.uspto.gov/) ships bulk dumps and Office Action data.
- **Europe — EPO.** [Espacenet](https://worldwide.espacenet.com/) covers 140M+ patents worldwide. [Open Patent Services (OPS) API](https://developers.epo.org/) is REST, with a free tier and weekly quotas. Bulk DOCDB/EPODOC dumps.
- **Global.** [Google Patents](https://patents.google.com/) covers ~120M docs in 100+ jurisdictions with machine translation. The [Google Patents Public Datasets on BigQuery](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data) are the single most useful programmatic surface for patents at scale — SQL-queryable, includes CPC/IPC, citations, claims, embeddings. [Lens.org](https://www.lens.org/) unifies scholarly + patent, free for academic use. [WIPO PatentScope](https://patentscope.wipo.int/) covers ~110M PCT applications. [J-PlatPat](https://www.j-platpat.inpit.go.jp/) (Japan) and CNIPA (China) have weaker programmatic access.

**Classifications.** [CPC](https://www.cooperativepatentclassification.org/) and [IPC](https://www.wipo.int/classifications/ipc/en/) are essential for systematic patent search; class-based recall catches what title/abstract search misses entirely. The practical default for engineering patent analytics is Google Patents BigQuery for breadth + PatentsView for US analytics + EPO OPS for European depth.

### 6.6 Data repositories

**General-purpose.** [Zenodo](https://zenodo.org/) (CERN, [REST API](https://developers.zenodo.org/), mostly CC-BY/CC0, GitHub-integration for citable releases), [Figshare](https://figshare.com/) ([API](https://docs.figshare.com/)), [Dryad](https://datadryad.org/) ([API](https://datadryad.org/api/v2/docs/), CC0 mandated), [OSF](https://osf.io/) ([OSF API](https://developer.osf.io/)), [Harvard Dataverse](https://dataverse.harvard.edu/) and the [Dataverse network](https://dataverse.org/) ([extensive API](https://guides.dataverse.org/en/latest/api/)), [ICPSR](https://www.icpsr.umich.edu/), [Mendeley Data](https://data.mendeley.com/) ([API](https://data.mendeley.com/api/docs/)).

**Domain-specific — chemistry, materials, energy.** [Materials Project](https://materialsproject.org/) (DFT-computed properties for ~150K materials; [API](https://api.materialsproject.org/docs) via [pymatgen](https://pymatgen.org/) and `MPRester`), [NIST Standard Reference Data](https://www.nist.gov/srd) and [NIST Chemistry WebBook](https://webbook.nist.gov/chemistry/) (thermophysical properties, gas-phase IR/MS), [NIST ThermoData Engine](https://trc.nist.gov/tde.html), [NOMAD Laboratory](https://nomad-lab.eu/) ([API](https://nomad-lab.eu/prod/v1/api/v1/)), [AFLOW](http://www.aflowlib.org/) ([AFLUX API](http://aflowlib.org/API/)), [OQMD](http://oqmd.org/) ([REST API](http://oqmd.org/static/docs/restful.html)), [ICSD](https://icsd.products.fiz-karlsruhe.de/) (paywalled), [Crystallography Open Database](http://www.crystallography.net/cod/) (open mirror, bulk SVN/Git), [PubChem](https://pubchem.ncbi.nlm.nih.gov/) ([PUG-REST](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest), >100M substances, public domain), [ChEMBL](https://www.ebi.ac.uk/chembl/) ([API](https://chembl.gitbook.io/chembl-interface-documentation/)), [NREL ATB](https://atb.nrel.gov/), [OpenEI](https://openei.org/) ([API](https://openei.org/services/doc/rest)).

**Earth, climate, NASA.** [NASA Earthdata](https://earthdata.nasa.gov/) ([CMR API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)), [USGS Water Services](https://waterservices.usgs.gov/), [NOAA NCEI](https://www.ncei.noaa.gov/) ([CDO API](https://www.ncei.noaa.gov/cdo-web/webservices/v2)), [Copernicus CDS](https://cds.climate.copernicus.eu/) ([CDS API](https://cds.climate.copernicus.eu/api-how-to) with Python client).

**Registry layer.** [re3data](https://www.re3data.org/) ([API](https://www.re3data.org/api/doc)) and [FAIRsharing](https://fairsharing.org/) ([API](https://fairsharing.org/API_doc)) register thousands of data repositories; [DataCite Commons](https://commons.datacite.org/) is the unified discovery layer across DOIs.

### 6.7 Code and computational research

[GitHub](https://github.com/) ([REST](https://docs.github.com/en/rest) and [GraphQL](https://docs.github.com/en/graphql) APIs), [GitLab](https://gitlab.com/), [Bitbucket](https://bitbucket.org/), and [Software Heritage](https://www.softwareheritage.org/) (~20B archived source files with stable SWHIDs; the [archival DOI integration](https://www.softwareheritage.org/save-and-reference-research-software/) is the canonical citation route for code). The [GitHub-Zenodo integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content) mints DOIs for tagged releases. [Papers With Code](https://paperswithcode.com/) (Meta-owned; future uncertain post-restructuring) links papers to code, datasets, and benchmark leaderboards. [Hugging Face Hub](https://huggingface.co/) is increasingly cited as a primary source for ML datasets and models. Package registries — [PyPI](https://pypi.org/) ([JSON API](https://warehouse.pypa.io/api-reference/json.html) + BigQuery), [CRAN](https://cran.r-project.org/) ([cranlogs](https://cranlogs.r-pkg.org/)), [conda-forge](https://conda-forge.org/) ([API](https://api.anaconda.org/docs)) — are under-recognized as research-artifact discovery surfaces (pymatgen, OpenMM, Cantera, etc.).

### 6.8 Conference proceedings

DBLP for CS bibliographic discovery; OpenReview for ML; arXiv for full text (often more current than the camera-ready); IEEE Xplore for IEEE-only venues. ACM DL coverage is reachable only via Crossref bibliographic metadata.

### Licensing posture summary

| Tier | Examples | Reuse posture |
|---|---|---|
| Public domain | NIST publications/data, NASA NTRS, USGS, EPA, OSTI, USPTO data | Fully reusable |
| Open CC | Zenodo (CC-BY/CC0), arXiv (per-paper), DOAB/OAPEN, OpenAlex (CC0), CORE | Reusable with attribution |
| Institutional TDM | Springer Nature TDM API, Elsevier Text Mining API, Wiley TDM Client | Requires licence + TDM agreement |
| Closed paywall | Knovel, CRC Handbook, ASTM/ISO/IEEE-SA standards, ICSD, ProQuest PQDT | Bibliographic metadata only |
| Restricted free | IEEE Xplore API (non-commercial quota), EPO OPS (quota-limited) | Quota-bound free |

---

## 7. Citation-network and federated discovery

These tools sit on top of the open metadata layer and surface relationships rather than running keyword retrieval.

**[Connected Papers](https://www.connectedpapers.com/)** — single-seed graph using co-citation/bibliographic-coupling similarity over Semantic Scholar. No Boolean refinement; user must re-run to discover new papers.

**[Litmaps](https://www.litmaps.com/)** — iterative citation chaining with new-paper alerts and reference-manager integration. Sits on Semantic Scholar / Crossref / OpenAlex. Free tier limited to ~5 maps/month.

**[ResearchRabbit](https://www.researchrabbit.ai/)** — visual citation chaining with personal collections; the [2025 revamp](https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative) emphasizes iterative chaining without UI clutter. Sits on Semantic Scholar and PubMed. As of October 2025 ResearchRabbit and Litmaps have a partnership combining indices and features.

**[Inciteful](https://inciteful.xyz/)** — dynamic citation graphs from one or more seeds, with PageRank-style importance ranking and link-prediction similarity. Sits on OpenAlex, Semantic Scholar, Crossref.

**[CitationGecko](https://github.com/CitationGecko/citation-network-explorer)** — open-source citation network explorer over OpenCitations / Semantic Scholar.

**[VOSviewer](https://www.vosviewer.com/)** (Leiden CWTS) — bibliometric network visualization (co-citation, co-authorship, bibliographic coupling, term co-occurrence) over WoS/Scopus/Dimensions/Lens/PubMed/Crossref exports. Free desktop tool, capped at ~10,000 publications per analysis, ignores time dimension ([van Eck & Waltman](https://link.springer.com/article/10.1007/s11192-017-2300-7)).

**[CitNetExplorer](https://www.citnetexplorer.nl/)** — citation-network analysis for millions of publications with explicit time modeling; WoS-specific input format.

**[Open Knowledge Maps](https://openknowledgemaps.org/)** — concept maps from PubMed/BASE; free non-profit; [API available](https://openknowledgemaps.org/services).

**General limitation of citation-graph traversal.** Highly-cited methods papers (R packages, foundational statistics references) dominate raw co-citation similarity even when topically irrelevant. Without semantic filtering or controlled-vocabulary anchoring, these tools surface noise. They are best used as a *complement* to keyword/semantic search, not a substitute.

**Library federated-search platforms.** [EBSCO Discovery Service](https://www.ebsco.com/products/ebsco-discovery-service) (309 publisher partners, 19k+ resources), [Ex Libris Primo / Summon](https://www.proquest.com/products-services/Ex-Libris-Primo.html) (Central Discovery Index of 5.2B records), [ProQuest Search Platform](https://www.proquest.com/), and [OCLC WorldCat](https://www.oclc.org/en/worldcat/inside-worldcat.html) (609M bibliographic records, 488 languages, 3.58B library holdings; recently integrated 122M OA resources from 3,000+ collections). These are index-based discovery services optimized for known-item lookup and library navigation, not for structured reproducible queries — typically not the right primary source for systematic reviews.

---

## 8. AI-assisted search agents: search mechanics

This section goes a layer deeper than [`prior-work.md`](../reviews/prior-work.md) on *how* the major AI search tools actually search, and adds coverage of tools not in the prior-work doc.

### 8.1 Tools previously surveyed — search dimension

**[Elicit](https://elicit.com/).** Single source: Semantic Scholar (~138M papers), with OpenAlex as a contributing source for journal coverage. Two modes: semantic search (dense embeddings over abstracts, default) and a Boolean [Keyword Search mode](https://elicit.com/blog/introducing-keyword-search) added in 2024 for systematic reviews. Iteration is user-driven, not agent-driven; there is no autonomous query reformulation loop. Top-k abstracts are re-summarized for the user-supplied question with per-claim sentence citations; no documented cross-encoder rerank. Search history visible, but the API-level query is not exposed and searches are not provably reproducible later. **Recall headline:** the [Lau et al. 2025 Cochrane evaluation](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70050) reported Elicit sensitivity averaging **39.5% (25.5–69.2%)** vs. **94.5% (91.1–98.0%)** for the original human searches across four evidence syntheses; average precision 41.8%. Authors recommend Elicit only as a *supplementary* search.

**[Consensus](https://consensus.app/).** ~220M records sourced from Semantic Scholar and OpenAlex. Publicly documented three-phase pipeline ([how Consensus works](https://consensus.app/home/blog/how-consensus-works/), [Elastic case study](https://www.elastic.co/customers/consensus)): (1) hybrid first-stage retrieval combining BM25 with [Elastic ELSER](https://www.elastic.co/search-labs/blog/introducing-elastic-learned-sparse-encoder) (a SPLADE-style learned sparse encoder) over titles and abstracts → top 1,500; (2) mid-stage rerank combining relevance + citation count + citation velocity + publication date → top 20; (3) precision rerank with a larger cross-encoder. The Consensus Meter then aggregates yes/no/mixed signals over the resulting set. A [Scholar Agent / Deep Search](https://help.consensus.app/en/articles/12641232-scholar-agent) mode does multi-step iterative search instead of one-shot retrieval. No external published recall benchmark.

**[Undermind](https://www.undermind.ai/).** The [whitepaper](https://www.undermind.ai/whitepaper.pdf) is one of the more informative public documents in this space. Strategy: multi-pass iterative search over Semantic Scholar and OpenAlex; each pass = query → fetch candidates → GPT-4-class classifier on full text into {highly relevant, closely related, ignorable} → refine the next query → follow citation trails of relevant hits. Classification accuracy ~96% on highly relevant papers in their internal eval. Reports ~10× higher density of relevant papers in top hits vs. Google Scholar, and gold-standard recovery of **30–80%** of papers in systematic-review reference sets. Explicit saturation stop condition (diminishing return of new relevant hits).

**[PaperQA2](https://github.com/Future-House/paper-qa)** — the reference open-source architecture. Index sources: local PDF library + on-demand fetch via Crossref + Semantic Scholar (default ~12 candidates per call). Hybrid embedding stack: dense (`text-embedding-3-small` default; large variants for benchmarks) **concatenated** with a 256-dim sparse keyword-encoded vector — explicit hybrid dense+sparse retrieval at chunk level ([Nature paper](https://arxiv.org/html/2409.13740v2)). Grobid or PyMuPDF for PDF→chunk parsing; section-aware chunking when Grobid headers are present. **The key technique is Re-ranking and Contextual Summarization (RCS):** top-k chunks pass through an LLM that scores relevance 1–10 and produces a ≤300-word contextual summary; only summaries above threshold reach the answer step. RCS reduces context bloat *and* hallucination. The agent has `search`, `gather_evidence`, `answer`, and `citation_traverse` tools; it decides when to re-search. Evaluation: 85.2% precision and 66% accuracy on LitQA2; SOTA on the science portion of [RAG-QA Arena](https://arxiv.org/abs/2407.13998) (+12.4% over closest competitor). Fully open code; every retrieval, RCS score, and citation is inspectable.

**[OpenScholar](https://github.com/AkariAsai/OpenScholar)** (Allen Institute for AI). 45M open-access papers from Semantic Scholar with **237M passage embeddings** — the largest open scientific datastore. Trained `OpenScholar-Retriever` (dense passage retrieval) → trained `OpenScholar-Reranker` (fine-tuned cross-encoder) → top-N passages to generator. Inference-time self-feedback loop: the generator can re-query the retriever after a draft, asking for evidence on under-supported claims. OpenScholar-8B beats GPT-4o by +6.1% correctness and PaperQA2 by +5.5% on multi-paper synthesis; citation hallucination drops from 78–90% (GPT-4o ungrounded) to expert-parity ([Nature 2025](https://www.nature.com/articles/s41586-025-10072-4)). Everything open: LM weights, retriever, reranker, datastore, ScholarQABench eval set.

**[FutureHouse Crow / Falcon / Owl](https://www.futurehouse.org/tools).** All draw on PubMed + OpenAlex + Semantic Scholar + specialized DBs (e.g., OpenTargets for Falcon). Crow is the production PaperQA2 — narrow, fast, scholarly Q&A. Falcon uses the same primitives tuned for *deep review* (larger candidate sets, longer retrieval chains). Owl (formerly HasAnyone) is optimized for **prior-art / "has anyone done X" recall** — the success criterion shifts from precision-at-top-k to coverage; the search loop is biased toward expansion. The architectural lesson is that the *same retrieval primitives* can produce three different products by changing budgets, stop conditions, and what counts as success.

### 8.2 Tools not in the prior-work doc

**[Perplexity Deep Research](https://docs.perplexity.ai/) and Spaces.** Generic web search agent with academic affordances. Deep Research (Feb 2025) does dozens of real-time searches and synthesizes; the [academic filter](https://docs.perplexity.ai/guides/academic-filter-guide) restricts to peer-reviewed journals, PubMed, arXiv, JSTOR, ACM DL, with partnerships including Wiley as of May 2025. Spaces is a closed-corpus mode: upload up to 50 documents per Space, add custom instructions, combine with web search. Pipeline routes across DeepSeek-R1, GPT-4.1, Claude 4.0, Gemini Pro 2.5. Sources cited inline; the agent's search trail is not user-inspectable.

**[OpenAI Deep Research](https://openai.com/index/introducing-deep-research/).** A fine-tuned variant of o3, RL-trained for browsing + Python tool use. End-to-end agentic: plans, searches, evaluates sources, refines queries, backtracks, synthesizes. Not retrieval-pipeline-based — the model itself runs the loop. No dedicated scholarly index; prefers original journal/preprint URLs over surveys. The [Deep Research system card](https://cdn.openai.com/deep-research-system-card.pdf) documents the model-as-agent design.

**[Gemini Deep Research](https://gemini.google/overview/deep-research/).** Default mix of academic journals, scientific reports, news, government databases. Plan-dependent extensions to user uploads, Gmail, Drive, Chat, and NotebookLM sources. Distinctive: Gemini surfaces an explicit research plan checklist that the user can edit before launch — the most transparent of the major Deep Research products.

**[Anthropic Claude Research](https://www.anthropic.com/engineering/multi-agent-research-system).** Lead Opus orchestrator plans + saves to memory + spawns parallel Sonnet subagents, each isolated, each acting as intelligent filter; orchestrator deduplicates and synthesizes. Anthropic reports +90.2% over single-agent on internal evals. Documented failure modes: excessive subagent spawning on simple queries, redundant searches, coordination failures — mitigated with explicit per-subagent budgets and scope.

**[Iris.ai](https://iris.ai/).** "Research fingerprint" approach: from a seed paper, extract key terms + synonyms/hypernyms, build a concept vector, score documents by fingerprint similarity. The Explore Tool generates concept maps using a hierarchy-building algorithm that combines topic similarity with concept generality and dependencies. Enterprise-focused; no public benchmark.

**[Petal](https://www.petal.org/).** Closed-corpus chat-with-documents + reference manager. RAG over uploaded PDFs with multi-document AI table comparison; 9,000+ citation styles and BibTeX export. Not a search engine over the open literature — complementary to a search skill, not a competitor.

**[AnswerThis](https://answerthis.io/)**. Indexes ~300M papers and frames the workflow as topic → research gaps → supporting literature. Citation-backed gap claims with clickable provenance. Search mechanics not publicly documented.

**[Scinapse](https://www.scinapse.io/)** (Pluto Network). ~250M papers from Microsoft Research / Semantic Scholar / Springer Nature / PubMed; 50,000+ journals; non-profit. Traditional faceted search + trend graphs + rising-paper metrics + an Expert Finder for top researchers by topic.

**[R Discovery](https://discovery.researcher.life/)** (CACTUS/Researcher.Life). 250M+ articles + 40M OA + 3M+ preprints + 32K journals. Personalized recommender (collaborative + content-based) keyed to user reading history. Awareness/discovery (push) model, not query-and-retrieve (pull).

**[STORM / Co-STORM](https://storm-project.stanford.edu/research/storm/)** (Stanford OVAL). STORM as a *search driver*: discover multiple perspectives by surveying related articles → simulate writer↔expert conversations grounded in retrieved sources → use generated follow-up questions to drive new retrieval rounds. Each perspective gives a different query family — directly mitigates single-viewpoint coverage gaps. Co-STORM adds a human-in-the-loop turn-management protocol over a shared dynamic mind map; users can inject utterances to steer search. 70% of surveyed Wikipedia editors felt it helps in pre-writing. **The implication for ResearchForge is that STORM-style perspective generation is a search technique, not just a writing technique.**

**[AlphaXiv](https://www.alphaxiv.org/).** Community discussion layer over arXiv — comments, paper blogs, chat-with-paper, topic communities. Useful as a complementary signal for detecting contested or corrected results. No public API for comment retrieval.

**[NotebookLM](https://notebooklm.google.com/)** (Google). Closed-corpus only — Gemini-grounded RAG over uploaded sources; no open-web search. Hallucination rate measured at ~13% vs. ~40% for ungrounded LLMs in journalistic testing. The right baseline for a "corpus mode" that operates on already-collected papers.

**[SciSpace](https://scispace.com/) Deep Review.** ~280M papers via Semantic Scholar/OpenAlex. Multi-step agentic loop with a visible "thinking" trace showing each iteration's query and added papers — more transparency than most competitors at this layer.

**Galactica successors.** [GeoGalactica](https://arxiv.org/abs/2401.00434) (Jan 2024, 65B-token geoscience pretraining over Galactica) is the only direct successor of note. The takeaway is that single-LLM-as-scientific-encyclopedia is essentially dead as a *search* paradigm — supplanted by grounded RAG. Mirrors the prior-work.md observation that Galactica failed.

**[OpenRead](https://www.openread.academy/).** ~300M papers + open-web; refreshed every 5 minutes. Semantic search + AI summary + highlight-driven Q&A + related-paper graph. No external benchmarks.

**EBSCO AI / [Aria](https://researcharia.com/).** EBSCO's "Generate AI Insights" and "Natural language" assistants layer onto the EBSCO database product: natural language → translated Boolean/keyword query → standard EBSCO retrieval → AI-generated insights on top ([EBSCO AI](https://about.ebsco.com/artificial-intelligence)). Importantly, this pattern keeps traditional search primitives intact and only adds AI on the wrapping — fundamentally different from agentic-RAG systems.

---

## 9. AI search techniques and evaluation

### 9.1 Underlying search techniques

**HyDE (Hypothetical Document Embeddings).** Zero-shot prompt an LLM to *write the answer it expects to exist*, embed the hypothetical document, and use its embedding (not the query embedding) for dense retrieval ([Haystack docs](https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde)). Bridges the query-document length/style gap; outperforms unsupervised Contriever and matches fine-tuned retrievers in many tasks without labels. Cheap upgrade for vague user queries; risk is mis-directed retrieval if the hypothetical is hallucinated.

**Query decomposition for multi-hop QA.** LLM-prompted decomposition templates that emit structured sub-questions; retrieval and answering happen per sub-question and integrate. Recent systems: [PRISM (2025)](https://arxiv.org/html/2510.14278v1) (decomposer + selector); [ReAgent](https://aclanthology.org/2025.emnlp-main.202.pdf) (decompose + retrieve + verify + integrate, with reversible reasoning); [ParallelSearch (2025)](https://arxiv.org/pdf/2508.09303) (RL-trained to decompose parallelizable multi-hop queries into concurrent sub-searches); plan-then-execute patterns (Collab-RAG, RT-RAG). For research questions like "what is the literature on X for materials with Y under Z conditions," explicit decomposition gives both better coverage and clearer provenance.

**Cross-encoder reranking.** Bi-encoder retrieval (dense or sparse) is fast but limited; a cross-encoder reads (query, candidate) jointly through every transformer layer and scores true relevance. Top open option: **[BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-base)** (278M params, multilingual, CPU-feasible for small batches; matches Cohere quality at zero API cost). Top closed option: **Cohere Rerank v3** + Nimble variant for latency. Snapshot: bge-reranker-large-v2 at 0.715 nDCG@10 (145ms p95); Cohere Rerank latest at 0.735 nDCG@10 (210ms p95).

**PaperQA2's RCS — rerank-that-summarizes.** A frontier LLM jointly scores relevance 1–10 *and* produces a chunk summary in context of the query. Two effects: a stronger relevance signal than a small cross-encoder, and a context-density gain (the answer step sees compressed summaries rather than raw chunks). Cost is the obvious trade-off. Should be treated as a separate technique from BGE-style reranking — they can stack.

**Citation verification agents.** Two recent academic agents explicitly target the central failure mode of LLM-generated literature outputs: [CiteAudit](https://arxiv.org/abs/2602.23452) (multi-agent: claim extraction → evidence retrieval → passage matching → calibrated judgment; releases a human-validated benchmark) and [BibAgent](https://arxiv.org/html/2601.16993v1) (end-to-end agentic citation verification with adaptive strategies; for paywalled refs, uses an Evidence Committee that infers validity via downstream citation consensus; ships MisciteBench, 6,350 samples across 254 fields). A standalone "verify-the-citations" step is high-leverage — it directly attacks the 78–90% baseline hallucination rate.

**Other agent patterns.** [BioDiscoveryAgent](https://github.com/snap-stanford/BioDiscoveryAgent) treats search as one tool among many in a closed-loop experiment-design agent. [ToolGen](https://arxiv.org/html/2503.08979v1) integrates tool knowledge directly into LLM parameters via unique tokens. [Google's open-source Gemini-LangGraph deep-research agent](https://towardsdatascience.com/langgraph-101-lets-build-a-deep-research-agent/) uses an `evaluate_research` node that decides at each step whether to re-search or finalize — a clean reference implementation of iterative-retrieval-with-sufficiency-check.

### 9.2 Evaluation benchmarks specific to search

| Benchmark | Focus | What it tests for SEARCH |
|---|---|---|
| **[LitQA2](https://github.com/Future-House/LitQA)** | Multi-paper Q&A from full text | Whether the system retrieved the exact DOI containing the answer in body text. PaperQA2: 85.2% precision / 66% accuracy; surpasses PhD humans. |
| **[ScholarQABench](https://github.com/AkariAsai/OpenScholar)** | Long-form citation-grounded answers across CS / physics / neuro / biomed | 2,967 queries + 208 long-form answers. Multi-domain is the value-add — directly relevant to ResearchForge's scope. |
| **[RAG-QA Arena](https://arxiv.org/abs/2407.13998)** | Long-form RAG across 7 domains; science split has 1,404 Qs over 1.7M docs | Tests domain robustness of retriever. PaperQA2 SOTA +12.4% on science. |
| **[BixBench](https://arxiv.org/abs/2503.00096)** | Agentic computational biology with file inputs | End-to-end agent loop, not pure search. |
| **MisciteBench** (BibAgent 2026) | Miscitation detection | Targets the citation-verification step downstream of search. |
| **Cochrane Elicit case studies** (Lau 2025) | Systematic-review search sensitivity | Gold standard: search recall against a human-conducted review's reference set. Elicit averaged 39.5% sensitivity. The single most damning published recall number on an AI search tool. |
| **Undermind whitepaper** | Gold-standard recovery + top-hit density | 30–80% of systematic-review reference papers recovered; ~10× density gain over Google Scholar. Internal but methodologically careful. |

**The story across these benchmarks.** For the question-answering task, agentic RAG matches or exceeds human experts. For the comprehensive-search task — recall against a reference set — the best published numbers are still 30–80%. That gap is the actual unsolved problem.

---

## 10. Methodology and reporting standards

### PRISMA 2020 and PRISMA-S

The [PRISMA 2020 Statement](https://www.bmj.com/content/372/bmj.n71) (Page et al., *BMJ* 2021) is the umbrella reporting guideline; Item 7 ("Search strategy") requires presenting full search strategies including filters and limits. The [PRISMA-S extension](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8074898/) (Rethlefsen et al. 2021, *J Med Libr Assoc*) specifies 16 reporting items for *where, what, and how* a search was constructed:

- Information sources (databases, registries, websites, grey literature, citation searches)
- Strategy specifics (full Boolean strings, line-by-line)
- Peer review of the strategy
- Limits and filters
- Search dates and updates
- Total records per source and deduplication

PRISMA-S is the right backbone for any reproducible-audit-trail design — every record in the audit log should map to a PRISMA-S item.

### PRISMA-trAIce (2025)

[PRISMA-trAIce](https://www.equator-network.org/) extends PRISMA for AI tool use *in* the review: model identity, version, prompts, training/fine-tuning, human-in-the-loop role, validation against held-out sets. For an agentic literature-search skill, this is the relevant rubric for disclosing what the agent did vs. the human.

### PRESS

The [PRESS 2015 Guideline](https://www.jclinepi.com/article/S0895-4356(16)00058-5/fulltext) (McGowan et al., *J Clin Epidemiol* 2016) is the standard auditing instrument for search strategies, with six domains: translation of the research question, Boolean and proximity operators, subject headings, text-word searching, spelling/syntax/line numbers, and limits/filters. Used by [Cochrane Information Specialists](https://training.cochrane.org/handbook/current/chapter-04) to peer-review every Cochrane search. [Spry & Mierzwinski-Urban (2018)](https://pubmed.ncbi.nlm.nih.gov/30237717/) and [Sampson et al. (2008)](https://pubmed.ncbi.nlm.nih.gov/18605626/) show PRESS-reviewed strategies retrieve significantly more relevant records than unreviewed ones (Sampson reported +21.7% relevant records on average).

### Cochrane Handbook and PROSPERO

[Cochrane Handbook chapter 4](https://training.cochrane.org/handbook/current/chapter-04) is the most thorough single methodological text on search design. Prescriptions: at minimum MEDLINE + Embase + CENTRAL for biomedical SRs; supplement with trial registries; combine controlled vocabulary + free-text; use validated filters (e.g., the Cochrane Highly Sensitive Search Strategy for RCTs); document everything per PRISMA-S. [PROSPERO](https://www.crd.york.ac.uk/prospero/) (NIHR / York) is the international prospective register of systematic reviews — registration prior to screening is a forcing function for search prespecification. Non-biomedical equivalents: [INPLASY](https://inplasy.com/) and [OSF Registries](https://osf.io/registries/).

---

## 11. Search-strategy building blocks

### Question-structuring frameworks

| Framework | Domain | Components |
|---|---|---|
| PICO | Clinical effectiveness | Population, Intervention, Comparison, Outcome |
| PEO | Qualitative / exposure | Population, Exposure, Outcome |
| SPIDER | Mixed-methods / qualitative | Sample, Phenomenon, Design, Evaluation, Research type |
| PCC | Scoping reviews (JBI) | Population, Concept, Context |
| PIRD | Diagnostic test accuracy | Population, Index test, Reference test, Diagnosis |
| **CIMO** | **Management / engineering** | **Context, Intervention, Mechanism, Outcome** |
| SPICE | Service / policy | Setting, Perspective, Intervention, Comparison, Evaluation |

For physical-sciences/engineering, [CIMO (Denyer et al., 2008)](https://journals.sagepub.com/doi/10.1177/1350507608091911) and the "objects–methods–contexts" decomposition are more natural fits than PICO. The [Joanna Briggs Institute's PCC framework](https://jbi-global-wiki.refined.site/space/MANUAL) is the standard for scoping reviews and maps cleanly onto materials-discovery, device-characterization, and other engineering questions.

### Boolean syntax across databases

Standard operators (`AND`, `OR`, `NOT`, parentheses, truncation, phrase quoting, proximity) diverge in ways that break naive copy-paste:

- **PubMed**: `[tiab]`, `[mh]` (MeSH), `[majr]`, automatic term mapping; proximity `:~n` added 2022
- **Web of Science**: `TS=`, `TI=`, `AB=`, `NEAR/n`, `*`, lemmatization
- **Scopus**: `TITLE-ABS-KEY()`, `W/n`, `PRE/n`; separate indexed/author keywords
- **Embase (Elsevier or Ovid)**: `/exp` for Emtree explosion, `:ti,ab`, `NEAR/n`
- **IEEE Xplore**: command search with `("Document Title":term)`; parentheses required around every field
- **INSPEC (EBSCO/Ovid)**: thesaurus terms with subheadings, `.mp.` multi-field
- **arXiv API**: `abs:`, `ti:`, `cat:`; limited Boolean nesting
- **OpenAlex**: REST with `search`, `filter`, `select`; no proximity, no truncation, but excellent concept/topic filters

The [Polyglot Search Translator](https://sr-accelerator.com/#/polyglot) (Bond University SR-Accelerator) handles conversions for major medical databases; engineering databases largely require hand-translation.

### Controlled vocabularies

| Vocabulary | Database | Domain | Access |
|---|---|---|---|
| [MeSH](https://www.nlm.nih.gov/mesh/meshhome.html) | PubMed/MEDLINE | Biomedicine | Free; [MeSH RDF SPARQL](https://id.nlm.nih.gov/mesh/) |
| [Emtree](https://www.elsevier.com/products/embase/emtree) | Embase | Biomed, pharma | Subscription |
| [INSPEC Thesaurus](https://www.theiet.org/publishing/inspec/about/content-coverage/inspec-thesaurus/) | INSPEC | Physics, EE, CS, control | Subscription; XML |
| [IEEE Thesaurus](https://www.ieee.org/publications/services/thesaurus.html) | IEEE Xplore | EE/CS | Free PDF |
| [CAS Index Terms](https://www.cas.org/cas-data/cas-registry) | SciFinder, CAplus | Chemistry | Subscription |
| [GeoRef Thesaurus](https://www.americangeosciences.org/georef/georef-thesaurus-lists) | GeoRef | Earth sciences | Subscription |
| [NASA ADS keywords](https://ui.adsabs.harvard.edu/) | ADS | Astronomy, astrophysics | Free API |
| [PsycINFO Thesaurus](https://www.apa.org/pubs/databases/training/thesaurus) | PsycINFO | Psychology | Subscription |
| [ACM CCS](https://dl.acm.org/ccs) | ACM DL | Computing | Free |
| [MSC](https://mathscinet.ams.org/msc/msc2020.html) | MathSciNet, zbMATH | Mathematics | Free |
| [PhySH](https://physh.aps.org/) | APS journals | Physics | Free JSON |

**When to combine controlled vocab and free text.** Every Cochrane-style search does both: controlled vocab catches the indexed set; free text catches recent papers not yet indexed (MeSH lag is typically 30–180 days) and papers where indexers used different terms. Conventional pattern: `(MeSH_term[mh] OR free_text_synonyms[tiab])` for each concept block, then `AND` the blocks ([Jenkins 2004](https://pubmed.ncbi.nlm.nih.gov/15173666/), Cochrane Handbook §4.4).

**Translation across databases.** Polyglot covers medical; [Yale MeSH Analyzer](https://mesh.med.yale.edu/) diagnoses a search by showing the MeSH/free-text distribution of a seed set; [HeTOP](https://www.hetop.eu/hetop/) does multilingual cross-thesaurus mapping. For engineering, no equivalent exists — INSPEC ↔ IEEE ↔ Compendex translation is largely manual.

---

## 12. Citation chasing and text-mining-assisted search construction

### Citation chasing

**Backward** ("references-of"): pull references of every included paper. Best automated via OpenAlex, Semantic Scholar `/references`, Crossref `/works/{doi}/references`, or Inciteful.

**Forward** ("cited-by"): query "what cites this?" via WoS, Scopus, Google Scholar, Lens, Semantic Scholar, OpenAlex.

[Hinde & Spackman (2015)](https://pubmed.ncbi.nlm.nih.gov/26073415/) and [Wright et al. (2014)](https://pubmed.ncbi.nlm.nih.gov/24559929/) show that citation searching consistently retrieves 10–30% of included studies that keyword searching missed in health-tech assessments.

**Pearl-growing.** Start with one known-relevant paper and iteratively harvest terms/MeSH, follow citations, and refine the search ([Schlosser et al. 2006](https://pubs.asha.org/doi/10.1044/1058-0360%282006/008%29)). The natural mode for an agentic skill — each pearl seeds an embedding query plus a citation expansion.

**Wohlin snowballing.** [Wohlin (2014, EASE)](https://dl.acm.org/doi/10.1145/2601248.2601268) formalized snowballing for systematic reviews in software engineering: seed set → iterative backward + forward passes → stop when no new included studies appear. The [Wohlin et al. (2022) follow-up](https://doi.org/10.1016/j.infsof.2022.106908) compared snowballing vs. database searches and found snowballing alone achieves >90% recall for software-engineering SRs when started from a good seed set. Particularly relevant for engineering where database coverage is patchy.

**Co-citation and bibliographic coupling.** Co-citation (two papers cited together) surfaces conceptual neighbors; bibliographic coupling (two papers sharing references) surfaces methodological neighbors. The algorithmic primitives behind Connected Papers, Inciteful, ResearchRabbit, Litmaps, and CitationGecko. Excel at finding papers a keyword search will miss because terminology shifted, the paper crossed disciplines, or the title is uninformative. Fail when the field is too new (no seed set), the paper is undercited (preprints, niche conferences, negative results), or the paper is cited only for unrelated reasons.

### Text-mining-assisted search development

**Word-frequency harvesting.** Build a seed corpus of 20–50 known-relevant papers; extract n-grams from titles/abstracts/keywords; compute frequency vs. background; feed domain-distinctive terms back into the Boolean string. Tools: [SR-Accelerator Word Frequency Analyser](https://sr-accelerator.com/#/help/wordfreq), [PubReMiner](https://hgserver2.amc.nl/cgi-bin/miner/miner2.cgi), [VOSviewer](https://www.vosviewer.com/), [Bibliometrix](https://www.bibliometrix.org/) (R, with Biblioshiny GUI). [Hausner et al. (2012, *Syst Rev*)](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/2046-4053-1-19) showed objectively-derived text-mined terms outperform expert-only term lists.

**Latent semantic / embedding-based query expansion.** [SPECTER2](https://github.com/allenai/SPECTER) and [SciNCL](https://github.com/malteos/scincl) for scientific paper embeddings; [Semantic Scholar's recommendation API](https://api.semanticscholar.org/api-docs/recommendations); [OpenAlex concept vectors](https://docs.openalex.org/api-entities/concepts); local FAISS/Chroma indexes for "find me 200 more like these 20". Useful inside an agentic loop.

**LLM-assisted Boolean string generation.** [Wang et al. (2023), SIGIR](https://arxiv.org/abs/2302.03495) found ChatGPT-generated queries had higher precision but lower recall than expert searches; the gap closes with iterative refinement and few-shot prompting with PICO scaffolding. [Wang et al. (2024)](https://arxiv.org/abs/2309.05238) found LLM-rewritten queries help screening prioritization more than retrieval. [Alaniz et al. (2024)](https://pubmed.ncbi.nlm.nih.gov/38879179/) found GPT-4 Boolean strings for orthopedic SRs underperformed librarian searches on recall. [Staudinger et al. (2024)](https://arxiv.org/abs/2407.03134) is a comparative benchmark of LLMs for SR query generation.

**Consensus through 2026.** LLMs are excellent term-brainstorming partners and acceptable for first-pass strings, but PRESS-style human or rule-based audit is still required for sensitivity-critical reviews. Cochrane Information Specialists' [2023–2025 evaluations](https://methods.cochrane.org/information-retrieval) warn that LLM-generated Boolean strings systematically miss niche, older, or non-English studies.

---

## 13. Reference management and systematic-review software

### Reference management

| Tool | License | Programmatic | Strengths | Weaknesses |
|---|---|---|---|---|
| [Zotero](https://www.zotero.org/) | Open (AGPL) | [REST Web API](https://www.zotero.org/support/dev/web_api/v3/start) + [translation-server](https://github.com/zotero/translation-server) + local SQLite | OA-friendly, group libraries, ~700 site translators, BetterBibTeX | UI dated |
| [EndNote](https://endnote.com/) | Clarivate, paid | Limited XML; no REST API | WoS integration, large install base | Closed; expensive |
| [Mendeley](https://www.mendeley.com/) | Elsevier, free tier | API sunsetting 2024–2025 | PDF management | Elsevier control |
| [JabRef](https://www.jabref.com/) | Open (MIT) | BibTeX file is the API | LaTeX-native, fetchers for arXiv/DOI/ISBN | BibTeX-centric UI |
| [Papers (ReadCube)](https://www.papersapp.com/) | Paid | Limited | Polished UI | Closed |
| [Paperpile](https://paperpile.com/) | Paid SaaS | Limited | Google Docs integration | Closed |

**Zotero is the standout for automation.** Web API is well-documented and rate-limited but generous; group libraries are first-class collaboration primitives; [translation-server](https://github.com/zotero/translation-server) lets you POST a URL and get back CSL-JSON; [translators](https://github.com/zotero/translators) cover hundreds of publisher sites; [pyzotero](https://github.com/urschrei/pyzotero) is the mature Python client. The natural durable store for a Claude-Agent literature-search skill: write structured CSL-JSON with attachments, tag with search provenance, and the user can open the library in the desktop client.

### Systematic-review platforms

| Platform | License | Strengths | Programmatic | Notes |
|---|---|---|---|---|
| [Rayyan](https://www.rayyan.ai/) | Free for academics; paid tiers | Title/abstract screening, blinded dual review, ML suggestions | REST API (paid) | Most-used free SR screening tool |
| [Covidence](https://www.covidence.org/) | Paid (Cochrane-recommended) | End-to-end SR, RoB tools | Limited; CSV in/out | Site licenses common |
| [DistillerSR](https://www.distillersr.com/) | Commercial enterprise | Full workflow, audit logs, FDA/HTA-grade | REST API | Used by HTA agencies |
| [EPPI-Reviewer 6/Web](https://eppi.ioe.ac.uk/eppireviewer-web/) | Paid (UCL) | Built-in classifier training, ML prioritization | API (limited) | PRISMA-aligned; supports living reviews |
| [SR-Accelerator](https://sr-accelerator.com/) | Free (Bond U) | Polyglot, Word Frequency Analyser, Deduplicator, Spider Citation Search, Disputatron | Some endpoints | A toolbox, not a single platform |
| [ASReview](https://asreview.nl/) | Open (Apache 2.0) | Active-learning screening | Python API + CLI | [van de Schoot et al., *Nat Mach Intell* 2021](https://www.nature.com/articles/s42256-020-00287-7) |
| [Abstrackr](http://abstrackr.cebm.brown.edu/) | Open | Simple screening with ML | Limited | Brown CEBM |
| [CADIMA](https://www.cadima.info/) | Free | Heavily used in agriculture / ecology SRs | CSV in/out | Julius Kühn-Institut |
| [Nested Knowledge](https://nested-knowledge.com/) | Paid SaaS | Living reviews, meta-analysis, visual evidence maps | API | |

**ASReview** is the open-source standout for active-learning screening; the [Nature Machine Intelligence paper](https://www.nature.com/articles/s42256-020-00287-7) reported recall@95% with 8–33% of the workload of full screening across six benchmark SRs. Python API, custom classifiers/feature extractors, fully scriptable — ideal for an agentic pipeline.

**EPPI-Reviewer's** built-in classifier ([Thomas et al., 2017](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-017-0664-7)) is the longest-running production deployment of ML-assisted screening; the engine behind several Cochrane living reviews.

**SR-Accelerator** ([Clark et al., 2020](https://www.jclinepi.com/article/S0895-4356(20)30152-X/fulltext)) is a toolbox of microservices: Polyglot translates strings; the Word Frequency Analyser harvests terms; Spider Citation Search does iterative citation expansion; Deduplicator handles cross-database dedup; Disputatron mediates dual-reviewer conflicts.

---

## 14. Deduplication

The problem: the same paper appears with different DOIs (preprint vs. version-of-record), different author-string formats, OCR-corrupted titles, missing volume/issue, or alternate language titles.

| Tool | License | Approach | Reference |
|---|---|---|---|
| [SR-Accelerator Deduplicator](https://sr-accelerator.com/#/deduplicator) | Free | Multi-field fuzzy match with confidence buckets | [Forbes et al., 2024](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-024-02451-1) |
| [Bramer 2016 EndNote method](https://pubmed.ncbi.nlm.nih.gov/27822157/) | Free protocol | Stepwise EndNote field comparisons | *J Med Libr Assoc* 2016 |
| [ASySD](https://camarades.shinyapps.io/RDedup/) | Open R | Token-based + similarity threshold | [Hair et al., 2023, *Res Synth Methods*](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1638) |
| EndNote 21 dedup | Paid | Author + year + title heuristic | Misses 10–25% per Bramer |
| Zotero duplicate detection | Free | DOI/ISBN + Levenshtein on title | Conservative |
| Covidence dedup | Paid | Built-in | Generally good, opaque |
| pyalex / OpenAlex IDs | Free | OpenAlex `Work` ID or DOI canonicalization | Best programmatic anchor |

**Why dedup is hard.** DOIs aren't universal (no DOI for many conference papers); DOIs differ between preprint and version-of-record; titles get truncated; author lists vary in completeness; Unicode handling differs across exports. The strongest pipelines use a cascade: exact DOI → normalized DOI → OpenAlex ID → fuzzy title + first-author + year → manual review of low-confidence pairs. [McKeown & Mir (2021)](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-021-01583-y) and the [ASySD validation](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1638) are the empirical references.

---

## 15. Bibliometric tools as discovery aids

| Tool | License | Strengths | Programmatic |
|---|---|---|---|
| [VOSviewer](https://www.vosviewer.com/) | Free (Leiden CWTS) | Co-occurrence and citation network maps | JSON I/O |
| [CiteSpace](https://citespace.podia.com/) | Free (Drexel) | Burst detection, structural variation analysis | Java; file-based |
| [Bibliometrix](https://www.bibliometrix.org/) | Open R | Full bibliometric workflow + Biblioshiny GUI | R API |
| [Sci2 Tool](https://sci2.cns.iu.edu/) | Free (Indiana CNS) | Scriptable network/temporal analysis | CLI |
| [OpenAlexR](https://github.com/ropensci/openalexR) | Open R | R wrapper for OpenAlex | API client |
| [pyalex](https://github.com/J535D165/pyalex) | Open Python | Python wrapper for OpenAlex | API client |

**When bibliometric mapping catches what keyword search misses.** Terminology shifts (e.g., "redox-flow batteries" was "regenerative fuel cells" pre-2000); cross-disciplinary diffusion (a method paper from chemistry cited heavily in materials science under different vocabulary); influential review/precursor papers that don't contain modern keywords but are reference hubs; research fronts via burst analysis ([Chen 2006](https://onlinelibrary.wiley.com/doi/10.1002/asi.20317)). [Aria & Cuccurullo (2017)](https://www.sciencedirect.com/science/article/abs/pii/S1751157717300500) is the Bibliometrix methodological reference.

---

## 16. Cross-cutting findings

**Single-source recall is uniformly inadequate.** Bramer's recall data, the Cochrane Elicit evaluation, and Undermind's gold-standard recovery numbers all converge on the same conclusion. Elicit's Semantic-Scholar-only single-source design is the clearest counterexample to "one big index is enough." OpenAlex + Semantic Scholar + arXiv + Crossref (+ PubMed for biomed adjacencies) is now the implicit minimum for credible coverage.

**Reproducibility of search strategies is poor in practice.** A [2024 cross-sectional metaresearch study (Pieper et al.)](https://www.sciencedirect.com/science/article/pii/S0895435623003190) found systematic-review search strategies are poorly reported and not reproducible. PRISMA-S exists precisely to address this gap. Most current AI search tools (Elicit, Perplexity, OpenAI/Claude/Gemini Deep Research) do not satisfy PRISMA-S's full-strategy-archive requirement. PaperQA2 and OpenScholar (open code) are the only mainstream agents that do.

**Two iteration patterns dominate AI search.** (a) **PaperQA2-style tool agent** — discrete `search`, `gather_evidence`, `answer` tools the agent decides when to call. (b) **Model-as-agent** — OpenAI Deep Research, Anthropic Research, Gemini Deep Research — where the search loop is internalized in an RL-trained policy. Both work; the first is auditable, the second is more flexible. ResearchForge's design context (verifiable audit trail) strongly favors the first.

**RCS is the dark-horse technique.** PaperQA2's contextual summarization is doing as much work as the cross-encoder reranker in classical pipelines and produces a synthesis-ready summary as a side effect. Should be treated as a first-class option, not just classical rerank.

**Recall-vs-precision is a mode choice, not a parameter.** Undermind converges on saturation (recall-favoring). Consensus truncates aggressively (precision-favoring). FutureHouse separates this into Falcon vs. Crow. Prior-art search, evidence-on-question, and full-corpus review are different success criteria with different stop conditions.

**Citation verification is now its own subfield.** CiteAudit and BibAgent (both 2026) are dedicated multi-agent systems for verifying that cited claims are supported by the cited source. This step belongs *after* synthesis in any serious search-and-compile workflow and directly attacks the 78–90% baseline hallucination rate documented for ungrounded LLMs.

**Engineering grey literature is under-served by every AI search product.** None of the major AI tools (Elicit, Consensus, Undermind, FutureHouse, Perplexity, OpenAI/Anthropic/Gemini Deep Research, SciSpace) integrate DOE OSTI, NASA NTRS, IAEA INIS, USGS, or EPA reports as first-class sources. For physical-sciences and engineering work, this is a real and exploitable gap.

**Standards and engineering handbooks are a structural coverage gap.** Closed paywalls make ASTM, ISO, IEEE-SA, ASME, SAE, and the major engineering reference handbooks (Knovel, CRC, AccessEngineering) effectively unreachable for a portable agent. NIST publications are the only fully open large-scale standards corpus. ResearchForge should be honest about this gap and provide explicit flags when a query likely needs paywalled standards/handbook coverage.

---

## 17. Design implications for the source search and compilation skill

A direct mapping from the findings above to specific design choices for the planned skill.

**Multi-source first-stage retrieval, in parallel.** OpenAlex + Crossref + Semantic Scholar + arXiv as the default cross-cutting layer (all CC0 or near-CC0, well-documented APIs); add PubMed/Europe PMC when the query touches biomedicine; add domain-specific repositories (NASA ADS, INSPIRE-HEP, IEEE Xplore, DOE OSTI, NASA NTRS, Materials Project, NIST WebBook, PubChem) when the query domain matches. Deduplicate via DOI → OpenAlex ID → fuzzy title+author+year cascade.

**Open infrastructure as the spine, not as a fallback.** Treat OpenAlex + Crossref + DataCite as the primary surface, not as a secondary backup. Premium indexes (WoS, Scopus, Engineering Village, INSPEC, SciFinder, Reaxys) are escalation paths when the user has institutional access and the query specifically benefits from controlled vocabulary or citation provenance the open layer can't provide.

**Coverage of engineering grey literature is a differentiator.** First-class integration of DOE OSTI, NASA NTRS, EPA, USGS, and IAEA INIS — all public-domain APIs — would directly distinguish the skill from any commercial competitor. Combined with PatentsView + EPO OPS + Google Patents BigQuery for patents and DataCite + Materials Project + NIST WebBook for data, the non-journal coverage would exceed what Elicit, Consensus, Undermind, and FutureHouse offer.

**Two-stage retrieve→rerank by default.** Hybrid first-stage (BM25 + dense embedding) per source where the source's API supports it; otherwise the API's native ranking. Cross-encoder rerank with [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-base) as the default (free, self-hostable); Cohere Rerank as a paid escalation. PaperQA2-style RCS on top survivors when the downstream task is question-answering or synthesis.

**HyDE-expand under-specified queries.** A cheap LLM-driven query expansion step that runs before retrieval for vague user prompts.

**Agentic iteration with explicit stop conditions.** PaperQA2-style tool agent rather than model-as-agent (auditability requirement). Stop conditions: (a) saturation criterion (Undermind-style — diminishing return of new relevant hits), (b) gold-standard recovery threshold when the user provides a seed set, or (c) budget cap. Re-search on insufficiency.

**STORM/Co-STORM perspective generation as a search driver, not just a writing tool.** Before issuing queries, imagine three or four stakeholder/sub-topic perspectives and run a search family per perspective. Directly mitigates single-viewpoint coverage gaps — the failure mode that hurt Elicit's Cochrane recall numbers.

**Citation-graph expansion as a complementary mode, not a replacement.** OpenAlex `referenced_works` + `related_works` + Semantic Scholar `/references` and `/citations` for one-hop and two-hop neighborhood expansion. Re-rank the expanded neighborhood semantically — pure citation-graph traversal surfaces noise.

**Wohlin-style snowballing for engineering corpora.** Particularly where journal-database coverage is patchy (software engineering, applied chemistry, energy systems), explicit forward+backward snowballing from a seed set is a known high-recall technique that should be a first-class mode.

**Mode parameter for success criteria.** Three modes with different defaults: (a) **prior-art / "has anyone done X"** — Owl-style, recall-favoring, saturation stop; (b) **evidence on a question** — Consensus-style, top-k precision, hard truncation; (c) **full corpus for review** — Falcon-style, completeness within scope, PRISMA-S-grade audit trail. The same retrieval primitives, different budgets and stop conditions.

**Reproducibility artifact per run.** A machine-readable JSON record satisfying PRISMA-S and PRISMA-trAIce fields: per-source provider, full query string, parameters, timestamp, retrieved DOIs, dedup decisions, rerank scores, RCS scores, agent's iteration trace, human override events. Re-runnable.

**Coverage report at the end of every run.** Explicit "what we did not search" — sources unindexed, paywalled, language-filtered, date-bounded, behind TDM agreements not granted. Surface this as a structured output, not buried in a log.

**Zotero as the durable store.** Output CSL-JSON via the Zotero Web API or translation-server; tag with search provenance; the user can open the library in any Zotero client. Avoids re-inventing the reference-management layer.

**Citation verification as a separate step.** A CiteAudit/BibAgent-style claim → evidence-retrieval → passage-matching pass before any citation is emitted by a downstream synthesis or report skill. Operates against the OpenScholar-baseline 78–90% citation hallucination problem.

**Explicit "needs paywall" flags.** When a query likely requires ASTM/ISO standards, engineering handbooks, or other paywalled sources, the skill should say so rather than silently returning only the openly-available subset. The user should know what they aren't seeing.

**Human-in-the-loop checkpoints between substages.** Default on; full-auto is a flag. The user can inspect and edit query families, the deduplicated source list, the rerank scores, and the screening decisions.

**Model-agnostic with hot-swappable model choice.** Frontier closed-source models for the verification and RCS layers (where hallucination cost is high); cheaper models acceptable for query reformulation and lightweight summarization. Skill should accept a model parameter and degrade gracefully.

The frontier on AI-assisted *answering* is largely solved (PaperQA2, OpenScholar exceed PhD experts). The frontier on AI-assisted *recall and reproducibility* is not — 30–80% gold-standard recovery and 39.5% sensitivity vs. Cochrane human reviews are the numbers to beat. A skill that genuinely composes multi-source retrieval, agentic iteration with saturation, hybrid + rerank + RCS, perspective-driven query families, snowballing where coverage is patchy, full engineering grey-literature integration, and post-hoc citation verification — with a fully inspectable PRISMA-S/PRISMA-trAIce run record — would push meaningfully past anything in the current commercial landscape.

---

## 18. Sources

### Open scholarly infrastructure

- [OpenAlex](https://openalex.org/) / [API docs](https://developers.openalex.org/) / [Rate limits and authentication](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication) / [API keys announcement](https://groups.google.com/g/openalex-users/c/rI1GIAySpVQ)
- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [Semantic Scholar API](https://api.semanticscholar.org/api-docs/)
- [OpenCitations](https://opencitations.net/) / [Indexes blog](https://opencitations.hypotheses.org/category/opencitations-indexes)
- [Unpaywall API](https://unpaywall.org/products/api)
- [DataCite REST API](https://support.datacite.org/docs/api)
- [ORCID Public API](https://info.orcid.org/documentation/api-tutorials/)
- [ROR](https://ror.org/) / [ROR API](https://ror.readme.io/)
- [CORE API](https://core.ac.uk/services/api) / [CORE in Nature Scientific Data 2023](https://www.nature.com/articles/s41597-023-02208-w)

### Premium bibliographic indexes

- [Web of Science Core Collection](https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/web-of-science-core-collection/) / [Coverage details](https://clarivate.libguides.com/librarianresources/coverage)
- [Scopus content](https://www.elsevier.com/products/scopus/content) / [Elsevier Developer Portal](https://dev.elsevier.com/sc_apis.html)
- [Dimensions](https://www.digital-science.com/products/dimensions/) / [Frontiers 2025 on the Dimensions API](https://www.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2025.1514938/full)
- [Engineering Village Databases](https://www.elsevier.com/products/engineering-village/databases) / [Compendex](https://www.elsevier.com/products/engineering-village/databases/compendex)
- [INSPEC](https://www.theiet.org/publishing/inspec/) / [INSPEC Thesaurus](https://www.theiet.org/publishing/inspec/about/content-coverage/inspec-thesaurus/)
- [CAS SciFinder](https://www.cas.org/solutions/cas-scifinder-discovery-platform/cas-scifinder) / [CAS Common Chemistry](https://commonchemistry.cas.org/)
- [Reaxys](https://www.elsevier.com/products/reaxys)

### Discovery engines and recall evaluations

- [Google Scholar — Wikipedia](https://en.wikipedia.org/wiki/Google_Scholar)
- [Khabsa & Giles, 2014, PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0093949)
- [Orduña-Malea et al. 2015](https://link.springer.com/article/10.1007/s11192-014-1455-8)
- [Gusenbauer & Haddaway 2020, Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/jrsm.1378)
- [BASE](https://www.base-search.net/) / [BASE API](https://api.base-search.net/)
- [Lens.org](https://www.lens.org/) / [Lens APIs and Bulk Data](https://about.lens.org/lens-apis/)
- [Bramer et al. 2017 — Optimal database combinations](https://pmc.ncbi.nlm.nih.gov/articles/PMC5718002/)
- [Pieper et al. 2024 — search strategies poorly reproducible](https://www.sciencedirect.com/science/article/pii/S0895435623003190)

### Domain-specific repositories

- [arXiv API](https://info.arxiv.org/help/api/user-manual.html) / [arXiv bulk data](https://info.arxiv.org/help/bulk_data.html) / [arXiv blog 2025](https://blog.arxiv.org/2025/)
- [bioRxiv FAQ](https://www.biorxiv.org/about/FAQ) / [medRxiv FAQ](https://www.medrxiv.org/about/FAQ) / [openRxiv](https://www.openrxiv.org/)
- [ChemRxiv FAQs](https://chemrxiv.org/faqs) / [EarthArXiv](https://eartharxiv.org/) / [engrXiv](https://engrxiv.org/) / [TechRxiv](https://www.techrxiv.org/)
- [OSF Preprints API](https://developer.osf.io/) / [RePEc/IDEAS](https://ideas.repec.org/) / [EconStor](https://www.econstor.eu/)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) / [E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/) / [PMC for Developers](https://pmc.ncbi.nlm.nih.gov/tools/developers/) / [Updated PMC E-Utilities 2026](https://ncbiinsights.ncbi.nlm.nih.gov/2026/01/06/updated-pmc-e-utilities/)
- [Europe PMC RESTful Web Service](https://europepmc.org/RestfulWebService)
- [S2ORC](https://github.com/allenai/s2orc) / [S2ORC ACL Anthology](https://aclanthology.org/2020.acl-main.447/)
- [NASA ADS API](https://ui.adsabs.harvard.edu/help/api/)
- [INSPIRE-HEP](https://inspirehep.net/) / [INSPIRE REST API](https://github.com/inspirehep/rest-api-doc)
- [IEEE Xplore Developer Portal](https://developer.ieee.org/) / [DBLP API](https://dblp.org/faq/13501473.html) / [OpenReview API](https://docs.openreview.net/getting-started/using-the-api)
- [Elsevier Developer Portal](https://dev.elsevier.com/) / [Springer Nature APIs](https://dev.springernature.com/) / [Wiley TDM](https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining)

### Sources beyond journal articles

- [HathiTrust](https://www.hathitrust.org/) / [HathiTrust Bibliographic API](https://www.hathitrust.org/bib_api) / [HTRC](https://www.hathitrust.org/htrc)
- [Internet Archive](https://archive.org/) / [Internet Archive Scholar](https://scholar.archive.org/)
- [Open Library API](https://openlibrary.org/developers/api) / [OAPEN](https://www.oapen.org/) / [DOAB](https://www.doabooks.org/) / [LibreTexts](https://libretexts.org/) / [Open Textbook Library](https://open.umn.edu/opentextbooks)
- [OATD](https://oatd.org/) / [DART-Europe](https://www.dart-europe.eu/) / [NDLTD](https://ndltd.org/)
- [DOE OSTI](https://www.osti.gov/) / [OSTI.GOV API](https://www.osti.gov/api/v1/docs)
- [NASA NTRS API](https://ntrs.nasa.gov/api/openapi.json)
- [DTIC](https://discover.dtic.mil/) / [USGS Publications Warehouse API](https://pubs.er.usgs.gov/documentation/web_service_documentation) / [GovInfo API](https://api.govinfo.gov/docs/)
- [World Bank Open Knowledge Repository](https://openknowledge.worldbank.org/) / [IAEA INIS](https://www.iaea.org/resources/databases/inis)
- [NIST Publications](https://www.nist.gov/publications) / [NIST PDR](https://data.nist.gov/sdp/) / [NIST SP 800](https://csrc.nist.gov/publications/sp800)
- [USPTO PatentsView API](https://patentsview.org/apis/api-endpoints) / [EPO OPS](https://developers.epo.org/) / [Google Patents BigQuery](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data) / [WIPO PatentScope](https://patentscope.wipo.int/) / [CPC](https://www.cooperativepatentclassification.org/)
- [Zenodo API](https://developers.zenodo.org/) / [Figshare API](https://docs.figshare.com/) / [Dryad API](https://datadryad.org/api/v2/docs/) / [Dataverse API](https://guides.dataverse.org/en/latest/api/)
- [Materials Project API](https://api.materialsproject.org/docs) / [NIST WebBook](https://webbook.nist.gov/chemistry/) / [NOMAD API](https://nomad-lab.eu/prod/v1/api/v1/) / [AFLOW API](http://aflowlib.org/API/) / [OQMD REST API](http://oqmd.org/static/docs/restful.html) / [PubChem PUG-REST](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest) / [ChEMBL API](https://chembl.gitbook.io/chembl-interface-documentation/)
- [NASA Earthdata CMR](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html) / [Copernicus CDS API](https://cds.climate.copernicus.eu/api-how-to)
- [re3data](https://www.re3data.org/) / [FAIRsharing](https://fairsharing.org/) / [DataCite Commons](https://commons.datacite.org/)
- [Software Heritage](https://www.softwareheritage.org/) / [GitHub-Zenodo integration](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)
- [Papers With Code API](https://paperswithcode.com/api/v1/docs/) / [Hugging Face Hub](https://huggingface.co/docs/hub/api)

### Citation-network and federated discovery

- [Connected Papers](https://www.connectedpapers.com/) / [Litmaps](https://www.litmaps.com/) / [ResearchRabbit](https://www.researchrabbit.ai/) / [Inciteful](https://inciteful.xyz/) / [CitationGecko](https://github.com/CitationGecko/citation-network-explorer)
- [VOSviewer](https://www.vosviewer.com/) / [CitNetExplorer](https://www.citnetexplorer.nl/) / [Open Knowledge Maps](https://openknowledgemaps.org/)
- [Effortless Academic: Litmaps vs ResearchRabbit vs Connected Papers 2026](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/)
- [Aaron Tay — ResearchRabbit 2025 revamp](https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative)
- [Inside WorldCat](https://www.oclc.org/en/worldcat/inside-worldcat.html) / [Marshall Breeding on Index-Based Discovery](https://journals.ala.org/index.php/ltr/article/view/6874/9255)

### AI-assisted search agents — search mechanics

- [Elicit Keyword Search](https://elicit.com/blog/introducing-keyword-search) / [Lau et al. 2025 Cochrane evaluation of Elicit](https://onlinelibrary.wiley.com/doi/full/10.1002/cesm.70050)
- [Consensus pipeline writeup](https://consensus.app/home/blog/how-consensus-works/) / [Elastic case study](https://www.elastic.co/customers/consensus) / [ELSER blog](https://www.elastic.co/search-labs/blog/introducing-elastic-learned-sparse-encoder) / [Consensus Scholar Agent](https://help.consensus.app/en/articles/12641232-scholar-agent)
- [Undermind whitepaper](https://www.undermind.ai/whitepaper.pdf)
- [PaperQA2 GitHub](https://github.com/Future-House/paper-qa) / [PaperQA2 Nature paper](https://arxiv.org/html/2409.13740v2) / [LitQA2](https://github.com/Future-House/LitQA)
- [OpenScholar in Nature 2025](https://www.nature.com/articles/s41586-025-10072-4) / [OpenScholar GitHub](https://github.com/AkariAsai/OpenScholar)
- [FutureHouse platform launch](https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents)
- [Perplexity Academic filter](https://docs.perplexity.ai/guides/academic-filter-guide)
- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) / [Deep Research system card](https://cdn.openai.com/deep-research-system-card.pdf)
- [Gemini Deep Research](https://gemini.google/overview/deep-research/)
- [Anthropic multi-agent research blog](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Iris.ai](https://iris.ai/blog/cut-through-the-noise-with-ai-powered-literature-search) / [Petal](https://www.petal.org/) / [AnswerThis Research Gap Finder](https://answerthis.io/ai/research-gap-finder) / [Scinapse](https://insights.pluto.im/comprehensive-search-scinapse-for-academic-data/) / [R Discovery](https://discovery.researcher.life/)
- [Stanford STORM project](https://storm-project.stanford.edu/research/storm/) / [STORM GitHub](https://github.com/stanford-oval/storm)
- [AlphaXiv](https://www.alphaxiv.org/) / [SciSpace](https://scispace.com/)
- [GeoGalactica](https://arxiv.org/abs/2401.00434)
- [EBSCO AI features](https://about.ebsco.com/artificial-intelligence)

### AI search techniques and benchmarks

- [HyDE](https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde)
- [PRISM agentic multi-hop retrieval](https://arxiv.org/html/2510.14278v1) / [ParallelSearch](https://arxiv.org/pdf/2508.09303) / [ReAgent](https://aclanthology.org/2025.emnlp-main.202.pdf)
- [BAAI BGE reranker](https://huggingface.co/BAAI/bge-reranker-base)
- [RAG-QA Arena](https://arxiv.org/abs/2407.13998) / [PaperQA2 SOTA on RAG-QA Arena](https://www.futurehouse.org/research-announcements/paperqa2-achieves-sota-performance-on-rag-qa-arena-science-benchmark)
- [CiteAudit](https://arxiv.org/abs/2602.23452) / [BibAgent](https://arxiv.org/html/2601.16993v1)
- [Agentic AI for Scientific Discovery survey](https://arxiv.org/html/2503.08979v1)

### Methodology and reporting standards

- [PRISMA 2020 Statement (BMJ)](https://www.bmj.com/content/372/bmj.n71)
- [PRISMA-S (J Med Libr Assoc)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8074898/)
- [PRESS 2015 Guideline (J Clin Epidemiol)](https://www.jclinepi.com/article/S0895-4356(16)00058-5/fulltext)
- [Cochrane Handbook ch. 4 — Searching for Studies](https://training.cochrane.org/handbook/current/chapter-04)
- [PROSPERO](https://www.crd.york.ac.uk/prospero/) / [INPLASY](https://inplasy.com/) / [OSF Registries](https://osf.io/registries/)
- [Sampson et al. 2008 — PRESS validation](https://pubmed.ncbi.nlm.nih.gov/18605626/)
- [Spry & Mierzwinski-Urban 2018](https://pubmed.ncbi.nlm.nih.gov/30237717/)
- [CIMO framework (Denyer et al. 2008)](https://journals.sagepub.com/doi/10.1177/1350507608091911)
- [JBI Manual (PCC framework)](https://jbi-global-wiki.refined.site/space/MANUAL)

### Citation chasing and text-mining

- [Hinde & Spackman 2015](https://pubmed.ncbi.nlm.nih.gov/26073415/) / [Wright et al. 2014](https://pubmed.ncbi.nlm.nih.gov/24559929/)
- [Schlosser et al. 2006 — Pearl-growing](https://pubs.asha.org/doi/10.1044/1058-0360%282006/008%29)
- [Wohlin 2014 EASE](https://dl.acm.org/doi/10.1145/2601248.2601268) / [Wohlin et al. 2022](https://doi.org/10.1016/j.infsof.2022.106908)
- [Hausner et al. 2012 — text-mined search terms](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/2046-4053-1-19)
- [Wang et al. 2023 — ChatGPT Boolean queries](https://arxiv.org/abs/2302.03495) / [Wang et al. 2024](https://arxiv.org/abs/2309.05238) / [Staudinger et al. 2024](https://arxiv.org/abs/2407.03134)
- [Cochrane Information Retrieval Methods Group](https://methods.cochrane.org/information-retrieval)

### Controlled vocabularies and translation

- [MeSH RDF SPARQL](https://id.nlm.nih.gov/mesh/) / [Polyglot Search Translator](https://sr-accelerator.com/#/polyglot) / [Yale MeSH Analyzer](https://mesh.med.yale.edu/) / [HeTOP](https://www.hetop.eu/hetop/)

### Reference management and SR software

- [Zotero Web API](https://www.zotero.org/support/dev/web_api/v3/start) / [translation-server](https://github.com/zotero/translation-server) / [pyzotero](https://github.com/urschrei/pyzotero)
- [Rayyan](https://www.rayyan.ai/) / [Covidence](https://www.covidence.org/) / [DistillerSR](https://www.distillersr.com/) / [EPPI-Reviewer](https://eppi.ioe.ac.uk/eppireviewer-web/) / [SR-Accelerator](https://sr-accelerator.com/) / [ASReview](https://asreview.nl/) / [Nested Knowledge](https://nested-knowledge.com/)
- [van de Schoot et al., Nat Mach Intell 2021 — ASReview](https://www.nature.com/articles/s42256-020-00287-7)
- [Clark et al. 2020 — SR-Accelerator](https://www.jclinepi.com/article/S0895-4356(20)30152-X/fulltext)
- [Thomas et al. 2017 — EPPI-Reviewer classifier](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-017-0664-7)

### Deduplication

- [SR-Accelerator Deduplicator](https://sr-accelerator.com/#/deduplicator) / [Forbes et al. 2024](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-024-02451-1)
- [Bramer 2016 EndNote method](https://pubmed.ncbi.nlm.nih.gov/27822157/)
- [ASySD — Hair et al. 2023](https://onlinelibrary.wiley.com/doi/10.1002/jrsm.1638)
- [McKeown & Mir 2021](https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-021-01583-y)

### Bibliometric tools

- [VOSviewer](https://www.vosviewer.com/) / [CiteSpace](https://citespace.podia.com/) / [Bibliometrix](https://www.bibliometrix.org/) / [Sci2 Tool](https://sci2.cns.iu.edu/) / [OpenAlexR](https://github.com/ropensci/openalexR) / [pyalex](https://github.com/J535D165/pyalex)
- [Aria & Cuccurullo 2017 — Bibliometrix](https://www.sciencedirect.com/science/article/abs/pii/S1751157717300500)
- [Chen 2006 — CiteSpace burst detection](https://onlinelibrary.wiley.com/doi/10.1002/asi.20317)

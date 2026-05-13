# How to find an open-access copy of a paper

The skill's `scripts/find_open_access.py` automates this — but here's what it tries, in order, and why each is useful.

## URL ranking (when the script returns multiple candidates)

When `find_open_access.py` returns multiple URLs for a DOI, prefer them in this order:

1. **Unpaywall (best PDF)** — most directly tested for OA availability
2. **OpenAlex / Semantic Scholar PDF** — high-confidence PDF URLs
3. **Europe PMC / PMC HTML or PDF** — reliable for biomedical/chemistry papers
4. **CORE** — institutional-repository copies (sometimes preprints, sometimes published)
5. **Wayback Machine snapshot** — last resort; may be a stale or partial copy

Skip Wayback in favor of any of the above when available. If the publisher landing page is one of the candidates and OA is confirmed, that's the most authoritative copy.

If multiple candidates are returned and none are obvious, fetch the first one, verify the title and DOI match expectations, and proceed. If it doesn't match, try the next.

## Discovery APIs (preferred — programmatic, free)

### 1. Unpaywall — `https://api.unpaywall.org/v2/<DOI>?email=<your-email>`

Best dedicated open-access tracker. Free, no key required (just an email parameter for politeness). Returns the paper's `best_oa_location` plus all known OA locations with PDF URLs and host types (publisher, repository, etc.). Funded by the Open Knowledge Foundation; used by major academic search engines.

**Returns:** `best_oa_location.url_for_pdf`, multiple `oa_locations`.

### 2. OpenAlex — `https://api.openalex.org/works/doi:<DOI>`

Newer comprehensive index (replaced Microsoft Academic Graph). No API key required for moderate use. Returns OA URL plus all known locations including preprint servers and institutional repositories.

**Returns:** `open_access.oa_url`, `primary_location.pdf_url`, `locations[].pdf_url`.

### 3. Semantic Scholar — `https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=openAccessPdf,...`

Often has direct PDF URLs when the paper has been indexed. Good for AI/ML papers especially.

**Returns:** `openAccessPdf.url`.

### 4. Europe PMC — `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:"<DOI>"&format=json`

Specifically for life sciences / biomedical papers but indexes a lot of chemistry too. Returns PMC IDs and full-text URLs.

**Returns:** `pmcid`, `fullTextUrlList[]`.

### 5. CORE — `https://api.core.ac.uk/v3/search/works?q=doi:"<DOI>"`

Repository aggregator. Often has institutional-repository copies that other APIs miss.

**Returns:** `downloadUrl`.

### 6. Wayback Machine — `https://archive.org/wayback/available?url=https://doi.org/<DOI>`

Last resort: an archived snapshot of the publisher page. Useful for dead links or temporarily-unavailable papers.

## Manual / less-automatable sources

When the APIs all return empty, try these in this order:

1. **PubMed Central direct link** — if the paper has a PMID, `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` often hosts the full text. Search PubMed for the title to get the PMID.
2. **The author's institutional repository.** Search for the corresponding author + institution + paper title.
3. **ChemRxiv preprint** — `https://chemrxiv.org/` has preprints for many ACS/RSC chemistry papers. Often the preprint is the same content as the published version.
4. **arXiv preprint** — for physics-adjacent or computational papers.
5. **ResearchGate** — frequently has author-uploaded copies, though access can be inconsistent.
6. **Google Scholar** — searches for the paper and shows free PDF links (the green "[PDF]" tag) when available. Manual but high yield.
7. **OSTI** (osti.gov) — for US government-funded research; many DOE-funded papers have public-access manuscript copies here.
8. **HAL** (hal.science) — French archive; many EU-funded papers.
9. **ZENODO** — if the paper has data deposits, the dataset entry sometimes includes the full paper.
10. **The paper's "Supporting Information" page** — even if the main article is paywalled, the SI is often free. Many useful redox-potential tables live in SI.
11. **Direct email to the corresponding author** — out of automation scope, but acceptable as a maintainer action.

## What NOT to use

- **Sci-Hub / LibGen / Anna's Archive** — copyright-questionable. Don't use these for production data extraction even though they sometimes have papers the legitimate routes don't. The extracted data would have ambiguous licensing.

## Troubleshooting

**"All APIs return empty but I know the paper is OA."** Try the publisher's site directly via `web_fetch`. Some publishers (especially RSC, Nature) have OA papers that are missed by the aggregators.

**"PDF URL works but the file is only the abstract."** Some publishers serve a "preview PDF" with only the first page. Look at the file size — if it's <500 KB for a research paper, it's probably truncated. Check OA aggregators for the full version.

**"Got the PDF but it's behind a JS gate."** Try `pdftotext -layout <pdf>` if you have the file locally. Many "JS-gated" PDFs are still readable as text.

**"The DOI resolves but the title looks wrong."** That's a real catch — the citation in the database is wrong. Fix it before extracting from the wrong paper.

## Practical workflow

```bash
# Try to find an OA copy
python scripts/find_open_access.py 10.1038/srep39101 --email me@example.com

# If multiple URLs are returned, prefer the one from a reputable host
# (publisher > PMC > university repo > preprint server)

# Once you have a URL, fetch it
curl -L -o paper.pdf "<URL>"

# Verify the file is the right paper
pdftotext paper.pdf - | head -20

# Then extract using the protocol in SKILL.md
```

# Melting and Boiling Point OA Test Corpus

Built from Europe PMC search results, targeted web/DOI lookups, and the official PMC Open Access Subset package service.
The verified corpus contains 164 open-access article records with manually confirmed melting-point or
boiling-point data in article text/tables. The first verified pass produced 62 records; the expansion
added 102 more records after manual verification. Records without extractable data, rejected expansion
artifacts, and XML-only abstract-like records were moved out of the verified corpus.

## Layout

- `articles/`: one directory per selected paper, with `article.nxml`, `article_text.txt`, `article.pdf`, and `metadata.json`.
- `packages/`: source PMC OA tarballs were removed after extraction to save disk space.
- `manifest.csv`: spreadsheet-friendly index.
- `manifest.jsonl`: complete line-delimited metadata.

## Category Counts

- boiling_point: 7
- measurement_or_data: 9
- synthetic_organic: 148

## Latest Expansion

- Expansion records kept after manual verification: 102
- Expansion records moved to `review_no_mp_bp_data/`: 14
- Expansion manual-verification pass rate: 87.9% (102/116)
- Rejected during the final top-up screening run: 132
- Current verified corpus size: 164

## Source Notes

- Europe PMC REST search: https://www.ebi.ac.uk/europepmc/webservices/rest/search
- PMC OA Web Service: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi
- PMC FTP Service documentation notes that, as of April 13, 2026, legacy OA files are under
  `https://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/`.
- Licenses are article-level values reported by the PMC OA service and are recorded in `manifest.csv`
  and each `metadata.json`.

#!/usr/bin/env python3
"""Append targeted PMC OA property-measurement/modeling papers to the corpus."""

from __future__ import annotations

import csv
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pmc_corpus as core  # noqa: E402


TARGETS = [
    ("PMC12395778", "AI-powered prediction of critical properties and boiling points", "boiling_point"),
    ("PMC12573032", "Prioritizing data quality for normal boiling points of organic compounds", "boiling_point"),
    ("PMC4702524", "How accurately can we predict the melting points of drug-like compounds", "measurement_or_data"),
    ("PMC8122861", "Group contribution estimation of ionic liquid melting points", "measurement_or_data"),
    ("PMC4724158", "Models to predict melting and pyrolysis point data mined from patents", "measurement_or_data"),
    ("PMC2603525", "Artificial ant colony case study of melting point prediction", "measurement_or_data"),
    ("PMC3127127", "QSPR study of aliphatic alcohols", "measurement_or_data"),
    ("PMC12004525", "Conformation importance in data-driven property prediction models", "measurement_or_data"),
    ("PMC8697427", "Thermodynamic properties of active pharmaceutical ingredients", "measurement_or_data"),
    ("PMC11846678", "Topological descriptors and physical properties via QSPR", "measurement_or_data"),
    ("PMC3685234", "Molecular descriptors for structure-property relationships", "measurement_or_data"),
    ("PMC6146921", "Quadratic indices for predicting physical properties", "measurement_or_data"),
]


def load_existing() -> list[dict]:
    if not core.MANIFEST_JSONL.exists():
        return []
    records = []
    for line in core.MANIFEST_JSONL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def update_outputs(records: list[dict]) -> None:
    core.MANIFEST_JSONL.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    fieldnames = [
        "category",
        "pmcid",
        "pmid",
        "doi",
        "title",
        "journal",
        "pub_year",
        "license",
        "citation",
        "melting_point_mentions",
        "boiling_point_mentions",
        "mp_numeric_contexts",
        "bp_numeric_contexts",
        "pdf",
        "xml",
        "text",
        "package",
        "pmc_url",
        "oa_package_url",
        "seed_query",
    ]
    with core.MANIFEST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    counts: dict[str, int] = {}
    for record in records:
        counts[record["category"]] = counts.get(record["category"], 0) + 1
    summary = "\n".join(f"- {name}: {count}" for name, count in sorted(counts.items()))
    core.README.write_text(
        f"""# Melting and Boiling Point OA Test Corpus

Built from Europe PMC search results, targeted web/DOI lookups, and the official PMC Open Access Subset package service.
The corpus contains {len(records)} open-access article records selected because their full text contains melting-point
or boiling-point mentions with numeric context, or because the paper is specifically about thermophysical-property
measurement, data quality, estimation, or prediction.

## Layout

- `articles/`: one directory per selected paper, with `article.nxml`, `article_text.txt`, `article.pdf`, and `metadata.json`.
- `packages/`: the source PMC OA `.tar.gz` package for each selected article.
- `manifest.csv`: spreadsheet-friendly index.
- `manifest.jsonl`: complete line-delimited metadata.

## Category Counts

{summary}

## Source Notes

- Europe PMC REST search: https://www.ebi.ac.uk/europepmc/webservices/rest/search
- PMC OA Web Service: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi
- PMC FTP Service documentation notes that, as of April 13, 2026, legacy OA files are under
  `https://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/`.
- Licenses are article-level values reported by the PMC OA service and are recorded in `manifest.csv`
  and each `metadata.json`.
""",
        encoding="utf-8",
    )


def fetch_europe_pmc(pmcid: str) -> dict:
    query = f"PMCID:{pmcid}"
    results = core.search_europe_pmc(query, page_size=1, max_pages=1)
    return results[0] if results else {}


def main() -> int:
    records = load_existing()
    seen = {record["pmcid"] for record in records}
    next_index = len(records) + 1

    for pmcid, reason, category in TARGETS:
        if pmcid in seen:
            continue
        try:
            result = fetch_europe_pmc(pmcid)
            candidate = {
                "pmcid": pmcid,
                "pmid": result.get("pmid", ""),
                "doi": result.get("doi", ""),
                "title": result.get("title", reason),
                "journal": result.get("journalTitle", ""),
                "pub_year": result.get("pubYear", ""),
                "authors": result.get("authorString", ""),
                "europe_pmc_url": f"https://europepmc.org/article/MED/{result.get('pmid')}" if result.get("pmid") else "",
                "pmc_url": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
                "seed_category": category,
                "seed_query": "targeted web/DOI lookup for property-measurement or prediction paper",
            }
            oa_meta, links = core.parse_oa_links(pmcid)
            if oa_meta.get("error") or oa_meta.get("retracted") == "yes":
                print(f"skip {pmcid}: {oa_meta}")
                continue
            package_link = next((link for link in links if link.get("format") == "tgz"), None)
            if not package_link:
                print(f"skip {pmcid}: no package")
                continue
            article_dir = core.ARTICLES / f"{next_index:03d}_{pmcid}_{core.safe_name(candidate['title'])}"
            article_dir.mkdir(parents=True, exist_ok=True)
            package_path = core.PACKAGES / f"{pmcid}.tar.gz"
            package_bytes = package_path.read_bytes() if package_path.exists() else core.download_package(package_link["href"], package_path)
            if not package_bytes:
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            extracted = core.extract_package(package_bytes, article_dir)
            text = (article_dir / "article_text.txt").read_text(encoding="utf-8", errors="ignore")
            counts = core.signal_counts(text)
            record = {
                **candidate,
                **oa_meta,
                **counts,
                **extracted,
                "category": category,
                "targeted_reason": reason,
                "package": str(package_path.relative_to(core.ROOT)),
                "oa_package_url": core.deprecated_https(package_link["href"]),
            }
            (article_dir / "metadata.json").write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
            records.append(record)
            seen.add(pmcid)
            print(f"appended {next_index:02d}: {pmcid} [{category}] {reason}")
            next_index += 1
            time.sleep(0.25)
        except Exception as exc:
            print(f"failed {pmcid}: {exc}")

    update_outputs(records)
    print(f"manifest total: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

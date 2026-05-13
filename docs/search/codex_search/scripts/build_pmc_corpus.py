#!/usr/bin/env python3
"""Build a small open-access corpus for melting/boiling-point extraction tests."""

from __future__ import annotations

import csv
import io
import json
import os
import re
import shutil
import ssl
import tarfile
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
PACKAGES = ROOT / "packages"
MANIFEST_JSONL = ROOT / "manifest.jsonl"
MANIFEST_CSV = ROOT / "manifest.csv"
README = ROOT / "README.md"

TARGET_TOTAL = 55
MIN_TARGET = 50
MAX_PACKAGE_BYTES = 90_000_000

USER_AGENT = "Codex OA corpus builder for local research-skill tests"
CTX = ssl._create_unverified_context()


SEARCHES = [
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "melting points were determined" AND (synthesis OR synthesized OR derivatives OR compounds)',
    },
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "melting points are uncorrected" AND (synthesis OR synthesized OR compound OR derivatives)',
    },
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND "uncorrected" AND (synthesis OR synthesized OR compound)',
    },
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "experimental section" AND "melting point" AND "NMR" AND synthesized',
    },
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND JOURNAL:"Molecules" AND "melting point" AND synthesis',
    },
    {
        "category": "synthetic_organic",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND JOURNAL:"Beilstein J Org Chem" AND "melting point"',
    },
    {
        "category": "measurement_or_data",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND TITLE:"melting point" AND (measurement OR determination OR prediction OR model OR data)',
    },
    {
        "category": "measurement_or_data",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND TITLE:"boiling point" AND (measurement OR determination OR prediction OR model OR data)',
    },
    {
        "category": "measurement_or_data",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND ("melting point data" OR "boiling point data") AND (organic OR compound OR prediction OR model)',
    },
    {
        "category": "measurement_or_data",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "melting point" AND "boiling point" AND ("organic compound" OR "organic compounds" OR solvent)',
    },
    {
        "category": "boiling_point",
        "query": 'OPEN_ACCESS:y AND SRC:PMC AND "boiling point" AND (distillation OR "vapor pressure" OR "organic compound" OR solvent)',
    },
]


def request_bytes(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as response:
        return response.read()


def request_json(url: str) -> dict:
    return json.loads(request_bytes(url).decode("utf-8"))


def search_europe_pmc(query: str, page_size: int = 25, max_pages: int = 3) -> list[dict]:
    results: list[dict] = []
    cursor = "*"
    for _ in range(max_pages):
        params = {
            "query": query,
            "format": "json",
            "resultType": "core",
            "pageSize": str(page_size),
            "cursorMark": cursor,
        }
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)
        try:
            payload = request_json(url)
        except Exception as exc:
            print(f"search failed: {query[:80]}... {exc}")
            break
        page = payload.get("resultList", {}).get("result", [])
        results.extend(page)
        next_cursor = payload.get("nextCursorMark")
        if not page or not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        time.sleep(0.25)
    return results


def parse_oa_links(pmcid: str) -> tuple[dict, list[dict]]:
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={urllib.parse.quote(pmcid)}"
    xml = request_bytes(url).decode("utf-8", "ignore")
    root = ET.fromstring(xml)
    error = root.find(".//error")
    if error is not None:
        return {"error": error.attrib.get("code", "oa_error")}, []
    records = root.findall(".//record")
    if not records:
        return {"error": "no_oa_record"}, []
    record = records[0]
    meta = {
        "citation": record.attrib.get("citation", ""),
        "license": record.attrib.get("license", ""),
        "retracted": record.attrib.get("retracted", ""),
    }
    links = [dict(link.attrib) for link in record.findall("link")]
    return meta, links


def deprecated_https(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"ftp", "https", "http"}:
        return url
    path = parsed.path
    if path.startswith("/pub/pmc/") and not path.startswith("/pub/pmc/deprecated/"):
        path = path.replace("/pub/pmc/", "/pub/pmc/deprecated/", 1)
    return urllib.parse.urlunparse(("https", "ftp.ncbi.nlm.nih.gov", path, "", "", ""))


def safe_name(value: str, limit: int = 90) -> str:
    value = re.sub(r"[^A-Za-z0-9._ -]+", "", value).strip()
    value = re.sub(r"\s+", "_", value)
    return (value or "article")[:limit]


def strip_xml_text(raw: bytes) -> str:
    try:
        root = ET.fromstring(raw)
        text = " ".join(piece.strip() for piece in root.itertext() if piece and piece.strip())
    except ET.ParseError:
        text = raw.decode("utf-8", "ignore")
    text = unescape(text)
    return re.sub(r"\s+", " ", text)


def signal_counts(text: str) -> dict:
    low = text.lower()
    mp_near_number = re.findall(
        r"(?:melting points?|m\.?\s*p\.?)\D{0,80}\d{2,4}(?:\s*[–-]\s*\d{1,4})?\s*(?:°|degrees?)?\s*c",
        low,
    )
    bp_near_number = re.findall(
        r"(?:boiling points?|b\.?\s*p\.?)\D{0,80}\d{2,4}(?:\s*[–-]\s*\d{1,4})?\s*(?:°|degrees?)?\s*c",
        low,
    )
    return {
        "melting_point_mentions": low.count("melting point") + len(re.findall(r"\bm\.?\s*p\.?\b", low)),
        "boiling_point_mentions": low.count("boiling point") + len(re.findall(r"\bb\.?\s*p\.?\b", low)),
        "mp_numeric_contexts": len(mp_near_number),
        "bp_numeric_contexts": len(bp_near_number),
        "nmr_mentions": low.count("nmr"),
        "experimental_mentions": low.count("experimental"),
    }


def looks_useful(counts: dict) -> bool:
    if counts["mp_numeric_contexts"] or counts["bp_numeric_contexts"]:
        return True
    if counts["melting_point_mentions"] >= 3 and counts["experimental_mentions"] >= 1:
        return True
    if counts["boiling_point_mentions"] >= 2:
        return True
    return False


def classify(seed_category: str, title: str, text: str, counts: dict) -> str:
    low = f"{title} {text[:3000]}".lower()
    if counts["boiling_point_mentions"] or "boiling point" in low:
        if seed_category == "boiling_point" or counts["bp_numeric_contexts"]:
            return "boiling_point"
    model_terms = ("prediction", "model", "dataset", "database", "measurement", "determination", "estimation")
    if seed_category == "measurement_or_data" or any(term in low for term in model_terms):
        return "measurement_or_data"
    if counts["nmr_mentions"] >= 4 or "synthesis" in low or "synthesized" in low:
        return "synthetic_organic"
    return seed_category


def extract_package(package_bytes: bytes, article_dir: Path) -> dict:
    text_parts: list[str] = []
    extracted = {"pdf": "", "xml": "", "supplement_count": 0}
    with tarfile.open(fileobj=io.BytesIO(package_bytes), mode="r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
        for member in members:
            lower = member.name.lower()
            if lower.endswith((".nxml", ".xml")) and not extracted["xml"]:
                raw = tar.extractfile(member).read()
                xml_path = article_dir / "article.nxml"
                xml_path.write_bytes(raw)
                extracted["xml"] = str(xml_path.relative_to(ROOT))
                text_parts.append(strip_xml_text(raw))
            elif lower.endswith(".pdf") and not extracted["pdf"]:
                raw = tar.extractfile(member).read()
                pdf_path = article_dir / "article.pdf"
                pdf_path.write_bytes(raw)
                extracted["pdf"] = str(pdf_path.relative_to(ROOT))
            elif lower.endswith((".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt")):
                extracted["supplement_count"] += 1
    if text_parts:
        text_path = article_dir / "article_text.txt"
        text_path.write_text("\n\n".join(text_parts), encoding="utf-8")
        extracted["text"] = str(text_path.relative_to(ROOT))
    else:
        extracted["text"] = ""
    return extracted


def download_package(url: str, package_path: Path) -> bytes | None:
    url = deprecated_https(url)
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=25) as response:
            length = int(response.headers.get("content-length") or 0)
    except Exception:
        length = 0
    if length > MAX_PACKAGE_BYTES:
        print(f"skip huge package ({length} bytes): {url}")
        return None
    package_bytes = request_bytes(url, timeout=90)
    if len(package_bytes) > MAX_PACKAGE_BYTES:
        print(f"skip huge package after download ({len(package_bytes)} bytes): {url}")
        return None
    package_path.write_bytes(package_bytes)
    return package_bytes


def build_candidates() -> list[dict]:
    seen: set[str] = set()
    candidates: list[dict] = []
    for search in SEARCHES:
        print(f"searching {search['category']}: {search['query'][:90]}")
        for result in search_europe_pmc(search["query"]):
            pmcid = result.get("pmcid") or ""
            if not pmcid or pmcid in seen:
                continue
            seen.add(pmcid)
            candidates.append(
                {
                    "pmcid": pmcid,
                    "pmid": result.get("pmid", ""),
                    "doi": result.get("doi", ""),
                    "title": result.get("title", ""),
                    "journal": result.get("journalTitle", ""),
                    "pub_year": result.get("pubYear", ""),
                    "authors": result.get("authorString", ""),
                    "europe_pmc_url": f"https://europepmc.org/article/MED/{result.get('pmid')}" if result.get("pmid") else "",
                    "pmc_url": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
                    "seed_category": search["category"],
                    "seed_query": search["query"],
                }
            )
        time.sleep(0.4)
    return candidates


def main() -> int:
    ARTICLES.mkdir(parents=True, exist_ok=True)
    PACKAGES.mkdir(parents=True, exist_ok=True)

    accepted: list[dict] = []
    candidates = build_candidates()
    print(f"candidate PMCID count: {len(candidates)}")

    for candidate in candidates:
        if len(accepted) >= TARGET_TOTAL:
            break
        pmcid = candidate["pmcid"]
        try:
            oa_meta, links = parse_oa_links(pmcid)
            if oa_meta.get("error") or oa_meta.get("retracted") == "yes":
                continue
            package_link = next((link for link in links if link.get("format") == "tgz"), None)
            if not package_link:
                continue
            index = len(accepted) + 1
            title_stub = safe_name(candidate["title"])
            article_dir = ARTICLES / f"{index:03d}_{pmcid}_{title_stub}"
            article_dir.mkdir(parents=True, exist_ok=True)
            package_path = PACKAGES / f"{pmcid}.tar.gz"
            if package_path.exists():
                package_bytes = package_path.read_bytes()
            else:
                package_bytes = download_package(package_link["href"], package_path)
            if not package_bytes:
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            extracted = extract_package(package_bytes, article_dir)
            if not extracted.get("text"):
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            text = (article_dir / "article_text.txt").read_text(encoding="utf-8", errors="ignore")
            counts = signal_counts(text)
            if not looks_useful(counts):
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            category = classify(candidate["seed_category"], candidate["title"], text, counts)
            record = {
                **candidate,
                **oa_meta,
                **counts,
                **extracted,
                "category": category,
                "package": str(package_path.relative_to(ROOT)),
                "oa_package_url": deprecated_https(package_link["href"]),
            }
            (article_dir / "metadata.json").write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
            accepted.append(record)
            print(
                f"accepted {len(accepted):02d}: {pmcid} [{category}] "
                f"mp={counts['mp_numeric_contexts']} bp={counts['bp_numeric_contexts']} pdf={'yes' if extracted['pdf'] else 'no'}"
            )
            time.sleep(0.3)
        except (urllib.error.URLError, TimeoutError, tarfile.TarError, ET.ParseError, OSError) as exc:
            print(f"failed {pmcid}: {exc}")
            continue

    MANIFEST_JSONL.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in accepted),
        encoding="utf-8",
    )
    if accepted:
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
        with MANIFEST_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(accepted)

    counts_by_category: dict[str, int] = {}
    for record in accepted:
        counts_by_category[record["category"]] = counts_by_category.get(record["category"], 0) + 1
    summary = "\n".join(f"- {name}: {count}" for name, count in sorted(counts_by_category.items()))
    README.write_text(
        textwrap.dedent(
            f"""\
            # Melting and Boiling Point OA Test Corpus

            Built from Europe PMC search results and the official PMC Open Access Subset package service.
            The corpus contains {len(accepted)} open-access article records selected because their full text
            contains melting-point or boiling-point mentions with numeric context, or repeated property
            mentions in experimental/data sections.

            ## Layout

            - `articles/`: one directory per selected paper, with `article.nxml`, `article_text.txt`,
              `article.pdf` when present in the OA package, and `metadata.json`.
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
            - Licenses are article-level values reported by the PMC OA service and are also recorded in
              `manifest.csv` and each `metadata.json`.
            """
        ),
        encoding="utf-8",
    )

    print(f"accepted total: {len(accepted)}")
    if len(accepted) < MIN_TARGET:
        print(f"WARNING: target not met; wanted at least {MIN_TARGET}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

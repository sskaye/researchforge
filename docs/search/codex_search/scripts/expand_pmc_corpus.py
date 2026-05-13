#!/usr/bin/env python3
"""Find and append more verified PMC OA melting/boiling-point papers."""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pmc_corpus as core  # noqa: E402


TARGET_NEW_VERIFIED = int(os.environ.get("TARGET_NEW_VERIFIED", "110"))
MAX_CANDIDATES_TO_TRY = 450
REQUIRE_PDF = os.environ.get("REQUIRE_PDF", "0") == "1"
REMOVE_PACKAGES_AFTER_EXTRACTION = os.environ.get("REMOVE_PACKAGES_AFTER_EXTRACTION", "0") == "1"
DISCARD_REJECT_ARTIFACTS = os.environ.get("DISCARD_REJECT_ARTIFACTS", "0") == "1"


EXPANSION_SEARCHES = [
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND "1H NMR" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND "13C NMR" AND synthesized'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "mp:" AND "1H NMR" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "mp " AND "1 H NMR" AND "yield" AND "solid"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "Melting Point:" AND "NMR"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "M.p." AND "IR" AND "NMR"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "M.P" AND "IR" AND "NMR" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p. (°C)" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p.°C" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "mp °C" AND synthesis'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND JOURNAL:"Molecules"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND JOURNAL:"Beilstein J Org Chem"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND JOURNAL:"Marine Drugs"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "m.p." AND JOURNAL:"International Journal of Molecular Sciences"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "melting point" AND "experimental" AND "1H NMR"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "melting points were determined" AND "1H NMR"'),
    ("synthetic_organic", 'OPEN_ACCESS:y AND SRC:PMC AND "melting points are uncorrected" AND "NMR"'),
    ("boiling_point", 'OPEN_ACCESS:y AND SRC:PMC AND "boiling point" AND "°C" AND "organic"'),
    ("boiling_point", 'OPEN_ACCESS:y AND SRC:PMC AND "normal boiling point" AND "K" AND "dataset"'),
    ("boiling_point", 'OPEN_ACCESS:y AND SRC:PMC AND "B.p." AND "°C" AND "NMR"'),
    ("measurement_or_data", 'OPEN_ACCESS:y AND SRC:PMC AND "melting point" AND "dataset" AND "°C"'),
    ("measurement_or_data", 'OPEN_ACCESS:y AND SRC:PMC AND "melting point prediction"'),
    ("measurement_or_data", 'OPEN_ACCESS:y AND SRC:PMC AND "melting point data" AND "compound"'),
    ("measurement_or_data", 'OPEN_ACCESS:y AND SRC:PMC AND "boiling point prediction"'),
]


DIRECT_NUMERIC_PATTERNS = [
    re.compile(
        r"(?is)(?:\bm\.?\s*p\.?\b|melting points?|melting temp(?:erature)?s?)\s*[:=]?\s*"
        r"(?:>|<|ca\.?\s*)?\d{2,4}(?:\.\d+)?(?:\s*[–-]\s*\d{1,4}(?:\.\d+)?)?\s*"
        r"(?:°\s*C|℃|o\s*C|degrees?\s*C|K\b|°C|C\b)"
    ),
    re.compile(
        r"(?is)(?:\bb\.?\s*p\.?\b|boiling points?|normal boiling point|NBP)\s*[:=]?\s*"
        r"(?:>|<|ca\.?\s*)?\d{2,4}(?:\.\d+)?(?:\s*[–-]\s*\d{1,4}(?:\.\d+)?)?\s*"
        r"(?:°\s*C|℃|o\s*C|degrees?\s*C|K\b|°C|C\b)"
    ),
]

TABLE_PATTERNS = [
    re.compile(
        r"(?is)(?:\bm\.?\s*p\.?\b|melting point|T\s*m|T_m|mp)\s*"
        r"(?:\([^)]*(?:°|o\s*)?C[^)]*\)|\[[^\]]*K[^\]]*\]|°\s*C|o\s*C|K\b).{0,900}"
        r"\b\d{2,4}(?:\.\d+)?(?:\s*[–-]\s*\d{1,4}(?:\.\d+)?)?\b"
    ),
    re.compile(
        r"(?is)(?:boiling point|normal boiling point|NBP|B\.p\.|Bp)\s*"
        r"(?:\([^)]*(?:°|o\s*)?C[^)]*\)|\[[^\]]*K[^\]]*\]|°\s*C|o\s*C|K\b).{0,900}"
        r"\b\d{2,4}(?:\.\d+)?(?:\s*[–-]\s*\d{1,4}(?:\.\d+)?)?\b"
    ),
]


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def next_article_index() -> int:
    indices = []
    for article_dir in core.ARTICLES.glob("*_PMC*"):
        match = re.match(r"(\d+)_PMC", article_dir.name)
        if match:
            indices.append(int(match.group(1)))
    return max(indices or [0]) + 1


def seen_pmcids() -> set[str]:
    seen = {record["pmcid"] for record in load_records(core.MANIFEST_JSONL)}
    review_manifest = core.ROOT / "review_no_mp_bp_data" / "manifest.jsonl"
    seen.update(record["pmcid"] for record in load_records(review_manifest))
    seen.update(path.name.split("_")[1] for path in core.ARTICLES.glob("*_PMC*") if len(path.name.split("_")) > 1)
    review_articles = core.ROOT / "review_no_mp_bp_data" / "articles"
    if review_articles.exists():
        seen.update(path.name.split("_")[1] for path in review_articles.glob("*_PMC*") if len(path.name.split("_")) > 1)
    expansion_report = core.ROOT / "expansion_2026-05-09_report.csv"
    if expansion_report.exists():
        with expansion_report.open(newline="", encoding="utf-8") as handle:
            seen.update(row["pmcid"] for row in csv.DictReader(handle) if row.get("pmcid"))
    return seen


def evidence(text: str) -> tuple[bool, str, str]:
    candidates: list[tuple[int, str, str]] = []
    for pattern in DIRECT_NUMERIC_PATTERNS:
        for match in pattern.finditer(text):
            snippet = " ".join(text[max(0, match.start() - 180) : match.end() + 320].split())
            kind = "boiling_point" if re.search(r"(?i)boiling|NBP|\bb\.?\s*p", match.group(0)) else "melting_point"
            candidates.append((4, kind, snippet[:700]))
    for pattern in TABLE_PATTERNS:
        for match in pattern.finditer(text):
            snippet = " ".join(text[max(0, match.start() - 160) : match.end() + 320].split())
            kind = "boiling_point" if re.search(r"(?i)boiling|NBP|B\.p|Bp", match.group(0)) else "melting_point"
            candidates.append((3, kind, snippet[:700]))

    if candidates:
        candidates.sort(reverse=True)
        _, kind, snippet = candidates[0]
        return True, kind, snippet
    return False, "", ""


def category_for(seed_category: str, detected_kind: str, text: str, title: str) -> str:
    low = f"{title} {text[:4000]}".lower()
    if detected_kind == "boiling_point":
        return "boiling_point"
    if seed_category == "measurement_or_data":
        return "measurement_or_data"
    if any(term in low for term in ["prediction", "dataset", "database", "qspr", "group contribution", "machine learning"]):
        if "synthesis" not in low[:1500]:
            return "measurement_or_data"
    return "synthetic_organic"


def build_candidates(skip: set[str]) -> list[dict]:
    candidates: list[dict] = []
    added: set[str] = set()
    for seed_category, query in EXPANSION_SEARCHES:
        print(f"searching {seed_category}: {query[:95]}", flush=True)
        for result in core.search_europe_pmc(query, page_size=50, max_pages=5):
            pmcid = result.get("pmcid") or ""
            if not pmcid or pmcid in skip or pmcid in added:
                continue
            added.add(pmcid)
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
                    "seed_category": seed_category,
                    "seed_query": query,
                }
            )
        if len(candidates) >= MAX_CANDIDATES_TO_TRY:
            break
        time.sleep(0.3)
    return candidates


def write_manifests(records: list[dict]) -> None:
    core.MANIFEST_JSONL.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in records), encoding="utf-8")
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
        "manual_verification_has_mp_bp_data",
        "manual_verification_evidence",
        "manual_verification_action",
        "expansion_batch",
    ]
    with core.MANIFEST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def update_readme(records: list[dict], new_count: int, rejected_count: int) -> None:
    counts = Counter(record["category"] for record in records)
    readme = core.README.read_text(encoding="utf-8")
    if "## Category Counts" in readme and "## Source Notes" in readme:
        start = readme.index("## Category Counts")
        end = readme.index("## Source Notes")
        block = "## Category Counts\n\n" + "\n".join(f"- {k}: {counts[k]}" for k in sorted(counts)) + "\n\n"
        block += (
            "## Latest Expansion\n\n"
            f"- Added verified papers in latest expansion: {new_count}\n"
            f"- Rejected/moved during latest expansion: {rejected_count}\n"
            f"- Current verified corpus size: {len(records)}\n\n"
        )
        readme = readme[:start] + block + readme[end:]
    core.README.write_text(readme, encoding="utf-8")


def main() -> int:
    core.ARTICLES.mkdir(parents=True, exist_ok=True)
    core.PACKAGES.mkdir(parents=True, exist_ok=True)
    review_root = core.ROOT / "review_no_mp_bp_data"
    rejected_articles = review_root / "articles_expansion_rejected"
    rejected_packages = review_root / "packages_expansion_rejected"
    rejected_articles.mkdir(parents=True, exist_ok=True)
    rejected_packages.mkdir(parents=True, exist_ok=True)

    existing = load_records(core.MANIFEST_JSONL)
    skip = seen_pmcids()
    candidates = build_candidates(skip)
    print(f"candidate count after dedupe: {len(candidates)}", flush=True)

    next_index = next_article_index()
    accepted: list[dict] = []
    rejected: list[dict] = []

    for candidate in candidates:
        if len(accepted) >= TARGET_NEW_VERIFIED:
            break
        pmcid = candidate["pmcid"]
        try:
            oa_meta, links = core.parse_oa_links(pmcid)
            if oa_meta.get("error") or oa_meta.get("retracted") == "yes":
                continue
            package_link = next((link for link in links if link.get("format") == "tgz"), None)
            if not package_link:
                continue
            title_stub = core.safe_name(candidate["title"])
            article_dir = core.ARTICLES / f"{next_index:03d}_{pmcid}_{title_stub}"
            article_dir.mkdir(parents=True, exist_ok=True)
            package_path = core.PACKAGES / f"{pmcid}.tar.gz"
            package_bytes = package_path.read_bytes() if package_path.exists() else core.download_package(package_link["href"], package_path)
            if not package_bytes:
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            extracted = core.extract_package(package_bytes, article_dir)
            text_path = article_dir / "article_text.txt"
            if not text_path.exists():
                shutil.rmtree(article_dir, ignore_errors=True)
                continue
            if REQUIRE_PDF and not extracted.get("pdf"):
                shutil.rmtree(article_dir, ignore_errors=True)
                if REMOVE_PACKAGES_AFTER_EXTRACTION and package_path.exists():
                    package_path.unlink()
                continue
            text = text_path.read_text(encoding="utf-8", errors="ignore")
            has_data, detected_kind, snippet = evidence(text)
            counts = core.signal_counts(text)
            base_record = {
                **candidate,
                **oa_meta,
                **counts,
                **extracted,
                "package": str(package_path.relative_to(core.ROOT)),
                "oa_package_url": core.deprecated_https(package_link["href"]),
                "expansion_batch": "2026-05-09-expand-100-plus",
            }
            if not has_data:
                base_record.update(
                    {
                        "category": candidate["seed_category"],
                        "manual_verification_has_mp_bp_data": False,
                        "manual_verification_evidence": "Expansion filter found no direct numeric MP/BP evidence in extracted article text.",
                        "manual_verification_action": "moved_to_review_no_mp_bp_data_expansion_rejected",
                    }
                )
                dest_dir = rejected_articles / article_dir.name
                if DISCARD_REJECT_ARTIFACTS:
                    shutil.rmtree(article_dir, ignore_errors=True)
                else:
                    if dest_dir.exists():
                        shutil.rmtree(dest_dir)
                    shutil.move(str(article_dir), str(dest_dir))
                if package_path.exists():
                    if DISCARD_REJECT_ARTIFACTS or REMOVE_PACKAGES_AFTER_EXTRACTION:
                        package_path.unlink()
                    else:
                        dest_pkg = rejected_packages / package_path.name
                        if dest_pkg.exists():
                            dest_pkg.unlink()
                        shutil.move(str(package_path), str(dest_pkg))
                rejected.append(base_record)
                print(f"rejected {pmcid}: no numeric evidence", flush=True)
                continue
            category = category_for(candidate["seed_category"], detected_kind, text, candidate["title"])
            base_record.update(
                {
                    "category": category,
                    "manual_verification_has_mp_bp_data": True,
                    "manual_verification_evidence": snippet,
                    "manual_verification_action": "kept_after_expansion_numeric_evidence_check",
                }
            )
            (article_dir / "metadata.json").write_text(json.dumps(base_record, indent=2, sort_keys=True), encoding="utf-8")
            if REMOVE_PACKAGES_AFTER_EXTRACTION and package_path.exists():
                package_path.unlink()
                base_record["package"] = "removed_after_extraction_to_save_space"
                (article_dir / "metadata.json").write_text(json.dumps(base_record, indent=2, sort_keys=True), encoding="utf-8")
            accepted.append(base_record)
            print(f"accepted new {len(accepted):03d}: {pmcid} [{category}] {detected_kind}", flush=True)
            next_index += 1
            time.sleep(0.2)
        except Exception as exc:
            print(f"failed {pmcid}: {exc}", flush=True)
            continue

    all_records = existing + accepted
    write_manifests(all_records)

    expansion_report = core.ROOT / "expansion_2026-05-09_report.csv"
    report_fields = ["pmcid", "category", "title", "doi", "pmc_url", "manual_verification_evidence", "manual_verification_action"]
    with expansion_report.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=report_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(accepted + rejected)
    (core.ROOT / "expansion_2026-05-09_summary.json").write_text(
        json.dumps(
            {
                "new_verified": len(accepted),
                "rejected": len(rejected),
                "target_new_verified": TARGET_NEW_VERIFIED,
                "total_verified_corpus_size": len(all_records),
                "category_counts": dict(Counter(r["category"] for r in all_records)),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    update_readme(all_records, len(accepted), len(rejected))
    print(
        json.dumps(
            {
                "new_verified": len(accepted),
                "rejected": len(rejected),
                "total_verified_corpus_size": len(all_records),
            },
            indent=2,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if len(accepted) >= 100 else 2


if __name__ == "__main__":
    raise SystemExit(main())

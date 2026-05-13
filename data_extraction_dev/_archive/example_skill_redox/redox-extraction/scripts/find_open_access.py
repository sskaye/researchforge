#!/usr/bin/env python3
"""
find_open_access.py — given a DOI, find an open-access source.

Tries multiple discovery APIs in order of reliability:
  1. Unpaywall (best dedicated OA tracker; needs an email parameter)
  2. OpenAlex (newer comprehensive index with OA links)
  3. Semantic Scholar (often has PDF URLs)
  4. Europe PMC (for PubMed-indexed papers)
  5. CORE (repository aggregator)
  6. Wayback Machine snapshots of the publisher page (last resort)

Output URLs are returned in priority order (highest-confidence first). When picking
a URL to fetch, prefer in this order:
  1. Unpaywall best PDF
  2. OpenAlex / Semantic Scholar PDF
  3. Europe PMC / PMC URL
  4. CORE
  5. Wayback Machine snapshot

Usage:
    python find_open_access.py <DOI> [--email you@example.com]
    python find_open_access.py 10.1038/srep39101

Returns a JSON object with discovered URLs:
    {"doi": "...", "candidates": [{"url": "...", "source": "Unpaywall (best PDF)"}, ...]}

Exit code 0 on success (at least one URL found), 1 on no results.
"""
import sys
import json
import urllib.request
import urllib.parse
import argparse


def _fetch_json(url, timeout=8):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "redox-extraction/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def unpaywall(doi, email):
    if not email:
        return []
    q = urllib.parse.quote(doi)
    data = _fetch_json(f"https://api.unpaywall.org/v2/{q}?email={email}")
    if not data:
        return []
    out = []
    best = data.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        out.append({"url": best["url_for_pdf"], "source": "Unpaywall (best PDF)"})
    if best.get("url"):
        out.append({"url": best["url"], "source": "Unpaywall (best landing)"})
    for loc in data.get("oa_locations", []) or []:
        if loc.get("url_for_pdf"):
            out.append({"url": loc["url_for_pdf"], "source": f"Unpaywall ({loc.get('host_type','?')} PDF)"})
    return out


def openalex(doi):
    q = urllib.parse.quote(doi)
    data = _fetch_json(f"https://api.openalex.org/works/doi:{q}")
    if not data:
        return []
    out = []
    oa = data.get("open_access") or {}
    if oa.get("oa_url"):
        out.append({"url": oa["oa_url"], "source": "OpenAlex"})
    primary = data.get("primary_location") or {}
    if primary.get("pdf_url"):
        out.append({"url": primary["pdf_url"], "source": "OpenAlex primary"})
    for loc in data.get("locations", []) or []:
        if loc.get("pdf_url"):
            out.append({"url": loc["pdf_url"], "source": f"OpenAlex ({loc.get('source',{}).get('display_name','?')})"})
    return out


def semantic_scholar(doi):
    q = urllib.parse.quote(doi)
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{q}?fields=openAccessPdf,externalIds,title"
    data = _fetch_json(url)
    if not data:
        return []
    out = []
    pdf = data.get("openAccessPdf") or {}
    if pdf.get("url"):
        out.append({"url": pdf["url"], "source": "Semantic Scholar"})
    return out


def europe_pmc(doi):
    q = urllib.parse.quote(f'DOI:"{doi}"')
    data = _fetch_json(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json&resultType=core")
    if not data:
        return []
    out = []
    results = (data.get("resultList") or {}).get("result") or []
    for r in results:
        if r.get("pmcid"):
            out.append({
                "url": f"https://europepmc.org/article/PMC/{r['pmcid'].replace('PMC','')}",
                "source": "Europe PMC",
            })
        for fu in (r.get("fullTextUrlList") or {}).get("fullTextUrl", []) or []:
            if fu.get("documentStyle") == "pdf":
                out.append({"url": fu["url"], "source": f"Europe PMC ({fu.get('site','?')} PDF)"})
    return out


def core_api(doi):
    """CORE is a repository aggregator; works on title or DOI."""
    q = urllib.parse.quote(f'doi:"{doi}"')
    data = _fetch_json(f"https://api.core.ac.uk/v3/search/works?q={q}&limit=3")
    if not data:
        return []
    out = []
    for r in data.get("results", []) or []:
        if r.get("downloadUrl"):
            out.append({"url": r["downloadUrl"], "source": "CORE"})
    return out


def wayback(doi):
    """Last resort: check Wayback Machine for the DOI URL."""
    target = f"https://doi.org/{doi}"
    q = urllib.parse.quote(target)
    data = _fetch_json(f"https://archive.org/wayback/available?url={q}")
    if not data:
        return []
    snap = (data.get("archived_snapshots") or {}).get("closest")
    if snap and snap.get("url"):
        return [{"url": snap["url"], "source": "Wayback Machine"}]
    return []


def find_open_access(doi, email=None):
    """Run all discovery APIs and return ordered results."""
    candidates = []
    seen = set()
    for fn, args in [
        (unpaywall, (doi, email)),
        (openalex, (doi,)),
        (semantic_scholar, (doi,)),
        (europe_pmc, (doi,)),
        (core_api, (doi,)),
        (wayback, (doi,)),
    ]:
        try:
            for c in fn(*args):
                if c["url"] in seen:
                    continue
                seen.add(c["url"])
                candidates.append(c)
        except Exception as e:
            candidates.append({"url": None, "source": f"{fn.__name__} error: {e}"})
    return candidates


def main():
    ap = argparse.ArgumentParser(description="Find open-access sources for a DOI.")
    ap.add_argument("doi", help="DOI (e.g., 10.1038/srep39101)")
    ap.add_argument("--email", default="", help="Email for Unpaywall (recommended; falls back if absent)")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    candidates = find_open_access(args.doi, email=args.email)
    if args.json:
        print(json.dumps({"doi": args.doi, "candidates": candidates}, indent=2))
    else:
        print(f"DOI: {args.doi}")
        print(f"Found {len([c for c in candidates if c.get('url')])} candidate URL(s):")
        for c in candidates:
            if c.get("url"):
                print(f"  [{c['source']}]")
                print(f"    {c['url']}")
            else:
                print(f"  ({c['source']})")
    sys.exit(0 if any(c.get("url") for c in candidates) else 1)


if __name__ == "__main__":
    main()

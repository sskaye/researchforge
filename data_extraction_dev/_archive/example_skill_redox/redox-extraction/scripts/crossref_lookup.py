#!/usr/bin/env python3
"""
crossref_lookup.py — get authoritative metadata for a DOI from CrossRef.

CrossRef is the canonical source for paper metadata (title, journal, year, volume, page).
Use it to:
  - Verify a citation's metadata matches the paper at a given DOI.
  - Catch citation errors (e.g., wrong year, wrong volume, paper unrelated to the molecule).

Usage:
    python crossref_lookup.py <DOI>
    python crossref_lookup.py 10.1038/srep39101

Output (JSON):
    {
      "doi": "...",
      "title": "...",
      "journal": "...",
      "year": ...,
      "volume": "...",
      "page": "...",
      "publisher": "..."
    }

Exit code 0 if metadata retrieved, 1 if DOI unresolvable.
"""
import sys
import json
import urllib.request
import urllib.parse
import argparse


class CrossRefUnavailable(Exception):
    """Raised when CrossRef itself is unreachable (vs DOI not found)."""


def crossref(doi):
    """Look up DOI metadata. Returns dict on success, None if DOI not found.

    If CrossRef is unreachable (network error / 5xx), returns None and prints a
    warning to stderr — the caller should treat this as 'unable to verify' rather
    than 'DOI is bad'. Use crossref_strict() if you want an exception instead.
    """
    q = urllib.parse.quote(doi)
    url = f"https://api.crossref.org/works/{q}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "redox-extraction/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # DOI doesn't exist
        print(f"WARNING: CrossRef returned {e.code} for {doi} — treating as unverifiable", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARNING: CrossRef unreachable ({e}) — DOI {doi} unverified", file=sys.stderr)
        return None

    msg = data.get("message", {})
    title = (msg.get("title") or [None])[0]
    container = (msg.get("container-title") or [None])[0]
    issued = msg.get("issued", {}).get("date-parts", [[None]])[0]
    year = issued[0] if issued else None
    return {
        "doi": doi,
        "title": title,
        "journal": container,
        "year": year,
        "volume": msg.get("volume"),
        "issue": msg.get("issue"),
        "page": msg.get("page"),
        "publisher": msg.get("publisher"),
    }


def title_keyword_check(title, keywords):
    """Return True if the title contains any of the given keywords (case-insensitive)."""
    if not title:
        return False
    lo = title.lower()
    return any(kw.lower() in lo for kw in keywords)


def main():
    ap = argparse.ArgumentParser(description="Look up paper metadata from CrossRef DOI.")
    ap.add_argument("doi")
    ap.add_argument("--require-keywords", nargs="+", default=[],
                    help="Exit 2 if title does not contain any of these keywords (case-insensitive).")
    args = ap.parse_args()

    md = crossref(args.doi)
    if md is None:
        print(json.dumps({"doi": args.doi, "error": "DOI unresolvable on CrossRef"}, indent=2))
        sys.exit(1)

    print(json.dumps(md, indent=2))

    if args.require_keywords:
        if not title_keyword_check(md["title"], args.require_keywords):
            print(f"\nWARNING: title does not contain any of {args.require_keywords}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
crossref_lookup.py — get authoritative metadata for a DOI from CrossRef.

Used to verify that a DOI extracted from a paper file actually resolves and
matches the paper at hand. CrossRef is the canonical source for paper
metadata (title, journal, year, volume).

Usage:
    python3 crossref_lookup.py <DOI>
    python3 crossref_lookup.py 10.3390/molecules23051212

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

Exit code:
    0 — metadata retrieved
    1 — DOI unresolvable
    2 — DOI resolvable but title-mismatch (when --require-keywords is used)
"""
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import argparse


def crossref(doi: str, timeout: int = 8) -> dict | None:
    """Look up DOI metadata. Returns dict on success, None if DOI not found
    or CrossRef is unreachable. Network errors are non-fatal (caller treats
    as 'unable to verify' rather than 'DOI is bad')."""
    q = urllib.parse.quote(doi)
    url = f"https://api.crossref.org/works/{q}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "mp-bp-extraction/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"WARNING: CrossRef returned {e.code} for {doi} — "
              "treating as unverifiable", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARNING: CrossRef unreachable ({e}) — "
              f"DOI {doi} unverified", file=sys.stderr)
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


def title_keyword_check(title: str | None, keywords: list[str]) -> bool:
    """True if title contains any of the given keywords (case-insensitive)."""
    if not title or not keywords:
        return False
    lo = title.lower()
    return any(kw.lower() in lo for kw in keywords)


def title_match_score(title: str | None, paper_title: str | None) -> float:
    """Rough word-overlap score between a CrossRef title and a paper-file
    title; useful when checking whether the DOI matches the paper at hand.
    Returns 0..1 (1 = identical word set ignoring stopwords)."""
    if not title or not paper_title:
        return 0.0
    STOP = {"a", "an", "the", "of", "and", "or", "for", "to", "in", "on",
            "by", "with", "from", "as", "at"}
    def tokens(s: str) -> set[str]:
        import re
        return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}
    t1, t2 = tokens(title), tokens(paper_title)
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / max(len(t1), len(t2))


def main():
    ap = argparse.ArgumentParser(
        description="Look up paper metadata from CrossRef DOI.")
    ap.add_argument("doi", help="DOI to look up (e.g., 10.3390/molecules23051212)")
    ap.add_argument("--require-keywords", nargs="+", default=[],
                    help="Exit 2 if title does not contain any of these "
                         "keywords (case-insensitive).")
    ap.add_argument("--paper-title",
                    help="Compare CrossRef title against this paper-file title; "
                         "warn if word-overlap is below --min-match.")
    ap.add_argument("--min-match", type=float, default=0.4,
                    help="Minimum word-overlap fraction with --paper-title.")
    args = ap.parse_args()

    md = crossref(args.doi)
    if md is None:
        print(json.dumps({"doi": args.doi,
                          "error": "DOI unresolvable on CrossRef"}, indent=2))
        sys.exit(1)

    print(json.dumps(md, indent=2))

    if args.require_keywords:
        if not title_keyword_check(md["title"], args.require_keywords):
            print(f"\nWARNING: title does not contain any of "
                  f"{args.require_keywords}", file=sys.stderr)
            sys.exit(2)

    if args.paper_title:
        score = title_match_score(md["title"], args.paper_title)
        if score < args.min_match:
            print(f"\nWARNING: CrossRef title overlap {score:.2f} < "
                  f"{args.min_match}; DOI may not match the paper file",
                  file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()

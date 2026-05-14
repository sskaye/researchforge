#!/usr/bin/env python3
"""Helper: search a paper file for substrings and return small context windows."""
import sys, os, unicodedata, re, json

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    # normalize whitespace + various dashes
    s = s.replace("‐", "-").replace("‑", "-").replace("‒", "-")
    s = s.replace("–", "-").replace("—", "-").replace("―", "-")
    s = s.replace("−", "-")
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    return s

def find(text_norm, needle_norm, ctx=80):
    if not needle_norm: return None
    idx = text_norm.find(needle_norm)
    if idx < 0: return None
    s = max(0, idx-ctx); e = min(len(text_norm), idx+len(needle_norm)+ctx)
    return text_norm[s:e]

def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    text = norm(raw)
    # take search list from stdin lines
    queries = []
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line: continue
        queries.append(line)
    out = []
    for q in queries:
        qn = norm(q)
        ctx = find(text, qn, 100)
        out.append({"q": q[:80], "found": ctx is not None, "ctx": ctx})
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bulk verify a batch CSV against paper sources. Produces minimal report for each row."""
import csv, json, sys, os, unicodedata, re

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‐", "-").replace("‑", "-").replace("‒", "-")
    s = s.replace("–", "-").replace("—", "-").replace("―", "-")
    s = s.replace("−", "-").replace("‒", "-")
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

URL_MAP = {}
with open("Trial3-full-opus47/url_to_folder_built.json", "r") as f:
    URL_MAP = json.load(f)

def folder_for(url):
    return URL_MAP.get(url)

def doi_or_pmc(url):
    if url.startswith("pmc:"):
        return url[4:]
    m = re.search(r"10\.\d{4,9}/[^\s]+", url)
    if m: return m.group(0)
    return url

def main(csvpath):
    rows = list(csv.DictReader(open(csvpath)))
    results = []
    for r in rows:
        rid = r["id"]
        url = r["source_url"]
        folder = folder_for(url)
        compound = r["compound_name"]
        value_raw = r["value_raw"]
        evidence = r["evidence_quote"]
        out = {"row_id": rid, "url": url, "folder": folder,
               "compound": compound, "value_raw": value_raw,
               "evidence_first120": evidence[:120],
               "doi_id": doi_or_pmc(url)}
        if not folder:
            out["error"] = "no_folder"
            results.append(out); continue
        text_path = os.path.join(folder, "article_text.txt")
        if not os.path.exists(text_path):
            out["error"] = "no_text"; results.append(out); continue
        with open(text_path, "r", encoding="utf-8", errors="replace") as f:
            text = norm(f.read())
        # DOI/PMC check
        out["doi_in_text"] = norm(out["doi_id"]) in text
        # evidence quote check (full + several substrings)
        ev = norm(evidence)
        # explicit checks: full quote, value_raw, "..." or "…", doubled tokens
        out["has_ellipsis"] = "..." in evidence or "…" in evidence
        out["full_evidence_found"] = ev in text
        # value_raw check
        v = norm(value_raw)
        out["value_in_text"] = v in text
        out["value_in_evidence"] = v in ev
        # compound shape: check what context around the located evidence
        # ctx
        idx = text.find(ev) if out["full_evidence_found"] else -1
        out["ev_idx"] = idx
        if idx >= 0:
            out["ctx"] = text[max(0, idx-30): idx+len(ev)+60]
        else:
            # try first 100 chars
            head = norm(evidence[:100])
            idx2 = text.find(head)
            out["partial_head_found"] = idx2 >= 0
            if idx2 >= 0:
                out["head_ctx"] = text[max(0, idx2-30): idx2+len(head)+60]
            # try last 100 chars
            tail = norm(evidence[-100:])
            idx3 = text.find(tail)
            out["partial_tail_found"] = idx3 >= 0
        results.append(out)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])

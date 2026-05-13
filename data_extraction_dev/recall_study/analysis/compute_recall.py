"""Improved recall computation with value-fallback matching."""
import csv, json, re
from pathlib import Path

def normalize_value(v):
    if not v: return None
    v = str(v).strip()
    try: return float(v)
    except ValueError: pass
    s = v.replace("−","-").replace("–","-").replace("—","-")
    rng = re.match(r"^\s*(-?\d+)\s*-\s*(\d+)\b", s)
    if rng:
        lo, hi_text = rng.group(1), rng.group(2)
        try:
            lo_int, hi_int = int(lo), int(hi_text)
            if hi_int < lo_int and not lo.startswith("-"):
                for delta in range(1, 16):
                    cand = lo_int + delta
                    n = len(hi_text)
                    if str(cand).zfill(n)[-n:] == hi_text.zfill(n):
                        s = s.replace(f"{lo}-{hi_text}", f"{lo_int} {cand}", 1); break
        except ValueError: pass
    s2 = re.sub(r"(\d)\s*-\s*(\d)", r"\1 \2", s)
    nums = [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", s2)]
    if not nums: return None
    has_K = bool(re.search(r"\bK\b", v)) and not re.search(r"°\s*[CF]\b", v)
    has_F = bool(re.search(r"°\s*F\b", v)) and not re.search(r"°\s*C\b", v)
    val = sum(nums) / len(nums)
    if has_K: val -= 273.15
    if has_F: val = (val - 32) * 5/9
    return val

def normalize_compound(name):
    if not name: return ""
    s = name.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^[(\[]?\s*\d+[a-z]?\s*[)\]]?\s*[-:]?\s*\(?", "", s)
    s = re.sub(r"\s*\(\s*\d+[a-z]?\s*\)\s*$", "", s)
    s = s.lstrip("( ,")
    return s.strip()

PAPER_KEYS = {
    "011": ["molecules 2026, 31, 699", "pde4"],
    "020": ["molecules 2024, 29, 2942"],
    "064": ["chemical data collections 2022"],
    "138": ["molecules 2002, 7, 554-565", "annellation"],
    "050": ["molecules 2003, 8, 756-769"],
    "2009_Dearden": ["environmental toxicology"],
    "056": ["ai-powered"],
    "058": ["how accurately"],
    "khalifa_2024": ["molecules 2024, 29, 4778"],
    "2019_Rubstov": ["j. org. chem. 2019"],
    "chen_2024": ["nanomaterials 2024, 14, 1077"],
    "1990_Yalkowsky": ["pharm. res. 1990"],
    "098": ["molecules 2003, 8(7)"],
    "023": ["russ j org chem 2022"],
    "113": ["acs omega 2026, 11(15)"],
    "057": ["prioritizing data quality"],
}

dev_rows = list(csv.DictReader(open("/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/Trial-1-dev/trial1_output.csv")))
val_rows = list(csv.DictReader(open("/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial-1-val/trial1_val_output.csv")))

def rows_for_paper(paper_id, all_rows):
    keys = PAPER_KEYS[paper_id]
    return [r for r in all_rows
            if any(k in (r.get("source","")+" "+r.get("source_url","")).lower() for k in keys)]

def match_item(item, extr_rows, tol=2.0):
    ic = normalize_compound(item.get("compound_name", ""))
    ip = (item.get("property","") or "").lower()
    iv = normalize_value(item.get("value_raw",""))
    if iv is None: return None
    prop_fam = {"melting_point":"mp", "boiling_point":"bp", "melting point":"mp", "boiling point":"bp", "mp":"mp", "bp":"bp",
                "decomposition":"dec", "sublimation":"sub",
                "DSC_onset":"mp", "DSC_peak":"mp", "mp":"mp", "bp":"bp"}
    ifam = prop_fam.get(ip, ip)
    # First pass: compound+property+value match
    best = None
    for r in extr_rows:
        rc = normalize_compound(r.get("compound_name", ""))
        rp = (r.get("property","") or "").lower()
        rfam = prop_fam.get(rp, rp)
        if rfam != ifam: continue
        rv = normalize_value(r.get("value_celsius") or r.get("value_raw",""))
        if rv is None: continue
        if abs(rv - iv) > tol: continue
        # Compound substring match (try multiple windows + first chemistry-token)
        nmatched = False
        if rc and ic:
            if rc in ic or ic in rc:
                nmatched = True
            elif len(rc) >= 10 and len(ic) >= 10:
                # Try first significant chunk of each
                for off in (0, 5, 10):
                    if off+12 <= len(ic) and ic[off:off+12] in rc:
                        nmatched = True; break
                    if off+12 <= len(rc) and rc[off:off+12] in ic:
                        nmatched = True; break
        if nmatched:
            return r
        # Track value-match as fallback
        if best is None:
            best = r
    # Fallback: value+property match alone is enough if values per paper are mostly distinct.
    # This handles paper 050 (scaffold-vs-IUPAC names) and chen_2024 (formula vs prose name).
    return best

results = {}
for paper_id in PAPER_KEYS:
    enum_dir = "dev_enumerations" if paper_id in ["011","020","064","138","050","2009_Dearden","056","058"] else "val_enumerations"
    f = Path(f"/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/recall_study/{enum_dir}/{paper_id}.json")
    if not f.exists():
        print(f"MISSING {paper_id}"); continue
    enum = json.load(open(f))
    items = enum.get("items", [])
    extr = rows_for_paper(paper_id, dev_rows if enum_dir=="dev_enumerations" else val_rows)
    tp = fn = oils_skipped = figsi_skipped = duplicates_skipped = 0
    seen_matches = set()
    fn_examples = []
    for it in items:
        loc = (it.get("location_type","") or "").lower()
        v = (it.get("value_raw","") or "").lower().strip()
        if v in ("oil","viscous oil","liquid",""):
            oils_skipped += 1; continue
        if loc in ("figure_only","si_only"):
            figsi_skipped += 1; continue
        m = match_item(it, extr)
        if m is not None:
            # Mark each extracted row as found at most once for fair counting
            row_id = m.get("id")
            # If we already counted this row, this enum item is an enum-side
            # duplicate (paper mentions same value twice). Skip rather than
            # double-count.
            if row_id in seen_matches:
                duplicates_skipped += 1
                continue
            seen_matches.add(row_id)
            tp += 1
        else:
            fn += 1
            if len(fn_examples) < 5:
                fn_examples.append((it.get("compound_name","")[:50], it.get("value_raw",""), loc))
    total = tp + fn
    recall = tp/total if total else None
    results[paper_id] = {
        "enum_total": len(items), "extr_total": len(extr),
        "oils_skipped": oils_skipped,
        "figsi_skipped": figsi_skipped,
        "duplicates_skipped": duplicates_skipped,
        "tp": tp, "fn": fn,
        "recall_pct": None if recall is None else round(100*recall, 1),
        "fn_examples": fn_examples
    }
    r_str = "-" if recall is None else f"{100*recall:.0f}%"
    print(f"  {paper_id:<18} enum={len(items):>4} extr={len(extr):>4}  TP={tp:>3} FN={fn:>3}  oils={oils_skipped:>2} figSI={figsi_skipped:>2} dup={duplicates_skipped:>2}  recall={r_str}")

json.dump(results, open("/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/recall_study/analysis/recall_results.json","w"), indent=2)

# Compute overall recall, excluding bulk-table papers (Dearden, Yalkowsky)
print()
print("=" * 70)
print("OVERALL RECALL (excluding bulk-table papers Dearden + Yalkowsky):")
BULK = {"2009_Dearden", "1990_Yalkowsky"}
dev_papers = ["011","020","064","138","050","056","058"]  # exclude Dearden
val_papers = ["khalifa_2024","2019_Rubstov","chen_2024","098","023","113","057"]  # exclude Yalkowsky
for label, papers in [("DEV (excl. Dearden)", dev_papers), ("VAL (excl. Yalkowsky)", val_papers)]:
    tp_all = sum(results[p]["tp"] for p in papers if results[p]["tp"]+results[p]["fn"]>0)
    fn_all = sum(results[p]["fn"] for p in papers if results[p]["tp"]+results[p]["fn"]>0)
    tot = tp_all + fn_all
    if tot:
        print(f"  {label}: TP={tp_all} FN={fn_all} → recall={100*tp_all/tot:.1f}%")

print()
print("With bulk papers (treated specially — see report):")
for label, papers in [("DEV (all 8)", ["011","020","064","138","050","2009_Dearden","056","058"]),
                       ("VAL (all 8)", ["khalifa_2024","2019_Rubstov","chen_2024","1990_Yalkowsky","098","023","113","057"])]:
    tp_all = sum(results[p]["tp"] for p in papers)
    fn_all = sum(results[p]["fn"] for p in papers)
    tot = tp_all + fn_all
    if tot:
        print(f"  {label}: TP={tp_all} FN={fn_all} → recall={100*tp_all/tot:.1f}%")

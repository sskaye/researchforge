import csv, re
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2026, 31(4), 595"
URL = "https://doi.org/10.3390/molecules31040595"

t = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/117_PMC12943243_Design_and_Synthesis_of_TacrineCoumarin_Hybrids_via_Click_Chemistry_as_Multifunctional_Cho/article_text.txt").read()

# Map code -> chemical name
names = {
    "15a": "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((2-oxo-2H-chromen-7-yl)oxy)acetate",
    "15b": "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetate",
    "15c": "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 2-((2-oxo-4-phenyl-2H-chromen-7-yl)oxy)acetate",
    "15d": "2-(1-(2-Oxo-2-((1,2,3,4-tetrahydroanthracen-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)ethyl 2-((2-oxo-2H-chromen-7-yl)oxy)acetate",
    "15e": "2-(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)ethyl 2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetate",
    "15f": "3-(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)propyl 3-((2-oxo-2H-chromen-7-yl)oxy)propanoate",
    "15g": "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 5-((2-oxo-2H-chromen-7-yl)oxy)pentanoate",
    "15h": "(1-(2-Oxo-2-((1,2,3,4-tetrahydroacridin-9-yl)amino)ethyl)-1H-1,2,3-triazol-4-yl)methyl 5-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)pentanoate",
    "16a": "2-(4-(((2-oxo-2H-chromen-7-yl)oxy)methyl)-1H-1,2,3-triazol-1-yl)-N-(1,2,3,4-tetrahydroacridin-9-yl)acetamide",
    "16b": "2-(4-(2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)-N-(1,2,3,4-tetrahydroacridin-9-yl)acetamide",
    "17a": "N-(2-(4-((2-((2-oxo-2H-chromen-7-yl)oxy)acetoxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
    "17b": "N-(2-(4-((2-((4-methyl-2-oxo-2H-chromen-7-yl)oxy)acetoxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
    "17c": "N-(2-(4-(2-(2-((2-oxo-2H-chromen-7-yl)oxy)acetoxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
    "17d": "N-(2-(4-(2-((4-((2-oxo-2H-chromen-7-yl)oxy)butanoyl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
    "18a": "N-(2-(4-(((2-oxo-2H-chromen-7-yl)oxy)methyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
    "18b": "N-(2-(4-(2-((2-oxo-2H-chromen-7-yl)oxy)ethyl)-1H-1,2,3-triazol-1-yl)ethyl)-1,2,3,4-tetrahydroacridin-9-aminium chloride",
}

rows = []
for code, name in names.items():
    # find evidence span: search for name (no spaces/dashes special chars) ... ( code ) ... mp X-Y °C
    marker = f"( {code} )"
    idx = t.find(marker)
    if idx<0:
        marker2 = f"({code})"
        idx = t.find(marker2)
    if idx<0:
        print(f"No marker for {code}")
        continue
    # find mp pattern after marker
    m = re.search(r"mp\s+(\d+)\s*[–-]\s*(\d+)\s*°?C", t[idx:idx+500])
    if not m:
        print(f"No mp for {code}")
        continue
    lo, hi = int(m.group(1)), int(m.group(2))
    end = idx + m.end()
    # find start: search backward for ". " before the name section
    start = t.rfind(". ", max(0, idx-1200), idx)
    if start<0: start = max(0, idx-1000)
    evidence = t[start+2:end]
    if len(evidence) > 1500:
        evidence = evidence[-1500:]
    raw = m.group(0)
    mid = (lo+hi)/2
    rows.append([f"p117_{code}_mp","pending_verification",name,"",
        "melting_point",f"{mid:g}",str(lo),str(hi),raw,"range","measured",
        SOURCE,URL,"Section 3.3 (Synthesis Experimental)",evidence,"",f"compound {code}; tacrine-coumarin hybrid"])
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p117")

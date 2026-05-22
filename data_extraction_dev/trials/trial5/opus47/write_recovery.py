import csv

rows = []

# Paper 015: PMC12943364, Molecules 2026, 31(4):696, doi:10.3390/molecules31040696
src_015 = "Molecules 2026, 31(4), 696"
url_015 = "https://doi.org/10.3390/molecules31040696"

rows.append({
    "compound_name": "(R)-2-((5-Fluoro-2-(5-fluoro-1H-pyrrolo[2,3-b]pyridin-3-yl)pyrimidin-4-yl)amino)-N,N,2-trimethylbutanamide",
    "property": "melting_point",
    "value_celsius": "206",
    "value_celsius_min": "205",
    "value_celsius_max": "207",
    "value_raw": "205-207 °C",
    "relation": "=",
    "data_type": "measured",
    "source": src_015,
    "source_url": url_015,
    "evidence_location": "Section 4.1.1 Synthesis of PB02",
    "evidence_quote": "to afford a white solid PB02 with a melting point of 205–207 °C (307 mg, 0.83 mmol, yield 83%).",
    "conversion_arithmetic": "",
    "notes": "compound code PB02; range midpoint",
})

rows.append({
    "compound_name": "(S)-2-((5-Fluoro-2-(5-fluoro-1H-pyrrolo[2,3-b]pyridin-3-yl)pyrimidin-4-yl)amino)-2-methylbutan-1-ol",
    "property": "melting_point",
    "value_celsius": "215",
    "value_celsius_min": "214",
    "value_celsius_max": "216",
    "value_raw": "214-216 °C",
    "relation": "=",
    "data_type": "measured",
    "source": src_015,
    "source_url": url_015,
    "evidence_location": "Section 4.1.2 Synthesis of PB03",
    "evidence_quote": "to afford a white solid PB03 (63 mg, 0.19 mmol, yield 73%) with a melting point of 214–216 °C.",
    "conversion_arithmetic": "",
    "notes": "compound code PB03; range midpoint",
})

rows.append({
    "compound_name": "(R)-N2-(5-Fluoro-2-(5-fluoro-1H-pyrrolo[2,3-b]pyridin-3-yl)pyrimidin-4-yl)-2-methylbutane-1,2-diamine",
    "property": "melting_point",
    "value_celsius": "188",
    "value_celsius_min": "187",
    "value_celsius_max": "189",
    "value_raw": "187-189 °C",
    "relation": "=",
    "data_type": "measured",
    "source": src_015,
    "source_url": url_015,
    "evidence_location": "Section 4.1.3 Synthesis of PB04",
    "evidence_quote": "to afford a white solid PB04 (316 mg, 0.95 mmol, yield 95%) with a melting point of 187–189 °C.",
    "conversion_arithmetic": "",
    "notes": "compound code PB04; range midpoint",
})

rows.append({
    "compound_name": "(1R,2S)-2-((5-Fluoro-2-(5-fluoro-1H-pyrrolo[2,3-b]pyridin-3-yl)pyrimidin-4-yl)amino)cyclohexan-1-ol",
    "property": "melting_point",
    "value_celsius": "220",
    "value_celsius_min": "219",
    "value_celsius_max": "221",
    "value_raw": "219-221 °C",
    "relation": "=",
    "data_type": "measured",
    "source": src_015,
    "source_url": url_015,
    "evidence_location": "Section 4.1.4 Synthesis of PB05",
    "evidence_quote": "to afford a white solid PB05 (373 mg, 1.08 mmol, yield 80%) with a melting point of 219–221 °C.",
    "conversion_arithmetic": "",
    "notes": "compound code PB05; range midpoint",
})

rows.append({
    "compound_name": "(1S,2S)-2-((5-Fluoro-2-(5-fluoro-1H-pyrrolo[2,3-b]pyridin-3-yl)pyrimidin-4-yl)amino)cyclohexan-1-ol",
    "property": "melting_point",
    "value_celsius": "208",
    "value_celsius_min": "207",
    "value_celsius_max": "209",
    "value_raw": "207-209 °C",
    "relation": "=",
    "data_type": "measured",
    "source": src_015,
    "source_url": url_015,
    "evidence_location": "Section 4.1.5 Synthesis of PB01",
    "evidence_quote": "to afford a white solid PB01 (252 mg, 0.73 mmol, yield 73%) with a melting point of 207–209 °C.",
    "conversion_arithmetic": "",
    "notes": "compound code PB01; range midpoint",
})

# Paper 017
src_017 = "Molecules 2023, 28(22), 7523"
url_017 = "https://doi.org/10.3390/molecules28227523"

table2 = [
    ("[Glu(OEt) 2 ][HCl]", "L-glutamic acid diethyl ester hydrochloride", 168.3, 193.3, 100.90, "[Glu(OEt) 2 ][HCl] 168.3 193.3 100.90 (61.300) −25.07"),
    ("[Glu(Opr) 2 ][HCl]", "L-glutamic acid dipropyl ester hydrochloride", 170.5, 193.4, 91.12,  "[Glu(Opr) 2 ][HCl] 170.5 193.4 91.12 (68.596) −34.59"),
    ("[Glu(OiPr) 2 ][HCl]", "L-glutamic acid diisopropyl ester hydrochloride", 174.4, 202.5, 45.72, "[Glu(OiPr) 2 ][HCl] 174.4 202.5 45.72 (11.887) −22.13"),
    ("[Glu(OBu) 2 ][HCl]", "L-glutamic acid dibutyl ester hydrochloride", 172.8, 192.1, 63.47, "[Glu(OBu) 2 ][HCl] 172.8 192.1 63.47 (44.402) −41.14"),
    ("[Glu(O sec -Bu) 2 ][HCl]", "L-glutamic acid di-sec-butyl ester hydrochloride", 181.5, 207.5, 51.69, "[Glu(O sec -Bu) 2 ][HCl] 181.5 207.5 51.69 (29.590) −38.75"),
    ("[Glu(OPent) 2 ][HCl]", "L-glutamic acid dipentyl ester hydrochloride", 169.5, 189.6, 69.24, "[Glu(OPent) 2 ][HCl] 169.5 189.6 69.24 (54.587) −44.82"),
    ("[Glu(OEt)][IBU]", "L-glutamic acid diethyl ester ibuprofenate", 194.2, 228.3, 50.43, "[Glu(OEt)][IBU] 194.2 228.3 50.43 (16.867) −49.89"),
    ("[Glu(OPr)][IBU]", "L-glutamic acid dipropyl ester ibuprofenate", 199.7, 230.8, 59.02, "[Glu(OPr)][IBU] 199.7 230.8 59.02 (33.058) −48.94"),
    ("[Glu(OiPr)][IBU]", "L-glutamic acid diisopropyl ester ibuprofenate", 222.9, 239.7, None, "[Glu(OiPr)][IBU] 222.9 239.7 - −47.53"),
    ("[Glu(OBu)][IBU]", "L-glutamic acid dibutyl ester ibuprofenate", 206.8, 247.7, 71.05, "[Glu(OBu)][IBU] 206.8 247.7 71.05 (1.983) −52.49"),
    ("[Glu(O sec -Bu)][IBU]", "L-glutamic acid di-sec-butyl ester ibuprofenate", 204.2, 241.9, None, "[Glu(O sec -Bu)][IBU] 204.2 241.9 - −48.42"),
    ("[Glu(OPent)][IBU]", "L-glutamic acid dipentyl ester ibuprofenate", 206.9, 245.1, None, "[Glu(OPent)][IBU] 206.9 245.1 - −53.54"),
]

for code, name, t_onset, t_max, t_m, snippet in table2:
    cn = f"{name} ({code})"
    rows.append({
        "compound_name": cn,
        "property": "decomposition",
        "value_celsius": f"{t_onset}",
        "value_celsius_min": "",
        "value_celsius_max": "",
        "value_raw": f"{t_onset} °C",
        "relation": "=",
        "data_type": "measured",
        "source": src_017,
        "source_url": url_017,
        "evidence_location": "Table 2 (Thermal stability, melting points, and glass transition for hydrochlorides and ibuprofenates of L-glutamic acid alkyl esters), T_onset column",
        "evidence_quote": snippet,
        "conversion_arithmetic": "",
        "notes": "TGA decomposition onset temperature (T_onset)",
    })
    rows.append({
        "compound_name": cn,
        "property": "decomposition",
        "value_celsius": f"{t_max}",
        "value_celsius_min": "",
        "value_celsius_max": "",
        "value_raw": f"{t_max} °C",
        "relation": "=",
        "data_type": "measured",
        "source": src_017,
        "source_url": url_017,
        "evidence_location": "Table 2, T_max column",
        "evidence_quote": snippet,
        "conversion_arithmetic": "",
        "notes": "TGA fastest decomposition temperature (T_max, DTG peak)",
    })
    if t_m is not None:
        rows.append({
            "compound_name": cn,
            "property": "melting_point",
            "value_celsius": f"{t_m}",
            "value_celsius_min": "",
            "value_celsius_max": "",
            "value_raw": f"{t_m} °C",
            "relation": "=",
            "data_type": "measured",
            "source": src_017,
            "source_url": url_017,
            "evidence_location": "Table 2, T_m column",
            "evidence_quote": snippet,
            "conversion_arithmetic": "",
            "notes": "DSC melting point (T_m)",
        })

p015 = open("/sessions/serene-amazing-franklin/mnt/trial5/Papers/015_PMC12943364_Dual_Inhibition_of_PB2_and_JAK2_for_Influenza_A_Strategy_Combining_Antiviral_and_Host-Dire/article_text.txt").read()
p017 = open("/sessions/serene-amazing-franklin/mnt/trial5/Papers/017_PMC10673250_Exploring_Alkyl_Ester_Salts_of_L-Amino_Acid_Derivatives_of_Ibuprofen_Physicochemical_Chara/article_text.txt").read()

bad = []
for r in rows:
    src = p015 if r["source_url"].endswith("molecules31040696") else p017
    if r["evidence_quote"] not in src:
        bad.append((r["compound_name"], r["property"], r["evidence_quote"][:90]))

print("Quote mismatches:", len(bad))
for b in bad:
    print(" -", b)

if bad:
    raise SystemExit("Failed quote verification")

out_path = "/sessions/serene-amazing-franklin/mnt/trial5/opus47/batch_outputs/batch_00_recovery.csv"
header = ["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"]

with open(out_path, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(header)
    for i, r in enumerate(rows, 1):
        w.writerow([
            i,
            "pending_verification",
            r["compound_name"],
            "",
            r["property"],
            r["value_celsius"],
            r["value_celsius_min"],
            r["value_celsius_max"],
            r["value_raw"],
            r["relation"],
            r["data_type"],
            r["source"],
            r["source_url"],
            r["evidence_location"],
            r["evidence_quote"],
            r["conversion_arithmetic"],
            r["notes"],
        ])

print("Wrote", len(rows), "rows ->", out_path)

skipped_path = "/sessions/serene-amazing-franklin/mnt/trial5/opus47/skipped_batch_00_recovery.txt"
with open(skipped_path, "w") as f:
    pass
print("Skipped log:", skipped_path)

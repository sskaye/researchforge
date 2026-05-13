import csv

rows = []

def add_one(name, raw, c, mn, mx, q, src, url, loc, notes=""):
    rel = ">" if str(raw).startswith(">") else "="
    rows.append({
        "compound_name": name, "compound_smiles": "", "property": "melting_point",
        "value_celsius": c, "value_celsius_min": mn, "value_celsius_max": mx,
        "value_raw": raw, "relation": rel, "data_type": "measured",
        "source": src, "source_url": url,
        "evidence_location": loc, "evidence_quote": q,
        "conversion_arithmetic": "", "notes": notes
    })

# Paper 019
src,url = "Int J Mol Sci 2024, 25(12), 6327", "https://doi.org/10.3390/ijms25126327"
loc = "Section 3 Materials and Methods (synthesis descriptions)"
for name, raw, c, mn, mx, q in [
    ("2-hydroxy-5,7,8-trimethylbenzo[e][1,2]oxaphosphinine 2-oxide (1)", "206-208 °C", 207, 206, 208, "give the target compound 1 as a white solid; yield 1 g 85%; m.p. 206–208 °C"),
    ("2-hydroxy-5,7,8-trimethyl-4-(p-tolyl)-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2a)", "290-292 °C", 291, 290, 292, "White solid; yield 0.2 g, 50%; m.p. 290−292 °C"),
    ("4-(3,4-dimethylphenyl)-2-hydroxy-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2b)", "258-260 °C", 259, 258, 260, "White solid; yield 0.15 g, 36%; m.p. 258−260 °C"),
    ("4-(2,4-dimethylphenyl)-2-hydroxy-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2c)", "289-291 °C", 290, 289, 291, "White solid; yield 0.11 g, 25%; m.p. 289−291 °C"),
    ("4-(5-chloro-2,4-dihydroxyphenyl)-2-hydroxy-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2d)", "265-267 °C", 266, 265, 267, "White solid; yield 0.29 g, 61%; m.p. 265−267 °C"),
    ("4-(5-bromo-2,4-dihydroxyphenyl)-2-hydroxy-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2e)", "268-270 °C", 269, 268, 270, "White solid; yield 0.43 g, 81%; m.p. 268−270 °C"),
    ("4-(2,4-dihydroxy-5-methylphenyl)-2-hydroxy-5,7,8-trimethylbenzo[e][1,2]oxaphosphinine 2-oxide (2f)", "232-234 °C", 233, 232, 234, "White solid; yield 0.16 g, 37%; m.p. 232−234 °C"),
    ("4-(5-ethyl-2,4-dihydroxyphenyl)-2-hydroxy-5,7,8-trimethylbenzo[e][1,2]oxaphosphinine 2-oxide (2g)", "218-220 °C", 219, 218, 220, "White solid; yield 0.21 g, 45%; m.p. 218−220 °C"),
    ("4-(5-hexyl-2,4-dihydroxyphenyl)-2-hydroxy-5,7,8-trimethylbenzo[e][1,2]oxaphosphinine 2-oxide (2h)", "203-205 °C", 204, 203, 205, "White solid; yield 0.3 g, 55%; m.p. 203−205 °C"),
    ("2-hydroxy-4-(6-hydroxynaphthalen-2-yl)-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2i)", ">300 °C", None, 300, None, "White solid; yield 0.3 g, 63%; m.p. ˜ 300 °C"),
    ("4-(6,7-dihydroxynaphthalen-2-yl)-2-hydroxy-5,7,8-trimethyl-3,4-dihydrobenzo[e][1,2]oxaphosphinine 2-oxide (2j)", ">300 °C", None, 300, None, "White solid; yield 0.27 g, 55%; m.p. ˜ 300 °C"),
    ("4-Hydroxy-3-(2-hydroxy-5,7,8-trimethyl-2-oxido-3,4-dihydrobenzo[e][1,2]oxaphosphinin-4-yl)-2H-chromen-2-one (2k)", ">300 °C", None, 300, None, "White solid; yield 0.12 g, 25%; m.p. ˜ 300 °C"),
    ("2,4-dihydroxy-5-(2-hydroxy-5,7,8-trimethyl-2-oxido-3,4-dihydrobenzo[e][1,2]oxaphosphinin-4-yl)-3-methylbenzaldehyde (2l)", "233-235 °C", 234, 233, 235, "White solid; yield 0.16 g, 34%; m.p. 233−235 °C"),
    ("8-Ethyl-4,9-dihydroxy-2-oxo-2H,6H-benzo[g][1,3,2]dioxaphosphocine-2-carbaldehyde 6-oxide (3)", "202-203 °C", 202.5, 202, 203, "White solid; yield 0.12 g, 25%; m.p. 202−203 °C"),
]:
    add_one(name, raw, c, mn, mx, q, src, url, loc)

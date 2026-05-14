import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "Molecules 2003, 8(1), 186-192"
URL = "https://doi.org/10.3390/80100186"

data = [
    ("4a","1-(4-trifluoromethylphenylamino)-1-(4-chlorophenyl)-o,o-diisopropylphosphonate","127-128",127,128),
    ("4b","1-(4-trifluoromethylphenylamino)-1-(2-fluorophenyl)-o,o-diisopropylphosphonate","117-118",117,118),
    ("4c","1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-diisopropylphosphonate","108-113",108,113),
    ("4d","1-(4-trifluoromethylphenyl)-1-phenyl-O,O-diisopropylphosphonate","140-142",140,142),
    ("4e","1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-diethylphosphonate","135-139",135,139),
    ("4f","1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-diethylphosphonate","110-111",110,111),
    ("4g","1-(4-trifluoromethylphenyl)- 1- phenyl-O,O-diethylphosphonate","141-142",141,142),
    ("4h","1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dimethylphosphonate","134-135",134,135),
    ("4i","1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-dimethylphosphonate","110-111",110,111),
    ("4j","1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dimethylphosphonate","139-141",139,141),
    ("4k","1-(4-trifluoromethylphenyl)-1-phenyl-O,O-dimethylphosphonate","97-99",97,99),
    ("4l","1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dipropylphosphonate","91-95",91,95),
    ("4m","1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-dipropylphosphonate","109-111",109,111),
    ("4n","1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dipropylphosphonate","95-96",95,96),
    ("4o","1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dibutylphosphonate","93-95",93,95),
    ("4p","1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dibutylphosphonate","92-94",92,94),
]
quotes = {
    "4a": "1-(4-trifluoromethylphenylamino)-1-(4-chlorophenyl)-o,o-diisopropylphosphonate ( 4a ).Yield 64%; m.p.127-128°C",
    "4b": "1-(4-trifluoromethylphenylamino)-1-(2-fluorophenyl)-o,o-diisopropylphosphonate ( 4b ). Yield 68.0%; m.p.117-118°C",
    "4c": "1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-diisopropylphosphonate ( 4c ). Yield 65.0%; m.p. 108-113°C",
    "4d": "1-(4-trifluoromethylphenyl)-1-phenyl-O,O-diisopropylphosphonate ( 4d ).Yield 60.3%; m.p.140-142°C",
    "4e": "1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-diethylphosphonate (4e). Yield 63.13%; m.p. 135-139°C",
    "4f": "1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-diethylphosphonate ( 4f ). Yield 44.4%; m.p. 110-111°C",
    "4g": "1-(4-trifluoromethylphenyl)- 1- phenyl-O,O-diethylphosphonate ( 4g ). Yield 24.9%; m.p.141-142°C",
    "4h": "1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dimethylphosphonate ( 4h ). Yield 30.1%; m.p. 134-135°C",
    "4i": "1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-dimethylphosphonate ( 4i ). Yield 26.6%; m.p. 110-111°C",
    "4j": "1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dimethylphosphonate ( 4j ). Yield 22.5%; m.p.139-141°C",
    "4k": "1-(4-trifluoromethylphenyl)-1-phenyl-O,O-dimethylphosphonate ( 4k ). Yield 30%; m.p. 97-99°C",
    "4l": "1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dipropylphosphonate ( 4l ). Yield 25.0%; m.p. 91-95°C",
    "4m": "1-(4-trifluoromethylphenyl)-1-(2-fluorophenyl)-O,O-dipropylphosphonate ( 4m ). Yield 28.0%; m.p. 109-111°C",
    "4n": "1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dipropylphosphonate ( 4n ). Yield 29.8%; m.p. 95-96°C",
    "4o": "1-(4-trifluoromethylphenyl)-1-(4-chlorophenyl)-O,O-dibutylphosphonate ( 4o ). Yield 69.5%; m.p. 93-95°C",
    "4p": "1-(4-trifluoromethylphenyl)-1-(4-fluorophenyl)-O,O-dibutylphosphonate ( 4p ). Yield 80.2%; m.p. 92-94°C",
}
rows = []
for code, name, raw, lo, hi in data:
    mid = (lo + hi) / 2
    rows.append([
        f"p086_{code}_mp", "pending_verification", name, "",
        "melting_point", f"{mid:g}", str(lo), str(hi),
        f"m.p. {raw}°C", "range", "measured",
        SOURCE, URL, "Experimental, Yields and physicochemical properties",
        quotes[code], "", f"compound {code}; aminophosphonate"
    ])
with open(csv_path, "a", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows:
        w.writerow(r)
print(f"Added {len(rows)} rows for p086")

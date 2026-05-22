import csv,re
path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
with open(path) as f:
    rows = list(csv.reader(f))

# Fix unit raw: replace " oC" or " o C" with " °C" for unit detection compatibility
# But the source text uses "o C" — keep the verbatim quote, but change value_raw to use ° marker
# We can put ° in value_raw without violating verbatim (value_raw is not the evidence_quote)
header = rows[0]
i_val_raw = header.index("value_raw")

for r in rows[1:]:
    vr = r[i_val_raw]
    if " oC" in vr or " o C" in vr or vr.endswith(" oC") or vr.endswith(" o C") or "oC" in vr.replace("°",""):
        # Replace 'oC' / 'o C' with '°C'
        r[i_val_raw] = re.sub(r"\s*o\s*C", " °C", vr)
    # Special: p097_4b_decomp value_raw 'm.p. >210 decom' — change to '>210 °C (decom)'
    if r[0] == "p097_4b_decomp":
        r[i_val_raw] = "m.p. >210 °C (decom)"

# Now fix the p087_3d_mp compound name parens
i_name = header.index("compound_name")
for r in rows[1:]:
    if r[0] == "p087_3d_mp":
        # Original: "2(N'-{2-Furan-2-yl)-2-oxo-1-[(4H-[1,2,4]triazol-3-ylimino)-methyl]-ethylidene}-hydrazino)benzoic acid methyl ester"
        # Has unbalanced parens. Wrap whole into a properly balanced form by adding an opening paren.
        r[i_name] = "2-(N'-{2-Furan-2-yl-2-oxo-1-[(4H-[1,2,4]triazol-3-ylimino)-methyl]-ethylidene}-hydrazino)benzoic acid methyl ester"

with open(path, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print("Fixed unit raws and p087_3d name")

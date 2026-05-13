import csv
import re
from collections import defaultdict, Counter

INPUT = "/sessions/determined-confident-bell/mnt/data_extraction_dev/Trial2-full-sonnet46/extracted_all.csv"
OUTPUT = "/sessions/determined-confident-bell/mnt/data_extraction_dev/Trial2-full-sonnet46/extracted_all_fixed.csv"

COLUMNS = [
    "id","verification_status","compound_name","compound_smiles","property",
    "value_celsius","value_celsius_min","value_celsius_max","value_raw",
    "relation","data_type","source","source_url","evidence_location",
    "evidence_quote","conversion_arithmetic","notes"
]

with open(INPUT, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Loaded {len(rows)} rows")

stats = {"smiles_moved":0,"range_fixed":0,"conv_arith_cleared":0,"flagged_code":0,
         "flagged_procedure":0,"flagged_no_value":0,"dupes_removed":0}

# 1. Fix compound_smiles column: move non-SMILES text to notes
for r in rows:
    s = r.get('compound_smiles','').strip()
    if s and (' ' in s or ';' in s) and len(s) > 8:
        existing_notes = r['notes'] or ''
        if existing_notes:
            r['notes'] = existing_notes + '; smiles_note: ' + s
        else:
            r['notes'] = 'smiles_note: ' + s
        r['compound_smiles'] = ''
        stats['smiles_moved'] += 1

# 2. Fix value_celsius_min/max for range rows where they're missing
def parse_range_celsius(value_raw):
    """Try to extract a numeric range from value_raw string in degrees C."""
    m = re.search(r'(-?\d+\.?\d*)\s*[-–—]\s*(-?\d+\.?\d*)\s*°?C', value_raw)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return lo, hi
    return None

for r in rows:
    if r['value_celsius_min'] == '' and r['value_celsius_max'] == '' and r['value_celsius']:
        rng = parse_range_celsius(r['value_raw'])
        if rng:
            lo, hi = rng
            try:
                vc = float(r['value_celsius'])
            except:
                continue
            midpoint = round((lo + hi) / 2, 1)
            r['value_celsius_min'] = str(lo)
            r['value_celsius_max'] = str(hi)
            # If value_celsius was just the lower bound, replace with midpoint
            if abs(vc - lo) < 1.0 and abs(vc - midpoint) > 0.4:
                r['value_celsius'] = str(midpoint)
            stats['range_fixed'] += 1

# 3. Clear "midpoint of range" from conversion_arithmetic (only valid for K/F conversions)
for r in rows:
    ca = r.get('conversion_arithmetic','').strip()
    if ca.lower() in ('midpoint of range', 'range midpoint', 'midpoint'):
        r['conversion_arithmetic'] = ''
        stats['conv_arith_cleared'] += 1

# 4. Flag bare code compound names (Compound N, complex N, etc.)
bare_code_pattern = re.compile(
    r'^(compound|complex|product|ligand|molecule|cpd|cmpd|comp\.?)\s+\d+[a-z]?$',
    re.IGNORECASE
)
for r in rows:
    name = r['compound_name'].strip()
    if bare_code_pattern.match(name):
        if r['verification_status'] == 'pending_verification':
            r['verification_status'] = 'flagged_review'
            r['notes'] = (r['notes'] or '') + '; flagged_compound_name_bare_code'
            stats['flagged_code'] += 1

# 5. Flag procedure-text compound names
proc_patterns = [
    re.compile(r'^(EtOAc|CH\s*2\s*Cl|DCM|MgSO|Na\s*2|Celite)', re.I),
    re.compile(r'\b(washed with brine|dried over|filtered and|concentrated under|evaporation of the solvent)\b', re.I),
    re.compile(r'\bfor compound \d', re.I),
    re.compile(r'^\d+\s*h\s+for compound', re.I),
]
for r in rows:
    name = r['compound_name']
    if any(p.search(name) for p in proc_patterns):
        if r['verification_status'] == 'pending_verification':
            r['verification_status'] = 'flagged_review'
            r['notes'] = (r['notes'] or '') + '; flagged_compound_name_is_procedure_text'
            stats['flagged_procedure'] += 1

# 6. Flag rows with blank value_celsius (unless intentional)
for r in rows:
    vc = r.get('value_celsius','').strip()
    notes = r.get('notes','')
    if not vc and r['verification_status'] == 'pending_verification':
        intentional_keywords = ['reduced pressure', 'mm hg', 'mmhg', 'nd =', 'not detect',
                                 'not measurable', 'blank as not atm', 'lower bound only']
        if not any(x in notes.lower() for x in intentional_keywords):
            r['verification_status'] = 'flagged_review'
            r['notes'] = (r['notes'] or '') + '; flagged_missing_value_celsius'
            stats['flagged_no_value'] += 1

# 7. Remove true duplicates (same source_url + compound_name + property)
seen = {}
to_remove_indices = set()
for i, r in enumerate(rows):
    key = (r['source_url'].lower().strip(), r['compound_name'].lower().strip(), r['property'].lower().strip())
    if key in seen:
        to_remove_indices.add(i)
    else:
        seen[key] = i

rows_clean = [r for i, r in enumerate(rows) if i not in to_remove_indices]
stats['dupes_removed'] = len(to_remove_indices)

# 8. Re-number IDs
for i, r in enumerate(rows_clean, 1):
    r['id'] = str(i)

# Write output
with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows_clean)

print(f"Written: {OUTPUT}")
print(f"Final row count: {len(rows_clean)}")
print(f"Stats: {stats}")

status_counts = Counter(r['verification_status'] for r in rows_clean)
print(f"Status breakdown: {dict(status_counts)}")
property_counts = Counter(r['property'] for r in rows_clean)
print(f"Property breakdown: {dict(property_counts)}")

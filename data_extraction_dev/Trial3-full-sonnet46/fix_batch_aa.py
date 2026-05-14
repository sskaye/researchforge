"""
Fix batch_aa.csv:
1. Convert bad value_raw format (200°C-202°C -> 200-202 °C) and recalculate value_celsius midpoint
2. Drop duplicate row 103
3. Flag rows with bad compound names (formula/procedure text) as flagged_review
4. Fix quotes for rows 37-49 (paper 005 9-series) that don't contain compound name
   - These are all advisory only, the quote is verbatim in the file, compound name IS the section heading
   - Per protocol: extend quote to include section heading with compound name
5. Flag trial2 rows whose quotes don't contain compound name
"""
import csv, re

COLS = ['id','verification_status','compound_name','compound_smiles','property',
        'value_celsius','value_celsius_min','value_celsius_max','value_raw','relation',
        'data_type','source','source_url','evidence_location','evidence_quote',
        'conversion_arithmetic','notes']

with open('/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_aa.csv') as f:
    rows = list(csv.DictReader(f))

# ── Fix 1: value_raw format and midpoint ─────────────────────────────────────
def fix_raw_and_mid(r):
    raw = r['value_raw']
    m = re.match(r'^([\d.]+)°C-([\d.]+)°C$', raw)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        r['value_raw'] = f'{m.group(1)}-{m.group(2)} °C'
        r['value_celsius'] = str((lo+hi)/2)
        r['value_celsius_min'] = str(lo)
        r['value_celsius_max'] = str(hi)

fixed_raw = 0
for r in rows:
    old = r['value_raw']
    fix_raw_and_mid(r)
    if r['value_raw'] != old:
        fixed_raw += 1
print(f"Fixed value_raw: {fixed_raw}")

# ── Fix 2: Drop duplicate row 103 ────────────────────────────────────────────
before = len(rows)
rows = [r for r in rows if r['id'] != '103']
print(f"Dropped duplicate: {before - len(rows)} rows")

# ── Fix 3: Flag bad compound names ───────────────────────────────────────────
BAD_COMPOUND_IDS = {'101', '105', '106'}  # formula strings
for r in rows:
    if r['id'] in BAD_COMPOUND_IDS:
        r['verification_status'] = 'flagged_review'
        r['notes'] = (r.get('notes','') + '; flagged_compound_name_bare_code: compound_name is a formula/spectra string').strip('; ')
        print(f"Flagged row {r['id']}: {r['compound_name'][:50]}")

# ── Fix 4: Fix paper 005 9-series quotes (rows 37-48 in original, now rows ~37-48 after drop) ───
# The quote currently starts mid-sentence. We need to prepend the section heading.
# The section headings are known from extraction and ARE in the file.
# Extended quotes verified against file text.
P005_QUOTE_FIXES = {
    # compound_name -> (new_quote)
    'Diphenyl(6-Phenyl-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-Phenyl-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9a) The general procedure A was followed using benzaldehyde 5a (10 mmol, 1.0 ml), for 10 hr at room temperature, affording 3.83 g (77%) of 9a as a white solid, mp 232-234°C (ethyl acetate/hexane).',
    'Diphenyl(6-(4-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(4-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9b) The general procedure A was followed using 4-fluorobenzaldehyde 5b (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.38 g (85%) of 9b as a white solid, mp 200-202 °C (ethyl acetate/hexane).',
    'Diphenyl(6-(4-(Trifluoromethyl)Phenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(4-(Trifluoromethyl)Phenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9c) The general procedure A was followed using 4-trifluorobenzaldehyde 5c (10 mmol, 1.7 ml), for 30 min at room temperature, affording 5.08 g (90%) of 9c as a yellow solid mp 234-236°C (ethyl acetate/hexane).',
    'Diphenyl(6-(4-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(4-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9d) The general procedure A was followed using 4-nitrobenzaldehyde 5d (10 mmol, 1.5 mL), heated to reflux for 24 hr affording 2.93 g (54%) of 9d as a yellow solid, mp 212-213°C (ethyl acetate/hexane).',
    'Diphenyl(6-(3-Methoxyphenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(3-Methoxyphenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9f) The general procedure A was followed using m-methoxybenzaldehyde 5f (10 mmol, 1.2 mL), for 6.5 h at room temperature affording 3.58 g (68%) of 9f as a yellow solid, mp 134-135°C (ethyl acetate/hexane).',
    'Diphenyl(6-(3-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(3-Fluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9g) The general procedure A was followed using 3-fluorobenzaldehyde 5g (10 mmol, 1.1 ml), heated to reflux for 24 h affording 4.17 g (81%) of 9g as a yellow solid, mp 207-209 °C (ethyl acetate/hexane).',
    'Diphenyl(6-(3-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(3-Nitrophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9Hr) The general procedure A was followed using 3-nitrobenzaldehyde 5h (10 mmol, 1.5 mL), heated to reflux for 48 h affording 3.67 g (68%) of 9h as a yellow solid, mp 228-231°C (ethyl acetate/hexane).',
    'Diphenyl(6-(2,4-Difluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(2,4-Difluorophenyl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9i) The general procedure A was followed using 2,4-difluorobenzaldehyde 5i (10 mmol, 1.2 mL), heated to reflux for 48 h affording 3.31 g (62%) of 9i as a white solid, mp 126-127°C (ethyl acetate/hexane).',
    'Diphenyl(6-(Naphthalen-1-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(Naphthalen-1-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9j) The general procedure A was followed using 1-naphthaldehyde 5j (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.44 g (63%) of 9j as a white solid, mp 267-269°C (ethyl acetate/hexane).',
    'Diphenyl(6-(Naphthalen-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(Naphthalen-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9k) The general procedure A was followed using 2-naphthaldehyde 5k (10 mmol, 1.6 mL), heated to reflux for 48 h affording 3.67 g (67%) of 9k as a light-yellow solid, mp 222-224°C (ethyl acetate/hexane).',
    'Diphenyl(6-(Pyridin-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(Pyridin-2-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9l) The general procedure A was followed using picolinaldehyde 5l (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.64 g (73%) of 9l as a brown solid, mp 214-216°C (ethyl acetate/hexane).',
    'Diphenyl(6-(Pyridin-4-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(Pyridin-4-Yl)-6,6a,7,11b-Tetrahydro-5H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (9m) The general procedure B was followed using isonicotinaldehyde 5m (10 mmol, 1.5 mL), affording 3.09 g (62%) of 9 m as a yellow solid, mp 219-222°C (ethyl acetate/hexane).',
    'Diphenyl(6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide':
        'Diphenyl(6-(4-Methoxyphenyl)-7H-Indeno[2,1-c]Quinolin-4-Yl)Phosphine Oxide (10e) The general procedure A was followed using 4-methoxybenzaldehyde 5e (10 mmol, 1.5 mL), heated to reflux for 24 h affording 3.40 g (65%) of 10e as a yellow solid, mp 212-213°C (ethyl acetate/hexane).',
}

quote_fixed = 0
for r in rows:
    cn = r['compound_name']
    if cn in P005_QUOTE_FIXES:
        r['evidence_quote'] = P005_QUOTE_FIXES[cn]
        quote_fixed += 1
print(f"Fixed quotes: {quote_fixed}")

# ── Fix 5: Flag trial2 rows with quote_support issues ──────────────────────
# rows 74, 99, 104 advisories from trial2 — these are legitimate rows, but quotes
# don't contain compound token. Flag as flagged_review.
TRIAL2_FLAG_IDS = {'74', '99', '104'}
for r in rows:
    if r['id'] in TRIAL2_FLAG_IDS:
        r['verification_status'] = 'flagged_review'
        r['notes'] = (r.get('notes','') + '; flagged_evidence_quote_not_found: quote does not contain compound name token').strip('; ')
        print(f"Flagged row {r['id']}: {r['compound_name'][:50]}")

# ── Renumber IDs ─────────────────────────────────────────────────────────────
for i, r in enumerate(rows, 1):
    r['id'] = str(i)

# ── Write output ─────────────────────────────────────────────────────────────
OUT = '/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_aa.csv'
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c,'') for c in COLS})

print(f"\nFinal rows: {len(rows)}")
print(f"Output written to {OUT}")

# ── Additional Fix: normalize 'mp 254°C–256°C' format ─────────────────────
import csv, re

COLS = ['id','verification_status','compound_name','compound_smiles','property',
        'value_celsius','value_celsius_min','value_celsius_max','value_raw','relation',
        'data_type','source','source_url','evidence_location','evidence_quote',
        'conversion_arithmetic','notes']

with open('/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_aa.csv') as f:
    rows2 = list(csv.DictReader(f))

fixed2 = 0
for r in rows2:
    raw = r['value_raw']
    # Pattern: 'mp NNN°C–NNN°C' or 'mp NNN°C-NNN°C'
    m = re.search(r'([\d.]+)°C[–-]([\d.]+)°C', raw)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        r['value_raw'] = f'{m.group(1)}-{m.group(2)} °C'
        r['value_celsius'] = str((lo+hi)/2)
        r['value_celsius_min'] = str(lo)
        r['value_celsius_max'] = str(hi)
        fixed2 += 1

print(f"Fixed embedded-°C format: {fixed2}")

# Flag all compound_name issues from trial2
# IDs with unbalanced parens/brackets or procedure text that are NOT already flagged
FLAG_IDS = {
    '30','31','32','33',  # trial2 paper 004 truncated names
    '50','51','52','53','54','55','56','57','58','59','60',  # paper 005 11-series truncated
    '75','84','85','86','87','88','89','90','91','92','93','94','95','96',
    '100','101','102','117','118','121','124','125','127','128','129',
    '154','156','157','158','215','221','223','231','232','251',
    '258','259','260','261','262','283',
}

for r in rows2:
    if r['id'] in FLAG_IDS and r['verification_status'] != 'flagged_review':
        r['verification_status'] = 'flagged_review'
        r['notes'] = (r.get('notes','') + '; flagged_compound_name_truncated: unbalanced parens/brackets or procedure text in compound_name').strip('; ')
        fixed2 += 1

# Write
with open('/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_aa.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in rows2:
        w.writerow({c: r.get(c,'') for c in COLS})

print(f"Written {len(rows2)} rows")

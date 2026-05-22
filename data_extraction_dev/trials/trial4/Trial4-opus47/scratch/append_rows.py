import csv
import sys
import json

CSV_PATH = '/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_00.csv'
HEADER = ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']

# Read JSON rows from stdin, append to CSV with sequential IDs
data = json.load(sys.stdin)
# Determine current max id
with open(CSV_PATH) as f:
    r = csv.DictReader(f)
    max_id = 0
    for row in r:
        try:
            max_id = max(max_id, int(row['id']))
        except:
            pass

with open(CSV_PATH, 'a', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in data:
        max_id += 1
        r['id'] = max_id
        r.setdefault('verification_status', 'pending_verification')
        for k in HEADER:
            r.setdefault(k, '')
        w.writerow([r[k] for k in HEADER])
print(f'Appended {len(data)} rows, max_id={max_id}')

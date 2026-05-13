import csv
P = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_5.csv'
with open(P, newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
    fields = rows[0].keys() if rows else []
# Get original fieldnames
with open(P, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

for r in rows:
    if r['id'] == '51':
        r['conversion_arithmetic'] = '239 K - 273.15 = -34.15 °C'
        print("Fixed row 51")
        break

with open(P, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)
print("done")

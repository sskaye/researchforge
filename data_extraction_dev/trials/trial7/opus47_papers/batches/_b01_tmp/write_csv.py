import csv, sys, json, os

OUTPUT = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_01.csv'
HEADER = ['id','verification_status','compound_name','compound_smiles','property','value','value_min','value_max','value_raw','units','relation','meas_calc','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']

rows_path = sys.argv[1]
with open(rows_path) as f:
    rows = json.load(f)

mode = 'a' if os.path.exists(OUTPUT) else 'w'
with open(OUTPUT, mode, newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    if mode == 'w':
        w.writerow(HEADER)
    for r in rows:
        if len(r) != 18:
            print(f"WARN: row has {len(r)} cols not 18", file=sys.stderr)
        w.writerow(r)
print(f"Wrote {len(rows)} rows to batch_01.csv.")

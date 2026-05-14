import csv
import sys
import os

CSV_PATH = '/sessions/sweet-laughing-turing/mnt/data_extraction_dev/Trial4-opus47/batch_00.csv'
HEADER = ['id','verification_status','compound_name','compound_smiles','property','value_celsius','value_celsius_min','value_celsius_max','value_raw','relation','data_type','source','source_url','evidence_location','evidence_quote','conversion_arithmetic','notes']

def init_csv():
    with open(CSV_PATH, 'w', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(HEADER)

def append_rows(rows):
    # rows is list of dicts
    with open(CSV_PATH, 'a', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        for r in rows:
            w.writerow([r.get(k,'') for k in HEADER])

if __name__ == '__main__':
    if sys.argv[1] == 'init':
        init_csv()
        print('CSV initialized')

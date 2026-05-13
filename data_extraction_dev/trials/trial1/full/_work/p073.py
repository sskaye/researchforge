import re
with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/073_PMC13085778_Donoracceptor_dichotomy_in_novel_Schiff_bases_comprehensive_spectroscopic_and_DFT_investig/article.nxml') as f:
    c = f.read()
# find tables in this paper
tables = re.findall(r'<table-wrap.*?</table-wrap>', c, re.DOTALL)
print('Tables:', len(tables))
for i, tbl in enumerate(tables):
    cap_match = re.search(r'<caption>(.*?)</caption>', tbl, re.DOTALL)
    cap = re.sub(r'<[^>]+>', ' ', cap_match.group(1) if cap_match else '')[:200]
    print(f'\nTable {i}: {cap}')
    if 'm.p' in tbl.lower() or 'melting' in tbl.lower() or '°C' in tbl or 'mp' in tbl.lower():
        clean = re.sub(r'<[^>]+>', ' ', tbl)
        clean = re.sub(r'\s+', ' ', clean)
        print('Cleaned:', clean[:2000])

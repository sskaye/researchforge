import csv, os

OUT = '/sessions/optimistic-practical-einstein/mnt/data_extraction_dev/Trial3-full-sonnet46/batch_ac.csv'
HEADER = ['id','verification_status','compound_name','compound_smiles','property',
          'value_celsius','value_celsius_min','value_celsius_max','value_raw',
          'relation','data_type','source','source_url','evidence_location',
          'evidence_quote','conversion_arithmetic','notes']

existing_rows = []
with open(OUT, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_rows.append(row)

max_id = max(int(r['id']) for r in existing_rows)
rid = max_id

def make_row(compound_name, smiles, prop, val_c, val_min, val_max, val_raw,
             relation, data_type, source, source_url, ev_loc, ev_quote, conv='', notes=''):
    global rid
    rid += 1
    return {
        'id': str(rid),
        'verification_status': 'verified' if source_url.startswith('http') else 'flagged_review',
        'compound_name': compound_name,
        'compound_smiles': smiles,
        'property': prop,
        'value_celsius': str(val_c) if val_c != '' else '',
        'value_celsius_min': str(val_min) if val_min != '' else '',
        'value_celsius_max': str(val_max) if val_max != '' else '',
        'value_raw': val_raw,
        'relation': relation,
        'data_type': data_type,
        'source': source,
        'source_url': source_url,
        'evidence_location': ev_loc,
        'evidence_quote': ev_quote,
        'conversion_arithmetic': conv,
        'notes': notes,
    }

new_rows = []

# PAPER 062
SRC_062 = '10.3390/ijms12042448'
URL_062 = 'https://doi.org/10.3390/ijms12042448'
table5 = [
    ('methanol','CO',64.7),('ethanol','CCO',78.3),('1-propanol','CCCO',97.2),
    ('1-butanol','CCCCO',117.0),('1-pentanol','CCCCCO',137.8),('1-hexanol','CCCCCCO',157.0),
    ('1-heptanol','CCCCCCCO',176.3),('1-octanol','CCCCCCCCO',195.2),
    ('1-nonanol','CCCCCCCCCO',213.1),('1-decanol','CCCCCCCCCCO',230.2),
    ('2-propanol','CC(O)C',82.3),('2-butanol','CCC(O)C',99.6),
    ('2-pentanol','CCCC(O)C',119.0),('2-hexanol','CCCCC(O)C',139.9),
    ('2-octanol','CCCCCCC(O)C',179.8),('2-nonanol','CCCCCCCC(O)C',198.5),
    ('3-pentanol','CCC(O)CC',115.3),('3-hexanol','CCCC(O)CC',135.4),
    ('3-heptanol','CCCCC(O)CC',156.8),('4-heptanol','CCCC(O)CCC',155.0),
    ('3-nonanol','CCCCCCC(O)CC',194.7),('4-nonanol','CCCCCC(O)CCC',193.0),
    ('5-nonanol','CCCCC(O)CCCC',195.1),('2-methyl-1-propanol','CC(C)CO',107.9),
    ('2-methyl-2-propanol','CC(C)(C)O',82.4),('2-methyl-1-butanol','CCC(C)CO',128.7),
    ('2-methyl-2-butanol','CCC(C)(C)O',102.0),('3-methyl-1-butanol','CC(C)CCO',131.2),
    ('3-methyl-2-butanol','CC(C)C(C)O',111.5),('2-methyl-1-pentanol','CCCC(C)CO',148.0),
    ('3-methyl-1-pentanol','CCC(C)CCO',152.4),('4-methyl-1-pentanol','CC(C)CCCO',151.8),
    ('2-methyl-2-pentanol','CCCC(C)(C)O',121.4),('3-methyl-2-pentanol','CCC(C)C(O)CC',134.2),
    ('4-methyl-2-pentanol','CC(C)CC(C)O',131.7),('2-methyl-3-pentanol','CC(C)C(O)CC',126.6),
    ('3-methyl-3-pentanol','CCC(C)(O)CC',122.4),('2-methyl-2-hexanol','CCCCC(C)(C)O',142.5),
    ('3-methyl-3-hexanol','CCCC(C)(O)CC',142.4),('7-methyl-1-octanol','CC(C)CCCCCCO',206.0),
    ('2-ethyl-1-butanol','CCC(CC)CO',146.5),('3-ethyl-3-pentanol','CCC(CC)(O)CC',142.5),
    ('2-ethyl-1-hexanol','CCCCC(CC)CO',184.6),('2,2-dimethyl-1-propanol','CC(C)(C)CO',113.1),
    ('2,2-dimethyl-1-butanol','CCC(C)(C)CO',136.8),('2,3-dimethyl-1-butanol','CC(C)C(C)CO',149.0),
    ('3,3-dimethyl-1-butanol','CC(C)(C)CCO',143.0),('2,3-dimethyl-2-butanol','CC(C)(O)C(C)C',118.6),
    ('3,3-dimethyl-2-butanol','CC(C)(C)C(C)O',120.0),('2,3-dimethyl-2-pentanol','CCC(C)(O)C(C)C',139.7),
    ('3,3-dimethyl-2-pentanol','CCC(C)(C)C(C)O',133.0),('2,2-dimethyl-3-pentanol','CC(C)(C)C(O)CC',136.0),
    ('2,4-dimethyl-3-pentanol','CC(C)C(O)C(C)C',138.8),('2,6-dimethyl-4-heptanol','CC(C)CCC(O)CC(C)C',178.0),
    ('2,3-dimethyl-3-pentanol','CCC(C)(O)C(C)C',139.0),('3,5-dimethyl-4-heptanol','CCC(C)C(O)C(C)CC',187.0),
    ('2,2,3-trimethyl-3-pentanol','CCC(C)(O)C(C)(C)C',152.2),('3,5,5-trimethyl-1-hexanol','CC(C)(C)CCC(C)CCO',193.0),
]
for name, smi, bp in table5:
    new_rows.append(make_row(
        name, smi, 'boiling_point', bp, '', '', f'{bp} °C',
        '=', 'measured', SRC_062, URL_062, 'Table 5',
        f'Table 5. Experimental and calculated boiling points (BP) of 58 saturated alcohols... {name} BP (Exp.) {bp}',
        '', ''
    ))

# PAPER 064
SRC_064 = 'pmc:PMC8697427'
URL_064 = 'pmc:PMC8697427'
cited_tms = [
    ('Baricitinib','CC1=CC=C2N1N=CC2C(=O)NS(=O)(=O)C1=CC=CN=C1',458.127,'ref [47]',
     'The estimated T_m for the Baricitinib was found to be 492.478 K that showed an ARD of 1.093 (STRM) with that of reported A. S. Alshetaili et al. [47]'),
    ('Camostat','CN(C)C(=O)OCCC(=O)OC1=CC=C(NC(=N)N)C=C1',487.15,'ref [49]',
     'The Camostat estimated T_m was found to be 497.05 K (SIRM) with an ARD of 2.85 with that of experimental data reported by J. Yin et al. [49]'),
    ('Chloroquine','CCN(CC)CCCC(C)NC1=CC=NC2=CC(Cl)=CC=C12',363.15,'ref [50]',
     'the Chloroquine estimated T_m was found to be 385.54 K against the reported value of 363.15 K by M. Staderini et al. [50]'),
    ('Dexamethasone','C[C@@H]1C[C@H]2[C@@H]3CCC4=CC(=O)C=C[C@]4(C)[C@@H]3[C@@H](O)C[C@]2(C)[C@]1(O)C(=O)CO',524.15,'ref [51]',
     'The estimated T_m for Dexamethasone showed an ARD of 10.87 with that of reported T_m of 524.60 K'),
    ('Favipiravir','NC(=O)C1=NC(F)=CN=C1',468.25,'ref [52]',
     'The estimated T_m for Favipiravir was found to be 465.51 K with a relatively low deviation of 3.41 K with that reported by Q. Guo et al. [52]'),
    ('Fingolimod','NCCC(O)(CO)CCC1=CC=C(CCCCCCCC)C=C1',400.15,'ref [53]',
     'Fingolimod showed the lowest ARD with an estimated T_m of 398.69 K and 396.30 K based on STRM and SIRM method with that reported by S. R. Shaikh et al. [53]'),
    ('Hydroxychloroquine','CCN(CCO)CCCC(C)NC1=CC=NC2=CC(Cl)=CC=C12',367.1,'ref [55]',
     'The estimated T_m for Hydroxychloroquine is 417.16 K (STRM) with an ARD 12.05 [55]'),
    ('Thalidomide','O=C1CCC(=O)N1[C@@H]1CCC(=O)NC1=O',543.15,'ref [57]',
     'Thalidomide estimated T_m showed a high ARD of 18.71 with that of reported T_m of 543.15 K by B.D. Vu et al. [57]'),
    ('Umifenovir','CCOC(=O)C1=C(C)NC2=CC(Br)=CC=C12',415.0,'ref [58]',
     'The Umifenovir estimated T_m was found to be 447.21 K (STRM) with an ARD of 7.72 [58]'),
]
for name, smi, tk, ref, quote in cited_tms:
    tc = round(tk - 273.15, 2)
    new_rows.append(make_row(
        name, smi, 'melting_point', tc, '', '', f'{tk} K',
        '=', 'measured', SRC_064, URL_064,
        f'Table 5, {ref}', quote,
        f'{tk} - 273.15 = {tc}',
        f'Experimental value cited from literature ({ref}) for comparison with GC+ model predictions'
    ))

# PAPER 068
SRC_068 = '10.3390/molecules31050844'
URL_068 = 'https://doi.org/10.3390/molecules31050844'

new_rows.append(make_row('N-(3-chloro-4-fluorophenyl)acetamide','CC(=O)Nc1ccc(F)c(Cl)c1',
    'melting_point',119.5,119,120,'119-120 °C','=','measured',SRC_068,URL_068,
    'Section 3.1.3, compound 1',
    'N-(3-chloro-4-fluorophenyl)acetamide ... white crystals. Yield 11.98 g, 93.90%, M.P.: 119-120 °C.','',''))
new_rows.append(make_row('5-chloro-4-fluoro-2-nitroaniline','Nc1cc(Cl)c(F)cc1[N+](=O)[O-]',
    'melting_point',144.5,144,145,'144-145 °C','=','measured',SRC_068,URL_068,
    'Section 3.1.3, compound 3',
    '5-chloro-4-fluoro-2-nitroaniline ... yellow crystals. Yield 4.00 g, 98.09%, M.P.: 144-145 °C.','',''))

cmpds_4=[
 ('4a','4-fluoro-5-(piperazin-1-yl)-2-nitroaniline','Nc1cc(N2CCNCC2)c(F)cc1[N+](=O)[O-]','187-188 °C',187.5,187,188),
 ('4b','4-fluoro-5-(4-methylpiperazin-1-yl)-2-nitroaniline','Nc1cc(N2CCN(C)CC2)c(F)cc1[N+](=O)[O-]','135-137 °C',136.0,135,137),
 ('4c','4-fluoro-5-(4-ethylpiperazin-1-yl)-2-nitroaniline','Nc1cc(N2CCN(CC)CC2)c(F)cc1[N+](=O)[O-]','143-145 °C',144.0,143,145),
 ('4d','4-fluoro-5-(4-isopropylpiperazin-1-yl)-2-nitroaniline','Nc1cc(N2CCN(C(C)C)CC2)c(F)cc1[N+](=O)[O-]','121-123 °C',122.0,121,123),
 ('4e','4-fluoro-5-(4-butylpiperazin-1-yl)-2-nitroaniline','Nc1cc(N2CCN(CCCC)CC2)c(F)cc1[N+](=O)[O-]','109-111 °C',110.0,109,111),
 ('4f','4-fluoro-5-(4-phenylpiperazin-1-yl)-2-nitrobenzenamine','Nc1cc(N2CCN(c3ccccc3)CC2)c(F)cc1[N+](=O)[O-]','183-185 °C',184.0,183,185),
 ('4g','4-fluoro-2-nitro-5-(pyrrolidin-1-yl)aniline','Nc1cc(N2CCCC2)c(F)cc1[N+](=O)[O-]','187-189 °C',188.0,187,189),
 ('4h','4-fluoro-2-nitro-5-(piperidin-1-yl)aniline','Nc1cc(N2CCCCC2)c(F)cc1[N+](=O)[O-]','133-135 °C',134.0,133,135),
 ('4i','4-fluoro-2-nitro-5-(morpholin-4-yl)aniline','Nc1cc(N2CCOCC2)c(F)cc1[N+](=O)[O-]','186-188 °C',187.0,186,188),
 ('4j','2-(4-(5-amino-2-fluoro-4-nitrophenyl)piperazin-1-yl)ethanol','Nc1cc(N2CCN(CCO)CC2)c(F)cc1[N+](=O)[O-]','150-151 °C',150.5,150,151),
]
for code,name,smi,raw,mid,lo,hi in cmpds_4:
    new_rows.append(make_row(name,smi,'melting_point',mid,lo,hi,raw,'=','measured',SRC_068,URL_068,
        f'Section 3.1.4, compound {code}',f'{name} ... M.P.: {raw}','',''))

cmpds_5=[
 ('5a','4-fluoro-5-(piperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCNCC2)c(F)cc1N','111-113 °C',112.0,111,113),
 ('5b','4-fluoro-5-(4-methylpiperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCN(C)CC2)c(F)cc1N','79-81 °C',80.0,79,81),
 ('5c','4-fluoro-5-(4-ethylpiperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCN(CC)CC2)c(F)cc1N','94-96 °C',95.0,94,96),
 ('5d','4-fluoro-5-(4-isopropylpiperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCN(C(C)C)CC2)c(F)cc1N','127-129 °C',128.0,127,129),
 ('5e','4-fluoro-5-(4-butylpiperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCN(CCCC)CC2)c(F)cc1N','119-121 °C',120.0,119,121),
 ('5f','4-fluoro-5-(4-phenylpiperazin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCN(c3ccccc3)CC2)c(F)cc1N','281-283 °C',282.0,281,283),
 ('5h','4-fluoro-5-(piperidin-1-yl)benzene-1,2-diamine','Nc1cc(N2CCCCC2)c(F)cc1N','128-130 °C',129.0,128,130),
 ('5i','4-fluoro-5-(morpholin-4-yl)benzene-1,2-diamine','Nc1cc(N2CCOCC2)c(F)cc1N','127-128 °C',127.5,127,128),
 ('5j','2-(4-(4,5-diamino-2-fluorophenyl)piperazin-1-yl)ethanol','Nc1cc(N2CCN(CCO)CC2)c(F)cc1N','115-117 °C',116.0,115,117),
]
for code,name,smi,raw,mid,lo,hi in cmpds_5:
    new_rows.append(make_row(name,smi,'melting_point',mid,lo,hi,raw,'=','measured',SRC_068,URL_068,
        f'Section 3.1.5, compound {code}',f'{name} ... M.P.: {raw}','',''))

cmpds_6=[
 ('6a','6-fluoro-5-(piperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCNCC1','234-236 °C',235.0,234,236),
 ('6b','6-fluoro-5-(4-methylpiperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCN(C)CC1','118-120 °C',119.0,118,120),
 ('6c','6-fluoro-5-(4-ethylpiperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCN(CC)CC1','138-139 °C',138.5,138,139),
 ('6d','6-fluoro-5-(4-isopropylpiperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCN(C(C)C)CC1','147-149 °C',148.0,147,149),
 ('6e','6-fluoro-5-(4-butylpiperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCN(CCCC)CC1','140-142 °C',141.0,140,142),
 ('6f','6-fluoro-5-(4-phenylpiperazin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCN(c2ccccc2)CC1','130-132 °C',131.0,130,132),
 ('6g','6-fluoro-5-(pyrrolidin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCCC1','190-192 °C',191.0,190,192),
 ('6h','6-fluoro-5-(piperidin-1-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCCCC1','168-170 °C',169.0,168,170),
 ('6i','6-fluoro-5-(morpholin-4-yl)-1H-benzo[d]imidazole','Fc1cc2[nH]cnc2cc1N1CCOCC1','209-211 °C',210.0,209,211),
 ('6j','2-(4-(6-fluoro-1H-benzo[d]imidazol-5-yl)piperazin-1-yl)ethanol','Fc1cc2[nH]cnc2cc1N1CCN(CCO)CC1','120-122 °C',121.0,120,122),
]
for code,name,smi,raw,mid,lo,hi in cmpds_6:
    new_rows.append(make_row(name,smi,'melting_point',mid,lo,hi,raw,'=','measured',SRC_068,URL_068,
        f'Section 3.1.6, compound {code}',f'{name} ... M.P.: {raw}','',''))

all_rows = existing_rows + new_rows
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=HEADER, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(all_rows)

print(f'Total rows written: {len(all_rows)}')
print(f'New rows added: {len(new_rows)}')
print(f'  Paper 062 (Table 5): 58 boiling points')
print(f'  Paper 064 (Table 5 cited): 9 melting points')
print(f'  Paper 068 (synthesis): {len(new_rows) - 58 - 9} melting points')

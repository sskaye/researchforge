with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/059_PMC8122861_Group_Contribution_Estimation_of_Ionic_Liquid_Melting_Points_Critical_Evaluation_and_Refin/article_text.txt') as f:
    t = f.read()
import re
print('len:', len(t))
# Find specific compound-mp pairs
for pat, name in [(r'\[[A-Za-z0-9_+-]+\]\[[A-Za-z0-9_+-]+\][^.]{0,100}', 'IL_cation_anion'),
                  (r'Tm\s*=\s*\d', 'Tm_eq'),
                  (r'melting point of [^.]{0,200}', 'mp_of'),
                  (r'\d+\.?\d* K', 'kelvin')]:
    hits = list(re.finditer(pat, t))
    print(f"\n=== {name} ({len(hits)} hits) ===")
    seen = set()
    for m in hits[:10]:
        if m.group() in seen: continue
        seen.add(m.group())
        print(repr(t[max(0, m.start()-50):m.end()+50]))

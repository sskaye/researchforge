with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/058_PMC4702524_How_accurately_can_we_predict_the_melting_points_of_drug-like_compounds/article_text.txt') as f:
    t = f.read()
import re
print('=== celsius temperatures with context ===')
seen = set()
for m in re.finditer(r'\d+(?:\.\d+)?\s*°C', t):
    if m.group() in seen: continue
    seen.add(m.group())
    print(repr(t[max(0, m.start()-150):m.end()+30]))
    print()

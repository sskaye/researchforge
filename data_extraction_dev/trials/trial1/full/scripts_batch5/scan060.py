with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/060_PMC4724158_The_development_of_models_to_predict_melting_and_pyrolysis_point_data_associated_with_seve/article_text.txt') as f:
    t = f.read()
import re
print('=== "MP = X" context ===')
for m in re.finditer(r'MP\s*=\s*\d+(?:\.\d+)?\s*°?C[^.]{0,100}', t):
    print(repr(t[max(0, m.start()-200):m.end()+50]))
    print()
print('=== celsius temps with context (first 25) ===')
seen=set()
for m in re.finditer(r'\d+(?:\.\d+)?\s*°C', t):
    if m.group() in seen: continue
    seen.add(m.group())
    if len(seen)>25: break
    print(repr(t[max(0, m.start()-100):m.end()+30]))
    print()

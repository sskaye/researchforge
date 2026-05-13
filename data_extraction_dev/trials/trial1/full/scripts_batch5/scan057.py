with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/057_PMC12573032_Prioritizing_Data_Quality_in_Machine_Learning_for_Thermophysical_Property_Prediction_A_Cas/article_text.txt') as f:
    t = f.read()
import re
print('=== "K" temperatures with context ===')
for m in re.finditer(r'(\d+\.?\d*)\s*K\b', t):
    print(repr(t[max(0, m.start()-100):m.end()+30]))
    print()
print('=== boiling point context ===')
for m in re.finditer(r'boiling point[^.]{0,300}', t):
    print(repr(m.group()))
    print()

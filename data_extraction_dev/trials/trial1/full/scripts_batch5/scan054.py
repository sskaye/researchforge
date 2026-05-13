with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/054_PMC6146489_Michael_Reactions_of_Arylidenesulfonylacetonitriles._A_New_Route_to_Polyfunctional_Benzoaq/article_text.txt') as f:
    t = f.read()
import re
for m in re.finditer(r'mp\s*[0-9][0-9]', t):
    print(repr(t[max(0,m.start()-80):m.end()+150]))
print('---')
print('chars total', len(t))
# look for compound start patterns and mp following
for m in re.finditer(r'mp[^.]{0,100}', t):
    print(repr(m.group()))

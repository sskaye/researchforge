with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/055_PMC3685236_Antiproliferative_Activity_of_-Hydroxy--Arylalkanoic_Acids/article_text.txt') as f:
    t = f.read()
import re
for i, m in enumerate(re.finditer(r'Melting point[^;]*', t)):
    s = t[max(0, m.start()-600):m.start()]
    # Find the most likely compound name preceding (usually heading "3.1.X. <name>")
    print('---', i+1, '---')
    print('PRE:', repr(s[-300:]))
    print('MATCH:', repr(m.group()))

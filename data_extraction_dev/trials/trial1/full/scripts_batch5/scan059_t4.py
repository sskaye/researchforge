with open('/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/059_PMC8122861_Group_Contribution_Estimation_of_Ionic_Liquid_Melting_Points_Critical_Evaluation_and_Refin/article_text.txt') as f:
    t = f.read()
import re
# Find Table 4 context
idx = t.find('Table 4')
print('Table 4 first occurrence at:', idx)
print(t[idx:idx+3000])

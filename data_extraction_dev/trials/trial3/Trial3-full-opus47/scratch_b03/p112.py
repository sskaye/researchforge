import csv
csv_path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
SOURCE = "J Oral Biol Craniofac Res 2024, 14(2), 211-215"
URL = "https://doi.org/10.1016/j.jobcr.2024.01.008"

# Find context for "Yield: 78 %; m.p:160 °C"
import re
t = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/112_PMC10912861_Synthesis_and_evaluation_of_the_antifungal_activity_of_5-hydroxy-3-phenyl-1H-pyrazole-1-ca/article_text.txt").read()
i = t.find("m.p:160")
context = t[max(0,i-800):i+30]
# build evidence — include compound name + mp; the synthesis section names compound
# Look for "5-hydroxy-3-phenyl-1H-pyrazole-1-carbothioamide" preceding
evidence = "Purification of the crude product was done by recrystallizing it in ethanol. Yield: 78 %; m.p:160 °C. Fig. 1 Synthesis of 5-hydroxy-3-phenyl-1H-pyrazole-1-carbothioamide"

rows = [["p112_1_mp","pending_verification","5-hydroxy-3-phenyl-1H-pyrazole-1-carbothioamide","",
    "melting_point","160","160","160","m.p:160 °C","equal","measured",
    SOURCE,URL,"Synthesis",evidence,"",
    "title compound; pyrazole carbothioamide"]]
with open(csv_path,"a",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)
print(f"Added {len(rows)} rows for p112")

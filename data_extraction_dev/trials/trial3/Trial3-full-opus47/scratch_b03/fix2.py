import csv
path = "/sessions/happy-brave-tesla/mnt/data_extraction_dev/Trial3-full-opus47/batch_03.csv"
t102 = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/102_PMC6236359_Synthesis_and_Electrophilic_Substitution_of_Pyrido234-kl-_acridines/article_text.txt").read()
t103 = open("/sessions/happy-brave-tesla/mnt/data_extraction_dev/corpora/full_168/103_PMC6146533_A_Simple_Synthesis_of_Some_New_Thienopyridine_and_Thieno-pyrimidine_Derivatives/article_text.txt").read()

with open(path) as f:
    rows = list(csv.reader(f))
header = rows[0]
i_q = header.index("evidence_quote")
i_id = header.index("id")

def grab(text, start_str, end_str):
    s = text.find(start_str)
    if s<0: return None
    e = text.find(end_str, s)
    if e<0: return None
    return text[s:e+len(end_str)]

new_quotes = {
    "p102_6a_mp": grab(t102, "H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 6a )", "m.p. 255°C"),
    "p102_8_mp": grab(t102, "H-benzo[i]pyrido[2,3,4-kl]acridin-9-one ( 8 )", "mp 258°C"),
    "p102_9_mp": grab(t102, "3(N)-(2,2’-diaminobenzophenone)-5-hydroxy-1,4-naphthoquinone ( 9 )", "m.p. 221°C"),
    "p102_10_mp": grab(t102, "Hydroxy-10H-benzo[i]quino[2,3,4-kl]acridin-10-one ( 10 )", "m.p. 292°C"),
    "p102_14_mp": grab(t102, "N-(4-methoxyaniline)-5-hydroxy-1,4-naphthoquinone ( 14 )", "m.p. 211°C"),
    # p103_18_mp had "( 18 )...To a solution" — get contiguous text
    "p103_18_mp": grab(t103, "7-(4,5-Dihydro-1H-2-imidazolyl)-2,3-dihydro-8- phenylaminoimidazo[1,2-c]thieno[2,3-e][1,2,3]-triazine ( 18 )", "m.p. 269 o C"),
}
for r in rows[1:]:
    if r[i_id] in new_quotes and new_quotes[r[i_id]]:
        r[i_q] = new_quotes[r[i_id]]
        print(f"Fixed {r[i_id]} (len {len(r[i_q])})")
with open(path, "w", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows: w.writerow(r)

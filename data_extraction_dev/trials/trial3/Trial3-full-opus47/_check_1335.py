import sys
sys.path.insert(0,'/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/Trial3-full-opus47')
from _verify_all_b8 import normalize, read_paper_text
folder = 'corpora/full_168/2019_Rubstov_One-pot synthesis of thieno[3,2-e]pyrrolo[1,2-a]pyrimidine derivatives scaffold - A valuable source of PARP-1 inhibitors.pdf'
text = read_paper_text(folder)
n_text = normalize(text)
quote = 'Yellow solid; 1.80 g, 89 % yield; m.p.\n209-210 °С (acetonitrile)'
n_quote = normalize(quote)
print('found:', n_quote in n_text)
print('quote:', repr(n_quote))
idx = n_text.find('1.80 g')
print('text snip:', repr(n_text[max(0,idx-50):idx+300]))

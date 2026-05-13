import csv
OUT='/sessions/practical-gifted-babbage/mnt/data_extraction_dev/Trial2-full-opus47/batches/batch_pmc_02_results.csv'
SOURCES = {
    "036": ("Synthesis (Stuttg). 2017; 49(12):2753-2760", "https://doi.org/10.1055/s-0036-1589496"),
    "037": ("Molecules. 2011; 16(10):8788-8802", "pmc:PMC6264548"),
    "038": ("Molecules. 2011; 16(10):8758-8774", "pmc:PMC6264341"),
    "039": ("Molecules. 2011; 16(5):4059-4069", "pmc:PMC6263281"),
    "040": ("Molecules. 2003; 8(3):342-349", "pmc:PMC6146956"),
    "041": ("Molecules. 2002; 7(2):239-244", "pmc:PMC6146472"),
    "042": ("Molecules. 2002; 7(7):507-510", "pmc:PMC6146455"),
    "043": ("Molecules. 2003; 8(3):310-317", "pmc:PMC6146928"),
    "044": ("Molecules. 2003; 8(5):453-458", "pmc:PMC6147016"),
    "045": ("Molecules. 2011; 16(10):8815-8832", "pmc:PMC6264237"),
    "046": ("Molecules. 2001; 6(12):1001-1005", "pmc:PMC6236381"),
    "047": ("Molecules. 2002; 7(7):534-539", "pmc:PMC6146789"),
    "049": ("Molecules. 2003; 8(5):444-452", "pmc:PMC6147017"),
    "050": ("Molecules. 2003; 8(11):756-769", "pmc:PMC6146942"),
    "051": ("Molecules. 2001; 6(9):728-735", "pmc:PMC6236391"),
    "052": ("Int J Mol Sci. 2007; 8(8):760-776", "pmc:PMC3715800"),
}
rows=[]
def add(name,prop,c,cmin,cmax,raw,rel,dt,P,loc,quote,conv="",notes="",smi=""):
    s,u=SOURCES[P]
    rows.append(["","pending_verification",name,smi,prop,c,cmin,cmax,raw,rel,dt,s,u,loc,quote,conv,notes])

P="036"
add("7-(Cyanomethyl)-1H-pyrrolo[2,3-b]pyridin-7-ium chloride","melting_point","203","","","203 °C","eq","measured",P,"Experimental, compound 1a","mp 203 °С","","Cyrillic С in source")
add("7-(Cyanomethyl)-1-methyl-1H-pyrrolo[2,3-b]pyridin-7-ium bromide","melting_point","194","","","194 °C","eq","measured",P,"Experimental, compound 1b","mp 194 °С","","")
add("3-(7H-Pyrrolo[2,3-b]pyridin-7-yl)-2H-chromen-2-one","decomposition","142","","","142 °C (dec)","eq","measured",P,"Experimental, compound 4a","mp 142 °С (dec)","","")
add("6-Bromo-3-(7H-pyrrolo[2,3-b]pyridin-7-yl)-2H-chromen-2-one","decomposition","240","","","240 °C (dec)","eq","measured",P,"Experimental, compound 4b","mp 240 °С (dec)","","")
add("6-Methoxy-3-(7H-pyrrolo[2,3-b]pyridin-7-yl)-2H-chromen-2-one","decomposition","150","","","150 °C (dec)","eq","measured",P,"Experimental, compound 4c","mp 150 °С (dec)","","")
add("1-Methyl-7-(2-oxo-2H-chromen-3-yl)-1H-pyrrolo[2,3-b]pyridin-7-ium bromide","decomposition","179","","","179 °C (dec)","eq","measured",P,"Experimental, compound 5a","mp 179 °С (dec)","","")
add("7-(6-Bromo-2-oxo-2H-chromen-3-yl)-1-methyl-1H-pyrrolo[2,3-b]pyridin-7-ium bromide","decomposition","125","","","125 °C (dec)","eq","measured",P,"Experimental, compound 5b","mp 125 °С (dec)","","")
add("1-Methyl-7-(3-oxo-3H-benzo[f]chromen-2-yl)-1H-pyrrolo[2,3-b]pyridin-7-ium bromide","decomposition","176","","","176 °C (dec)","eq","measured",P,"Experimental, compound 5c","mp 176 °С (dec)","","")
add("7-(6,8-Dichloro-2-oxo-2H-chromen-3-yl)-1-methyl-1H-pyrrolo[2,3-b]pyridin-7-ium bromide","decomposition","118","","","118 °C (dec)","eq","measured",P,"Experimental, compound 5d","mp 118 °С (dec)","","")
add("1-Methyl-1,12-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-e]pyridine","melting_point","148","","","148 °C","eq","measured",P,"Experimental, compound 6a","mp 148 °С","","")
add("10-Methoxy-1-methyl-1,12-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-e]pyridine","melting_point","188","","","188 °C","eq","measured",P,"Experimental, compound 6b","mp 188 °С","","")
add("8-Ethoxy-1-methyl-1,12-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-e]pyridine","melting_point","149","","","149 °C","eq","measured",P,"Experimental, compound 6c","mp 149 °С","","")
add("5-(Cyanomethyl)-1H-pyrrolo[3,2-c]pyridin-5-ium chloride","melting_point","213","212","214","212–214 °C","range","measured",P,"Experimental, compound 2","mp 212–214 °С","","")
add("4-(Cyanomethyl)-1H-pyrrolo[3,2-b]pyridin-4-ium chloride","melting_point","227","226","228","226–228 °C","range","measured",P,"Experimental, compound 3","mp 226–228 °С","","")
add("3,7-Dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-c]pyridine","decomposition","277","276","278","276–278 °C (dec)","range","measured",P,"Experimental, compound 7a","mp 276–278 °С (dec)","","")
add("9-Bromo-3,7-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-c]pyridine","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 7b","mp >300 °C","","")
add("9-Methoxy-3,7-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-c]pyridine","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 7c","mp >300 °С","","")
add("3,7-Dihydrobenzo[5',6']chromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-c]pyridine","decomposition","294.5","293","296","293–296 °C (dec)","range","measured",P,"Experimental, compound 7d","mp 293–296 °С (dec)","","")
add("11-Ethoxy-3,7-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[3,2-c]pyridine","decomposition","301.5","299","304","299–304 °C (dec)","range","measured",P,"Experimental, compound 7e","mp 299–304 °С (dec)","","")
add("3,12-Dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[2,3-e]pyridine","decomposition","281.5","280","283","280–283 °C (dec)","range","measured",P,"Experimental, compound 8a","mp 280–283 °С (dec)","","")
add("10-Bromo-3,12-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[2,3-e]pyridine","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 8b","mp >300 °С","","")
add("10-Methoxy-3,12-dihydrochromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[2,3-e]pyridine","decomposition","274.5","273","276","273–276 °C (dec)","range","measured",P,"Experimental, compound 8c","mp 273–276 °С (dec)","","")
add("3,14-Dihydrobenzo[5',6']chromeno[2',3':4,5]imidazo[1,2-a]pyrrolo[2,3-e]pyridine","decomposition","274.5","273","276","273–276 °C (dec)","range","measured",P,"Experimental, compound 8d","mp 273–276 °С (dec)","","")

P="037"
add("6-Amino-2-(benzylsulfanyl)-5-nitrosopyrimidin-4-one","melting_point","198","","","198 °C","eq","measured",P,"Experimental, compound 3","mp 198 °C","","")
add("5,6-Diamino-2-(benzylsulfanyl)pyrimidin-4-one","melting_point","244","","","244 °C","eq","measured",P,"Experimental, compound 4","mp 244 °C","","")
add("2-(Benzylsulfanyl)-7H-purin-6-one","melting_point","260","","","260 °C","eq","measured",P,"Experimental, compound 5","mp = 260 °C","","")
for code,name in [
    ("6a","2-(Benzylsulfanyl)-8-[(4-methoxyphenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6b","2-(Benzylsulfanyl)-8-[(4-methylphenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6c","2-(Benzylsulfanyl)-8-[(3-methylphenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6d","2-(Benzylsulfanyl)-8-(phenylhydrazono)-1,8-dihydropurin-6-one"),
    ("6e","2-(Benzylsulfanyl)-8-[(4-chlorophenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6f","2-(Benzylsulfanyl)-8-[(3-chlorophenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6g","2-(Benzylsulfanyl)-8-[(4-bromophenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6h","2-(Benzylsulfanyl)-8-[(2-nitrophenyl)hydrazono]-1,8-dihydropurin-6-one"),
    ("6i","2-(Benzylsulfanyl)-8-[(4-nitrophenyl)hydrazono]-1,8-dihydropurin-6-one"),
]:
    add(name,"melting_point","300","","",">300 °C","gt","measured",P,f"Experimental, compound {code}","mp > 300 °C","","")

P="038"
m038=[("5-(But-3-ynylthio)-5'-(methylthio)-2,2'-bithiophene","6b","69","68","70","68–70 °C"),
("5-(2-Azidoethylthio)-5'-(methylthio)-2,2'-bithiophene","7a","45","44","46","44–46 °C"),
("S-8-(4-((5'-(Methylthio)-2,2'-bithiophen-5-ylthio)methyl)-1H-1,2,3-triazol-1-yl)octyl thioacetate","4a","86","85","87","85–87 °C"),
("S-8-(4-(2-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-1-yl)octyl thioacetate","4b","86","85","87","85–87 °C"),
("S-8-(4-(3-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-1-yl)octyl thioacetate","4c","85","84","86","84–86 °C"),
("S-8-(1-(2-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-4-yl)octyl thioacetate","5a","81","80","82","80–82 °C"),
("S-8-(1-(3-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-4-yl)octyl thioacetate","5b","81","80","82","80–82 °C"),
("8-(4-((5'-(Methylthio)-2,2'-bithiophen-5-ylthio)methyl)-1H-1,2,3-triazol-1-yl)octane-1-thiol","2a","81","80","82","80–82 °C"),
("8-(4-(2-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-1-yl)octane-1-thiol","2b","80","79","81","79–81 °C"),
("8-(4-(3-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-1-yl)octane-1-thiol","2c","77","76","78","76–78 °C"),
("8-(1-(2-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-4-yl)octane-1-thiol","3a","77","76","78","76–78 °C"),
("8-(1-(3-(5'-(Methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-4-yl)octane-1-thiol","3b","75","74","76","74–76 °C"),
("1,2-Bis(8-(4-((5'-(methylthio)-2,2'-bithiophen-5-ylthio)methyl)-1H-1,2,3-triazol-1-yl)octyl)disulfide","11a","123","122","124","122–124 °C"),
("1,2-Bis(8-(4-(2-(5'-(methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-1-yl)octyl)disulfide","11b","119","118","120","118–120 °C"),
("1,2-Bis(8-(4-(3-(5'-(methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-1-yl)octyl)disulfide","11c","119","118","120","118–120 °C"),
("1,2-Bis(8-(1-(2-(5'-(methylthio)-2,2'-bithiophen-5-ylthio)ethyl)-1H-1,2,3-triazol-4-yl)octyl)disulfide","12a","126","125","127","125–127 °C"),
("1,2-Bis(8-(1-(3-(5'-(methylthio)-2,2'-bithiophen-5-ylthio)propyl)-1H-1,2,3-triazol-4-yl)octyl)disulfide","12b","120","119","121","119–121 °C")]
for nm,c,vc,vmn,vmx,r in m038:
    add(nm,"melting_point",vc,vmn,vmx,r,"range","measured",P,f"Experimental, compound {c}",f"mp: {r}","","")

P="039"
m039=[("Ethyl 6-methylsalicylate","1","43.5","43","44","43–44 °C","Mp: 43–44 °C"),
("(Z)-6-(1-Pentenyl)salicylic acid","8a","85.5","85","86","85–86 °C","Mp 85–86 °C"),
("(E)-6-(1-Pentenyl)salicylic acid","9a","97","96","98","96–98 °C","Mp 96–98 °C"),
("(Z)-6-(1-Heptenyl)salicylic acid","8b","55.5","55","56","55–56 °C","Mp 55–56 °C"),
("(E)-6-(1-Heptenyl)salicylic acid","9b","71","70","72","70–72 °C","Mp 70–72 °C"),
("(Z)-6-(1-Nonenyl)salicylic acid","8c","41","40","42","40–42 °C","Mp 40–42 °C"),
("(E)-6-(1-Nonenyl)salicylic acid","9c","76","75","77","75–77 °C","Mp 75–77 °C"),
("(Z)-6-(1-Undecenyl)salicylic acid","8d","48","47","49","47–49 °C","Mp 47–49 °C"),
("(E)-6-(1-Undecenyl)salicylic acid","9d","80","79","81","79–81 °C","Mp 79–81 °C"),
("(Z)-6-(1-Dodecenyl)salicylic acid","8e","53","52","54","52–54 °C","Mp 52–54 °C"),
("(E)-6-(1-Dodecenyl)salicylic acid","9e","83","82","84","82–84 °C","Mp 82–84 °C"),
("(Z)-6-(1-Tridecenyl)salicylic acid","8f","56","55","57","55–57 °C","Mp 55–57 °C"),
("(E)-6-(1-Tridecenyl)salicylic acid","9f","91","90","92","90–92 °C","Mp 90–92 °C"),
("(Z)-6-Phenylethylenyl salicylic acid","8g","85","84","86","84–86 °C","Mp 84–86 °C"),
("(E)-6-Phenylethylenyl salicylic acid","9g","131","130","132","130–132 °C","Mp 130–132 °C")]
for nm,c,vc,vmn,vmx,r,q in m039:
    add(nm,"melting_point",vc,vmn,vmx,r,"range","measured",P,f"Experimental, compound {c}",q,"","")

P="040"
add("5-(4-Carboxyphenyl)-2-thiophenecarboxylic acid","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 2b","m.p.: >300 °C","","")
add("2-(4-Carboxyphenyl)-5-(6-cyanobenzothiazol-2-yl)furan","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 3a","m.p.>300°C","","")
add("2-(4-Carboxyphenyl)-5-(6-cyanobenzothiazol-2-yl)thiophene","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 3b","m.p.>300°C","","")
add("2-(4-Chlorocarbonylphenyl)-5-(6-cyanobenzothiazol-2-yl)furan","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 4a","m.p.>300°C","","")
add("2-(4-Chlorocarbonylphenyl)-5-(6-cyanobenzothiazol-2-yl)thiophene","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 4b","m.p.>300°C","","")
add("2-(4-Chlorocarbonylphenyl)-5-chlorocarbonylfuran","melting_point","104","102","106","102–106 °C","range","measured",P,"Experimental, compound 5a","m.p.102-106 °C","","")
add("2-(4-Chlorocarbonylphenyl)-5-chlorocarbonylthiophene","melting_point","90","88","92","88–92 °C","range","measured",P,"Experimental, compound 5b","m.p.88-92 °C","","")
add("2-[4-(6-Cyanobenzothiazol-2-yl)phenyl]-5-(6-cyanobenzothiazol-2-yl)furan","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 6a","m.p.>300°C","","")
add("2-[4-(6-Cyanobenzothiazol-2-yl)phenyl]-5-(6-cyanobenzothiazol-2-yl)thiophene","melting_point","300","","",">300 °C","gt","measured",P,"Experimental, compound 6b","m.p.>300°C","","")

P="041"
add("3,5-Di(N-phthalimidoxymethyl)-2,6-diphenyl-4H-pyran-4-one","melting_point","234","233","235","233–235 °C","range","measured",P,"Experimental, compound 2a","m.p. 233-235°C","","")
add("2,6-Di(N-phthalimidoxymethyl)-3,5-diphenyl-4H-pyran-4-one","melting_point","228.75","228","229.5","228–229.5 °C","range","measured",P,"Experimental, compound 2b","m.p. 228-229.5°C","","")
add("3,5-Di(aminoxymethyl)-2,6-diphenyl-4H-pyran-4-one","melting_point","128","127","129","127–129 °C","range","measured",P,"Experimental, compound 3a","m.p. 127-129°C","","")
add("2,6-Di(aminoxymethyl)-3,5-diphenyl-4H-pyran-4-one","melting_point","132.25","131.5","133","131.5–133 °C","range","measured",P,"Experimental, compound 3b","m.p. 131.5-133°C","","")
add("(E,E)-4-Methylbenzal[(2,6-diphenyl-3,5-4H-pyran-4-one-diyl)bis(methylene)]dioxime","melting_point","128","","","128 °C","eq","measured",P,"Experimental, compound 6a","m.p. 128°C","","")
add("(E,Z)-4-Methylbenzal[(2,6-diphenyl-3,5-4H-pyran-4-one-diyl)bis(methylene)]dioxime","melting_point","138","","","138 °C","eq","measured",P,"Experimental, compound 7a","m.p. 138°C","","")

P="042"
add("Dimethyl 2,4-diphenylquinazoline-6,7-dicarboxylate","melting_point","157","156","158","156–158 °C","range","measured",P,"Experimental, compound 6","mp (from hexane): 156-158 °C","","")
add("2,4-Diphenylfuro[3,4-g]quinazoline-6,8-dione","melting_point","281","280","282","280–282 °C","range","measured",P,"Experimental, compound 7","mp (from acetic anhydride): 280- 282 °C","","")

P="043"
add("5,5'-Bis(methylthio)-2,2'-bi-1,3,4-thiadiazole","melting_point","177.5","177","178","177–178 °C","range","measured",P,"Experimental section, bis(methylthio) derivative","mp. 177-178 °C","","")
add("5-Mercapto-5'-(methylthio)-2,2'-bi-1,3,4-thiadiazole","decomposition","225","","","225 °C (dec)","eq","measured",P,"Experimental section, yellow needles from filtrate","mp 225 °C (dec.)","","")

P="044"
add("7,10-Cyclooxalamide-N,N'-bis-(phenyl-2-ylmethylene)-cyclohexane-1R,2R-diamine","decomposition","224","223","225","223–225 °C (dec)","range","measured",P,"Experimental, compound 2","mp = 223-225 °C (dec.)","","")
add("7,10-Cyclodicarbonic-diamide-N,N'-bis-(phenyl-2-ylmethylene)-cyclohexane-1R,2R-diamine","decomposition","254","253","255","253–255 °C (dec)","range","measured",P,"Experimental, compound 3","mp = 253-255 °C (dec.)","","")

P="045"
m045=[("(1R)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-valine methyl ester","4a","119","","","119 °C","eq"),
("(1R)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-leucine methyl ester","4b","140","139","141","139–141 °C","range"),
("(1R)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-t-leucine methyl ester","4c","165.5","165","166","165–166 °C","range"),
("(1R)-N-(1-(N-tert-butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-isoleucine methyl ester","4d","98.5","97","100","97–100 °C","range"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-phenylalanine methyl ester","4e","128.5","128","129","128–129 °C","range"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-phenylglycine methyl ester","4f","147.5","146","149","146–149 °C","range"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-serine methyl ester","4g","121","","","121 °C","eq"),
("(1R)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-methionine methyl ester","4h","99","98","100","98–100 °C","range"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) O-t-butyl L-threonine methyl ester","4i","136","","","136 °C","eq"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) L-glutamic acid dimethyl ester","4j","89.5","89","90","89–90 °C","range"),
("(1SR)-Benzyl N-(1-(N-tert-butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-aspartic acid methyl ester","4k","105","","","105 °C","eq"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) O-benzyl L-serine methyl ester","4l","145","","","145 °C","eq"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-histidine methyl ester","4m","111.5","110","113","110–113 °C","range"),
("(1SR)-N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-proline methyl ester","4o","107","105","109","105–109 °C","range")]
for nm,c,vc,vmn,vmx,r,rel in m045:
    add(nm,"melting_point",vc,vmn,vmx,r,rel,"measured",P,f"Experimental, compound {c}",f"m.p. {r}","","")

P="046"
add("2-Hydroxy-3-hydroxymethyl-5-methylbenzaldehyde","melting_point","72.5","72","73","72–73 °C","range","measured",P,"Experimental, compound 5","M.p. 72-73° (lit. [ 7 ] 75-76°C)","","Lit: 75-76°C")
add("2-Hydroxy-3-chloromethyl-5-methylbenzaldehyde","melting_point","92.5","92","93","92–93 °C","range","measured",P,"Experimental, compound 6","m.p. 92-93°C","","")
add("1,6-Bis(2-furyl)-2,5-bis(2-hydroxy-3-formyl-5-methylbenzyl)-2,5-diazahexane","melting_point","109.5","109","110","109–110 °C","range","measured",P,"Experimental, compound 3","m.p. 109-110°C","","")

P="047"
add("2-(Bromomethyl)benzothiazole","decomposition","82","","","82 °C (decomp)","eq","measured",P,"Experimental, compound 1","m.p. 82°C (decomp.)","","")
add("6,13-Dihydropyrazino[2,1-b:5,4-b']bis(1,3-benzothiazole)-7,14-diiumdibromide","decomposition","115","","","115 °C (decomp)","eq","measured",P,"Experimental, compound 2","m.p.115°C (decomp.)","","")

P="049"
add("3β-Acetoxy-16-[bis(methylthio)methylene]androst-5-en-17-one","melting_point","166.85","165.7","168.0","165.7–168.0 °C","range","measured",P,"Experimental, compound 2","mp: 165.7–168.0 °C","","")
add("5'-Methylthio-pyrazolo[4',3':16,17]androst-5-en-3β-ol","melting_point","177.1","176.2","178.0","176.2–178.0 °C","range","measured",P,"Experimental, compound 3a","mp (ethanol): 176.2–178.0 °C","","")
add("1'-Methyl-5'-methylthio-pyrazolo[4',3':16,17]androst-5-en-3β-ol","melting_point","182","181","183","181–183 °C","range","measured",P,"Experimental, compound 3b","mp (ethanol): 181–183 °C","","")
add("6'-Methoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol","melting_point","179","178","180","178–180 °C","range","measured",P,"Experimental, compound 4a","mp (acetone): 178–180 °C","","")
add("6'-Methoxy-2'-methyl-pyrimido[5',4':16,17]androst-5-en-3β-ol","melting_point","211","210","212","210–212 °C","range","measured",P,"Experimental, compound 4b","mp (acetone): 210–212 °C","","")
add("6'-Methoxy-2'-phenyl-pyrimido[5',4':16,17-c]androst-5-en-3β-ol","melting_point","242","241","243","241–243 °C","range","measured",P,"Experimental, compound 4c","mp (acetone): 241–243 °C","","")
add("2'-Amino-6'-methoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol","melting_point","219.5","218","221","218–221 °C","range","measured",P,"Experimental, compound 4d","mp (acetone): 218–221 °C","","")
add("2',6'-Dimethoxy-pyrimido[5',4':16,17]androst-5-en-3β-ol","melting_point","215","214","216","214–216 °C","range","measured",P,"Experimental, compound 4e","mp (acetone): 214–216° C","","")

P="050"
def fR(r):
    return {"H":"H","4-Cl":"4-chloro","3,4-Cl 2":"3,4-dichloro","4-CH 3":"4-methyl","4-C 2 H 5":"4-ethyl","4-isoC 3 H 7":"4-isopropyl","3-Cl":"3-chloro","4-C 4 H 9":"4-butyl","4-Br":"4-bromo","4-OCH 3":"4-methoxy"}.get(r,r)
def qn(series,X,R):
    Rfmt=fR(R)
    pref="6-Chloro-" if X=="Cl" else ""
    phenyl="3-phenyl" if Rfmt=="H" else f"3-({Rfmt}phenyl)"
    if series==1:
        return f"{pref}2,2-dimethyl-{phenyl}-1,2-dihydroquinazoline-4(3H)-thione"
    else:
        return f"{pref}2-methyl-{phenyl}quinazoline-4(3H)-thione"

t050=[("1a","H","H","212","214"),("1b","H","4-Cl","238","241"),("1c","H","3,4-Cl 2","199","201"),
("1d","H","4-CH 3","229","231"),("1e","H","4-C 2 H 5","187","188"),("1f","H","4-isoC 3 H 7","199","200"),
("1g","Cl","H","218","219"),("1h","Cl","3-Cl","157","158"),("1i","Cl","3,4-Cl 2","189","190"),
("1j","Cl","4-isoC 3 H 7","205","207"),("1k","Cl","4-C 4 H 9","183","184"),
("2a","Cl","H","153","154"),("2b","Cl","3-Cl","172","173"),("2c","Cl","4-Cl","202","204"),
("2d","Cl","4-Br","212","214"),("2e","Cl","4-CH 3","157","158"),("2f","Cl","4-isoC 3 H 7","135","136"),
("2g","Cl","4-OCH 3","145","146")]
for code,X,R,vmn,vmx in t050:
    series=1 if code.startswith("1") else 2
    name=qn(series,X,R)
    c=str((int(vmn)+int(vmx))/2)
    raw=f"{vmn}-{vmx} °C"
    quote=f"{code} ... {vmn}-{vmx}"
    add(name,"melting_point",c,vmn,vmx,raw,"range","measured",P,f"Table 1, compound {code}",quote,"",f"Table 1: X={X}, R={R}")

P="051"
add("2-Deoxy-2-(2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside","melting_point","209","208","210","208–210 °C","range","measured",P,"Experimental, compound 6","m p 208-210 °C","","")
add("2-Deoxy-2-(5-nitro-2-furamido)-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside","melting_point","110","109","111","109–111 °C","range","measured",P,"Experimental, compound 7","m p 109-111 °C","","")
add("2-Deoxy-2-(furfural)-imino-1,3,4,6-tetra-O-acetyl-β-D-glucopyranoside","melting_point","115","114","116","114–116 °C","range","measured",P,"Experimental, compound 8","m p 114-116 °C","","")
add("1-Deoxy-1-(5-nitro-2-furamido)-2,3;4,5-di-O-isopropylidene-β-D-fructopyranoside","melting_point","160.5","159","162","159–162 °C","range","measured",P,"Experimental, compound 12","m p 159-162 °C","","")
add("(1R,2S,3R,5R)-1,2-O-Cyclohexylidene-5-C-[(O-tosyl)-hydroxymethyl]-cyclohexane-1,2,3,5-tetrol","melting_point","135","134","136","134–136 °C","range","measured",P,"Experimental, compound 14","m p 134-136 °C","","")
add("(1R,2S,3R,5R)-1,2-O-Cyclohexylidene-3-O-tosyl-5-C-[(O-tosyl)-hydroxy-methyl]-cyclohexane-1,2,3,5-tetrol","melting_point","125","124","126","124–126 °C","range","measured",P,"Experimental, compound 18","m p 124-126 °C (lit [ 13 ] m p 123-125 °C)","","Lit: 123-125 °C")

P="052"
add("2-(4-Methoxyphenyl)benzothiazole","melting_point","119.85","118.85","120.85","393 K (392–394 K)","range","measured",P,"Experimental section 3.1","M.p. 393 K (392–394 K)","393 K - 273.15 = 119.85 °C; 392 K = 118.85 °C; 394 K = 120.85 °C","Converted K to °C")

with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    w.writerow(["id","verification_status","compound_name","compound_smiles","property","value_celsius","value_celsius_min","value_celsius_max","value_raw","relation","data_type","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"])
    for i,r in enumerate(rows,1):
        r[0]=str(i)
        w.writerow(r)
print(f"Wrote {len(rows)} rows.")

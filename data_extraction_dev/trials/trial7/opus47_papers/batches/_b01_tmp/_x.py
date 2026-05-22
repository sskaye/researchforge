import csv, os
CSV_PATH = '/sessions/wizardly-beautiful-tesla/mnt/opus47_books/batches/batch_02.csv'
src044 = "Molecules 2003, 8, 453-458"
url044 = "https://doi.org/10.3390/80500453"
src045 = "Molecules 2011, 16, 8815-8835"
url045 = "https://doi.org/10.3390/molecules16108815"

rows = []
rows.append(["2000","pending_verification",
    "7,10-Cyclooxalamide-N,N´-bis-(phenyl-2-ylmethylene)-cyclohexane-1R,2R-diamine",
    "","melting_point","224.0","223.0","225.0","223-225 °C","°C","=","measured",
    src044, url044,"Synthesis of the ligands, characterization of compound 2",
    "the cyclic compound 2 (318 mg, 0.85 mmol, 68 %), mp = 223-225 °C (dec.)","","decomposes at mp"])
rows.append(["2001","pending_verification",
    "7,10-Cyclodicarbonic-diamide-N,N´-bis-(phenyl-2-ylmethylene)-cyclohexane-1R,2R-diamine",
    "","melting_point","254.0","253.0","255.0","253-255 °C","°C","=","measured",
    src044, url044,"Synthesis of the ligands, characterization of compound 3",
    "a colorless product (230 mg, 0.59 mmol, 38 %) was obtained, mp = 253-255 °C (dec.)","","decomposes at mp"])
rows.append(["2002","pending_verification",
    "7,10-Cyclodicarbonic-diamide-N,N´-bis-(phenyl-2-ylmethylene)-cyclohexane-1R,2R-diamine",
    "","decomposition","259.1","","","259.1 °C","°C","=","measured",
    src044, url044,"Note [9] / DSC analysis",
    "The reaction set in at 259.1 °C and the sample lost 0.818 mg in weight","","DSC decomposition with CO2 loss"])

p045 = [
    ("4a","(1R) N-(1-(N-tert-butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-valine methyl ester","119","119","",""),
    ("4b","(1R) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-leucine methyl ester","139-141","140.0","139","141"),
    ("4c","(1R) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-t-leucine methyl ester","165-166","165.5","165","166"),
    ("4d","(1R) N-(1-(N-tert-butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-isoleucine methyl ester","97-100","98.5","97","100"),
    ("4e","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-phenylalanine methyl ester","128-129","128.5","128","129"),
    ("4f","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-phenylglycine methyl ester","146-149","147.5","146","149"),
    ("4g","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-serine methyl ester","121","121","",""),
    ("4h","(1R) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-methionine methyl ester","98-100","99.0","98","100"),
    ("4i","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) O-t-butyl L-threonine methyl ester","136","136","",""),
    ("4j","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) L-glutamic acid dimethyl ester","89-90","89.5","89","90"),
    ("4k","(1SR)-Benzyl N-(1-(N-tert-butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-aspartic acid methyl ester","105","105","",""),
    ("4l","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl) O-benzyl L-serine methyl ester","145","145","",""),
    ("4m","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-histidine methyl ester","110-113","111.5","110","113"),
    ("4o","(1SR) N-(1-(N-tert-Butylcarbamoyl)-1-(4-(dimethylamino)pyridyn-3-yl)methyl)-L-proline methyl ester","105-109","107.0","105","109"),
]

quotes045 = {
    "4a":"colorless solid (99.7 mg, 55% yield, d.r. 92:8, Table 5 , entry 1). For the major diastereomer: m.p. 119 °C",
    "4b":"( 4b ): A colorless solid (118.6 mg, 63% yield, d.r. 86:14); For the major diastereomer: m.p. 139–141 °C",
    "4c":"( 4c ): A colorless solid (39.6 mg, 52% yield, d.r. 89:11); For the major diastereomer: m.p. 165–166 °C",
    "4d":"( 4d ): A colorless solid (104.3 mg, 55% yield, d.r. 93:7); For the major diastereomer: m.p. 97–100 °C",
    "4e":"( 4e ): A colorless solid (123.3 mg, 60% yield, d.r. 88:12); For mixture of two diastereomers: m.p. 128–129 °C",
    "4f":"( 4f ): A colorless solid (90.0 mg, 45% yield, d.r. 59:41); For mixture of two diastereomers: m.p. 146–149 °C",
    "4g":"( 4g ): A yellowish solid (76.2 mg, 43% yield, d.r. 77:23); For mixture of two diastereomers: m.p. 121 °C",
    "4h":"( 4h ): A colorless solid (115.0 mg, 58% yield, d.r. 83:17). For the major diastereomer: m.p. 98–100 °C",
    "4i":"( 4i ): A colorless solid (132.6 mg, 63% yield, d.r. 82:18); For mixture of two diastereomers: m.p. 136 °C",
    "4j":"( 4j ): A colorless solid (94.9 mg, 47% yield, d.r. 83:17); For the major diastereomer: m.p. 89–90 °C",
    "4k":"( 4k ): A colorless solid (122.5 mg, 52% yield, d.r. 79:21); For mixture of two diastereomers: m.p. 105 °C",
    "4l":"( 4l ): A colorless solid (120.2 mg, 54% yield, d.r. 75:25); For mixture of two diastereomers: m.p. 145 °C",
    "4m":"( 4m ): A colorless solid (88.1 mg, 44% yield, d.r. 77:23); For mixture of two diastereomers: m.p. 110–113 °C",
    "4o":"( 4o ): A yellowish solid (93.5 mg, 51% yield, d.r. 74:26); For mixture of two diastereomers: m.p. 105–109 °C",
}

next_id = 2003
for code, name, raw, val, vmin, vmax in p045:
    rows.append([str(next_id),"pending_verification",name,"","melting_point",val,vmin,vmax,
        raw + " °C","°C","=","measured",src045,url045,
        f"section 3.3 characterization of compound {code}",quotes045[code],"",""])
    next_id += 1

with open(CSV_PATH, 'a', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    for r in rows:
        assert len(r) == 18, f"row length {len(r)}"
        w.writerow(r)
print(f"wrote {len(rows)} rows, next id = {next_id}")

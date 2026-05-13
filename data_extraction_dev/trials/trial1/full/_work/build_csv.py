"""Build the final CSV with verified rows. Each row has verified evidence_quote."""
import csv, re, os

OUT = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/trial1-full/extracted_batch_6.csv'
BASE = '/sessions/practical-dreamy-pascal/mnt/data_extraction_dev/mp_bp_full_set/'

def get_dir(paper):
    for d in os.listdir(BASE):
        if d.startswith(paper + '_'):
            return BASE + d

# Verified rows. Each entry:
# (compound, property, value_raw, value_C, vmin, vmax, source_url, source, ev_loc, ev_quote, data_type, conv_arith, notes)

rows = []

# ---- Paper 064 (Nagar et al., 2022, Chem Data Collections, 37, 100820) ----
DOI064 = 'https://doi.org/10.1016/j.cdc.2021.100820'
SRC064 = 'Chemical Data Collections, 2022, 37, 100820'

# Table 5 has STRM Tm | SIRM Tm | [ref] literature Tm for 9 compounds (in K)
# Text confirms several with explicit "X K (STRM)" or "X K (SIRM)" patterns.
# Conservative: only emit rows where the text explicitly states the value with method label.

# Baricitinib STRM 492.478 K -> 219.328 °C (text-confirmed)
rows.append(('Baricitinib', 'melting_point', '492.478 K', 219.328, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'The estimated T m for the Baricitinib was found to be 492.478 K that showed an ARD of 1.093 (STRM)',
             'calculated', '492.478 K − 273.15 = 219.328 °C', 'STRM GC+ predicted; Hukkerikar et al. method'))

# Baricitinib literature [47] Alshetaili 487.15 K -> 214.0 °C (from table 5 ref column)
# Text: "with that of reported A. S. Alshetaili et al. [47]" implies 487.15 K from table; conservative: only add Tm STRM from text-confirmed

# Camostat SIRM 497.05 K — TEXT states 497.05 (SIRM). Note: table cell at SIRM position is 468.250; table-text inconsistency.
# Per protocol: when source is ambiguous, prefer text or flag. Text says SIRM=497.05 with ARD 2.85.
# Cross-check with table: Camostat row has STRM 453.792, SIRM 468.250, [49] 467.15. ARD of 2.85 matches STRM (453.792 vs 467.15).
# So text "(SIRM)" appears mislabeled. The value 497.05 doesn't appear next to Camostat in the table.
# Per v1.2 quote re-confirmation step 2: the value next to the compound in the quote must match value_raw.
# In table 5 Camostat column, 497.05 is NOT present. SKIP Camostat row to avoid misattribution.

# Chloroquine STRM 385.54 K -> 112.39 °C (text-confirmed)
rows.append(('Chloroquine', 'melting_point', '385.54 K', 112.39, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'the Chloroquine estimated T m was found to be 385.54 K against the reported value of 363.15 K by M. Staderini et al. [50]',
             'calculated', '385.54 K − 273.15 = 112.39 °C', 'SIRM GC+ predicted'))

# Chloroquine literature [50] Staderini 363.15 K -> 90.0 °C (text-confirmed)
rows.append(('Chloroquine', 'melting_point', '363.15 K', 90.0, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'the Chloroquine estimated T m was found to be 385.54 K against the reported value of 363.15 K by M. Staderini et al. [50]',
             'measured', '363.15 K − 273.15 = 90.00 °C', 'literature comparison value, cited via [50] Staderini Adv. Synth. Catal. 357:185'))

# Dexamethasone literature [51] 524.60 K -> 251.45 °C
rows.append(('Dexamethasone', 'melting_point', '524.60 K', 251.45, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'The estimated T m for Dexamethasone showed an ARD of 10.87 with that of reported T m of 524.60 K [51]',
             'measured', '524.60 K − 273.15 = 251.45 °C', 'literature comparison value via [51] Cai J Pharm Sci 86:372'))

# Favipiravir STRM 465.51 K -> 192.36 °C
rows.append(('Favipiravir', 'melting_point', '465.51 K', 192.36, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'The estimated T m for Favipiravir was found to be 465.51 K with a relatively low deviation of 3.41 K with that reported by Q. Guo et al. [52]',
             'calculated', '465.51 K − 273.15 = 192.36 °C', 'STRM GC+ predicted'))

# Fingolimod STRM 398.69 K -> 125.54 °C
rows.append(('Fingolimod', 'melting_point', '398.69 K', 125.54, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'Fingolimod showed the lowest ARD with an estimated T m of 398.69 K and 396.30 K based on STRM and SIRM method',
             'calculated', '398.69 K − 273.15 = 125.54 °C', 'STRM GC+ predicted'))

# Fingolimod SIRM 396.30 K -> 123.15 °C
rows.append(('Fingolimod', 'melting_point', '396.30 K', 123.15, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'Fingolimod showed the lowest ARD with an estimated T m of 398.69 K and 396.30 K based on STRM and SIRM method',
             'calculated', '396.30 K − 273.15 = 123.15 °C', 'SIRM GC+ predicted'))

# Hydroxychloroquine STRM 417.16 K -> 144.01 °C
rows.append(('Hydroxychloroquine', 'melting_point', '417.16 K', 144.01, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'The estimated T m for Hydroxychloroquine is 417.16 K (STRM) with an ARD 12.05',
             'calculated', '417.16 K − 273.15 = 144.01 °C', 'STRM GC+ predicted'))

# Thalidomide estimated 441.49 K -> 168.34 °C
rows.append(('Thalidomide', 'melting_point', '441.49 K', 168.34, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'Thalidomide estimated T m ( 441.49 K ) should a high ARD of 18.71',
             'calculated', '441.49 K − 273.15 = 168.34 °C', 'predicted by GC+ method (per surrounding context, STRM-style)'))

# Thalidomide literature [57] 543.15 K -> 270.0 °C
rows.append(('Thalidomide', 'melting_point', '543.15 K', 270.0, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'with that of reported T m of 543.15 K by et al. B.D. Vu et al. [57]',
             'measured', '543.15 K − 273.15 = 270.00 °C', 'literature comparison value via [57] Vu Org Process Res Dev 23:1374'))

# Umifenovir STRM 447.21 K -> 174.06 °C
rows.append(('Umifenovir', 'melting_point', '447.21 K', 174.06, None, None,
             DOI064, SRC064, 'p. 3 col 2 ¶ 3 (Result and discussion)',
             'The Umifenovir estimated T m was found to be 447.21 K (STRM) with an ARD of 7.72',
             'calculated', '447.21 K − 273.15 = 174.06 °C', 'STRM GC+ predicted'))


# ---- Paper 075 (Antibiotics 2026, 15(2), 127) ----
DOI075 = 'https://doi.org/10.3390/antibiotics15020127'
SRC075 = 'Antibiotics (Basel), 2026, 15(2), 127'

# Full IUPAC names from "Synthesis of <NAME> (code)" headers
rows.append(('N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-fluoroaniline', 'melting_point', '144–145 °C', 144.5, 144.0, 145.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 4a)',
             'Synthesis of N -[(3,5-dimetyl-4-iodo-1 H -pyrazol-1-yl)-methyl]-4-fluoroaniline ( 4a ) Yield 88%; mp 144–145 °C',
             'measured', '', 'compound 4a; note paper uses "dimetyl" (typo for dimethyl)'))

rows.append(('N,N-bis-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-iodoaniline', 'melting_point', '99–100 °C', 99.5, 99.0, 100.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 5d)',
             'hesis of N , N -bis-[(3,5-dimetyl-4-iodo-1 H -pyrazol-1-yl)-methyl]-4-iodoaniline ( 5d ) Yield 79%; mp 99–100 °C',
             'measured', '', 'compound 5d'))

rows.append(('N-[(3,5-dimethyl-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline', 'melting_point', '108–110 °C', 109.0, 108.0, 110.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 6b)',
             'e ( 6b ) Compound 6b was synthesized according to the general procedure described for 6c Yield 91%; mp 108–110 °C',
             'measured', '', 'compound 6b (synthesis follows procedure of 6c)'))

rows.append(('N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline', 'melting_point', '78–80 °C', 79.0, 78.0, 80.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 6c)',
             'nthesis of N -[(3,5-dimetyl-4-iodo-1 H -pyrazol-1-yl)-methyl]-2,4-dichloroaniline ( 6c ) Yield 70%; mp 78–80 °C',
             'measured', '', 'compound 6c'))

rows.append(('N-[(3,5-dimethyl-4-nitro-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline', 'melting_point', '136–138 °C', 137.0, 136.0, 138.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 6d)',
             'e ( 6d ) Compound 6d was synthesized according to the general procedure described for 6c Yield 93%; mp 136–138 °C',
             'measured', '', 'compound 6d'))

rows.append(('N-[(3,5-dimethyl-1H-pyrazol-1-yl)-methyl]-2,6-dichloroaniline', 'melting_point', '108–110 °C', 109.0, 108.0, 110.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 6e)',
             'e ( 6e ) Compound 6e was synthesized according to the general procedure described for 6c Yield 35%; mp 108–110 °C',
             'measured', '', 'compound 6e'))

rows.append(('N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-2,6-dichloroaniline', 'melting_point', '81–82 °C', 81.5, 81.0, 82.0,
             DOI075, SRC075, 'Section 3.2 (Synthesis of compound 6f)',
             'e ( 6f ) Compound 6f was synthesized according to the general procedure described for 6c Yield 51%; mp 81–82 °C',
             'measured', '', 'compound 6f'))

# ---- Paper 070 (Molecules 2026, 31(5), 862) ----
DOI070 = 'https://doi.org/10.3390/molecules31050862'
SRC070 = 'Molecules, 2026, 31(5), 862'

rows.append(('2-(4-(3-Chloropropyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '112–115 °C', 113.5, 112.0, 115.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1a)',
             '2-(4-(3-Chloropropyl)-1 H -1,2,3-triazol-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 1a ) White crystals, m.p. 112–115 °C',
             'measured', '', 'compound 1a; recrystallized from iPrOH'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-phenyl-1H-1,2,3-triazol-1-yl)acetamide', 'melting_point', '83–86 °C', 84.5, 83.0, 86.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1b)',
             'N -(2-(3-Methoxyphenoxy)phenyl)-2-(4-phenyl-1 H -1,2,3-triazol-1-yl)acetamide ( 1b ) White crystals, m.p. 83–86 °C',
             'measured', '', 'compound 1b; recrystallized from iPrOH'))

rows.append(('2-(4-(4-Chlorophenyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '104–108 °C', 106.0, 104.0, 108.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1c)',
             'rophenyl)-1 H -1,2,3-triazol-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 1c ) White crystals, m.p. 104–108 °C',
             'measured', '', 'compound 1c'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-(4-methoxyphenyl)-1H-1,2,3-triazol-1-yl)acetamide', 'melting_point', '138–141 °C', 139.5, 138.0, 141.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1d)',
             'hoxyphenoxy)phenyl)-2-(4-(4-methoxyphenyl)-1 H -1,2,3-triazol-1-yl)acetamide ( 1d ) White crystals, m.p. 138–141 °C',
             'measured', '', 'compound 1d'))

rows.append(('2-(4-(p-Tolyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '121–124 °C', 122.5, 121.0, 124.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1e)',
             'ylphenyl)-1 H -1,2,3-triazol-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 1e ) White crystals, m.p. 121–124 °C',
             'measured', '', 'compound 1e — methylphenyl/4-tolyl substituent'))

rows.append(('2-(4-(Biphenyl-4-yl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '156–158 °C', 157.0, 156.0, 158.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1f)',
             'enyl]-4-yl)-1H-1,2,3-triazol-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 1f ) White crystals, m.p. 156–158 °C',
             'measured', '', 'compound 1f'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-(4-pentylphenyl)-1H-1,2,3-triazol-1-yl)acetamide', 'melting_point', '77–80 °C', 78.5, 77.0, 80.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 1g)',
             'thoxyphenoxy)phenyl)-2-(4-(4-pentylphenyl)-1 H -1,2,3-triazol-1-yl)acetamide ( 1g ) White crystals, m.p. 77–80 °C',
             'measured', '', 'compound 1g'))

rows.append(('2-(Dimethylamino)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '54–56 °C', 55.0, 54.0, 56.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2a)',
             '2-(Dimethylamino)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 2a ) White crystals, m.p. 54–56 °C',
             'measured', '', 'compound 2a; recrystallized from cyclohexane'))

rows.append(('2-(Aziridin-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '75–78 °C', 76.5, 75.0, 78.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2b)',
             '2-(Aziridin-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 2b ) White crystals, m.p. 75–78 °C',
             'measured', '', 'compound 2b'))

rows.append(('2-(Azetidin-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide', 'melting_point', '91–94 °C', 92.5, 91.0, 94.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2c)',
             '2-(Azetidin-1-yl)- N -(2-(3-methoxyphenoxy)phenyl)acetamide ( 2c ) White crystals, m.p. 91–94 °C',
             'measured', '', 'compound 2c'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-(pyrrolidin-1-yl)acetamide', 'melting_point', '88–91 °C', 89.5, 88.0, 91.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2e)',
             'N -(2-(3-Methoxyphenoxy)phenyl)-2-(pyrrolidin-1-yl)acetamide ( 2e ) White crystals, m.p. 88–91 °C',
             'measured', '', 'compound 2e'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-(piperidin-1-yl)acetamide', 'melting_point', '89–92 °C', 90.5, 89.0, 92.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2f)',
             'N -(2-(3-Methoxyphenoxy)phenyl)-2-(piperidin-1-yl)acetamide ( 2f ) White crystals, m.p. 89–92 °C',
             'measured', '', 'compound 2f'))

rows.append(('N-(2-(3-Methoxyphenoxy)phenyl)-2-morpholinoacetamide', 'melting_point', '114–117 °C', 115.5, 114.0, 117.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 2g)',
             'N -(2-(3-Methoxyphenoxy)phenyl)-2-morpholinoacetamide ( 2g ) White crystals, m.p. 114–117 °C',
             'measured', '', 'compound 2g'))

rows.append(('N-(2-((2-(3-Methoxyphenoxy)phenyl)amino)-2-oxoethyl)-4-nitrobenzamide', 'melting_point', '134–136 °C', 135.0, 134.0, 136.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 3a)',
             'N -(2-((2-(3-Methoxyphenoxy)phenyl)amino)-2-oxoethyl)-4-nitrobenzamide ( 3a ) Yellowish crystals, m.p. 134–136 °C',
             'measured', '', 'compound 3a'))

rows.append(('2-Fluoro-N-(2-((2-(3-methoxyphenoxy)phenyl)amino)-2-oxoethyl)benzamide', 'melting_point', '93–95 °C', 94.0, 93.0, 95.0,
             DOI070, SRC070, 'Section 3 (Synthesis section, compound 3b)',
             '2-Fluoro- N -(2-((2-(3-methoxyphenoxy)phenyl)amino)-2-oxoethyl)benzamide ( 3b ) White crystals, m.p. 93–95 °C',
             'measured', '', 'compound 3b'))

# ---- Paper 068 (Molecules 2026, 31(5), 844) ----
# Compounds 1, 2, 3 have full IUPAC names. 4a-j and 5a-j are series — 5c has full name.
DOI068 = 'https://doi.org/10.3390/molecules31050844'
SRC068 = 'Molecules, 2026, 31(5), 844'

rows.append(('N-(3-chloro-4-fluorophenyl) acetamide', 'melting_point', '119–120 °C', 119.5, 119.0, 120.0,
             DOI068, SRC068, 'Section 3 (Synthesis of compound 1)',
             ' as white crystals. Yield 11.98 g, 93.90%, M.P.: 119–120 °C',
             'measured', '', 'compound 1 from synthesis section header "Synthesis of N -(3-chloro-4-fluorophenyl) acetamide (1)"'))

rows.append(('N-(5-chloro-4-fluoro-2-nitrophenyl) acetamide', 'melting_point', '112–113 °C', 112.5, 112.0, 113.0,
             DOI068, SRC068, 'Section 3 (Synthesis of compound 2)',
             'target compound. Yield 12.23 g, 97.64%, M.P.: 112–113 °C',
             'measured', '', 'compound 2 from synthesis section header "Synthesis of N -(5-chloro-4-fluoro-2-nitrophenyl) acetamide (2)"'))

rows.append(('5-chloro-4-fluoro-2-nitroaniline', 'melting_point', '144–145 °C', 144.5, 144.0, 145.0,
             DOI068, SRC068, 'Section 3 (Synthesis of compound 3)',
             'using absolute ethanol to give yellow crystals. Yield 4.00 g, 98.09%, M.P.: 144–145 °C',
             'measured', '', 'compound 3 from synthesis section header "Synthesis of 5-chloro-4-fluoro-2-nitroaniline (3)"'))

rows.append(('4-fluoro-5-(4-ethylpiperazin-1-yl) benzene-1,2-diamine', 'melting_point', '79–81 °C', 80.0, 79.0, 81.0,
             DOI068, SRC068, 'Section 3 (Synthesis of compound 5b/5c series)',
             'Solid cream crystals; molecular formula: C 11 H 17 FN 4 . Yield 0.92 g, 77.54%, M.P.: 79–81 °C (literature [ 61 ], 78–80 °C)',
             'measured', '', 'compound 5b — note paper "Synthesis of 4-fluoro-5-(4-ethylpiperazin-1-yl) benzene-1,2-diamine (5c)" header but C11H17FN4 formula belongs to ethyl piperazine derivative; literature value 78–80 °C also cited'))


# ---- Paper 078 (Turk J Chem 2022, 46(2), 506-522) ----
DOI078 = 'https://doi.org/10.55730/1300-0527.3324'
SRC078 = 'Turkish Journal of Chemistry, 2022, 46(2), 506-522'

# Two compounds with full IUPAC names inline
rows.append(('(3aS,5R,7aR)-7a-methyl-5-(p-tolyl)hexahydrobenzo[d]isoxazol-2-en-1-one', 'melting_point', '96–98 °C', 97.0, 96.0, 98.0,
             DOI078, SRC078, 'Section 3 / Scheme (compound 2 characterization)',
             'Chemical Formula: C 18 H 21 NO 2 Exact mass: 306.1470 Molecular weight: 306.1466 Solid m.p: 96–98 °C',
             'measured', '', 'Compound 2 — bis-isoxazoline with monoterpenic skeleton; name inferred from context but compound identifier is 2, drop if uncertain'))

# For paper 078, both names involve fused ring isoxazoline with code names; full IUPAC not visible above mp.
# Conservative: flag this row with notes since the exact compound name is uncertain — actually drop since the
# IUPAC name above the mp is partial. Let's drop this paper 078 row.
rows.pop()

# Paper 071, 072, 074: most compounds are coded (S)-3, (S)-4, etc. or complex Au/Pt structures.
# Per protocol, drop bare codes. Skip.

# Paper 069: carbohydrazide/carboxamide series 1a-k, 2a-l. The class scaffold is named
# "1-(4-Methylbenzyl)-1,4-dihydroindeno[1,2-b]pyrrole-3-carbohydrazides 1a–d, carboxamides 1e–k"
# but per-compound substituents (X = various aryl) not explicit in text. Skip.

# Paper 073: Schiff bases with codes I-V; no per-compound IUPAC names. Skip.

# Paper 076: Knoevenagel reaction product (benzylidene malononitrile) mp 82-85 °C is literature value,
# but no specific compound name for the actual measured product. Skip.

# Paper 067: review/QSPR paper with no per-compound mp/bp values in text. Skip.

# Write CSV
header = ['id','verification_status','compound_name','compound_smiles','property',
         'value_celsius','value_celsius_min','value_celsius_max','value_raw','relation',
         'data_type','source','source_url','evidence_location','evidence_quote',
         'conversion_arithmetic','notes']

with open(OUT, 'w', newline='', encoding='utf-8') as fout:
    w = csv.writer(fout)
    w.writerow(header)
    for i, r in enumerate(rows, 1):
        compound, prop, vraw, vc, vmin, vmax, url, src, loc, quote, dtype, conv, notes = r
        w.writerow([
            i, 'pending_verification', compound, '', prop,
            vc, vmin if vmin else '', vmax if vmax else '',
            vraw, '=', dtype, src, url, loc, quote, conv, notes
        ])

print(f'Wrote {len(rows)} rows to {OUT}')

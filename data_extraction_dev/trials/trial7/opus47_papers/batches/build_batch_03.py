#!/usr/bin/env python3
"""Build batch_03.csv for the data-extraction skill (mp_bp overlay)."""
import csv

import os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "batch_03.csv")
HEADER = ["id","verification_status","compound_name","compound_smiles","property","value","value_min","value_max","value_raw","units","relation","meas_calc","source","source_url","evidence_location","evidence_quote","conversion_arithmetic","notes"]

rows = []
nid = 3000

def add(compound, prop, value, value_raw, source, source_url, evidence_location, evidence_quote, meas_calc="measured",
        relation="=", value_min="", value_max="", conversion="", notes="", smiles=""):
    global nid
    rows.append({
        "id": str(nid),
        "verification_status": "pending_verification",
        "compound_name": compound,
        "compound_smiles": smiles,
        "property": prop,
        "value": str(value),
        "value_min": str(value_min),
        "value_max": str(value_max),
        "value_raw": value_raw,
        "units": "°C",
        "relation": relation,
        "meas_calc": meas_calc,
        "source": source,
        "source_url": source_url,
        "evidence_location": evidence_location,
        "evidence_quote": evidence_quote,
        "conversion_arithmetic": conversion,
        "notes": notes
    })
    nid += 1

# =====================
# Paper 064 - Thermodynamic properties APIs (COVID-19)
# DOI: 10.1016/j.cdc.2021.100820
# =====================
SRC_064 = "Chemical Data Collections 37 (2022) 100820"
URL_064 = "https://doi.org/10.1016/j.cdc.2021.100820"

TB_QUOTE_1 = "Tb         [K]         794.469         760.077              757.482     771.300              688.550     682.652              722.347      717.264               618.948       688.871"
TM_QUOTE_1 = "Tm         [K]         492.478         458.127     487.15   453.792     468.250     467.15   393.375     385.545     363.15   467.128      462.022      524.15   465.514       497.056     450.15"

add("Baricitinib","boiling_point",521.319,"794.469 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Baricitinib STRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="794.469 K − 273.15 = 521.319 °C", notes="STRM (stepwise regression) calculated value")
add("Baricitinib","boiling_point",486.927,"760.077 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Baricitinib SIRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="760.077 K − 273.15 = 486.927 °C", notes="SIRM (simultaneous regression) calculated value")
add("Camostat","boiling_point",484.332,"757.482 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Camostat STRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="757.482 K − 273.15 = 484.332 °C", notes="STRM calculated value")
add("Camostat","boiling_point",498.150,"771.300 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Camostat SIRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="771.300 K − 273.15 = 498.150 °C", notes="SIRM calculated value")
add("Chloroquine","boiling_point",415.400,"688.550 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Chloroquine STRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="688.550 K − 273.15 = 415.400 °C", notes="STRM calculated value")
add("Chloroquine","boiling_point",409.502,"682.652 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Chloroquine SIRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="682.652 K − 273.15 = 409.502 °C", notes="SIRM calculated value")
add("Dexamethasone","boiling_point",449.197,"722.347 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Dexamethasone STRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="722.347 K − 273.15 = 449.197 °C", notes="STRM calculated value")
add("Dexamethasone","boiling_point",444.114,"717.264 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Dexamethasone SIRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="717.264 K − 273.15 = 444.114 °C", notes="SIRM calculated value")
add("Favipiravir","boiling_point",345.798,"618.948 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Favipiravir STRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="618.948 K − 273.15 = 345.798 °C", notes="STRM calculated value")
add("Favipiravir","boiling_point",415.721,"688.871 K",SRC_064,URL_064,"Table 5 row 'Tb [K]' col 'Favipiravir SIRM'",
    TB_QUOTE_1, meas_calc="calculated", conversion="688.871 K − 273.15 = 415.721 °C", notes="SIRM calculated value")

add("Baricitinib","melting_point",219.328,"492.478 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Baricitinib STRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="492.478 K − 273.15 = 219.328 °C", notes="STRM calculated Tm")
add("Baricitinib","melting_point",184.977,"458.127 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Baricitinib SIRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="458.127 K − 273.15 = 184.977 °C", notes="SIRM calculated Tm")
add("Baricitinib","melting_point",214.000,"487.15 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Baricitinib [47]'",
    TM_QUOTE_1, meas_calc="measured", conversion="487.15 K − 273.15 = 214.000 °C", notes="Reported experimental Tm from ref [47] (Alshetaili)")
add("Camostat","melting_point",180.642,"453.792 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Camostat STRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="453.792 K − 273.15 = 180.642 °C", notes="STRM calculated Tm")
add("Camostat","melting_point",195.100,"468.250 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Camostat SIRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="468.250 K − 273.15 = 195.100 °C", notes="SIRM calculated Tm")
add("Camostat","melting_point",194.000,"467.15 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Camostat [49]'",
    TM_QUOTE_1, meas_calc="measured", conversion="467.15 K − 273.15 = 194.000 °C", notes="Reported experimental Tm from ref [49] (J. Yin)")
add("Chloroquine","melting_point",120.225,"393.375 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Chloroquine STRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="393.375 K − 273.15 = 120.225 °C", notes="STRM calculated Tm")
add("Chloroquine","melting_point",112.395,"385.545 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Chloroquine SIRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="385.545 K − 273.15 = 112.395 °C", notes="SIRM calculated Tm")
add("Chloroquine","melting_point",90.000,"363.15 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Chloroquine [50]'",
    TM_QUOTE_1, meas_calc="measured", conversion="363.15 K − 273.15 = 90.000 °C", notes="Reported experimental Tm from ref [50] (Staderini)")
add("Dexamethasone","melting_point",193.978,"467.128 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Dexamethasone STRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="467.128 K − 273.15 = 193.978 °C", notes="STRM calculated Tm")
add("Dexamethasone","melting_point",188.872,"462.022 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Dexamethasone SIRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="462.022 K − 273.15 = 188.872 °C", notes="SIRM calculated Tm")
add("Dexamethasone","melting_point",251.000,"524.15 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Dexamethasone [51]'",
    TM_QUOTE_1, meas_calc="measured", conversion="524.15 K − 273.15 = 251.000 °C", notes="Reported experimental Tm from ref [51]")
add("Favipiravir","melting_point",192.364,"465.514 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Favipiravir STRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="465.514 K − 273.15 = 192.364 °C", notes="STRM calculated Tm")
add("Favipiravir","melting_point",223.906,"497.056 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Favipiravir SIRM'",
    TM_QUOTE_1, meas_calc="calculated", conversion="497.056 K − 273.15 = 223.906 °C", notes="SIRM calculated Tm")
add("Favipiravir","melting_point",177.000,"450.15 K",SRC_064,URL_064,"Table 5 row 'Tm [K]' col 'Favipiravir [52]'",
    TM_QUOTE_1, meas_calc="measured", conversion="450.15 K − 273.15 = 177.000 °C", notes="Reported experimental Tm from ref [52] (Q. Guo)")

TB_QUOTE_2 = "Tb         [K]             687.396    689.003               681.390    714.345               648.734     650.895                           776.060               772.496"
TM_QUOTE_2 = "Tm         [K]             398.693     396.310     400.15   417.170     414.588     367.1    441.490     440.390     543.15                447.213               448.603                   415"

add("Fingolimod","boiling_point",414.246,"687.396 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Fingolimod STRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="687.396 K − 273.15 = 414.246 °C", notes="STRM calculated")
add("Fingolimod","boiling_point",415.853,"689.003 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Fingolimod SIRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="689.003 K − 273.15 = 415.853 °C", notes="SIRM calculated")
add("Hydroxychloroquine","boiling_point",408.240,"681.390 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Hydroxychloroquine STRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="681.390 K − 273.15 = 408.240 °C", notes="STRM calculated")
add("Hydroxychloroquine","boiling_point",441.195,"714.345 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Hydroxychloroquine SIRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="714.345 K − 273.15 = 441.195 °C", notes="SIRM calculated")
add("Thalidomide","boiling_point",375.584,"648.734 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Thalidomide STRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="648.734 K − 273.15 = 375.584 °C", notes="STRM calculated")
add("Thalidomide","boiling_point",377.745,"650.895 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Thalidomide SIRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="650.895 K − 273.15 = 377.745 °C", notes="SIRM calculated")
add("Umifenovir","boiling_point",502.910,"776.060 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Umifenovir STRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="776.060 K − 273.15 = 502.910 °C", notes="STRM calculated")
add("Umifenovir","boiling_point",499.346,"772.496 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tb [K]' col 'Umifenovir SIRM'",
    TB_QUOTE_2, meas_calc="calculated", conversion="772.496 K − 273.15 = 499.346 °C", notes="SIRM calculated")

add("Fingolimod","melting_point",125.543,"398.693 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Fingolimod STRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="398.693 K − 273.15 = 125.543 °C", notes="STRM calculated Tm")
add("Fingolimod","melting_point",123.160,"396.310 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Fingolimod SIRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="396.310 K − 273.15 = 123.160 °C", notes="SIRM calculated Tm")
add("Fingolimod","melting_point",127.000,"400.15 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Fingolimod [53]'",
    TM_QUOTE_2, meas_calc="measured", conversion="400.15 K − 273.15 = 127.000 °C", notes="Reported experimental Tm from ref [53] (S. R. Shaikh)")
add("Hydroxychloroquine","melting_point",144.020,"417.170 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Hydroxychloroquine STRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="417.170 K − 273.15 = 144.020 °C", notes="STRM calculated Tm")
add("Hydroxychloroquine","melting_point",141.438,"414.588 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Hydroxychloroquine SIRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="414.588 K − 273.15 = 141.438 °C", notes="SIRM calculated Tm")
add("Hydroxychloroquine","melting_point",93.950,"367.1 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Hydroxychloroquine [55]'",
    TM_QUOTE_2, meas_calc="measured", conversion="367.1 K − 273.15 = 93.950 °C", notes="Reported experimental Tm from ref [55]")
add("Thalidomide","melting_point",168.340,"441.490 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Thalidomide STRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="441.490 K − 273.15 = 168.340 °C", notes="STRM calculated Tm")
add("Thalidomide","melting_point",167.240,"440.390 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Thalidomide SIRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="440.390 K − 273.15 = 167.240 °C", notes="SIRM calculated Tm")
add("Thalidomide","melting_point",270.000,"543.15 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Thalidomide [57]'",
    TM_QUOTE_2, meas_calc="measured", conversion="543.15 K − 273.15 = 270.000 °C", notes="Reported experimental Tm from ref [57] (B.D. Vu)")
add("Umifenovir","melting_point",174.063,"447.213 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Umifenovir STRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="447.213 K − 273.15 = 174.063 °C", notes="STRM calculated Tm")
add("Umifenovir","melting_point",175.453,"448.603 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Umifenovir SIRM'",
    TM_QUOTE_2, meas_calc="calculated", conversion="448.603 K − 273.15 = 175.453 °C", notes="SIRM calculated Tm")
add("Umifenovir","melting_point",141.850,"415 K",SRC_064,URL_064,"Table 5 (cont.) row 'Tm [K]' col 'Umifenovir [58]'",
    TM_QUOTE_2, meas_calc="measured", conversion="415 K − 273.15 = 141.850 °C", notes="Reported experimental Tm from ref [58] (A. Kons)")

# =====================
# Paper 067 - QSPR alkyl alcohols (Molecules 2003, 8, 687-726)
# =====================
SRC_067 = "Molecules 2003, 8(9), 687-726"
URL_067 = "pmc:PMC6146921"

samples_067 = [
    ("methanol", 64.70, "64.70", "          1. methanol                      64.70      65.50      -0.80   -1.24   65.24 (-0.54)"),
    ("ethanol", 78.30, "78.30", "          2. ethanol                       78.30      78.43      -0.13   -0.17    77.69 (0.61)"),
    ("1-propanol", 97.20, "97.20", "          3. 1-propanol                    97.20      95.63      1.57     1.62    96.42 (0.77)"),
    ("2-propanol", 82.30, "82.30", "          4. 2. propanol                   82.30      85.83      -3.53   -4.28   84.11 (-1.81)"),
    ("1-butanol", 117.70, "117.70", "          5. 1-butanol                    117.70      113.40     4.30     3.65    115.67 (2.03)"),
    ("2-butanol", 99.60, "99.60", "          6. 2-butanol                     99.60      102.87     -3.27   -3.28   102.43 (-2.83)"),
    ("2-methyl-1-propanol", 107.90, "107.90", "          7. 2-methyl-1-propanol          107.90      108.66     -0.76   -0.71   109.15 (-1.25)"),
    ("2-methyl-2-propanol", 82.40, "82.40", "          8. 2-methyl-2-propanol           82.40      87.68      -5.28   -6.41   84.52 (-2.12)"),
    ("1-pentanol", 137.80, "137.80", "          9. 1-pentanol                   137.80      133.16     4.64     3.36    134.92 (2.88)"),
    ("2-pentanol", 119.00, "119.00", "          10. 2-pentanol                  119.00      120.59     -1.59   -1.34   121.68 (-2.68)"),
    ("3-pentanol", 115.30, "115.30", "          11. 3-pentanol                  115.30      119.90     -4.60   -3.99   120.75 (-5.45)"),
    ("2-methyl-1-butanol", 128.70, "128.70", "          12. 2-methyl-1-butanol          128.70      126.39     2.31     1.80   127.97 (0.73)"),
    ("3-methyl-1-butanol", 131.20, "131.20", "          13. 3-methyl-1-butanol          131.20      127.13     4.07     3.10   128.90 (2.30)"),
    ("2-methyl-2-butanol", 102.00, "102.00", "          14. 2.methyl-2-butanol           102.00      104.57     -2.57   -2.52   102.41 (-0.41)"),
    ("3-methyl-2-butanol", 111.50, "111.50", "          15. 3-methyl-2-butanol          111.50      115.75     -4.25   -3.81   114.72 (-3.22)"),
    ("2,2-dimethyl-1-propanol", 113.10, "113.10", "          16. 2,2-dimethyl-1-propanol     113.10      117.54     -4.44   -3.93   115.84 (-2.74)"),
    ("1-hexanol", 157.13, "157.13", "          17. 1-hexanol                   157.13      153.12     4.01     2.55   154.17 (2.83)"),
    ("2-hexanol", 139.90, "139.90", "          18. 2-hexanol                   139.90      140.35     -0.45   -0.32   140.92 (-1.02)"),
    ("3-hexanol", 135.40, "135.40", "          19. 3-hexanol                   135.40      137.63     -2.23   -1.64   139.99 (-4.59)"),
    ("2-methyl-1-pentanol", 148.00, "148.00", "          20. 2-methyl-1-pentanol         148.00      146.14     1.86     1.25   147.22 (0.78)"),
    ("4-methyl-1-pentanol", 151.80, "151.80", "          22. 4-methyl-1-pentanol         151.80      148.97     2.83     1.86   148.15 (3.65)"),
    ("2-ethyl-1-butanol", 146.50, "146.50", "          28. 2-ethyl-1-butanol           146.50      144.11     2.39     1.63   146.79 (-0.29)"),
    ("1-heptanol", 176.30, "176.30", "          34. 1-heptanol                  176.30      173.38     2.92     1.66   173.41 (2.87)"),
    ("1-octanol", 195.20, "195.20", "          45. 1-octanol                   195.20      193.67     1.53     0.78   192.58 (2.62)"),
    ("2-octanol", 179.80, "179.80", "          46. 2-octanol                   179.80      180.57     -0.77   -0.43   179.33 (0.47)"),
]
for nm, val, vraw, qt in samples_067:
    add(nm, "boiling_point", val, f"{vraw} °C", SRC_067, URL_067,
        "Table 8 'Experimental and Calculated Bp of Alkyl Alcohols in full Set' (Bp exp column)",
        qt, meas_calc="measured", notes="sampled from Table 8 (25 of 58 alkyl alcohols); compiled experimental Bp")

# =====================
# Paper 068 - Benzimidazole derivatives (Molecules 2026, 31, 844)
# =====================
SRC_068 = "Molecules 2026, 31, 844"
URL_068 = "https://doi.org/10.3390/molecules31050844"

add("N-(3-chloro-4-fluorophenyl)acetamide","melting_point",119.5,"119–120 °C",
    SRC_068,URL_068,"Section 3.1.3 compound 1",
    "Yield 11.98 g, 93.90%, M.P.: 119–120 ◦ C", value_min=119, value_max=120, notes="Compound 1")
add("N-(5-chloro-4-fluoro-2-nitrophenyl)acetamide","melting_point",112.5,"112–113 °C",
    SRC_068,URL_068,"Section 3.1.3 compound 2",
    "12.23 g, 97.64%, M.P.: 112–113 ◦ C", value_min=112, value_max=113, notes="Compound 2")
add("4-fluoro-5-(4-piperazin-1-yl)-2-nitroaniline","melting_point",187.5,"187–188 °C",
    SRC_068,URL_068,"Section 3.1 compound 4a",
    "Solid orange crystals; molecular formula: C10 H13 FN4 O2 . Yield 4.72 g, 88.57%, M.P.: 187–188 ◦ C",
    value_min=187, value_max=188, notes="Compound 4a")
add("4-fluoro-5-(4-methylpiperazin-1-yl)-2-nitroaniline","melting_point",136.0,"135–137 °C",
    SRC_068,URL_068,"Section 3.1 compound 4b",
    "Solid orange crystals; molecular formula: C11 H15 FN4 O2 . Yield 6.64 g, 99.10%, M.P.: 135–137 ◦ C",
    value_min=135, value_max=137, notes="Compound 4b")
add("4-fluoro-5-(4-ethylpiperazin-1-yl)-2-nitroaniline","melting_point",144.0,"143–145 °C",
    SRC_068,URL_068,"Section 3.1 compound 4c",
    "Solid orange crystals; molecular formula: C12 H17 FN4 O2 . Yield 6.73 g, 94.91%, M.P.: 143–145 ◦ C",
    value_min=143, value_max=145, notes="Compound 4c")
add("4-fluoro-5-(4-isopropylpiperazin-1-yl)-2-nitroaniline","melting_point",122.0,"121–123 °C",
    SRC_068,URL_068,"Section 3.1 compound 4d",
    "Solid orange crystals; molecular formula: C13 H19 FN4 O2 . Yield 2.28 g, 61.62%, M.P.: 121–123 ◦ C",
    value_min=121, value_max=123, notes="Compound 4d")
add("4-fluoro-5-(4-butylpiperazin-1-yl)-2-nitroaniline","melting_point",110.0,"109–111 °C",
    SRC_068,URL_068,"Section 3.1 compound 4e",
    "Solid orange crystals; molecular formula: C14 H21 FN4 O2 . Yield 3.57 g, 91.8%, M.P.: 109–111 ◦ C",
    value_min=109, value_max=111, notes="Compound 4e")
add("4-fluoro-5-(4-phenylpiperazin-1-yl)-2-nitrobenzenamine","melting_point",184.0,"183–185 °C",
    SRC_068,URL_068,"Section 3.1 compound 4f",
    "Solid orange crystals; molecular formula: C16 H17 FN4 O2 . Yield 4.02 g, 94.37%, M.P.: 183–185 ◦ C",
    value_min=183, value_max=185, notes="Compound 4f")
add("4-fluoro-2-nitro-5-(pyrrolidin-1-yl)aniline","melting_point",188.0,"187–189 °C",
    SRC_068,URL_068,"Section 3.1 compound 4g",
    "Solid orange crystals; molecular formula: C10 H12 FN3 O2 . Yield 5.61 g, 94.94%, M.P.: 187–189 ◦ C",
    value_min=187, value_max=189, notes="Compound 4g")
add("4-fluoro-2-nitro-5-(morpholin-1-yl)aniline","melting_point",187.0,"186–188 °C",
    SRC_068,URL_068,"Section 3.1 compound 4i",
    "Solid orange crystals; molecular formula: C10 H12 FN3 O3 . Yield 2.88 g, 90.0%, M.P.: 186–188 ◦ C",
    value_min=186, value_max=188, notes="Compound 4i")
add("2-(4-(5-amino-2-fluoro-4-nitrophenyl)piperazin-1-yl)ethanol","melting_point",150.5,"150–151 °C",
    SRC_068,URL_068,"Section 3.1 compound 4j",
    "Solid orange crystals; molecular formula: C12 H17 FN4 O3 . Yield 3.130 g, 83.9%, M.P.: 150–151 ◦ C",
    value_min=150, value_max=151, notes="Compound 4j")
add("4-fluoro-5-(4-piperazin-1-yl)benzene-1,2-diamine","melting_point",112.0,"111–113 °C",
    SRC_068,URL_068,"Section 3.1 compound 5a",
    "Solid cream crystals; molecular formula: C10 H15 FN4 . Yield 0.92 g, 77.54%, M.P.: 111–113 ◦ C",
    value_min=111, value_max=113, notes="Compound 5a")
add("4-fluoro-5-(4-ethylpiperazin-1-yl)benzene-1,2-diamine","melting_point",95.0,"94–96 °C",
    SRC_068,URL_068,"Section 3.1 compound 5c",
    "Solid cream crystals; molecular formula: C12 H19 FN4 . Yield 0.76 g, 85.60%, M.P.: 94–96 ◦ C",
    value_min=94, value_max=96, notes="Compound 5c")
add("4-fluoro-5-(4-isopropylpiperazin-1-yl)benzene-1,2-diamine","melting_point",128.0,"127–129 °C",
    SRC_068,URL_068,"Section 3.1 compound 5d",
    "Solid cream crystals; molecular formula: C13 H21 FN4 . Yield 0.97 g, 99.5%, M.P.: 127–129 ◦ C",
    value_min=127, value_max=129, notes="Compound 5d")
add("4-fluoro-5-(4-butylpiperazin-1-yl)benzene-1,2-diamine","melting_point",120.0,"119–121 °C",
    SRC_068,URL_068,"Section 3.1 compound 5e",
    "Solid cream crystals. Molecular formula: C14 H23 FN4 . Yield 0.96 g, 99.5%, M.P.: 119–121 ◦ C",
    value_min=119, value_max=121, notes="Compound 5e")
add("4-fluoro-5-(4-phenylpiperazin-1-yl)benzene-1,2-diamine","melting_point",282.0,"281–283 °C",
    SRC_068,URL_068,"Section 3.1 compound 5f",
    "Solid cream crystals; molecular formula: C16 H19 FN4 . Yield 0.95 g, 99.4%, M.P.: 281–283 ◦ C",
    value_min=281, value_max=283, notes="Compound 5f")
add("4-fluoro-5-(morpholin-1-yl)benzene-1,2-diamine","melting_point",127.5,"127–128 °C",
    SRC_068,URL_068,"Section 3.1 compound 5i",
    "Solid cream crystals; molecular formula: C10 H14 FN3 O. Yield 0.92 g, 99.4%, M.P.: 127–128 ◦ C",
    value_min=127, value_max=128, notes="Compound 5i")
add("2-(4-(4,5-diamino-2-fluorophenyl)piperazin-1-yl)ethanol","melting_point",116.0,"115–117 °C",
    SRC_068,URL_068,"Section 3.1 compound 5j",
    "Solid cream crystals; molecular formula: C12 H19 FN4 O. Yield 0.8 g, 89.4, M.P.: 115–117 ◦ C",
    value_min=115, value_max=117, notes="Compound 5j")
add("6-fluoro-5-(4-piperazin-1-yl)-1H-benzo[d]imidazole","melting_point",235.0,"234–236 °C",
    SRC_068,URL_068,"Section 3.1 compound 6a",
    "Solid orange crystals; molecular formula: C11 H13 FN4 . Yield 0.84 g, 80.46%, M.P.: 234–236 ◦ C",
    value_min=234, value_max=236, notes="Compound 6a")
add("6-fluoro-5-(4-ethylpiperazin-1-yl)-1H-benzo[d]imidazole","melting_point",138.5,"138–139 °C",
    SRC_068,URL_068,"Section 3.1 compound 6c",
    "Solid orange crystals; molecular formula: C13 H17 FN4 . Yield 0.85 g, 81.7%, M.P.: 138–139 ◦ C",
    value_min=138, value_max=139, notes="Compound 6c")
add("6-fluoro-5-(4-isopropylpiperazin-1-yl)-1H-benzo[d]imidazole","melting_point",148.0,"147–149 °C",
    SRC_068,URL_068,"Section 3.1 compound 6d",
    "Solid orange crystals. Molecular formula: C14 H19 FN4 . Yield 0.85 g, 81.2%, M.P.: 147–149 ◦ C",
    value_min=147, value_max=149, notes="Compound 6d")
add("6-fluoro-5-(4-butylpiperazin-1-yl)-1H-benzo[d]imidazole","melting_point",141.0,"140–142 °C",
    SRC_068,URL_068,"Section 3.1 compound 6e",
    "Solid orange crystals; molecular formula: C15 H21 FN4 . Yield 0.93 g, 89.8%, M.P.: 140–142 ◦ C",
    value_min=140, value_max=142, notes="Compound 6e")
add("6-fluoro-5-(4-phenylpiperazin-1-yl)-1H-benzo[d]imidazole","melting_point",131.0,"130–132 °C",
    SRC_068,URL_068,"Section 3.1 compound 6f",
    "Solid orange crystals; molecular formula: C17 H17 FN4 . Yield 0.84 g, 81.1%, M.P.: 130–132 ◦ C",
    value_min=130, value_max=132, notes="Compound 6f")
add("6-fluoro-5-(4-piperidin-1-yl)-1H-benzo[d]imidazole","melting_point",169.0,"168–170 °C",
    SRC_068,URL_068,"Section 3.1 compound 6h",
    "Solid orange crystals. Molecular formula: C12 H14 FN3 . Yield 0.96 g, 95.4%, M.P.: 168–170 ◦ C",
    value_min=168, value_max=170, notes="Compound 6h")
add("6-fluoro-5-(4-morpholine-1-yl)-1H-benzo[d]imidazole","melting_point",210.0,"209–211 °C",
    SRC_068,URL_068,"Section 3.1 compound 6i",
    "Solid orange crystals; molecular formula: C11 H12 FN3 O. Yield 0.81 g, 82.8%, M.P.: 209–211 ◦ C",
    value_min=209, value_max=211, notes="Compound 6i")
add("2-(4-(6-fluoro-1H-benzo[d]imidazol-5-yl)piperazin-1-yl)ethanol","melting_point",121.0,"120–122 °C",
    SRC_068,URL_068,"Section 3.1 compound 6j",
    "Solid orange crystals; molecular formula: C13 H17 FN4 O. Yield 0.87 g, 83.71%, M.P.: 120–122 ◦ C",
    value_min=120, value_max=122, notes="Compound 6j")

# =====================
# Paper 069 - Tricyclic pyrrole-based Zika inhibitors (IJMS 2026, 27, 2306)
# =====================
SRC_069 = "Int. J. Mol. Sci. 2026, 27, 2306"
URL_069 = "https://doi.org/10.3390/ijms27052306"

add("Ethyl-1-(4-methylbenzyl)-1,4-dihydroindeno[1,2-b]pirrole-3-carboxilate","melting_point",107.0,"106–108 °C",
    SRC_069,URL_069,"Section 4.1.3 compound 11",
    "FC purification (petroleum benzine/EtOAc: 8/2) furnished 11 as a white solid (750 mg, 64.99%), mp = 106–108 ◦ C",
    value_min=106, value_max=108, notes="Compound 11")
add("Ethyl-6-methyl-1-(4-methylbenzyl)-1,4-dihydroindeno[1,2-b]pirrole-3-carboxilate","melting_point",128.0,"127–129 °C",
    SRC_069,URL_069,"Section 4.1.4 compound 12",
    "FC purification (petroleum benzine/EtOAc: 9/1) furnished 12 as a yellow solid (680 mg, 57.05%), mp = 127–129 ◦ C",
    value_min=127, value_max=129, notes="Compound 12")
add("1-(4-Methylbenzyl)-1,4-dihydroindeno[1,2-b]pirrole-3-carboxilic acid","melting_point",233.0,"232–234 °C",
    SRC_069,URL_069,"Section 4.1.6 compound 13",
    "13 as a white solid (380 mg, 99.73%), mp = 232–234 ◦ C",
    value_min=232, value_max=234, notes="Compound 13")
add("6-Methyl-1-(4-methylbenzyl)-1,4-dihydroindeno[1,2-b]pirrole-3-carboxilic acid","melting_point",231.0,"230–232 °C",
    SRC_069,URL_069,"Section 4.1.7 compound 14",
    "14 as a white solid (300 mg, 75.75%), mp = 230–232 ◦ C",
    value_min=230, value_max=232, notes="Compound 14")

# =====================
# Paper 070 - PCNA Inhibitor AOH1996 Analogs (Molecules 2026, 31, 862)
# =====================
SRC_070 = "Molecules 2026, 31, 862"
URL_070 = "https://doi.org/10.3390/molecules31050862"

p070_data = [
    ("2-(4-(3-Chloropropyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",113.5,"112–115 °C",112,115,"1a","White crystals, m.p. 112–115 ◦ C (iPrOH), Yield 2 g (74%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-phenyl-1H-1,2,3-triazol-1-yl)acetamide",84.5,"83–86 °C",83,86,"1b","White crystals, m.p. 83–86 ◦ C (iPrOH), Yield 1 g (50%)."),
    ("2-(4-(4-Fluorophenyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",106.0,"104–108 °C",104,108,"1c","White crystals, m.p. 104–108 ◦ C (iPrOH), Yield 1.5 g (54%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-(4-methoxyphenyl)-1H-1,2,3-triazol-1-yl)acetamide",139.5,"138–141 °C",138,141,"1d","White crystals, m.p. 138–141 ◦ C (iPrOH), Yield 2 g (69%)."),
    ("2-(4-(4-Ethylphenyl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",122.5,"121–124 °C",121,124,"1e","White crystals, m.p. 121–124 ◦ C (iPrOH), Yield 2.1 g (56%)."),
    ("2-(4-([1,1'-Biphenyl]-4-yl)-1H-1,2,3-triazol-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",157.0,"156–158 °C",156,158,"1f","White crystals, m.p. 156–158 ◦ C (iPrOH), Yield 2.0 g (63%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-(4-(4-pentylphenyl)-1H-1,2,3-triazol-1-yl)acetamide",78.5,"77–80 °C",77,80,"1g","White crystals, m.p. 77–80 ◦ C (EtOH), Yield 1.8 g (57%)."),
    ("2-(Dimethylamino)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",55.0,"54–56 °C",54,56,"2a","White crystals, m.p. 54–56 ◦ C (cyclohexane), Yield 1.7 g (83%)."),
    ("2-(Aziridin-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",76.5,"75–78 °C",75,78,"2b","White crystals, m.p. 75–78 ◦ C (cyclohexane), Yield 1.5 g (63%)."),
    ("2-(Azetidin-1-yl)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",92.5,"91–94 °C",91,94,"2c","White crystals, m.p. 91–94 ◦ C (iPrOH), Yield 1.7 g (73%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-(pyrrolidin-1-yl)acetamide",89.5,"88–91 °C",88,91,"2e","White crystals, m.p. 88–91 ◦ C (iPrOH), Yield 1.5 g (67%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-(piperidin-1-yl)acetamide",90.5,"89–92 °C",89,92,"2f","White crystals, m.p. 89–92 ◦ C (iPrOH), Yield 1.5 g (80%)."),
    ("N-(2-(3-Methoxyphenoxy)phenyl)-2-morpholinoacetamide",115.5,"114–117 °C",114,117,"2g","White crystals, m.p. 114–117 ◦ C (iPrOH), Yield 1.8 g (78%)."),
    ("N-(2-((2-(3-Methoxyphenoxy)phenyl)amino)-2-oxoethyl)-4-nitrobenzamide",135.0,"134–136 °C",134,136,"3a","Yellowish crystals, m.p. 134–136 ◦ C (iPrOH), Yield 2.5 g (80%)."),
    ("2-Fluoro-N-(2-((2-(3-methoxyphenoxy)phenyl)amino)-2-oxoethyl)benzamide",94.0,"93–95 °C",93,95,"3b","White crystals, m.p. 93–95 ◦ C (iPrOH), Yield 2.5 g (80%)."),
    ("N-(2-((2-(3-Methoxyphenoxy)phenyl)amino)-2-oxoethyl)-4-phenylbutanamide",107.5,"106–109 °C",106,109,"3d","White crystals, m.p. 106–109 ◦ C (iPrOH), Yield 2.7 g (90%)."),
    ("2-((4,6-Dichloro-1,3,5-triazin-2-yl)amino)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",162.0,"160–164 °C",160,164,"3e","White crystals, m.p. 160–164 ◦ C (iPrOH), Yield 0.67 g (22%)."),
    ("2-((6-Chloro-1,2,4,5-tetrazin-3-yl)amino)-N-(2-(3-methoxyphenoxy)phenyl)acetamide",167.5,"166–169 °C",166,169,"3f","Orange crystals, m.p. 166–169 ◦ C (iPrOH), Yield 0.62 g (32%)."),
]
for nm,val,vraw,vmin,vmax,code,qt in p070_data:
    add(nm,"melting_point",val,vraw,SRC_070,URL_070,f"Section 4 synthesis compound {code}",
        qt, value_min=vmin, value_max=vmax, notes=f"Compound {code}")

# =====================
# Paper 074 - NHC Gold complexes (IJMS 2026, 27, 2032)
# =====================
SRC_074 = "Int. J. Mol. Sci. 2026, 27, 2032"
URL_074 = "https://doi.org/10.3390/ijms27042032"

add("Chlorido-[1,3-dimethyl-4-anisyl-5-(4-chlorophenyl)imidazole-2-ylidene]gold(I)","melting_point",210.5,"210–211 °C",
    SRC_074,URL_074,"Section 3 complex 5",
    "Yield: 66 mg (0.12 mmol, 81%); amber solid of m.p. 210–211 ◦ C", value_min=210, value_max=211, notes="Complex 5")
add("Iodido-[1,3-dimethyl-4-anisyl-5-(4-chlorophenyl)imidazole-2-ylidene]gold(I)","melting_point",190.5,"190–191 °C",
    SRC_074,URL_074,"Section 3 complex 6",
    "Yield: 56 mg (0.088 mmol, 80%); off-white solid of mp 190–191 ◦ C", value_min=190, value_max=191, notes="Complex 6")

# =====================
# Paper 075 - Pyrazole derivatives (Antibiotics 2026, 15, 127)
# =====================
SRC_075 = "Antibiotics 2026, 15, 127"
URL_075 = "https://doi.org/10.3390/antibiotics15020127"

p075 = [
    ("N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-fluoroaniline",144.5,"144–145 °C",144,145,"4a","Yield 88%; mp 144–145 ◦ C; Rf 0.85"),
    ("N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-chloroaniline",156.5,"156–157 °C",156,157,"4b","Yield 70%; mp 156–157 ◦ C; Rf 0.83"),
    ("N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-bromoaniline",123.5,"123–124 °C",123,124,"4c","Yield 92%; mp 123–124 ◦ C; Rf 0.81"),
    ("N,N-bis-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-fluoroaniline",83.5,"82–85 °C",82,85,"5a","Yield 91%; mp 82–85 ◦ C; Rf 0.78"),
    ("N,N-bis-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-chloroaniline",101.5,"101–102 °C",101,102,"5b","Yield 84%; mp 101–102 ◦ C; Rf 0.55"),
    ("N,N-bis-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-bromoaniline",113.5,"113–114 °C",113,114,"5c","Yield 86%; mp 113–114 ◦ C; Rf 0.63"),
    ("N,N-bis-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-4-iodoaniline",99.5,"99–100 °C",99,100,"5d","Yield 79%; mp 99–100 ◦ C; Rf 0.24"),
    ("N-[(1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline",104.0,"103–105 °C",103,105,"6a","Yield 68%; mp 103–105 ◦ C; Rf 0.84"),
    ("N-[(3,5-dimethyl-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline",109.0,"108–110 °C",108,110,"6b","Yield 91%; mp 108–110 ◦ C; Rf 0.69"),
    ("N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline",79.0,"78–80 °C",78,80,"6c","Yield 70%; mp 78–80 ◦ C; Rf 0.85"),
    ("N-[(3,5-dimethyl-4-nitro-1H-pyrazol-1-yl)-methyl]-2,4-dichloroaniline",137.0,"136–138 °C",136,138,"6d","Yield 93%; mp 136–138 ◦ C; Rf 0.88"),
    ("N-[(3,5-dimethyl-1H-pyrazol-1-yl)-methyl]-2,6-dichloroaniline",109.0,"108–110 °C",108,110,"6e","Yield 35%; mp 108–110 ◦ C; Rf 0.79"),
    ("N-[(3,5-dimethyl-4-iodo-1H-pyrazol-1-yl)-methyl]-2,6-dichloroaniline",81.5,"81–82 °C",81,82,"6f","Yield 51%; mp 81–82 ◦ C; Rf 0.76"),
    ("N-[(3,5-dimethyl-4-nitro-1H-pyrazol-1-yl)-methyl]-2,6-dichloroaniline",112.5,"112–113 °C",112,113,"6g","Yield 86%; mp 112–113 ◦ C; Rf 0.85"),
]
for nm,val,vraw,vmin,vmax,code,qt in p075:
    add(nm,"melting_point",val,vraw,SRC_075,URL_075,f"Section synthesis compound {code}",
        qt, value_min=vmin, value_max=vmax, notes=f"Compound {code}")

# =====================
# Paper 078 - bis-isoxazole monoterpenic
# =====================
SRC_078 = "Turk. J. Chem.; doi:10.55730/1300-0527.3324"
URL_078 = "https://doi.org/10.55730/1300-0527.3324"

add("(R)-2-methyl-5-(5-methyl-3-(p-tolyl)-4,5-dihydroisoxazol-5-yl)cyclohex-2-en-1-one","melting_point",97.0,"96-98 °C",
    SRC_078,URL_078,"Table 2 row 2",
    "m.p: 96-98 °C", value_min=96, value_max=98, notes="Compound 2 (Table 2)")
add("(3aS,5R,7aR)-7a-methyl-5-(5-methyl-3-(p-tolyl)-4,5-dihydroisoxazol-5-yl)-3-(p-tolyl)-3a,4,5,6-tetrahydrobenzo[d]isoxazol-7(7aH)-one","melting_point",112.0,"112±2 °C",
    SRC_078,URL_078,"Section 2 compound 3 synthesis",
    "Yield 11%; white solid: mp = 112±2 °C (Ethanol)", value_min=110, value_max=114, notes="Compound 3")

# =====================
# Paper 079 - Anti-T. cruzi triazoles (Molecules 2023, 28, 7461)
# =====================
SRC_079 = "Molecules 2023, 28, 7461"
URL_079 = "https://doi.org/10.3390/molecules28227461"

add("2-Chloro-1-(2,4-difluorophenyl)ethanone","melting_point",46.5,"46–47 °C",
    SRC_079,URL_079,"Section 4.1.1 compound 4",
    "melting point: 46–47 ◦ C (lit. 46–48 ◦ C [19])", value_min=46, value_max=47, notes="Compound 4 (intermediate)")
add("1-(2,4-Difluorophenyl)-2-(3-nitro-1H-1,2,4-triazol-1-yl)ethanone","melting_point",118.0,"117–119 °C",
    SRC_079,URL_079,"Section 4.1.2 compound 5",
    "Yield: 73%; melting point: 117–119 ◦ C (lit. 113–114 ◦ C [16])", value_min=117, value_max=119, notes="Compound 5")
add("1-(2,4-Difluorophenyl)-2-(2-nitro-1H-imidazol-1-yl)ethanone","melting_point",129.0,"128–130 °C",
    SRC_079,URL_079,"Section 4.1.3 compound 6",
    "Measured melting point: 128–130 ◦ C", value_min=128, value_max=130, notes="Compound 6")
add("1-(2,4-Difluorophenyl)-2-(1H-1,2,4-triazol-1-yl)ethanone","melting_point",104.5,"104–105 °C",
    SRC_079,URL_079,"Section 4.1.4 compound 7",
    "melting point: 104–105 ◦ C (lit. 104–105 ◦ C [19])", value_min=104, value_max=105, notes="Compound 7")
add("1-(2,4-Difluorophenyl)-2-(3-nitro-1H-1,2,4-triazol-1-yl)ethanol","melting_point",128.5,"128–129 °C",
    SRC_079,URL_079,"Section 4.1.5 compound 8",
    "Yield: 92%; melting point: 128–129 ◦ C", value_min=128, value_max=129, notes="Compound 8")
add("1-(2,4-Difluorophenyl)-2-(2-nitro-1H-imidazol-1-yl)ethanol","melting_point",185.0,"184–186 °C",
    SRC_079,URL_079,"Section 4.1.6 compound 9",
    "melting point: 184–186 ◦ C", value_min=184, value_max=186, notes="Compound 9")
add("1-(2,4-Difluorophenyl)-2-(1H-1,2,4-triazol-1-yl)ethanol","melting_point",120.0,"119–121 °C",
    SRC_079,URL_079,"Section 4.1.7 compound 10",
    "Melting point: 119–121 ◦ C (lit. 118–120 ◦ C [18])", value_min=119, value_max=121, notes="Compound 10")

# =====================
# Paper 081 - Azo-CMP polymer (J. Polym. Res. 2021)
# =====================
SRC_081 = "J. Polym. Res. 2021; doi:10.1007/s10965-021-02803-8"
URL_081 = "https://doi.org/10.1007/s10965-021-02803-8"
add("3,6-dinitro-9-ethylcarbazole","melting_point",244.5,"244-245 °C",
    SRC_081,URL_081,"Synthesis section Cz-2NO2",
    "(Cz-2NO2) as yellow solid 5.16 g (85 %). mp: 244-245 °C.", value_min=244, value_max=245,
    notes="Compound abbreviated Cz-2NO2 in paper")

# =====================
# Paper 083 - 2-Ethoxy-4H-3,1-benzoxazin-4-one (Pharmaceuticals 2011, 4, 1032-1051)
# =====================
SRC_083 = "Pharmaceuticals 2011, 4, 1032-1051"
URL_083 = "https://doi.org/10.3390/ph4071032"

add("2-Ethoxy-3-(2-hydroxyethyl)quinazolin-4-one","melting_point",108.5,"108–109 °C",
    SRC_083,URL_083,"Section synthesis compound 3",
    "2-Ethoxy–3-(2-hydroxyethyl)quinazolin–4–one (3). Light brown crystals from ethanol; m.p. 108–109 °C",
    value_min=108, value_max=109, notes="Compound 3")
add("2-Ethoxycarbonylamino-N-(2-bromophenyl)benzamide","melting_point",105.5,"105-106 °C",
    SRC_083,URL_083,"Section synthesis compound 4e",
    "2-Ethoxycarbonylamino-N-(2-bromophenyl)benzamide (4e): Brown crystals from ethanol; m.p. 105-106 °C",
    value_min=105, value_max=106, notes="Compound 4e")
add("2-Ethoxy-3-(4-methoxyphenyl)quinazolin-4-one","melting_point",114.5,"114–115 °C",
    SRC_083,URL_083,"Section synthesis compound 5b",
    "2-Ethoxy-3-(4-methoxyphenyl)quinazolin-4-one (5b): Dark brown crystals from toluene; m.p. 114–115",
    value_min=114, value_max=115, notes="Compound 5b (text quotes m.p. 114-115; °C inferred from convention)")
add("2-Ethoxy-3-(4-hydroxyphenyl)quinazolin-4-one","melting_point",105.5,"105–106 °C",
    SRC_083,URL_083,"Section synthesis compound 5c",
    "2-Ethoxy-3-(4-hydroxyphenyl)quinazolin-4-one (5c): Dark brown crystals from benzene; m.p. 105–106",
    value_min=105, value_max=106, notes="Compound 5c")
add("4-[2-Ethoxy-4-quinazolon-3-yl]benzoic acid","melting_point",151.5,"151–152 °C",
    SRC_083,URL_083,"Section synthesis compound 6a",
    "4-[2-Ethoxy-4-quinazolon-3-yl]benzoic acid (6a): Light brown crystals from ethanol; m.p. 151–152 °C",
    value_min=151, value_max=152, notes="Compound 6a")
add("2-Ethoxy-3-(4-aminophenyl)quinazolin-4-one","melting_point",105.5,"105–106 °C",
    SRC_083,URL_083,"Section synthesis compound 6b",
    "2-Ethoxy-3-(4-aminophenyl)quinazolin-4-one (6b): Light blue crystal from ethanol; m.p. 105–106 °C",
    value_min=105, value_max=106, notes="Compound 6b")

# Write CSV
with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(HEADER)
    for r in rows:
        writer.writerow([r[h] for h in HEADER])

print(f"Wrote {len(rows)} rows to {OUT}")
print(f"id range: 3000-{3000+len(rows)-1}")

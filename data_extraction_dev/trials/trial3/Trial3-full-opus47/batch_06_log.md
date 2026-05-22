# Batch 06 extraction log

Batch list: 15 PMC papers (169-183) + 4 historical PDFs (1952, 1990, 2000, 2005) + 11 "_out.txt"/"_clean.txt" intermediate-file entries skipped (not papers).

Total rows extracted: 143 (verification_status = pending_verification).

| Paper | Rows | DOI / identifier | Notes |
|-------|------|------------------|-------|
| 169 PMC11843341 (triazole-indole-pyrazolones) | 15 | 10.1021/acsbiomedchemau.4c00060 | All 5a-5o synthesized derivatives, mp ranges 150–242 °C |
| 170 PMC11843339 (mycophenolic acid analogues) | 7 | 10.1021/acsbiomedchemau.4c00079 | 2a, 2c, 2d, 2e, 4b, 4c, 6a; dropped 3a/3c (only bare codes available) |
| 171 PMC11206658 (1,2-dihydroisoquinolines) | 6 | 10.3390/molecules29122917 | 2e, 4af, 4ag/4da, 4ah, 4ba, 4ca |
| 172 PMC11209911 (ieodomycin intermediates) | 8 | 10.1021/acsomega.4c03241 | 26a, 26b, 26c, 26d and their 26x-1 dioxan analogues |
| 173 PMC10914095 (rotaxane) | 0 | 10.1039/d4ra00566j | Only "rotaxane 1" bare-code reference; dropped per drop rules |
| 174 PMC11203676 (coumarin sulfonamides) | 11 | 10.3390/ijms25126803 | Compounds 2, 10a, 11a-c, 12a, 13a-c, 14a-c |
| 175 PMC11206905 (naphthothiazole-4,9-diones) | 7 | 10.3390/molecules29122777 | 3, 5a-5e, PNT |
| 176 PMC11206253 (triazoline glucose) | 10 | 10.3390/molecules29122839 | 8a-8j (β-D-glucose tetraacetyl derivatives) |
| 177 PMC11206731 (carbonyl selenides) | 0 | 10.3390/molecules29122866 | No mp/bp reported |
| 178 PMC11208899 (Cu-MOF benzoxanthenones) | 3 | 10.1039/d4ra03468f | 4h, 4i, 4j (full IUPAC names); 4a-4g have bare codes only in table 2 (dropped) |
| 179 PMC10763744 (BODIPY probe) | 1 | 10.55730/1300-0527.3325 | BOD-AP probe |
| 180 PMC12943207 (PEGylation review) | 0 | 10.3390/molecules31040675 | Review paper; only generic ester mixtures (HLB X.X), not compounds |
| 181 PMC10806150 (geranylacetone derivs) | 11 | 10.3389/fchem.2023.1303479 | Compounds 1a-1l (no 1k extracted: same name as 1j per paper text) |
| 182 PMC10804403 (amodiaquine process) | 5 | 10.1021/acs.oprd.3c00205 | Compounds 9, 10, 5, 12, 3; dropped compound 14 (Mannich base — no specific IUPAC name in paper) |
| 183 PMC9007260 (isatin derivatives) | 11 | 10.1134/S1070428022030101 | 1a-1c, 2a-2b, 3a-3d, 4a-4b; several reported as decomp. |
| 1952 Livingston (methylcyclobutane) | 1 | legacy (no DOI) | f.p. = -161.51° (mp). bp value lost to OCR corruption |
| 1990 Yalkowsky | 0 | legacy | PDF image-only; pdftotext output empty |
| 2000 Brown (mp & symmetry) | 47 | legacy (DOI not in pdftotext) | All compounds in Tables 1, 2, 3 (K → °C converted). Compiled from CRC Handbook; data_type=measured |
| 2005 Yalkowsky | 0 | legacy | Dissertation; tables are group-contribution fragments, no compound-mp pairs |

## Phase 3 results

`run_all_checks.py` exit codes (all PASS / advisory-only):
- csv_quote_lint: 0
- quote_template_lint: 0
- quote_support_lint: 0 (advisory notes only: compound names with very long prefixes — serial codes verify identity)
- validate_compound_name: 0
- value_range_check: 0
- unit_conversion_arithmetic: 0
- dedup_within_paper: 0
- placeholder-citation: 0

DOI / evidence-quote verification SKIPPED (no --paper-root passed; would need full corpus path).

## Known limitations / flags

- Rows 72 & 77 (paper 181, 1a & 1f): paper prints the mp range in reverse order ("119°C–114°C", "145°C–139°C"). value_celsius is midpoint; min/max are sorted; note recorded.
- Rows 88-94 (paper 183): mp followed by "(decomp.)" — values stored as melting_point with notes recording decomposition.
- Rows 91, 92, 98 (paper 183): ">300°C" → relation=`>`, value_celsius=300.
- Row 99 (paper 1952): bp lost to OCR corruption ("3F.98" → 36.98 unreadable verbatim); only mp row kept.
- Rows 100-146 (paper 2000): Kelvin → °C conversions per Table 1/2/3 of Brown's teaching paper; data_type=measured (Brown compiled from CRC Handbook).
- Row 145 (hexamethylenetetramine): paper text reads ">523" K, recorded with relation=`>`, value_celsius=249.85.

## Phase 4

Not run (out of scope for this subagent batch). All rows retain `pending_verification` status.

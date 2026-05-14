# batch_00 extraction log

Batch covers 21 papers; total rows emitted: 358.

| Paper | PMC | rows_emitted | rows_flagged | status / notes |
|---|---|---|---|---|
| 001 | PMC12938810 | 10 | 0 | mp's for AL1–AL10 caffeine-thio-propanehydrazide series |
| 003 | PMC12943044 | 16 | 0 | mp's for compounds 2,3,4,5,6a-c,7a-c,8a-c,9a-c (HQ-phthalimide hybrids) |
| 004 | PMC13084458 | 16 | 0 | DSC mp's for 3a–3p piperazine-thioureas |
| 005 | PMC12987641 | 24 | 0 | mp's for 9a-d,9f-m,10e,11a,11c-i,11k-m indenoquinoline phosphine oxides |
| 006 | PMC13006720 | 14 | 0 | mp's for compounds 7–20 nitrofuryl-thiadiazole piperidines |
| 007 | PMC13093257 | 1 | 0 | Only compound 3 has mp in main text; 6a-r mp's were in SI (not provided) |
| 008 | PMC12944436 | 9 | 0 | mp's for terpene-imatinib hybrids 6a–6i |
| 009 | PMC12943507 | 13 | 0 | mp's for arylazo pyrazole carboxamides 5a–5m |
| 010 | PMC12940417 | 28 | 0 | mp's for TRPA1 compounds 1,6,10,11–34 (dropped 2 entries with non-contiguous compound IDs: cmpd 8 and cmpd 28) |
| 011 | PMC12943719 | 55 | 0 | mp's for PDE4 inhibitors 2a–2w, 3a–3l, 4a-g, 5a-l, 7, 9, 10a, 10b (one 2n is decomposition) |
| 012 | PMC12987640 | 8 | 0 | mp's for σ1R/HDAC duals 2a-d, 3a-b, 4a-b |
| 013 | PMC12943095 | 34 | 0 | mp's for benzo[c]chromene precursors and 5a–5s |
| 014 | PMC12943640 | 35 | 1 | bisphosphonic acids 1–35; compound 16 flagged (OCR truncated range '244–24 °C') |
| 015 | PMC12943364 | 5 | 0 | mp's for PB01–PB05 PB2/JAK2 dual inhibitors |
| 017 | PMC10673250 | 9 | 0 | Tm's from DSC table for L-Glu alkyl ester [HCl] and [IBU] salts |
| 018 | PMC10672206 | 2 | 0 | Chol-phthalonitrile (186 °C) and Chol-ZnPc (>300 °C) |
| 019 | PMC11203683 | 15 | 0 | mp's for phosphacoumarin 1, 2a–2m, 3 |
| 020 | PMC11206691 | 39 | 0 | mp's / decomp for HBV RNase H series A, B, 1–5, 6, 7, 8, 9–13, 33–60 (many decomposition values reported) |
| 021 | PMC10673159 | 15 | 0 | mp's for terphenyl sulfinyl methanones 10a–10o |
| 022 | PMC9764318 | 1 | 0 | Only compound 3a (2,3-Diphenyl quinoxaline) has an explicit IUPAC name in the main text; remaining table entries (3b–3q) lack standalone names in the body, so dropped to avoid bare-code rows |
| 023 | PMC9790764 | 9 | 0 | mp's for adamantyl diureas 4a–4i |

Totals
- Papers contributing rows: 21 (all)
- Papers with NO mp/bp data: 0
- INACCESSIBLE papers: 0
- Total rows emitted: 358
- Rows flagged_review: 1 (row 244, paper 014, compound 16 OCR-truncated value)

Phase 3 deterministic check result: **all Tier-1 hard checks PASS**
- validate_compound_name.py: exit 0
- value_range_check.py: exit 0
- unit_conversion_arithmetic.py: exit 0 (after normalizing 'X°C–Y°C' format value_raw fields and resolving rows 244 and 328)
- dedup_within_paper.py: exit 0
- placeholder-citation check: 0 flagged
- csv_quote_lint: clean

Tier-2 advisory flags (quote_support_lint / verify_evidence_quote) remain on rows where the compound is referenced by a serial code (e.g. '4c', '10b', 'PB02') and the local quote does not embed the full IUPAC name. These are acceptable per skill v1.6 (advisory only; not auto-dropped).

Fixes applied after Phase 3 run:
- ~70 paper-5 rows had `value_raw` like "200°C–202°C"; normalized to "200–202 °C" so the K/°F-conversion check parses the range correctly (no value changes; only string formatting).
- row 244: value_raw '244–24 °C' kept as printed (flagged), value_celsius set to 244 with empty min/max so the range-parser does not infer a wrong midpoint; status = flagged_review.
- row 328: value_raw '> 250 °C (dec.: 200 °C)' simplified to '> 250 °C' (decomposition note moved to `notes`) so the conversion check sees a single value.

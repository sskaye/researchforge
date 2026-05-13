# Verification of 100-row random sample

## Sampling

- Source file: `melting_boiling_points.csv`
- Sample size: 100 rows from 438 data rows
- Random seed: `20260511`
- Sample file used during audit: `/private/tmp/verification_sample.csv`

## Verification method

For PMC articles, I reopened the local `article.nxml` or `article_text.txt` and checked the compound identity against the surrounding section title, experimental paragraph, or table row/column headers. For PDF-only articles, I extracted the PDF text with the bundled Python `pypdf` package and checked the relevant table or experimental entry. I did not treat the CSV evidence snippet alone as sufficient; each sampled row was checked back against the article source context.

For Kelvin values, I independently checked the conversion to °C by subtracting 273.15. For table records with method-specific properties, I checked that the property suffix (for example `STRM`, `SIRM`, `experimental`, `calculated`, or cycle/peak/onset labels) matched the table column or table caption.

## Results

- Updated strict compound-name wrong rows: 11/100 = 11.0%
- Updated strict compound-name correct rows: 89/100 = 89.0%
- Previous, overly permissive score: 4/100 = 4.0% wrong. That only counted names that disagreed with the source context; it did not count names that were source-faithful but unusable without reading the paper.
- Cleanup-only rows: 59/100 have article-local labels, citations, or similar clutter appended to an otherwise interpretable compound name. I did not include these in the 11.0% wrong rate unless the compound identity itself was not standalone-interpretable, but they should be cleaned before the final table is considered useful.
- Error type observed: all strict wrong sampled rows had incorrect or insufficient compound names. I did not find a sampled row where the DOI or numeric temperature conversion was wrong after the row was tied to the correct source context.

## Updated Compound-Name Scoring

For the updated score, I treated `compound_name` as correct only if it can be interpreted as a specific compound without consulting the article. It is not enough for the row to be traceable when the verifier reopens the paper. A final table user needs the name itself to carry the identity.

I counted a row as wrong when the name was a section title, prose fragment, compound range, generic derivative label, or unresolved local reference such as `complex of compound 4`; or when it depended on undefined substituent variables such as `X` and `R`. I counted a row as cleanup-only, not wrong, when the full chemical name was present but followed by removable local labels or citations such as `(5e)`, `, 2n [36]`, or `(compound 6)`.

The stricter wrong set is:

- Original source-context name errors: samples 19, 79, 94, and 98.
- Undefined R-group/table-label names: samples 37, 46, 59, 71, and 74.
- Unresolved complex-of-local-compound name: sample 60.
- Generic derivative name: sample 69.

## Error analysis

The errors came from fallback name selection. When the parser could not confidently identify a compound name in a paragraph, it sometimes used the nearest section title or a prose heading as the compound name. This produced bad rows in three contexts:

1. `064` narrative discussion paragraphs: values for Dexamethasone and Thalidomide were real Tm values, but the recorded compound name became `Result and discussion`.
2. `020` characterization paragraph for compound 37: the value was correct, but the compound name fell back to the section title `N-Hydroxypyridinedione Oximes 33–50`.
3. `141` prose property list: the value `mp 109.5 °C` belongs to Tyrindoleninone, but the recorded compound name was a nearby prose fragment.

The stricter review found a second failure mode: the extractor sometimes preserved article-local identifiers instead of resolving them into standalone compound identities. These rows were traceable in the source paper but not usable in a standalone CSV. Examples include `1j (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=Cl, R=4-isoC3H7)`, `Pb(II) complex of compound 4 (complex 8)`, and `benzoxanthenone derivative 4i`.

This suggests the extraction skill should require an explicit compound-name source and reject generic section titles/prose fragments as names. A useful validator would blacklist names like `Results and discussion`, names beginning with generic section labels, names that use ranges such as `2a-g`, names containing unresolved variables like `X=` or `R=`, and names containing unresolved local-reference phrases like `derivative 4a` or `complex of compound 4`.

## Observations for Skill Design

The extractor needs a compound identity resolution step, not just a nearby-name capture step. A good workflow would be:

1. Capture the temperature-bearing row or paragraph.
2. Identify the local compound label, if present.
3. Resolve that label against nearby experimental headings, characterization paragraphs, tables, schemes, captions, or supplementary material.
4. Record only a standalone compound name in `compound_name`.
5. Keep article-local labels, method names, and citations out of `compound_name`; optionally store them in a separate `compound_label` field.

For R-group tables, the skill should not write names like `1a (...; X=H, R=H)` unless it can also resolve where `X` and `R` attach on the scaffold. If the article gives a scheme or structure diagram but no textual name, the safe behavior is either to reconstruct a fully specified name only when unambiguous or skip the row. A name with unresolved variables is not final-table quality.

For metal complexes, the skill should resolve the ligand identity and the complex identity. `Hg(II) complex of compound 4` or `Pb(II) complex of compound 4` is not enough because `compound 4` is local to the paper. The final name needs the ligand name and, when available, metal, stoichiometry, counterions, and hydration/solvation state. If those cannot be recovered from text or tables, the row should be rejected rather than emitted with a local pointer.

For generic derivative tables, a row such as `benzoxanthenone derivative 4i` is wrong unless `4i` is resolved to the full product name. In article `178`, the full names for 4h-4j appear in the characterization text, so those can be recovered by cross-referencing. The older known products 4a-4g may require table structures, schemes, or cited literature; if the structure is only graphical and not text-resolvable, those rows should be treated as not safely extractable.

Finally, post-processing should strip non-name clutter from otherwise valid names: local compound labels like `(5e)`, table labels after commas like `, 2w`, citations like `[36]`, phrases like `compound 6`, and method/procedure text like `Method 2`. These labels are useful for verification but should not live in the final `compound_name` field.

## Sample findings

| Sample | CSV row | Status | Recorded compound | Property | Temp °C | Verification note |
|---:|---:|---|---|---|---:|---|
| 1 | 279 | OK | Umifenovir | melting_point_SIRM | 175.45 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 2 | 151 | OK | 5-(1-(((3,5-Difluorophenyl)(pyridin-2-yl)methoxy)imino)ethyl)-1,6-dihydroxy-4-methylp… | melting_point | 102-104 | NXML characterization paragraph checked; leading compound name and m.p. value match. |
| 3 | 74 | OK | 5-Acetyl-4-(3,5-difluorophenylamino)-2-ethyl-6-phenylpyridazin-3(2H)-one, 2w | melting_point | 243-245 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 4 | 255 | OK | Favipiravir | boiling_point_SIRM | 415.72 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 5 | 275 | OK | Thalidomide | melting_point_STRM | 168.34 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 6 | 374 | OK | [MOC2-MPip][zBF3] | melting_point_experimental | -16.0 | PDF text extracted with pypdf and table/experimental entry checked. |
| 7 | 67 | OK | 5-Acetyl-2-ethyl-6-phenyl-4-[(pyridin-2-ylmethyl)-amino]pyridazin-3(2H)-one, 5h | melting_point | 138-140 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 8 | 213 | OK | Methyl rac-(2′R,3aS,4′S,6R,9aR)-5″-bromo-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-di… | melting_point | 260-262 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 9 | 191 | OK | Ethyl rac-(2′R,3aS,4′R,7S,9aR)-1′-ethyl-1,3-dimethyl-2,2″,8-trioxo-3a,9a-diphenyl-1,2… | melting_point | 244-246 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 10 | 298 | OK | 7-(3-Chloro-4-fluorophenyl)-9-(4-methoxyphenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyri… | melting_point | 219-221 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 11 | 190 | OK | Ethyl rac-(2′R,3aS,4′R,7S,9aR)-1,1′,3-trimethyl-2,2″,8-trioxo-3a,9a-diphenyl-1,2,3,3a… | melting_point | 253-255 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 12 | 120 | OK | 9-methoxy-6-(4-nitrobenzyl)-6H-benzo[c]chromene (5e) | melting_point | 123 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 13 | 52 | OK | 5-Acetyl-2-ethyl-4-(4-nitrophenylamino)-6-phenylpyridazin-3(2H)-one, 2p | melting_point | 209-211 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 14 | 38 | OK | 4-(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)naphthalene-1-carbo… | melting_point | 258-260 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 15 | 438 | OK | 1-Cyclohexyl-3-cyclohexylimino-1H,3H-[1,2,4]thiadiazolo[4,3-a]benzimidazole (2c) | melting_point | 116 | PDF text extracted with pypdf and table/experimental entry checked. |
| 16 | 356 | OK | [EMIm][NO3] | melting_point_subsequent_cycles_peak | 46.6 | PDF text extracted with pypdf and table/experimental entry checked. |
| 17 | 57 | OK | 5-Acetyl-2-ethyl-4-(naphthalen-1-ylamino)-6-phenylpyridazin-3(2H)-one, 3l | melting_point | 196-198 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 18 | 54 | OK | 5-Acetyl-2-ethyl-4-(6-hydroxynaphthalen-1-ylamino)-6-phenylpyridazin-3(2H)-one, 3d | melting_point | 235-236 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 19 | 270 | WRONG | Result and discussion | melting_point | 251.45 | Compound name is wrong. Source paragraph says this value is the reported Tm for Dexamethasone: 524.60 K = 251.45 °C; CSV compound name is the section title "Result and discussion". |
| 20 | 98 | OK | 1-(6-(2-bromophenyl)benzo[d][1,3]dioxol-5-yl)-2-(4-nitrophenyl)ethan-1-ol (3d) | melting_point | 168 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 21 | 382 | OK | [N1,1,1,16][fCO2] | melting_point_experimental | 198.5 | PDF text extracted with pypdf and table/experimental entry checked. |
| 22 | 403 | OK | [N2,2,2,2][AlCl4] | melting_point_calculated | 139.4 | PDF text extracted with pypdf and table/experimental entry checked. |
| 23 | 84 | OK | 5-Acetyl-4-butylamino-2-ethyl-6-phenylpyridazin-3(2H)-one, 4g | melting_point | 67-69 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 24 | 257 | OK | Favipiravir | melting_point_SIRM | 223.91 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 25 | 59 | OK | 5-Acetyl-2-ethyl-4-[(4-methylisoxazol-3-ylmethyl)-amino]-6-phenylpyridazin-3(2H)-one,… | melting_point | 113-115 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 26 | 408 | OK | [N2,2,2,6][ONf] | melting_point_experimental | 157.0 | PDF text extracted with pypdf and table/experimental entry checked. |
| 27 | 283 | OK | 1,4-Di(4-methoxyphenyl)-N-ethoxymethylene-2-amino-3-cyanopyrrole (6c) | melting_point | 117-118 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 28 | 34 | OK | 3-(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)-benzonitrile, 2f | melting_point | 226-227 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 29 | 145 | OK | 2-(But-3-yn-1-yloxy)isoindoline-1,3-dione (7) | melting_point | 104 | NXML characterization paragraph checked; leading compound name and m.p. value match. |
| 30 | 363 | OK | [EMPyr][ONf] | melting_point_calculated | 49.6 | PDF text extracted with pypdf and table/experimental entry checked. |
| 31 | 300 | OK | 7-(4-Chlorophenyl)-9-phenyl-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine (3c) | melting_point | 218-220 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 32 | 214 | OK | Methyl rac-(2′R,3aS,4′S,6R,9aR)-6″-chloro-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-d… | melting_point | 260-261 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 33 | 171 | OK | 5-methyl-1,3,4-oxadiazole -2(3H)-thione (4) | melting_point | 68 | NXML synthesis/table context checked; compound identity and M.P. value match. |
| 34 | 351 | OK | [C4MPyr][BF4] | melting_point_subsequent_cycles_onset | 150.6 | PDF text extracted with pypdf and table/experimental entry checked. |
| 35 | 202 | OK | Methyl rac-(2′R,3aS,4′R,6R,9aR)-1′-isopropyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-dipheny… | melting_point | >300 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 36 | 43 | OK | 5-Acetyl-2-ethyl-4-(3-fluorophenyl)-6-phenylpyridazin-3(2H)-one, 9 | melting_point | 127-128 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 37 | 225 | WRONG | 1j (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=Cl, R=4-isoC3H7) | melting_point | 205-207 | Temperature matches Table 2, but compound name is not standalone because X/R attachment positions are only defined by the article scaffold/table. |
| 38 | 210 | OK | Methyl rac-(2′R,3aS,4′S,6R,9aR)-1,1′,3-trimethyl-2,2″,7-trioxo-3a,9a-diphenyl-1,2,3,3… | melting_point | 231-232 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 39 | 235 | OK | Baricitinib | boiling_point_SIRM | 486.93 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 40 | 414 | OK | [N4,4,4,4][Bz,z,z,MO] | melting_point_experimental | 134.0 | PDF text extracted with pypdf and table/experimental entry checked. |
| 41 | 44 | OK | 5-Acetyl-2-ethyl-4-(3-fluorophenylamino)-6-phenylpyridazin-3(2H)-one, 2b | melting_point | 174-175 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 42 | 321 | OK | 2-(Thiocyanomethylthio)Benzothiazole | boiling_point | >120 | NXML biocide subsection checked; TCMTB boiling point is stated as >120 °C. |
| 43 | 111 | OK | 6-(4-nitrobenzyl)-6H-[1,3]dioxolo[4′,5′:4,5]benzo[1,2-c]chromene (5d) | melting_point | 186 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 44 | 436 | OK | 1,1'-(1,2-Phenylene)bis(3-cyclohexylthiourea) (1c) | melting_point | 185 | PDF text extracted with pypdf and table/experimental entry checked. |
| 45 | 297 | OK | 7-(3-Chloro-4-fluoropheny)l-9-(4-chlorophenyl)tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrim… | melting_point | 220-222 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 46 | 218 | WRONG | 1c (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=H, R=3,4-Cl2) | melting_point | 199-201 | Temperature matches Table 2, but compound name is not standalone because X/R attachment positions are only defined by the article scaffold/table. |
| 47 | 416 | OK | [N4,4,4,4][Fap] | melting_point_first_cycle_onset | 54.3 | PDF text extracted with pypdf and table/experimental entry checked. |
| 48 | 80 | OK | 5-Acetyl-4-(4-chlorophenylamino)-2-ethyl-6-phenylpyridazin-3(2H)-one, 2k | melting_point | 183-184 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 49 | 405 | OK | [N2,2,2,2][zBF3] | melting_point_calculated | 61.6 | PDF text extracted with pypdf and table/experimental entry checked. |
| 50 | 56 | OK | 5-Acetyl-2-ethyl-4-(8-hydroxyquinolin-5-ylamino)-6-phenylpyridazin-3(2H)-one, 3h | melting_point | 261-262 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 51 | 48 | OK | 5-Acetyl-2-ethyl-4-(4-methoxybenzylamino)-6-phenylpyridazin-3(2H)-one, 5a | melting_point | 106-107 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 52 | 127 | OK | [Glu(OPr)2][HCl] | melting_point | 91.12 | NXML Table 2 row checked against compound column and Tm column. |
| 53 | 182 | OK | Ethyl rac-(2′R,3aS,4′R,6R,9aR)-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-diphenyl-1,2… | melting_point | >300 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 54 | 3 | OK | (2E,4E)-5-(3-(Cinnamyloxy)phenyl)-N-isobutylpenta-2,4-dienamide (23) | melting_point | 131-133 | NXML experimental subsection and paragraph checked; compound title and Mp value match. |
| 55 | 301 | OK | 7-(4-Chorophenyl)-9-phenyl-7H-triazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine (4a) | melting_point | 256-258 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 56 | 264 | OK | Fingolimod | melting_point_literature | 127 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 57 | 346 | OK | [4M-MTr][ClO4] | melting_point_experimental | 61.3 | PDF text extracted with pypdf and table/experimental entry checked. |
| 58 | 401 | OK | [N1,4,4,4][CN] | melting_point_calculated | 103.6 | PDF text extracted with pypdf and table/experimental entry checked. |
| 59 | 224 | WRONG | 1i (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=Cl, R=3,4-Cl2) | melting_point | 189-190 | Temperature matches Table 2, but compound name is not standalone because X/R attachment positions are only defined by the article scaffold/table. |
| 60 | 179 | WRONG | Pb(II) complex of compound 4 (complex 8) | melting_point | 78 | Temperature matches table context, but name depends on local compound 4 and complex 8 labels; ligand/complex identity is not standalone. |
| 61 | 245 | OK | Chloroquine | boiling_point_SIRM | 409.5 | NXML Table 5 checked; K value converts to recorded °C and method suffix matches table column. |
| 62 | 37 | OK | 4-(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)benzoic Acid, 2n [3… | melting_point | 252 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 63 | 173 | OK | 5-methyl-1,3,4-thiadiazol-2(3H)-thione (compound 6) | melting_point | 153 | NXML synthesis/table context checked; compound identity and M.P. value match. |
| 64 | 349 | OK | [C4MPyr][BF4] | melting_point_first_cycle_onset | 150.2 | PDF text extracted with pypdf and table/experimental entry checked. |
| 65 | 105 | OK | 6-(2-nitrobenzyl)-6H-benzo[c]chromene (5j) | melting_point | 154 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 66 | 198 | OK | Ethyl rac-(2′R,3aS,4′S,6R,9aR)-5″-bromo-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-dip… | melting_point | 244-245 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 67 | 433 | OK | [bItaz][OTos] | melting_point_calculated | 98.8 | PDF text extracted with pypdf and table/experimental entry checked. |
| 68 | 114 | OK | 6-(5-methyl-2-nitrobenzyl)-6H-benzo[c]chromene (5o) | melting_point | 187 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 69 | 341 | WRONG | benzoxanthenone derivative 4i | melting_point | 185-187 | Temperature matches product 4i, but `benzoxanthenone derivative 4i` is a generic local-label name; full product name appears elsewhere and should have been resolved. |
| 70 | 97 | OK | 1-(2′-bromo-[1,1′-biphenyl]-2-yl)-2-(4′-nitro-[1,1′-biphenyl]-4-yl)ethan-1-ol (4k) | melting_point | 138 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 71 | 229 | WRONG | 2b (2-methyl-3-phenylquinazoline-4(3H)-thione; X=Cl, R=3-Cl) | melting_point | 172-173 | Temperature matches Table 2, but compound name is not standalone because X/R attachment positions are only defined by the article scaffold/table. |
| 72 | 343 | OK | [3M-MTr][ClO4] | melting_point_calculated | 93.1 | PDF text extracted with pypdf and table/experimental entry checked. |
| 73 | 17 | OK | (E)-3-([1,1′-Biphenyl]-4-yl)-N-(adamantan-1-yl)acrylamide (31) | melting_point | 171-173 | NXML experimental subsection and paragraph checked; compound title and Mp value match. |
| 74 | 228 | WRONG | 2a (2-methyl-3-phenylquinazoline-4(3H)-thione; X=Cl, R=H) | melting_point | 153-154 | Temperature matches Table 2, but compound name is not standalone because X/R attachment positions are only defined by the article scaffold/table. |
| 75 | 136 | OK | 1,6-Dihydroxy-5-(1-(((3-methoxybenzyl)oxy)imino)ethyl)-4-methylpyridin-2(1H)-one (35) | melting_point | 120-122 | NXML characterization paragraph checked; leading compound name and m.p. value match. |
| 76 | 192 | OK | Ethyl rac-(2′R,3aS,4′R,7S,9aR)-5″-bromo-1,1′,3-trimethyl-2,2″,8-trioxo-3a,9a-diphenyl… | melting_point | 231-232 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 77 | 211 | OK | Methyl rac-(2′R,3aS,4′S,6R,9aR)-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-diphenyl-1,… | melting_point | 247-249 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 78 | 91 | OK | 1-(2′-bromo-5-fluoro-[1,1′-biphenyl]-2-yl)-2-(4-nitrophenyl)ethan-1-ol (3i) | melting_point | 112 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 79 | 169 | WRONG | N-Hydroxypyridinedione Oximes 33–50 | melting_point | 118-120 | Compound name is wrong. Source paragraph identifies compound 37, N-(2-(3,5-difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)furan-2-carboxamide; CSV used the section title. |
| 80 | 200 | OK | Methyl rac-(2′R,3aS,4′R,6R,9aR)-1,1′,3-trimethyl-2,2″,7-trioxo-3a,9a-diphenyl-1,2,3,3… | melting_point | 295-297 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 81 | 130 | OK | [Glu(Osec-Bu)2][HCl] | melting_point | 51.69 | NXML Table 2 row checked against compound column and Tm column. |
| 82 | 397 | OK | [N1,1,1,f][MSO3] | melting_point_calculated | 84.8 | PDF text extracted with pypdf and table/experimental entry checked. |
| 83 | 92 | OK | 1-(2′-bromo-5-methyl-[1,1′-biphenyl]-2-yl)-2-(4-nitrophenyl)ethan-1-ol (3c) | melting_point | 67 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 84 | 400 | OK | [N1,2,i3,i3][NTf2] | melting_point_experimental | 140.0 | PDF text extracted with pypdf and table/experimental entry checked. |
| 85 | 428 | OK | [S1,f,f][OTf] | melting_point_subsequent_cycles_peak | 98.5 | PDF text extracted with pypdf and table/experimental entry checked. |
| 86 | 292 | OK | 7,9-Di(4-chlorophenyl)-7H-tetrazolo[1,5-c]-7H-pyrrolo[3,2-e]pyrimidine (3k) | melting_point | 224-225 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 87 | 174 | OK | 5-methyl-1,3,4-thiadiazol-2(3H)-thione/thiol (6) | melting_point | 153 | NXML synthesis/table context checked; compound identity and M.P. value match. |
| 88 | 36 | OK | 4-(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydro-pyridazin-4-ylamino)benzoic Acid Ethyl… | melting_point | 171-173 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 89 | 189 | OK | Ethyl rac-(2′R,3aS,4′R,6S,9aR)-6″-chloro-1′-ethyl-1,3-dimethyl-2,2″,7-trioxo-3a,9a-di… | melting_point | 280-282 | NXML characterization paragraph checked; leading compound name and mp value match. |
| 90 | 121 | OK | 9-methyl-6-(4-nitrobenzyl)-6H-benzo[c]chromene (5c) | melting_point | 133 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 91 | 170 | OK | 4-amino-5-methyl-2H-1,2,4-triazole-3-thiol (7) | melting_point | 115 | NXML synthesis/table context checked; compound identity and M.P. value match. |
| 92 | 290 | OK | 3-Amino-4-imino-5-(4-methoxyphenyl)-7-phenyl-7H-pyrrolo[2,3-d]pyrimidine (7b) | melting_point | 193-195 | NXML/PDF-derived experimental text checked; compound entry and mp value match. |
| 93 | 131 | OK | 1,6-Dihydroxy-4-methyl-5-(1-(((4(methylthio)benzyl)oxy)imino)ethyl)pyridin-2(1H)-one … | melting_point | 110-115 | NXML characterization paragraph checked; leading compound name and m.p. value match. |
| 94 | 310 | WRONG | The precursors of the purple | melting_point | 109.5 | Compound name is wrong. Source text identifies Tyrindoleninone: red needles, mp 109.5 °C; CSV used prose fragment "The precursors of the purple". |
| 95 | 119 | OK | 9-fluoro-6-(4-nitrobenzyl)-6H-benzo[c]chromene (5i) | melting_point | 144 | NXML experimental paragraph checked; leading compound name and Mp value match. |
| 96 | 75 | OK | 5-Acetyl-4-(3-bromophenylamino)-2-ethyl-6-phenylpyridazin-3(2H)-one, 2d | melting_point | 189-190 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 97 | 71 | OK | 5-Acetyl-2-ethyl-6-phenyl-4-phenylaminopyridazin-3(2H)-one, 2a | melting_point | 187-189 | NXML chemistry subsection and characterization paragraph checked; compound title and mp value match. |
| 98 | 271 | WRONG | Result and discussion | melting_point | 270 | Compound name is wrong. Source paragraph says this value is the reported Tm for Thalidomide: 543.15 K = 270.00 °C; CSV compound name is the section title "Result and discussion". |
| 99 | 364 | OK | [EMPyr][ONf] | melting_point_experimental | 176.0 | PDF text extracted with pypdf and table/experimental entry checked. |
| 100 | 95 | OK | 1-(2′-bromo-[1,1′-biphenyl]-2-yl)-2-(4,5-dimethoxy-2-nitrophenyl)ethan-1-ol (4d) | melting_point | 76 | NXML experimental paragraph checked; leading compound name and Mp value match. |

## Wrong sampled rows

- Sample 19, CSV row 270: Compound name is wrong. Source paragraph says this value is the reported Tm for Dexamethasone: 524.60 K = 251.45 °C; CSV compound name is the section title "Result and discussion".
- Sample 37, CSV row 225: Temperature matches Table 2, but `1j (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=Cl, R=4-isoC3H7)` is not standalone because the X/R positions are defined only in the article.
- Sample 46, CSV row 218: Temperature matches Table 2, but `1c (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=H, R=3,4-Cl2)` is not standalone because the X/R positions are defined only in the article.
- Sample 59, CSV row 224: Temperature matches Table 2, but `1i (2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione; X=Cl, R=3,4-Cl2)` is not standalone because the X/R positions are defined only in the article.
- Sample 60, CSV row 179: Temperature matches table context, but `Pb(II) complex of compound 4 (complex 8)` depends on local article labels and does not name the ligand/complex in a standalone way.
- Sample 69, CSV row 341: Temperature matches product 4i, but `benzoxanthenone derivative 4i` is a generic local-label name. The full product name is available elsewhere in the article and should have been resolved.
- Sample 71, CSV row 229: Temperature matches Table 2, but `2b (2-methyl-3-phenylquinazoline-4(3H)-thione; X=Cl, R=3-Cl)` is not standalone because the X/R positions are defined only in the article.
- Sample 74, CSV row 228: Temperature matches Table 2, but `2a (2-methyl-3-phenylquinazoline-4(3H)-thione; X=Cl, R=H)` is not standalone because the X/R positions are defined only in the article.
- Sample 79, CSV row 169: Compound name is wrong. Source paragraph identifies compound 37, N-(2-(3,5-difluorophenyl)-2-(((1-(1,2-dihydroxy-4-methyl-6-oxo-1,6-dihydropyridin-3-yl)ethylidene)amino)oxy)ethyl)furan-2-carboxamide; CSV used the section title.
- Sample 94, CSV row 310: Compound name is wrong. Source text identifies Tyrindoleninone: red needles, mp 109.5 °C; CSV used prose fragment "The precursors of the purple".
- Sample 98, CSV row 271: Compound name is wrong. Source paragraph says this value is the reported Tm for Thalidomide: 543.15 K = 270.00 °C; CSV compound name is the section title "Result and discussion".

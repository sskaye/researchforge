# Batch 05 Extraction Log

## Summary
- Papers processed: 20 (148, 149, 151-158, 160-169)
- Rows extracted: 65
- Skipped papers (no extractable mp/bp): 5 (148, 154, 162-partial, 166, 167)
- Flags after Phase 3 checks: 0 blocking; 10 advisory (compound-name token not in quote span for paper 161 Table 1 rows — acceptable per protocol since table cells are compressed and quote is the contiguous span containing both substituent code and value)

## Per-paper notes

- **148** PCL review (PMC10671727): Skipped. Review-cited PCL Tm "about 60 °C" and "51 °C [259]" are vague/cited; no original measurement.
- **149** SNMICON 2024 Abstracts (PMC11831906): 3 mp rows (Mebrofenin 205, Mannose triflate 118-120, L,L-EC 225-232).
- **151** Pyranoxanthone (PMC6263260, Molecules 2011, 16, 3999-4004): 6 mp rows (soulattrin, caloxanthone B, C, macluraxanthone, friedelin, stigmasterol).
- **152** Thio-oxocrown ethers (PMC6264337, Molecules 2011, 16, 8670): 2 mp rows (B3 63-64, B5 93-94). Others are oils.
- **153** Niobate ionic liquids (PMC3692303, Int J Mol Sci 2007, 8, 392): Skipped 4 ionic mixture mp values and 3 coumarin product mp values — table cells too compressed for contiguous quote + compound name; mixtures only identified by composition mol%, coumarin products by entry number/phenol precursor only.
- **154** Silicoaluminates polymerization (PMC5513518, Materials 2010, 3, 1015): Skipped. Single Tm ~134 °C for polyethylene products with no individual compound name.
- **155** Pyranoxanthones Mesua beccariana (PMC6259158, Molecules 2010, 15, 6733): 5 mp rows (mesuarianone, mesuasinone, stigmasterol, friedelin, betulinic acid).
- **156** Cordycepin (PMC7123108, Biology of Macrofungi 2019): 1 mp row from Table 16.1.
- **157** Dehydrocholic acid clathrates (PMC3716435, Int J Mol Sci 2007, 8, 662): 4 host mp rows from Table 3 (dehydrocholic acid Tm 244, 243, 243, 244 in clathrate A-D).
- **158** Philinopgenins (PMC3783257, Mar Drugs 2004, 2, 185): 3 mp rows (A 208.5, B 212.5-213.5, C 216.5-217.5). Philinopgenin A reported as "208.5-208.5" (apparent typo).
- **160** Pyrazolylmethyl aminoethane (PMC6147103, Molecules 2003, 8, 780): 2 mp rows (ligand 82-84, Cu(II) complex 188-190).
- **161** Imidoyl azides (PMC6146427, Molecules 2002, 7, 189): 10 decomposition rows from Table 1 (substituent codes 1-10, decomp T 77-120 °C). Compound names use substituent encoding; quote contiguous from table cell. Advisory only.
- **162** Nitroxide radicals (PMC5521752, Materials 2010, 3, 3625): 1 mp row (MeO-TEMPO 313 K = 39.85 °C).
- **163** Caledonixanthone (PMC6146543, Molecules 2002, 7, 38): 1 mp row (Caledonixanthone G 201).
- **164** Microbiological problems (PMC7158184, Pulp and Paper Industry 2015): 5 rows — 1,3-dichloro-5,5-dimethylhydantoin mp 159-163, chlorine dioxide mp -59 + bp 11, glutaraldehyde mp -14 + bp 187. All review-cited reference values.
- **165** Pyrophosphoryl chloride acylation (PMC6236387, Molecules 2001, 6, 279): 6 mp rows (anthraquinone 284, anthrone 152, 2-methoxyanthraquinone 196, 2-chloroanthraquinone 209, 1-indanone 40, 2-coumaranone 49). Paper uses "°" alone; normalized to "°C".
- **166** Pentacene oligomers (PMC5445842, Materials 2010, 3, 2772): Skipped. mp 272/160 °C for compounds 50/51 are explicitly attributed to ref [71]; Td values in Table 1 use bare numeric codes (27, 59, 60...).
- **167** SciPharm conference posters (PMC3002819): Skipped. Only "NLC mp 45.1 °C" — NLC is a formulation (Nanostructured Lipid Carrier), not a single compound.
- **168** Marine natural products review (PMC3756327, Mar Drugs 2005, 3, 36): 1 mp row (sulfolane 28 °C); review-cited.
- **169** Triazole-indole-pyrazolones (PMC11843341, ACS Bio Med Chem Au 2025, 5, 66): 15 mp rows (compounds 5a-5o).

## Phase 3 check results
All blocking checks pass (exit=0). 10 advisory flags on paper 161 Table 1 rows where quote begins with substituent code rather than full compound name; the substituent code IS a token from the compound name field — advisory only, not blocking.

## Rows by source
- Paper 149: 3
- Paper 151: 6
- Paper 152: 2
- Paper 155: 5
- Paper 156: 1
- Paper 157: 4
- Paper 158: 3
- Paper 160: 2
- Paper 161: 10
- Paper 162: 1
- Paper 163: 1
- Paper 164: 5
- Paper 165: 6
- Paper 168: 1
- Paper 169: 15
- **Total: 65**

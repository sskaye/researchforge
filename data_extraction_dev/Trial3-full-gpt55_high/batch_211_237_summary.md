# Batch 211-237 summary

Protocol: mp-bp-extraction v1.5, direct local-file reading only. Output rows are `pending_verification`; no regex/bulk extraction script was used.

## Per-paper notes

- 211 diaba_2024_dichlorolactams_synthesis.html: emitted 6 melting-point rows from Section 3.1.3 product characterization. Other thermal-looking temperatures were reaction conditions or biological assay values and were skipped.
- 212 fernandes_2018_pyridazine_suzuki.html: emitted 5 melting-point rows from experimental compound characterization for 3a-3e.
- 213 gomezayuso_2024_ugi_nitrogen_heterocycles.html: emitted 0 rows. Local HTML has no compound-characterization mp/bp values; boiling mentions are reaction conditions.
- 214 huang_2026_paracyclophane_ligands.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 215 khalifa_2024_thiopyrimidine_sulfonamide.html: emitted 30 melting-point rows from Sections 3.1.1 and 3.1.5. M1 and M2 omit an explicit unit beside the range; rows retain the printed raw range and note Celsius inferred from melting-point context.
- 216 kim_2026_2quinolone_synthesis.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 217 ledermann_2023_iodoindoles_synthesis.html: emitted 0 rows. The local HTML has a few mp values, but the contiguous evidence text binds them only to bare product codes, so they were dropped under the no-bare-code rule.
- 218 nakanishi_2024_pyridine_ch_arylation.html: emitted 1 melting-point row for 5-octyldibenzo[b,f][1,7]naphthyridin-6(5H)-one.
- 219 norouzi_2024_pyrrole_fused_benzazepine.html: emitted 0 rows. Main local HTML states the apparatus for melting points but does not include individual mp values.
- 220 plourde_2002_oxaspiro_spirolactone.html: emitted 4 melting-point rows from the Experimental section.
- 221 pusztai_2025_thiadiazino_carbazole.html: emitted 7 melting-point rows from the detailed Experimental characterization included in the article body. Supporting-information-only compounds were not accessed/extracted.
- 222 rios_2026_dhpm_vorinostat.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 223 wang_2026_glucosamine_glycosides.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 224 yanovich_2024_spiroheterocycles_rh_catalysis.html: emitted 0 rows. Local HTML did not contain individual mp/bp/decomposition/DSC measurements; thermal-looking hits were reaction conditions or references.
- 225 adrjanowicz_2017_amorphous_fenofibrate.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 226 bock_2024_cardarine_polymorphs.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 227 chmielewska_2020_API_fatty_alcohol_eutectic.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 228 dichi_2025_polyphenols_thermal.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 229 doan_2021_mechanochemistry_cocrystals.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 230 fini_2013_diclofenac_salts_polymorphism.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 231 gokhale_2016_HME_ASD_clinical_scale.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 232 khan_2017_piroxicam_cocrystal.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 233 khan_2019_diclofenac_ester_cocrystal.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 234 lee_2021_ginsenoside_K_polymorphs.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 235 liu_2024_matrine_salts_thermal.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 236 weng_2020_itraconazole_terephthalic_cocrystal.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.
- 237 wirth_2024_imepitoin_polymorphism.html: flagged paper-level only. Local HTML is a Europe PMC shell/navigation page without readable article body or thermal-property evidence.

Rows emitted: 53.

Flagged paper count: 17 shell-only/unreadable local HTML pages. No CSV data rows were emitted for those papers.

# Batch 151-180 summary

Rows emitted: 70

Flagged rows: 0

Validation note: `mp-bp-extraction/scripts/run_all_checks.py` passed deterministic checks. Source-aware DOI/evidence scripts locate PMC subdirectories but not standalone PDFs kept at the corpus root, so rows from manifest 165 and 178 remain pending verification. Phase 4 independent verification was not available in this single-agent run; rows are left as `pending_verification`.

- manifest 151: Emitted 9 clear MPA analogue melting-point rows from experimental characterization; code-derived names expanded with analogue family context.
- manifest 152: Emitted 6 melting-point ranges from compound characterization paragraphs.
- manifest 153: Emitted 4 sulfonate intermediate melting-point rows; additional similar rows were dropped where not re-confirmed in this pass.
- manifest 154: No rows emitted; candidate rotaxane/alkyne passages had abbreviated/product-code naming that I did not consider sufficiently evidence-locked.
- manifest 155: Emitted 12 chromenyl sulfonamide/chromene melting-point rows from experimental section.
- manifest 156: Emitted 8 naphtho[2,3-d]thiazole-4,9-dione derivative melting-point rows.
- manifest 157: No rows emitted in CSV; paper has many 8-series values, but I did not include them because the PDF/NXML snippets require further quote reconfirmation for each long glycoside name.
- manifest 158: Emitted 2 alpha-carbonyl selenide ester melting-point rows.
- manifest 159: Emitted 3 benzoxanthenone derivative melting-point rows with full compound names.
- manifest 160: Emitted 1 BOD-AP melting-point row.
- manifest 161: Emitted 2 review-reported polyglycerol fatty-acid ester melting-point rows from a contiguous paragraph.
- manifest 162: No rows emitted in CSV; geranylacetone derivative section had several values, but two ranges were internally reversed and I left the paper for review rather than mixing uncertain rows.
- manifest 163: Emitted 6 amodiaquine-process intermediate/product melting-point rows.
- manifest 164: Emitted 10 isatin derivative melting/decomposition rows.
- manifest 165: Emitted methylcyclobutane freezing point and boiling point from sample constants; source has no DOI in file.
- manifest 166: No rows emitted; pypdf extracted essentially no usable text from the PDF.
- manifest 167: No rows emitted; pedagogical/review paper contained compiled examples but no batch rows were added.
- manifest 168: No rows emitted; dissertation contains very large appendix tables that were not safely re-confirmed row-by-row in this pass.
- manifest 169: No rows emitted; synthesis paper has candidate values but compound headings were not fully captured in a contiguous quote during this pass.
- manifest 170: No rows emitted; supporting information/dataset not safely re-confirmed row-by-row.
- manifest 171: No rows emitted; supporting information/dataset not safely re-confirmed row-by-row.
- manifest 172: No rows emitted; QSPR article, no individual evidence-locked extracted values added.
- manifest 173: No rows emitted; QSPR boiling-point article not extracted row-by-row.
- manifest 174: No rows emitted; relationship/review article not extracted row-by-row.
- manifest 175: No rows emitted; prediction article not extracted row-by-row.
- manifest 176: No rows emitted; simulation/comparison article not extracted row-by-row.
- manifest 177: No rows emitted; many EPAC2 characterization values were found but not included without full row-by-row quote verification.
- manifest 178: Emitted 5 thiourea/thiadiazolobenzimidazole melting-point rows.
- manifest 179: No rows emitted; minireview table values not extracted row-by-row.
- manifest 180: No rows emitted; review/prediction article not extracted row-by-row.

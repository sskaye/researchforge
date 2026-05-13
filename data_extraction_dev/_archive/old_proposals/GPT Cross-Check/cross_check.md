# Cross-check of GPT Test and Claude Test extraction tables

## Files compared

- `GPT Test/melting_boiling_points.csv`: 438 rows.
- `Claude Test/mp_bp_extracted.csv`: 517 rows.
- Detailed adjudication table: `comparison.csv`.

I compared the two tables by article, compound identity, property type, and temperature after normalizing obvious representation differences such as ranges versus midpoints. For disagreements, I checked the source article text/NXML or PDF text extraction rather than relying on either table's evidence snippet.

## Headline findings

The two outputs differ for three main reasons:

1. **Scope policy differences**: GPT included open-bound values, calculated/predicted values, and multiple DSC event values. Claude generally kept exact measured or literature experimental values and skipped open bounds and predicted values.
2. **Compound-name quality**: GPT has more severe standalone-name failures, including section titles, prose fragments, unresolved `compound N` references, and generic derivative labels. Claude is usually better on names but still has unresolved R-group names and several generic product-code names.
3. **Missed article/table coverage**: GPT missed the entire Dearden PDF table of experimental BP/MP values. Claude skipped the entire API thermodynamics article because it treated the paper as prediction-only.

## Article-level summary

| Article | GPT rows | Claude rows | Main difference | Adjudication |
|---|---:|---:|---|---|
| 010 TRPA1 | 31 | 29 | GPT has one duplicate, one bad compound name, and one open-bound value Claude skipped. | Claude cleaner; GPT captures the `>270 °C` row if open bounds are in scope. |
| 011 PDE4 | 55 | 55 | Same apparent coverage; representation differs. | No major cross-check issue found. |
| 013 benzocchromenes | 34 | 34 | Same apparent coverage; representation differs. | No major cross-check issue found. |
| 017 ibuprofen salts | 9 | 9 | Same apparent coverage. | No major cross-check issue found. |
| 020 HPD oximes | 39 | 32 | GPT includes open bounds but has name errors; Claude skips open bounds and has one unresolved `compound 3`. | Mixed; needs policy and name cleanup. |
| 026 nucleoside analogs | 11 | 8 | GPT duplicates ligands and leaves complexes as `compound 4/6`; Claude resolves ligand names but skips `>300`. | Claude better for names; GPT captures an open-bound value. |
| 028 dispiro compounds | 35 | 31 | GPT includes four `>300` rows; Claude skips them. | Policy difference on open bounds. |
| 050 quinazoline thiones | 19 | 18 | GPT has one spurious series-heading row; both keep unresolved X/R labels. | Claude avoids the extra row; both need R-group resolution or rejection. |
| 064 API thermodynamics | 47 | 0 | GPT includes predicted STRM/SIRM Tb/Tm and literature Tm; Claude skips article. | Scope ambiguity. If calculated/literature values are in scope, GPT is closer but has two bad prose-derived names. |
| 138 pyrrolopyrimidines | 27 | 27 | Same apparent coverage. | No major cross-check issue found. |
| 141 Tyrian purple | 3 | 4 | GPT names are prose fragments; Claude resolves compounds and captures an extra 6-bromoisatin value. | Claude correct. |
| 157 dehydrocholic acid | 8 | 8 | Same values; GPT has DOI, Claude has PMCID; Claude names host-melting rows more precisely. | Merge: use GPT DOI and Claude-style names. |
| 164 microbiological control | 10 | 11 | GPT duplicates chlorine dioxide, misnames BCDMH, misses several biocides, and drops `50% aqueous` qualifier. | Claude substantially better. |
| 178 benzoxanthenones | 13 | 10 | GPT duplicates 4h-4j and generic names; Claude better but still generic for 4b-4g. | Claude better; unresolved products should be resolved or skipped. |
| 2009 Dearden | 0 | 196 | GPT missed Table 2 experimental BP/MP values. | Claude correct for experimental columns. |
| 2011 Krossing | 92 | 40 | GPT includes calculated values and multiple DSC cycle/peak/onset events; Claude keeps curated experimental Tfus/literature values. | Claude better for measured-constants table; GPT values need `data_origin`/`thermal_event` fields if retained. |
| 2014 Schmittel | 5 | 5 | Same apparent coverage. | No major cross-check issue found. |

## Most important specific discrepancies

- **GPT missed Dearden entirely**: The PDF has Table 2 with experimental boiling points and melting points for a 100-compound test set. Claude extracted 100 BP and 96 MP values; four MP cells are `NA`. GPT recorded zero rows. Root cause: GPT treated a QSPR review as aggregate/prediction-only and did not inspect the per-compound table.
- **Claude skipped API thermodynamics entirely**: Article 064 has per-compound Table 5 values for predicted Tb/Tm and cited literature Tm values. GPT extracted them with method suffixes. This is a scope-policy disagreement, not a simple numeric error. The skill needs a user-visible distinction between measured, literature-cited, and predicted/calculated values.
- **GPT compound-name failures**: Confirmed section/prose fallbacks include `Result and discussion`, `The minor components in the purple`, `The precursors of the purple`, `Halogen-Release Biocides`, and `N-Hydroxypyridinedione Oximes 33-50`.
- **Both outputs have unresolved structured-name problems**: The quinazoline table records names with `X=` and `R=` substituents, but the final CSV does not specify where those groups attach. These are table-correct but not standalone compound names.
- **GPT duplicated rows from table + prose fusion**: Examples include ligand rows in article 026, chlorine dioxide in article 164, and benzoxanthenone 4h-4j in article 178.
- **Claude often uses midpoints**: Claude's numeric `value_celsius` collapses ranges like `212-214` to `213`. That is convenient for modeling, but it loses the printed range unless the original string is also preserved.

## Root causes

1. **Unspecified extraction scope**: The two tests made different choices about open bounds, ranges, predicted values, literature-cited values, and auxiliary DSC events.
2. **No standalone-name validator**: Both pipelines sometimes accepted names that are only meaningful inside the paper.
3. **Weak cross-reference resolution**: Local labels such as `compound 4`, `4i`, or `X/R` table variables were not consistently resolved against schemes, headings, or characterization text.
4. **Evidence-window errors**: Nearby prose or adjacent compound blocks were sometimes captured as provenance or even as names.
5. **No table-level reconciliation**: Whole tables were missed or over-extracted when article type was misclassified.

## Recommendations for a reliable skill

Use a stricter schema:

- `compound_name`: standalone chemical/common/material name only.
- `compound_label`: article-local label such as `4i`, `compound 37`, `Table 2 row 1a`.
- `property_type`: `melting_point` or `boiling_point`.
- `value_original_text`: exact printed value, including ranges and qualifiers.
- `value_c_min`, `value_c_max`, `value_c_midpoint`, `temperature_relation`: normalized numeric representation.
- `data_origin`: `measured_by_article`, `literature_cited`, `predicted_calculated`, or `unknown`.
- `thermal_event`: `melting`, `boiling`, `decomposition`, `DSC_onset`, `DSC_peak`, etc.
- `evidence_text`: source text containing both the resolved label/name and value, or a table reference plus row/column headers.

Implement extraction as a multi-pass workflow:

1. Enumerate all candidate MP/BP mentions and table columns before extracting rows.
2. Build a local compound-label map from headings, schemes, tables, captions, and characterization paragraphs.
3. Resolve each candidate row through that map.
4. Reject names that are section headings, plural/range labels, unresolved `compound N` references, unresolved `X/R` variables, or generic `derivative 4a` labels.
5. Deduplicate across inline text and tables using normalized article, compound label, property, value, and evidence location.
6. Reconcile row counts against detected candidate mentions/tables and require an explicit skip reason for every candidate not emitted.

For high precision, the skill should default to **measured/literature experimental values only**, while allowing an explicit mode to include predicted/calculated values. Open bounds should be retained structurally rather than discarded, because `>270 °C` is still useful data when labeled correctly.

# Extraction notes for `mp_bp_dev_set`

## Output files

- `melting_boiling_points.csv`
- `extraction_notes.md`

## Scope and standard used

The goal was high-precision extraction of compound-level melting point and boiling point data. I only recorded values when the article text gave enough context to connect a compound, material, or table row identifier to an MP/BP value. I omitted aggregate model-error statistics, mentions of MP/BP as modeling targets, and vague value ranges that were not tied to a specific compound.

Temperature values in the CSV are in degrees Celsius. Values reported in Kelvin were converted by subtracting 273.15 and rounded to two decimals where needed. Ranges are retained as ranges. Inequality values such as `>300` were retained.

## Files and parsing approach

1. Inventoried `mp_bp_dev_set` and confirmed 16 PMC article directories with NXML/text/PDF plus 4 PDF-only articles.
2. Used NXML as the primary source for PMC papers because it preserves front-matter DOI, section titles, paragraphs, and tables.
3. For inline experimental values, used explicit patterns such as `mp`, `m.p.`, `Mp`, `melting point`, `boiling point`, `Tm`, `Tb`, and `Tfus` followed by a numeric value and unit.
4. Used the nearest compound-specific section title when available. Where experimental paragraphs began with a full compound name followed by a compound label, used that paragraph opening as the compound name.
5. Parsed key tables manually/structurally where the data were table-dominant or where the NXML table text joined headers and values awkwardly.
6. Used the bundled Python runtime with `pypdf` for PDF-only papers because `pdftotext` was unavailable.
7. De-duplicated records on article, compound name, property, value, and DOI so repeated table/inline values do not create duplicate rows.

## Article-level decisions

- `010`: Extracted inline synthesis/characterization melting points from compound-specific sections.
- `011`: Extracted inline synthesis/characterization melting points; corrected for values under section titles beginning `Synthesis of Compound ...`.
- `013`: Extracted inline melting points where the paragraph begins with the compound name and label.
- `017`: Extracted Table 2 `Tm (°C)` values. Rows with `Tm` shown as `-` were omitted.
- `020`: Extracted inline `m.p.` values from compound characterization paragraphs beginning `The compound ... was synthesized`.
- `026`: Extracted table values for ligands/complexes and inline values not covered by the physical-property tables.
- `028`: Extracted inline `mp` values for compounds 4, 5, 6, and 11 series. Six long compound-name rows in the 11 series needed manual addition because internal stereochemical parentheses confused the automatic name boundary.
- `050`: Extracted Table 2 melting points. Because the article table uses compound IDs plus substituent columns, compound names are recorded as compound ID plus series name and `X/R` substituents.
- `056`: No compound-specific boiling/melting points were recorded; the paper discusses prediction datasets/modeling rather than article-level compound records suitable for this CSV.
- `058`: No records retained; the candidate hit was an aggregate low-melting-point performance statement, not a compound-level value.
- `064`: Extracted Table 5 `Tb` and `Tm` values for STRM, SIRM, and literature/reference `Tm` columns, converting K to °C. Properties are labeled with method suffixes.
- `138`: Extracted narrative/experimental melting points from compound-specific entries.
- `141`: Extracted three prose melting point records where the compound context was recoverable.
- `157`: Extracted Table 3 host melting `Tm` and pure guest boiling `Tb` values. The local NXML had no DOI, so I verified the DOI from the MDPI article page: `10.3390/i8070662`.
- `164`: Extracted physical-property values for named biocides and Table 8.8 chlorine dioxide MP/BP values.
- `178`: Extracted Table 2 product melting points for benzoxanthenone derivatives 4a-4j and inline characterization values for new compounds 4h-4j; duplicates were removed where applicable.
- `2008_Mitchell`: No compound-level MP/BP values retained; the PDF is a modeling comparison paper with aggregate model statistics.
- `2009_Dearden`: No compound-level BP records retained; tables summarize QSPR studies/classes and errors, not individual compound boiling points.
- `2011_Krossing`: Extracted Table 1 measured melting points and Tables 6/7 experimental/calculated compound-specific melting points. Values were already in °C in the PDF text.
- `2014_Schmittel`: Extracted five PDF-only inline melting points from the experimental section.

## Verification performed

- Parsed the final CSV with Python `csv.DictReader`.
- Confirmed 438 data rows and no blank compound names or temperature fields.
- Confirmed all rows have DOIs after filling the DOI for `157`.
- Reviewed per-article record counts to catch missing article groups and false positive modeling records.

## Known limitations

- For some table-only articles, the article provides compound IDs and substituent tables rather than full IUPAC names in extractable text. I used the article's compound ID plus available series/substituent context instead of inventing names from structures.
- For prediction/modeling papers, I retained compound-specific experimental/calculated MP rows when explicitly listed in tables, but omitted model-performance metrics and dataset-level summaries.
- The CSV includes an `article` column in addition to the requested fields to make auditing easier.

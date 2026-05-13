# MP/BP Extraction Notes

A running log of methods, decisions, surprises, and quality concerns for the melting/boiling-point extraction across the 20-article `mp_bp_dev_set`. The goal of these notes is to support skill design and error root-causing.

## Scope and decisions (confirmed with user up front)

- **Ranges** (e.g., "mp 154–156 °C"): record midpoint as `value_celsius` (155). Range is recoverable from the captured `source_text`.
- **Non-°C units** (K, °F): convert to °C in `value_celsius`; also store `value_original` and `unit_original`.
- **Thermal events to include**: melting point (`mp`/`m.p.`), boiling point (`bp`/`b.p.`), decomposition temperatures, and DSC `Tm`. Glass transition (`Tg`) and crystallization (`Tc`) are excluded.
- **Measurement / instrument columns**: `measurement_type` ∈ {melt, decomp, melt_or_decomp, boil}. `instrument` ∈ {DSC, unk, …}. "melt_or_decomp" is for values reported as <!-- fmc:1 -->"mp 245 (dec)"<!-- /fmc:1 --> where both phenomena are implicated. "boil" is the natural extension for `bp` rows (no melt/decomp distinction applies there).
- **Prediction/modeling papers**: only extract per-compound experimental MP/BP values cited inside the paper. Aggregate statistics ("mean MAE 35 °C") are not extracted.

## CSV schema

| column | description |
| --- | --- |
| compound_name | name as printed in the article (IUPAC, common, or compound code) |
| value_celsius | numeric °C; midpoint of any range; converted from K/°F if needed |
| value_original | numeric value as printed in the article (e.g., 154 if range was 154–156, or 425.3 if reported in K) |
| unit_original | "°C", "K", or "°F" as printed |
| property_type | "mp" or "bp" |
| measurement_type | "melt", "decomp", "melt_or_decomp" |
| instrument | "DSC" if explicitly stated; "unk" otherwise |
| source_text | exact quoted text from article that supports the row (compound + value + unit) |
| doi | article DOI from metadata.json (or first authoritative source) |
| article_id | folder name in mp_bp_dev_set (provenance + traceability) |

## Source preference order

1. `article.nxml` — preferred for PMC papers because table structure is preserved as XML.
2. `article_text.txt` — pre-extracted plain text for inline values and prose.
3. `article.pdf` (`pdftotext`) — fallback when NXML is absent (loose PDFs).

## Working principles

- **Recall vs. precision**: skewed toward precision. If I cannot verify a value is correctly tied to a compound from the surrounding text, I skip it and note the skip below rather than guessing.
- **Source text is a verbatim quote** from the article that contains the compound name and the numeric value with its unit. This is the audit trail.
- **No fabrication**: if a value or compound name isn't visible in extracted text, I do not invent it.

## Workflow

The 20-article corpus was processed in 4 batches mirroring the README groups:

1. **Table-dominant papers** (026, 178, 050, 157) — processed by parsing the NXML `<table-wrap>` elements directly (a small `nxml_utils.py` helper was written for this; preserved in `work/`). Tables yielded structured compound-code → MP/BP mappings; identities of the compound codes were resolved by reading surrounding prose.
2. **Experimental / synthesis papers** (011, 020, 010, 013, 028, Schmittel) — one was done manually (011) to characterize the regex patterns; the other five were processed by parallel subagents given a strict schema and a verbatim-source-text requirement. Each agent wrote a per-paper JSON file under `work/` plus a per-paper notes file.
3. **Narrative / main-text papers** (138, 164, 141, 017) — same parallel-agent approach. 017 required explicit instruction to skip Tg/Tc (paper mixes thermal events from DSC).
4. **Prediction / modeling + measurement** (058, 056, 2008_Mitchell, 2011_Krossing, 2009_Dearden, 064) — same approach with stricter "aggregate statistics are NOT extractable" rules. Several papers yielded 0 rows (see below).

## Source preference, in practice

For PMC papers, `article_text.txt` and `article.nxml` together carried all the values needed; the PDF was not consulted unless the text/nxml were missing or ambiguous. NXML tables were the gold source for any tabular MP/BP data because cell structure is preserved.

For the 4 loose PDFs (Mitchell, Dearden, Krossing, Schmittel) `pdftotext -layout` was the workhorse. `pdftotext -raw` was needed in one case (Dearden) to disambiguate minus signs that `-layout` mode rendered as "2" — the Dearden agent verified the reconstruction against literature spot-checks for plausibility.

## Per-article observations and skip log

### 026 — seco-acyclo-N-diazolyl-thione nucleosides (8 rows)

- Clean "M.P (°C)" column in two tables (Table 1 for ligand 4 and complexes 8, 9; Table 2 for ligand 6 and complexes 10, 11).
- Compounds 8, 9, 10, 11 are not given explicit IUPAC names in the article; recorded compound_name as "Pb(II) / Hg(II) complex of \[ligand name\] (compound N)" because synthesis text unambiguously identifies the metal and the ligand.
- Compound 10 (Pb-thiadiazole complex) reports `M.P > 300 °C` — **skipped** as open bound.

### 178 — Cu/Vit B3 MOF + benzoxanthenone derivatives (10 rows)

- Table 2 columns "Mp (°C)" gave ranges (e.g., 150–151) for products 4a–4j. Footnote "c" notes that 4a–4g MPs match literature values.
- Article gives explicit IUPAC names only for the new derivatives 4h, 4i, 4j; for 4a–4g the article keeps the code only. For 4a the model substrate is benzaldehyde and the parent scaffold is named in the abstract, so 4a is recorded as "12-phenyl-…tetrahydrobenzo\[a\]xanthen- 11-one"; 4b–4g recorded as "compound 4X (tetrahydrobenzo\[a\]xanthen-11-one derivative)" because the substituent isn't explicitly stated.
- **Caveat**: source_text for 4a–4g uses a paraphrased "Table 2 'Cu-MOF catalyzed synthesis…'" preamble rather than a verbatim slice — the values themselves were taken directly from the NXML cells. Verified in spot-check; flagged as a precision limitation.

### 050 — quinazoline-4-thiones (18 rows)

- Table 1 of paper has the M.p. (°C) values along with X and R substituents. Compound parent scaffold differs by class (1 vs 2); recorded compound_name preserving the X/R details so each row is unambiguous. All inline ranges.

### 157 — Dehydrocholic acid inclusion compounds (8 rows)

- Table 3 has split-header columns: `Guest release T_on`, `Host melting T_m`, `Bp of pure guest T_b`. T_on is a desorption onset (not a bp/mp of any compound) — **skipped**.
- T_m column gives the host (dehydrocholic acid) melting point in four different clathrate environments — recorded as four separate rows because they're separate measurements (243/243/244/244 °C).
- T_b column gives the boiling point of the pure guest solvent — recorded as four bp rows for acetone (56), DMSO (189), NMP (202), DMF (153 °C).
- No DOI in NXML or PDF; PMCID used as identifier (PMC3716435). The likely DOI is 10.3390/i8070662 (MDPI IJMS pattern) but not verified — left as PMCID.

### 011 — PDE4 inhibitors with pyridazinone scaffold (55 rows)

- Densely characterized synthesis paper; every product has an in-line "mp = X–Y °C" entry following the IUPAC name and code. Processed manually with a regex sweep, then full names mapped from section headings.
- One entry (compound 2n) reads "mp = 252 °C dec." — recorded as `melt_or_decomp`.
- Four matches did not auto-resolve a compound name (the regex caught a "Yield = …; mp = …" not preceded by a ", `" pattern); located their compound IDs (3j, 7, 3k, 9) by reading the preceding "Synthesis of Compound …" section header.`

### `020 — N-Hydroxypiridinedione antiviral series (32 rows)`

- `Processed by subagent. 37 m.p. matches; 32 extracted. 5 skipped — all open-bounded >250 °C. 14 entries are annotated "(dec.)" and were encoded as melt_or_decomp. Compound 3 lacks an in-place IUPAC name at the mp line; agent recorded it as "compound 3" per the rules.`

### `010 — TRPA1 multi-scaffold synthesis (29 rows)`

- `Processed by subagent. 32 Mp matches; 29 unique extractions. 3 skipped: one open-bound (>270 °C), two duplicate restatements of the same measurement. Methods state Gallenkamp apparatus → instrument = "unk".`
- `Compounds with parenthetical literature mp comparisons (e.g. "(lit. X °C)") had only the article-measured value extracted; the lit value is in the source_text but not a separate row.`

### `013 — 6H-benzo[c]chromene synthesis (34 rows)`

- `4 carbaldehyde precursors, 11 ethanol intermediates, 19 final products (5a–5s). Two precursors (1b, 1c) reported as oils → no MP, skipped. Stuart SMP3 apparatus → instrument = "unk".`

### `028 — Dispiro imidazothiazolotriazine-pyrrolidin-oxindoles (31 rows)`

- `Long IUPAC names with stereodescriptors preserved verbatim. 4 compounds reported mp: >300 °C — skipped. Compounds 4l/4m are an inseparable diastereomer mixture with a single mp range (205–212 °C) recorded as one entry.`

### `Schmittel — thiadiazoloimidazoles loose PDF (5 rows)`

- `pdftotext two-column layout interleaved compound headings with their data blocks; the agent disambiguated by matching the anal. calcd for CxHyNzSw formula to the named compound in the left column. Molecular masses + mmol quantities cross-validate the assignment.`
- `Caveat: source_text contains "..." abridgements (not a strict verbatim substring of the pdftotext output) — values are still defensible via the elemental analysis check.`

### `138 — Annellation triazole/tetrazole on pyrrolopyrimidines (27 rows)`

- `Despite the README labeling this as "narrative results", the data was actually in a clearly formatted Experimental section. Values printed in two-digit shorthand (e.g. "215-17" → 215-217). Three entries (6d, 7c, 7e) print the range with a space (167- 68°C); preserved verbatim.`

### `164 — Microbiological problems textbook chapter (11 rows: 7 mp + 4 bp)`

- `True narrative style. Negative °C values (chlorine dioxide mp −59, glutaraldehyde mp −14) retained. Glutaraldehyde appears twice in different physical forms (pure vs 50% aqueous) — both kept.`
- `TCMTB skipped — both bp (>120) and mp (<-10) are open bounds. Glutaraldehyde freezing point and Dazomet flash point excluded (different thermal events).`

### `141 — Tyrian Purple (4 rows)`

- `Historical chemistry; mp values appear in prose like "red needles, mp 109.5 °C". 6-Bromoisatin has two literature mp values from different refs printed side-by-side; both rows retained. Tyriverdin skipped — "darkens above 60 °C" and "sublimes at 220 °C without melting" are open bounds / non-melt events.`

### `017 — Ibuprofen amino-acid ester salts (9 rows)`

- `DSC paper with Tg, Tm, and Tc per compound. Only Tm extracted; Tg and Tc explicitly skipped per task scope.`
- `3 compounds had "-" for Tm in Table 2 → no row created.`

### `058 — Drug-like MP prediction (Tetko-style) (0 rows)`

- `Aggregate-only benchmark study. All tables contain RMSE statistics by dataset/model, or functional-group breakdowns. Outlier compound lists are referenced as supplementary, not in the main paper.`

### `056 — AI-powered BP / critical-property prediction (0 rows)`

- `Per-compound values live in Table 4 with the molecule column rendered as PNG images (Figa_HTML.gif, etc.). The compound names are not recoverable from the NXML, the text, or the PDF text layer. Recording values without compound names would violate the schema's compound_name (verbatim) requirement, so 0 rows extracted.`
- `This is an honest skill-design data point: OCR or image-anchored table extraction is required for this style of paper. Plain-text extraction misses everything.`

### `2008_Mitchell — QSPR comparison loose PDF (0 rows)`

- `Aggregate-only. RMSEs, bias, range descriptions — no per-compound experimental mp values inline. Named compounds (naphthacene, diazoxide, …) appear as outlier examples but without inline experimental values. Per-compound data references SI Table SI1, not in the main PDF.`

### `2011_Krossing — universal MP prediction loose PDF (40 rows)`

- `Mixed organic-salt MP data in tables. Several authors-measured DSC values from Table 1 (using the paper's T_e of "subsequent cycles" per their stated convention), plus literature-cited values from Tables 6 (outliers) and 7 (excluded calibration).`
- `Caveat: 3 negative MP values (−1.05, −16, −18 °C). pdftotext rendered the minus sign as a non-printable byte (\x02); agent inferred negative sign from the position + context. Plausible by literature comparison ([C6MIm][NTf2] ≈ −10 °C lit; agent's −1.05 is the paper's reported value not lit), but a residual precision risk exists. Flagged.`

### `2009_Dearden — QSPR review loose PDF (196 rows; 100 bp + 96 mp)`

- `Table 2 of the paper benchmarks 6 prediction programs against 100 organic compounds, listing experimental bp and experimental mp columns. The agent extracted both columns exactly. 4 compounds had "NA" mp (1,2-Dichlorobutane, 2,3-Dimethylpentane, 3-Hexanone, Methyl n-butyl sulfide) — no row created.`
- `Critical pdftotext gotcha: minus glyph rendered as ASCII "2" in -layout mode. Agent used -raw mode where each token is on its own line; the minus appears as a standalone "2" preceding the number, allowing reconstruction. Sanity-checked: acetone mp −94.3 °C matches literature (−95 °C); 1-butanal −96 matches literature.`
- `Caveat: source_text for some negative-MP rows shows the table row context (compound name + many numeric columns) but the specific reconstructed minus-sign value may not literally appear in the source_text substring. The value is correct (verified by -rawreconstruction + literature) but the audit chain has one extra hop. Flagged for the 2 sample rows that triggered the verification function (1-Butanal, Vinyl bromide).`

### `064 — Thermodynamic properties of COVID APIs (0 rows)`

- `Despite the title, this is a prediction/modeling paper: applies Hukkerikar group-contribution method to estimate Tm for 9 APIs. The paper does not measure any thermal property; Table 5 cites literature Tm values from refs [47]–[58] for ARD calculation. Per the rule "skip literature-cited values unless the paper explicitly remeasured them", 0 rows extracted.`
- `This is interesting as a misclassification example: the manifest groups it as "other / measurement" but it is functionally a prediction paper.`

## `Aggregate counts`

`Total rows: 517 across 16 papers (4 of the 20 yielded 0 rows).`

`By property type:`

- `mp: 409 (382 melt, 27 melt_or_decomp)`
- `bp: 108 (all "boil")`

`By source kind:`

- `PMC dirs (NXML + text): 14 papers, 276 rows`
- `Loose PDF: 4 papers, 241 rows (Dearden contributes 196)`

## `Verification results`

`Random 80-row sample (~15% of corpus) was checked against article text (combined article_text.txt + pdftotext -layout + pdftotext -raw). 78 / 80 verified (97.5%) by normalized-substring match. The 2 failures were paper 178 rows where my own paraphrased table-context preamble isn't a verbatim substring of the article (the underlying values were verified independently against the NXML).`

`Sanity checks across all 517 rows:`

- `0 out-of-range values (all within −273 to +600 °C).`
- `0 K→°C conversion errors.`
- `0 exact duplicates.`
- `0 rows missing DOI.`
- `2 rows where value_original doesn't appear in source_text — both are Dearden negative-MP cases (1-Butanal −96, Vinyl bromide −139.5) where pdftotext mangled the minus sign and the agent reconstructed it via -raw mode; values verified against literature.`

## `Methodological observations for skill design`

 1. `Pre-extracted plain text + NXML covers ~95% of cases. For PMC papers, neither PDF parsing nor OCR was needed. Tables in NXML preserve the cell structure cleanly.`

 2. `Inline-MP papers benefit enormously from a regex sweep + name- resolution step. The pattern <NAME>, <code> Yield = N%; mp = X–Y °Cwas nearly universal in synthesis papers. A two-stage extractor (regex for mp =, then walk back for <NAME>, <code>) handled 011 completely.`

 3. `Compound-code → IUPAC-name mapping is the most error-prone step. In paper 178, products 4a–4g have MPs in a table but no inline IUPAC name — the article just calls them "known compounds". Honest extraction leaves these as codes; an aggressive extractor would invent names. A skill should expose this trade-off and default to honesty.`

 4. `Open-bounded values (>250 °C, <-10 °C) require a policy. We skipped all open bounds. Counts: ~13 such skips across the corpus. These are real data points that QSAR users might still want — a skill could optionally surface them with an is_open_bound flag.`

 5. `PDF minus-sign rendering is unreliable. pdftotext -layout may render the minus glyph as ASCII "2" or a non-printable byte (\x02). pdftotext -raw (token-per-line) is more reliable for sign reconstruction. The Dearden run is the canonical example.`

 6. `Image-based table cells (paper 056 has 13 PNG molecule cells in its key BP table) defeat plain-text extractors. A skill that wants to handle these needs an OCR step or supplementary-data harvesting.`

 7. `Tg / Tc / decomposition / sublimation contamination: a strict "mp / bp only" extractor must distinguish thermal events. Paper 017 has Tg, Tm, Tc all in the same DSC table; paper 141 has "sublimes at 220 °C without melting"; paper 020 has many "(dec.)" qualifiers. The schema's measurement_type column was useful for the first two cases.`

 8. `"Compound 4a" or no compound name is common in tables. When the article uses only codes and points readers to supplementary or literature for full structures, the extractor must record codes and not fabricate names. ~20 rows in the corpus are coded-only.`

 9. `Range vs single value: the agreed midpoint-in-numeric + preserve- range-in-original schema captures everything. ~70% of synthesis-paper MPs are ranges, ~30% single values.`

10. `Modeling papers vary in extractability. Some (Mitchell, 058) keep per-compound data only in SI. Others (Dearden, Krossing) put it in main-text tables. The skill should peek at main-text tables before deciding "this is aggregate-only."`

## `Files`

- `/sessions/.../outputs/mp_bp_extracted.csv — final CSV (517 rows + header)`
- `/sessions/.../outputs/extraction_notes.md — this file`
- `/sessions/.../outputs/work/ — per-paper JSON intermediates, helper scripts, and per-paper notes from each subagent. Preserved for audit / debugging.`

<!-- forgemark-comments
- id: 1
  anchor_text: "\"mp 245 (dec)\""
  context_before: "ent_type ∈ {melt, decomp, melt_or_decomp, boil}. instrument ∈ {DSC, unk, …}. \"melt_or_decomp\" is for values reported as "
  context_after: " where both phenomena are implicated. \"boil\" is the natural extension for bp rows (no melt/decomp distinction applies th"
  author: Steven
  timestamp: "2026-05-10T23:40:49.141Z"
  resolved: false
  body: "When a paper reports mp # (dec), it means it decomposed and should be recorded as decomp."
-->

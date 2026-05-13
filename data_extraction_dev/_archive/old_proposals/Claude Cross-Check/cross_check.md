# Cross-check: Claude Test vs GPT Test

Two independent MP/BP extractions over the same 20-paper corpus.

## Top-line numbers

| | Claude | GPT |
|---|---:|---:|
| Total rows | 517 | 438 |
| Schema columns | 10 | 6 |
| Articles with rows | 16 / 20 | 17 / 20 |
| Distinct `property_type` values | 2 (`mp`, `bp`) | 13 (granular: `melting_point_SIRM`, `melting_point_subsequent_cycles_onset`, etc.) |

Row-level value matching (value-proximity, ≤1.5 °C tolerance, per article and
property kind):

| Status | Count |
|---|---:|
| Agreement (same compound, same value within 1.5 °C) | 313 |
| Claude only | 204 |
| GPT only | 125 |

**Where both extracted the same compound, agreement is essentially perfect:**
the mean absolute value difference across all 313 matched pairs is **0.00 °C**,
and every single matched pair has a value diff of 0. The two systems disagree
mostly on **scope** (what should be extracted) and on **coverage** (recall on
specific tables/sections), not on individual numbers.

The full comparison row-level dataset is in `comparison.csv` alongside this
file.

## Per-article counts

| Article | Claude | GPT | Δ |
|---|---:|---:|---:|
| 010 TRPA1 | 29 | 31 | −2 |
| 011 PDE4 pyridazinones | 55 | 55 | +0 |
| 013 6H-benzo[c]chromene | 34 | 34 | +0 |
| 017 ibuprofen amino-acid esters | 9 | 9 | +0 |
| 020 N-hydroxypiridinedione | 32 | 39 | −7 |
| 026 seco-acyclo-N-diazolyl-thione | 8 | 11 | −3 |
| 028 dispiro spirocyclics | 31 | 35 | −4 |
| 050 quinazoline-4-thiones | 18 | 19 | −1 |
| 056 AI BP prediction | 0 | 0 | 0 |
| 058 drug-like MP prediction | 0 | 0 | 0 |
| 064 COVID-API thermodynamics | **0** | **47** | **−47** |
| 138 triazole/tetrazole annellation | 27 | 27 | +0 |
| 141 Tyrian Purple | 4 | 3 | +1 |
| 157 dehydrocholic-acid clathrates | 8 | 8 | +0 |
| 164 microbiological problems | 11 | 10 | +1 |
| 178 Cu/Vit B3 MOF benzoxanthenones | 10 | 13 | −3 |
| 2008_Mitchell QSPR | 0 | 0 | 0 |
| **2009_Dearden QSPR** | **196** | **0** | **+196** |
| 2011_Krossing organic-salt MP | 40 | 92 | −52 |
| 2014_Schmittel thiadiazoloimidazoles | 5 | 5 | +0 |

Two papers drive almost the entire disagreement: **Dearden** (Claude
extracted 196 rows, GPT extracted 0) and **064 / Krossing** (GPT extracted
many predicted/literature-reference values that Claude excluded by scope).

## Disagreements by category

### Category 1 — Major recall failures (each system missed real data)

#### 1a. GPT missed all of Dearden Table 2 (196 rows)

Dearden 2003 (folder `2009_Dearden_…`) is a QSPR review whose Table 2 lists
**100 organic compounds with experimental bp and experimental mp values**,
used as the benchmark test set for six prediction programs. The "exp." columns
are real experimental data. Claude extracted 196 rows from this table (100
bp + 96 mp, with 4 mp shown as `NA`); GPT extracted 0.

GPT's extraction notes for Dearden read:
> "No compound-level BP records retained; tables summarize QSPR studies/classes and errors, not individual compound boiling points."

This is incorrect — Table 2 is per-compound experimental data with named
chemicals, not a summary table. **Claude is correct here.**

**Root cause**: GPT applied its "prediction/modeling paper → skip" rule too
broadly. Dearden is a review paper, but its Table 2 functions as a per-compound
data table. The skill needs a more nuanced rule: *some* tables in modeling
papers contain real experimental data.

Spot-check of Claude's Dearden values against external chemistry:
- Acetone bp 56.3 ✓ (lit. 56)
- Methanol mp −98.0 ✓ (lit. −97.6)
- 1,4-Dioxane bp 101.3 ✓ (lit. 101.1)

#### 1b. Claude missed at least 2 compounds in paper 020

In paper 020 (N-hydroxypiridinedione antiviral series), GPT found two
compounds with inline mp values that Claude missed:

- **Compound 5**, `2-((4-Hydroxybenzyl)oxy)isoindoline-1,3-dione`,
  mp 145–148 °C. Source: "White solid (225 mg, 30%), Rf = 0.28 (AcOEt),
  mp: 145–148 °C." Claude has no code-5 entry.
- **Compound 40**, `1,6-Dihydroxy-4-methyl-5-(1-((pent-4-yn-1-yloxy)
  imino)ethyl)pyridin-2(1H)-one`, mp 93–95 °C (dec.). Source: "Green solid
  (21.2 mg, 28%). Rf = 0.30 (1:1 AcOEt:MeOH), mp: 93–95 °C (dec.)".
  Claude has codes 33–39 and 41–50 for this series — but skipped 40.

Both compounds have clear, properly-formatted "compound (NN): mp X–Y °C"
entries in the article. **GPT is correct here.**

**Root cause**: My agent processed paper 020 by regex over `article_text.txt`
but the regex pattern that captured `mp: 93-95 °C (dec.)` evidently did not
trigger for those two specific entries. This is a recall bug in my agent's
pattern, not a scope decision.

### Category 2 — Scope-policy disagreements (both defensible)

#### 2a. Open-bounded values (>X, <X)

Roughly 15 rows across the corpus carry open-bounded mp/bp annotations like
`>250 °C`, `>300 °C`, `<−10 °C`. Claude **skipped** these per its agreed scope
policy ("midpoint isn't defined for open bounds; record nothing rather than a
misleading number"). GPT **included** them, putting the inequality string
directly into `temperature_c`.

Specific examples:
- Paper 020: compounds 54, 55, 58, 59, 60 with `>250 °C`
- Paper 028: 4 dispiro compounds (5c, 5d, 5g, 5h) with `>300 °C`
- Paper 026: Pb-thiadiazole complex (compound 10) with `>300 °C`
- Paper 164: TCMTB with `mp <−10 °C` and `bp >120 °C`

**Neither is wrong; the systems disagree on a sensible scope policy.** GPT's
approach surfaces more data but can't be used directly for numeric analysis;
Claude's approach is loss-of-information but cleanly numeric. The right
answer is probably to **keep both** and add a column flagging the value as
an open bound.

#### 2b. Predicted (calculated) values

The Krossing paper studies 520 organic salts and reports tables containing
both *measured* (`T_fus, exp`) and *calculated* (`T_fus, calc`) melting
points. GPT extracted both, labeling the calculated ones as
`melting_point_calculated`. Claude extracted **only the measured values** and
treated calculated values as out of scope ("not actually a melting point of
the compound — it's a model output").

GPT got 53 additional rows here, all with `property = melting_point_calculated`.

**Both are defensible.** A user who wants measured-only data agrees with
Claude; a user benchmarking prediction methods may want both. The right
answer is a typed schema where calculated values are tagged and easily
filtered.

#### 2c. Paper 064 (Nagar 2021)

Claude extracted 0 rows from paper 064 (judging it a prediction paper that
only cites literature for comparison). GPT extracted 47 rows from Table 5:
- 9 × `melting_point_SIRM` (model prediction A)
- 9 × `melting_point_STRM` (model prediction B)
- 9 × `melting_point_literature` (literature reference cited for comparison)
- 9 × `boiling_point_SIRM`
- 9 × `boiling_point_STRM`
- 2 × `melting_point` (free text mentions)

The 9 literature reference values are **real measured data** that the paper
prints (per-compound, from cited papers, in K). Claude's broad skip rule
threw these out along with the predictions. The SIRM/STRM rows are model
outputs — same status as the Krossing "calculated" rows above.

**GPT got more useful data here.** Claude over-skipped. The 9 literature
values for baricitinib, camostat, chloroquine, dexamethasone, favipiravir,
fingolimod, hydroxychloroquine, thalidomide, umifenovir should have been
extracted; they are per-compound experimental MPs cited explicitly.

### Category 3 — GPT duplicate rows

GPT's CSV has multiple rows for the same compound when the paper names that
compound in two different places (e.g., a table row AND an inline
characterization paragraph). This inflates GPT's row count without adding
new measurements.

Examples:
- **Paper 026**: compounds 4 and 6 appear **twice each**:
  - `5-methyl-1,3,4-oxadiazole-2(3H)-thione (4)` mp=68 (from inline)
  - `5-methyl-1,3,4-oxadiazole-2(3H)-thione (compound 4)` mp=68 (from Table 1)
  - Same for compound 6: 153 °C, two rows.
- **Paper 178**: compounds 4h, 4i, 4j appear twice each (inline IUPAC name +
  table row labeled `benzoxanthenone derivative 4h`).
- **Paper 010**: one compound appears twice with a typo'd name variant:
  - `(E)-N-(A-adamantan-1-yl)-3-(4-(pyridin-4-yl)phenyl)acrylamide` mp=227-229
  - `(E)-N-(Adamantan-1-yl)-3-(4-(pyridin-4-yl)phenyl)acrylamide` mp=227-229

Claude deduplicated these on output (the paper-026 acetohydrazide
double-entry is preserved on Claude's side because the paper itself reports
two methods producing the same compound at slightly different observed mps,
which IS legitimately two measurements).

**Claude is correct** to deduplicate when the value is identical; GPT's
extraction notes say it "de-duplicated records on article, compound name,
property, value, and DOI" but in practice the name variants escape that
dedupe key.

**Root cause**: GPT's dedup uses string-equality on `compound_name`. When the
inline section heading and the table cell give the same compound slightly
different name strings, the dedup misses them.

### Category 4 — Compound-name differences (detailed)

For the 313 matched (agreement) pairs where both systems found the same
compound with the same value, the names differ in characterizable ways:

| Naming-pair category | Count | % of matched |
|---|---:|---:|
| Identical names (case-insensitive) | 106 | 33.9 % |
| Code-format differences only (`(compound 4a)` vs `(4a)` vs `, 4a`) | 23 | 7.3 % |
| One name is a substring of the other (mostly GPT adds `[NN]` ref citations) | 60 | 19.2 % |
| Curly apostrophe / en-dash typography (`1,1′-` vs `1,1'-`) | 20 | 6.4 % |
| Paper 178 "(compound 4a)" vs "benzoxanthenone derivative 4a" | 7 | 2.2 % |
| Paper 050 X/R template format (identical between sides) | 18 | 5.7 % |
| Paper 020 compound 3 (Claude bare code vs GPT full IUPAC) | 1 | 0.3 % |
| Same prefix, different completion (mostly punctuation/spacing in deep IUPAC) | 13 | 4.2 % |
| Wrong-pair matching artifacts (value-collision in different compounds) | 76 | 24.3 % |

The 76 "wrong-pair" matches are an artifact of value-based pairing: when
two distinct compounds in the same paper happen to share a melting point
(common when compounds are in a homologous series), my greedy
value-matching algorithm paired them incorrectly. Looking at those rows
individually, both extractions have **correct names for the correct
compound** — they just got paired against each other in my comparison
matrix.

So among matched-and-genuinely-the-same-compound pairs, the real naming
differences cluster into a handful of style patterns plus the
already-flagged template/missing-name cases.

### Naming-style patterns

**1. Compound-code annotation style.** Claude appends `(compound 4a)` or
`(compound 2b)` to the IUPAC name. GPT uses the paper's exact format,
typically `(4a)` or `, 2b` — preserving how the source-paper section
heading formats the code. GPT's matches the paper more closely; Claude's
is more explicit. Both are unambiguous when parsed.

**2. Reference citations.** GPT preserves trailing reference citations in
the compound_name field: `(2E,4E)-N-Isobutyl-5-phenylpenta-2,4-dienamide
(11) [51]`. Claude strips them. The `[51]` is a citation, not part of
the compound name — **Claude is cleaner here** (60 rows affected; the
`[NN]` should live in a notes column, not in the name field).

**3. Typography of apostrophes and dashes.** Source PDFs and NXML often
use curly apostrophes (`′`) and en-dashes (`–`); plain-text extraction
converts these to straight ASCII in one direction or the other. Claude
tends to use `'` (straight); GPT preserves `′` (curly). 20 rows have
this difference. Neither is wrong; both refer to the same compound. A
production pipeline should pick a normalization (preferably preserve
the publisher's typography for fidelity, normalize to ASCII for
matching).

**4. Compound IDs from inline IUPAC vs from table.** When a paper has the
same compound both in a table (with a code only) and in an inline
characterization section (with full IUPAC name), GPT sometimes emits
two rows: one for the table appearance, one for the inline. Claude
deduplicates. See Category 3 ("GPT duplicate rows") above. The most
explicit example: paper 178 has `benzoxanthenone derivative 4h` (from
table) AND `4-(9,9-Dimethyl-11-oxo-…-yl)phenyl benzoate (4h)` (from
inline) as two separate rows in GPT's output.

**5. Paper-specific qualifier text.** Claude appends contextual
qualifiers like `(compound 3, Method 1)`, `(NMP, pure guest)`, `- in
1·DMSO clathrate B`. GPT keeps the name cleaner: `Acetohydrazide (3)`
or `N-methyl-2-pyrrolidinone` or `Dehydrocholic acid`. **GPT's
approach is cleaner**; this matches a recommendation in the earlier
verification pass to move provenance qualifiers to a separate column.
8 rows in paper 157 and 2 in paper 026.

**6. Paper 178 4b–4g — generic vs inferred-IUPAC.** Claude inferred
`12-phenyl-8,9,10,12-tetrahydrobenzo[a]xanthen-11-one` for 4a (because
the paper identifies the reactant) but used a "tetrahydrobenzo[a]xanthen-
11-one derivative" placeholder for 4b–4g. GPT used the generic form
`benzoxanthenone derivative 4X` for all of them, including 4a. Both
fail the stand-alone-interpretability test for 4b–4g; Claude's 4a is
the most useful entry. Neither names them properly because the paper
itself doesn't.

**7. Paper 020 compound 3 — code-only vs full IUPAC.** Claude recorded
just `compound 3` (the local-window extractor missed the IUPAC name
which is printed elsewhere in the article). GPT recorded the full
`2-((3-Methoxybenzyl)oxy)isoindoline-1,3-dione (3)` — verified against
the paper. **GPT is correct here.**

### A substantive chemistry name error (Claude side)

While investigating the naming differences, I discovered **one real
chemistry-level transcription error in the Claude CSV**:

**Paper 011, compound 5d.**
- Claude recorded: `4-[(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)-methyl]benzonitrile (compound 5d)` (mp 193–195 °C)
- The paper actually prints: `4-[(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)-methyl]benzoic Acid, 5d` (mp 193–195 °C)
- GPT correctly extracted: `4-[(5-Acetyl-2-ethyl-3-oxo-6-phenyl-2,3-dihydropyridazin-4-ylamino)-methyl]benzoic Acid, 5d`

The mp value is correct in both systems (193–195 °C); but Claude has the
wrong functional group on the terminal benzene ring. The chemistry is
substantively different: benzonitrile (`–C≡N`) versus benzoic acid
(`–COOH`).

**Root cause**: paper 011 was processed by me manually rather than by a
sub-agent. I built a Python dictionary mapping compound code → IUPAC
name by reading and transcribing each compound's name from the paper.
For compound 5d I mis-typed "benzonitrile" — almost certainly confusing
it with the adjacent benzonitrile-containing compounds 2f (mp 226–227)
and 2q (mp 204–205) in the same series. The `source_text` column for
the 5d row actually contains the *correct* paper text
(`...methyl]benzoic Acid, 5d Yield = 52%; mp = 193–195 °C`), but the
`compound_name` field has the wrong transcription. This is a
copy-from-source-to-name failure introduced by manual transcription
that an automated source-text-then-parse extractor would not have made.

**Why my earlier verification missed it**: my random 100-row sample
included 10 rows from paper 011, but compound 5d was not one of them.
Even if it had been, the verifier's job was to check that the recorded
value matches the paper, not that the recorded name's functional groups
match the source_text. The bug would have escaped a value-only audit.

**Verification scan over all Claude rows** (specifically checking for
substantive functional-group mismatches: nitrile ↔ acid, amide ↔ ester,
ester ↔ acid, sulfonate ↔ sulfide, etc.):
- Claude: 1 chemistry-name error (the 5d case)
- GPT: 0 chemistry-name errors

So GPT is more reliable on compound name transcription. Claude's
strength is verbatim source_text capture and per-row provenance, but
its single manual-transcription step in paper 011 introduced an error
that didn't get caught by the value-only verification pass.

### Adjudication on the naming front

| Naming style point | Claude | GPT |
|---|---|---|
| Verbatim-style preservation (typography) | weaker | stronger |
| Trailing `[NN]` reference cleanup | stronger | weaker |
| Stand-alone interpretability ("(X=Cl, R=...)" template) | tied (both fail) | tied (both fail) |
| Deduplication of inline+table appearances | stronger | weaker |
| Resolution of code-only references (paper 020 #3) | weaker | stronger |
| Avoidance of paper-jargon parentheticals | weaker | stronger |
| Inferred IUPAC where reactant is known (178 #4a) | stronger | weaker |
| Manual transcription accuracy (011 #5d) | weaker (1 error) | stronger (0 errors) |

The two systems have **complementary strengths**. GPT is more faithful
to printed names; Claude is cleaner on auxiliary metadata. Neither
solves the template-name problem in paper 050 (both leave `(X=Cl,
R=...)` unexpanded). **The single substantive chemistry-level naming
error in this study is on Claude's side**: paper 011 compound 5d's
functional group was mis-transcribed from `benzoic Acid` to
`benzonitrile`.

### Category 5 — Cosmetic / structural differences

- **Negative-MP sign reconstruction**: Both systems correctly extracted
  negative MPs where they appeared. Claude's Dearden run used `pdftotext
  -raw` to reconstruct minus signs from a `-layout` artifact (`2141.8` →
  `-141.8`); GPT used `pypdf` which handles the sign differently. Both
  produced the same numbers where they overlap (verified by chemistry
  spot-check of −94 °C for acetone, etc.).
- **Kelvin → °C conversion**: Both convert; both correct in the rows that
  overlap.
- **Unit columns**: Claude separates `value_celsius`, `value_original`,
  `unit_original`; GPT just stores `temperature_c`. Claude's schema
  preserves the K-vs-°C provenance; GPT's is simpler.
- **DOI for paper 157**: Both supplied a DOI. Claude used PMCID
  `PMC3716435` as a sentinel because the NXML had no DOI; GPT verified the
  actual DOI from the MDPI article page (`10.3390/i8070662`). **One point
  for GPT** on cleanliness here.

## Adjudication summary

| Disagreement | Magnitude | Adjudication |
|---|---:|---|
| Dearden Table 2 | 196 rows | Claude correct — GPT over-skipped |
| Paper 064 literature MPs | 9 of 47 rows | GPT correct — Claude over-skipped |
| Paper 064 model predictions (SIRM/STRM) | 38 of 47 | Scope question; both defensible |
| Krossing calculated MPs | 53 rows | Scope question; both defensible |
| Open-bound values (>X, <X) | ~15 rows | Scope question; GPT preserves more |
| GPT duplicates (026, 178, 010) | ~7 rows | Claude correct — dedup gap on GPT side |
| Paper 020 missed compounds (5, 40) | 2 rows | GPT correct — Claude recall gap |
| Paper 010 GPT extra (compound 18 dup) | 1 row | Claude correct — name-variant dup on GPT |
| Paper 020 compound 3 IUPAC name | 1 row | GPT correct — Claude missed the cross-reference |
| Paper 157 DOI | – | GPT correct (verified from publisher) |

Where one side is definitively right: **GPT has ~12 rows that Claude should
have had** (Dearden compounds GPT missed are not applicable here — those go
the other way; here I'm counting the cases where GPT got something
Claude didn't: paper 020 #5 & #40, paper 064 9 literature values, paper 020
compound-3 IUPAC name = 12), and **Claude has ~196 rows that GPT should
have had** (Dearden Table 2). The asymmetry is large because the Dearden
table is large.

## Where both systems agree on a flaw

Both extractions show the same systematic naming gap for paper 050: neither
expanded "X=Cl" into "6-chloro-…" even though the paper's prose explicitly
defines X at position 6. Both extractions left the names in a
template+substituent-code format that is not a chemical name.

Both extractions also struggle with paper 178 compounds 4b–4g: the paper
itself does not provide IUPAC names, only "known cpds reported in the
literature." Both systems handle this honestly (Claude calls them
`compound 4b (tetrahydrobenzo[a]xanthen-11-one derivative)`; GPT calls them
`benzoxanthenone derivative 4b`). Neither follows the literature
references to recover the full name.

## Root causes (consolidated)

1. **Scope policy mismatch**: open bounds, calculated values, and
   literature-cited values are handled by different rules in the two
   systems. The right answer is to extract *all* such values and tag them
   with a type column, so consumers can filter.

2. **Dedup uses string-equality on names**: GPT's dedup misses identical
   data points that have slightly different name strings. The right answer
   is to dedup on `(article, value, ±tolerance, normalized_name)`.

3. **Per-paper recall depends on regex flexibility**: my agents missed two
   compounds in paper 020 because the synthesis-paragraph regex didn't
   match the specific format used for those compounds. GPT missed all of
   Dearden because its "modeling paper" classifier ran too aggressively. A
   robust skill needs BOTH a permissive per-section regex AND a manual
   table audit per paper.

4. **Name-resolution is local-window-only**: both systems resolve compound
   names from a local context window around the mp value. When the IUPAC
   name appears in a different section (paper 020 compound 3 is named in
   one paragraph but its mp appears in another), local-window extraction
   fails. The fix is a two-pass approach: first locate every
   `<NAME>\s*\(\s*<code>\s*\)` mention to build a code→name dictionary;
   second resolve mp-line codes against that dictionary.

5. **Template-format compound names slip through**: paper 050's
   `(X=Cl, R=…)` rows survived both extractions. Neither system has a
   post-processing step that detects "this is not a chemical name" and
   either re-extracts with prose integration or marks the row.

6. **Table-image cells defeat both systems**: paper 056's Table 4
   contains compound structures only as PNG images. Both extracted 0 rows
   from that paper.

## Recommendations for a rigorously reliable skill

A production skill should layer these techniques. Sorted from highest to
lowest leverage:

1. **Explicit scope-type column in the schema**.
   Add a `value_kind` column: `experimental_measured` (this paper's own
   measurement) | `experimental_cited` (paper cites another paper's
   measurement) | `predicted_model_X` | `open_bound`. Then consumers can
   filter to what they need. This single change makes the 2c, 2b, 2a
   disagreements above moot.

2. **Two-pass name resolution**.
   Pass 1: scan the entire article for the pattern
   `<text>\s*\(\s*<code>\s*\)` (and `<code>:\s*<text>`, etc.) to build a
   dictionary `code → IUPAC name`. Pass 2: when extracting an mp from an
   `mp:\s*<value>` line whose surrounding ±300 chars contains only the
   code, look up the IUPAC name from the dictionary. This catches the
   paper 020 compound-3 case.

3. **Cross-reference table headers with prose**.
   When a table column header uses an abstract placeholder like "X" or
   "R", scan the paper text for definitions like "X = Cl at position 6"
   or "the 6-chloro derivatives (X = Cl)" and merge that into the
   compound naming. This catches the paper 050 systematic issue.

4. **Per-section regex catalog, not one global regex**.
   Synthesis sections, Experimental sections, characterization paragraphs,
   tables, and narrative discussions all have different MP/BP phrasings.
   A skill should run a *catalog* of patterns and union the results. My
   single-regex approach for paper 020 missed two compounds because their
   inline format was slightly different from the dominant pattern.

5. **Strong dedup key**.
   Dedup on `(article, normalized_name, property_kind, value_celsius
   ±0.5°C)`. Use a name-normalization that strips parenthetical codes,
   collapses whitespace, lowercases, and (optionally) maps known
   abbreviations. This catches the paper 026 / 178 / 010 GPT duplicate
   pattern.

6. **Open-bound preservation with explicit marker**.
   Don't skip `>X` or `<X`. Record `value_celsius=NULL`,
   `value_original=">X"`, `is_open_bound=true`. Lossless and filterable.

7. **Auto-verification pass before delivery — including a name-against-source check**.
   For each extracted row, programmatically verify:
   - `value_original` (or its midpoint) appears in `source_text`
   - **The chemistry-bearing tokens of `compound_name`** (specifically the
     functional-group suffix: `-nitrile`, `-acid`, `-amide`, `-ester`,
     `-amine`, `-thione`, etc.) appear in `source_text` or in the article
     near the value. **This single check would have caught Claude's 5d
     error.**
   - Source text is a verbatim substring of the article
   Any row that fails any of these checks should be flagged and either
   re-extracted or marked. My earlier value-only verification found 2
   rows failing the value test but missed the 5d functional-group
   transcription error entirely.

8. **Per-paper "yield curve" sanity check**.
   For papers in similar genres (synthesis, characterization), a normal
   article reports ~20–50 mp values. If your extractor returns 0 from a
   paper whose abstract says "we synthesized X derivatives", that's a red
   flag for a missed table or section. A skill should compare its row
   count to a per-paper "expected count" inferred from abstract keywords
   and warn on outliers. (This would have caught GPT's 0-row Dearden.)

9. **Schema-aware table parsing**.
   For NXML tables, parse cell coordinates and use header text to know
   which column is "exp.", which is "calc.", which is "Tm", which is
   "Tg". The Krossing and 064 cases need this to distinguish measured
   from predicted columns.

10. **Image-cell fallback (OCR or alt-text)**.
    For papers like 056 where structures are PNGs in table cells, fall
    back to OCR on the cell images or pull from the SMILES strings in
    supplementary CIF files. Without this, papers with image-based
    compound IDs are unrecoverable.

11. **Honest "not identifiable" sentinel**.
    When a paper truly does not name a compound (paper 178 4b–4g), emit
    `compound_name = not_identifiable_from_paper` and `paper_code = "4b"`
    in a separate column. Don't pad with "derivative".

## Concrete proposal: a 3-tier extraction pipeline

```
TIER 1 — Source ingest
  - PMC NXML preferred (structured tables, sections, DOI)
  - pdftotext -layout AND -raw (loose PDFs)
  - First-pass code→IUPAC dictionary built from <NAME> ( <code> ) pattern
    across the whole article.

TIER 2 — Pattern catalog
  For each known phrasing pattern (mp:, m.p., Mp, melting point, Tm, Tfus,
  bp, etc.), scan with a permissive regex, returning (value, raw text,
  position).
  For each NXML table, parse with column-header awareness; identify "exp.",
  "calc.", "literature" columns separately.

TIER 3 — Resolution + emit
  - For each candidate, resolve compound_name via the local context window
    (preferred) or the Tier-1 code dictionary (fallback) or the prose
    cross-reference for table substituents (paper 050 case).
  - Tag with value_kind (experimental_measured / cited / predicted / open_bound).
  - Tag with measurement_type (melt / decomp / boil / DSC-onset / etc.).
  - Verify source_text is a verbatim substring; if not, re-extract.
  - Dedup on normalized name + value within ±0.5 °C.
  - Emit row.

TIER 4 — Self-verification
  - Random-sample 15% of output, ask an independent agent to verify.
  - Sanity-check row counts per paper against an expected range from
    abstract keyword frequencies ("we synthesized N compounds").
```

This pipeline would have caught:
- GPT's Dearden miss (Tier-3 "literature column is experimental data")
- Claude's paper 020 misses (Tier-2 pattern catalog)
- Both systems' paper 050 X-position gap (Tier-3 prose cross-reference)
- GPT's paper 026 / 178 duplicates (Tier-3 dedup)
- Both systems' paper 020 compound-3 naming (Tier-1 code dictionary)

It would *not* have automatically resolved scope policy questions
(open bounds, predictions, literature references) — those would still
need a user-configurable rule, which is why the explicit `value_kind`
column is the highest-leverage recommendation.

## Files

- `comparison.csv` — row-level cross-match of the two CSVs, with status
  `agreement` / `claude_only` / `gpt_only`. 642 rows.
- `cross_check.md` — this file.
- `verification.md` — earlier verification of the Claude CSV (still
  valid; the value-correctness finding of 100/100 in the random sample
  is unchanged by this cross-check).

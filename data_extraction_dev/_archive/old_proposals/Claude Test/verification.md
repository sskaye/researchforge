# Independent Verification — Random 100-Row Audit

## Headline

- **Sample size**: 100 rows (≈19.3% of the 517-row CSV).
- **Sampling**: simple random sample with fixed seed `20260510`, then grouped
  by source paper for efficient verification. The seed is independent from
  the earlier 80-row spot-check (which used seed `2026`).
- **Value audit**: **100 / 100 correct (100.0%); 0 wrong (0.0%).**
- **Compound-name audit** (separate pass over the same 100 rows):
  **99 / 100 defensible (99.0%); 1 / 100 with an inferred attribute (1.0%).**

## Method

For each sampled row, an independent reviewer (a separate agent that was
NOT involved in the original extraction) was given:
- The recorded fields (compound_name, value_celsius, value_original,
  unit_original, property_type, measurement_type, instrument).
- The path to the source article (text, NXML, and/or PDF).

The reviewer was explicitly instructed NOT to rely on the `source_text`
snippet in the row. Instead, for each row, they:

1. Opened the source article fresh (article_text.txt for PMC papers;
   pdftotext output for loose PDFs).
2. Searched for the compound by IUPAC name AND/OR compound code,
   independently of the snippet stored in the row.
3. Located the printed mp/bp value in the surrounding text or table cell.
4. Compared what the paper actually prints to what is recorded, checking
   the value, the compound assignment, the property type (mp vs bp), the
   midpoint computation, the unit, and any (dec.) annotations.
5. For loose PDFs with sign-rendering issues (Dearden, Krossing), used
   `pdftotext -raw` mode to disambiguate minus signs that `-layout` mode
   renders as ASCII `2` or a non-printable byte.
6. Sanity-cross-checked plausibility against general chemistry knowledge
   (e.g., acetone mp ≈ −95 °C, water bp = 100 °C).

The verification was done in four batches by independent agents:

| Batch | Papers | Rows | Method |
|---|---|---|---|
| A | 011, 010, 050 | 25 | grep article_text.txt by compound code, parse NXML table |
| B | 020, 026, 028, 013, 138, 141, 157, 164, 178, 2014_Schmittel | 30 | grep article_text.txt and Schmittel pdftotext |
| C | 2009_Dearden | 36 | pdftotext both `-layout` and `-raw`; sign reconstruction confirmed against chemistry |
| D | 2011_Krossing | 9 | pdftotext both modes; sign-byte position re-verified |

## Sample distribution

| Article (truncated) | Rows in sample |
|---|---:|
| 010 TRPA1 | 6 |
| 011 PDE4 pyridazinones | 10 |
| 013 6H-benzo[c]chromene | 5 |
| 020 N-hydroxypiridinedione | 3 |
| 026 seco-acyclo-N-diazolyl-thione | 2 |
| 028 dispiro spirocyclics | 5 |
| 050 quinazoline-4-thiones | 9 |
| 138 triazole/tetrazole pyrrolopyrimidines | 9 |
| 141 Tyrian Purple | 2 |
| 157 dehydrocholic acid clathrates | 1 |
| 164 microbiological problems chapter | 1 |
| 178 Cu/Vit B3 MOF benzoxanthenones | 1 |
| 2009_Dearden QSPR review | 36 |
| 2011_Krossing organic-salt MPs | 9 |
| 2014_Schmittel thiadiazoloimidazoles | 1 |
| **Total** | **100** |

Papers with 0 extracted rows (058, 056, 064, 2008_Mitchell, plus paper 017
narrowly missed inclusion in the random sample) cannot contribute to the
audit but were already evidenced as 0-row extractions in the main notes.

## Result breakdown

| Verdict | Count | % of sample |
|---|---:|---:|
| `correct` | 100 | 100.0% |
| `wrong_value` | 0 | 0.0% |
| `wrong_compound` | 0 | 0.0% |
| `wrong_midpoint` | 0 | 0.0% |
| `wrong_property_type` | 0 | 0.0% |
| `wrong_unit` | 0 | 0.0% |
| `wrong_dec_annotation` | 0 | 0.0% |
| `wrong_sign` | 0 | 0.0% |
| `wrong_unit_conversion` | 0 | 0.0% |
| `other` | 0 | 0.0% |

## Analysis

Every value, compound assignment, property-type label, decomposition
annotation, midpoint computation, and minus-sign reconstruction in the
100-row sample matches what the underlying paper prints.

A 95% binomial confidence interval for the population accuracy, given 100/100
observed in the sample, is approximately **96.4 % – 100 %** (Clopper-Pearson).
With this audit alone we cannot rule out a few-percent error rate hidden in
the unseen 417 rows, but we have strong evidence that the rate is small.

There were no errors to analyze. Below are the only items worth recording —
each is a process / provenance observation, not a data error.

### Non-error observations

1. **Two rows in paper 011 (compounds 3a and 3g) carry a
   misaligned `source_text` snippet.** The snippet stored on these rows
   quotes the characterization paragraph of a neighbouring compound
   (compound 2l, which coincidentally has mp = 185–186 °C). Independent
   grep on `article_text.txt` for `"3a Yield"` and `"3g Yield"`
   confirmed that the paper's recorded values for 3a and 3g are also
   185–186 °C, so the *data* are correct. Cause: my own extraction
   script's 250-char back-context window straddled an adjacent
   compound block in the source text. **The data are right; the
   provenance trail for those two rows points at the wrong instance of
   the same value.** This is a precision-pipeline concern that should
   be fixed in any future skill: the back-window should snap to the
   nearest section/heading boundary rather than a hard char count.

2. **Dearden negative-MP values relied on `pdftotext -raw` sign
   reconstruction.** All 18 negative values in the batch-C sample were
   independently re-confirmed via the `-raw` mode (where the minus
   appears as a standalone `2` token before the magnitude). Where
   layout mode prints "2141.8" for compound `Methyl fluoride`, raw
   mode shows `-` `141.8` on consecutive lines, and the literature value
   for methyl fluoride is mp = −141.8 °C. All such reconstructions
   independently passed. The audit chain on these rows is one
   tool-mode-switch longer than for other rows but is sound.

3. **Krossing minus-byte position is in the right column.** In Krossing
   Tables 6/7, the `\x02` (non-printable minus) bytes appear in front
   of the `Diff. [%]` (deviation) column, not the `Exp. Tfus` column.
   The original extraction agent did not propagate that minus into the
   recorded melting point, which is correct. Two genuinely negative
   IL melting points elsewhere in the table do carry `\x02` immediately
   before the Tfus value, and those signs were correctly preserved
   (these specific rows happened not to be sampled in the audit, but
   the convention was independently verified).

4. **Some rows have paraphrased rather than verbatim `source_text`
   preambles.** Paper 178 rows (built from NXML cells) and paper 157
   rows (Table 3 with split headers) carry a synthesized "Table N:
   columns…" preamble around the actual cell value. The underlying
   cell values were re-verified directly against the NXML table and
   match. In any future skill design, the `source_text` field should
   be assembled as a contiguous substring of the article whenever
   possible, even when source data is tabular.

5. **One row (Dearden compound labeled "1-Hexane") preserves the paper's
   own labeling typo.** The mp value extracted (`-139.8 °C`) is the
   value that the paper prints next to the string "1-Hexane". The
   correct compound for that mp is almost certainly 1-hexene
   (1-hexane is not a real chemical species — n-hexane is just
   "hexane"). The extraction is faithful to the source. A skill could
   optionally flag values that conflict with the compound name's
   chemistry, but doing so would require chemistry-aware checks
   beyond pure text extraction.

## What would change the headline

For the headline to drop below 100%, one or more of the following would have
to be discovered in further auditing:

- A value mis-transcribed (e.g., 152 typed as 125) — none seen in 100.
- A range midpoint mis-computed (e.g., 154-156 → 154 instead of 155) — none seen.
- A compound mis-assigned (the value belongs to the previous/next compound) —
  none seen, though item (1) above is a related provenance bug.
- A property mis-labeled (BP recorded as MP or vice versa) — none seen.
- A sign error from PDF rendering — none seen, including 18 sign
  reconstructions verified against literature.
- A unit conversion error (K → °C) — none seen.

## Bottom line — values

**0 errors found in 100 rows.** The data are sound at the per-row level.
The two issues worth carrying into skill design are (a) the source-text
back-window can straddle compound boundaries, leaving correct values with
mislocated provenance snippets, and (b) tabular source_text would benefit
from contiguous-substring assembly rather than synthesized prose.

---

# Compound-name audit (second pass)

The first audit confirmed every MP/BP value is correct, but a value without
a correct compound identification is not useful. A second independent pass
was therefore run over the same 100 rows asking only one question: **does
the recorded `compound_name` correctly identify the chemical the value
belongs to?**

## Method

Each row's `compound_name` was scored against what the paper actually prints
for that compound. Independent agents (one per batch, separate from both
the original extractors and the value-audit reviewers) re-opened each
paper, found where the compound is named, and compared.

Verdict categories used:

| Verdict | Meaning |
|---|---|
| `match_exact` | recorded name matches the paper's printed name verbatim (modulo trivial whitespace/case/punctuation) |
| `match_faithful` | recorded name is a clear, accurate representation of what the paper prints (e.g., flattening italics/subscripts to ASCII; or a structured summary of a table row caption like "1d - 2,2-dimethyl-…-thiones (1) (X=H, R=4-CH3)") |
| `code_only_acceptable` | recorded name is just a code (e.g., "compound 4a") and the paper itself does not provide an IUPAC name nearby — code-only is the most honest representation |
| `code_only_unnecessary` | recorded name uses a code, but the paper does print a full name that should have been captured |
| `wrong_name` | the recorded name doesn't match the paper (wrong locants, wrong substituent, etc.) |
| `fabricated_attribute` | recorded name includes detail not stated in the paper (e.g., inferred IUPAC structure) |
| `paper_typo_preserved` | matches what the paper prints, but the paper itself has an error |

## Result

| Verdict | Count | % of sample |
|---|---:|---:|
| `match_exact` | 79 | 79.0% |
| `match_faithful` | 19 | 19.0% |
| `paper_typo_preserved` | 1 | 1.0% |
| `code_only_acceptable` | 0 | 0.0% |
| `code_only_unnecessary` | 0 | 0.0% |
| `wrong_name` | 0 | 0.0% |
| `fabricated_attribute` | 1 | 1.0% |
| `other` | 0 | 0.0% |

**Defensible names (exact + faithful + paper-typo-preserved): 99/100 (99.0%).**
**Inferred/fabricated names: 1/100 (1.0%).**

## The 1% issue — paper 178, compound 4a

The single flagged row is **row 8** in the CSV: paper 178 (Cu/Vit B3 MOF
benzoxanthenones), recorded compound_name:

> `12-phenyl-8,9,10,12-tetrahydrobenzo[a]xanthen-11-one (compound 4a, benzaldehyde-derived)`

**What the paper actually says about 4a**:
- Table 2 row 1 lists "4a" with reaction time and mp = 150–151 °C — no IUPAC name in the table.
- The Results section identifies the reactant: "the synthesis of 4a as a model example is a one-pot reaction of one mole of benzaldehyde, one mole of dimedone and one mole of β-naphthol."
- A footnote says "spectral data of known benzoxanthenones (4a–g) are reported in the literature." No IUPAC name is given for 4a in the paper itself.

The recorded full IUPAC name was inferred from the reactants (the canonical
chemistry of this benzoxanthenone synthesis). It is chemically correct and
any organic chemist reading the paper would identify 4a the same way, but
it is not strictly verbatim. The trailing "benzaldehyde-derived" qualifier
*is* directly grounded in the paper.

**Why this happened**: during the extraction of paper 178, I chose to
infer the IUPAC name for 4a because the paper *did* fully specify the
parent scaffold (in the abstract and in section headers for 4h/4i/4j) and
the reactant for 4a (benzaldehyde). The product identity follows
unambiguously. For compounds 4b–4g I did not make the same inference
(those rows are recorded as `compound 4b (tetrahydrobenzo[a]xanthen-11-one
derivative)` etc.), because the aldehyde reactants for 4b–4g are not
explicitly named in the visible text.

**The fix**: for strict-precision applications, the row could be rewritten
to `compound 4a (tetrahydrobenzo[a]xanthen-11-one derivative, benzaldehyde-
derived)` — same level of identification as 4b–4g, no inferred substituent.
Decision left to the user; the value is unchanged either way.

## The 1% paper-typo case — Dearden "1-Hexane"

The Dearden paper's Table 2 literally prints `1-Hexane` (with locant `1-`)
for the entry whose experimental BP = 63.5 °C and MP = −139.8 °C. These
values are the canonical values for **n-hexane**, and the locant `1-` makes
no chemical sense for a saturated straight-chain alkane — almost certainly
a typo in the source. The extractor faithfully preserved the paper's text
rather than silently "correcting" the name. This was scored
`paper_typo_preserved`, not an extraction error.

## Other observations from the name audit

- **138 (annellation paper) preserves typos verbatim** in two rows: one
  uses the paper's spelling `Chorophenyl` (likely meant `Chlorophenyl`),
  and another has a substituent description that elemental analysis
  suggests should be `4-methoxyphenyl` rather than what the paper prints.
  These were classified `match_exact` because the recorded name matches
  what the paper prints — but the underlying paper has issues. Surfacing
  these as flags in a future skill would be valuable.
- **Krossing batch** (9 ionic-liquid shorthand names) was clean except
  for one row (`[N1,1,1,1][HT]`) where the paper prints `["HT"]` with
  typographic quote marks and the extractor dropped the quotes. Anion
  identity is unambiguous; classified `match_faithful`.
- **Dearden batch** (36 organic compounds) was 35 `match_exact` + 1 paper
  typo. Halocarbons, locants, hyphenation, and "n-" prefixes all
  transcribed correctly.

## Bottom line — names (with the lenient "matches what the paper prints" criterion)

**99 / 100 defensible (99.0%); 1 / 100 with an inferred IUPAC attribute (1.0%).**

Zero outright wrong names, zero mis-assignments, zero transcription errors
in the audited sample under this criterion.

## Files (compound-name audit)

- `/sessions/.../outputs/work/verify_names_batch_{A,B,C,D}_results.json`
  — per-batch name-verdict objects from each independent agent
- `/sessions/.../outputs/work/verify_names_all_results.json` —
  consolidated name verdicts across all 100 rows

---

# Compound-name audit — corrected pass (strict "stand-alone interpretability" criterion)

The lenient audit above asked only "does the recorded name match what the
paper prints?" That's the wrong question. A CSV consumer will read the
row without the paper in front of them, so the right question is:

> **Can a chemist identify a unique molecular structure from the
> `compound_name` field alone, without reading the paper?**

Under this stricter standard, several rows fail. The user's spot-check
flagged five representative problems, all of which I confirmed and
generalized.

## Failure modes found

### A. "Derivative" with no specific substituent — 6 rows

Examples (paper 178, products 4b through 4g):
- `compound 4b (tetrahydrobenzo[a]xanthen-11-one derivative)`
- `compound 4c (tetrahydrobenzo[a]xanthen-11-one derivative)`
- … through `4g`

The paper says only "spectral data of known benzoxanthenones (4a-g) are
reported in the literature" and does not name the aldehyde reactant for
each. The product structures are recoverable only by following the
literature references the paper cites — not from this paper's text alone.
The compound_name as recorded cannot identify the specific compound.

**Why this happened**: the paper lists products 4a–4j with mp values in
Table 2 but only explicitly names the new compounds 4h, 4i, 4j (and
identifies 4a's reactant as benzaldehyde). For 4b–4g the paper provides
neither the IUPAC name nor an unambiguous reactant identification. The
extractor recorded a generic "derivative" placeholder rather than
fabricating, which is honest but unusable.

**Fix**: requires reading the literature references cited by the paper,
or extracting structures from the figures/scheme images (which the
plain-text pipeline doesn't see). Without that, these rows should
either be dropped, or marked with an explicit "compound not identifiable
from this paper" flag.

### B. Template + substituent codes is not a chemical name — 18 rows

Examples (paper 050, the entire 18-compound series):
- `1a - 2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thiones (1) (X=H, R=H)`
- `1g - 2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thiones (1) (X=Cl, R=H)`
- `2e - 2-methyl-3-phenylquinazoline-4(3H)-thiones (2) (X=Cl, R=4-CH3)`
- … etc.

Two issues:
1. The format is a template + substituent codes (X=…, R=…) — not a real
   chemical name. A reader has to *do work* to derive the actual molecule.
2. The position of X on the backbone is not stated in the field.

**Cross-referencing the paper shows X is the 6-position.** Buried in the
paper text:

> "6-Chloro-2,2-dimethyl-3-phenyl-1,2-dihydro-quinazoline-4(3H)-thione and its 3´-chloro- and 3´,4´-dichloro analogs"
> "6-chloro derivatives (X = Cl)"

So the paper *does* give enough information to assign all 18 compounds
proper IUPAC names — but only by combining the Table 1 caption,
substituent columns, and the prose synthesis section. The extractor
relied on the table caption alone and produced template-format names.

**What the proper names should be**:
- 1a → 2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione
- 1g → 6-chloro-2,2-dimethyl-3-phenyl-1,2-dihydroquinazoline-4(3H)-thione
- 2e → 6-chloro-3-(4-methylphenyl)-2-methylquinazoline-4(3H)-thione
- … etc.

**Fix**: re-process paper 050 by reading prose alongside tables, parsing
the X/R columns into substituent positions, and emitting full IUPAC names.

### C. Bare code with no name elsewhere captured — 1 row

Example (paper 020, compound 3):
- `compound 3` (with mp 144–146 °C)

The paper *does* name compound 3 elsewhere:

> "The compound 2-(3-Methoxybenzyloxy)isoindolin-1,3-dione ( 3 ) was synthesized as follows: …"

But the extracting agent's "search 300 chars before the mp" window didn't
reach the section header where the IUPAC name appears, so it fell back
to `compound 3`. The paper has the data; the extraction missed it.

**Fix**: when a row gets only a code, the extractor should search the
paper globally for "<NAME> ( <code> )" patterns to recover the IUPAC
name from a different location in the text.

### D. Paper-specific parenthetical jargon — 8 rows (paper 157), 2 rows (paper 026)

Examples:
- `acetone (pure guest AC)` — "pure guest AC" is meaningless outside the paper
- `N-methyl-2-pyrrolidinone (NMP, pure guest)`
- `dimethyl sulfoxide (DMSO, pure guest)`
- `dimethylformamide (DMF, pure guest)`
- `Dehydrocholic acid (compound 1, host) - in 1·DMSO clathrate B` (×4 — one per clathrate)
- `Acetohydrazide (compound 3, Method 1)`
- `Acetohydrazide (compound 3, Method 2)`

The chemical name component is correct and unambiguous in all of these,
but the trailing parenthetical is paper-specific context that should not
be in the `compound_name` field. A consumer reading "acetone (pure
guest AC)" out of context will be confused.

**Fix**: strip the parenthetical context to a separate "notes" column,
keeping `compound_name` to the chemical identity only. For the
dehydrocholic-acid rows the four entries arguably should be a single
entry with the four measurements averaged or recorded separately; the
clathrate-environment qualifier is not part of the compound name.

For paper 026 acetohydrazide, the two rows record the *same compound*
prepared by two different routes. The `compound_name` should be just
"Acetohydrazide" and the route should live elsewhere (e.g., a notes or
preparation column). Both rows are otherwise fine.

## Updated counts (full 517-row CSV)

I ran a systematic regex sweep over all 517 rows to count each failure
mode:

| Verdict | Count | % of CSV |
|---|---:|---:|
| **PASS** (full chemical name; identifiable on its own) | 482 | 93.2 % |
| `FAIL_derivative` (paper 178, 4b–4g) | 6 | 1.2 % |
| `FAIL_X_position_unspecified` (paper 050, X=Cl rows) | 12 | 2.3 % |
| `FAIL_template_format` (paper 050, X=H rows — format issue even though X=H is degenerate) | 6 | 1.2 % |
| `FAIL_code_only` (paper 020 compound 3) | 1 | 0.2 % |
| `FLAG_paper_jargon` (paper 157 jargon parentheticals) | 8 | 1.5 % |
| `FLAG_method_qualifier` (paper 026 "Method 1/2") | 2 | 0.4 % |

**Strict failures: 25 / 517 = 4.8 %.**
**Failures + flags (anything needing cleanup): 35 / 517 = 6.8 %.**

The earlier "99 / 100 defensible" headline only measured *fidelity to
what the paper prints*. It missed the larger problem that some papers
print their compounds in template form, not as full IUPAC names, and a
faithful extraction of those templates is not a useful CSV row.

## Re-scoring the random 100-row sample (strict criterion)

The 100-row sample contains:
- **9 paper 050 rows** — all 9 are FAIL under the strict criterion
  (whether X=H or X=Cl, the template format isn't a chemical name)
- **1 paper 157 row** (`N-methyl-2-pyrrolidinone (NMP, pure guest)`) — FLAG
- **1 paper 178 row** (4a) — PASS, with the previous-pass caveat that
  the IUPAC name was inferred from the reactant rather than printed
- **89 other rows** — all PASS

| Verdict | Count | % of sample |
|---|---:|---:|
| PASS | 90 | 90.0 % |
| FAIL (strict) | 9 | 9.0 % |
| FLAG | 1 | 1.0 % |

**Strict error rate: 9 / 100 = 9.0 %.**

This is a meaningful correction to the earlier headline. The values are
still all correct, but the compound names for 9 % of the audited rows
fail the stand-alone test.

## What would be needed to fix this

Five complementary techniques, applied during extraction:

1. **Read prose alongside tables.** Paper 050's X position (6-Cl) is
   stated in the synthesis section, not in the table. A skill that
   extracts from tables should also scan the surrounding prose for
   substituent-position definitions and merge them in.

2. **Resolve compound codes globally.** When a row's surrounding
   ~300-char window only yields a code (e.g., "compound 3"), search the
   entire article for `<NAME>\s*\(\s*<code>\s*\)` patterns. Paper 020
   names compound 3 cleanly elsewhere in the text; the local window
   just missed it.

3. **Detect template-format names.** Patterns like "(X=…, R=…)" and the
   word "derivative" are signals that the field is not a final chemical
   name. A post-processing step should flag these for re-extraction or
   for downgrading to "compound not identifiable from paper" status.

4. **Separate provenance from identity.** Trailing parentheticals like
   "(pure guest AC)", "(compound 1, host) - in 1·DMSO clathrate B",
   "(compound 3, Method 1)" belong in a *notes / preparation* column,
   not in `compound_name`. The schema would benefit from an explicit
   `compound_context` column.

5. **Honest "not identifiable" labels.** When a paper truly does not
   identify a compound (paper 178's 4b–4g send the reader to the
   literature), the extractor should emit a clear sentinel like
   `not_identifiable_from_this_paper` rather than a vague
   "derivative" string. Consumers can then filter these out.

## What I'm leaving as-is in this CSV (and why)

I am *not* re-extracting and overwriting the CSV in this pass — the
user asked for an updated audit and remediation thoughts, not a
re-extraction. Concretely:

- The 25 strict-failure rows and the 10 flag rows are left as-is. The
  values they carry are correct. The compound identification is the
  problem.
- A future skill should apply the five fixes above to bring this from
  4.8 % strict failure rate to (hopefully) under 1 %.
- The "compound 3" → "2-(3-Methoxybenzyloxy)isoindolin-1,3-dione" row
  and the paper 050 series are the easiest wins because the paper has
  the data; just the local-window extraction missed it.
- The paper 178 4b–4g rows are genuinely hard — the paper itself does
  not provide enough information.

## Final corrected headline

- **Values: 100 / 100 correct (100 %).**
- **Compound names (strict stand-alone interpretability):
  91 / 100 acceptable; 9 / 100 fail** (under the random-sample audit).
- **Across the full 517-row CSV: 25 strict failures (4.8 %), 10 flags
  (1.9 %), 482 clear pass (93.2 %).**

The data values are sound. The compound-name extraction pipeline has
systematic gaps for three specific patterns — table templates with
unspecified positions, papers that name compounds far from where the
mp appears, and papers that don't fully name their compounds at all.
All three are fixable with cross-referencing strategies that this
extraction did not implement.

## Files

- `/sessions/.../outputs/work/verify_sample.json` — the 100-row sample
  (random seed 20260510)
- `/sessions/.../outputs/work/verify_batch_{A,B,C,D}.json` — per-batch
  sample input given to each agent
- `/sessions/.../outputs/work/verify_batch_{A,B,C,D}_results.json` —
  per-batch verdicts written by each independent agent
- `/sessions/.../outputs/work/verify_all_results.json` — consolidated
  verdict objects across all 100 rows

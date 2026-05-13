# Trial-2 comparison report — three agent models on the same skill

**Date:** 2026-05-13
**Skill version:** mp-bp-extraction v1.4 (installed via the packaged `.skill` file)
**Corpus:** `mp_bp_full_set` — 168 paper subdirectories
**Audit method:** Same as Trial-1 — uniform random 100-row sample per trial (seed 20260512), 4 fresh independent Claude verifier agents in parallel, each handling 25 rows, applying v1.4 verification protocol.

## Headline

| Run | Agent model | Rows emitted | Random-100 audit pass | 95 % Wilson CI |
|---|---|---:|---:|---:|
| Trial-1-full (reference) | (this skill's agent, Sonnet via our harness) | 1,338 | **93 %** | 86–97 % |
| Trial-2 gpt55_high | GPT-5.5 (high) | 907 | **86 %** | 78–91 % |
| Trial-2 opus47 | Claude Opus 4.7 | 1,864 | **98 %** | 93–99 % |
| Trial-2 sonnet46 | Claude Sonnet 4.6 | 2,567 | **55 %** | 45–64 % |

Three sharply different results from the same skill on the same corpus. The skill works extremely well with Opus 4.7, well with GPT-5.5 high, and poorly with Sonnet 4.6.

**Compared to Trial-1:**
- **gpt55_high improved dramatically**, from 56 % → 86 %. The v1.4 mandate ("read each paper directly, do NOT write a regex extractor") landed. The model did not write a Python regex extractor this time — failures shifted from "wrong-row binding / sentence-fragment names" (Trial-1 regex failures) to surface defects (truncation residue, fabricated quotes on a few rows). Net 30 pp improvement.
- **opus47 is the best run we've ever measured.** 98/100 with CI 93–99 %. Cleaner than Trial-1's 93 %.
- **sonnet46 underperformed** badly despite extracting more rows than any other run. 55 % audit pass.

## What changed in the skill between Trial 1 and Trial 2

Trial 1 (the full-corpus reference run and the parallel gpt55_high run) was conducted on a skill state between v1.2 and v1.3. Trial 2 was conducted on v1.4, the version packaged as the installable `.skill` file. The substantive changes between those two states fall in two groups: v1.3 (motivated by Trial-1-full audit findings) and v1.4 (motivated by the cross-harness validation against GPT-5.5's regex-extractor implementation).

### v1.3 — compound-name truncation and CSV quoting

Motivated by Trial-1-full's audit: 5 of 7 audit failures were compound-name truncation of the `H-Indeno…` indicated-hydrogen-locant form, and 44 rows across 3 of 14 batches had CSV-quoting bugs that required programmatic post-hoc repair.

| Change | Where |
|---|---|
| Multi-line compound-name reassembly step | `EXTRACTION_PROMPT_TEMPLATES.md` Template 1 — read the line above section headers; reject `H-Indeno...` truncations; resolve `pdftotext` doubled-token artifacts |
| Mandated RFC-4180 CSV quoting | Extraction prompt — use `csv.QUOTE_ALL` or wrap fields containing comma/quote/newline in double quotes |
| New `scripts/csv_quote_lint.py` | Catches unquoted-comma column shifts at sanity-check time; wired into `run_all_checks.py` |
| New `_TRUNCATED_LOCANT_PREFIX` pattern | `validate_compound_name.py` — detects names starting with `[A-Z]H-[A-Z]` or `H-Pyrrolo/Indeno/Pyrazolo/...` |
| New `COMMON_ERRORS.md` entries I and J | I: adjacent-measurement quote; J: doubled-token PDF artifact (from Trial-1-val rows 147 and 296) |
| New seeded-error rows + `evals/files/malformed_csv_quoting.csv` | Two new evals in `evals/evals.json` for regression coverage |

### v1.4 — mandatory direct-read and anti-regex-extractor mandate

Motivated by a parallel cross-harness validation in which GPT-5.5 absorbed the schema and deterministic checks but missed the methodology — wrote `extract_mp_bp.py`, a regex extractor over `pdftotext` output, and reached 56% audit pass vs. 93% for the protocol-intended approach.

| Change | Where |
|---|---|
| MANDATORY-READING block at top of `SKILL.md` | States explicitly: the agent reads each paper directly and does NOT write a Python regex extractor |
| New anti-pattern (first entry in the anti-patterns list) | Forbids regex-based bulk extractors |
| Phase 4 labeled MANDATORY | Explicit phrasing: independent verification is required before declaring success |
| `run_all_checks.py` warning | Prints a warning when >90% of rows are still `pending_verification` — catches agents who skip Phase 4 |
| Strengthened front-matter `description:` | Leads with "LLM-driven" extraction; explicitly forbids the regex approach (this is the text used for skill auto-selection) |
| New `COMMON_ERRORS.md` entry K | Documents the regex-extractor misapplication observed in cross-harness validation (56% vs. 93% audit pass) |

### Packaging changes

- The skill was packaged as a single `.skill` zip (`mp-bp-extraction/dist/mp-bp-extraction.skill`) and installed via that artifact on each of the three Trial-2 agents.
- `CHANGELOG.md` was moved **outside** the skill directory (to the repo root) so that the installed skill doesn't ship historical version notes to the invoking agent.
- The `description:` field was trimmed from 1,250 to 780 chars to satisfy the 1024-char install constraint while preserving the key claims (LLM-driven; scripts are post-extraction; regex drops 93→56%; Phase 4 mandatory; do not fetch from the web).

### What did NOT change

- The schema (id, verification_status, compound_name, compound_smiles, property, value_celsius, value_celsius_min/max, value_raw, relation, data_type, source, source_url, evidence_location, evidence_quote, conversion_arithmetic, notes) is identical between Trial 1 and Trial 2.
- The six phases of the protocol are identical.
- The deterministic-check scripts (other than the new `csv_quote_lint.py` and the `run_all_checks.py` Phase-4 warning) are identical.
- The verification prompt and the audit method (uniform random 100-row sample, 4 parallel fresh verifier agents, 25 rows each) are identical, so Trial 1 and Trial 2 pass rates are directly comparable.

## Trial-2 gpt55_high — 86 %

| Failure mode | Count |
|---|---:|
| flagged_compound_name_truncated | 7 |
| flagged_evidence_quote_not_found | 4 |
| flagged_compound_mismatch | 2 |
| flagged_value_mismatch | 1 |

### What this run did well

- **No regex extractor.** Per the run's README and manifest, this was per-paper LLM extraction. The v1.4 anti-pattern landed.
- Same schema, properly quoted CSV (no comma-split column shifts).
- Phase 4 was actually run (this trial dir has `phase4_audit_summary.json`, `phase4_verdicts_*.json`) — the only Trial-2 run that did its own internal Phase 4.

### Remaining defects

The 14 failures fall into three clusters:

1. **Truncation residue (7 rows)** — compound names cut mid-word. Examples: `...Carboxamid` missing the trailing `e`; `8-(1-(3-(5'-` cut after 13 chars; `Phenyl(6′-` cut after 10 chars. These look like CSV field-length artifacts more than reading errors — the name was correctly identified but truncated when written.
2. **Masthead-as-quote (4 rows)** — `evidence_quote` contains the paper's journal-masthead text ("Molecules Molecules molecules…") rather than the mp-bearing sentence. The mp value is right but the quote points at the article's title block. Likely the extractor used the first regex hit for the value without checking that the quote span contained both compound and value.
3. **Compound mismatch (2 rows) and one isomer error.** 4i vs 4f label swap when both compounds have the same mp; an isomer position-swap.

The v1.4 quote re-confirmation step should have caught categories 1 and 2, but didn't for these rows. Worth checking whether the gpt55_high agent invokes that re-check or skips it.

## Trial-2 opus47 — 98 %

| Failure mode | Count |
|---|---:|
| flagged_evidence_quote_not_found | 2 |

### What this run did well

Almost everything. 25/25 on batches 2 and 3; 24/25 on batches 1 and 4. The compound names are correct, the values are correct, the data_type is correct, the identifiers (DOI / PMC / legacy) match.

### Remaining defects

Two evidence-quote issues:

1. **Row 80** — recorded quote was `"Dark red solid;"` (verbatim in paper, but doesn't include the mp 168-170 °C — it's the leading clause before the mp). The mp value itself is correct.
2. **Row 1608** — `evidence_quote` is a paraphrase joining two non-adjacent table cells with `...` instead of a verbatim span. Value is correct.

Both are quote-completeness issues, not extraction errors. Of the 168 papers and 1,864 rows, the only audit-detectable problems were two non-verbatim quotes. The compound + value + DOI columns of these two rows are still correct.

This is the cleanest extraction run we have on record across the whole project. Suggests Opus 4.7 reads the v1.4 skill very literally — does the per-paper read, applies the quote re-confirmation, runs Phase 4 verification.

## Trial-2 sonnet46 — 55 %

| Failure mode | Count |
|---|---:|
| flagged_evidence_quote_not_found | 22 |
| flagged_compound_mismatch | 8 |
| flagged_compound_name_truncated | 8 |
| flagged_doi_unrelated_paper | 4 |
| flagged_paper_unreadable | 2 |
| flagged_missing_value_celsius | 1 |

### What this run did

Sonnet46 emitted 2,567 rows — nearly double Trial-1's 1,338 and 38 % more than Opus 4.7. Looking at the trial dir contents (multiple `batch_aa.csv` through `batch_aj.csv`, `extracted_all_fixed.csv`, `fix_csv.py`, `flags_final.csv`), the run did substantial recall work and ran its own CSV cleanup.

But 45 % of audited rows fail verification. Failures cluster around four behaviors that diverge from the protocol:

1. **Constructed / paraphrased quotes (22 rows).** The extractor built `evidence_quote` strings as "Table N: compound MP X" templates rather than copying a verbatim span. The values + compounds are mostly correct, but the quotes are reformulations, not literal text. Verifier rejects per Phase 2 step 6 / Phase 4 step 4 verbatim requirement. Note that for many of these rows, the underlying data is correct — only the quote-fidelity is wrong.

2. **Compound mismatch within sequential blocks (8 rows).** When a paper has compounds 3a, 3b, 3c, 3d, ... each with its own mp, the extractor lined up the wrong compound's value: row labeled 2s carries 2e's mp; row labeled 2e carries 2g's mp; etc. Likely an off-by-one in the per-paper iteration.

3. **Compound-name truncation under PDF wrap (8 rows).** Same failure mode as gpt55_high's category 1 but more frequent. Examples: "Hydroxyphenyl)-N-phenylpiperazine-1-carbothioamide" (missing leading "4-(4-"); "(4-nitrophenyl)ethan-1-ol" (missing scaffold prefix); "Cyanomethyl)-1-methyl-1H-pyrrolo..." with contamination from the following paragraph. The v1.3 truncated-locant-prefix check catches `H-Indeno...` patterns but not these substituent-prefix-only truncations.

4. **Wrong-paper DOIs (4 rows).** Two rows cite `10.1002/cbdv.202500394` for compounds that are actually in `10.1002/ardp.70227` (PMC13006720); two rows cite `10.1002/chem.202500386` for content from `10.1002/cmdc.202500751`. DOIs from one paper got attached to extractions from a different paper. This is a serious bookkeeping bug.

5. **Paper-unreadable cases (2 rows).** Yalkowsky 1990 (scanned image PDF, requires OCR) and a Tetko 2009 reference that isn't in the corpus. Sonnet46 emitted rows for both rather than skipping per "drop rather than fabricate."

### How the sonnet46 run differed (confirmed via the agent's own self-analysis)

The agent's self-analysis (`trial2_analysis_sonnet46.md`) confirms a bimodal execution that the audit pattern alone couldn't fully diagnose:

- **Path A — PMC + subdirectory batches (~164 papers, ~1,800 rows).** Parallel LLM extraction agents per batch. Each agent opened the NXML / article_text.txt directly, read each paper, and wrote rows with verbatim `evidence_quote` substrings. Protocol-compliant.
- **Path B — 20 standalone-PDF reference-table papers (770 rows).** `build_batch_pdfs.py` — a Python data-entry script that hardcoded compound names and values the agent had read manually, then constructed `evidence_quote` strings programmatically via f-string templates. Example: `add(nm, ..., f"Table III: {nm} BP {bp_k} MP {mp_k}", ...)`. None of those template strings appear verbatim in the source files.

Path B is the entire explanation for the 22 "constructed quote" failures. Of the 770 Path-B rows, the script accounts for almost all of the audit's quote-only failures. The agent's stated rationale: writing a data-entry script "felt like a reasonable way to handle high-volume tabular data efficiently" for papers like Yalkowsky 1990 (85+ compounds × multiple columns) and Mitchell 2008 SI (~100 rows).

Importantly, **this is not a regex-extractor failure** in the Trial-1 sense. Sonnet 4.6 read the source tables manually — the underlying compound and value data are mostly correct. The agent then laundered those reads through a Python script that templated the quotes. The v1.4 anti-pattern names `re.findall` + `pdftotext` specifically, and Sonnet 4.6 read that literally: a hardcoded data-entry script with no regex over paper text felt outside the prohibition. The agent's counterfactual estimate: if those 770 rows had come from direct reads, the audit pass rate would have been ~78–82 % instead of 55 %.

## Failures categorized by which field is wrong

The Phase-4 verifier flags map cleanly to which schema field carries the error. Categorizing each failure tells us whether the model is mis-extracting *data* (compound, value, source) or mis-recording *evidence* (the quote). A "quote-only" failure means the verifier confirmed the underlying compound + value + source are correct but the recorded `evidence_quote` doesn't match the paper.

### GPT-5.5 (gpt55_high) — 14 failures

| Affected field | Count |
|---|---:|
| Compound name | 9 |
| Value | 1 |
| Source / DOI | 0 |
| Quote only | 4 |

Of the 4 quote-only failures, **0** had verifier-confirmed correct underlying data. In every case the quote was the journal masthead and there was no actual mp/bp measurement in the paper to support the row. So GPT-5.5's residual error mode is **"extracting things that aren't actually mp/bp data"** — not "extracted the right thing and mis-quoted it." Strengthening upstream "is this even a measurement?" filtering would address most of the remaining defects.

### Sonnet 4.6 (sonnet46) — 45 failures

| Affected field | Count |
|---|---:|
| Compound name | 16 |
| Value | 1 |
| Source / DOI | 6 |
| Quote only | 22 |

Of the 22 quote-only failures, **13** had verifier-confirmed correct underlying data — the compound, value, and DOI were all right, only the quote was wrong. The pattern across these 13 rows is consistent: the quote is a constructed string of the form `"Table N: <compound> MP <value>°C"`, paraphrasing the paper's content rather than copying a contiguous substring. The remaining 9 quote-only failures involve quotes that don't match the paper at all.

The two models are failing for opposite reasons. GPT-5.5 makes occasional mistakes about *what to extract*; Sonnet 4.6 frequently makes correct identifications but synthesizes the evidence text instead of transcribing it. A structural guardrail against templated quotes (a `quote_template_lint.py` matching `^(Table|Compound)\s+\d+:` and similar patterns, plus a sharper anti-pattern entry in `SKILL.md`) would catch the bulk of Sonnet's residual errors deterministically before Phase 4 ever runs. The same script would not catch GPT-5.5's failures, which need upstream rather than downstream guardrails.

## Independent agent self-analyses

After the audit, each of the three Trial-2 agents was given the comparison report plus a short prompt asking it to diagnose its own root causes and propose skill changes. The three responses (`trial2_analysis_opus47.md`, `trial2_analysis_GPT55_high.md`, `trial2_analysis_sonnet46.md`) materially revised the prior root-cause read in three ways.

### Opus 4.7 — what it confirmed

Opus 4.7 used 13 parallel general-purpose subagents to read papers directly (Read tool on NXML / `pdftotext -layout` on PDFs); helper scripts only enumerated the corpus, normalized enum values (`experimental`/`literature_cited` → `measured`; `decomposition_onset` → `decomposition`), and selected the Phase 4 sample. The post-extraction script never modified `evidence_quote`, `compound_name`, `value_raw`, or `source_url`. Phase 4 was a real 62-row stratified sample with 4 fresh-context audit subagents.

Both failures are genuine reading defects in narrow gaps the current rules don't cover:

- **Row 80** — `"Dark red solid;"` is verbatim and contains no value, so it satisfies every existing "do NOT allow" bullet in Step 6.1 (no missing words within the span, no doubled tokens, no reordering). The rule is implicitly "quote must contain the value" but nowhere stated explicitly.
- **Row 1608** — `"...Melting point coformer 324"` glues non-adjacent table cells with literal `...`. The forbidden-transformations list names missing words, doubled tokens, reordering — but not ellipsis-bridged spans.

Opus's diagnosis is the sharpest of the three: "quote must contain value" is *implied* but never *required*.

### GPT-5.5 high — what it revealed

GPT-5.5 confirmed it did not write a regex extractor (v1.4 mandate held), but it ran a different shortcut: parallel LLM batch workers + helper scripts for orchestration, with **no coordinator re-confirmation of merged rows**. The coordinator relied on:

- Deterministic schema checks (passed).
- Substring-presence quote check (passed even for masthead text).
- A Phase 4 sample of only 40 rows out of 907 (4.4 %), declared done after fixing the 6 it caught.

Specifically: the 4 masthead-as-quote failures slipped through because nothing in the post-merge checks required that `evidence_quote` *contain the value* — only that it appear somewhere in the paper file. The journal masthead appears in every paper. Truncation-residue failures (`Carboxamid`, `Phenyl(6′-`, `8-(1-(3-(5′-`) slipped through because the v1.3 `_TRUNCATED_LOCANT_PREFIX` pattern catches `H-Indeno...` but not generic terminal fragments.

GPT-5.5's diagnosis: "row exists in paper text" plus "worker says it read the paper" was allowed to substitute for row-level evidence support. The coordinator-accountability gap is real.

### Sonnet 4.6 — what it changed in our read

This is the largest revision. Sonnet 4.6's actual execution was **bimodal**:

- **Path A** (164 PMC + subdirectory papers, ~1,800 rows): parallel LLM extraction subagents reading papers directly. Protocol-compliant. The quotes for these rows are real verbatim substrings.
- **Path B** (20 standalone-PDF reference-table papers, 770 rows): `build_batch_pdfs.py` — a Python data-entry script that hardcoded compound names and values the agent had read manually from large tables, then constructed `evidence_quote` strings programmatically via f-string templates (`f"Table III: {nm} BP {bp_k} MP {mp_k}"`).

The script accounts for essentially all 22 "constructed quote" failures. The underlying data is mostly correct — Sonnet did read the tables — but the quotes were templated, not transcribed.

Sonnet's own counterfactual: if those 770 rows had come from direct LLM reads (as Path A did), the audit would have landed around 78–82 %, comparable to GPT-5.5's 86 %. The 55 % headline is almost entirely a Path-B artifact.

Sonnet's stated reasoning for Path B: writing a Python data-entry script "felt like a reasonable way to handle high-volume tabular data efficiently" for papers like Yalkowsky 1990 (85+ compounds × multiple columns). The v1.4 anti-pattern names `re.findall` + `pdftotext` specifically; a hardcoded data-entry script with no regex over paper text reads as outside the prohibition if interpreted literally.

### Cross-agent pattern: layered constraints failed in three different ways

Reading the three analyses together, the v1.4 skill's anti-regex mandate **worked in a narrow sense**: none of the three agents wrote `extract_mp_bp.py`-style regex extractors. It **failed in a broader sense**: two of three agents found alternative paths that the explicit prohibition didn't name.

| Agent | Anti-regex mandate held? | Quote-fidelity rule held? | Coordinator re-verified merged rows? | Phase 4 sample size |
|---|---|---|---|---|
| Opus 4.7 | Yes | Mostly (2 narrow gaps) | Yes (62-row stratified) | 3.3 % |
| GPT-5.5 high | Yes | No (masthead quotes passed substring-check) | No (declared done at 40 rows) | 4.4 % |
| Sonnet 4.6 | Yes (no regex) | No (Path B: templated quotes) | Mixed (Path A yes, Path B no) | varied |

The pattern: each agent stayed inside the *letter* of the existing rules but found a different way to satisfy them without the underlying methodology. The v1.5 changes have to generalize the constraints so that the methodology — not specific named scripts — is what's protected.

## Cross-trial pattern observations

### What the v1.4 update actually changed (gpt55_high before/after)

| | Trial-1 gpt55_high (v1.2/3) | Trial-2 gpt55_high (v1.4) |
|---|---|---|
| Rows emitted | 304 | 907 |
| Audit pass | 56 % | 86 % |
| Approach | Wrote `extract_mp_bp.py` (regex extractor) | Per-paper LLM extraction |
| Failure modes | Sentence-fragment compound names, citation numbers as °C, NMR shifts as mp, wrong-cell binding in tables | Truncation residue, masthead-as-quote, isomer/label confusion |

The v1.4 mandate worked. The failure modes shifted from "regex caught garbage" to "LLM made occasional mistakes during reading." Magnitude is much smaller and the remaining failures are recoverable surface defects.

### Why opus47 led

Opus 4.7 produced the best run because it follows the protocol most literally:
- Per-paper LLM reads (didn't write a script).
- Quote re-confirmation actually applied.
- Phase 4 self-verification visible in dir contents.

Its 1,864 rows is in the same range as Trial-1's 1,338 and gpt55_high's 907 — not an outlier on recall, but with substantially higher precision than either.

### Why sonnet46 underperformed

Sonnet 4.6 emitted the most rows (2,567) but the lowest precision. Two competing hypotheses:

1. **The agent slipped back toward scripted extraction** despite the v1.4 anti-pattern. The `build_batch_pdfs.py` / `fix_csv.py` files in the trial dir are circumstantial evidence.
2. **The agent maximized recall by relaxing the verbatim-quote rule.** The 22 paraphrased-quote failures all use the same Table-N-template formulation — suggests deliberate construction rather than direct quotation. This would explain the high row count.

Either way, the skill's quote-fidelity requirement didn't constrain sonnet46's output strongly enough.

## Implications and recommendations

### For the skill — consolidated v1.5 plan

The three self-analyses converged on a smaller, sharper set of changes than the post-audit speculation suggested. The plan below combines the high-conviction items from all three.

#### 1. Quote must contain the value AND the compound (or its code)

Every Trial-2 quote-only failure violates this rule, even though the existing prose doesn't state it explicitly. Three places to add it:

- **`SKILL.md` schema row** for `evidence_quote`: change from "Verbatim text from the source from which the value was extracted" to "Verbatim contiguous substring of the source. **MUST contain the numeric `value_raw` token AND the compound name (or its label like `4f`).** If you can't produce a contiguous span containing both, DROP the row."
- **`EXTRACTION_PROMPT_TEMPLATES.md` Step 6.0** (new, before Step 6.1 substring check): "Take the numeric portion of `value_raw` and substring-search it inside your `evidence_quote`. If the value isn't in the quote, the quote is incomplete — extend it across page/column/line breaks until it contains both the value and the compound name/code."
- **New `scripts/quote_support_lint.py`**: deterministic check that the numeric value from `value_raw` appears in `evidence_quote`, and the compound name (or a recognizable token from it) appears in `evidence_quote`. Wired into `run_all_checks.py`.

This single change closes Opus's row 80 and most of GPT-5.5's masthead failures.

#### 2. Forbid any script that produces final row values — not just regex extractors

The v1.4 anti-pattern names `re.findall` + `pdftotext`. Sonnet 4.6 read this literally and wrote a data-entry script that hardcodes values + templates quotes via f-strings — outside the letter of the rule, inside its spirit. Two additions:

- **Second anti-pattern entry** sitting next to the existing one, naming the data-entry-script case: "❌ A Python script that hardcodes compound names/values and constructs `evidence_quote` strings via f-strings (e.g., `f\"Table III: {nm} BP {bp}\"`). Even if you read the table manually, templated quotes are not verbatim. The quote must be a string a `grep -F` over the paper file would return."
- **General principle** added near both anti-patterns: "Scripts for orchestration, file enumeration, enum normalization, dedup, and audit dispatch are fine. Scripts that produce or transform `compound_name`, `value_raw`, `evidence_quote`, or `source_url` are forbidden. The LLM must produce those four fields by reading the source for the row that ends up in the deliverable."

#### 3. Forbid ellipsis / templated quotes — both prose and deterministic

- **Step 6.1 "Do NOT allow" list** gains a bullet: "Ellipsis-bridged spans (`compound X ... mp 220 °C` where `...` represents elision of non-adjacent text). The quote must be one contiguous substring."
- **New `scripts/quote_template_lint.py`**: flags the patterns Sonnet's script produced:
  - `^Table\s+[IVX\d]+[:,.]\s+\w` ("Table I. compound...")
  - `\bMP\s+\d{1,3}\b.*\bBP\s+\d{3}\b` ("MP 27 BP 286" inline)
  - Literal `...` or `…` in `evidence_quote` (catches ellipsis-bridges)
  - `\bMelting point \(deg C\)\b` (column-header text in quote)

Catches row 1608 and the bulk of Sonnet's Path-B failures in Phase 3, before Phase 4.

#### 4. Expanded compound-name shape lint

Extend `validate_compound_name.py` beyond the v1.3 `_TRUNCATED_LOCANT_PREFIX`:

- Names ending in unfinished suffix tokens: `Carboxamid$`, `Carbo$`, `carbonitril$`, `sulfonamid$`, dangling hyphen, dangling apostrophe/prime
- Unbalanced parens, brackets, braces, or primes
- Names starting with `(` or a bare substituent prefix locant
- Names containing procedure words (`solution`, `added`, `filtered`, `yield`, `afforded`, `NMR`, `IR`) that suggest an experimental paragraph rather than a compound name

Catches all 7 of GPT-5.5's truncation residues and most of Sonnet's substituent-prefix truncations.

#### 5. DOI must come from the paper file

Sonnet's 4 wrong-paper-DOI rows used DOIs that don't appear anywhere in the source files — likely training-memory guesses. Add to `SKILL.md` Phase 1 Step 2:

> Extract the DOI only from: (a) NXML `<article-id pub-id-type="doi">`, (b) the paper's front matter ("https://doi.org/..." or "DOI: 10.xxx"), (c) `metadata.json`. **Do not** use a DOI from the paper's reference list or bibliography — that's a cited paper's DOI. **Do not** use a DOI from training memory. If no DOI is in those locations, use the PMC / PMID / legacy fallback.

`verify_doi.py` already does substring matching against the paper file; this codifies the rule in prose so the extractor doesn't reach for a memory-guess in the first place.

#### 6. Phase 4 sampling rule + explicit parallel-dispatch pattern

Replace the current "fresh-context agent re-audit of a random sample" wording with a concrete rule:

- **Sample size: `max(100 rows, 5 % of total rows)`.** Floor of 100 ensures defensible statistics on small runs; 5 % scales linearly for large corpora.
- **Parallel dispatch: 25 rows per agent, one batch.** A 100-row audit = 4 fresh-context agents; a 500-row audit = 20 agents. Both run in roughly the same wall time.
- **On failure: run the relevant deterministic lint across the full CSV** to catch the same defect class everywhere, fix or drop matches, then run one more 100-row confirmation sample. Class-targeted sweeps catch ~100 % of a known defect; random re-sampling catches it at the prevalence rate.

Per-row audit cost is comparable to per-row extraction cost (both involve locating the paper and reading the relevant section), so 5 % sampling adds ~5 % to total agent-time. Since both stages parallelize the same way, it adds ~5 % to wall time. Affordable at any corpus size.

This codifies the pattern the project has actually used on every audit so far (4 agents × 25 rows) and prevents GPT-5.5's "I sampled 40 of 907 and called it done" failure mode.

### What we are *not* implementing for v1.5

- **Compound code in quote as a hard drop rule.** Useful as a `quote_support_lint.py` flag (`flagged_compound_code_absent_from_quote`) but not as a drop rule. Many legitimate paper sentences identify a compound by name without restating the code.
- **Adjacent-binding lint** (clusters with same source/property/value/similar compounds). Worth implementing eventually but lower priority — it's a heuristic flagger, not a deterministic gate. Defer to a v1.6 if the v1.5 changes don't close the residual gap.
- **Coordinator accountability rule** (parallel workers + post-merge re-verification). Worth saying in prose, but Opus's run shows it's not strictly required when the workers themselves follow protocol. The v1.5 row-support gates (`quote_support_lint.py`) accomplish the same end via a deterministic check rather than a process rule.

### For the project

- **Opus 4.7 is the recommended model** for running this skill in production. 98 % precision, complete adherence to the protocol, no protocol drift observed.
- **GPT-5.5 high is usable** at 86 % with v1.4. Remaining defects are minor surface issues; would benefit from quote re-confirmation enforcement.
- **Sonnet 4.6 is not production-ready for this skill in its current form.** 55 % precision is below the corpus' Trial-1 baseline and not suitable for downstream use without significant Phase 4 cleanup.

### For the academic writeup

This trial is the most interesting data point in the project. Same skill, same corpus, three different agents, three different outcomes. It demonstrates that:

- Skill quality is necessary but not sufficient for high extraction precision.
- Model adherence to written protocol varies substantially across agent families and versions.
- A skill that reaches 98 % with one model can reach 55 % with another; reporting "the skill achieves X %" without the model name is misleading.
- The v1.4 anti-pattern + mandatory-reading block successfully redirected GPT-5.5 from the regex-extractor pattern (Trial-1: 56 % → Trial-2: 86 %), but couldn't redirect Sonnet 4.6 from a constructed-quote pattern. The mechanism by which models read skill instructions matters as much as the content.

This is worth a dedicated section in the eventual paper: **"Cross-model variability in skill adherence."**

## Files

[Trial-2 gpt55_high audit verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial2/full-gpt55_high/_my_verdicts_all.json)
[Trial-2 opus47 audit verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial2/full-opus47/_my_verdicts_all.json)
[Trial-2 sonnet46 audit verdicts](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial2/full-sonnet46/_my_verdicts_all.json)
[Opus 4.7 self-analysis](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/reports/trial2_analysis_opus47.md)
[GPT-5.5 high self-analysis](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/reports/trial2_analysis_GPT55_high.md)
[Sonnet 4.6 self-analysis](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/reports/trial2_analysis_sonnet46.md)
[All trial outputs](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/)

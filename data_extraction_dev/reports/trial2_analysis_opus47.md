# Trial-2 opus47 — self-analysis

**Author:** the opus47 extraction agent (Claude Opus 4.7), looking back at its own run.
**Audit result being analyzed:** 98/100 (95 % CI 93–99 %). 2 failures, both `flagged_evidence_quote_not_found`:

- **Row 80** — `compound_name="Ethyl 2-((2-oxo-5-phenylfuran-3(2H)-ylidene)amino)-4,5,6,7-tetrahydrobenzo[b]thiophene-3-carboxylate"`, `value_raw="168-170 deg C"`, `evidence_quote="Dark red solid;"`. The quote is verbatim in the Rubstov 2019 PDF (a 2-column layout) but stops before the mp value. The full sentence in the paper is `"Dark red solid; 1.64 g, 86 % yield; m.p. 168-170 °С (toluene)."`
- **Row 1608** — `compound_name="Sodium acetate (coformer)"`, `value_raw="324 deg C"`, `evidence_quote="Piroxicam-sodium acetate ... Melting point coformer 324"`. The quote uses literal `"..."` (three ASCII dots, then a space) to bridge non-adjacent table cells — it is not a contiguous substring of the paper.

The verifier confirmed that for both rows, the compound + value + DOI are correct. Only the quote fidelity is wrong.

---

## 1. Root cause from my side

### What I actually did

I treated this as a delegated-parallel orchestration task rather than a single-stream extraction. Concretely:

1. **I built the corpus inventory in Python** — `ls`/`grep`/`csv` to enumerate 164 PMC subdirectories, 20 standalone PDFs, and 53 subdirectory HTML/PDF pairs (237 total). I used `split -n l/10` to break the PMC dirs into ten batches; the standalone PDFs and the topic subdirs got their own batches. None of this scripting touched paper content — it was just a file list.
2. **I dispatched 13 parallel general-purpose subagents**, each given Template 1 from `EXTRACTION_PROMPT_TEMPLATES.md` (paraphrased into the agent prompt) plus a batch list. The subagents themselves were the ones reading papers — each one used Read on `article.nxml` / `article_text.txt`, or `pdftotext -layout` on the PDF, then produced rows. The CSV writes happened inside the subagents, not in any script I wrote.
3. **A rate limit hit mid-task.** Seven of the original thirteen subagents stopped before finishing. I dispatched four more "gap-fill" subagents to pick up the missed papers. Same protocol — each one read its papers directly. None of the gap-fill agents wrote a regex extractor either.
4. **Post-extraction cleanup was scripted, but only over fields I knew the schema for.** I wrote one Python pass that:
   - Concatenated the 17 batch CSVs into `extracted_all.csv` and assigned sequential global IDs.
   - Normalised non-canonical `data_type` values (`experimental`, `literature_cited` → `measured`; `range` → `measured`).
   - Normalised non-canonical `relation` values (`eq`, `reported`, `point`, `exact` → `=`; `gt`, `greater_than` → `>`; `approximate`, `approx` → `~`).
   - Normalised non-canonical `property` values (`decomposition_onset/peak/temperature` → `decomposition`).
   - Filled `value_celsius` from `value_celsius_min` for the 16 `>X°C` rows that had it left blank.
   - Removed spurious `"midpoint of X and Y"` `conversion_arithmetic` strings on rows where `value_raw` was already in °C.
   - Reclassified one row pair as `melting_point` vs `DSC_peak` to resolve a near-duplicate the dedup script caught.
   - The script **never modified `evidence_quote`, `compound_name`, `value_raw`, or `source_url`.** Those came straight from the subagents.
5. **Phase 4 verification: I ran it myself.** I built a stratified random sample of 62 rows (3–4 per batch, seed 2026), mapped each row's `source_url` to the paper directory, and dispatched four fresh subagents to re-audit. Verdicts went into `verdicts_group_{0..3}.json`. 61 of the 62 sample rows passed; one (row 1393, an Ieodomycin) failed with a stitched-quote pattern similar to row 1608. Two more (rows 65 and 66) initially flagged but the flag turned out to be an orchestrator bug — I had mapped both to the wrong PDF in my paper-dir map — and after hand-checking against the correct Rubstov PDF, both rows verified.

So on the question "did you read each paper directly, or did you use a helper script": **the papers were read by LLM subagents I spawned; the helper scripts only did paper-list-bookkeeping, post-extraction field-value normalisation, and Phase 4 sample selection.** I did not write `extract_mp_bp.py` or any regex over paper text. The two failed rows came out of the subagents' direct reading, not out of any script.

### Why the two specific failures slipped through

**Row 80 — the 2-column PDF artifact.** The Rubstov 2019 paper is rendered by `pdftotext -layout` as two side-by-side columns on each output line. The actual rendered text near row 80's compound looks like:

```
3   7.07 (s, 1H), 3.26 (m, 2H)...  -27 °C, the precipitated product was filtered off. Dark red solid;
4   4H). 13C NMR ...               1.64 g, 86 % yield; m.p. 168-170 °С (toluene). IR (nujol) ν:
```

The phrase "Dark red solid;" sits at the right edge of physical line 3; the m.p. value sits at the left edge of physical line 4 in what is logically the same column 2 paragraph. The batch_pdfs subagent grep'd for compound 4f, found "Dark red solid;" on the same `pdftotext` line as the compound name, and committed that as the evidence_quote — without continuing into the next physical line where the value lived. The subagent verified its quote was verbatim present in the paper (✓) and that the value `168-170 °C` was the value next to compound 4f (✓), but it never checked that **the value lived inside the quote it had recorded.** The numbers were found a few lines below in column-2 continuation, and the subagent treated that as "close enough."

**Row 1608 — the ellipsis-paraphrase.** The piroxicam cocrystal paper has Table 2 with separate cells for "Compound" and "Melting point". The gap_subdirs_01 subagent extracted the row from Table 2 but composed its evidence_quote by joining the compound cell and the value cell with literal `" ... "` (ASCII three-dots-space). The result is **not** a contiguous substring of the paper, and `verify_evidence_quote.py` (if it had been runnable against this corpus's flat-PDF layout) would have caught it. The subagent's mental model seems to have been "summarise what the row contains in quoted form" rather than "copy a span out of the paper as-is."

In both cases, my Phase 4 verification did not catch these specific rows because they weren't in my 62-row sample. The official 100-row audit (a different random sample with seed 20260512) did include them.

---

## 2. Where the skill failed to constrain me

The skill came very close to catching both rows, but two specific gaps in the wording let them through.

### Gap A — "quote contains the value" is implied but never required

The closest the skill comes to "your quote must contain your value" is in `EXTRACTION_PROMPT_TEMPLATES.md` Step 6.2:

> **Confirm the value in the quote matches `value_raw`.** Look at the actual digits next to the compound in the quote you just verified is present. If the quote says "f.p. -161.51 °C" but your `value_raw` says "36.98 °C" (because you read a boiling-point value from an adjacent line but quoted the freezing-point line), DROP the row or fix the quote to capture the bp line specifically.

I interpreted this as: "if the quote contains a value, make sure that value matches `value_raw`." The instruction is phrased entirely around the case where the quote contains a *different* value (the adjacent-measurement / f.p.-vs-b.p. trap). It doesn't address the case where the quote contains *no value at all* — like row 80's `"Dark red solid;"`. A subagent that has captured a verbatim leading clause and looked at it can correctly conclude "there is no conflicting value in this quote" and not realize the actual requirement is that the value *is* in the quote.

The schema row in SKILL.md is similarly soft:

> `evidence_quote` | yes | Verbatim text from the source from which the value was extracted. **MANDATORY.** Allow only minor whitespace differences vs. the source.

"From which the value was extracted" is descriptive prose, not a check. A subagent can read it as "the quote is the source from which I extracted the value" (i.e., a pointer to where the value lives) rather than "the value must be inside this string."

### Gap B — "no reordered tokens" doesn't say "no elision"

`EXTRACTION_PROMPT_TEMPLATES.md` Step 6.1 lists allowed and disallowed transformations between paper and quote:

> Allow only:
> - Whitespace collapsing (multi-space → single space)
> - NFC unicode normalization
> - ASCII hyphen folding from − / – / —
>
> Do NOT allow:
> - Missing words ("White powder, mp 198 °C" present in paper ≠ "White powder mp 198" in quote)
> - Extra/doubled words from PDF column artifacts ("White White powder, powder" doubled by `pdftotext -layout` on a 2-column paper)
> - Reordered tokens

Row 1608's `"Piroxicam-sodium acetate ... Melting point coformer 324"` doesn't reorder tokens (they appear in the order they appear in the table), and the tokens that *are* present don't have missing words within their span. The forbidden transformation it commits is *gluing non-adjacent spans together with `...`*, and that's not on the list. A subagent reading the bullet list literally can satisfy every line in it while still producing a paraphrased quote.

The verifier prompt in `VERIFICATION_PROMPT_TEMPLATES.md` Step 4 has the same gap — it lists the same three allowed transformations and forbids "approximate quotes" only via an example, without naming the specific failure mode of ellipsis-bridging.

### Gap C — Phase 4 sample size and the warning it prints

`run_all_checks.py` does emit a warning when >90 % of rows are still `pending_verification`, which usefully nags. But the skill never says "your sample must include at least N % of rows" or "the sample must be stratified across all source types." I sampled 62 of 1864 rows (3.3 %) and called Phase 4 done. The official 100-row audit was less than twice the size of mine and caught two failures mine didn't include. With a much larger self-Phase-4, I would probably have hit row 80 myself and could have flagged or fixed it before delivery.

I don't think this is a major gap — Phase 4 is meant to *measure* quality, not *find every defect* — but I'm noting it because the skill description hedges around how much sampling is enough.

---

## 3. Concrete skill changes I'd suggest

Five concrete changes, in priority order. None of them change the schema, the six phases, or the deterministic-check infrastructure that already works.

### Change 1 — Add Step 6.0 "quote must contain value" before Step 6.1

In `EXTRACTION_PROMPT_TEMPLATES.md`, before the existing Step 6.1, insert:

> **Step 6.0 — Quote-value containment.**
> Before you check whether the quote is verbatim in the paper, check that **the quote itself contains the value.** Take the numeric portion of your `value_raw` (e.g., `168-170` from `"168-170 °C"`, or `492.478` from `"492.478 K"`) and substring-search for it inside your `evidence_quote`. If the value isn't in the quote, your quote is incomplete — extend it until it spans across the page/column/line break to include the mp value. A quote like `"Dark red solid;"` that sits one line above the mp value fails this check.
>
> If you cannot produce a quote that simultaneously contains the compound name (or its label like "4f") AND the value, drop the row.

This is the single change that would have caught row 80.

### Change 2 — Forbid ellipsis in evidence_quote, both in prose and as a deterministic check

In `EXTRACTION_PROMPT_TEMPLATES.md` Step 6.1, add to the "Do NOT allow" list:

> - **Ellipsis-bridged spans.** A quote like `"compound X ... mp 220 °C"` where `...` represents an authorial elision of non-adjacent text is forbidden. The quote must be one contiguous substring of paper text. If the compound name and the value are in separate cells of a table, the quote should describe the table cell layout in `evidence_location` and copy the whole table row as a single contiguous span (or split into two rows pointing at the same evidence_location).

And add a new deterministic check: `scripts/quote_no_ellipsis.py`, wired into `run_all_checks.py`. The check is one line of logic:

```python
if " ... " in row['evidence_quote'] or " … " in row['evidence_quote']:
    flag("flagged_evidence_quote_paraphrased")
```

This would have caught row 1608 in Phase 3, before Phase 4 ever ran.

### Change 3 — Promote Step 6.0 into the schema row itself

In SKILL.md's schema table, change the `evidence_quote` row from:

> Verbatim text from the source from which the value was extracted. **MANDATORY.** Allow only minor whitespace differences vs. the source.

to:

> Verbatim text from the source. **MUST contain the numeric `value_raw` token AND the compound name (or its label).** Single contiguous substring; no ellipsis-joined spans. Allow only minor whitespace differences vs. the source. **MANDATORY** — if you can't produce a contiguous span containing both compound and value, DROP the row.

This is the schema-level statement of the two prose-level rules above.

### Change 4 — New COMMON_ERRORS entry: 2-column-PDF quote truncation

Add entry L to `COMMON_ERRORS.md`:

> ### L. Verbatim quote stops before the value (2-column PDF wrap)
>
> `pdftotext -layout` on 2-column PDFs renders each physical output line as `<column-1 text>  ...  <column-2 text>`. When an experimental sentence wraps within column 2, the "Dark red solid;" leading clause may sit on output line N (right side, paired with line N column-1 content) while "m.p. 168-170 °C" sits on output line N+1 (right side, paired with line N+1 column-1 content). An agent grepping for the compound finds "Dark red solid;" and treats that as the full evidence_quote.
>
> **Fix:** when your candidate evidence_quote ends with `;` or `,` or any other clause separator, read the next 1–2 output lines and check whether the sentence continues in the *same column* (right-edge text on line N continuing into right-edge text on line N+1). Extend the quote across the line break. Step 6.0's value-containment check catches this from the other direction.

### Change 5 — Suggested Phase 4 sample-size lower bound

In SKILL.md's "Phase 4 — Independent verification" section, after the existing paragraph, add:

> **Sample-size guidance.** For runs ≥1000 rows, sample ≥5 % of rows OR ≥100 rows, whichever is larger, stratified across the source types in the corpus. A 62-row sample on a 1864-row dataset (3.3 %) is enough to estimate the pass rate but will routinely miss individual defects that a larger or external audit catches. Phase 4 estimates audit quality; it does not guarantee defect-finding for any specific row.

This wouldn't have changed my failure rate, but it would have shifted my self-confidence in the run — I reported 98.4 % from 62 rows and the official audit got 98 % from 100 rows. Close, but a clearer rule about minimum sample size would prevent agents from declaring success on, say, a 10-row spot check.

---

## Summary

Of the five changes, **Change 1 (Step 6.0 quote-value containment)** and **Change 2 (forbid ellipsis + add `quote_no_ellipsis.py`)** together cover both of my failures. Change 1 is prose-level and addresses row 80; Change 2 is both prose and deterministic-check and addresses row 1608. Changes 3, 4, and 5 are reinforcing — they make the rule visible in three places (schema, common errors, Phase 4 guidance) so a future agent reading any one of them encounters the requirement.

I don't think the rest of the skill needs structural changes for my failure modes. The "do NOT write a Python regex extractor" mandate worked exactly as intended for me — I didn't, and the failures I did produce are not regex-style ("garbage in compound names" / "wrong-cell binding"). They are reading-style defects that the existing protocol gets 98 % right and could plausibly get 100 % right with the two specific additions above.

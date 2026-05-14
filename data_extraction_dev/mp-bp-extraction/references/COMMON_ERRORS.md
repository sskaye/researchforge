# Common errors in mp/bp extraction

This file catalogs error patterns observed in real extraction runs of this skill, with concrete examples, root causes, and how the protocol prevents them.

**This file is intentionally minimal at v1.** Past attempts on this problem produced many error patterns, but most of those were specific to a regex-based extraction approach. Re-listing them here would presuppose that this LLM-driven skill will exhibit the same failure modes — and it likely won't. We will add entries here **only as we observe and verify errors in real runs of this skill.**

When an error pattern is observed during a trial:
1. Note the specific example (which paper, which row).
2. Identify the root cause (extraction-side, source-side, or verifier-side).
3. Decide whether the protocol can prevent it via a new rule or a refined script.
4. Add an entry here documenting the pattern + prevention.

---

## Carried-forward known patterns (from prior work, may or may not recur)

These were observed in a regex-based predecessor and are worth checking for in the first trial. They may not recur in the LLM-driven approach.

### A. NMR / mass-spec chemical shifts read as mp/bp values

**Pattern:** A number like `130.31` extracted as a melting point, when in fact it's a 13C NMR ppm chemical shift in the same paper's characterization section.

**Example (predecessor):** Paper 020 c00015, value=130, came from `δ 163.67 (C1, C3), 140.40 (C4'), 134.59 (C2'), 130.56 (C7a, C3a), 130.31 (C6, C5)`.

**Prevention in this skill:** Phase 2 step 5 explicitly tells the agent not to extract from NMR / mass-spec context. Phase 4 verifier reads the surrounding text and rejects on `flagged_value_mismatch` if the "quote" is from an NMR/MS section.

### B. Truncated / fragmented compound names from PDF line wrapping

**Pattern:** A long IUPAC name that wraps across two PDF lines gets captured as just the second-line substituent fragment, e.g., `Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl` — a `-yl` substituent, not a parent compound.

**Example (predecessor):** khalifa_2024_thiopyrimidine_sulfonamide — 14 rows of fragment names.

**Prevention in this skill:** Phase 2 explicitly instructs the agent to reassemble multi-line names before emitting. Phase 3 has a "truncated-name pattern" check (`-yl$`, `-yloxy$`, etc.). Phase 4 verifier compares the row's name against the paper's actual full name.

### C. Multi-row table thead column misalignment

**Pattern:** A table whose header spans multiple rows (e.g., "compound | exp. | calc. | predicted") causes a programmatic extractor to bind a value to the wrong column. Result: Chloroquine's row inherits Thalidomide's value.

**Example (predecessor):** Paper 064 Table 5 — STRM/SIRM/[ref] sub-columns; extractor mis-mapped 5+ rows.

**Prevention in this skill:** The LLM reads the actual table layout rather than parsing it from raw text positions. Phase 4 verifier re-reads the table cell and confirms (row, col) alignment.

### D. Workup solvent names extracted as the product

**Pattern:** `CH2Cl2` in an `Rf: 0.3 (CH2Cl2:MeOH 95:5); mp 165 °C` annotation gets captured as the compound — but the mp belongs to the actual product, not the eluent.

**Example (predecessor):** Paper 020 c00010 — CH2Cl2 bound to mp 165.

**Prevention in this skill:** Phase 2 step 5 lists common workup solvents (CH2Cl2, EtOAc, MeOH, DMSO, DMF, THF) to drop when they appear in `Rf:` or eluent context. Phase 4 verifier rejects on `flagged_compound_mismatch` if the row's name is a solvent and the value is for a different compound.

### E. PDF sign-loss

**Pattern:** A negative value like `−77.9 °C` rendered in PDF text as `277.9 °C` because the leading minus sign is stripped or rendered as a "2" by the PDF text extractor.

**Example (predecessor):** Paper 2009_Dearden — multiple Methanol / Benzene mp rows.

**Prevention in this skill:** The LLM extracting from PDF text via `pdftotext` will see `277.9 °C` — same artifact. The defenses are: (a) value_range_check flags 277.9 °C as suspiciously out-of-range for a small organic; (b) Phase 4 verifier reads the surrounding context and notes the discrepancy with chemistry expectations. If the LLM has access to the original PDF (not just stripped text), it may see the minus sign directly.

### F. Bare-code compound names

**Pattern:** Compound name is just a paper-local code like `compound 5`, `complex 9a`, `4b`. The code has no chemistry meaning outside that paper.

**Prevention in this skill:** Phase 2 step 5 lists bare codes as a drop pattern. Phase 3 has a required-field / format check that flags compound_name matching `^(compound|complex|cpd)\s+\d+[a-z]?$` or `^\d+[a-z]?$`.

### G. Wrong-paper DOI

**Pattern:** A DOI in the row's `source_url` resolves to a completely different paper. Common when the extractor invents a likely DOI rather than reading the file.

**Prevention in this skill:** Phase 1 step 3 runs CrossRef title check at extraction time. Phase 3 `verify_doi.py` confirms the DOI appears in the paper file's text.

### H. Memory-based fabrication

**Pattern:** Agent without access to the file generates plausible values from training memory. The specific decimals are wrong even when the compound is well-known.

**Prevention in this skill:** Hard rule in Phase 1 + Phase 2: every row must have an `evidence_quote` drawn from a file actually read. The Phase 4 verifier confirms verbatim presence. If the agent can't read the file, it must report INACCESSIBLE rather than emit values.

---

## Observed in this skill's trials

### I. Adjacent-measurement quote

**Pattern:** Compound + value are correct, but `evidence_quote` points at a different adjacent measurement on a nearby line.

**Example (Trial-1-val row 147):** Methylcyclobutane, claimed `value_raw = "36.98 °C"` (boiling point). The paper contains `"b.p. 36.98° (755 mm.)"` (correct) but the agent recorded `evidence_quote = "f.p. -161.51"` (the freezing point on an adjacent line). All other fields are correct; the quote just points at the wrong measurement.

**Prevention:** SKILL.md Phase 2 quote re-confirmation step (added in v1.2) requires the agent to substring-search the paper for the quote AND confirm the value in the quote matches `value_raw`. If the quoted text doesn't carry the recorded value, drop the row or rewrite the quote.

### J. Doubled-token PDF artifact

**Pattern:** `pdftotext -layout` on 2-column scientific PDFs sometimes duplicates words at column boundaries ("White White powder, powder"). The agent transcribes the artifact instead of the actual paper text.

**Example (Trial-1-val row 296):** Khalifa 2024 M7 compound, mp 257–260 °C. The actual paper line reads `"White powder, mp 257–260 °C"` but the agent's extracted text had `"White White powder, powder, mp"` due to column-doubling. The agent recorded the doubled form as `evidence_quote`.

**Prevention:** SKILL.md Phase 2 quote re-confirmation step rejects doubled tokens explicitly. Optional: also run `pdftotext` without `-layout` and cross-reference, OR strip repeated adjacent tokens at extraction time.

### K. Misapplying the skill as a Python regex extractor

**Pattern:** Agent reads SKILL.md and concludes "this is a Python pipeline; my job is to write the missing extraction script." Writes `extract_mp_bp.py` that uses `pdftotext` + `re.findall` over paper text to bulk-emit rows, with `evidence_quote` populated from the regex match.

**Example (cross-harness validation):** A parallel agent on the same 168-paper corpus wrote a regex extractor following this misreading. The extractor:
- Maintained the schema correctly (`evidence_quote`, `source_url`, etc.).
- Passed all the deterministic Phase 3 checks on its 304 output rows.
- Reached **56 % audit pass rate** in independent verification — vs. **93 %** for the LLM-driven approach prescribed by this skill on the same corpus.

**Failures it produced:** Sentence fragments captured as compound names ("Rf = 0.21 (Hexane/EtOAc, 1:4) and"); citation numbers extracted as temperatures (`16 °C` from `[16]`); ring locants treated as °C (`5 °C` from "5-substituted"); counts of compounds treated as values (`307 °C` from "307 hydrocarbons"); NMR shift lists captured as compound names; PDF-column-merge row swaps in dense tables.

Regex can't distinguish these cases from real `compound + value` pairs even when `evidence_quote` is enforced — the quote IS present in the source file, it just contains text adjacent to an mp pattern that isn't actually a measurement.

**Prevention in this skill:** v1.4 added an explicit MANDATORY-READING block at the top of SKILL.md stating that the agent reads each paper directly and does NOT write a Python regex extractor. The anti-patterns list has a corresponding entry. The skill's `description:` front-matter (used for skill selection) calls out "LLM-driven" extraction and explicitly forbids the regex approach. `run_all_checks.py` prints a warning if >90 % of rows are still `pending_verification`, since shipping without Phase 4 verification is how this failure mode goes undetected.

### L. Verbatim quote stops before the value (2-column PDF wrap)

**Pattern:** `pdftotext -layout` on 2-column PDFs renders each physical output line as `<column-1 text>  ...  <column-2 text>`. When an experimental sentence wraps within column 2, the leading clause (e.g., `"Dark red solid;"`) lands on output line N (right side) while the value (`"m.p. 168-170 °C"`) lands on output line N+1 (right side). An agent grepping for the compound finds the leading clause on the same `pdftotext` line as the compound name and commits that as the `evidence_quote` — verbatim present in the paper, but it doesn't actually contain the value.

**Example (Trial-2 opus47 row 80):** Compound = `Ethyl 2-((2-oxo-5-phenylfuran-3(2H)-ylidene)amino)-...`, value_raw = `"168-170 deg C"`, evidence_quote = `"Dark red solid;"`. The full sentence in the paper is `"Dark red solid; 1.64 g, 86 % yield; m.p. 168-170 °С (toluene)."` The quote stopped at the leading clause; everything after the semicolon (including the value) was missed.

**Prevention in this skill:** v1.5 added Step 6.2 of the quote re-confirmation: "Confirm the quote contains the value." Take the numeric portion of `value_raw` and substring-search inside `evidence_quote`. If the value isn't there, the quote is incomplete — extend it across the column / line break until it contains both compound and value. The deterministic `scripts/quote_support_lint.py` catches this in Phase 3.

### M. Constructed / templated quotes from a data-entry script

**Pattern:** Agent reads SKILL.md, notes that a regex extractor is forbidden, but writes a Python data-entry script that hardcodes compound names + values read manually and constructs `evidence_quote` strings via f-string templates:

```python
add(nm, mp, bp, f"Table III: {nm} BP {bp} MP {mp}")
```

The underlying compound + value are usually correct, but the quote strings don't appear verbatim in the source — they're paraphrases. The v1.4 regex-extractor anti-pattern doesn't catch this because no regex is involved.

**Example (Trial-2 sonnet46):** `build_batch_pdfs.py` produced 770 rows from 20 large reference-table PDFs (Yalkowsky 1990, Mitchell 2008 SI, etc.). Templated quotes included `"Table III: 1,2-diiodobenzene BP 286 MP 27"`, `"compound ... Expt. 158.3"`. About 22 of 45 audit failures (~half) traced to this script. Stated rationale: "writing a data-entry script felt efficient for high-volume tables."

**Prevention in this skill:** v1.5 generalized the anti-pattern from "no regex extractor" to "no script that produces or transforms the four evidence-locked fields (`compound_name`, `value_raw`, `evidence_quote`, `source_url`)." Specific anti-pattern in SKILL.md names f-string-templated quotes. New `scripts/quote_template_lint.py` deterministically flags the patterns observed (`^Table\s+[IVX\d]+[:,.]`, inline `MP X BP Y`, literal `...` in quote, column-header tokens used as separators).

### N. DOI from training memory or bibliography

**Pattern:** Agent can't find a DOI in the paper file's front matter and (a) guesses one based on the journal/year/title from training memory, or (b) picks a DOI from the paper's *reference list* (those DOIs belong to cited papers, not this paper). The wrong DOI then propagates as the `source_url`.

**Example (Trial-2 sonnet46):** 4 rows cited DOIs that don't appear anywhere in the source files. Two rows cited `10.1002/cbdv.202500394` for compounds that are actually in `10.1002/ardp.70227` (PMC13006720); two rows cited `10.1002/chem.202500386` for content from `10.1002/cmdc.202500751`.

**Prevention in this skill:** v1.5 SKILL.md Phase 1 Step 2 and EXTRACTION_PROMPT_TEMPLATES.md Step 1b both state explicitly: extract DOIs only from (a) NXML `<article-id pub-id-type="doi">`, (b) PDF front matter (first 1–2 pages), or (c) `metadata.json`. The DOI must appear as a substring of the paper file's text. If none of these has a DOI, use the PMC / PMID / `legacy:` fallback. **Never guess** — `verify_doi.py` substring-checks the DOI against the paper file and will catch a memory-guess, but the rule has to apply at extraction time too.

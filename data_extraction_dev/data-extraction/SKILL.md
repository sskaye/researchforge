---
name: data-extraction
description: LLM-driven evidence-locked extraction of chemistry property data from supplied journal articles. Generic at its core; the property family (mp/bp, redox, etc.) is supplied as a data-type overlay under the datatypes/ folder. The agent reads each paper directly and writes rows with a mandatory evidence_quote. Phase 0 enumerates the corpus to _corpus_manifest.txt (descending into subfolders); intentional exclusions go in _skipped.txt. The four fields compound_name, value_raw, evidence_quote, source_url come from LLM reading, not scripts — no regex extractors, no data-entry helpers. DOIs must come from the paper file, never from memory. Past trial outputs are reference, not protocol. Phase 4 independent verification is mandatory (max(100, 5%) parallel sample). The user MUST specify the data type (e.g., mp_bp, redox); the skill halts if no matching overlay exists. Apply when compiling, auditing, or extending a property database from supplied papers.
version: v2.1
---

# Data extraction protocol

## How this skill is applied — MANDATORY READING

**This skill is applied by an LLM agent reading each paper directly. It is NOT applied by writing a Python extraction script.**

You — the agent invoking this skill — will:

1. **Identify the data type you are extracting** (e.g., `mp_bp`, `redox`). The user must specify this explicitly. Read `datatypes/<datatype>/OVERLAY.md` for the property-specific schema, anti-patterns, value ranges, and example row BEFORE starting Phase 0. If the named overlay folder doesn't exist under `datatypes/`, **halt and ask the user** to either pick from the available data types or write a new overlay first. This is a hard rule — no inference from corpus content, no fallback to a "generic" extraction without an overlay.
2. **Enumerate the corpus first (Phase 0).** Before processing any paper, write `_corpus_manifest.txt` listing every paper-bearing location, descending into subfolders. Any location you intentionally skip goes in `_skipped.txt` with a reason. Do NOT silently omit corpus parts.
3. **Iterate the corpus one paper at a time.** Use the Read tool / bash / `pdftotext` to open each paper's `article.nxml`, `article_text.txt`, or `article.pdf` and read the actual text.
4. **For each paper, write extracted rows yourself.** Apply the EXTRACTION_PROMPT_TEMPLATES.md Template 1 protocol per paper. Each row must include a verbatim `evidence_quote` drawn from text you actually read.
5. **Run the bundled scripts AFTER extraction as deterministic checks** — they validate compound names, value ranges, unit arithmetic, CSV formatting, evidence-quote presence, etc. They are NOT the extraction engine. Always invoke `run_all_checks.py` with `--datatype <name>` so the overlay's data-type-specific checks (value ranges, conversion math) are included.
6. **Run mandatory Phase 4 independent verification** before declaring the output ready. Dispatching fresh Claude agents (or equivalent) to re-audit a random sample against the source papers is required, not optional.

You will NOT:

- **Write a Python regex extractor** (e.g., `extract_<property>.py` that calls `re.findall` over paper text and emits rows in bulk). Past attempts at regex-based extraction on this exact problem plateaued at 56-67% audit pass rate even after extensive iteration. The LLM-driven approach reaches 93-100% on the same corpus.
- **Run extraction as a single batch script.** Parallelization is fine — you can dispatch multiple LLM agent invocations to handle different paper batches concurrently — but each agent must read its papers directly, not write a regex pipeline.
- **Skip Phase 4 verification and ship rows as `pending_verification`.** Without Phase 4 evidence the audit pass rate is unmeasured; reports must not claim quality numbers.
- **Extract without a data-type overlay.** If the user hasn't specified one, halt and ask. Do not infer the data type from corpus content.

### Pre-flight checklist

Before starting, confirm:

- [ ] I have been told the data type to extract (e.g., `mp_bp`, `redox`) and `datatypes/<datatype>/` exists. I have read its `OVERLAY.md` end-to-end.
- [ ] I am an LLM agent applying this protocol by reading papers directly.
- [ ] I will NOT write a Python regex extractor. The scripts in `scripts/` and `datatypes/<datatype>/scripts/` are post-extraction checks only.
- [ ] **Before Phase 1**, I will enumerate every paper-bearing location in the corpus (descending into subfolders) and write the enumeration to `_corpus_manifest.txt`. Anything I intentionally skip will be logged in `_skipped.txt` with a one-line reason. I will NOT silently skip parts of the corpus. See Phase 0 below.
- [ ] I will process each paper via Read / bash / `pdftotext` and produce rows with mandatory verbatim `evidence_quote`.
- [ ] I will run Phase 4 independent verification (fresh-context agent re-audit of a random sample) before declaring success.
- [ ] I will treat any past trial's outputs as historical reference, NOT as protocol. Operational choices made in previous runs do not bind this one.

## Goal

Produce a CSV of property measurements where **independent spot checks find zero data-extraction errors**. The literature may disagree across sources for the same compound — that's normal and acceptable. What is not acceptable is misattributing a value to a paper, mis-stating a unit, fabricating a citation, or producing values from training memory.

## Why the discipline matters

A property database without provenance is worse than no database — downstream users will trust it for design and synthesis decisions, and each fabricated row poisons the dataset. Past attempts on extraction problems like this produced 30–60 % extraction-error rates when independently spot-checked. Errors that look plausible (right compound, right ballpark value, wrong specific number or wrong source) are the most damaging.

This protocol forces:

- A **verbatim evidence quote** for every row, locatable in the cited paper in under 30 seconds.
- **No memory-based extraction** — if a paper file can't be read, the agent must skip rather than synthesize.
- **Independent verification** — a fresh-context agent re-reads the source and confirms the quote, without seeing the extractor's notes.

## Input contract

The user provides a directory containing one subdirectory per paper. Each subdirectory may contain:

- An NXML file (`article.nxml` from PMC) — preferred when available
- A PDF (`article.pdf`)
- A pre-extracted text file (`article_text.txt`)
- A metadata file (`metadata.json`) — may have DOI / title

The agent **must read these files** to extract values. It is forbidden to extract values that aren't supported by text actually present in the provided files.

## The schema

The deliverable is a **single CSV** with 18 columns. One row per (compound × property × value). The schema below is the v2.0 generic core; each overlay's `SCHEMA.md` declares its property enum, standardized unit string, and any extension columns.

| Column | Required | Notes |
|---|---|---|
| `id` | yes | Sequential integer row identifier. |
| `verification_status` | yes | One of `pending_verification`, `verified_extraction`, `verified_textbook`, `verified_by_audit`, `audit_corrected`, `flagged_review`, `unverified`. New rows start `pending_verification`. |
| `compound_name` | yes | Full IUPAC, common, or recognizable trivial name. **Never truncated** (e.g., `5-acetyl-2-ethyl-…-quinolone`, not `5-acetyl`). For ionic-liquid / coordination-salt shorthand of the form `[cation][anion]`, the shorthand itself is acceptable. Standardized across data types so future joins are possible. |
| `compound_smiles` | optional | SMILES when the source provides one. Empty when not provided. |
| `property` | yes | The specific property recorded. Each overlay defines its enum (e.g., mp_bp: `melting_point`, `boiling_point`, `DSC_onset`, etc.). |
| `value` | yes | The value in the property's standardized unit (the overlay's `SCHEMA.md` declares it). Usually numeric; may be a categorical string for non-numeric properties (e.g., state-of-matter `solid`). Nothing in the generic schema or scripts blocks non-numeric strings. |
| `value_min`, `value_max` | when range | When the source reports a range. Empty for single values. |
| `value_raw` | yes | As printed in the source, including original units (e.g., `"188–190 °C"`, `"1655 K"`, `"−77.9 °C"`, `"200 °F"`). |
| `units` | yes (numeric) | The unit of `value` (e.g., `°C`, `V vs SHE`, `Pa·s`). Empty allowed only for categorical properties. |
| `relation` | yes | One of `=`, `>`, `<`, `~`, `≈`. Use `=` for an exact value; `>` for ">300 °C", etc. |
| `meas_calc` | yes | `measured` (any experimental measurement, including ones compiled from other literature) or `calculated` (predicted by a model, e.g., QSPR / MPBPVP / DFT). |
| `source` | yes | Citation: journal, year, vol, page (or paper title). **NO author names** — the DOI in `source_url` is the canonical identifier when present. When no DOI exists, `source` MUST include journal + year + volume + page so the paper is still identifiable. |
| `source_url` | yes | One of, in priority order: (a) a DOI URL `https://doi.org/10.xxx/xxxxx`; (b) `pmc:PMCxxxxxxx` when the paper has a PMC ID but no DOI; (c) `pmid:xxxxxxxx`; (d) `textbook:<short-id>` for textbook references. Always non-empty. |
| `evidence_location` | yes | Precise pointer (e.g., `"Table 1 row 3"`, `"p. 6469 col 2 ¶ 3"`, `"SI Table S4 row 12"`, `"section 3.2.5 ¶ 1"`). |
| `evidence_quote` | yes | Verbatim text from the source containing the value (and ideally the compound name or its serial code). **MANDATORY** — every row must carry one. Prefer a contiguous substring; allow only minor whitespace differences vs. the source. Quote fidelity is a verifiability concern (Tier 2), not a correctness gate. |
| `conversion_arithmetic` | when conversion applied | Math shown explicitly per v2.0 standardized syntax (see below). Empty when no conversion was applied. |
| `notes` | optional | Free text; flag-reason details, family / class, audit history, etc. |

### Empty-when-not-applicable conventions (v2.0)

- `compound_smiles` empty when the source has no SMILES.
- `value_min` / `value_max` empty for single values (only set when value is a range).
- `units` empty for categorical-valued properties; required when value is numeric.
- `conversion_arithmetic` empty when no conversion was applied.
- `notes` empty by default.

All other generic columns are required to be populated. Each overlay can declare its own empty-allowed conventions for its extension columns.

### Conversion-arithmetic syntax (standardized in v2.0)

The `conversion_arithmetic` column uses a single format across every data type:

```
<input_value_with_units> <operator> <constant> = <output_value_with_units>
```

Examples:

- mp/bp Kelvin → Celsius: `300 K − 273.15 = 26.85 °C`
- mp/bp Fahrenheit → Celsius: `(300 °F − 32) × 5/9 = 148.89 °C`
- redox SCE → SHE: `+0.40 V vs SCE + 0.241 = +0.641 V vs SHE`

Both ASCII operators (`-`, `*`) and unicode (`−`, `×`) are accepted by the syntax lint, but new outputs should use unicode. `scripts/conversion_arithmetic_lint.py` verifies the syntax shape; the overlay's own conversion script verifies the math.

### Verification status values

Set by the **extractor**:

- `pending_verification` — newly extracted, not yet through Phase 4.

Upgraded by the **verifier** (Phase 4):

- `verified_extraction` — extracted by an agent that read the provided file, independently verified.
- `verified_textbook` — standard reference (CRC, IUPAC tables); no Phase 4 needed.
- `verified_by_audit` — pre-existing row that passed an explicit audit.
- `audit_corrected` — issue found and explicitly corrected (with audit trail in notes).

Set by audits or sanity checks:

- `flagged_review` — issue found; details in notes. Granular reasons go in `notes`:
  `flagged_doi_unresolvable`, `flagged_doi_unrelated_paper`,
  `flagged_evidence_quote_not_found`, `flagged_value_mismatch`,
  `flagged_compound_mismatch`, `flagged_unit_conversion_error`,
  `flagged_value_out_of_range`, `flagged_metadata_mismatch`,
  `flagged_compound_name_truncated`, `flagged_compound_name_bare_code`.
- `unverified` — residual that didn't fit other categories.

**Why no author field:** The DOI in `source_url` uniquely identifies the paper. Author names add error surface.

**Why a single file:** Tier filtering happens via `verification_status`. Don't split into separate files by tier or by `meas_calc`. For cross-property datasets, run the skill twice (once per data type) and join the two CSVs on `compound_name` afterwards.

## Worked example

See `datatypes/<datatype>/OVERLAY.md` § Worked examples for fully-populated rows covering the patterns this overlay sees most often.

## The phases

### Phase 0 — Corpus manifest (required, before anything else)

Before processing any paper, enumerate every paper-bearing location in the corpus. The goal is to make the set of papers you will process explicit and accounted for. Silent omission of corpus parts has been the dominant recall problem in past trials.

**Required outputs:**

- `_corpus_manifest.txt` — one entry per paper-bearing location in the corpus. **Descend into subfolders.** A paper-bearing location is anything that contains an article body: an indexed subdirectory containing `article.nxml` / `article.pdf` / `article_text.txt`, a standalone `.pdf` file at the corpus root or inside a category subfolder, an `article.html` companion to a PDF, or any other layout the corpus actually uses. Use whatever enumeration mechanism is appropriate for the corpus layout (`ls`, `find`, `glob`, etc.).
- `_skipped.txt` — one line per paper-bearing location you intentionally exclude from extraction, formatted as `<location>\t<reason>`. Use the most specific reason; ask the user before using a free-text reason. The reasons below are property-agnostic; each overlay may add a small number of property-specific reasons (e.g., `no_mp_bp_data_in_text` for the mp_bp overlay) — see your data type's OVERLAY.md.

**Generic skip-reason vocabulary (applies to every data type):**

- `review_no_per_compound_binding` — review / ML / QSPR paper whose data is aggregate-only or not cleanly bindable to individual compounds.
- `bare_code_compounds_only` — compounds referenced only by paper-local codes (`compound 4a-l`) with no IUPAC / common names. (This is a paper-level skip ONLY when the paper has no named compounds at all. A paper with some named compounds and some bare codes is NOT a `bare_code_compounds_only` skip — emit the named rows and drop the bare-code rows individually per Phase 2 step 5.)
- `binding_ambiguous` — property values present but not cleanly bindable to compounds in the linearized text (multi-row table heads, missing row labels after PDF flattening, etc.).
- `image_only_compound_table` — compound table consists of structure images without textual names; no extractable text.
- `formulation_only_no_discrete_compound` — values are for mixtures or formulations, not pure compounds.
- `paper_unreadable` — file is corrupt, encrypted, or empty after `pdftotext`.

**Per-paper skip vs per-row drop.** The skip vocabulary above is for whole-paper exclusion (the paper contributes zero rows to the deliverable). A paper that has some extractable rows and some that should be dropped does NOT belong here — emit the good rows and drop the bad ones individually using the overlay's per-row drop patterns. The distinction matters because conflating the two systematically loses extractable data.

**Phase 1 is gated on the manifest being non-empty.** If your manifest has zero entries, stop — the corpus path is wrong or the enumeration is broken.

**The EXTRACTION_SUMMARY.md you produce at the end must account for every manifest entry as either processed or skipped-with-reason.** The accounting is `processed + skipped == manifest`, no silent loss.

**Do not skip a paper-bearing location because a prior trial run skipped it.** Past trials are reference, not protocol. See the anti-pattern about this in the anti-patterns section.

### Phase 1 — Source preparation (per-paper, after Phase 0)

For each paper subdirectory in the user's input:

1. **Read the files.** Open the NXML if present; otherwise extract text from the PDF (`pdftotext -layout`). Read `metadata.json` if present.
2. **Identify the paper's canonical identifier.** Extract from the paper file ONLY — never from training memory, never from the paper's reference list. The DOI in `<reference>` / bibliography entries belongs to a *cited* paper, not to this paper. Use only these locations, in priority order:
   - **DOI.** NXML `<article-id pub-id-type="doi">`, the PDF front matter (first 1–2 pages), or `metadata.json`. The DOI must appear as a substring of the paper file's text. If found, this is the `source_url` (as `https://doi.org/<DOI>`).
   - **PMC ID.** NXML `<article-id pub-id-type="pmc">` or `PMC########` in PDF text. If no DOI but PMC found, `source_url = pmc:PMC########`.
   - **PMID.** NXML `<article-id pub-id-type="pmid">` or `PMID: ########` in PDF text. If no DOI/PMC, `source_url = pmid:########`.
   - **Textbook.** When the paper file is a textbook compilation (CRC HCP, IUPAC tables, NIST WebBook printout, etc.), use `source_url = textbook:<short-id>` (e.g., `textbook:crc_hcp_97` for CRC Handbook of Chemistry and Physics 97th edition). The DOI substring check is skipped for textbook entries.
   - **Citation-only.** Older papers (pre-2000) sometimes have no DOI/PMC/PMID. In that case ensure `source` carries the full citation (journal + year + volume + page) and `source_url` uses whatever identifier IS available. A paper with no DOI but a complete citation is **not** an extraction failure.

   **If none of the above is in the paper file**, the paper has no DOI you can use — use the PMC / PMID / legacy fallback. **Never guess a DOI from training memory**.

   **`source_url` is the DOI of the paper file you are physically reading, NOT the DOI of any paper it cites.** This applies even when the value was originally measured by an earlier paper and the row's value comes from a compilation table inside the paper-at-hand. The upstream primary's DOI is irrelevant to `source_url`. If you want to credit the original measurement, mention it in `notes` (e.g., `notes = "upstream primary: Chu_Yalkowsky_2009"`). Compiled-literature values still belong to the compilation paper for citation purposes — the user can chase the upstream chain by following the compilation's bibliography. (This is the v2.1 affirmative form of the "DOI from this paper only" rule. Trial-7 surfaced cases where the rule was understood negatively — "don't take DOIs from bibliography" — but the affirmative form — "use THIS paper's DOI even for compiled values" — wasn't explicit.)

3. **Verify the identifier.** If you found a DOI, run `python3 scripts/crossref_lookup.py <DOI>`. Confirm the returned title is consistent with the paper file. If the title doesn't match, the DOI in the file is wrong — flag the paper, do not extract. If you found only a PMC/PMID/citation, skip the CrossRef step.

4. **Note the paper's reporting conventions.** Read the abstract / experimental section to identify: (a) is this paper *measuring* the values it reports or *calculating / compiling* them? (b) what units are used? The overlay's `OVERLAY.md` covers the candidate tokens specific to the data type.

5. **Identify candidate locations.** Per the overlay's `OVERLAY.md` (candidate-token list), skim the paper for relevant tables, figures, paragraph mentions. Note page / table / figure numbers per region.

If a paper file can't be read or its DOI can't be verified, **set its rows to `flagged_review` with reason and skip extraction**. Do not synthesize values from training memory.

### Phase 2 — Evidence-locked extraction

For every (compound × property × value) you extract, produce one row with:

1. **`evidence_location`** — precise pointer specific enough to find in <30 seconds.
2. **`evidence_quote`** — verbatim text containing the value. Character-for-character, allowing only minor whitespace differences.
3. **`conversion_arithmetic`** — if you converted units, show the math (in v2.0 standardized syntax — see above). Blank if `value_raw` is already in the property's standardized unit.

**Quote re-confirmation (before committing each row).** After you've drafted the row, BEFORE adding it to the output:

1. Re-open the paper file at `evidence_location`.
2. Try to produce a verbatim contiguous span that contains both the compound (or its serial code) and the value. Permitted normalizations: whitespace collapsing, NFC unicode, ASCII hyphen folding (`−`/`–`/`—` → `-`). The ideal quote is a string `grep -F` over the paper file would return.
3. **If you can't capture both in one contiguous span** (2-column PDF wrap, watermark, table cells separated by spacing) — record the closest contiguous span that supports the row, typically the local clause containing the value. Phase 3 lints flag quote-fidelity issues for maintainer review; they do NOT cause the row to be dropped.
4. **CRITICAL — confirm the recorded `value_raw` matches the paper's printed value for this compound.** If the quote points at a different measurement on a nearby line, fix the row — that's a Tier-1 correctness failure (wrong value bound to compound), not a quote-fidelity issue.
5. **CRITICAL — confirm `compound_name` is the compound the value actually belongs to.** Multi-row PDF tables can put a value on the row of a different compound than the agent assumed. Re-read the row label.
6. **Verify `conversion_arithmetic`** (if present) is mathematically correct and uses v2.0 standardized syntax.
7. **Suspect PDF line wrap when `value_raw` ends at a non-token boundary.** If the recorded `value_raw` ends in a trailing decimal point with no following digit (e.g., `"158-159."`), a dangling hyphen (e.g., `"36.98-"`), or a dangling letter (e.g., `"−77.9 °"`), the actual value is almost certainly continued on the next physical line of the `pdftotext` output. Re-read forward one line in the source. Trial-7 row 902 was a `mp 158–159.5 °C` where the `.5 °C` wrapped to the next line and was lost; recording `value_raw = "158-159"` truncated the value. Catching this is part of Step 6's value-confirmation check.

The bar for emitting a row is: compound is identifiable, value matches the paper, source citation is real. Quote fidelity is a separate verifiability property — Phase 3 lints flag it, but a non-ideal quote does not by itself cause the row to be dropped.

Also:

- `compound_name`: full name as printed. For prose names that span multiple PDF lines, reassemble them.
- `property`: pick the most specific applicable value from the overlay's enum. See `datatypes/<datatype>/OVERLAY.md` § Properties (including the property-disambiguation table for borderline cases).
- `meas_calc`: `measured` if any actual measurement (the cited paper's or compiled from another paper) underlies the value. `calculated` if the value is a model output (QSPR, DFT, MPBPVP, SPARC, ACD, MMP, etc.).
- `relation`: `=` by default; `>` for `">300"`; `<` for `"<5"`; `~` or `≈` for `"approximately X"` / `"ca. X"`.

**Drop these aggressively** — they are common failure modes. The data-type-specific drop patterns live in `datatypes/<datatype>/OVERLAY.md` § "drop patterns". Generic drop patterns:

- Compound names that are bare codes (`compound 3`, `complex 9a`) without an accompanying name.
- Compound names that are obviously truncated mid-token.
- Compound names that look like section-procedure titles, journal names, vendor labels, dataset descriptors, or non-chemistry prose.

When in doubt, **flag the row** with `verification_status = flagged_review` and explain in `notes` rather than guessing.

### Phase 3 — Programmatic sanity checks

After extraction, run:

```bash
python3 scripts/run_all_checks.py --datatype <name> <your-output.csv>
```

The `--datatype` flag is **required**; the umbrella halts if it's missing or names an overlay that doesn't exist. The umbrella runs:

| Check | Scope | What it catches |
|---|---|---|
| Required-field check | Generic | Any required column empty. |
| `csv_quote_lint.py` | Generic | Unquoted commas in compound names producing column shifts (RFC-4180). |
| `quote_support_lint.py` | Generic | `evidence_quote` doesn't contain the numeric value. **Tier 2 verifiability (advisory).** |
| `validate_compound_name.py` | Generic | SMILES invalid (RDKit); compound-name shape defects (bare codes, truncated locants, dangling hyphen/prime, unbalanced parens, terminal unfinished-suffix tokens, procedure-text contamination, EA-prefix contamination, leading paper-local code prefix, procedure-text at start). |
| `conversion_arithmetic_lint.py` | Generic | `conversion_arithmetic` field violates v2.0 standardized syntax. |
| `verify_doi.py` | Generic (needs `--paper-root`) | DOI in `source_url` doesn't appear in the paper file's text. |
| `verify_evidence_quote.py` | Generic (needs `--paper-root`) | `evidence_quote` not verbatim in the paper file. **Tier 2 verifiability.** |
| `dedup_within_paper.py` | Generic | Same (compound, property, value) emitted multiple times for one paper. |
| Placeholder citations | Generic | Source contains `Author et al.` / `(related ... cited in)`. |
| `datatypes/<datatype>/scripts/*.py` | Data-type-specific | Auto-discovered per overlay. For mp_bp: `value_range_check.py` (mp ∈ [−275, 4500] °C; bp ∈ [−275, 6500] °C), `unit_conversion_arithmetic.py` (K/°F → °C arithmetic). |

If any rows are flagged, **fix them before delivery**. Do not deliver flagged rows mixed with verified ones — they should sit in `flagged_review` status with notes.

### Phase 4 — Independent verification (MANDATORY before declaring success)

This phase is required, not optional. A run that has not been through Phase 4 has unmeasured audit quality — the deterministic Phase 3 checks alone don't catch semantic errors (compound mis-binding, wrong-cell extraction in tables, NMR shift mistaken for mp, etc.). Reports should not claim audit pass-rate numbers without Phase 4 evidence.

**A different agent** (fresh invocation, no context from the extraction) verifies each row in the sample. Use the prompt in `references/VERIFICATION_PROMPT_TEMPLATES.md`. The verifier:

1. Opens the paper file at the path indicated by the row's `source` / `source_url`.
2. Navigates to `evidence_location` and confirms `evidence_quote` is verbatim present.
3. Confirms `compound_name` and `value_raw` match what the quote says.
4. Confirms `conversion_arithmetic` (when present) is mathematically correct.
5. On full pass: upgrades `verification_status` to `verified_extraction`.
6. On any failure: sets `verification_status = flagged_review` and adds a granular sub-verdict in `notes`.

The verifier **must NOT silently correct values** — it reports the discrepancy and lets the maintainer decide.

#### Sample size

**`max(100 rows, 5 % of total rows)`**, drawn uniformly at random. The floor of 100 ensures a defensible pass-rate estimate (CI half-width ~5 percentage points near 90 % pass) on small runs. The 5 % minimum scales for large corpora.

For runs with fewer than 100 rows total, audit all rows.

#### Parallel dispatch (required at scale)

Verifier agents run **in parallel, 25 rows per agent, dispatched as one batch**. A 100-row audit = 4 fresh-context agents; a 500-row audit = 20 agents. Wall time is bounded by one agent's per-row time, not by total row count.

When the corpus has heterogeneous source types (DOI / PMC / legacy / OCR), **stratify** the sample proportionally across those buckets rather than sampling uniformly.

#### What to do when the sample finds failures

When the Phase 4 sample turns up a failure pattern that looks like a class:

1. **Run the relevant deterministic lint across the full CSV** to catch the same defect class everywhere.
2. **Fix or drop the matched rows.**
3. **Run one more 100-row Phase 4 sample** (different seed) to confirm the class is gone before declaring success.

Class-targeted sweeps catch ~100 % of a known defect; random re-sampling catches it only at the prevalence rate. Don't re-sample without sweeping first.

#### Programmatic-only verification

For programmatic-only verification (no agent needed), `scripts/verify_row.py --datatype <name> <csv> <row_id>` runs the deterministic checks but cannot verify that the row's compound name matches the paper semantically (which is what the agent step is for). Phase 4 must include at least one agent-based verification pass on a sample — programmatic checks alone are not Phase 4.

### Phase 5 — Confidence tagging

The `verification_status` enum is documented above. Use it consistently. Granular `flagged_*` reasons go in `notes` when status is `flagged_review`.

### Phase 6 — Failure handling

- **Paper file can't be read** (corrupt, encrypted) → mark `flagged_review` with `flagged_paper_unreadable`. Do NOT synthesize from memory.
- **Paper has no DOI** → this is NOT a failure. Use a `pmc:` / `pmid:` source_url if available, otherwise leave it as the paper's stable URL or filename. Ensure `source` carries the full citation. Rows continue normally.
- **DOI in the file doesn't match CrossRef metadata** → flag, don't extract.
- **Value stated only in a figure (no text)** → either OCR carefully and mark `notes = "figure OCR"`, or skip.
- **Citation chain unclear** → cite the paper at hand, set `meas_calc = measured`, mention in `notes` that the upstream primary couldn't be identified.
- **Value compiled in a review** → `meas_calc = measured` (it IS a measurement, just by someone other than the cited paper). The citation to the review is provenance enough.
- **Multiple values for the same compound in one paper** → one row per distinct value, distinguish via `meas_calc` and `evidence_location`.
- **Textbook source** → `source_url = textbook:<short-id>`; the DOI check skips textbook entries; verifier upgrades to `verified_textbook` when appropriate.

## Anti-patterns (forbidden)

### The four evidence-locked fields — general rule

The four fields `compound_name`, `value_raw`, `evidence_quote`, and `source_url` **must come from the LLM directly reading the paper** for the row that ends up in the deliverable. No script may produce, transform, hardcode, or template these fields. This is the methodology the skill is built around — every other rule below is a specific case of it.

Scripts ARE allowed for:

- Corpus enumeration (listing paper subdirectories, splitting into batches).
- Orchestration (dispatching parallel LLM agents, merging their CSVs).
- Enum normalization (e.g., `experimental` → `measured` in `meas_calc`).
- Field-format cleanup (RFC-4180 CSV quoting, ID assignment, dedup).
- Phase-3 deterministic checks (the bundled scripts).
- Phase-4 audit dispatch (sample selection, parallel verifier dispatch).
- One-off migrations between skill versions (e.g., `migrate_v17_to_v20.py`).

Scripts are NOT allowed for:

- Producing `compound_name`, `value_raw`, `evidence_quote`, or `source_url` values.
- Constructing `evidence_quote` strings via f-string templates from variables you read manually.
- Bulk-extracting rows from `pdftotext` output via regex.
- Any "data-entry helper" that hardcodes paper content into Python literals.

### Specific anti-patterns (generic)

- ❌ **"I'll write a Python regex extractor with `pdftotext` + `re.findall` to scan all papers in bulk."** — Cross-harness validation showed this approach reaches ~56% audit pass rate vs. ~93% for the LLM-driven approach.
- ❌ **"I'll write a Python data-entry script that hardcodes the compound names and values and constructs `evidence_quote` strings via f-strings."** — Even when you read the source tables manually, a script that emits `f"Table III: {nm} BP {bp} MP {mp}"` produces a paraphrased quote, not a verbatim one.
- ❌ "I'll compile from training memory since I can't read the file" — **STOP and flag.**
- ❌ "The value seems plausible for this compound" — plausibility is not provenance.
- ❌ "I'll guess at the DOI" — use what's in the paper file; if it's missing, flag.
- ❌ "I'll use 'Author et al.' as a placeholder citation" — placeholder citations propagate as errors.
- ❌ "I'll extract many rows in one batch without per-row provenance" — every row needs evidence_location + evidence_quote.
- ❌ "I'll add author names to the source field" — DOI is the canonical identifier.
- ❌ "I'll truncate the compound name to save space" — never truncate.
- ❌ **"The prior trial run did X, so I'll do X too."** — Past trial outputs are *observations* about what some other agent did. They can inform what to look out for, but they do NOT define protocol. Only this SKILL.md and your assigned corpus define your task. If a past run skipped part of the corpus, that's a fact about that run, not a directive for yours.
- ❌ **"I'll just pick a data type that looks plausible from the corpus and start extracting."** — The user must specify the data type explicitly. If they haven't, halt and ask.

Data-type-specific anti-patterns live in `datatypes/<datatype>/OVERLAY.md` § "anti-patterns" (e.g., for mp_bp: NMR shifts as mp values, PDF sign-loss, TLC eluents extracted as compounds, EA-prefix contamination).

## Bundled scripts

All in `scripts/` (generic) and `datatypes/<datatype>/scripts/` (overlay). Run with `python3 scripts/<name>.py --help` for arguments.

| Script | Purpose |
|---|---|
| `scripts/crossref_lookup.py` | DOI → authoritative title / journal / year. Verifies a DOI extracted from a paper file resolves. |
| `scripts/validate_compound_name.py` | RDKit-based SMILES validation + compound-name shape lint (bare codes, truncated locants, dangling hyphen/prime, unbalanced parens, terminal unfinished-suffix tokens, procedure-text contamination, EA-prefix contamination, leading paper-local code prefix, procedure-text at start). |
| `scripts/conversion_arithmetic_lint.py` | Verify the v2.0 standardized `conversion_arithmetic` syntax shape (new in v2.0). |
| `scripts/verify_doi.py` | Confirm the DOI in `source_url` actually appears in the paper file's text. |
| `scripts/verify_evidence_quote.py` | Confirm `evidence_quote` is verbatim present in the paper file. Advisory (Tier 2 verifiability). |
| `scripts/quote_support_lint.py` | Confirm `evidence_quote` contains the numeric `value_raw` token. Advisory (Tier 2); does NOT auto-drop rows. |
| `scripts/csv_quote_lint.py` | Verify RFC-4180 CSV quoting; detect column shifts from unquoted commas. |
| `scripts/dedup_within_paper.py` | Flag duplicate rows within one paper. |
| `scripts/verify_row.py` | Run all programmatic checks (generic + overlay) for a single row. |
| `scripts/run_all_checks.py` | Umbrella runner; auto-discovers `datatypes/<datatype>/scripts/*.py`. |
| `datatypes/mp_bp/scripts/value_range_check.py` | Flag mp/bp values outside plausible ranges (mp: [−275, 4500] °C, bp: [−275, 6500] °C). |
| `datatypes/mp_bp/scripts/unit_conversion_arithmetic.py` | Verify K → °C and °F → °C math (mp/bp-specific). |

## When to apply this skill

Apply this skill any time you are:

- Building a new property database (mp/bp, redox, viscosity, etc.) from a set of provided papers.
- Extending an existing database with new papers.
- Auditing an existing extraction for errors.
- Compiling data for downstream design / synthesis decisions.

For one-off conversational questions about a single compound's property ("What's the boiling point of methanol?"), this protocol is overkill. Apply when the data will be used as a basis for downstream decisions.

## Reference files

- `references/COMMON_ERRORS.md` — property-agnostic failure-mode catalog (NMR-as-value, PDF sign-loss, compound-name truncation, multi-row thead misalignment, workup solvents, bare codes, wrong-paper DOI, memory fabrication, adjacent-measurement quote, doubled-token, quote-stops-before-value, regex extractor, templated quotes, memory-guessed DOIs). Property-specific instances and overlays' unique failure modes are in each overlay's own failure-modes section.
- `references/EXTRACTION_PROMPT_TEMPLATES.md` — copy-paste agent prompts; per-step specifics live in each overlay's `OVERLAY.md`.
- `references/VERIFICATION_PROMPT_TEMPLATES.md` — independent-verification agent prompt with Q1–Q5 framework; Q1(b) and Q2 customize per overlay.
- `datatypes/<datatype>/OVERLAY.md` — **single file per data type**, containing property enum, schema (extension columns, units), worked examples, value ranges, unit conversions, property-specific drop patterns, property-specific skip reasons, and property-specific failure-mode catalog. In v2.1 this was consolidated from three files (`OVERLAY.md`, `SCHEMA.md`, `COMMON_ERRORS.md`) into one to reduce cross-reference burden on the agent.

## Evals

Test cases in `evals/evals.json` and fixture CSVs split between `evals/files/` (generic) and `datatypes/<datatype>/evals/files/` (overlay). Each eval entry carries a `datatype` key (`generic`, `mp_bp`, etc.). Coverage:

- **scripts-clean-baseline** (per overlay): rows that pass all checks.
- **scripts-detect-seeded-errors** (per overlay): rows with deliberate errors of each type.
- **range-check-edge-cases** (mp/bp): helium / tungsten / decomposition values at the extremes.
- **unit-conversion-arithmetic** (mp/bp): K → °C and °F → °C correctness.
- **evidence-quote-verification** (generic): verbatim-present detection.
- **doi-verification** (generic): DOI substring check.
- **conversion-arithmetic-syntax** (generic, new in v2.0): standardized syntax shape.
- **INACCESSIBLE-handling** (generic, agent): agent given an unreadable paper file must flag rather than fabricate.

## How to add a new data type

To add a new property family (e.g., `viscosity`):

1. Copy `datatypes/mp_bp/` to `datatypes/viscosity/`.
2. Rewrite `OVERLAY.md`, `SCHEMA.md`, `COMMON_ERRORS.md` for the new property.
3. Rewrite or replace the overlay scripts (`value_range_check.py`, `unit_conversion_arithmetic.py` if applicable).
4. Add overlay-specific evals to `evals/evals.json` (with `datatype: "viscosity"`) and put fixtures under `datatypes/viscosity/evals/files/`.
5. Document any new optional extension columns in `SCHEMA.md`.
6. Run the eval suite with `--datatype viscosity` to confirm.

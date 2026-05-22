---
name: mp-bp-extraction
description: LLM-driven evidence-locked extraction of melting-point and boiling-point data (plus DSC onset, decomposition, sublimation) from supplied journal articles. The agent reads each paper directly (Read / bash / pdftotext) and writes rows with a mandatory evidence_quote. Phase 0 requires enumerating the corpus to `_corpus_manifest.txt` first (descending into subfolders) and logging intentional exclusions to `_skipped.txt`; silent omission is forbidden. The four fields compound_name, value_raw, evidence_quote, source_url come from LLM reading, not scripts — no regex extractors and no data-entry helpers. The bar for emitting a row is compound + value + source correct; quote fidelity is a separate verifiability metric (advisory). DOIs must come from the paper file, never from memory. Past trial outputs are reference, not protocol. Phase 4 independent verification is mandatory (max(100, 5%) parallel sample). Apply when compiling, auditing, or extending an mp/bp database from supplied papers.
version: v1.7
---

# mp/bp extraction protocol

## How this skill is applied — MANDATORY READING

**This skill is applied by an LLM agent reading each paper directly. It is NOT applied by writing a Python extraction script.**

You — the agent invoking this skill — will:

1. **Enumerate the corpus first (Phase 0).** Before processing any paper, write `_corpus_manifest.txt` listing every paper-bearing location, descending into subfolders. Any location you intentionally skip goes in `_skipped.txt` with a reason. Do NOT silently omit corpus parts.
2. **Iterate the corpus one paper at a time.** Use the Read tool / bash / `pdftotext` to open each paper's `article.nxml`, `article_text.txt`, or `article.pdf` and read the actual text.
3. **For each paper, write extracted rows yourself.** Apply the EXTRACTION_PROMPT_TEMPLATES.md Template 1 protocol per paper. Each row must include a verbatim `evidence_quote` drawn from text you actually read.
4. **Run the bundled scripts AFTER extraction as deterministic checks** — they validate SMILES, value ranges, unit arithmetic, CSV formatting, evidence-quote presence, etc. They are NOT the extraction engine.
5. **Run mandatory Phase 4 independent verification** before declaring the output ready. Dispatching fresh Claude agents (or equivalent) to re-audit a random sample against the source papers is required, not optional.

You will NOT:

- **Write a Python regex extractor** (e.g., `extract_mp_bp.py` that calls `re.findall` over paper text and emits rows in bulk). Past attempts at regex-based extraction on this exact problem plateaued at 56-67% audit pass rate even after extensive iteration. The LLM-driven approach reaches 93-100% on the same corpus.
- **Run extraction as a single batch script.** Parallelization is fine — you can dispatch multiple LLM agent invocations to handle different paper batches concurrently — but each agent must read its papers directly, not write a regex pipeline.
- **Skip Phase 4 verification and ship rows as `pending_verification`.** Without Phase 4 evidence the audit pass rate is unmeasured; reports must not claim quality numbers.

### Pre-flight checklist

Before starting, confirm:

- [ ] I am an LLM agent applying this protocol by reading papers directly.
- [ ] I will NOT write a Python regex extractor. The scripts in `scripts/` are post-extraction checks only.
- [ ] **Before Phase 1**, I will enumerate every paper-bearing location in the corpus (descending into subfolders) and write the enumeration to `_corpus_manifest.txt`. Anything I intentionally skip will be logged in `_skipped.txt` with a one-line reason. I will NOT silently skip parts of the corpus. See Phase 0 below.
- [ ] I will process each paper via Read / bash / `pdftotext` and produce rows with mandatory verbatim `evidence_quote`.
- [ ] I will run Phase 4 independent verification (fresh-context agent re-audit of a random sample) before declaring success.
- [ ] I will treat any past trial's outputs as historical reference, NOT as protocol. Operational choices made in previous runs do not bind this one.

## Goal

Produce a CSV of melting-point and boiling-point measurements where **independent spot checks find zero data-extraction errors**. The literature may disagree across sources for the same compound — that's normal and acceptable. What is not acceptable is misattributing a value to a paper, mis-stating a unit, fabricating a citation, or producing values from training memory.

## Why the discipline matters

A property database without provenance is worse than no database — downstream users will trust it for design and synthesis decisions, and each fabricated row poisons the dataset. Past attempts on this exact problem produced 30–60 % extraction-error rates when independently spot-checked. Errors that look plausible (right compound, right ballpark value, wrong specific number or wrong source) are the most damaging.

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

The deliverable is a **single CSV**. One row per (compound × property × value). Required columns:

| Column | Required | Notes |
|---|---|---|
| `id` | yes | Sequential integer row identifier. |
| `verification_status` | yes | See "verification status values" below. New rows start `pending_verification`. |
| `compound_name` | yes | Full IUPAC, common name, or recognizable trivial name. **Never truncated** (e.g., "5-acetyl-2-ethyl-..."-quinolone, not "5-acetyl"). For ionic-liquid / coordination-salt shorthand of the form `[cation][anion]`, the shorthand itself is acceptable (e.g., `[EMIm][NO3]`). |
| `compound_smiles` | optional | SMILES when the source provides one; left blank otherwise. |
| `property` | yes | One of: `melting_point`, `boiling_point`, `DSC_onset`, `DSC_peak`, `decomposition`, `sublimation`. |
| `value_celsius` | yes | Numeric value in °C, after any unit conversion. For ranges, this is the midpoint. |
| `value_celsius_min` | when value is a range | Low end of range, °C |
| `value_celsius_max` | when value is a range | High end of range, °C |
| `value_raw` | yes | As printed in the source, including original units (e.g., "188–190 °C", "1655 K", "−77.9 °C", "200 °F"). |
| `relation` | yes | One of `=`, `>`, `<`, `~`, `≈`. Use `=` for an exact value; `>` for ">300 °C", etc. |
| `data_type` | yes | `measured` (any experimental measurement, including ones compiled from other literature) or `calculated` (predicted by a model, e.g., QSPR / MPBPVP / DFT). |
| `source` | yes | Citation: journal, year, vol, page (or paper title). **NO author names** — the DOI in source_url is the canonical identifier when present. **When no DOI exists**, the `source` field MUST include journal + year + volume + page so the paper is still identifiable. |
| `source_url` | yes | One of, in priority order: (a) a DOI URL `https://doi.org/10.xxx/xxxxx`; (b) a PMC ID `pmc:PMCxxxxxxx` when the paper has a PMC ID but no DOI in the file; (c) a PubMed ID `pmid:xxxxxxxx`; (d) `textbook:<short-id>` for textbook references. Always non-empty; if no DOI/PMC/PMID can be found, use the paper file's path. |
| `evidence_location` | yes | Precise pointer (e.g., "Table 1 row 3", "p. 6469 col 2 ¶ 3", "SI Table S4 row 12", "section 3.2.5 ¶ 1"). |
| `evidence_quote` | yes | Verbatim text from the source containing the value (and ideally the compound name or its serial code). **MANDATORY** — every row must carry one. Prefer a contiguous substring; allow only minor whitespace differences vs. the source. When PDF layout / watermarks / table-cell separation prevent capturing compound and value in one contiguous span, record the closest local span and let Phase 3 lints flag the quote-fidelity issue as advisory. Quote fidelity is a verifiability concern (Tier 2), not a correctness gate. |
| `conversion_arithmetic` | when conversion applied | Math shown explicitly, e.g., "200 K − 273.15 = −73.15 °C" or "200 °F − 32) × 5/9 = 93.33 °C". Blank when the source already reports °C. |
| `notes` | optional | Free text; flag-reason details, family / class, audit history, etc. |

### Verification status values

Set by the **extractor**:
- `pending_verification` — newly extracted, not yet through Phase 4

Upgraded by the **verifier** (Phase 4):
- `verified_extraction` — extracted by an agent that read the provided file, independently verified
- `verified_textbook` — standard reference (CRC, IUPAC tables); no Phase 4 needed
- `verified_by_audit` — pre-existing row that passed an explicit audit
- `audit_corrected` — issue found and explicitly corrected (with audit trail in notes)

Set by audits or sanity checks:
- `flagged_review` — issue found; details in notes. Granular reasons go in `notes`:
  `flagged_doi_unresolvable`, `flagged_doi_unrelated_paper`,
  `flagged_evidence_quote_not_found`, `flagged_value_mismatch`,
  `flagged_compound_mismatch`, `flagged_unit_conversion_error`,
  `flagged_value_out_of_range`, `flagged_metadata_mismatch`,
  `flagged_compound_name_truncated`, `flagged_compound_name_bare_code`.
- `unverified` — residual that didn't fit other categories.

**Why no author field:** The DOI in source_url uniquely identifies the paper. Author names add error surface — past extractions got first-authors wrong frequently. Use CrossRef when you need to display authors.

**Why a single file:** Tier filtering happens via `verification_status`. Don't split into separate files by tier or by data_type.

## Worked example

A single fully-populated row:

```csv
id,verification_status,compound_name,compound_smiles,property,value_celsius,value_celsius_min,value_celsius_max,value_raw,relation,data_type,source,source_url,evidence_location,evidence_quote,conversion_arithmetic,notes
1,pending_verification,3-phenylquinazoline-4(3H)-thione,,melting_point,189.0,188.0,190.0,"188–190 °C",=,measured,"Molecules 2018, 23, 1212",https://doi.org/10.3390/molecules23051212,"Table 1 row 2a","2a Yield 67% 188–190 °C",,
```

Note: `conversion_arithmetic` is empty because the source already reports °C.

A range with K → °C conversion:

```csv
2,pending_verification,Camostat,,melting_point,219.85,,,492.478 K,=,measured,"Thermodynamic properties of APIs ...",https://doi.org/10.xxxx/xxxxx,"Table 5 col 'Camostat | exp.' row 'Tm'","Camostat Tm = 492.478 K","492.478 K − 273.15 = 219.328 °C",
```

A calculated value:

```csv
3,pending_verification,Anthracene,,melting_point,210.0,,,210.0 °C,=,calculated,"AI-powered prediction of critical properties ...",https://doi.org/10.xxxx/xxxxx,"Table 4 row 'Anthracene' col 'mp_calc'","Anthracene 210.0 °C (predicted by MPBP)",,QSPR_SOFTWARE
```

## The phases

### Phase 0 — Corpus manifest (required, before anything else)

Before processing any paper, enumerate every paper-bearing location in the corpus. The goal is to make the set of papers you will process explicit and accounted for. Silent omission of corpus parts has been the dominant recall problem in past trials.

**Required outputs:**

- `_corpus_manifest.txt` — one entry per paper-bearing location in the corpus. **Descend into subfolders.** A paper-bearing location is anything that contains an article body: an indexed subdirectory containing `article.nxml` / `article.pdf` / `article_text.txt`, a standalone `.pdf` file at the corpus root or inside a category subfolder, an `article.html` companion to a PDF, or any other layout the corpus actually uses. Use whatever enumeration mechanism is appropriate for the corpus layout you've been given (`ls`, `find`, `glob`, etc.). The skill does not prescribe a specific command because corpora vary in structure.
- `_skipped.txt` — one line per paper-bearing location you intentionally exclude from extraction, formatted as `<location>\t<reason>`. Allowed reasons (use the most specific):
  - `review_no_per_compound_binding` — review / ML / QSPR paper with no per-compound mp/bp table.
  - `bare_code_compounds_only` — compounds referenced only by codes like `compound 4a-l`, no IUPAC names.
  - `no_mp_bp_data_in_text` — paper has no melting/boiling-point data at all.
  - `tga_or_nmr_only_no_mp_bp` — characterization without mp/bp (TGA, NMR, IR alone).
  - `binding_ambiguous` — values present but not cleanly bindable to compounds in the linearized text.
  - `image_only_compound_table` — compound table is structure images without textual names.
  - `formulation_only_no_discrete_compound` — values are for mixtures / formulations, not pure compounds.
  - `paper_unreadable` — file is corrupt, encrypted, or empty after `pdftotext`.

Anything not in this list goes in `_skipped.txt` with a free-text reason; ask the user before doing so.

**Phase 1 is gated on the manifest being non-empty.** If your manifest has zero entries, stop — the corpus path is wrong or the enumeration is broken.

**The EXTRACTION_SUMMARY.md you produce at the end must account for every manifest entry as either processed or skipped-with-reason.** The accounting is `processed + skipped == manifest`, no silent loss.

**Do not skip a paper-bearing location because a prior trial run skipped it.** Past trials are reference, not protocol. See the anti-pattern about this in the anti-patterns section.

### Phase 1 — Source preparation (per-paper, after Phase 0)

For each paper subdirectory in the user's input:

1. **Read the files.** Open the NXML if present; otherwise extract text from the PDF (`pdftotext -layout`). Read `metadata.json` if present.
2. **Identify the paper's canonical identifier.** Extract from the paper file ONLY — never from training memory, never from the paper's reference list. The DOI in `<reference>` / bibliography entries belongs to a *cited* paper, not to this paper. Use only these locations, in priority order:
   - **DOI.** NXML `<article-id pub-id-type="doi">`, the PDF front matter (first 1–2 pages), or `metadata.json`. The DOI must appear as a substring of the paper file's text. If found, this is the `source_url` (as `https://doi.org/<DOI>`).
   - **PMC ID.** NXML `<article-id pub-id-type="pmc">` or "PMC########" in PDF text. If no DOI but PMC found, `source_url = pmc:PMC########`.
   - **PMID.** NXML `<article-id pub-id-type="pmid">` or "PMID: ########" in PDF text. If no DOI/PMC, `source_url = pmid:########`.
   - **Citation-only.** Older papers (pre-2000) sometimes have no DOI/PMC/PMID. In that case ensure `source` carries the full citation (journal + year + volume + page) and `source_url` uses whatever identifier IS available. A paper with no DOI but a complete citation is **not** an extraction failure.

   **If none of the above is in the paper file**, the paper has no DOI you can use — use the PMC / PMID / legacy fallback. **Never guess a DOI from training memory** based on the journal/year/title. Trial-2 found 4 rows that cited DOIs which appeared nowhere in the source files — likely memory-guesses. The `verify_doi.py` script substring-checks the DOI against the paper file and will catch this, but the rule has to apply during extraction.
3. **Verify the identifier.** If you found a DOI, run `python3 scripts/crossref_lookup.py <DOI>`. Confirm the returned title is consistent with the paper file. If the title doesn't match, the DOI in the file is wrong — flag the paper, do not extract. If you found only a PMC/PMID/citation, skip the CrossRef step — citations are self-verifying through their journal+year+vol+page.
4. **Note the paper's reporting conventions.** Read the abstract / experimental section to identify: (a) is this paper *measuring* the values it reports (synthesis paper, characterization study, thermodynamic measurement) or *calculating / compiling* them (review, QSPR, prediction model)? (b) what unit conventions are used (°C, K, °F)?
5. **Identify candidate locations.** Skim the paper for tables, figures, paragraph mentions of mp / bp / m.p. / Tm / Tfus / boiling point / Tb. Note page / table / figure numbers per region.

If a paper file can't be read or its DOI can't be verified, **set its rows to `flagged_review` with reason and skip extraction**. Do not synthesize values from training memory.

### Phase 2 — Evidence-locked extraction

For every (compound × property × value) you extract, produce one row with:

1. **`evidence_location`** — precise pointer specific enough to find in <30 seconds (e.g., "Table 1 row 3", "p. 6469 col 2 ¶ 3").
2. **`evidence_quote`** — verbatim text containing the value. Character-for-character, allowing only minor whitespace differences.
3. **`conversion_arithmetic`** — if you converted units, show the math. Blank if `value_raw` is already in °C.

**Quote re-confirmation (before committing each row).** After you've drafted the row, BEFORE adding it to the output:

1. Re-open the paper file at `evidence_location`.
2. Try to produce a verbatim contiguous span that contains both the compound (or its serial code) and the value. Permitted normalizations: whitespace collapsing (multi-space → single space), NFC unicode, ASCII hyphen folding (−/–/— → -). The ideal quote is a string `grep -F` over the paper file would return.
3. **If you can't capture both in one contiguous span** (2-column PDF wrap puts the value on a separate physical line, a watermark splits a sentence, table cells are separated by spacing, the paper uses its own ellipsis or shorthand) — record the closest contiguous span that supports the row, typically the local clause containing the value. Phase 3 lints flag quote-fidelity issues for maintainer review; they do NOT cause the row to be dropped.
4. **CRITICAL — confirm the recorded `value_raw` matches the paper's printed value for this compound.** If the quote says "f.p. -161.5" but `value_raw` says "36.98 °C" because you read a boiling-point value but quoted the freezing-point line, fix the row — that's a Tier-1 correctness failure (wrong value bound to compound), not a quote-fidelity issue.
5. **CRITICAL — confirm `compound_name` is the compound the value actually belongs to.** Multi-row PDF tables can put a value on the row of a different compound than the agent assumed. Re-read the row label.
6. **Verify `conversion_arithmetic`** (if present) is mathematically correct.

The bar for emitting a row is: compound is identifiable, value matches the paper, source citation is real. Quote fidelity is a separate verifiability property — Phase 3 lints flag it, but a non-ideal quote does not by itself cause the row to be dropped.

The Tier-1 correctness failure this step exists to prevent is **wrong-compound-bound-to-value** (the agent records compound 23 with compound 25's m.p. because they sat on adjacent table rows). Quote-fidelity issues (PDF column wraps, watermarks, OCR-mangled text, paper's own ellipsis usage) are NOT failures and should not cause the row to be dropped; the lint will flag them as advisory.

Also:
- `compound_name`: full name as printed in the source. For prose-style names that span multiple PDF lines, reassemble them. For multi-line table cells, capture the complete name.
- `property`: pick the most specific applicable subtype (e.g., `DSC_onset` if the source explicitly says "DSC onset"; otherwise `melting_point` for "mp" / "m.p." / "Tm" / "Tfus").
- `data_type`: `measured` if any actual measurement (the cited paper's or compiled from another paper) underlies the value. `calculated` if the value is a model output (QSPR, DFT, MPBPVP, SPARC, ACD, MMP, etc.). The clue is usually in the surrounding column header or paragraph context — e.g., "Calc. Tm", "predicted by SIRM", "Eq. 16".
- `relation`: `=` by default; `>` for ">300 °C"; `<` for "<5 °C"; `~` or `≈` for "approximately X" / "ca. X".

**Drop these aggressively** — they are common failure modes:
- Compound names that are bare codes ("compound 3", "complex 9a") without an accompanying name.
- Compound names that are obviously truncated mid-token.
- Compound names that look like section-procedure titles ("Synthesis of compounds 4–7"), journal names, vendor labels, dataset descriptors, or non-chemistry prose.
- Compound names that are common workup solvents (CH2Cl2, EtOAc, MeOH, DMF, DMSO, THF) when they appear as Rf-eluent annotations rather than as the characterized product.
- Numeric values that come from NMR / mass-spec context (`δ X.X ppm`, `m/z`, `[M+H]+`) rather than mp/bp tables.

When in doubt, **flag the row** with `verification_status = flagged_review` and explain in `notes` rather than guessing.

### Phase 3 — Programmatic sanity checks

After extraction, run:

```bash
python3 scripts/run_all_checks.py <your-output.csv>
```

The umbrella runs:

| Check | What it catches |
|---|---|
| `validate_compound_name.py` | SMILES invalid (RDKit); compound-name shape defects: bare codes, truncated-locant `H-Indeno...` prefix, dangling hyphen/prime, unbalanced parens, terminal unfinished-suffix tokens (`Carboxamid`, `Carbo`), procedure-text contamination, EA-prefix contamination, leading paper-local code prefix, procedure-text at start. **Tier-1 correctness.** |
| `value_range_check.py` | mp outside [−275, 4500] °C; bp outside [−275, 6500] °C. **Tier-1 correctness.** |
| `unit_conversion_arithmetic.py` | Arithmetic errors in K/°F → °C conversion; missing conversion when units don't match. **Tier-1 correctness.** |
| `verify_doi.py` | DOI in `source_url` doesn't appear in the paper file's text (catches memory-guessed or bibliography-sourced DOIs). **Tier-1 correctness.** |
| `csv_quote_lint.py` | Unquoted commas in compound names producing column shifts (RFC-4180). **Tier-3 hygiene.** |
| `dedup_within_paper.py` | Same (compound, property, value) emitted multiple times for one paper. **Tier-3 hygiene.** |
| Required-field check | Any of `compound_name`, `value_celsius`, `source_url`, `evidence_location`, `evidence_quote` empty. **Tier-3 hygiene.** |
| Placeholder citations | Source contains "Author et al." / "(related ... cited in)". **Tier-1 correctness.** |
| `verify_evidence_quote.py` | `evidence_quote` not verbatim in the paper file. **Tier-2 verifiability (advisory).** |
| `quote_support_lint.py` | `evidence_quote` doesn't contain the numeric value. **Tier-2 verifiability (advisory).** |

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

**`max(100 rows, 5 % of total rows)`**, drawn uniformly at random. The floor of 100 ensures a defensible pass-rate estimate (CI half-width ~5 percentage points near 90 % pass) on small runs. The 5 % minimum scales for large corpora — per-row audit cost is comparable to per-row extraction cost, so a 5 % sample adds ~5 % to total agent-time. Affordable at any corpus size.

For runs with fewer than 100 rows total, audit all rows.

#### Parallel dispatch (required at scale)

Verifier agents run **in parallel, 25 rows per agent, dispatched as one batch**. A 100-row audit = 4 fresh-context agents; a 500-row audit = 20 agents. Wall time is bounded by one agent's per-row time (typically 5–10 min for 25 rows), not by total row count. Sequential single-agent audit is unnecessarily slow at scale.

When the corpus has heterogeneous source types (DOI / PMC / legacy / OCR), **stratify** the sample proportionally across those buckets rather than sampling uniformly. A uniform random sample can under-represent a rare-but-failure-prone bucket.

#### What to do when the sample finds failures

When the Phase 4 sample turns up a failure pattern that looks like a class (e.g., 3 of 100 rows have constructed `evidence_quote` strings matching `f"Table N: ..."`):

1. **Run the relevant deterministic lint across the full CSV** to catch the same defect class everywhere. `quote_template_lint.py` for templated quotes, `quote_support_lint.py` for missing-value quotes, `validate_compound_name.py` for shape defects, `verify_doi.py` for DOI mismatches.
2. **Fix or drop the matched rows.**
3. **Run one more 100-row Phase 4 sample** (different seed) to confirm the class is gone before declaring success.

Class-targeted sweeps catch ~100 % of a known defect; random re-sampling catches it only at the prevalence rate. Don't re-sample without sweeping first.

#### Programmatic-only verification

For programmatic-only verification (no agent needed), `scripts/verify_row.py <csv> <row_id>` runs the deterministic checks but cannot verify that the row's compound name matches the paper semantically (which is what the agent step is for). Phase 4 must include at least one agent-based verification pass on a sample — programmatic checks alone are not Phase 4.

### Phase 5 — Confidence tagging

The `verification_status` enum is documented above. Use it consistently. Granular `flagged_*` reasons go in `notes` when status is `flagged_review`.

### Phase 6 — Failure handling

- **Paper file can't be read** (corrupt, encrypted) → mark `flagged_review` with `flagged_paper_unreadable`. Do NOT synthesize from memory.
- **Paper has no DOI** (older / pre-DOI-era papers, some non-PMC sources) → this is NOT a failure. Use a `pmc:` / `pmid:` source_url if available, otherwise leave it as the paper's stable URL or filename. Ensure `source` carries the full journal+year+volume+page citation. Rows continue normally.
- **DOI in the file doesn't match CrossRef metadata** → flag, don't extract. The file may be the wrong paper.
- **Value stated only in a figure (no text)** → either OCR carefully and mark `notes = "figure OCR"`, or skip.
- **Citation chain unclear** (paper compiled this value from another paper but doesn't say which) → cite the paper at hand, set `data_type = measured`, mention in `notes` that the upstream primary couldn't be identified.
- **Value compiled in a review** → `data_type = measured` (it IS a measurement, just by someone other than the cited paper). The citation to the review is provenance enough; the review is the user's path to the primary source.
- **Multiple values for the same compound in one paper** (e.g., raw + literature comparison columns) → one row per distinct value, distinguish via `data_type` and `evidence_location`.
- **Textbook source** → `source_url = textbook:<short-id>`; the DOI check skips textbook entries.

## Anti-patterns (forbidden)

### The four evidence-locked fields — general rule

The four fields `compound_name`, `value_raw`, `evidence_quote`, and `source_url` **must come from the LLM directly reading the paper** for the row that ends up in the deliverable. No script may produce, transform, hardcode, or template these fields. This is the methodology the skill is built around — every other rule below is a specific case of it.

Scripts ARE allowed for:
- Corpus enumeration (listing paper subdirectories, splitting into batches)
- Orchestration (dispatching parallel LLM agents, merging their CSVs)
- Enum normalization (e.g., `experimental` → `measured` in `data_type`)
- Field-format cleanup (RFC-4180 CSV quoting, ID assignment, dedup)
- Phase-3 deterministic checks (validate_compound_name.py, value_range_check.py, etc.)
- Phase-4 audit dispatch (sample selection, parallel verifier dispatch)

Scripts are NOT allowed for:
- Producing `compound_name`, `value_raw`, `evidence_quote`, or `source_url` values
- Constructing `evidence_quote` strings via f-string templates from variables you read manually
- Bulk-extracting rows from `pdftotext` output via regex
- Any "data-entry helper" that hardcodes paper content into Python literals

### Specific anti-patterns

- ❌ **"I'll write a Python regex extractor with `pdftotext` + `re.findall` to scan all papers in bulk."** — Cross-harness validation showed this approach reaches ~56% audit pass rate vs. ~93% for the LLM-driven approach. Regex matches text adjacent to mp/bp patterns that an LLM would semantically reject (`5 °C` from "5-substituted aryloxytetrazoles"; `307 °C` from "307 hydrocarbons"; sentence fragments captured as compound names; NMR chemical shifts as mp values).
- ❌ **"I'll write a Python data-entry script that hardcodes the compound names and values and constructs `evidence_quote` strings via f-strings."** — Even when you read the source tables manually, a script that emits `f"Table III: {nm} BP {bp} MP {mp}"` produces a paraphrased quote, not a verbatim one. The string never appeared in the paper. Trial-2 measured this failure mode at ~45% audit pass on 770 rows of large reference-table PDFs. The quote must be a string a `grep -F` over the paper file would return. If a table has 100 compounds and direct LLM reading feels slow, dispatch more parallel LLM workers — do not template the quotes.
- ❌ "I'll compile from training memory since I can't read the file" — **STOP and flag.**
- ❌ "The value seems plausible for this compound" — plausibility is not provenance.
- ❌ "I'll guess at the DOI" — use what's in the paper file; if it's missing, flag.
- ❌ "I'll use 'Author et al.' as a placeholder citation" — placeholder citations propagate as errors.
- ❌ "The compilation says values are in °C" — verify the actual unit in the original measurement; compilations frequently get this wrong.
- ❌ "I'll extract many rows in one batch without per-row provenance" — every row needs evidence_location + evidence_quote.
- ❌ "I'll add author names to the source field" — DOI is the canonical identifier.
- ❌ "I'll truncate the compound name to save space" — never truncate.
- ❌ "I'll extract this NMR shift, it looks like an mp value" — read the surrounding context (NMR / MS values can land in mp/bp range numerically but aren't mp/bp).
- ❌ **"The prior trial run did X, so I'll do X too."** — Past trial outputs (e.g., a `Trial<N>-*/EXTRACTION_SUMMARY.md`, a sibling agent's run notes, an example run from documentation) are *observations* about what some other agent did on some other day. They can inform what to look out for, but they do NOT define protocol. Only this SKILL.md and your assigned corpus define your task. If a past run skipped part of the corpus, that's a fact about that run, not a directive for yours. If a past run made a particular methodological choice, that's a data point, not authority. When in doubt, ask the user; do not adopt prior-run choices as if they were rules. (Trial-4 observed an agent silently excluding ~50 papers by lifting an exclusion regex from a previous trial's summary — a 17 % recall loss caused by treating reference material as protocol.)

## How this protocol catches errors observed in the wild

| Failure (real example) | What stops it |
|---|---|
| Memory-based fabrication of values for a paper that couldn't be read | Phase 1 requires file-read confirmation; Phase 2 mandates evidence_quote drawn from the read content. |
| NMR ppm 130.31 extracted as a melting point | Phase 4 verifier reads the surrounding context and rejects (Q5 property_subtype mismatch). |
| Long IUPAC compound name fragmented at a PDF line break ("Cyano-6-Oxo-...-2-yl") | Phase 4 verifier compares the row's compound_name against the paper's actual full name. Phase 3 truncated-name pattern catches some cases. |
| Multi-row table thead misalignment → wrong compound bound to a value | Phase 4 verifier re-reads the table and confirms the (row, col) cell matches. |
| QSPR paper's "Exp." column misclassified as `calculated` | Phase 4 verifier checks `data_type` against the surrounding column header / paper context. |
| PDF sign-loss: "−77.9 °C" rendered as "277.9 °C" | Phase 3 `value_range_check.py` flags 277.9 °C as out-of-range for typical organic mp. Phase 4 verifier confirms the printed value. |
| DOI in row doesn't match paper file's actual DOI | Phase 3 `verify_doi.py` substring-checks the DOI in the file. |
| Wrong-paper citation (DOI resolves to a different paper) | Phase 1 step 3 + Phase 3 `verify_doi.py`. |
| TLC eluent "CH2Cl2" extracted as compound | Phase 4 verifier reads context and rejects (Q3 identity tokens — the value belongs to the product, not the eluent). |
| Bare code "compound 5" as compound_name | Phase 3 required-field + truncated-name check; Phase 4 verifier flags. |

## Bundled scripts

All in `scripts/`. Run with `python3 scripts/<name>.py --help` for arguments.

| Script | Purpose |
|---|---|
| `crossref_lookup.py` | DOI → authoritative title / journal / year. Verifies the DOI extracted from a paper file is real. |
| `validate_compound_name.py` | RDKit-based SMILES validation + compound-name shape lint (bare codes, truncated-locant prefix, dangling hyphen/prime, unbalanced parens, terminal unfinished-suffix tokens, procedure-text contamination, **v1.6:** EA-prefix contamination, leading paper-local code prefix, procedure-text at start). |
| `value_range_check.py` | Flag values outside plausible mp/bp ranges (mp: [−275, 4500] °C, bp: [−275, 6500] °C). |
| `unit_conversion_arithmetic.py` | Verify K → °C and °F → °C math. |
| `verify_doi.py` | Confirm the DOI in `source_url` actually appears in the paper file's text. |
| `verify_evidence_quote.py` | Confirm `evidence_quote` is verbatim present in the paper file. Advisory (Tier 2 verifiability). |
| `quote_support_lint.py` | Confirm `evidence_quote` contains the numeric `value_raw` token. Advisory (Tier 2 verifiability); does NOT auto-drop rows. |
| `csv_quote_lint.py` | Verify RFC-4180 CSV quoting; detect column shifts from unquoted commas in compound names. |
| `dedup_within_paper.py` | Flag duplicate rows within one paper. |
| `verify_row.py` | Run all programmatic checks for a single row. |
| `run_all_checks.py` | Umbrella runner; produces `flags.csv` listing every flagged row. |

## When to apply this skill

Apply this skill any time you are:
- Building a new mp/bp database from a set of provided papers
- Extending an existing database with new papers
- Auditing an existing mp/bp database for errors
- Compiling thermal-property data for downstream design / synthesis decisions

For one-off conversational questions about a single mp/bp ("What's the boiling point of methanol?"), this protocol is overkill. Apply when the data will be used as a basis for downstream decisions.

## Reference files

- `references/COMMON_ERRORS.md` — anti-pattern catalog, filled in as we encounter and verify errors in real runs
- `references/EXTRACTION_PROMPT_TEMPLATES.md` — copy-paste agent prompts that bake in the protocol
- `references/VERIFICATION_PROMPT_TEMPLATES.md` — independent-verification agent prompt with granular flagged_* verdicts

## Evals

Test cases in `evals/evals.json` and fixture CSVs in `evals/files/`. Coverage:
- **scripts-clean-baseline**: rows that pass all checks
- **scripts-detect-seeded-errors**: rows with deliberate errors of each type
- **range-check-edge-cases**: helium / tungsten / decomposition values at the extremes
- **unit-conversion-arithmetic**: K → °C and °F → °C correctness
- **evidence-quote-verification**: verbatim-present detection
- **doi-verification**: DOI substring check
- **truncated-name-detection**: substituent-prefix-only names flagged
- **INACCESSIBLE-handling**: agent given an unreadable paper file must flag rather than fabricate

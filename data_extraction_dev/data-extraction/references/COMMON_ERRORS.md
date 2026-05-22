# Common errors in data extraction

Property-agnostic failure-mode catalog. Each entry describes a pattern that
applies to any data type, with concrete examples (most drawn from mp/bp
extraction trials, since that's where the bulk of historical observations
come from). Property-specific failure modes — the ones that depend on a
particular property's value range, candidate vocabulary, or domain
context — live in each overlay's failure-modes section (e.g., the
"Failure modes observed in past mp/bp trials" section of
`datatypes/mp_bp/OVERLAY.md`).

When a new property-agnostic error pattern is observed during a trial:

1. Note the specific example (which paper, which row, which data type).
2. Identify the root cause (extraction-side, source-side, or verifier-side).
3. Decide whether the protocol can prevent it via a new rule or a refined script.
4. Add an entry here documenting the pattern + prevention.

Property-specific examples are tagged as `**Example (mp_bp):**` or
`**Example (redox):**`. The underlying pattern is generic.

---

## A. NMR / mass-spec context values mistaken for property values

**Pattern.** Numbers from NMR (`δ X.X ppm`, 13C / 1H lists), mass-spec
(`m/z`, `[M+H]+`), or other instrumental context fall within plausible
property-value ranges numerically but aren't measurements of the target
property. The agent's value-finder looks for numbers near keyword tokens
and can latch onto the wrong one.

**Mechanism.** Most chemistry papers report many numerical values
(yields, NMR shifts, m/z peaks, retention times, percentages) clustered
together in characterization paragraphs. A simple "find numeric value
near the candidate token" heuristic doesn't distinguish them.

**Example (mp_bp):** Paper 020 c00015 — value 130 extracted as a melting
point. Actual source: `δ 163.67 (C1, C3), 140.40 (C4'), 134.59 (C2'),
130.56 (C7a, C3a), 130.31 (C6, C5)` — a 13C NMR list. The 130 sits in
typical mp range for small organics.

**Prevention.** Phase 2 of `SKILL.md` instructs the agent to read the
surrounding clause, not just the local span. Each overlay carries
domain-specific "context tells" (mp/bp: `δ`, `ppm`, `m/z`, `13C NMR`;
redox: solvent / electrode mentions adjacent to the value; etc.) in its
own drop-pattern section. The Phase 4 verifier rejects on
`flagged_value_mismatch` if the quote is from an instrumental context.

---

## B. Truncated or fragmented compound names from PDF line wrapping

**Pattern.** Long IUPAC names wrap across PDF lines. The agent captures
the wrapped fragment as the full name. The fragment is often a
substituent suffix (`-yl`, `-yloxy`, `-amine`) without the parent
scaffold, or an indicated-hydrogen form missing the leading locant
(`H-Indeno...` for `7H-Indeno...`).

**Mechanism.** `pdftotext -layout` segments PDFs by physical line. When
a name spans a paragraph boundary, the second-line fragment looks
self-contained.

**Example (mp_bp):** khalifa_2024 paper produced 14 rows of names like
`Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl` — a `-yl` substituent fragment,
not a compound name. Other instances of `H-Indeno...` for `7H-Indeno...`
across the v1.4-era runs.

**Prevention.** The generic `validate_compound_name.py` flags
trailing-substituent patterns (`-yl$`, `-yloxy$`), unbalanced
parens/brackets, dangling hyphens/primes, and indicated-hydrogen
locant truncation (`H-<Capital>-` patterns). Phase 2 step 7.5 of
`EXTRACTION_PROMPT_TEMPLATES.md` covers multi-line reassembly.

---

## C. Multi-row table thead column misalignment

**Pattern.** A table whose header spans multiple physical rows
(e.g., `compound | exp. | calc. | predicted`) causes a programmatic
extractor — or an LLM operating on `pdftotext` output — to bind a
value to the wrong column. One row inherits an adjacent row's value.

**Mechanism.** PDF text extractors flatten 2D tables to 1D text streams
with whitespace separators. Sub-headers under a spanning header lose
their parent association in the flattened form.

**Example (mp_bp):** Paper 064 Table 5 had `STRM | SIRM | [ref]`
sub-columns. The extractor mis-mapped 5+ rows: Chloroquine's row
inherited Thalidomide's value.

**Prevention.** The LLM reading the actual PDF (not just the text dump)
usually catches this — the visual layout is unambiguous. Phase 4 verifier
re-reads the cell and confirms (row, col) alignment. For tables where
text-extraction reliably mangles the structure, the overlay's drop
patterns may include this as a flag-with-`flagged_review` case.

---

## D. Workup solvents extracted as the compound

**Pattern.** In chromatography / chemistry papers, the row's
`compound_name` becomes a workup solvent abbreviation (CH2Cl2, EtOAc,
MeOH, DMSO, DMF, THF, etc.) because that solvent name sits adjacent to
the property value in an Rf or eluent annotation. The actual product
compound is named elsewhere on the page.

**Mechanism.** Text like `Rf: 0.3 (CH2Cl2:MeOH 95:5); mp 165 °C` puts
the solvents and the mp on the same line. A naive name-finder picks
the first capitalized chemistry word near the mp keyword.

**Example (mp_bp):** Paper 020 c00010 — CH2Cl2 captured as the compound,
mp 165 attached. Actual product was named two lines up.

**Prevention.** Each overlay can list common workup solvents in its
drop patterns. Phase 4 verifier rejects on `flagged_compound_mismatch`
if the row's name is a solvent and the value belongs to a different
compound.

---

## E. PDF sign-loss artifacts

**Pattern.** A negative value is rendered without its minus sign by the
PDF text extractor. `−77.9 °C` becomes `77.9 °C` or `277.9 °C` (the `−`
either disappears or is mis-rendered as a `2`).

**Mechanism.** Unicode minus (`−`, U+2212), en-dash (`–`, U+2013), em-dash
(`—`, U+2014), and minus-as-typographic-character are all distinct
codepoints. `pdftotext` and similar extractors don't always preserve
them faithfully. Some PDFs use minus as a glyph that doesn't extract
at all.

**Example (mp_bp):** Paper 2009_Dearden — Methanol mp `−77.9 °C` rendered
as `277.9 °C` in the extracted text. Out of range for a small alcohol
mp, caught by `value_range_check.py`.

**Prevention.** Overlay value-range checks catch dramatically out-of-range
values. For values that land in-range despite sign-loss (e.g., a `−10 °C`
that becomes `10 °C`), the Phase 4 verifier reading the original PDF
sees the sign and reports the discrepancy.

---

## F. Bare-code compound names

**Pattern.** `compound_name` is just a paper-local serial code like
`compound 5`, `complex 9a`, `4b`. The code has no chemistry meaning
outside the paper that uses it.

**Mechanism.** Many synthesis papers introduce compounds by full IUPAC
name once at the start of a section, then refer to them by serial code
throughout. An extractor scanning for `(compound, value)` pairs may
capture the serial code as the name instead of doing the name
resolution.

**Example (mp_bp):** Trial-1 had compound names like `compound 5`,
`complex 9a`, `4b` mixed into the output. Many papers in the corpus
use this pattern.

**Prevention.** Generic `validate_compound_name.py` flags
`^(compound|complex|cpd)\s+\d+[a-z]?$` and `^\d+[a-z]?$`. Phase 2 step
7.5 of `EXTRACTION_PROMPT_TEMPLATES.md` requires multi-line name
reassembly — the agent must look earlier in the section for the full
IUPAC name corresponding to the serial code.

---

## G. Wrong-paper DOI (fabrication or cross-paper bibliography pull)

**Pattern.** The DOI in `source_url` resolves to a paper that doesn't
contain the data. Two sub-causes:
- The extractor invented a plausible DOI from training memory.
- The extractor pulled a DOI out of the paper's bibliography (which
  references *cited* papers, not this paper).

**Mechanism.** When the paper file's own DOI isn't obvious in the front
matter, an extractor under time pressure may substitute one that
"sounds right" or grab the first DOI it sees in the text — often from
the references section.

**Example (mp_bp):** Trial-2 sonnet46 produced 4 rows with DOIs that
appeared nowhere in the source files. Memory-guessed based on
journal/year/title.

**Prevention.** `SKILL.md` Phase 1 step 2 mandates DOI from this
paper's front matter only (NXML `<article-id pub-id-type="doi">`, PDF
front matter, or `metadata.json`). `verify_doi.py` substring-checks
the DOI against the paper file. Phase 4 verifier rejects on
`flagged_doi_fabricated` or `flagged_doi_unrelated_paper`.

A related variant — using the upstream primary's DOI as `source_url`
for a value compiled inside a different paper — is addressed by the
v2.1 affirmative rule in `SKILL.md` Phase 1 step 2: `source_url` is
the DOI of the paper file you are physically reading, regardless of
whether the value was originally measured elsewhere.

---

## H. Memory-based fabrication

**Pattern.** Agent without access to (or skipping) the paper file
generates plausible values from training memory. Specific decimals are
wrong even when the compound is well-known.

**Mechanism.** Extraction agents have seen many chemistry compounds in
training. When the paper file is unreadable or hasn't been opened,
generating a number that "sounds right" feels less effortful than
flagging the row as unreadable.

**Example:** Pre-skill predecessor on 020 dataset — multiple rows for
common compounds (methanol mp, water mp, benzene mp) had the right
chemistry but the wrong decimal places, suggesting memory-based
generation.

**Prevention.** Hard rule in Phase 1 + Phase 2 of `SKILL.md`: every row
must have an `evidence_quote` drawn from a file actually read.
`verify_evidence_quote.py` confirms verbatim presence. If the agent
can't read the file, it must report INACCESSIBLE rather than emit
values. The Phase 4 verifier catches fabricated quotes.

---

## I. Adjacent-measurement quote

**Pattern.** Compound + value + source are all correct, but
`evidence_quote` points at a different adjacent measurement on a
nearby line. The row's data is right; the quote is just pointing the
wrong way.

**Mechanism.** Experimental sections often report multiple
measurements per compound (mp, bp, density, NMR, IR) in adjacent
lines. An agent that grabs the first verbatim string containing the
compound name or a value-keyword can land on a different measurement
than the one whose value they recorded.

**Example (mp_bp):** Trial-1-val row 147 — Methylcyclobutane, claimed
`value_raw = "36.98 °C"` (boiling point). Paper contains
`"b.p. 36.98° (755 mm.)"` (correct), but the agent recorded
`evidence_quote = "f.p. -161.51"` (the freezing point on an adjacent
line).

**Prevention.** Phase 2 step 6 of `EXTRACTION_PROMPT_TEMPLATES.md`
("Quote re-confirmation") instructs the agent to confirm the value in
the quote matches `value_raw`. `quote_support_lint.py` (Tier 2)
catches it as a verifiability issue.

---

## J. Doubled-token PDF artifact

**Pattern.** `pdftotext -layout` on 2-column scientific PDFs sometimes
duplicates words at column boundaries: `"White White powder, powder"`.
The agent transcribes the duplicated form as the evidence_quote.

**Mechanism.** Layout-aware PDF text extraction interleaves left-column
and right-column content line by line. When a sentence wraps in one
column, the duplicate's interleave can produce token-doubling.

**Example (mp_bp):** Trial-1-val row 296 — Khalifa 2024 M7 compound,
mp 257–260 °C. Paper line: `"White powder, mp 257–260 °C"`. Extracted
text: `"White White powder, powder, mp"`. The agent recorded the
doubled form as `evidence_quote`.

**Prevention.** Phase 2 step 6 of `EXTRACTION_PROMPT_TEMPLATES.md`
explicitly rejects doubled tokens. Falling back to `pdftotext` without
`-layout` (or to NXML when available) resolves the artifact.

---

## K. Misapplying the skill as a Python regex extractor

**Pattern.** Agent reads `SKILL.md` and concludes "this is a Python
pipeline; my job is to write the missing extraction script." Writes
`extract_<property>.py` that uses `pdftotext` + `re.findall` over paper
text to bulk-emit rows, with `evidence_quote` populated from the regex
match.

**Mechanism.** Cross-harness validation showed this approach reaches
~56 % audit pass rate vs ~93 % for the LLM-driven approach prescribed
by the skill. Regex can't distinguish context-adjacent numbers
(citation numbers, locants, NMR shifts, counts) from real measurements.

**Example (mp_bp corpus, cross-harness validation):** A parallel agent
wrote a regex extractor on the same 168-paper corpus. The extractor
maintained the schema correctly, passed all the deterministic Phase 3
checks on its 304 output rows, and reached 56 % audit pass rate
(vs 93 % for the LLM-driven approach on the same corpus).

This pattern is property-agnostic. Any data type where the property
keyword appears in non-measurement contexts is vulnerable.

**Prevention.** v1.4 added an explicit MANDATORY-READING block at the
top of `SKILL.md` stating that the agent reads each paper directly and
does NOT write a Python regex extractor. The skill's `description:`
front-matter calls out "LLM-driven" extraction.

---

## L. Verbatim quote stops before the value (2-column PDF wrap)

**Pattern.** `pdftotext -layout` on 2-column PDFs renders each physical
output line as `<column-1 text>  ...  <column-2 text>`. When an
experimental sentence wraps within column 2, the leading clause
(e.g., `"Dark red solid;"`) lands on output line N (right side) while
the value (`"m.p. 168-170 °C"`) lands on output line N+1 (right
side). An agent grepping for the compound finds the leading clause on
the same `pdftotext` line as the compound name and commits that as the
`evidence_quote` — verbatim present in the paper, but it doesn't
actually contain the value.

**Example (mp_bp):** Trial-2 opus47 row 80 — compound
`Ethyl 2-((2-oxo-5-phenylfuran-3(2H)-ylidene)amino)-...`, value_raw
`"168-170 deg C"`, evidence_quote `"Dark red solid;"`. The full
sentence in the paper is `"Dark red solid; 1.64 g, 86 % yield; m.p.
168-170 °С (toluene)."` The quote stopped at the leading clause;
everything after the semicolon (including the value) was missed.

**Prevention.** v1.5 added Step 6.2 of the quote re-confirmation
("Confirm the quote contains the value"). The deterministic
`scripts/quote_support_lint.py` catches this in Phase 3.

---

## M. Constructed / templated quotes from a data-entry script

**Pattern.** Agent reads `SKILL.md`, notes that a regex extractor is
forbidden, but writes a Python data-entry script that hardcodes
compound names + values read manually and constructs `evidence_quote`
strings via f-string templates:

```python
add(nm, mp, bp, f"Table III: {nm} BP {bp} MP {mp}")
```

The underlying compound + value are usually correct, but the quote
strings don't appear verbatim in the source — they're paraphrases.
The K (regex-extractor) anti-pattern doesn't catch this because no
regex is involved.

**Mechanism.** When facing a large reference table (Yalkowsky 1990 SI,
Mitchell 2008 SI, etc.) with hundreds of compounds, an extractor under
time pressure may rationalize: "I'm reading the table manually, just
not writing the quotes manually." The quote templates feel like an
abbreviation, not a fabrication. Audit-time substring-search reveals
they don't appear in the paper.

**Example (mp_bp, Trial-2 sonnet46):** `build_batch_pdfs.py` produced
770 rows from 20 large reference-table PDFs. Templated quotes
included `"Table III: 1,2-diiodobenzene BP 286 MP 27"`. About 22 of
45 audit failures (~half) traced to this script.

This pattern is property-agnostic: any data type that ships through a
CSV with a mandatory `evidence_quote` column is vulnerable.

**Prevention.** v1.5 generalized the anti-pattern from "no regex
extractor" to "no script that produces or transforms the four
evidence-locked fields (`compound_name`, `value_raw`, `evidence_quote`,
`source_url`)." The anti-pattern in `SKILL.md` explicitly names
f-string-templated quotes.

---

## N. DOI from training memory or bibliography

**Pattern.** Agent can't find a DOI in the paper file's front matter
and (a) guesses one based on the journal/year/title from training
memory, or (b) picks a DOI from the paper's *reference list* (those
DOIs belong to *cited* papers, not this paper). A related variant
(new in v2.1): using the upstream primary's DOI as `source_url` for a
value compiled inside a different paper. The wrong DOI then
propagates as the `source_url`.

This pattern is property-agnostic — applies any time the row needs a
paper-level identifier.

**Example (mp_bp, Trial-2 sonnet46):** 4 rows cited DOIs that don't
appear anywhere in the source files. Two rows cited
`10.1002/cbdv.202500394` for compounds that are actually in
`10.1002/ardp.70227` (PMC13006720).

**Example (mp_bp, Trial-7):** Row 1212 cited
`10.1016/j.ijpharm.2009.01.026` (Chu & Yalkowsky 2009) for a value
Alprenolol mp=108 tabulated inside a QSPR paper. The upstream primary
isn't in the corpus; the value was compiled in the corpus paper, so
the corpus paper's DOI should have been `source_url`.

**Prevention.** v1.5 `SKILL.md` Phase 1 Step 2 and
`EXTRACTION_PROMPT_TEMPLATES.md` Step 1b both state: extract DOIs
only from (a) NXML `<article-id pub-id-type="doi">`, (b) PDF front
matter (first 1–2 pages), or (c) `metadata.json`. The DOI must
appear as a substring of the paper file's text. If none of these has
a DOI, use the PMC / PMID / `legacy:` fallback. **Never guess.**
v2.1 adds the affirmative rule: `source_url` is the DOI of the paper
you are physically reading, NOT the DOI of the upstream measurement,
even when the value was compiled from elsewhere.

---

## Where to find data-type-specific errors

Each overlay maintains its own failure-modes section covering
property-specific instances of the patterns above plus failure modes
unique to that property:

- `datatypes/mp_bp/OVERLAY.md` § "Failure modes observed in past mp/bp
  trials" — instances of A, B, C, D, E, I, J, L specific to mp/bp;
  plus mp/bp-only failures (NMR shift in mp range, workup solvent in
  Rf, PDF sign-loss for small-organic mp range).
- `datatypes/redox/OVERLAY.md` § "Redox-specific failure modes" —
  redox-specific patterns (SCE-as-SHE, methyl viologen couple
  ambiguity, aprotic-vs-aqueous conflation, Ag/AgCl electrolyte
  ambiguity).

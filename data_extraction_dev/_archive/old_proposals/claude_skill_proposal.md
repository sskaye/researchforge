# Property Extraction Skill — Design Proposal

A modular skill for extracting compound-level physical-property data from scientific papers. Target: **≥ 98 % correct** on compound names, property values, and provenance. **Precision over recall** — a missed row is better than a wrong row.

The skill is property-agnostic at the top level. Melting-point / boiling-point logic lives in a swappable property module. New properties (log P, pKa, density, solubility, λ\_max, …) plug in via the same interface.

---

## 1. What both audits taught us

The Claude-Test and GPT-Test extractions, the two cross-checks, and the adjudication of 100-row random audits surfaced **eight failure modes**. Every design decision below maps back to one of these:

| \# | Failure mode | Where it bit | Fix in this skill |
| --- | --- | --- | --- |
| F1 | Wrong compound name (one functional group transcribed wrong) | Claude row for paper 011 compound 5d (benzonitrile vs benzoic acid) | All names emitted by string-extraction from source text, never typed by hand; functional-group check against source text |
| F2 | Section title used as compound name | GPT extractor used `"Result and discussion"`, `"N-Hydroxypyridinedione Oximes 33-50"` as compound names | Compound-name blacklist + must-contain check (must match a real-compound lexicon pattern OR be in the article's local code-to-name dictionary) |
| F3 | Local-label-only names (unusable without paper) | Both: `compound 3`, `Pb(II) complex of compound 4`, `benzoxanthenone derivative 4b` | Standalone-name validator with explicit "not-identifiable-from-paper" sentinel |
| F4 | Template-format names with unresolved variables | Both, paper 050: `(X=Cl, R=4-CH3)` with X position never bound in the field | Cross-reference table headers against prose; reject `(X=…)` patterns unless resolved |
| F5 | Whole table or paper missed | GPT missed all 196 Dearden rows; Claude missed all 47 paper 064 rows | Per-paper coverage sanity check: warn if any table with property-keyword headers yields 0 rows |
| F6 | Duplicate rows from inline + table appearances | GPT: paper 026 compounds 4 & 6 twice, paper 178 4h–4j twice | Strong dedup key `(article, normalized_name, value ±0.5, property_kind)` |
| F7 | Open-bound and predicted values handled inconsistently | Claude skipped `>X`; GPT included. Krossing calculated values divided the systems | Explicit `value_kind` + `data_origin` columns; both sides preserve everything, consumer filters |
| F8 | Prose-fragment provenance / paper-jargon in name field | Both: `(NMP, pure guest)`, `Method 1`, `clathrate B`, `[51]` citation marks | Separate `compound_label` and `evidence_text` columns; name field is chemical identity only |

The audits agree on a clear remediation pattern: **resolve compound identity to a standalone name before emitting a row**, and **reject any row where that cannot be done**.

---

## 2. Schema (property-agnostic)

```
column                    type     description
--------------------------------------------------------------------------
compound_name             str      standalone, unique chemical identity (IUPAC,
                                   common, or unambiguous shorthand). Must pass
                                   the standalone-name validator. No paper-local
                                   labels.
compound_label            str      paper-local label or compound code (e.g.,
                                   "4a", "compound 3"). Optional; for traceability.
property_name             str      controlled vocabulary (e.g., "melting_point",
                                   "boiling_point", "log_p", "pka").
thermal_event             str      property-specific subtype (e.g., "melt",
                                   "decomp", "boil", "DSC_onset", "Tg", "Tc").
                                   Defined per-property module.
value_si                  float    value in canonical SI / standard unit, with
                                   ranges collapsed to midpoint. NULL for open bounds.
value_si_min              float    range lower bound, or NULL if single point.
value_si_max              float    range upper bound, or NULL.
value_original            str      printed value exactly as in paper.
unit_original             str      "°C", "K", "°F" as printed.
relation                  str      "=" (default), ">", "<", "≥", "≤", "approx".
data_origin               str      "measured_by_article" | "literature_cited"
                                   | "predicted_<method>" | "unknown".
instrument                str      "DSC", "capillary", "Mettler FP62", "unk".
source_section            str      hierarchical path: "Experimental > Synthesis 
                                   of compounds X > IUPAC name".
evidence_text             str      verbatim substring of the article containing
                                   compound + value + unit. MUST be a
                                   substring of the original article text.
extraction_confidence     str      "high" | "medium" | "low" | "rejected_<reason>".
doi                       str      verified DOI.
article_id                str      stable file/folder/source identifier.
```

**Differences from both prior schemas:**

- `compound_name` is **standalone identity only**. Paper-local labels go in `compound_label`.
- `data_origin` handles the open-bound / predicted / cited disagreement surfaced by both cross-checks.
- `thermal_event` is the property-specific dimension; defined inside each property module.
- `value_si_min`/`max` preserve range information losslessly.
- `extraction_confidence` is set by validators; rows that fail validation get an explicit `rejected_*` value and are emitted only in the audit log, not the final CSV.
- `evidence_text` is **enforced as a verbatim substring** of the article via a programmatic check.

---

## 3. Skill structure

A single Claude Code skill named `property-extraction` with the following file layout. Property-agnostic code at the top, property-specific reference docs/scripts under `properties/`.

```
property-extraction/
├── SKILL.md                      # Top-level workflow (this proposal § 4)
├── reference/
│   ├── schema.md                 # Exact column spec (§ 2 above)
│   ├── name_validators.md        # The standalone-name rules
│   ├── source_ingestion.md       # NXML, PDF, text parsing recipes
│   ├── verification_protocol.md  # The mandatory final audit
│   └── extending_to_new_properties.md  # How to add a new property
├── scripts/
│   ├── ingest_article.py         # → returns sections, tables, text
│   ├── build_label_dictionary.py # → returns {code: iupac_name} from article
│   ├── extract_candidates.py     # → invokes the property module to find
│   │                               #   candidate (compound, value) pairs
│   ├── validate_name.py          # → applies the standalone-name validator
│   ├── verify_substring.py       # → confirms evidence_text in article
│   ├── functional_group_check.py # → checks name vs evidence for FG mismatch
│   ├── dedup.py                  # → strong-key dedup
│   ├── audit_sample.py           # → random-sample verifier
│   └── coverage_check.py         # → per-paper sanity check (F5)
└── properties/
    ├── mp_bp/                    # Reference property module
    │   ├── module.md             # Property-specific instructions
    │   ├── patterns.py           # Regexes per section
    │   ├── unit_conversion.py    # K→°C, °F→°C
    │   ├── thermal_events.py     # melt/decomp/boil/Tg/Tc classifier
    │   └── tests/                # Per-paper expected extractions
    ├── log_p/
    │   ├── module.md
    │   └── …
    └── pka/
        └── …
```

Adding a new property is **purely additive**: create a new directory under `properties/`, implement the module interface (see § 7), and the shared scripts in `scripts/` work unchanged.

---

## 4. [SKILL.md](http://SKILL.md) — the workflow

This is what the top-level `SKILL.md` should instruct the agent to do. The workflow is property-agnostic; everything property-specific is delegated to the property module.

```
Inputs:
  - input_path        : folder, file, or list of articles
  - property          : "mp_bp" | "log_p" | "pka" | …
  - output_csv        : path
  - audit_log         : path

Procedure:

1. Load the property module from properties/{property}/module.md and
   import its functions.

2. For each article:

   a. INGEST. scripts/ingest_article.py extracts:
        - sections (with hierarchical headings)
        - tables (with column/row headers as structured cells)
        - DOI (from NXML front-matter or PDF text)
        - article_id
      Three source modes: NXML > article_text.txt > pdftotext.
      For PDFs, use BOTH `-layout` and `-raw` modes and merge — `-raw`
      is needed to disambiguate negative signs (the Dearden case).

   b. BUILD LABEL DICTIONARY. scripts/build_label_dictionary.py walks
      the entire article text/NXML looking for these patterns:
        "<IUPAC name> ( <code> )"
        "<IUPAC name>, <code>"
        "Synthesis of <IUPAC name>"  (used as the next-paragraph code)
        "<code>: <IUPAC name>"
      Emits {code: standalone_iupac_name} for the whole article.
      This catches the Claude paper 020 compound 3 case — the IUPAC
      name is in a different paragraph from the mp.

   c. RESOLVE TABLE TEMPLATES. For each table, scan the article prose
      for the table's variable definitions:
        - "X = Cl at position 6"
        - "the 6-chloro derivatives (X = Cl)"
        - "R substituent is at the 4-position of the phenyl"
      Build a {variable: (substituent, position)} dictionary. This
      catches the paper 050 case where X is at position 6.

   d. EXTRACT CANDIDATES. Call the property module's
      find_candidates(article) function. It returns:
        list of (compound_handle, value_data, evidence_text, source_path)
      where compound_handle is either a code (to be resolved via the
      label dictionary) or a verbatim chemical name.

   e. RESOLVE COMPOUND NAME. For each candidate:
        - If compound_handle is a code → look up in label dictionary.
          If not found → reject row (extraction_confidence =
          "rejected_unresolved_code").
        - If compound_handle is from a table with X/R variables → use
          the template-resolution dictionary from step (c) to expand
          to a full IUPAC name. If the variable cannot be resolved →
          reject row.
        - If compound_handle is verbatim → keep it.

   f. VALIDATE STANDALONE NAME. scripts/validate_name.py applies the
      rules in reference/name_validators.md (see § 5). Reject any
      name that is a section title, prose fragment, "compound N",
      "derivative N", "X=…, R=…" template, etc.

   g. FUNCTIONAL-GROUP CONSISTENCY CHECK.
      scripts/functional_group_check.py extracts the functional-group
      tokens from compound_name (suffixes like "-nitrile", "-acid",
      "-amide", "-ester", "-thione", and prefixes like "fluoro-",
      "nitro-") and verifies they all appear in evidence_text. This
      catches the Claude paper 011 compound 5d case (recorded
      "benzonitrile" while source said "benzoic Acid").

   h. VERIFY EVIDENCE_TEXT IS A SUBSTRING.
      scripts/verify_substring.py confirms that the evidence_text
      column is a verbatim substring of the article text (after
      whitespace normalization). If not → reject row.

   i. CLASSIFY data_origin AND thermal_event. The property module's
      classify(candidate) function tags this. For mp/bp:
        - "measured_by_article": this paper's own DSC/capillary run
        - "literature_cited": value cited from another paper's measurement
        - "predicted_<method>": e.g., "predicted_SIRM", "predicted_STRM"
        - thermal_event: "melt", "decomp", "boil", "Tg", "Tc",
          "DSC_onset", "DSC_peak", etc.

   j. EMIT row with all schema fields populated.

3. DEDUPLICATE. scripts/dedup.py applies a strong key
   (article, normalized_name, property_name, value_si ±0.5,
   thermal_event). Multiple rows with same compound + value from
   table + inline characterization collapse to one.

4. COVERAGE CHECK. scripts/coverage_check.py runs after extraction
   and warns if any of:
     - A paper with property keywords in the abstract returned 0 rows.
     - A table whose headers match property-keywords yielded 0 rows.
     - The row count is more than 50 % lower than the article's
       "N compounds were synthesized" claim.
   These warnings go to audit_log and require human review before
   the CSV is considered final.

5. RANDOM-SAMPLE VERIFICATION. scripts/audit_sample.py picks a 15 %
   random sample, dispatches each row to an independent verifier agent
   (different instance from the extractor), and records:
     - Does the recorded value match the printed value?
     - Is compound_name's functional-group suffix present in source?
     - Is compound_name standalone-interpretable?
     - Is evidence_text a verbatim substring?
   If <98 % pass → fail the run; require human review.

Outputs:
  - output_csv: clean rows only (no rejected rows).
  - audit_log: all rejected/flagged rows with reasons, coverage warnings,
    and the verification-sample audit results.
```

The workflow is intentionally **chained gates**. Every row must clear:

1. **Compound name resolved** (label dictionary or verbatim).
2. **Compound name standalone-valid** (§ 5 validator).
3. **Functional-group suffix check** (§ 6).
4. **Evidence is a verbatim substring** (§ 6).
5. **Random-sample auditor agrees** (§ 8).

Any row that fails any gate is rejected, not emitted. This is the precision-over-recall stance the user asked for, made operational.

---

## 5. The standalone-name validator

`reference/name_validators.md` defines the rules. Concretely, a name is **rejected** if any of these match:

```
REJECT_PATTERNS = [
    # Section titles / prose fragments
    r"^(?:Results?\s+and\s+Discussion|Introduction|Experimental|Methods?)$",
    r"^(?:Synthesis|Preparation|General\s+Procedure)\b",
    r"^The\s+(?:precursors|compound|product|minor)",

    # Bare codes / local labels  
    r"^compound\s+\d+[a-z]?$",         # "compound 3"
    r"^\d+[a-z]?$",                     # just "4a"

    # Generic derivative labels
    r"\bderivative\b\s*\d*[a-z]?$",     # "benzoxanthenone derivative 4b"
    r"\bcomplex\s+of\s+compound\s+\d",  # "Pb(II) complex of compound 4"

    # Unresolved template variables
    r"\(\s*X\s*=",                      # any "(X="
    r"\(\s*R\s*=",                      # any "(R="
    r"R\d+\s*=",                        # "R1=H"

    # Range labels  
    r"\bcompounds?\s+\d+\s*[-–]\s*\d+", # "compounds 33-50"
    r"^\w+s\s+\d+-\d+",                 # "Oximes 33-50"

    # Empty / too short
    r"^\s*$",
    r"^.{1,3}$",
]

REQUIRE_PATTERNS = [
    # Must contain at least one chemistry-bearing token OR be in a 
    # known-common-name lexicon
    r"(?:yl|oxy|amine|amino|acid|ester|amide|nitrile|thione|thiol|"
    r"alcohol|phenyl|methyl|ethyl|hydroxy|naphthal|benzo|pyrid|pyrim|"
    r"thiadiazol|oxadiazol|triazol|imid|sulfanyl|sulfonyl)",
    # Acceptable IL shorthand: [...][...]
    r"\[[^\]]+\]\[[^\]]+\]",
]

EXEMPT_NAMES = {  # known small molecules that don't match the above
    "acetone", "methanol", "ethanol", "water", "benzene", "toluene",
    "chloroquine", "dexamethasone", …  # property module can extend
}
```

A name passes only if **no REJECT_PATTERN matches** AND **at least one REQUIRE_PATTERN matches OR the name is in the EXEMPT_NAMES lexicon**.

Failed names get `extraction_confidence = "rejected_name_not_standalone"`and go to the audit log with the rejection reason. The audit log lets a human decide whether to extend `EXEMPT_NAMES` or fix the upstream resolution.

---

## 6. The substring + functional-group gate

This is the gate that would have caught the Claude paper 011 #5d error. Implemented as two scripts:

### 6a. `verify_substring.py`

```
def verify_evidence_is_substring(evidence_text, article_full_text):
    """Confirm evidence_text is a verbatim substring of the article
    after whitespace normalization. Returns True/False."""
    e = re.sub(r"\s+", " ", evidence_text).strip()
    a = re.sub(r"\s+", " ", article_full_text)
    return e in a
```

If False → reject row with reason `rejected_evidence_not_in_article`.

### 6b. `functional_group_check.py`

```
FG_TOKENS = [
    # Suffixes that indicate a specific functional group
    "nitrile", "acid", "ester", "amide", "amine", "alcohol",
    "ether", "ketone", "aldehyde", "phenol", "sulfonate",
    "sulfanyl", "sulfonyl", "sulfide", "thione", "thiol",
    # Substituent prefixes that change identity  
    "fluoro", "chloro", "bromo", "iodo", "nitro", "methoxy",
    "ethoxy", "hydroxy", "amino", "cyano",
    # Heterocycle stems
    "pyridazin", "pyrimidin", "thiadiazol", "oxadiazol", "triazol",
    "imidazol", "thiazol", "pyrrol", "furan", "thiophen",
    "naphthalen", "indol", "quinolin", "isoquinolin",
]

def functional_group_consistency(compound_name, evidence_text):
    """Every FG token in the name must also appear in evidence_text.
    Returns (ok: bool, missing_tokens: list)."""
    name_low = compound_name.lower()
    evid_low = evidence_text.lower()
    name_tokens = {t for t in FG_TOKENS if t in name_low}
    evid_tokens = {t for t in FG_TOKENS if t in evid_low}
    missing = name_tokens - evid_tokens
    return (len(missing) == 0, list(missing))
```

If `ok` is False → reject row with reason `rejected_functional_group_mismatch: <token>`.

This is the single most important precision gate. Across both this study's audited datasets, this check alone would have caught **the one real chemistry-level transcription error** (the benzonitrile/benzoic-acid case) **and** every section-title-as-name failure in GPT's output (those rows have zero FG tokens in `compound_name`).

---

## 7. Property module interface

A property module is a self-contained directory under `properties/`. It must expose:

```python
# properties/{name}/module.py

PROPERTY_NAME = "melting_point"  # or list ["melting_point", "boiling_point"]

# Allowed thermal-event tags for this property
THERMAL_EVENTS = ["melt", "decomp", "melt_or_decomp", "boil",
                  "DSC_onset", "DSC_peak", "sublimation"]

# Allowed data_origin tags
DATA_ORIGINS = ["measured_by_article", "literature_cited",
                "predicted_<method>"]

# Property-specific extras to the EXEMPT_NAMES lexicon
EXTRA_EXEMPT_NAMES = {"glutaraldehyde", "dehydrocholic acid", ...}

def find_candidates(article):
    """Yields (compound_handle, value_data, evidence_text, source_path).
    Implementation may use regex catalogs, NXML table parsers,
    chemistry-specific cues, etc. See patterns.py for mp/bp patterns."""
    ...

def parse_value(value_text):
    """Convert printed value to {value_si, value_si_min, value_si_max,
    value_original, unit_original, relation}.
    For mp/bp: handles °C / K / °F, ranges, '>X', '<X'."""
    ...

def classify(candidate, article_context):
    """Returns (data_origin, thermal_event, instrument).
    For mp/bp: distinguishes 'mp 245 (dec.)' as melt_or_decomp,
    'Te' from DSC subsequent-cycles as DSC_onset, table column
    'experimental Tfus' as measured_by_article vs 'calculated' as
    predicted_<method>."""
    ...
```

The top-level workflow calls these four functions per article. Property modules can also ship a `patterns.py` (regex catalog), a `unit_conversion.py`, and a `tests/` folder with golden extractions for canonical papers.

**Adding a new property** (e.g., log P):

1. Create `properties/log_p/`.
2. Write `module.py` implementing the four functions above.
3. Write `module.md` documenting the property's idioms (typical phrasings, units, measurement methods).
4. Drop in 1–2 known papers under `tests/` with manually-verified expected outputs.
5. The top-level skill works unchanged.

---

## 8. Verification protocol (the audit log)

The skill emits **two** files per run, not just one:

1. `output.csv` — clean, verified rows only. Every row in this file passed:

   - Name resolution
   - Standalone-name validator
   - Functional-group consistency check
   - Evidence-substring check
   - Random-sample independent verification (98 % threshold)

2. `audit_log.json` — everything that didn't make it, with reasons. Structure:

   ```
   {
     "run_metadata": {
       "input": "...", "property": "mp_bp", "timestamp": "...",
       "row_counts": {"emitted": N, "rejected": M, "duplicates_collapsed": K}
     },
     "rejected_rows": [
       {"reason": "rejected_name_not_standalone", "candidate": {...}},
       {"reason": "rejected_functional_group_mismatch: acid", "candidate": {...}},
       ...
     ],
     "coverage_warnings": [
       {"article": "058_…", "warning": "abstract mentions synthesis but 0 rows emitted",
        "candidates_found": 0}
     ],
     "verification_sample": {
       "sample_size": N, "seed": ..., "pass_rate": 0.98,
       "failures": [{"row_id": ..., "reason": ...}]
     }
   }
   ```

The audit log is **the verifiability story**. Anyone can re-run the extractor and get the same audit log; anyone can spot-check the audit log to confirm the rejected rows really should have been rejected.

The random-sample verification step uses a **separate agent instance**from the extractor — same precaution as in the earlier 100-row audit where independent agents went back to the source paper. The sample size is 15 % of emitted rows by default; the pass threshold is configurable but defaults to **98 %** (the user's target).

If the pass rate is below the threshold, the run is flagged as `failed`and the output CSV is not delivered. The user must either:

- Inspect and fix the cause of the failures, OR
- Lower the threshold in the run config (and accept lower quality).

---

## 9. Scope policy — how to handle the audited disagreements

The two audits surfaced four scope questions on which Claude and GPT disagreed. The skill resolves each by **always extracting and tagging**, then letting the consumer filter.

| Scope question | Default policy | Configurable |
| --- | --- | --- |
| <!-- fmc:1 -->Open-bound values<!-- /fmc:1 --> (`>X`, `<X`) | Emit with `relation = ">"` and `value_si = NULL`. `value_original` keeps the inequality string. | Always on |
| Predicted/calculated values | Emit with `data_origin = predicted_<method>`. | `--include-predicted false` flag drops them |
| Literature-cited values from another paper | Emit with `data_origin = literature_cited`. | `--measured-only` flag drops them |
| Table cell that's an image (no text) | Reject with `rejected_image_only_compound_name`; log to audit. | Optional OCR fallback (out of scope for v1) |

This converts the four prior-extraction disagreements from "data lost because of scope" into "data tagged and filterable." A user who wants strict measurement-only data sets `--measured-only`. A user training a QSPR model who wants both measured and predicted values doesn't.

---

## 10. Targeting ≥ 98 % accuracy — the four-gate stack

The user's accuracy target translates into concrete pass criteria:

| Gate | What it checks | What it would have caught in this study |
| --- | --- | --- |
| **1. Compound-name validator (§ 5)** | No section titles, no template variables, no generic "derivative" | GPT: `"Result and discussion"`, `"N-Hydroxypyridinedione Oximes 33-50"`. Both: 25 paper-050 `(X=…)` rows and 6 paper-178 "derivative" rows |
| **2. Functional-group consistency (§ 6b)** | <!-- fmc:2 -->Every FG token in name appears in evidence_text<!-- /fmc:2 --> | Claude: paper 011 #5d (benzonitrile vs benzoic Acid) |
| **3. Evidence substring (§ 6a)** | Evidence is a verbatim substring of the article | Claude: my synthesized "Table 2 …" preambles for paper 178; some prose-fragment names in GPT |
| **4. Random-sample independent verification (§ 8)** | An independent agent re-reads the source and confirms | All four bugs above plus the 2 paper-020 Claude misses (revealed at the coverage-warning level) |

With these four gates in place, the only way for a wrong row to reach the output CSV is if:

- A wrong functional-group transcription happens **and** the wrong functional-group token also appears somewhere in the evidence text (this would be a near-miss; the FG check uses presence, not position, so a paper that mentions both benzoic acid and benzonitrile in the same paragraph could in principle pass — see § 12 for the residual-risk plan).
- A name passes the standalone-name validator but is still ambiguous (e.g., a common name like "naphthalene" that actually refers to a derivative in the paper). Mitigation: § 11 (`compound_label` retains the paper's code, so a human auditor can trace).

These are residual ≤ 1 % failure modes; the targeted-98 %-correct budget can absorb them.

---

## 11. Compound-label retention (traceability without identity pollution)

A separate `compound_label` column holds the paper's local code (`4a`, `compound 3`, `1g`, etc.) for traceability. This is **not** in `compound_name`. Two columns, two purposes:

- `compound_name` → "this is *what the compound is*", standalone.
- `compound_label` → "this is *what the paper called it*", traceable.

Both Claude and GPT's outputs conflated these. The skill keeps them separate.

When a code cannot be resolved to a standalone name and the name field would otherwise have to be rejected, the skill emits:

```
compound_name = "<not_identifiable_from_paper>"
compound_label = "4b"
extraction_confidence = "low_unresolved_compound"
```

This is honest: the value is correct, the code is real, but the name cannot be recovered from this paper alone. A downstream consumer can join against external databases (CAS lookup, PubChem) to resolve, or filter these rows out.

---

## 12. Residual risks and how the skill handles them

The four-gate stack still leaves these:

| Residual risk | Probability | Mitigation |
| --- | --- | --- |
| FG token in name appears in evidence (e.g., paper mentions multiple FGs near one value) | Low | Mitigate with token-position check: require FG token to be near the compound-name occurrence in evidence, not just present anywhere |
| Common-name ambiguity (paper uses "naphthalene" for a derivative) | Low | Retain `compound_label`; flag with `extraction_confidence = "medium"` so a downstream auditor can sample |
| Table cells with structural image only (paper 056) | Known limitation | Audit-log warning; OCR fallback is a v2 feature |
| Paper-typo preservation (1-Hexane vs n-hexane in Dearden) | Acceptable | Skill faithfully transcribes; consumer-side QC can fix |
| Pdftotext sign-rendering bug (`-141.8` → `2141.8`) | Mitigated | Always run both `-layout` and `-raw`; reconciliation step in `parse_value` |

<!-- fmc:3 -->A v2 of the skill could add:<!-- /fmc:3 -->

- **CAS/PubChem cross-reference** of every emitted name (`compound_name`
  - molecular formula must match a known compound).
- **OCR fallback** for image-cell tables.
- **Compound-name fuzzy dedup** that recognizes `2-((Cyclopentyloxy)methyl)isoindoline-1,3-dione`and `2-((cyclopentyl-oxy)methyl)isoindoline-1,3-dione` as the same compound.

---

## 13. Worked example — running the skill on this corpus

Hypothetically, if this skill had run over the 20-paper `mp_bp_dev_set`:

| Paper | Claude actual | GPT actual | Skill prediction |
| --- | --- | --- | --- |
| 011 PDE4 | 55 (1 chemistry error) | 55 | 54 emitted, 1 FG-mismatch rejected (compound 5d), audit-log entry |
| 020 N-hydroxypyridinedione | 32 (2 missed) | 39 | ≥34 emitted, both 5 and 40 caught via candidate enumeration |
| 050 quinazolines | 18 (X-position unresolved) | 19 | 0 emitted as-is; coverage warning issued; with template-resolver from § 4(c) producing "6-chloro-…" names, 18 emitted |
| 064 COVID API | 0 (over-skipped) | 47 (incl. predictions) | 9 emitted (literature_cited), 36 emitted as predicted\_, 2 rejected as section-title names |
| 178 benzoxanthenones | 10 (4a only inferred) | 13 (3 duplicates) | 4 emitted with full names (4a, 4h, 4i, 4j), 6 rejected as not_identifiable_from_paper |
| 2009 Dearden | 196 | 0 | 196 emitted (coverage check would have caught GPT's 0) |
| 2011 Krossing | 40 | 92 (with predictions) | ≥40 emitted measured + ≥50 emitted predicted, tagged |

The skill ends up **closer to Claude on stand-alone-quality, closer to GPT on coverage**, and **strictly better on the residual error modes both systems exhibited.**

---

## 14. Summary

The skill is built around the user's stated priority:

> *It's much more important that all data extracted be correct and verifiable than that no data be missed.*

The mechanism is a **four-gate stack** (standalone-name validator, functional-group consistency check, evidence-substring check, random- sample independent verification) backed by a **two-column identity schema** (`compound_name` for standalone identity, `compound_label` for paper-local provenance) and **explicit-tagging of scope-policy disagreements** (`value_kind`, `data_origin`, `thermal_event`).

Modularity is delivered by a thin property-module interface (`find_candidates`, `parse_value`, `classify`, EXTRA_EXEMPT_NAMES); the existing mp/bp logic becomes the reference module. Adding log P, pKa, density, or any other property is a directory-create plus four-function implementation away.

Verifiability is delivered by emitting **two files per run**: the clean output CSV, and an audit log that captures every rejection, every coverage warning, and every verification-sample result. A downstream auditor can re-derive the output from the audit log without re-running the extractor.

This should meet the **≥ 98 % correct** target on compound names, property values, and provenance — the four gates would have caught every substantive error surfaced by the two prior audits in this study, and the audit-log mechanism makes any residual error inspectable rather than hidden.

<!-- forgemark-comments
- id: 1
  anchor_text: "Open-bound values"
  context_before: "ays extracting and tagging, then letting the consumer filter. Scope question Default policy Configurable "
  context_after: " (>X, <X) Emit with relation = \">\" and value_si = NULL. value_original keeps the inequality string. Always on"
  author: Steven
  timestamp: "2026-05-11T02:25:15.019Z"
  edited_at: "2026-05-11T02:26:07.123Z"
  resolved: false
  body: "If melting point is ># (e.g. >50), then the melting point should be recorded as “50” with relation=“>”. Then, the user of the table can filter by relation if the want to exclude those values."
- id: 2
  anchor_text: "Every FG token in name appears in evidence_text"
  context_before: " 33-50\". Both: 25 paper-050 (X=…) rows and 6 paper-178 \"derivative\" rows 2. Functional-group consistency (§ 6b) "
  context_after: " Claude: paper 011 #5d (benzonitrile vs benzoic Acid) 3. Evidence substring (§ 6a) Evidence is a verbatim sub"
  author: Steven
  timestamp: "2026-05-11T02:28:33.877Z"
  resolved: false
  body: "For this rule to be useful, we need to make sure the evidence text includes not just the snippet containing the name & property value, but also where the agent determines and substitutions in the name. For example, if the text says “compound 4, mp=32 C” and elsewhere in the text it says “benzonitrile (compound 4)”, then both text snippets should be included."
- id: 3
  anchor_text: "A v2 of the skill could add:"
  context_before: "endering bug (-141.8 → 2141.8) Mitigated Always run both -layout and -raw; reconciliation step in parse_value "
  context_after: " CAS/PubChem cross-reference of every emitted name (compound_name molecular formula must match a known compound)."
  author: Steven
  timestamp: "2026-05-11T02:30:14.277Z"
  resolved: false
  body: "These are all good ideas. Add them as a TODO in the proposal with instructions that this list should be maintained as we build the skill."
-->

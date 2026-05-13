# data_extraction_dev — folder organization

This folder holds the development work for the **`mp-bp-extraction` skill** — an LLM-driven, evidence-locked extractor for melting-point and boiling-point data from scientific papers. The skill itself is at `mp-bp-extraction/`; everything else is supporting material (paper corpora used for trials, trial outputs, audits, analyses, and reports).

The current production version of the skill is **v1.4**, packaged as `mp-bp-extraction/dist/mp-bp-extraction.skill`. The Trial-2 evidence (`reports/trial2_comparison_report.md`) shows it reaches 98 % audit pass with Claude Opus 4.7, 86 % with GPT-5.5 high, and 55 % with Claude Sonnet 4.6 on the 168-paper corpus. A v1.5 update is planned (see `development_report.md` section 15) but not yet implemented.

## Top-level layout

```
data_extraction_dev/
├── README.md                          # this file
├── CHANGELOG.md                       # skill version history (v1.0 → v1.4)
├── development_report.md              # full project narrative + best-practice principles
│
├── mp-bp-extraction/                  # THE SKILL (production v1.4)
│
├── corpora/                           # paper sets used for trials
│   ├── dev_20/                        # 20 development papers
│   ├── val_30/                        # 30 validation papers
│   └── full_168/                      # 168-paper corpus (Trial-1-full + Trial-2)
│
├── trials/                            # extraction outputs + audit verdicts
│   ├── trial1/
│   │   ├── dev/                       # Trial-1 on dev (100 % audit)
│   │   ├── val/                       # Trial-1 on val (98 % audit)
│   │   ├── full/                      # Trial-1 on full (93 % audit, native harness)
│   │   └── full-gpt55_high/           # cross-harness regex-extractor run (56 % audit)
│   └── trial2/
│       ├── full-gpt55_high/           # Trial-2 GPT-5.5 high on v1.4 (86 % audit)
│       ├── full-opus47/               # Trial-2 Opus 4.7 on v1.4 (98 % audit)
│       └── full-sonnet46/             # Trial-2 Sonnet 4.6 on v1.4 (55 % audit)
│
├── reports/                           # cross-trial analyses and self-analyses
│   ├── skill_comparison.md            # attempt 1 vs sibling redox-extraction skill
│   ├── trial2_comparison_report.md    # three-model Trial-2 comparison + v1.5 plan
│   ├── trial2_analysis_opus47.md      # Opus 4.7's self-analysis of its run
│   ├── trial2_analysis_GPT55_high.md  # GPT-5.5's self-analysis of its run
│   ├── trial2_analysis_sonnet46.md    # Sonnet 4.6's self-analysis (Path A / Path B)
│   └── trial2_summary.json            # machine-readable Trial-2 audit summary
│
├── recall_study/                      # recall-side audit on dev + val (precision-only audits don't measure recall)
│   ├── recall_report.md
│   ├── dev_enumerations/              # per-paper enumeration JSONs (8 dev papers)
│   ├── val_enumerations/              # per-paper enumeration JSONs (9 val papers)
│   └── analysis/                      # compute_recall.py + results
│
├── _archive/                          # superseded / reference work
│   ├── property-extractor_attempt1/   # first regex-based attempt, plateaued at 67 % / 41 %
│   ├── old_proposals/                 # early design proposals + baseline extractions
│   └── example_skill_redox/           # redox-extraction sibling skill (informed attempt 2)
│
└── _to_delete/                        # files staged for deletion
```

## What each directory contains

### `mp-bp-extraction/` — the skill

The shipped skill. Self-contained; everything an installed agent sees is in here.

- `SKILL.md` — the protocol (mandatory direct-read, six phases, anti-patterns, schema)
- `references/` — extraction + verification prompt templates, common-errors catalog
- `scripts/` — deterministic Phase-3 sanity checks (crossref lookup, name validation, value-range check, unit-conversion arithmetic, DOI verification, quote verification, dedup, CSV-quote lint, umbrella `run_all_checks.py`)
- `evals/` — clean baseline + seeded-error fixtures; 10 evals total
- `dist/mp-bp-extraction.skill` — packaged installable zip artifact

The `CHANGELOG.md` lives at the project root, *outside* the skill, so that installed agents don't see version history.

### `corpora/` — paper sets

Three paper corpora used as test inputs. Each subdir is one paper per folder (NXML + PDF for PMC papers, single PDF for older or non-PMC papers, occasionally HTML+PDF pairs for newer Wiley papers).

- `dev_20/` — 20 papers used during initial skill development
- `val_30/` — 30 held-out validation papers
- `full_168/` — large-scale validation corpus including pharma cocrystals, materials/inorganic, ionic liquids, and prediction/QSPR papers

**Note on licensing:** these are journal articles. They should NOT be committed to a public repo — see "What to gitignore" below.

### `trials/` — extraction outputs + audit verdicts

One subdirectory per trial run. Each contains:

- The extraction CSV (e.g. `extracted_all.csv`, `trial1_output.csv`)
- Per-batch CSVs from parallel extraction agents
- The audit sample (typically 100 random rows)
- Per-verifier-agent verdict JSONs (`_my_verdicts_1.json` … `_my_verdicts_4.json`)
- An aggregated verdict JSON (`_my_verdicts_all.json`)
- Run notes (e.g. `README.md`, `EXTRACTION_SUMMARY.md`, `RUN_REPORT.md`)

Naming convention: `trial<N>/<corpus>[-<agent>]`. The Trial-1 native-harness runs have no agent suffix; cross-harness or alternate-model runs append the model identifier.

### `reports/` — cross-trial analyses

Markdown analyses that span multiple trials or compare approaches.

- `skill_comparison.md` — original architectural comparison: attempt 1 (regex) vs the redox-extraction sibling that informed the rebuild
- `trial2_comparison_report.md` — three-agent Trial-2 comparison + field-level failure categorization + agent self-analysis findings + consolidated v1.5 plan
- `trial2_analysis_<agent>.md` — each Trial-2 agent's first-person account of what it did and where the skill failed to constrain it
- `trial2_summary.json` — pass/fail counts + Wilson CIs + failure-mode histograms for the three Trial-2 runs

### `recall_study/`

The Trial-1 audits measured **precision** (of emitted rows, how many are correct). The recall study measured **recall** (of values that should have been emitted, how many did the skill find). Conducted on 8 dev papers + 9 val papers; results in `recall_report.md`. Headline: ~89 % dev recall, ~93 % val recall on normal papers, with the gap being mostly schema-modeling decisions and protocol-driven sampling rather than true misses.

### `_archive/`

Three sub-folders for superseded work that's worth keeping for historical / pedagogical reasons but is not part of the active project:

- `property-extractor_attempt1/` — the original 6,370-LOC regex-based extraction attempt that plateaued at 67 % dev / 41 % val. Sections 3 and 17 of the development report describe what we learned from it. Contains its own `merged_skill_proposal.md` and the pre-rebuild `validation_report.md`.
- `old_proposals/` — early design proposals, the no-skill baseline extractions, and the Claude-vs-GPT cross-checks that motivated the schema.
- `example_skill_redox/` — the redox-extraction sibling skill that informed attempt 2's architecture (LLM-driven extraction + small deterministic scripts + verbatim evidence quote). Not part of this project, but referenced as the canonical example of the pattern.

### `_to_delete/`

Files I judged spurious or scratch-only during the reorg. Listed here rather than deleted in place so they can be reviewed before removal.

| File | Why it's here |
|---|---|
| `.DS_Store` | macOS metadata; should never be committed |
| `flags.csv.toplevel-stray` | Single-row test artifact from an early sanity-check pass; not used |
| `build_csv.py.toplevel-stray` | Duplicate of `trials/trial1/full/build_csv.py`; top-level copy is a stray |
| `li2025.txt` | Plain-text extract from Li 2025 paper; source PDF is in the corpus, this was scratch |
| `rios.txt` | Plain-text extract from Rios paper; same reason as above |

All of these can be safely deleted. The renamed `.toplevel-stray` suffix is to make it clear which top-level copy was removed (the meaningful copies are elsewhere in the tree).

## What to gitignore

This folder was developed locally and has not been committed yet. When committing, the following should be in `.gitignore`:

```gitignore
# macOS metadata
.DS_Store
**/.DS_Store

# Python bytecode (appears in scripts/ and analysis/ dirs)
__pycache__/
*.pyc

# Paper corpora — copyrighted journal PDFs/HTML/NXML, should not be in a public repo
corpora/

# Files staged for deletion
_to_delete/
```

### Notes on the gitignore

- **`corpora/`** is the most important entry. The full 168-paper corpus contains journal articles from ACS, Wiley, RSC, Elsevier, etc. — committing it would be a copyright issue. If you need the trials to be reproducible by someone else, document the paper list (DOI + citation) in a manifest instead of shipping the files.
- **Trial outputs** (`trials/`) are NOT gitignored — they're CSVs of extracted data plus audit verdicts, which are the project's outputs and should be tracked in git so the trial history is preserved.
- **`_to_delete/`** is gitignored so a future `rm -rf _to_delete/` doesn't show up as a destructive commit.
- **`mp-bp-extraction/dist/*.skill`** is committed (NOT gitignored). It's the packaged installable artifact for the current release version, and the canonical reference an external user would install from. Treat it as the release deliverable, not as a build artifact. Rebuild + commit it on each version bump.
- The skill directory `mp-bp-extraction/` itself should be tracked in full — that's the deliverable.

## What to do before committing

1. Review `_to_delete/` and either delete the files (`rm -rf _to_delete/`) or move anything back to its proper location.
2. Confirm `corpora/` is in `.gitignore` (or move it out of the repo if you'd prefer not to keep it tracked at all locally).
3. Tag this commit clearly — it represents **v1.4 of the skill at 98 % Opus / 86 % GPT / 55 % Sonnet on the 168-paper corpus**. The v1.5 work will be a separate branch / commit, so this tag is the revert target if v1.5 regresses Opus performance.
4. The `recall_study/` directory contains paper enumeration JSONs but no PDF content — safe to commit.

## Where to look first for context

- **What is this project?** Read `development_report.md` sections 1–5 (problem statement → first attempt → architectural pivot → second attempt design).
- **What's the current state of the skill?** `mp-bp-extraction/SKILL.md`, then `CHANGELOG.md`.
- **What's the most recent evidence?** `reports/trial2_comparison_report.md`.
- **What's planned next?** `development_report.md` sections 15 and 19.
- **What's the publication-ready meta-lesson?** `development_report.md` sections 13–15 (cross-model variability + agent self-analyses + the v1.5 plan derived from them).

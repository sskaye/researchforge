# data_extraction_dev — folder organization

This folder holds the development work for the **`mp-bp-extraction` skill** — an LLM-driven, evidence-locked extractor for melting-point and boiling-point data from scientific sources (journal articles and reference textbooks). The skill itself is at `mp-bp-extraction/`; everything else is supporting material (corpora used for trials, trial outputs, audits, analyses, and reports).

**Current production version: v1.7**, packaged as `mp-bp-extraction/dist/mp-bp-extraction.skill`. Six trials have been run; the most recent (Trial-5 on a 168-paper journal corpus and Trial-6 on a 2,643-page reference textbook) audited at **99.7 %** and **99.3 %** Tier-1 correctness respectively. The audit framework that produces those numbers is documented in `audit_criteria.md` at this folder's root.

Production target is **Claude Opus 4.7**. The skill carries cross-model robustness defenses (validated against GPT-5.5 and Sonnet 4.6 in Trial-2) but those models are not actively re-tested.

## Top-level layout

```
data_extraction_dev/
├── README.md                          # this file
├── CHANGELOG.md                       # skill version history (v1.0 → v1.7)
├── audit_criteria.md                  # three-tier audit framework + Phase-4 procedure
├── development_report.md              # full project narrative + best-practice principles
│
├── mp-bp-extraction/                  # THE SKILL (production v1.7)
│
├── corpora/                           # source material used for trials
│   ├── dev_20/                        # 20 development papers
│   ├── val_30/                        # 30 validation papers
│   └── full_168/                      # 168-paper journal corpus (T1-full, T2, T3, T4, T5)
│
├── trials/                            # extraction outputs + audit verdicts
│   ├── trial1/
│   │   ├── dev/                       # Trial-1 on dev (100 % audit)
│   │   ├── val/                       # Trial-1 on val (98 % audit)
│   │   ├── full/                      # Trial-1 on full (93 % audit, native harness)
│   │   └── full-gpt55_high/           # cross-harness regex-extractor run (56 % audit)
│   ├── trial2/
│   │   ├── full-gpt55_high/           # T2 GPT-5.5 high on v1.4 (86 % audit, 907 rows)
│   │   ├── full-opus47/               # T2 Opus 4.7 on v1.4 (98 % audit, 1,864 rows)
│   │   └── full-sonnet46/             # T2 Sonnet 4.6 on v1.4 (55 % audit, 2,567 rows)
│   ├── trial5/opus47/                 # T5 Opus 4.7 on v1.7 (99.7 % audit, 2,063 rows)
│   └── trial6/                        # T6 Opus 4.7 on v1.7, CRC Handbook textbook
│       ├── book/                      # CRC Handbook of Chemistry & Physics, 97th Ed.
│       └── opus47/                    # 15,741 rows, 99.3 % audit
│
├── Trial3-full-opus47/                # T3 Opus 4.7 on v1.5 (97.0 % audit, 1,352 rows)
├── Trial3-full-gpt55_high/            # T3 GPT-5.5 (76 % strict, heavy self-flagging)
├── Trial3-full-sonnet46/              # T3 Sonnet 4.6 (79 % strict, +24 pp vs T2)
├── Trial4-opus47/                     # T4 Opus 4.7 on v1.6 (98.0 % audit, 1,529 rows)
│
├── reports/                           # cross-trial analyses and self-analyses
│   ├── skill_comparison.md            # attempt 1 vs sibling redox-extraction skill
│   ├── trial2_comparison_report.md    # T2 three-model comparison + v1.5 plan
│   ├── trial2_analysis_*.md           # T2 agent self-analyses (Opus, GPT, Sonnet)
│   ├── trial2_summary.json            # T2 machine-readable audit summary
│   ├── trial3_comparison_report.md    # T3 + 300-row Opus expansion + audit-rubric correction + v1.6 plan
│   ├── trial4_comparison_report.md    # T4 + cross-trial-contamination + v1.7 plan
│   ├── trial5_comparison_report.md    # T5 + manifest validation + steady-state confirmation
│   └── trial6_comparison_report.md    # T6 + textbook generalization + 6-trial summary
│
├── recall_study/                      # recall-side audit on dev + val
│   ├── recall_report.md
│   ├── dev_enumerations/
│   ├── val_enumerations/
│   └── analysis/
│
├── _archive/                          # superseded / reference work
│   ├── property-extractor_attempt1/   # first regex-based attempt
│   ├── old_proposals/                 # early design proposals + baseline extractions
│   └── example_skill_redox/           # redox-extraction sibling skill
│
└── _to_delete/                        # files staged for deletion
```

The Trial-3 and Trial-4 directories sit at the project root rather than under `trials/` because of how those runs were dispatched. Trial-5 and Trial-6 went into the canonical `trials/trialN/` layout.

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
3. Tag releases by skill version, not by trial. The current release is **v1.7** (`mp-bp-extraction/dist/mp-bp-extraction.skill`). v1.7 is validated on T5 (99.7 % Tier-1 correctness, 2,063 rows on the 168-paper journal corpus) and T6 (99.3 % correctness, 15,741 rows on the CRC Handbook 97th Edition). Any future revisions (v1.8 polish items below, or a generalization to other property types) should ship as a new tag.
4. The `recall_study/` directory contains paper enumeration JSONs but no PDF content — safe to commit.

## v1.8 polish items (not blocking)

Three small clarifications surfaced during Trial-6 (textbook extraction). None are blockers and none change behavior on existing trials:

- **`property: mp` / `bp` alias.** T6's CRC extraction collapsed `melting_point` / `boiling_point` to `mp` / `bp`. The skill could endorse the short form explicitly or instruct agents to use the long form. Currently undocumented either way.
- **Phase 0 manifest abstraction.** SKILL.md's manifest step mentions "paper-bearing locations". T6 demonstrated that the manifest unit is naturally "table sections of one PDF" rather than papers. A clarifying sentence ("the manifest unit is the natural unit of work for the corpus — papers, files, table sections, etc.") would generalize without changing existing trials.
- **Two new `_skipped.txt` reasons.** T6 used `dedup_with_S3` and `no_per_compound_mp_bp_row` outside the v1.7 taxonomy. Could be added formally.

See `reports/trial6_comparison_report.md` for the rationale.

## Where to look first for context

- **What is this project?** Read `development_report.md` sections 1–5 (problem statement → first attempt → architectural pivot → second attempt design).
- **What's the current state of the skill?** `mp-bp-extraction/SKILL.md`, then `CHANGELOG.md`.
- **How do you run / interpret a trial audit?** `audit_criteria.md` is the source of truth for what an audit measures (three-tier framework: Tier-1 correctness, Tier-2 verifiability, Tier-3 hygiene).
- **What's the most recent evidence?** `reports/trial5_comparison_report.md` (journal-paper corpus, v1.7) and `reports/trial6_comparison_report.md` (CRC Handbook textbook, v1.7).
- **What's the full per-trial evolution?** Read the trial reports in order: `trial2` → `trial3` → `trial4` → `trial5` → `trial6`.
- **What's planned next?** `development_report.md` section "What's next" — generalizing the skill to extract data types beyond melting/boiling point.
- **What are the publication-ready meta-lessons?** The "context shapes the result" failure family — three findings across six trials:
  - **Cross-model variability** (T2): same skill, three models, 98 % / 86 % / 55 %.
  - **Audit-rubric drift** (T3): two of the project's most striking numbers were rubric artifacts. Codified in `audit_criteria.md`.
  - **Cross-trial contamination** (T4): an agent silently dropped 17 % of the corpus by copying a prior trial's exclusion regex. Fixed by Phase 0 manifest + sandboxed dispatch.

## Audit-pass-rate summary across trials

| Trial | Source | Rows | Tier-1 Correctness | Tier-2 Verifiability |
|---|---|---:|---:|---:|
| T2 (v1.4) | 168 journal papers | 1,864 | 98.7 % | ~91.3 % |
| T3 (v1.5) | 168 journal papers | 1,352 | 97.0 % | ~97.0 % |
| T4 (v1.6) | 168 journal papers | 1,529 | 98.0 % | 95.7 % |
| T5 (v1.7) | 168 journal papers | 2,063 | 99.7 % | 99.7 % |
| T6 (v1.7) | CRC HCP textbook | 15,741 | 99.3 % | 99.7 % |

All audited under matched criteria from `audit_criteria.md`, 300-row uniform-random samples per trial, 12 fresh-context Claude verifier agents in parallel.

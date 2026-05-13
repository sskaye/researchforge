# Held-out corpus annotation process

This document defines the operational process for building ground-truth
annotations on the held-out corpus used in Phase 6.5 and § 12.5 of the
merged proposal. Without a defined process the 98 % held-out target is
not operationalizable.

## Why this matters

The held-out corpus is **the actual precision measurement** for the
skill. The dev corpus (`mp_bp_dev_set`) is what the gates were tuned
against; it can produce a misleadingly high pass rate. The held-out
corpus tests whether the gates generalize.

A bad annotation process invalidates the measurement in two ways:
1. **Bad ground truth → silent false negatives**. The verifier
   correctly says a row matches the paper, but the annotator's
   expected output says otherwise — the row is wrongly quarantined.
2. **Annotator drift over time**. Different annotators, different
   sessions, different conventions → annotations no longer comparable.

## Roles

- **Annotator**: produces the per-paper expected output. Should have
  enough chemistry background to read a synthesis section, recognize
  property values, and identify when a compound name is standalone.
  Minimum bar: a chemistry undergraduate who has done a synthesis
  lab. Better: a research chemist.
- **Adjudicator**: resolves disagreements between annotators. Should
  be more senior than the annotators; same chemistry background.
- **Annotation lead**: defines the scope and conventions for a given
  property, owns the annotation guide, signs off on the locked
  ground truth for each paper.

A small build team can have one person play multiple roles, but
the **annotation and verification must be done by different people**
than the people who wrote the extractor's gates. Otherwise the
ground truth inherits the same blind spots as the extractor.

## Annotation workflow

For each paper:

1. **Pre-read** (5 min). Skim the abstract, section headings, and
   table captions. Note how many compounds are claimed and roughly
   where the property values appear.

2. **Per-paper annotation guide check** (1 min). Confirm any
   paper-specific conventions in `tests/held_out/<adapter>/notes/<paper>.md`.
   This file is created when needed during annotation (e.g., "Paper
   X uses pent-4-yn-1-yl when most papers use 4-pentynyl; use the
   paper's form").

3. **Per-row annotation** (30 sec to 5 min per row depending on
   complexity). For every claimed compound + value pair, fill in
   the same schema the extractor uses:
   - `compound_name` (the canonical, standalone form — NOT necessarily
     verbatim from the paper)
   - `compound_label` (paper-local code, if any)
   - `property_name`, `property_subtype`
   - `value_canonical`, `_min`, `_max`, `canonical_unit`
   - `value_original`, `unit_original`, `relation`
   - `data_origin`
   - `instrument`
   - `compound_evidence_text`, `compound_evidence_type`
   - `property_evidence_text`, `property_evidence_type`
   - `evidence_location`
   - `source_section`
   - `doi`
   - `notes` (free text, only for unusual cases)

4. **Verify each row** (the annotator is also the verifier here).
   Apply the six verification questions from
   `reference/verifier_prompt.md`. If any answers "Cannot determine",
   the row is omitted from the expected output with `omit_reason`.

5. **Output**: one file per paper at
   `tests/held_out/<adapter>/<paper_id>.expected.csv`. Same schema
   as the production output CSV.

## What the annotator does NOT do

- Does not run the skill on the paper. Annotations are produced
  independently.
- Does not consult the skill's intermediate outputs (candidate
  index, label dictionary, etc.).
- Does not refer to the dev-corpus expected outputs except for
  schema reference.

## Disagreement-resolution protocol

To detect annotator drift and improve ground-truth quality:

- **Sample size**: 20 % of held-out papers are annotated by **two
  independent annotators**. The other 80 % are single-annotator.
- **Agreement metric**: for the double-annotated subset, compute
  row-level agreement on (compound_name, property_name, property_subtype,
  value_canonical ±0.5, data_origin). Field-level agreement on
  each per matched row.
- **Threshold for resolved-by-adjudication**: any pair of annotations
  with row-level agreement < 95 % goes to the adjudicator.
- **Adjudication output**: the adjudicator produces the final
  expected CSV. The disagreement is recorded in
  `tests/held_out/<adapter>/notes/<paper>_adjudication.md` for
  process improvement (the disagreement may indicate an ambiguous
  case the gates also struggle with).

## "Qualified annotator"

Operational definition (minimum):

- Chemistry undergraduate degree or equivalent self-study.
- Has done a wet-lab synthesis (can read a synthesis paragraph).
- Can recognize functional-group names from IUPAC names.
- Comfortable reading scientific PDFs / tables.
- Has annotated a "training paper" (a known dev-corpus paper) and
  agreed with the locked expected output to within 95 % row-level
  agreement before working on real held-out papers.

The "training paper" check is the calibration. Any new annotator
spends their first day on already-annotated dev papers, comparing
their output to the locked dev expected. If they hit 95 %
agreement they are cleared to annotate held-out papers; otherwise
they spend more time on training papers, get adjudicator feedback,
and try again.

## Ground-truth file format

```
tests/
└── held_out/
    └── <adapter>/                   # e.g., mp_bp/
        ├── <paper_id_1>.expected.csv
        ├── <paper_id_2>.expected.csv
        ├── …
        ├── notes/                   # only when needed
        │   ├── <paper_id_1>.md
        │   └── <paper_id_3>_adjudication.md
        └── manifest.json            # holds annotator ids, dates,
                                     # adjudication status per paper
```

`manifest.json`:

```json
{
  "adapter": "mp_bp",
  "lock_date": "YYYY-MM-DD",
  "papers": {
    "<paper_id>": {
      "annotators": ["A_id"],          # one or two ids
      "adjudicator": null,             # or adjudicator id if needed
      "annotation_date": "YYYY-MM-DD",
      "row_count": N,
      "training_agreement": 0.97,      # if double-annotated
      "locked": true
    }
  }
}
```

Once `locked: true`, the expected file is immutable. Updates require
a new lock date and a re-evaluation of any past pass-rate measurements
against the changed ground truth (the old measurements are not
invalidated, but they should be recomputed if the expected file
changes substantively).

## Operational risks and mitigations

- **Cost**: a 30-paper held-out corpus at 30 min/paper = 15 hours of
  annotation, plus the double-annotation overhead. Plan for ~20-25
  annotator-hours total before Phase 6.5 can run.
- **Annotator burnout / drift**: limit annotation sessions to 90
  minutes. Insert random training papers periodically to spot drift.
- **Annotator-extractor entanglement**: if the annotator is also the
  build engineer, they will unconsciously match their own extractor's
  decisions. Mitigate by using a different person, or by annotating
  before the gates are finalized.
- **Updates to held-out ground truth invalidate past pass rates**:
  this is a real cost. Once held-out is locked, only add new papers,
  don't change existing ones except to fix annotation errors
  (recorded in adjudication notes).

## Minimal viable v1

If full process is too heavy at the start, the minimum is:

1. **One annotator** per paper, lead reviews 100% (lead is the
   adjudicator).
2. **No double annotation** for the first held-out batch (the
   build is at low scale; adjudication overhead exceeds benefit).
3. **One training paper** the annotator must hit 95 % on before
   producing held-out annotations.

Add the double-annotation protocol after the first held-out run
when you have a baseline.

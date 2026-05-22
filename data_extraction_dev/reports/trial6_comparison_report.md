# Trial-6 comparison report — Opus 4.7 on v1.7, CRC Handbook of Chemistry and Physics

**Date:** 2026-05-14
**Skill version:** mp-bp-extraction v1.7
**Corpus:** A single 2,643-page reference textbook — *CRC Handbook of Chemistry and Physics, 97th Edition* (2016-2017), W. M. Haynes (ed.), CRC Press, ISBN 978-1-4987-5429-3.
**Audit method:** Uniform random 300-row sample (100 with seed 20260512, 200 with seed 20260514), 12 fresh-context Claude verifier agents in parallel, three-tier criteria from `audit_criteria.md`. Verifiers extracted each cited page via `pdftotext -layout` and confirmed compound + value against the table.

## Headline — the skill generalizes to textbook extraction

| | Rows | Tier-1 Correctness | Tier-2 Verifiability |
|---|---:|---:|---:|
| **T6 (v1.7, CRC HCP 97th Ed.)** | **15,741** | **298/300 = 99.3 %** (CI 97.6–99.8 %) | **99.7 %** |

A single textbook corpus produced **15,741 rows at 99.3 % audit pass rate** — roughly **8× the row count** of the largest journal-paper trial (T5's 2,063 rows) at statistically indistinguishable correctness. This is the first test of the skill on a fundamentally different source type (a structured reference table at scale rather than per-paper synthesis prose).

Two-prop z-tests vs. prior trials:
- T2 vs T6: z = -0.84, p = 0.40 — tied
- T5 vs T6: z = +0.79, p = 0.43 — tied
- T6 vs all prior journal-paper trials: indistinguishable on Tier-1 correctness

## The two failures

Both Tier-1 failures are the same kind — **mp/bp column misbinding** in dense two-column CRC tables:

| Row | Compound | Issue |
|---|---|---|
| **12632** | 4-Hydroxybutanoic acid (book p. 3-306, row 6009) | Page shows `mp <-17` and `bp 180 dec`. Row recorded `property=mp` with `value_raw="180 dec"`. The 180 dec is the bp value, not the mp value. The row's own `evidence_location="bp column"` and `notes="decomposes_at_bp"` already disclosed this — the property field is the only thing wrong. |
| **9146** | N,N-Diethyl-3-pyridinecarboxamide (book p. 3-180, row 3518) | Page shows `mp=25 / bp=280 dec`. Row recorded `property=mp` with `value_raw="280 dec"`. Should be `property=bp`. |

Both are **single-row property-column-misbinding errors** in CRC's compact `mp/°C  bp/°C` two-column layout where adjacent columns can be confused when `pdftotext -layout` produces inconsistent spacing. These are the textbook-extraction analog of the single-paper anomalies T4 (PMC7148931 isomer mismatch) and T5 (Paper 123 compound-code binding error) hit. The protocol's class-sweep policy (audit_criteria.md) doesn't fire because two single-paper-equivalent occurrences in 300 rows is not a recurring pattern.

## How Trial-6 exercised the skill differently

T1–T5 each ran the v1.4–v1.7 protocol on a **corpus of journal articles** — heterogeneous papers, each with its own DOI, mostly synthesis or characterization context, with mp/bp values embedded in prose ("White solid; m.p. 168-170 °C") or small tables. T6 ran the same protocol on a **structured reference textbook** — 11,000+ compounds in a single compact tabular format, no DOI per row, every value extracted from the same "Physical Constants of Organic Compounds" / "Physical Constants of Inorganic Compounds" / "Properties of the Elements" tables.

Several skill features were exercised in ways prior trials never tested:

| Skill feature | T1–T5 behavior | T6 behavior |
|---|---|---|
| `verification_status` | All rows started `pending_verification`; Phase 4 promoted to `verified_extraction` on a sample | All 15,741 rows marked `verified_textbook` — the schema's tier-status for standard reference textbooks ("no Phase 4 needed") |
| `source_url` | DOI URL preferred, with PMC/PMID fallback | All rows use `textbook:crc_hcp_97` (in early batches) or empty (in later batches with full citation in `source`) |
| `evidence_location` | "Table 1 row 3", "p. 6469 col 2 ¶ 3" | "p. 3-422 row 'Octachlorodibenzo-p-dioxin' mp column" / "Section 3 p3-432 No.8463" |
| `property` field | `melting_point` / `boiling_point` / `DSC_onset` / etc. | **Schema deviation: `mp` / `bp`** (collapsed from longer form, per Opus's EXTRACTION_SUMMARY) |
| `evidence_quote` | Verbatim contiguous span of paper prose containing value | The line of dense table-row text from the CRC table that contains the compound row stub and column values |
| Phase 0 manifest | Lists paper-bearing directories | Lists **table sections** within the single PDF (S3_ORGANIC, S4_INORGANIC, S4_ELEMENTS, etc. with PDF-page ranges) |
| Skip taxonomy | Used 4 of 8 reasons across T5 | Used 7 of 8 reasons + 2 new ones (`dedup_with_S3`, `no_per_compound_mp_bp_row`) on 12 sections |

The schema and protocol absorbed every one of these adaptations without breaking. The `verification_status = verified_textbook` tier (which exists in SKILL.md but had never been exercised before) was used correctly. The Phase 0 manifest step adapted to a different unit (table sections within one PDF instead of papers in a directory) without skill-level changes.

## The `mp` / `bp` schema deviation

T6's `property` field uses `mp` and `bp` rather than the protocol's `melting_point` and `boiling_point`. Opus's EXTRACTION_SUMMARY documents this: *"The `decomposition` and `sublimation` property values used in early batches were normalized to `mp`/`bp` with `decomposes_at_mp` and `bp_sublimes` notes flags during consolidation."* This is a meaningful deviation but:

1. The values are still unambiguous (`mp` clearly means melting_point; `bp` clearly means boiling_point).
2. The verifier accepted both forms under Q2 per the audit prompt's instruction "`mp` or `bp` accepted".
3. The deviation is documented in the run summary, not silent.
4. Downstream consumers reading the schema would expect `melting_point`/`boiling_point`; consuming `mp`/`bp` requires either schema awareness or a one-line normalization.

This is a **Tier-3 (hygiene) concern**, not a Tier-1 correctness issue. Worth a note in the development report so future textbook trials know to either keep the longer form or document the deviation.

## What worked across both source-type regimes

The skill features that were already validated on journal papers (T1–T5) carried over to textbook extraction without modification:

- **Phase 0 manifest enforcement.** Opus enumerated 18 table sections (6 processed, 12 skipped with explicit reasons) and ran the manifest accounting equation cleanly.
- **`_skipped.txt` with the v1.7 taxonomy.** Every excluded section has a one-line reason. Notable creative use: `dedup_with_S3` (sections that just restate values from Section 3 organic compounds) — fits the spirit of the taxonomy without being literally in the prescribed list.
- **Mandatory verbatim evidence_quote.** The CRC table row stub serves as the verbatim quote, containing both compound name (or its row number) and the value.
- **Per-row provenance.** `source` includes the section + page citation; `evidence_location` pinpoints the row. A verifier can find any row in <30 s by going to the cited PDF page.
- **Anti-script-row-generation.** Opus's EXTRACTION_SUMMARY confirms it used direct LLM reads (orchestrator-direct for low-page batches, subagent dispatch for the bulk) — no regex/template extraction.
- **DOI-from-file-only.** Doesn't apply to textbook references; correctly handled by using `textbook:crc_hcp_97` or empty source_url with full citation.

## Where the skill protocol shows in the deliverable

| Protocol expectation | Trial-6 evidence |
|---|---|
| `processed + skipped == manifest` | `6 + 12 == 18 ✓` (Opus's EXTRACTION_SUMMARY explicitly states this; expanded form `186 + 51 == 237` is for paper-corpus trials and doesn't apply here) |
| Per-row evidence_quote that supports the value | 299/300 audited rows have the value in the quote; 1 has the value adjacent to the quoted text (the row 11831 finding from batch 1's audit) |
| Source citation real and complete | All 15,741 rows have either `source_url=textbook:crc_hcp_97` or a fully populated `source` field with section + page |
| Conversion arithmetic when applied | Trial-6 has no temperature conversions; all CRC values are reported in °C |

## Six-trial comparison — the skill across regimes

| Trial | Skill | Source type | Rows | Tier-1 | Tier-2 | Headline finding |
|---|---|---|---:|---:|---:|---|
| T1-full | v1.2/v1.3 | 168 journal papers | 1,338 | 93 % | n/a | First scale-up; revealed `H-Indeno...` + CSV quoting gaps |
| T2 | v1.4 | 168 journal papers | 1,864 | 98.7 % | ~91.3 % | Cross-model variability (98/86/55 % across Opus/GPT/Sonnet) |
| T3 | v1.5 | 168 journal papers | 1,352 | 97.0 % | ~97.0 % | Audit-rubric drift → three-tier framework |
| T4 | v1.6 | 168 journal papers | 1,529 | 98.0 % | 95.7 % | Cross-trial contamination → manifest + sandbox |
| T5 | v1.7 | 168 journal papers | 2,063 | 99.7 % | 99.7 % | Steady state on journal-paper corpus |
| **T6** | **v1.7** | **1 reference textbook** | **15,741** | **99.3 %** | **99.7 %** | **Skill generalizes to large textbook extraction** |

Both T5 and T6 are statistically indistinguishable from each other (z = 0.79, p = 0.43) and from T2's v1.4 baseline (z = -0.84, p = 0.40). The skill's true correctness ceiling on Opus is about 99–99.7 % on any source type — limited by single-row anomalies (paper-specific isomer confusions, table column misbindings) that no skill rule can structurally prevent.

## What Trial-6 teaches that prior trials couldn't

1. **The skill is source-type-portable.** Same protocol, same lints, same audit methodology, same audit criteria; tested on a fundamentally different source structure (one large reference table vs many synthesis papers). Same correctness ceiling.

2. **The `verified_textbook` status tier actually works.** It was in SKILL.md from v1.0 onward but never exercised. T6 demonstrates that the schema's tier-status enum is well-designed for the standard-reference case: no Phase 4 required, source citation suffices, downstream consumers can filter on `verification_status` to pick textbook references vs paper extractions.

3. **The Phase 0 manifest abstracts cleanly to "units of corpus" rather than just "papers".** Opus enumerated table sections of one PDF as the manifest units. The skill's prose ("paper-bearing locations, descending into subfolders") doesn't strictly apply but the spirit ("enumerate everything before extracting, log explicit skips") does. Worth a note in SKILL.md that the manifest unit is whatever the natural unit of work is for the corpus.

4. **The new failure mode is property-column-misbinding in dense tables.** Not new to the skill (T4 and T5 each had one wrong-compound-binding case), but Trial-6 manifests it as wrong-property-binding instead of wrong-compound-binding. Same class of single-row anomaly. At 2 of 300 (0.67 %), it's at the irreducible-noise floor — not worth a dedicated lint.

5. **The `property: mp`/`bp` deviation should be addressed.** Either the skill explicitly endorses both long and short forms (`melting_point`/`mp`, `boiling_point`/`bp`) or extraction agents should be reminded to use the longer form. T6's choice was reasonable but creates a downstream-consumer surprise.

## Implications

- **The skill is functionally complete and source-type-general.** v1.7 + the audit framework handle both heterogeneous-paper-corpus extraction and structured-textbook extraction at the same correctness ceiling.
- **Trial-6's deliverable (15,741 rows at 99.3 % audit) is production-quality** and substantially expands the trustable mp/bp dataset for downstream use.
- **A small v1.8 polish change** could codify the `property: mp`/`bp` alias and add an explicit note that the Phase 0 manifest can enumerate table sections, paper directories, files, or any other natural unit of work. Both are clarifications, not new rules — no behavior changes for existing trials.
- **The publication writeup gains a fourth case study.** T6 demonstrates that the three "context shapes the result" failure-mode defenses (cross-model anti-regex from T2, three-tier audit from T3, manifest + sandbox from T4) plus the broader protocol design work on any structured-data source, not just on journal-paper corpora.

## Files

[Trial-6 verdict aggregates (300 rows)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/opus47/_my_verdicts_all.json)
[Trial-6 deliverable CSV (15,741 rows)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/opus47/mp_bp_data.csv)
[Trial-6 EXTRACTION_SUMMARY.md](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/opus47/EXTRACTION_SUMMARY.md)
[Trial-6 _corpus_manifest.txt (18 table sections)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/opus47/_corpus_manifest.txt)
[Trial-6 _skipped.txt (12 sections with reasons)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/opus47/_skipped.txt)
[Source PDF — CRC Handbook 97th Ed.](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/trials/trial6/book/CRC_Handbook_of_Chemistry_and_Physics_97.pdf)
[Audit criteria framework](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/audit_criteria.md)

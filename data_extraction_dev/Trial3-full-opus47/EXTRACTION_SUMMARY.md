# mp/bp extraction — Trial3-full-opus47

Extraction run produced by Claude (Opus 4.7) following the mp-bp-extraction skill protocol against `corpora/full_168` (202 entries: 168 PMC paper subdirectories + ~16 individual older PDFs + 18 review-file artifacts + 4 category sub-folders that were not descended into).

## Output

| File | Description |
|---|---|
| `mp_bp_full_168.csv` | The deliverable — 1,352 mp/bp/decomposition/sublimation rows with evidence-locked quotes. |
| `phase4_sample.csv` | Random sample of 100 rows used for independent verification. |
| `phase4_verdicts_part_{1..4}.json` | Per-row verifier verdicts from 4 parallel fresh-context agents. |
| `batch_{00..07}.csv` + `batch_{00..07}_log.md` | Per-batch extraction outputs and per-paper logs. |
| `url_to_folder.json` | Map from `source_url` → paper subdirectory, used by Phase 4 verifiers. |

## Coverage

- **Papers attempted**: ~190 individual papers across 8 extraction batches (26+26+26+26+26+26+19+16 = 191 paper-equivalents; the 4 category sub-folders `materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals` at the corpus tail were left to the parallel agent and not descended into in this run).
- **Papers contributing ≥1 row**: 136 unique `source_url` values.
- **Papers yielding zero rows**: ~50, almost all because the paper had no measurable mp/bp data (DFT/biology/review papers, polymer Tm without identifiable compound names, or paper-local bare-code identifiers like `compound 4a-l` with no IUPAC names).

## Row counts

| Field | Count |
|---|---|
| Total rows | 1,352 |
| `property = melting_point` | 1,260 |
| `property = decomposition` | 78 |
| `property = boiling_point` | 13 |
| `property = sublimation` | 1 |
| `data_type = measured` | 1,349 |
| `data_type = calculated` | 3 |

## Verification status

| Status | Count | Notes |
|---|---|---|
| `verified_extraction` | 97 | Passed Phase 4 independent agent verification. |
| `flagged_review` | 5 | 3 from Phase 4 (`flagged_compound_mismatch` ×1, `flagged_evidence_quote_not_found` ×2 — both PDF column-splice in batch_07); 2 source-typo unbalanced brackets in compound names (paper PMC6147013, preserved verbatim with note). |
| `pending_verification` | 1,250 | Outside the 100-row Phase 4 sample. |

**Phase 4 audit pass rate: 97/100 = 97.0 %** on a uniform random sample drawn with `random.seed(42)`.

## Methodology

The skill protocol was applied as specified:

1. **Source preparation** — each paper read directly (article.nxml preferred, then article_text.txt, then `pdftotext -layout` on article.pdf). DOIs / PMC IDs / PMIDs were taken only from substrings of the paper file's own text; none were guessed from training memory.
2. **Evidence-locked extraction** — eight parallel general-purpose Claude agents handled ~26 papers each. Each agent emitted one row per (compound × property × value) with a mandatory contiguous verbatim `evidence_quote` containing both the compound name (or its label/code such as `4f`) and the printed value.
3. **Phase 3 deterministic checks** — `run_all_checks.py` was run on the merged CSV. Hard failures fixed: 5 rows dropped (bare codes and a quote that didn't contain its value), 2 rows downgraded to `flagged_review` (source-typo unbalanced brackets), 1 row's `value_raw` corrected from a single value to the printed range. Final Phase 3 state: all hard checks pass; the 2 unbalanced-bracket rows are honestly flagged.
4. **Phase 4 independent verification** — a 100-row sample (`max(100, 5 % × 1,250)` = 100) was split into 4 batches of 25 and verified by 4 fresh-context general-purpose Claude agents that had no access to the extraction notes. Verdicts were merged back into the main CSV.
5. **Phase 5 confidence tagging** — `verification_status` reflects each row's audit state. Granular flag reasons are recorded in `notes`.

### Class sweep (Phase 4 follow-up)

Both `flagged_evidence_quote_not_found` failures came from older raw-PDF papers in batch_07 (DOIs `10.3762/bjoc.15.258` and `10.1021/acs.joc.9b00711`) where `pdftotext -layout` interleaved column text or a page number between fragments the extractor had concatenated into one quote. The deterministic `verify_evidence_quote.py` lint did not catch these because the substring is in fact present in one of the `pdftotext` output modes — the verifier was reading more strictly than the script. Rows from these two papers are highlighted as candidates for closer review if the dataset is used downstream; the rest of the batch_07 rows (Sharik 2006, Maginn 2012, Zhou 2013, Schmittel 2014, Marek 2019, Moncho 2021) were not implicated by the sample.

## Known limitations

- **Older raw-PDF papers (batch_07)** are over-represented in the 3 % failed-audit population. Their two-column PDF layout sometimes splices adjacent-column text into the `pdftotext` output, which the extractor occasionally captured as a contiguous span when it should not have been.
- **Category sub-folders not descended** — `materials_inorganic`, `measurement_prediction`, `organic_synthesis`, `pharma_cocrystals` at the corpus tail each contain ~10–15 additional PDFs that were not extracted. A second pass could cover them.
- **Calculated values are scarce (3 rows)** — most papers in the corpus are synthesis / characterization studies that report measured mp values; the QSPR / prediction studies were either skipped by the extractor (when they only compile values from cited primary references — see batch_07 log) or covered narrowly.
- **DOI substring check** does not fire on most older PDFs because their DOI is not present as substring text inside the PDF; this is a known limitation of the file format, not the extraction.

## Reproducing the audit

```bash
cd /path/to/data_extraction_dev
# Phase 3 deterministic checks (all hard checks pass)
python3 mp-bp-extraction/scripts/run_all_checks.py \
    Trial3-full-opus47/mp_bp_full_168.csv

# Phase 4 verifiers were dispatched as 4 parallel general-purpose agents
# each handling 25 rows of phase4_sample_part_{1..4}.csv against the
# corpus. Verdicts are saved as phase4_verdicts_part_{1..4}.json.
```

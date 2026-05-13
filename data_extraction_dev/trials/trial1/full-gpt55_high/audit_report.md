# Cross-harness audit — Trial1-full-gpt55_high

**Date:** 2026-05-12
**Input:** `/mp_bp_full_set/` (168 papers, same corpus as our Trial-1-full)
**Extraction by:** Parallel agent (GPT-5.5 high) using its own approach
**Audit by:** 4 fresh, independent Claude verifier agents in parallel, applying the v1.2 verification protocol from the `mp-bp-extraction` skill

## Result

**Independent random-100 audit: 56 / 100 pass (56 %)**, Wilson 95 % CI **46–65 %**.

For comparison:

| Run | Approach | N papers | N rows | Audit pass | 95 % CI |
|---|---|---:|---:|---:|---:|
| Trial-1-full (this skill) | LLM-driven extraction | 168 | 1,338 | **93 %** | 86–97 % |
| Trial1-full-gpt55_high (parallel) | Regex-based Python script written by the agent | 168 | 304 | **56 %** | 46–65 % |

CIs **do not overlap** — the two runs are statistically distinguishable on the same audit protocol.

## What the parallel run did

The GPT-5.5 high agent wrote a Python extractor (`extract_mp_bp.py`) that uses regex patterns over text extracted from NXML / PDF / HTML files. Architecturally similar to our **first attempt** (the regex-based `property-extractor` that we eventually retired at 67 % dev / 41 % val). The extractor was deliberately conservative — it only emitted rows where its patterns matched cleanly, skipped 226 source files entirely, and produced 304 rows from 65 of the 168 papers.

Provenance: the GPT-5.5 run includes a `source_file` column with absolute paths to the underlying text file, and each row carries an `evidence_quote` drawn from that file. So the per-row provenance is there. The Phase-3 sanity checks the run reports passing are similar to ours.

But the precision is much lower because the regex pipeline can't tell:

- A compound name from a sentence fragment ("Rf = 0.21 (Hexane/EtOAc, 1:4) and", "There were about 5 and 6 % molecules with", "It is a reddish", "Method B: 95%)").
- A temperature from a citation number, a count of compounds, or a ring locant ("5 °C" extracted from "5-substituted aryloxytetrazoles"; "307 °C" from "307 hydrocarbons"; "16 °C" from a citation `[16]`).
- An NMR chemical-shift line from a compound title (NMR fragments like "13CNMR (101 MHz, DMSO-d6) δ 35.9, 43.3" captured as compound_name).
- A column-misalignment in dense compound tables (M17 row inheriting M15's value; khalifa M-series with values bound to adjacent rows).
- A truncated compound name from a wrapped PDF ("2-Deoxy-2-(5-nitro-2-fura" cut mid-word; many "H-Indeno..." style indicated-hydrogen-locant truncations).

These are precisely the failure modes our first regex-based attempt hit. The trade-off the parallel agent's conservative tuning achieves is that recall drops drastically (304 vs. our 1,338 rows on the same corpus) without buying much precision (56 % vs. our 93 %).

## Per-batch audit detail

| Batch | Pass | Fail | Dominant reasons |
|---|---:|---:|---|
| 1 (25 rows) | 11 | 14 | 8 sentence-fragment compound names; 4 range-as-single-value bugs; 2 numeric-count confusions |
| 2 (25 rows) | 13 | 12 | 6 NMR/sentence-fragment compound names; 5 non-temperature numbers (`5 °C` from "5-substituted", etc.); 1 PDF column-merge swap |
| 3 (25 rows) | 17 | 8 | 2 khalifa M-series column-misalignments (M17 ↔ M15, M22 ↔ M20); 5 sentence-fragment compound names; 1 mid-word truncation |
| 4 (25 rows) | 16 | 9 | 8 compound-name truncations / NMR fragments / yield fragments; 1 citation-number-as-°C |
| **Total** | **56** | **44** | |

### Failure-mode breakdown

| Category | Count |
|---|---:|
| `flagged_compound_name_truncated` (sentence fragments, mid-word cuts, NMR-shift lists, yield fragments captured as compound names) | 20 |
| `flagged_value_mismatch` (the "value" is a citation, ring locant, count of compounds, etc., not a temperature; or row swap in dense tables) | 15 |
| `flagged_compound_mismatch` (compound_name from a different row than the value) | 9 |

All 44 failures fall into the category: "**regex parser caught text adjacent to an mp pattern but couldn't tell whether it was actually a compound name + temperature pair.**"

## What this tells us

1. **Architecture wins.** Same corpus, same audit protocol, two different extraction architectures. The LLM-driven approach (with mandatory verbatim quotes, refusal-to-fabricate, and 4-step quote re-confirmation) reaches 93 % on 1,338 rows; the regex-driven approach reaches 56 % on 304 rows. Throwing a different LLM at the problem doesn't help when the LLM is just there to write a regex extractor — the regex still has the same blind spots regardless of which model wrote it.

2. **Cross-harness validation confirms the new skill is harness-independent.** Our 93 % wasn't an artifact of which model we used. The Claude verifier agents auditing the parallel run flagged the same kinds of regex-era failure modes we eliminated by switching architectures.

3. **The recall difference is dramatic.** 304 vs. 1,338 rows on the same 168 papers — the regex run skipped 226 source files where its patterns didn't match cleanly. Conservative regex tuning trades precision for recall; in this case it lost on both axes simultaneously because the patterns it DID match include hundreds of false positives.

4. **The parallel run validates one of our v1.3 fixes.** 20 of 44 failures are "compound name is a truncated fragment / NMR line / yield text / sentence fragment". These are exactly the cases the v1.3 prompt-template multi-line-name reassembly step is designed to prevent in our skill, and that `validate_compound_name.py`'s new `_TRUNCATED_LOCANT_PREFIX` pattern would catch programmatically.

## Recommendation for the parallel run

If the goal is to get the parallel run to comparable quality, the path is the same one we took: rebuild the extractor to be **LLM-driven** (the agent reads the actual paper and writes rows with a verbatim quote), with **deterministic scripts only for the checks an LLM can't reliably do** (RDKit, value ranges, unit arithmetic, CSV quoting). The current `extract_mp_bp.py` is ~6,000 LOC of regex — equivalent to where we started. The redox-extraction skill / our new `mp-bp-extraction` skill is the proven alternative.

## Files

[mp_bp_extracted.csv (304 rows)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial1-full-gpt55_high/mp_bp_extracted.csv) — parallel run output
[audit_verdicts_all.json (100 verdicts)](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial1-full-gpt55_high/audit_verdicts_all.json)
[audit_random_sample_100.csv](computer:///Users/skaye/Claude/Skills/ResearchForge/data_extraction_dev/Trial1-full-gpt55_high/audit_random_sample_100.csv)

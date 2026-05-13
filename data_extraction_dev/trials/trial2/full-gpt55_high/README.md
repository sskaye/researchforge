# Trial2 full GPT-5.5 high mp/bp extraction summary

Final CSV: `mp_bp_extracted.csv`

## Counts
- Rows: 907
- Verification statuses: {'pending_verification': 861, 'verified_extraction': 34, 'audit_corrected': 12}
- Properties: {'melting_point': 796, 'decomposition': 86, 'boiling_point': 10, 'DSC_peak': 9, 'sublimation': 1, 'DSC_onset': 5}
- Data types: {'measured': 905, 'calculated': 2}
- Rows from paired collection HTML/PDF papers: 86

## Validation
- Phase 3 deterministic checks: PASS (`phase3_run_all_checks.log`)
- Phase 4 independent sample audit: 40 rows sampled; 34 passed initially; 6 were flagged and then corrected or removed.
- Final flagged_review rows: 0

## Notes
- The final CSV keeps unaudited rows as `pending_verification`.
- Audited passing rows are `verified_extraction`.
- Rows corrected after Phase 4 or same-source follow-up are `audit_corrected` with details in `notes` and `phase4_audit_summary.json`.
- `phase3_paper_root_index/` is a checker-only index used so the bundled scripts can validate both ordinary paper directories and paired HTML/PDF collection papers.

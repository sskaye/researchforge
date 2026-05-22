# Phase 4 Verification Summary - Part 4

Verified 25 sampled rows from `phase4_sample_part_4.csv` against the supplied source files under `corpora/full_168` and `Trial3-full-gpt55_high`.

- Verified extractions: 17
- Flagged for review: 8

Flagged rows:

- Row 203: `flagged_value_mismatch` - source prints shorthand `233-35°C`; row `value_raw` is expanded to `233-235 °C`.
- Row 128: `flagged_compound_mismatch` - source context is gold(I) complex 11, not a platinum(II) complex.
- Row 172: `flagged_compound_name_truncated` - row omits the leading terpenyl substituent from the full compound 6 name.
- Row 365: `flagged_evidence_quote_not_found` - specified `paper_path` HTML does not contain the claimed Ag(AN)2(BF4) quote/value.
- Row 133: `flagged_compound_mismatch` - quoted value belongs to a different intermediate, compound 5.
- Row 293: `flagged_compound_mismatch` - row mixes stereochemistry/code: 26a is `(2S,4R,E)-...`, while `(2R,4R,E)-...` is 26b.
- Row 363: `flagged_evidence_quote_not_found` - specified `paper_path` HTML does not contain the claimed Ag(GN)2(BF4) quote/value.
- Row 154: `flagged_compound_mismatch` - quoted boiling point belongs to an aldimine from cyclohexylamine and butyraldehyde, not the named compound.

The final CSV was not edited.

# Data type: melting-point and boiling-point (mp/bp)

Single overlay file for the mp/bp data type. Property-specific schema,
worked examples, value ranges, conversions, candidate tokens, drop patterns,
skip reasons, and failure-mode catalog all live here. Use this file
alongside `SKILL.md` (generic protocol) and `references/COMMON_ERRORS.md`
(generic LLM-behavior anti-patterns and PDF-rendering pitfalls).

In v2.1 this overlay was consolidated from three files (`OVERLAY.md`,
`SCHEMA.md`, `COMMON_ERRORS.md`). Content that's generic to every data type
moved up to `SKILL.md` and `references/COMMON_ERRORS.md`. Everything that
remains here is genuinely mp/bp-specific.

## Properties extracted

This overlay covers six values for the row's `property` column:

| Value | Notes |
|---|---|
| `melting_point` | mp / m.p. / Tm / Tfus / "melting point". Default for unqualified "mp". |
| `boiling_point` | bp / b.p. / Tb / "boiling point". |
| `DSC_onset` | DSC onset temperature when the source explicitly labels it "DSC onset" (DSC technique, not TGA or other). |
| `DSC_peak` | DSC peak temperature when the source explicitly labels it "DSC peak". |
| `decomposition` | Decomposition temperature. Use whenever the paper labels the value with `decomp.`, `dec.`, "decomposes at", "decomposition onset", or describes the value as a TGA decomposition measurement. **Pick this over `melting_point` or `DSC_onset` whenever the paper's wording invokes decomposition.** |
| `sublimation` | Sublimation temperature when explicitly labeled. |

`melting_point` and `boiling_point` are distinct properties; the other four
are related thermal events that mp/bp papers frequently report alongside mp.

If the user asks for only one property (e.g., "only boiling points"),
restrict your emissions to that property value.

### Property-disambiguation table

Use this when the paper's wording is borderline. The right column is what
the row's `property` column should be set to:

| If the paper labels the value as ... | Set `property` to |
|---|---|
| `mp` / `m.p.` / `Tm` / `Tfus` / "melting point" | `melting_point` |
| `bp` / `b.p.` / `Tb` / "boiling point" | `boiling_point` |
| "DSC onset" (in a DSC trace) | `DSC_onset` |
| "DSC peak" (in a DSC trace) | `DSC_peak` |
| "onset of decomposition" / "decomposition onset" / "TGA onset" (TGA technique, even though "onset" appears in the text) | `decomposition` |
| `"X °C, decomp."` / `"dec. at X °C"` / `"decomposes at X °C"` | `decomposition` |
| "sublimes at X" / "sublimation at X" | `sublimation` |
| Bare value in an experimental block with no qualifier, on a per-compound characterization line | `melting_point` (default for the experimental-section pattern) |

The disambiguation rule that matters most: **the word "onset" alone does
not mean `DSC_onset`.** `DSC_onset` is specifically about the DSC technique.
A TGA-measured decomposition onset is `decomposition`, not `DSC_onset`.
Trial-7's row 163 ("onset of decomposition at 194.2 °C") was a TGA value
that got tagged `DSC_onset` by token-matching on "onset"; the correct
property is `decomposition`.

## Schema

The mp/bp overlay declares **zero extension columns**. Rows use the v2.1
generic 18-column schema from `SKILL.md` exactly:

- `compound_name` for the compound identity.
- `property` is one of the six values above.
- `value` is the temperature in °C (after any unit conversion).
- `value_min` / `value_max` populated when the source reports a range.
- `value_raw` is the value as printed in the source (e.g., `"188–190 °C"`,
  `"1655 K"`, `"−77.9 °C"`, `"200 °F"`).
- `units` is always `"°C"` for this overlay.
- `conversion_arithmetic` populated when the source's value was in K or °F
  (see "Unit conversions" below).

## Worked examples

Four example rows showing the cases that have historically caused
extraction confusion. The header line is the v2.1 18-column schema for
this overlay (no extension columns).

```csv
id,verification_status,compound_name,compound_smiles,property,value,value_min,value_max,value_raw,units,relation,meas_calc,source,source_url,evidence_location,evidence_quote,conversion_arithmetic,notes
```

**1. Ordinary mp from a synthesis paper's experimental section.**

```csv
1,pending_verification,3-phenylquinazoline-4(3H)-thione,,melting_point,189.0,188.0,190.0,"188–190 °C",°C,=,measured,"Molecules 2018, 23, 1212",https://doi.org/10.3390/molecules23051212,"Table 1 row 2a","2a: White solid, yield 67%, mp 188–190 °C",,
```

Note the quote captures the compound serial `2a:` followed by the
characterization line — both the compound identifier and the value land in
one verbatim contiguous span (Phase 2 Step 6 wins on the first try).

**2. K → °C conversion (paper reports in Kelvin).**

```csv
2,pending_verification,Camostat,,melting_point,219.328,,,492.478 K,°C,=,measured,"Thermodynamic properties of APIs, 2021","https://doi.org/10.0000/test1","Table 5 col 'Camostat | exp.' row 'Tm'","Camostat Tm = 492.478 K","492.478 K − 273.15 = 219.328 °C",
```

The `conversion_arithmetic` column uses the v2.1 standardized syntax (see
SKILL.md). Both unicode minus (`−`) and ASCII hyphen (`-`) are accepted as
input by the conversion-arithmetic lint, but new output should use unicode.

**3. Decomposition annotation → `property = decomposition` (NOT melting_point).**

```csv
3,pending_verification,Compound 10,,decomposition,260.0,,,"260 °C, decomp.",°C,=,measured,"J. Med. Chem. 2024, 67, 1234","https://doi.org/10.0000/test2","Table II row 10","Compound 10: ... 260 °C, decomp.",,decomp_temperature
```

The `decomp.` annotation in the cell makes this a decomposition row, not a
melting-point row, even though the value sits in the column labeled "M.p."
in the table header. The property reflects the underlying phenomenon, not
the column header.

**4. Value compiled from prior literature inside a QSPR / review paper.**

```csv
4,pending_verification,Alprenolol,,melting_point,108.0,,,108 °C,°C,=,measured,"AI-powered prediction of critical properties, 2024","https://doi.org/10.0000/this_paper","Table 1 row 'Alprenolol'","Alprenolol 108 °C [12]",,upstream_primary=Chu_Yalkowsky_2009
```

Critical: `source_url` is the DOI of the paper you are physically reading
(the QSPR / compilation paper that tabulates Alprenolol's mp), **not** the
DOI of the upstream primary measurement paper (Chu & Yalkowsky 2009) that
[12] cites. The upstream primary's DOI is irrelevant to `source_url`. If
you want to credit it, mention it in `notes`. This is the rule for every
compiled-literature value.

## Value ranges

| Property | Range | Notes |
|---|---|---|
| `melting_point` | [−275, 4500] °C | Helium (−272 °C at high pressure) through highest-melting refractory carbides. |
| `boiling_point` | [−275, 6500] °C | Helium (−269 °C) through rhenium/tungsten. |
| `DSC_onset`, `DSC_peak` | [−275, 4500] °C | Same range as mp. |
| `decomposition`, `sublimation` | [−275, 6500] °C | Wide; ranges aren't meaningful gates here. |

Enforced by `scripts/value_range_check.py`. A value outside the range is
almost always a parsing artifact — PDF sign-loss (`277.9` actually
`−77.9`), wrong unit not yet converted (K stored as °C), or a non-property
number captured by mistake.

## Unit conversions

mp/bp papers report in °C (most), K (thermodynamics papers, refractory
materials), or °F (older US references, some reference tables). For
non-°C sources, set `value` to the °C-converted result and populate
`conversion_arithmetic`:

- K → °C: `<X> K − 273.15 = <Y> °C`
- °F → °C: `(<X> °F − 32) × 5/9 = <Y> °C`

Numeric correctness enforced by `scripts/unit_conversion_arithmetic.py`.
Syntax shape enforced by the generic `scripts/conversion_arithmetic_lint.py`
in the skill root.

## Skip reasons specific to mp/bp

In addition to the six generic `_skipped.txt` reasons in `SKILL.md`'s
Phase 0 section, mp/bp papers can carry these reasons:

- `no_mp_bp_data_in_text` — paper has no mp / bp / DSC / decomposition /
  sublimation values at all.
- `tga_or_nmr_only_no_mp_bp` — characterization is exclusively TGA, NMR, or
  IR with no thermal-transition temperatures reported.

These extend rather than replace the generic vocabulary. If a paper has
some IUPAC-named compounds and some bare codes, the right action is to
emit rows for the named compounds and drop the bare-code rows individually
— NOT to mark the whole paper `bare_code_compounds_only`.

## Candidate-token list (Phase 1 step 5)

When scanning each paper for mp/bp candidate locations, search for these
tokens in tables, figures, and paragraphs:

`mp`, `m.p.`, `M.p.`, `melting point`, `Tm`, `Tfus`, `bp`, `b.p.`,
`boiling point`, `Tb`, `DSC onset`, `DSC peak`, `decomposition`,
`decomp.`, `dec.`, `decomposes at`, `sublimation`, `sublimes at`,
`thermal decomposition`, `TGA onset`.

Note page / table / figure numbers per region before extraction.

## mp/bp-specific drop patterns (per-row, NOT paper-level)

These patterns suggest a row should be dropped or rewritten. They apply
**per-row** — a paper containing one of these does not become a whole-paper
skip. (Paper-level skips are listed under "Skip reasons" above.)

### NMR / mass-spec context values mistaken for mp/bp

Numbers like `δ 130.31 ppm` (13C NMR), `m/z 268`, or `[M+H]+ 354.2` can
fall within plausible mp/bp ranges numerically but aren't temperature
measurements. The general "context numbers aren't property values" pattern
is in `references/COMMON_ERRORS.md`; what makes it mp/bp-specific is the
range overlap: 13C NMR shifts sit in the 0–200 ppm range, which is the
same as common organic melting points in °C.

**Drop signal:** the surrounding paragraph mentions `NMR`, `MS`, `m/z`,
`δ`, `13C`, `1H`, `HRMS`, or appears inside an NMR characterization
block.

### Workup solvents inside Rf-eluent annotations

`Rf = 0.3 (CH2Cl2:MeOH 95:5); mp 165 °C` — the mp 165 belongs to the
characterized product, not the eluent. Compounds named CH2Cl2, EtOAc,
MeOH, DMSO, DMF, THF (etc.) inside `Rf:` parens or eluent-list contexts
are virtually never the row's compound.

**Drop signal:** the candidate compound_name is a common workup solvent
abbreviation AND it appears in an Rf / eluent / column-chromatography
context.

### PDF sign-loss for small-organic mp range

`pdftotext` and similar PDF extractors sometimes render unicode minus
(`−`) as no character or as `2`. `−77.9 °C` (methanol freezing point)
can come out as `77.9 °C` or `277.9 °C`. The latter is out of range for
a small organic mp and the value-range check catches it; the former
silently inverts the sign.

**Drop signal:** a small-molecule organic with mp / bp dramatically out of
its expected family range. Especially: alcohols, simple ethers, and
hydrocarbons with reported mp > 200 °C should be sanity-checked against
known references.

## mp/bp-specific anti-patterns

- ❌ **"I'll extract this NMR shift, it looks like an mp value."** Read the
  surrounding sentence. NMR / MS / m/z values can land numerically in mp/bp
  range but are property-typed by their context, not by their value.

- ❌ **`mp =` / `m.p. =` tokens inside `compound_name`.** Patterns like
  `"1-(4-Chlorophenyl)ethanone, mp = 65 °C"` captured as the compound name
  are procedure-text leaking into the name field. v2.1 doesn't have a
  deterministic lint for this (it was removed when `validate_compound_name`
  became generic), so the agent must catch it at Phase 2 quote re-confirmation:
  if the compound name contains an `=` sign or a value-keyword token like
  `mp` / `bp` / `Tm`, the name is contaminated.

- ❌ **"260 °C, decomp." captured as `property = melting_point`.** When
  the cell carries an explicit `decomp.` annotation, the underlying
  phenomenon is decomposition, not melting. See the property-disambiguation
  table above and worked example #3.

- ❌ **Using the upstream primary's DOI as `source_url` for a compiled
  literature value.** The compilation paper's DOI is the right answer.
  See worked example #4 and `SKILL.md` Phase 1 step 2.

## Failure modes observed in past mp/bp trials

The generic patterns (NMR-as-value, PDF sign-loss, multi-row table
misalignment, etc.) and their generic descriptions live in
`references/COMMON_ERRORS.md`. This section catalogs the mp/bp-specific
instances of those patterns plus mp/bp-only failure modes.

### Adjacent-measurement quote (mp/bp instance of the generic "adjacent-quote" pattern)

**Trial-1-val row 147:** Methylcyclobutane, claimed `value_raw = "36.98 °C"`
(boiling point). The paper contains `"b.p. 36.98° (755 mm.)"` correctly,
but the agent recorded `evidence_quote = "f.p. -161.51"` (the freezing
point on an adjacent line). Compound, value, and source were all correct;
only the quote points at the wrong measurement.

Phase 2 Step 6 of `SKILL.md` requires confirming `value_raw` matches the
paper's printed value for this compound; this catches the failure.

### Doubled-token PDF artifact (mp/bp instance)

**Trial-1-val row 296:** Khalifa 2024 M7 compound, mp 257–260 °C. The
paper line was `"White powder, mp 257–260 °C"`, but `pdftotext -layout`
on the 2-column PDF produced `"White White powder, powder, mp"`. The
agent transcribed the doubled form.

Phase 2 Step 6 rejects doubled tokens; falling back to `pdftotext` without
`-layout` resolves the artifact.

### Quote stops before the value, 2-column PDF wrap (mp/bp instance)

**Trial-2 opus47 row 80:** Ethyl 2-(...) compound, value_raw = `"168-170 deg C"`,
evidence_quote = `"Dark red solid;"`. The full sentence was `"Dark red solid;
1.64 g, 86 % yield; m.p. 168-170 °С (toluene)."` The quote stopped at the
leading clause; everything after the semicolon (including the value) was
missed.

`quote_support_lint.py` (Tier 2 advisory) catches this. Phase 2 Step 6
should now bridge the wrap.

### NMR shift extracted as mp (mp/bp-specific)

**Predecessor paper 020 c00015:** value 130 came from the 13C NMR list
`δ 163.67 (C1, C3), 140.40 (C4'), 134.59 (C2'), 130.56 (C7a, C3a), 130.31 (C6, C5)`.
The agent saw `130.31` in plausible mp range and extracted it. Defense:
Phase 2 drop list above (NMR context).

### Workup solvent CH2Cl2 with adjacent mp value (mp/bp-specific)

**Predecessor paper 020 c00010:** `CH2Cl2` extracted as the compound, mp 165
attached. Real source line was an Rf annotation. Defense: Phase 2 drop
list above (workup solvents).

### Multi-row table thead — Chloroquine misbinding (mp/bp-specific)

**Predecessor paper 064 Table 5:** STRM / SIRM / [ref] sub-columns;
Chloroquine row's value was inherited from the adjacent Thalidomide row.
Defense: Phase 2 Step 6 (re-read row label); Phase 4 verifier re-reads
the table.

### PDF sign-loss on small alcohol mp (mp/bp-specific)

**Predecessor paper 2009_Dearden:** multiple Methanol / Benzene mp rows
where `−77.9 °C` rendered as `277.9 °C` in pdftotext output. Defense:
`value_range_check.py` flags 277.9 °C as out-of-range for a small
organic; Phase 4 verifier confirms the printed value.

### Truncated IUPAC name from PDF wrap (mp/bp-specific)

**Predecessor paper khalifa_2024_thiopyrimidine_sulfonamide:** 14 rows
captured names like `Cyano-6-Oxo-1,6-Dihydropyrimidin-2-yl` — a `-yl`
substituent, not a parent compound. Defense: `validate_compound_name.py`
flags trailing-substituent patterns; Phase 2 Step 7.5 multi-line
reassembly.

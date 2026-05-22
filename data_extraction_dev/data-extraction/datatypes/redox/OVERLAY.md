# Data type: redox potentials

Single overlay file for the redox data type. Property-specific schema,
worked examples, value ranges, conversions, candidate tokens, drop patterns,
skip reasons, and failure-mode catalog all live here. Use this file
alongside `SKILL.md` (generic protocol), `references/COMMON_ERRORS.md`
(generic LLM-behavior anti-patterns), and `datatypes/redox/REFERENCE_ELECTRODES.md`
(electrode-offset data table consulted by the conversion-arithmetic script).

This overlay was ported from the archived `_archive/example_skill_redox/`
skill in migration Step 10 (v2.0) and consolidated to a single overlay
file in v2.1.

## Properties extracted

This overlay covers four values for the row's `property` column:

| Value | Notes |
|---|---|
| `redox_potential` | Measured half-wave or formal potential, expressed in V vs SHE. |
| `formal_potential` | E°' / E_1/2 / midpoint of cathodic and anodic peaks. Use for typical CV mid-points. |
| `reduction_potential` | When source explicitly labels as reduction. |
| `oxidation_potential` | When source explicitly labels as oxidation. |

For simple cyclic-voltammetry mid-points, prefer `formal_potential`.

### Property-disambiguation table

| If the paper labels the value as ... | Set `property` to |
|---|---|
| `E_1/2` / `E1/2` / "half-wave potential" / "formal potential" / "E°'" | `formal_potential` |
| `E°` / `E0` (standard potential, single direction) | `redox_potential` |
| Single cathodic peak, no anodic return, paper explicitly labels reduction | `reduction_potential` |
| Single anodic peak labeled oxidation | `oxidation_potential` |
| Bare `E` with no qualifier in an electrochemistry table | `redox_potential` (most generic) |
| Two-electron couple's first reduction labeled `E1/2 (V2+/V+•)` | `formal_potential` (with disambiguation note in `notes`) |

## Schema

The redox overlay declares **four extension columns** beyond the v2.1
generic 18-column core:

| Extension column | Required? | Notes |
|---|---|---|
| `reference_electrode` | yes | The reference the measurement was made against (e.g., `Ag/AgCl 3M KCl`, `SCE`, `Fc/Fc+ (CH3CN)`, `SHE`). Required because the SHE conversion depends on it. |
| `solvent` | when present in source | Solvent the measurement was made in (`water`, `acetonitrile`, `DMF`, ...). Empty allowed for gas-phase or when source omits. |
| `ph` | when present in source | Numeric pH. Empty allowed for non-aqueous. |
| `n_electrons` | when reported | Number of electrons transferred. Often 1 for organics. Empty allowed when source doesn't say. |

The `value` column is the converted-to-SHE voltage (numeric). `units` is
always `"V vs SHE"` for this overlay. `value_raw` is the source's printed
value including the original reference electrode (e.g., `"+0.40 V vs SCE"`).

## Worked example

A fully-populated redox row with all 18 generic columns + 4 extension
columns:

```csv
id,verification_status,compound_name,compound_smiles,property,value,value_min,value_max,value_raw,units,relation,meas_calc,source,source_url,evidence_location,evidence_quote,conversion_arithmetic,notes,reference_electrode,solvent,ph,n_electrons
1,pending_verification,"9,10-anthraquinone-2,7-disulfonic acid",O=C1c2ccccc2C(=O)c2cc(S(=O)(=O)O)ccc21,formal_potential,-0.213,,,-0.45 V vs Ag/AgCl,V vs SHE,=,measured,"J. Am. Chem. Soc. 2017, 139, 9, 3438",https://doi.org/10.1021/jacs.6b13125,"Table 1 row 'AQDS' col 'E_1/2'","AQDS E_1/2 = −0.45 V vs Ag/AgCl (3M KCl)","-0.45 V vs Ag/AgCl(3M KCl) + 0.210 = -0.240 V vs SHE",,Ag/AgCl 3M KCl,water,7,2
```

Note the four extension columns sit at the end of the row, after the
generic 18 columns.

## Value ranges

Plausible voltage windows depend on the chemical class. The script
`scripts/voltage_range_check.py` encodes per-class windows (anthraquinones,
ferrocenes, viologens, TEMPO derivatives, etc.). A value outside its
class's window flags as `flagged_value_out_of_range`.

If the compound's class can't be determined, the script abstains rather
than flagging (avoids false positives for novel chemistries).

## Unit conversions

Reference-electrode conversion is mandatory when the source measured
against anything other than SHE. v2.1 standardized syntax (see `SKILL.md`):

- SCE → SHE: `+0.40 V vs SCE + 0.241 = +0.641 V vs SHE`
- Ag/AgCl 3M KCl → SHE: `-0.47 V vs Ag/AgCl(3M KCl) + 0.210 = -0.26 V vs SHE`
- Ag/AgCl saturated KCl → SHE: `-0.47 V vs Ag/AgCl(sat. KCl) + 0.197 = -0.27 V vs SHE`
- Fc/Fc+ in CH3CN → SHE: `+0.30 V vs Fc/Fc+ (CH3CN) + 0.40 = +0.70 V vs SHE`

Reference offsets are in `REFERENCE_ELECTRODES.md`.

Subtract-form (for absolute-scale / vacuum-referenced storage) is also
supported by `scripts/conversion_arithmetic.py`:

- `4.42 - 5.50 = -1.08 V vs SHE` (E_SHE = constant − raw)

## Skip reasons specific to redox

In addition to the six generic `_skipped.txt` reasons in `SKILL.md`'s
Phase 0 section, redox papers may carry these reasons:

- `no_redox_data_in_text` — paper has no electrochemistry section.
- `irreversible_no_reportable_e_half` — cyclic voltammetry too irreversible
  to give a defensible E_1/2 (only cathodic peak reported, no return).
- `ambiguous_reference_electrode` — paper doesn't say which reference
  electrode was used (common in older papers).
- `aprotic_aqueous_conflation` — source mixes aprotic and aqueous values
  without distinguishing.

## Candidate-token list (Phase 1 step 5)

When scanning each paper for redox candidate locations, search for these
tokens in tables, figures, and paragraphs:

`E_1/2`, `E1/2`, `E°`, `E0`, `formal potential`, `redox potential`,
`reduction potential`, `oxidation potential`, `half-wave potential`,
`cyclic voltammetry`, `CV`, `cathodic peak`, `anodic peak`, `E_pc`, `E_pa`,
`reference electrode`, `vs SHE`, `vs SCE`, `vs Ag/AgCl`, `vs Fc/Fc+`.

## Redox-specific drop patterns (per-row, NOT paper-level)

### Half-cell potentials where the reference electrode is not stated

Even when the value looks unambiguous, without a reference electrode the
value can't be converted to SHE. Drop the row.

### SCE-as-SHE conversion errors

A value labeled `vs SHE` but actually measured vs SCE without conversion.
The error is +0.241 V — within typical measurement scatter, so it doesn't
always look wrong by inspection.

**Drop signal:** the value's `reference_electrode` says `SHE` but the
paper's electrochemistry section describes the experimental setup with
SCE. Flag as `flagged_unit_conversion_error`.

### Methyl-viologen-couple ambiguity (V²⁺/V⁺• vs V⁺•/V⁰)

Methyl viologen has two reversible reductions about 350 mV apart. Papers
often report one without clearly labeling which.

**Drop signal:** `compound_name = methyl viologen` and the paper doesn't
explicitly specify the couple. Either include a disambiguation note in
`notes` (e.g., `notes = "first reduction V²⁺/V⁺•"`) or flag as
`flagged_compound_mismatch`.

### Aprotic-vs-aqueous conflation

Same compound has different potentials in different solvents (often by
100–500 mV). A row that doesn't specify `solvent` isn't fully
characterized.

**Drop signal:** the row's `solvent` is empty in a context where the
paper explicitly mentions a solvent. Re-extract.

### Ag/AgCl electrolyte ambiguity

The "Ag/AgCl" reference electrode has at least four common electrolyte
variants with different offsets. Without the electrolyte concentration,
the SHE conversion is underspecified.

**Drop signal:** `reference_electrode = "Ag/AgCl"` without electrolyte
specification (no "3M KCl", "saturated KCl", etc.). Re-extract from the
paper's experimental section to find the electrolyte.

## Redox-specific anti-patterns

- ❌ **Reporting a potential without specifying the reference electrode.**
  Generic Phase 1 requires citation; redox requires reference-electrode
  identification within the row.

- ❌ **Reporting an irreversible cathodic peak as `formal_potential`.**
  When the CV is irreversible (no anodic return), there's no defensible
  E_1/2. Either skip the row (with reason `irreversible_no_reportable_e_half`)
  or set `property = reduction_potential` with a `notes` mention of
  irreversibility.

- ❌ **Mixing aprotic and aqueous values for the same compound without
  the `solvent` column populated.**

## Failure modes observed in past redox trials

The generic patterns (NMR-as-value, PDF sign-loss, multi-row table
misalignment, etc.) live in `references/COMMON_ERRORS.md`. This section
covers redox-specific instances and redox-only failure modes.

### R1. SCE-as-SHE conversion errors

**Pattern:** Row's `value` is the source's printed value without
applying the SCE → SHE conversion. The +0.241 V error is within
typical measurement scatter for some couples.

**Prevention:** `reference_electrode` is a required extension column;
`scripts/conversion_arithmetic.py` checks that the offset matches the
declared electrode.

### R2. Methyl viologen couple ambiguity

**Pattern:** Two reversible reductions ~350 mV apart; papers often
report one without labeling which.

**Prevention:** Agent identifies the couple from context (anodic / cathodic
sweep range, paper's mention of `V²⁺/V⁺•` vs `V⁺•/V⁰`); flag if
ambiguous.

### R3. Aprotic-vs-aqueous conflation

**Pattern:** Same compound has different potentials in different
solvents. Rows that don't specify solvent are underspecified.

**Prevention:** `solvent` extension column populated when the paper
mentions a solvent; verifier checks against the experimental section.

### R4. Ag/AgCl electrolyte ambiguity

**Pattern:** "Ag/AgCl" reference has multiple electrolyte variants
(3M KCl, saturated KCl, 1M KCl, 1M NaCl) with different offsets.

| Electrolyte | Offset vs SHE |
|---|---|
| 3M KCl | +0.210 V |
| Saturated KCl | +0.197 V |
| 1M KCl | +0.235 V |
| 1M NaCl | +0.236 V |

13 mV gap between 3M KCl and saturated KCl matters for precise work.

**Prevention:** `reference_electrode` must specify the electrolyte
(e.g., `"Ag/AgCl 3M KCl"`, not `"Ag/AgCl"`). See
`REFERENCE_ELECTRODES.md` for the full table.

### R5. Irreversible CV reported as E_1/2

**Pattern:** Irreversible cyclic voltammogram (no anodic return) reported
as `formal_potential`. Some papers report only the cathodic peak; an
agent may capture this as if it were a reversible mid-point.

**Prevention:** If the paper reports only one peak with no return, the
row should either skip (`irreversible_no_reportable_e_half`) or specify
`property = reduction_potential` with `notes` mention of irreversibility.

### R6. Reference offsets vary with temperature and solvent

**Pattern:** Same as R4 but for non-Ag/AgCl electrodes. Fc/Fc+ offsets
depend strongly on solvent (0.40 V in CH3CN, 0.50 V in DMF, 0.56 V in
DMSO).

**Prevention:** `reference_electrode` should include solvent qualifier
when needed (e.g., `Fc/Fc+ (CH3CN)` not just `Fc/Fc+`).

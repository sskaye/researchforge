# Reference electrode conversions to SHE

All values in V at 25 °C unless noted. Conventions: add the offset to the reported potential to get vs SHE — i.e. `E_SHE = E_reported + offset`.

This table is kept in sync with `scripts/conversion_arithmetic.py`'s `KNOWN_OFFSETS` dict. If you need a reference not listed here, add it to both files.

## Aqueous

| Reference reported | Offset to SHE | Notes |
|---|---:|---|
| SHE / NHE | +0.000 | Conventional zero |
| SCE (saturated KCl) | +0.241 | Most common older lit; varies +/-2 mV with temperature |
| SCE (1 M KCl) | +0.283 | "Normal calomel"; rare |
| Ag/AgCl (saturated KCl) | +0.197 | Most common modern aqueous |
| Ag/AgCl (3 M KCl) | +0.210 | Common in commercial reference electrodes |
| Ag/AgCl (3 M NaCl) | +0.209 | |
| Ag/AgCl (1 M KCl) | +0.236 | |
| Ag/AgCl (0.1 M KCl) | +0.288 | |
| Hg/Hg₂Cl₂ in saturated KCl | +0.241 | = SCE |
| Hg/HgO (1 M NaOH) | +0.098 | Standard alkaline reference |
| Hg/HgO (1 M KOH) | +0.098 | Same |
| Hg/HgO (0.1 M NaOH) | +0.165 | |
| Hg/Hg₂SO₄ (saturated K₂SO₄) | +0.640 | Used in non-chloride media |
| Pseudo-reference Ag wire | NOT CONVERTIBLE | Calibrate vs internal Fc/Fc⁺ |

**Always specify the electrolyte when noting Ag/AgCl** — sat KCl, 3 M KCl, 3 M NaCl give different offsets. The `conversion_arithmetic.py` check requires the electrolyte to be explicit; "Ag/AgCl" alone fails the offset-match check.

## Non-aqueous

| Reference reported | Offset to SHE | Notes |
|---|---:|---|
| Fc/Fc⁺ in MeCN | +0.400 ± 0.05 | Approximate; IUPAC-recommended internal reference for non-aqueous CV |
| Fc/Fc⁺ in DMF | +0.45 | Similar |
| Fc/Fc⁺ in DMSO | +0.45 | Similar |
| Fc/Fc⁺ in THF | +0.56 | |
| Fc/Fc⁺ in DCM | +0.46 | |
| Ag/Ag⁺ (0.01 M AgNO₃ in MeCN) | +0.55 | Common pseudo-reference; varies by salt |

These are approximate and depend on supporting electrolyte. **For non-aqueous values, prefer reporting vs Fc/Fc⁺ in the original solvent rather than converting to SHE**, because the absolute conversion is uncertain by ±50–100 mV.

## pH-dependent references

For RHE (reversible hydrogen electrode at the measurement pH):
- E_SHE = E_RHE − 0.0591 × pH (at 25 °C)

Common conversions:
- RHE at pH 7 → subtract 0.4137 V
- RHE at pH 14 → subtract 0.8274 V

For PCET-active molecules (most quinones, phenazines), the Pourbaix relationship E°′(pH) = E°′(pH 0) − 0.0591 × pH × (m/n) applies, where m = protons, n = electrons. For the standard 2H⁺/2e⁻ quinone case this is −59 mV per pH unit.

## Pseudo-references and uncalibrated values

Some papers report "vs platinum wire" or "vs Ag wire" with no internal Fc/Fc⁺ calibration. **These values cannot be converted to SHE.** Either:
- Mark `voltage_v_she = blank`, status `flagged_review` with `flagged_reference_electrode_mismatch` in notes, OR
- If the paper provides a calibration in a related figure, use that with `conversion_arithmetic` showing the math.

Never convert pseudo-reference values using a guessed offset.

## Absolute-scale (vacuum-referenced) conventions

Some computational databases store potentials on an absolute scale referenced to vacuum, where the absolute SHE potential is approximately 4.42–4.44 V. Conversions take one of two forms depending on which underlying field is exported:

- `E_SHE = E_raw − E_abs(SHE)` if raw is the absolute single-electrode potential
- `E_SHE = E_abs(SHE) − E_raw` if raw is the absolute energy of a half-reaction in the opposite direction

**Critical:** the sign and offset depend on what the source dataset actually stores. **Read the dataset's API/schema source code** (typically GitHub) to confirm the convention before applying it — paper prose alone is often ambiguous about field semantics.

The `conversion_arithmetic.py` parser supports a **subtract-form** for these conversions:
```
4.42 - 5.50 = -1.08 V vs SHE
```

The parser validates the constant (4.42 V or 4.44 V) against known absolute-scale conventions. Even when the math passes the parser, **calibrate against canonical molecules** (e.g., parent quinones, ferrocene) before relying on the values — see the calibration spot-check guidance in `EXTRACTION_PROMPT_TEMPLATES.md`. If post-conversion values for known molecules are systematically wrong, the convention itself is wrong (sign error, wrong field exported, etc.) and you must re-confirm against the source's API code.

## RHE conversions

Some computational papers report potentials vs RHE at a specific pH. Use add-form:
```
-0.50 V vs RHE at pH 7 - 0.4137 = -0.91 V vs SHE
```

General formula: `E_SHE = E_RHE − 0.0591 × pH`. Common values:
- RHE at pH 7 → subtract 0.4137 V
- RHE at pH 14 → subtract 0.8274 V

## Standard sources for verification

When in doubt about a textbook value, cross-check against:
- Bard, Parsons, Jordan, "Standard Potentials in Aqueous Solution", IUPAC, Marcel Dekker (1985). Definitive aqueous reference.
- CRC Handbook of Chemistry and Physics, current edition. Section "Electrochemical Series".
- Pavlishchuk & Addison, *Inorg. Chim. Acta* 298, 97 (2000) for Fc/Fc⁺ vs SHE conversions across solvents.

For these textbook entries, use `source_url = textbook:CRC-Handbook-102nd` (or similar). The DOI title check skips textbook entries automatically.

These are the gold-standard references. If your value disagrees with these by >50 mV for a simple aquo ion or halide, your extraction is probably wrong.

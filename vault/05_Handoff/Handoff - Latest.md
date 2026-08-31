# Handoff - Latest

Last updated: 2026-08-31
Repository snapshot: `hardy-coefficients` at `069494f`
Worktree state: Hardy coefficients, evaluator, tests, and documentation are
uncommitted; the earlier project-memory checkpoint remains modified

## Project state

`icPhysics` now contains the crude shared calculation chain: Robinson,
camera-response tables, SI12 proton correction, the R method, WIC-derived
electron energy flux and uncertainty, E0--Fe covariance, Zhang--Paxton
collapse, the bundled 8.4-MB lookup table, loader, and generator. Two public
functions match the `PrecipitationImage` input/output boundary.

SI12 proton correction is now the public `proton_correct_images()` step.
`precipitation_from_ratio()` consumes corrected WIC/SI13 arrays and
`precipitation_from_zhang_paxton()` consumes corrected WIC plus Kp and MLT.
icBuilder calls correction once before method selection. The separated ratio
path matches the legacy combined calculation in a frozen reference case.

The public array-based `robinson_conductance()` entry point now supports the
modular icBuilder Product-3 boundary and preserves the scalar equations and
zero-flux uncertainty behavior in focused tests.

Hardy is now the default proton-energy model in icBuilder Product 2. The
public `PROTON_RESPONSE_ENERGY_RANGE` exposes the Frey table domain
(0.47--46.7 keV); icBuilder retains raw Hardy energy and clips only the array
passed to the camera responses. SI12 remains the proton-flux source. The
full icPhysics test suite passes (15 tests), and an
isolated real orbit-0364 Product-2/Product-3 round trip passed.

The copied table has the same SHA-256 as icBuilder. A small ratio-method
comparison matched the original scalar routine exactly. The new and old
Zhang--Paxton paths also matched exactly for every saved Product-2 field over
complete example orbit 0085. The two icPhysics Robinson tests and nine focused
icBuilder Product-2 tests pass.

Hardy et al. (1991) Table 1 is transcribed in
`src/icphysics/hardy_coefficients.py`. It contains both integral number-flux
and energy-flux coefficients with shape `(7, 13, 6)`, indexed by Kp level,
Fourier term, and generalized-Epstein parameter. All 1092 scalar values were
visually compared with the rendered journal table; no ambiguous cells remain.

`src/icphysics/hardy.py` implements equations 5--11 and exposes
`hardy_ion_precipitation(kp, mlt, mlat)`. Fractional Kp is handled by
interpolating evaluated log-flux profiles, never coefficients. The model
returns native integral number flux, integral energy flux, and their ratio as
mean ion energy in keV. Its Kp 0, 2, and 4 map morphology agrees visually with
the published model panels, and four independent checkpoints agree within 12%
with mean energies tabulated from the original 1989 statistical data. The full
icPhysics suite passes 14 tests.

The dependency boundary is confirmed: icAnalyzer must not depend on the full
icBuilder package and inherit fuvpy or other production-pipeline dependencies.
icPhysics depends on neither consumer. The separate `ZhangPaxton2008` package
remains authoritative for the published model equations.

## Next action

Run an icAnalyzer batched-array import check. Keep cleanup and removal of the
old icBuilder copies separate from this verified crude extraction.

Do not start the staged file-product redesign or VAE integration in this
repository. Those consuming-project changes follow only after the shared
calculation is stable.

Repeat the complete-corpus image-ratio diagnostics with Hardy proton energy and
retain the Modified-Apex coordinate approximation in the interpretation.

## Risks and open decisions

- The existing functions may encode undocumented clipping, singular-boundary,
  mask, or uncertainty behavior that must be preserved during extraction.
- Zhang--Paxton mean-energy versus characteristic-energy compatibility remains
  a scientific gate outside simple code movement.
- The probabilistic E0 interpretation remains undecided, but the lookup and
  collapse belong in icPhysics.
- Adding a generalized model interface before a second forward model exists
  would create unnecessary framework code.
- The Hardy evaluator is connected to the IMAGE proton-correction pipeline,
  but the complete corpus has not yet been regenerated with it.
- Hardy is defined in corrected geomagnetic latitude and MLT, whereas the
  IMAGE pipeline currently supplies Modified Apex coordinates at a 130-km
  reference height. Coumans et al. (2004) made the same comparison and cited a
  maximum latitude difference of 0.17 degrees near 68 degrees MLAT for Apex at
  110 km versus ground-level corrected geomagnetic coordinates, below the
  IMAGE-FUV resolution. Keep the coordinate convention explicit and perform a
  small grid-wide sensitivity check before pipeline integration.

## Portfolio impact

- Central update needed: Yes
- Changes: the Hardy et al. (1991) coefficients and functional ion model are
  now available through a tested icPhysics API.
- Sync summary: Hardy implementation is complete. Coordinate sensitivity and
  Frey-event integration tests are the next scientific gates; the pre-existing
  icAnalyzer batch/import check also remains open.

## Entry points

- `AGENTS.md`
- `README.md`
- `vault/01_Project/Project Brief.md`
- `vault/01_Project/Current State.md`
- `vault/02_Algorithm/Dependency and Model Boundary.md`
- `vault/03_Decisions/Decision Log.md`

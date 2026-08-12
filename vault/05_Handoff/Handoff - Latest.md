# Handoff - Latest

Last updated: 2026-08-12
Repository snapshot: `core_physics` at `8e63215`
Worktree state: crude precipitation and Zhang--Paxton extraction uncommitted

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

The copied table has the same SHA-256 as icBuilder. A small ratio-method
comparison matched the original scalar routine exactly. The new and old
Zhang--Paxton paths also matched exactly for every saved Product-2 field over
complete example orbit 0085. The two icPhysics Robinson tests and nine focused
icBuilder Product-2 tests pass.

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

## Risks and open decisions

- The existing functions may encode undocumented clipping, singular-boundary,
  mask, or uncertainty behavior that must be preserved during extraction.
- Zhang--Paxton mean-energy versus characteristic-energy compatibility remains
  a scientific gate outside simple code movement.
- The probabilistic E0 interpretation remains undecided, but the lookup and
  collapse belong in icPhysics.
- Adding a generalized model interface before a second forward model exists
  would create unnecessary framework code.

## Portfolio impact

- Central update needed: Yes
- Changes: crude precipitation chain implemented and connected to icBuilder;
  exact small and orbit-level comparisons passed.
- Sync summary: the next bounded milestone is an icAnalyzer batch/import check.

## Entry points

- `AGENTS.md`
- `README.md`
- `vault/01_Project/Project Brief.md`
- `vault/01_Project/Current State.md`
- `vault/02_Algorithm/Dependency and Model Boundary.md`
- `vault/03_Decisions/Decision Log.md`

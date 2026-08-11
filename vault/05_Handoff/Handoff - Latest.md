# Handoff - Latest

Last updated: 2026-08-11
Repository snapshot: `core_physics` at `c3d3cad`
Worktree state: initial project memory, package, TODO, and Robinson extraction uncommitted

## Project state

`icPhysics` now has a minimal `src/icphysics` package and the first copied
scientific module. Robinson Hall/Pedersen conductance and uncertainty match the
current icBuilder source for the checked ordinary case, including the existing
one-sided zero-flux rule. Two focused tests pass.

The dependency boundary is confirmed: icAnalyzer must not depend on the full
icBuilder package and inherit fuvpy or other production-pipeline dependencies.
icPhysics depends on neither consumer. The separate `ZhangPaxton2008` package
remains authoritative for the published model equations.

## Next action

Follow `TODO.md`: copy the camera responses and SI12 proton correction, then
the shared WIC electron-flux calculation and R method. Keep the code close to
icBuilder until an end-to-end comparison works.

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
- Changes: first reference-tested physics extraction implemented; Zhang--Paxton
  lookup ownership assigned to icPhysics.
- Sync summary: the next bounded milestone is the copied proton correction and
  electron-flux/R-method chain.

## Entry points

- `AGENTS.md`
- `README.md`
- `vault/01_Project/Project Brief.md`
- `vault/01_Project/Current State.md`
- `vault/02_Algorithm/Dependency and Model Boundary.md`
- `vault/03_Decisions/Decision Log.md`

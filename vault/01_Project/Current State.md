# Current State

Last reviewed: 2026-08-11
Repository snapshot: `core_physics` at `c3d3cad`
Worktree state: initial package, TODO, and Robinson extraction uncommitted

## Current position

The first implementation slice is in place. The repository now has minimal
package metadata and a direct extraction of the Robinson Hall/Pedersen forward
and uncertainty equations. Two small regression tests pass, and a direct
source-versus-extracted comparison is numerically identical for the tested
ordinary case.

Zhang--Paxton ownership is now settled: `ZhangPaxton2008` retains the published
base model, while icPhysics will own the latitude collapse, uncertainty and
sampling, lookup generation, bundled lookup file, and loader. icBuilder will
eventually call icPhysics and contain no Zhang--Paxton implementation.

## Confirmed boundary

- icAnalyzer must not depend on the full icBuilder distribution because that
  would propagate pipeline dependencies such as fuvpy.
- icPhysics sits below both projects and depends on neither.
- `ZhangPaxton2008` remains the authoritative implementation of the published
  Zhang--Paxton equations.
- icBuilder owns IMAGE preprocessing, coordinate handling, Kp assignment,
  orchestration, and files.
- icAnalyzer owns VAE and statistical-analysis workflows.
- Shared numerical equations should be pure, array-based, lightweight, and
  tested against the existing implementation before replacement.

## Not yet decided

- final distribution and import name;
- initial module layout and public function names;
- minimal declared dependency set;
- versioning and first alpha release criteria.

## Next action

Copy the existing IMAGE response tables, SI12 proton correction, WIC energy
flux conversion, and R method with minimal restructuring. Their detailed work
list is in `TODO.md`.

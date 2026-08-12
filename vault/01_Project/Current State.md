# Current State

Last reviewed: 2026-08-12
Repository snapshot: `core_physics` at `8e63215`
Worktree state: crude precipitation and Zhang--Paxton extraction uncommitted

## Current position

The crude shared-physics implementation is in place. Alongside Robinson, the
package now contains the copied IMAGE response tables, SI12 proton correction,
WIC/SI13 ratio method, WIC energy-flux conversion, uncertainty and E0--Fe
covariance, Zhang--Paxton collapse, bundled lookup table, loader, and lookup
generator.

`proton_correct_images()` now exposes SI12-based proton correction separately.
`precipitation_from_ratio()` accepts corrected WIC/SI13 arrays, while
`precipitation_from_zhang_paxton()` accepts corrected WIC plus Kp and MLT.
icBuilder performs correction once before selecting either precipitation
method. A frozen scalar comparison matches the legacy combined ratio routine.

`robinson_conductance()` is the array entry point for Product 3. It returns
Hall/Pedersen conductance and propagated uncertainty, including the established
one-sided uncertainty at zero energy flux.

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

Confirm that icAnalyzer can import the package and call the functions on a
batched array. Cleanup, module splitting, and removal of the old icBuilder
copies remain intentionally deferred.

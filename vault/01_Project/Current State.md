# Current State

Last reviewed: 2026-08-31
Repository snapshot: `hardy-coefficients` at `069494f`
Worktree state: Hardy coefficients, evaluator, tests, and documentation are
uncommitted; the earlier project-memory checkpoint remains modified

## Current position

The crude shared-physics implementation is in place. Alongside Robinson, the
package now contains the copied IMAGE response tables, SI12 proton correction,
WIC/SI13 ratio method, WIC energy-flux conversion, uncertainty and E0--Fe
covariance, Zhang--Paxton collapse, bundled lookup table, loader, and lookup
generator.

The full Hardy et al. (1991) Table 1 is transcribed in
`hardy_coefficients.py`, and `hardy.py` now implements the published Fourier,
generalized-Epstein, background-limit, and Kp-interpolation equations. The
public `hardy_ion_precipitation()` function returns ion number flux, energy
flux, and mean energy for broadcast-compatible Kp, MLT, and latitude arrays.
The 1092 coefficients were visually checked against the rendered paper table.
The evaluator reproduces the morphology of the paper's Kp 0, 2, and 4 model
maps and agrees within 12% at four independent mean-energy checkpoints from
the original 1989 statistical tables.

Hardy is now connected to icBuilder's modular Product-2 proton correction.
icPhysics publicly exposes the 0.47--46.7 keV domain of the Frey proton camera-
response tables so the caller can preserve raw model energy while clipping the
response input explicitly. The response functions accept spatial Ep/dEp
arrays; SI12 still supplies the event-specific proton flux.

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

Repeat the complete-corpus image-ratio diagnostics with Hardy proton energy.
Keep the corrected-geomagnetic versus Modified-Apex coordinate approximation
explicit when interpreting the result.

The pre-existing icAnalyzer batched-array import check, cleanup, and removal of
old icBuilder copies remain deferred.

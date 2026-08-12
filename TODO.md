# TODO

Last reviewed: 2026-08-12

## First working version

- [x] Create a minimal installable package.
- [x] Copy the Robinson Hall/Pedersen equations and uncertainty propagation.
- [x] Copy the IMAGE camera response tables and SI12 proton correction.
- [x] Copy the WIC electron response, energy-flux calculation, and uncertainty.
- [x] Copy the WIC/SI13 ratio method, including its current fallbacks and clipping.
- [x] Copy the Zhang--Paxton latitude collapse from icBuilder.
- [x] Move the Zhang--Paxton lookup loader and bundled lookup table from
  icBuilder to icPhysics.
- [x] Add two direct precipitation entry points:
  `precipitation_from_ratio()` and `precipitation_from_zhang_paxton()`.
- [x] Replace the placeholder functions in `icBuilder.PrecipitationImage`.
- [x] Compare one complete orbit before removing the old icBuilder routines.
- [ ] Confirm that icAnalyzer can call the functions on batched arrays.

## Ownership

- `ZhangPaxton2008` owns the published `ZP(Kp, MLT, MLAT)` equations.
- `icPhysics` owns the collapse, uncertainty/sampling, lookup generation,
  lookup file, and lookup loader.
- `icBuilder` owns Kp acquisition and frame matching, grids, image processing,
  products, and orbit execution.

## Scientific questions to revisit after the copied pipeline works

- Does Product-1 `sigma` already contain uncertainty that the old count
  equations add separately as a Poisson term?
- Is Zhang--Paxton mean energy compatible with the energy expected by the
  Robinson equations?
- Should the Zhang--Paxton residual distribution be sampled empirically or as
  a Gaussian common log-space amplitude offset?
- Which parts of the R method should remain available only as diagnostics?
- Propagate the shared SI12-induced covariance between corrected WIC and SI13.
- After numerical equivalence is secure, split or retire the remaining legacy
  `E0_eflux_propagated()` wrapper instead of maintaining duplicate paths.

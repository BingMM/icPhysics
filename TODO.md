# TODO

Last reviewed: 2026-08-11

## First working version

- [x] Create a minimal installable package.
- [x] Copy the Robinson Hall/Pedersen equations and uncertainty propagation.
- [ ] Copy the IMAGE camera response tables and SI12 proton correction.
- [ ] Copy the WIC electron response, energy-flux calculation, and uncertainty.
- [ ] Copy the WIC/SI13 ratio method, including its current fallbacks and clipping.
- [ ] Copy the Zhang--Paxton latitude collapse from icBuilder.
- [ ] Move the Zhang--Paxton lookup loader and bundled lookup table from
  icBuilder to icPhysics.
- [ ] Add two direct precipitation entry points:
  `precipitation_from_ratio()` and `precipitation_from_zhang_paxton()`.
- [ ] Replace the placeholder functions in `icBuilder.PrecipitationImage`.
- [ ] Compare one complete orbit before removing the old icBuilder routines.
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


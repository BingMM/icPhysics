# Dependency and Model Boundary

Last reviewed: 2026-08-11
Status: Accepted boundary; first extraction implemented

## Dependency direction

```text
ZhangPaxton2008
        |
        v
     icPhysics
       /   \
      v     v
icBuilder  icAnalyzer
```

Dependencies must remain acyclic. icPhysics must not import either consuming
project.

## Data and calculation responsibilities

### icBuilder

- reads and preprocesses WIC, SI12, and SI13;
- performs coordinate conversion and binning;
- obtains and assigns definitive Kp to IMAGE frames;
- serializes binned, precipitation, and conductance products;
- calls icPhysics for shared numerical equations.

### icPhysics

- transforms already prepared numerical arrays;
- implements shared precipitation and conductance equations;
- accepts numerical Kp when a shared model calculation requires it;
- exposes explicit units, uncertainty inputs, masks, and array behavior;
- contains no orbit or file-product knowledge.
- owns the Zhang--Paxton collapse, uncertainty/sampling, lookup generation,
  bundled lookup file, and lookup loader;

`ZhangPaxton2008` remains the dependency that owns the published base
`ZP(Kp, MLT, MLAT)` equations. icBuilder should not retain a third copy of
application-specific Zhang--Paxton code.

### icAnalyzer

- reads prepared products through the appropriate reader;
- trains and samples statistical models;
- calls icPhysics in memory for ensemble propagation;
- does not independently rematch Kp for an existing IMAGE frame.

## Initial extraction rule

Move one calculation at a time. First copy its current behavior into frozen
reference tests, then extract it without scientific alteration, switch one
consumer, and compare the full result. Changes to equations or uncertainty are
separate scientific tasks after equivalence is established.

## Candidate order

1. Robinson Hall/Pedersen forward calculation and uncertainty.
2. Camera response and SI12-based proton correction.
3. R-method energy and flux calculation.
4. Zhang--Paxton collapse/lookup boundary.
5. Probabilistic E0 sampling after its interpretation is scientifically
   accepted.

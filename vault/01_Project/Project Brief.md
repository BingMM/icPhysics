# Project Brief

Last reviewed: 2026-08-10

## Purpose

`icPhysics` provides one lightweight, tested implementation of the physical
calculations that must be identical in icBuilder's IMAGE production pipeline
and icAnalyzer's VAE and Monte-Carlo experiments.

It prevents shared equations from being copied between projects and prevents
icBuilder's heavy pipeline dependencies from propagating into icAnalyzer.

## Intended consumers

- `icBuilder`: prepares IMAGE observations and produces staged precipitation
  and conductance products.
- `icAnalyzer`: propagates sampled observations and energy through the same
  physical equations when constructing conductance ensembles.

## Proposed scope

- IMAGE camera-response and SI12 proton-correction calculations;
- WIC/SI13 ratio-based electron energy and flux;
- higher-level use of the external `ZhangPaxton2008` model, including the
  collapsed estimate, lookup, and later sampling definition;
- Robinson Hall/Pedersen conductance and uncertainty propagation;
- simple public array-based APIs and numerical reference tests.

## Out of scope

- reading, calibrating, background-correcting, binning, or plotting images;
- coordinate conversion, orbit processing, multiprocessing, and product I/O;
- downloading or assigning historical Kp to IMAGE frames;
- VAE architecture, training, reconstruction, covariance estimation, or data
  assimilation;
- general-purpose framework abstractions not required by current equations.

## Desired outcome

A small installable package that both consuming projects can use without
duplicating equations or importing each other's dependency stacks. Each public
calculation is documented by units and assumptions and verified against its
current icBuilder reference implementation before adoption.

## Repository position

The project began as an empty MIT-licensed repository. Package layout, public
API, dependencies, and extracted routines have not yet been implemented.

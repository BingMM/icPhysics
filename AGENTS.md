# Repository guidance

## Purpose

`icPhysics` is the lightweight scientific layer shared by `icBuilder` and
`icAnalyzer`. It exists so both projects use identical precipitation and
conductance equations without making icAnalyzer depend on icBuilder's image
processing, coordinate, file-I/O, or orchestration stack.

The intended dependency direction is:

```text
ZhangPaxton2008
        |
        v
     icPhysics
       /   \
      v     v
icBuilder  icAnalyzer
```

Neither consuming project may become a dependency of this package.

## Project memory

Before substantive work, read:

1. `vault/01_Project/Current State.md`
2. `vault/05_Handoff/Handoff - Latest.md`
3. `vault/01_Project/Project Brief.md`

Then read relevant algorithm and decision notes only as needed.

Use this source-of-truth order:

1. live code, Git state, focused tests, and numerical reference comparisons;
2. `Current State.md` and `Handoff - Latest.md`;
3. decision and algorithm notes;
4. dated session history.

## Scientific boundary

Candidate shared calculations include:

- SI12-based proton correction and IMAGE camera-response equations;
- the WIC/SI13 ratio method for electron energy and energy flux;
- collapsed Zhang--Paxton evaluation, lookup, and probabilistic sampling;
- Robinson Hall and Pedersen conductance and uncertainty propagation.

Keep these outside icPhysics:

- `fuvpy` image processing and background removal;
- ApexPy coordinate conversion;
- orbit discovery, time matching, and multiprocessing;
- historical Kp acquisition and assignment to IMAGE frames;
- NetCDF product orchestration and project-specific file layouts;
- VAE, PyTorch, reconstruction, and assimilation workflows.

icPhysics may accept numerical Kp as model input. icBuilder remains responsible
for assigning authoritative Kp to IMAGE frames and serializing its provenance.

## Working rules

- Preserve unrelated and pre-existing worktree changes.
- Do implementation work on a feature branch; keep `main` as the reviewed
  integration point.
- During extraction, preserve the existing scientific calculation exactly.
  Separate code movement from changes to equations, thresholds, uncertainty,
  clipping, or missing-data semantics.
- Establish frozen reference values from icBuilder before replacing its local
  routines. A successful import is not evidence of numerical equivalence.
- Prefer small public functions operating on NumPy arrays and returning arrays
  or ordinary dictionaries.
- Make units, shapes, masks, NaN behavior, clipping, and covariance inputs
  explicit. Support leading batch or ensemble dimensions where this does not
  obscure the calculation.
- Do not add file-product classes, plotting, command-line orchestration,
  factories, plugin systems, compatibility frameworks, or speculative APIs.
- Keep dependencies minimal. NumPy/SciPy-level numerical dependencies and the
  focused `ZhangPaxton2008` package are acceptable when justified; do not add
  fuvpy, ApexPy, NetCDF pipeline packages, or machine-learning frameworks.
- Do not copy Zhang--Paxton equations into this repository. Depend on the
  maintained `ZhangPaxton2008` package and add only the shared higher-level
  collapse or sampling logic needed by the two consuming projects.
- Do not download Kp or other external data at import time or inside a
  scientific calculation.

## Scientific coding style

- Write for a small research group. A student or scientist should be able to
  follow the calculation from top to bottom.
- Write for a scientist reading the code interactively in an editor. Make
  workflows visually scannable with `#%%` sections where appropriate, blank
  lines between conceptual stages, and short comments that identify each block.
- Keep the main calculation linear and visible from top to bottom. Prefer
  familiar intermediate variables and explicit operations over nested
  expressions, generic plumbing, or compressed control flow.
- Extract a helper when it represents a distinct calculation or removes
  meaningful repetition. Do not hide a few obvious sequential steps behind an
  abstraction merely to shorten the main function.
- Comments may serve as navigational headings even when the underlying Python
  is straightforward. Treat formatter conventions and line-length targets as
  secondary to human readability, while avoiding ambiguous or unwieldy code.
- Challenge unclear nearby code when correctness, numerical rigor, or clarity
  can be materially improved, but do not add production-style architecture.

## Verification

Every extracted routine needs:

1. focused unit tests for ordinary, boundary, masked, NaN, and zero-flux cases;
2. a frozen comparison with the source icBuilder calculation;
3. an icBuilder integration comparison on at least one representative orbit;
4. an icAnalyzer-side import and batched-array test before the API is tagged.

Numerical differences must be quantified and explained. Do not update a
reference output merely to make a changed implementation pass.

For documentation-only setup, run:

```bash
git diff --check
```

Once Python source exists, a safe syntax check is:

```bash
python -c "import ast, pathlib; files=list(pathlib.Path('src').rglob('*.py'))+list(pathlib.Path('tests').rglob('*.py')); [ast.parse(p.read_text(), filename=str(p)) for p in files]; print(f'parsed {len(files)} files')"
```

## Automatic memory checkpoints

Project-memory maintenance is a default responsibility. Checkpoint after a
verified extraction, public-API decision, numerical comparison, dependency
change, blocker, or changed next action.

At a meaningful checkpoint:

1. create `vault/04_Sessions/YYYY-MM-DD.md` only when historical detail is
   worth preserving;
2. rewrite `Current State.md` when verified project state changed;
3. append only durable choices to the decision log;
4. replace obsolete content in `Handoff - Latest.md`;
5. update algorithm notes only when scientific interpretation changed;
6. refresh the handoff's `Portfolio impact` section.

Do not record raw logs, transient speculation, or unchanged state. Never edit
the central second brain directly; report portfolio changes through the latest
handoff.

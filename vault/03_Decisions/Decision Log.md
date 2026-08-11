# Decision Log

Last reviewed: 2026-08-11

## 2026-08-11 — Keep the Zhang--Paxton application layer in icPhysics

**Decision:** `ZhangPaxton2008` retains the published base equations.
icPhysics owns the collapse, uncertainty/sampling, lookup generation, bundled
lookup table, and loader. icBuilder will consume those interfaces instead of
retaining Zhang--Paxton code or data.

**Rationale:** This keeps the validated base model separate while avoiding an
application implementation split across ZhangPaxton2008, icPhysics, and
icBuilder.

## 2026-08-10 — Create a lightweight shared physics package

**Decision:** Use the dedicated `icPhysics` repository for numerical
precipitation and conductance routines shared by icBuilder and icAnalyzer.
Neither consumer depends on the other.

**Rationale:** icBuilder requires pipeline packages such as fuvpy that are not
needed in icAnalyzer. A direct icAnalyzer dependency on icBuilder would couple
the VAE environment to the complete data-production stack. Copying equations
would instead create scientific drift.

## 2026-08-10 — Keep project-specific orchestration outside icPhysics

**Decision:** Keep image processing, coordinate conversion, file products,
orbit execution, Kp acquisition and frame matching, and VAE workflows in their
own projects. icPhysics accepts prepared arrays and numerical model inputs.

**Rationale:** The shared unit is the scientific calculation, not the complete
workflow. A narrow boundary keeps dependencies small and makes numerical
equivalence testable.

## 2026-08-10 — Retain ZhangPaxton2008 as the model authority

**Decision:** Do not copy the published Zhang--Paxton implementation into
icPhysics. Depend on `ZhangPaxton2008` and add only shared higher-level collapse,
lookup, or sampling behavior where it belongs.

**Rationale:** The focused repository already owns transcription, validation,
figures, and publication provenance for that model.

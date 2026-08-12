# icPhysics

Lightweight precipitation and ionospheric-conductance physics shared by
`icBuilder` and `icAnalyzer`.

The first copied routines implement the Robinson et al. (1987) Hall and
Pedersen conductance equations and their existing uncertainty propagation.
The remaining extraction is tracked in [`TODO.md`](TODO.md).

```python
from icphysics import hall, ped

Sigma_P = ped(E0, Fe)
Sigma_H = hall(E0, Fe)
```

The crude precipitation API is also available:

```python
from icphysics import precipitation_from_ratio
from icphysics import precipitation_from_zhang_paxton
```

`ZhangPaxton2008` supplies the published empirical model. icPhysics contains
the IMAGE-specific latitude collapse and bundled Kp lookup table.

Licensed under the MIT License.

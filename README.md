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

The Hardy et al. (1991) statistical ion-precipitation model is available as a
separate pure-array calculation:

```python
from icphysics import hardy_ion_precipitation

ions = hardy_ion_precipitation(kp=2, mlt=0, mlat=67)
proton_energy = ions["mean_energy"]  # keV
```

The Hardy coordinates are corrected geomagnetic latitude and MLT. Modified
Apex latitude, as used by the IMAGE pipeline, is a close but not identical
approximation.

Licensed under the MIT License.

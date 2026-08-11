"""Small regression check for the first copied physics routines."""

import numpy as np

from icphysics import hall, halluncertainty, ped, peduncertainty


def test_robinson_reference_values():
    inputs = (2.5, 4.0, 0.3, 0.5, -0.02)

    np.testing.assert_allclose(ped(*inputs[:2]), 8.98876404494382)
    np.testing.assert_allclose(hall(*inputs[:2]), 8.813765704000613)
    np.testing.assert_allclose(
        peduncertainty(*inputs), 0.6842658428542764
    )
    np.testing.assert_allclose(
        halluncertainty(*inputs), 1.3998674616220634
    )


def test_zero_flux_uses_one_sided_excursion():
    E0 = 4.0
    dFe = 0.25

    assert peduncertainty(E0, 0.0, 1.0, dFe, 0.0) == ped(E0, dFe)
    assert halluncertainty(E0, 0.0, 1.0, dFe, 0.0) == hall(E0, dFe)

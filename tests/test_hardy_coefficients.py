"""Checks for the transcribed Hardy et al. (1991) coefficient table."""

import numpy as np

from icphysics.hardy_coefficients import (
    ENERGY_FLUX_COEFFICIENTS,
    EPSTEIN_PARAMETERS,
    FOURIER_TERMS,
    KP_LEVELS,
    NUMBER_FLUX_COEFFICIENTS,
)


def test_hardy_table_axes_and_shapes():
    assert np.array_equal(KP_LEVELS, np.arange(7))
    assert FOURIER_TERMS == (
        "c0", "c1", "c2", "c3", "c4", "c5", "c6",
        "s1", "s2", "s3", "s4", "s5", "s6",
    )
    assert EPSTEIN_PARAMETERS == ("r0", "h0", "h1", "S0", "r1", "S2")

    assert NUMBER_FLUX_COEFFICIENTS.shape == (7, 13, 6)
    assert ENERGY_FLUX_COEFFICIENTS.shape == (7, 13, 6)
    assert NUMBER_FLUX_COEFFICIENTS.size + ENERGY_FLUX_COEFFICIENTS.size == 1092


def test_hardy_table_contains_only_finite_values():
    assert np.all(np.isfinite(NUMBER_FLUX_COEFFICIENTS))
    assert np.all(np.isfinite(ENERGY_FLUX_COEFFICIENTS))


def test_representative_values_match_table_1():
    # Spot checks cover both quantities, all Kp levels, and both PDF pages.
    assert NUMBER_FLUX_COEFFICIENTS[0, 0, 0] == 6.0735
    assert ENERGY_FLUX_COEFFICIENTS[0, 12, 5] == -0.0019
    assert NUMBER_FLUX_COEFFICIENTS[1, 7, 5] == 0.0000
    assert ENERGY_FLUX_COEFFICIENTS[2, 10, 3] == -0.0004
    assert NUMBER_FLUX_COEFFICIENTS[3, 8, 1] == -1.2035
    assert ENERGY_FLUX_COEFFICIENTS[4, 12, 2] == 0.3609
    assert NUMBER_FLUX_COEFFICIENTS[5, 0, 0] == 6.6795
    assert ENERGY_FLUX_COEFFICIENTS[5, 9, 3] == -0.1239
    assert NUMBER_FLUX_COEFFICIENTS[6, 12, 5] == 0.0240
    assert ENERGY_FLUX_COEFFICIENTS[6, 0, 2] == 76.3270

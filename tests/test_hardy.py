"""Tests for the Hardy et al. (1991) auroral ion model."""

import numpy as np

from icphysics import hardy_ion_precipitation
from icphysics.hardy import (
    POLEWARD_ENERGY_FLUX,
    POLEWARD_NUMBER_FLUX,
    _epstein_log_flux,
    _fourier_parameters,
)
from icphysics.hardy_coefficients import NUMBER_FLUX_COEFFICIENTS


def test_fourier_expansion_at_midnight_and_wraparound():
    parameters = _fourier_parameters(NUMBER_FLUX_COEFFICIENTS, 2, 0)
    expected = np.sum(NUMBER_FLUX_COEFFICIENTS[2, :7], axis=0)
    np.testing.assert_allclose(parameters, expected, atol=1e-14)

    wrapped = _fourier_parameters(NUMBER_FLUX_COEFFICIENTS, 2, 24)
    np.testing.assert_allclose(wrapped, parameters, atol=1e-14)


def test_epstein_profile_passes_through_both_breakpoints():
    parameters = _fourier_parameters(NUMBER_FLUX_COEFFICIENTS, 3, 21)
    r0, h0, h1, _, r1, _ = parameters

    np.testing.assert_allclose(_epstein_log_flux(parameters, h0), r0)
    np.testing.assert_allclose(_epstein_log_flux(parameters, h1), r1)


def test_published_background_levels_are_applied():
    result = hardy_ion_precipitation(2, 0, np.array([40.0, 95.0]))

    equatorward_number = 8.32e3 * 10**(0.157 * 2)
    equatorward_energy = 4.17e2 * 10**(0.126 * 2)

    np.testing.assert_allclose(result["number_flux"][0], equatorward_number)
    np.testing.assert_allclose(result["energy_flux"][0], equatorward_energy)
    np.testing.assert_allclose(result["number_flux"][1], POLEWARD_NUMBER_FLUX)
    np.testing.assert_allclose(result["energy_flux"][1], POLEWARD_ENERGY_FLUX)


def test_fractional_kp_interpolates_the_evaluated_log_flux():
    lower = hardy_ion_precipitation(2, 21, 67)
    middle = hardy_ion_precipitation(2.5, 21, 67)
    upper = hardy_ion_precipitation(3, 21, 67)

    for name in ("number_flux", "energy_flux"):
        expected = (np.log10(lower[name]) + np.log10(upper[name])) / 2
        np.testing.assert_allclose(np.log10(middle[name]), expected)


def test_model_broadcasting_units_and_mean_energy():
    kp = np.array([0.0, 2.5, 6.0])[:, None]
    mlt = np.array([0.0, 6.0, 12.0, 18.0])[None, :]
    result = hardy_ion_precipitation(kp, mlt, 70.0)

    assert result["number_flux"].shape == (3, 4)
    assert result["energy_flux"].shape == (3, 4)
    assert result["mean_energy"].shape == (3, 4)
    assert np.all(result["number_flux"] > 0)
    assert np.all(result["energy_flux"] > 0)
    np.testing.assert_allclose(
        result["mean_energy"],
        result["energy_flux"] / result["number_flux"],
    )


def test_kp_limits_mlt_periodicity_and_nan_propagation():
    np.testing.assert_equal(
        hardy_ion_precipitation(-1, 0, 70)["mean_energy"],
        hardy_ion_precipitation(0, 24, 70)["mean_energy"],
    )
    np.testing.assert_equal(
        hardy_ion_precipitation(9, 12, 70)["mean_energy"],
        hardy_ion_precipitation(6, 12, 70)["mean_energy"],
    )

    result = hardy_ion_precipitation(np.nan, 0, 70)
    assert np.isnan(result["number_flux"])
    assert np.isnan(result["energy_flux"])
    assert np.isnan(result["mean_energy"])


def test_mean_energy_agrees_with_original_1989_statistical_tables():
    # The 1991 functional model is a smooth fit, so exact agreement with the
    # original binned values is not expected. These independent checkpoints
    # come from Tables 1 and 2 of Hardy et al. (1989).
    locations = [
        (0, 12.0, 79.5),
        (2, 12.0, 77.5),
        (2, 0.0, 66.5),
        (6, 0.0, 62.5),
    ]
    reported_energy = np.array([1.19, 1.57, 13.4, 19.2])

    model_energy = np.array([
        hardy_ion_precipitation(kp, mlt, mlat)["mean_energy"]
        for kp, mlt, mlat in locations
    ])
    np.testing.assert_allclose(model_energy, reported_energy, rtol=0.12)

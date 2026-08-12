"""Reference check for the separated IMAGE precipitation steps."""

import numpy as np

from icphysics.image import E0_eflux_propagated
from icphysics import precipitation_from_ratio, proton_correct_images


def test_separate_proton_correction_matches_legacy_ratio_calculation():
    counts = [500.0, 50.0, 20.0]
    uncertainties = [5.0, 2.0, 2.0]
    proton_energy = 2.0
    dproton_energy = 0.1

    corrected = proton_correct_images(
        wic=np.array([counts[0]]),
        dwic=np.array([uncertainties[0]]),
        si12=np.array([counts[1]]),
        dsi12=np.array([uncertainties[1]]),
        si13=np.array([counts[2]]),
        dsi13=np.array([uncertainties[2]]),
        proton_energy=proton_energy,
        proton_energy_uncertainty=dproton_energy,
    )
    separated = precipitation_from_ratio(
        corrected["wic_corrected"],
        corrected["dwic_corrected"],
        corrected["si13_corrected"],
        corrected["dsi13_corrected"],
    )

    legacy = E0_eflux_propagated(
        counts,
        [0.0, 0.0, 0.0],
        uncertainties,
        proton_energy,
        dproton_energy,
    )
    names = ["E0", "Fe", "dE0", "dFe", "R", "dR"]

    for name, expected in zip(names, legacy):
        np.testing.assert_allclose(separated[name][0], expected)

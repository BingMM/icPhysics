"""Hardy et al. (1991) statistical model of auroral ion precipitation.

The model returns average integral ion number flux, integral ion energy flux,
and their ratio (the mean ion energy) as functions of Kp, magnetic local time,
and corrected geomagnetic latitude.

Calculation outline
-------------------
For each of the two flux quantities, the calculation follows the paper:

1. Table 1 supplies 13 Fourier coefficients for each of six latitude-profile
   parameters at every integer Kp level.
2. Equation 9 reconstructs those six parameters at the requested MLT.
3. Equations 6--8 determine the otherwise missing middle slope, ``S1``.
4. Equation 5 evaluates the generalized Epstein latitude profile in log10
   flux.
5. Equations 10--11 impose the measured background levels outside the oval.
6. Fractional Kp is interpolated between the completed log-flux profiles.
7. Energy flux divided by number flux gives mean ion energy in keV.

This is a Kp-conditioned statistical climatology, not an event-specific
measurement. IMAGE studies use its mean ion energy as an estimate of proton
mean energy when interpreting SI12, but this module does not attach an
uncertainty to that estimate.

Hardy used corrected geomagnetic coordinates.  The current IMAGE pipeline
uses Modified Apex coordinates at a 130-km reference height.  Those systems
are close at auroral latitudes, but they are not formally identical; the
coordinate choice must remain explicit when this model is connected to
icBuilder.

References
----------
Hardy et al. (1989), JGR, https://doi.org/10.1029/JA094iA01p00370
Hardy et al. (1991), JGR, https://doi.org/10.1029/90JA02451
"""

#%% Imports

import numpy as np

from .hardy_coefficients import (
    ENERGY_FLUX_COEFFICIENTS,
    NUMBER_FLUX_COEFFICIENTS,
)


#%% Published background levels

# ions cm^-2 s^-1 sr^-1 and keV cm^-2 s^-1 sr^-1, respectively
POLEWARD_NUMBER_FLUX = 6.31e5
POLEWARD_ENERGY_FLUX = 1.41e5


#%% Published equations

def _fourier_parameters(coefficients, kp_level, mlt):
    """Reconstruct the six latitude-profile parameters at one MLT.

    ``coefficients`` has axes ``Kp, Fourier term, Epstein parameter``.
    Equation 9 is a sixth-order Fourier series in MLT. The returned array has
    the broadcast input shape followed by a final six-parameter axis ordered
    as ``r0, h0, h1, S0, r1, S2``.

    ``kp_level`` must contain integer table indices from 0 through 6. This
    helper never interpolates coefficients between Kp levels.
    """

    kp_level, mlt = np.broadcast_arrays(kp_level, mlt)

    # Selecting Kp leaves the 13 Fourier rows and six parameter columns as
    # the final two axes.
    selected = coefficients[kp_level]

    # One MLT day corresponds to 2*pi radians. Each higher harmonic completes
    # one additional cycle over the 24-hour MLT range.
    harmonic = np.arange(1, 7)
    phase = np.pi * mlt[..., None] * harmonic / 12

    cosine = np.cos(phase)[..., :, None]
    sine = np.sin(phase)[..., :, None]

    parameters = selected[..., 0, :]
    parameters = parameters + np.sum(selected[..., 1:7, :] * cosine, axis=-2)
    parameters = parameters + np.sum(selected[..., 7:13, :] * sine, axis=-2)
    return parameters


def _epstein_log_flux(parameters, mlat):
    """Evaluate the generalized Epstein latitude profile.

    ``r0`` and ``r1`` define the log10 flux at the two breakpoint latitudes
    ``h0`` and ``h1``. ``S0`` and ``S2`` are the far-equatorward and
    far-poleward slopes. Equation 6 chooses the middle slope ``S1`` so that
    the smooth profile also passes through ``(h1, r1)``.

    The natural logarithms inside equation 5 control how smoothly the slopes
    change. The value returned by the complete equation remains log10 flux
    because that is how ``r0``, ``r1``, and the slopes were fitted.
    """

    r0, h0, h1, S0, r1, S2 = np.moveaxis(parameters, -1, 0)

    # Equations 7 and 8. np.logaddexp evaluates log(1 + exp(x))
    # without overflowing for large positive x.
    b1 = np.logaddexp(0, h1 - h0) - np.log(2)
    b2 = np.log(2) - np.logaddexp(0, h0 - h1)

    # Equation 6: choose S1 so that the profile passes through (h1, r1).
    S1 = (
        r1 - r0 - S0 * (h1 - h0) + S0 * b1 - S2 * b2
    ) / (b1 - b2)

    # These two soft transitions replace sharp corners at h0 and h1.
    first_transition = np.logaddexp(0, mlat - h0) - np.log(2)
    second_transition = (
        np.logaddexp(0, mlat - h1)
        - np.logaddexp(0, h0 - h1)
    )

    log_flux = r0 + S0 * (mlat - h0)
    log_flux = log_flux + (S1 - S0) * first_transition
    log_flux = log_flux + (S2 - S1) * second_transition
    return log_flux


def _apply_background(log_flux, parameters, kp_level, mlat, quantity):
    """Replace unrealistically low tails with the measured background.

    The Epstein function describes the central auroral precipitation region.
    Hardy separately estimated nearly constant fluxes outside it. A low value
    equatorward of ``h0`` is therefore replaced by the Kp-dependent
    equatorward limit, while a low value poleward of ``h1`` is replaced by the
    fixed poleward limit. Values inside the fitted oval are left untouched.
    """

    h0 = parameters[..., 1]
    h1 = parameters[..., 2]

    if quantity == "number":
        poleward_limit = np.log10(POLEWARD_NUMBER_FLUX)
        equatorward_limit = np.log10(8.32e3) + 0.157 * kp_level
    elif quantity == "energy":
        poleward_limit = np.log10(POLEWARD_ENERGY_FLUX)
        equatorward_limit = np.log10(4.17e2) + 0.126 * kp_level
    else:
        raise ValueError("quantity must be 'number' or 'energy'")

    use_equatorward_limit = (mlat < h0) & (log_flux < equatorward_limit)
    log_flux = np.where(use_equatorward_limit, equatorward_limit, log_flux)

    use_poleward_limit = (mlat > h1) & (log_flux < poleward_limit)
    log_flux = np.where(use_poleward_limit, poleward_limit, log_flux)
    return log_flux


def _log_flux_at_kp_level(coefficients, kp_level, mlt, mlat, quantity):
    """Evaluate a complete flux profile at one tabulated Kp level.

    This small wrapper keeps the scientific sequence visible: reconstruct the
    MLT-dependent parameters, calculate the latitude profile, and finally
    impose the appropriate background values.
    """

    parameters = _fourier_parameters(coefficients, kp_level, mlt)
    log_flux = _epstein_log_flux(parameters, mlat)
    return _apply_background(log_flux, parameters, kp_level, mlat, quantity)


#%% Public model

def hardy_ion_precipitation(kp, mlt, mlat):
    """Return the statistical auroral ion precipitation from Hardy.

    Parameters
    ----------
    kp : float or array
        Planetary Kp index. Fractional values are interpolated in the final
        log10 flux, as prescribed by Hardy et al. (1991). Values below zero
        use the Kp=0 model and values at or above six use the final Kp>=6-
        activity level.
    mlt : float or array
        Magnetic local time [hours]. Values are wrapped onto [0, 24).
    mlat : float or array
        Northern corrected geomagnetic latitude [degrees]. The published
        statistical model was constructed over 50--90 degrees. Modified Apex
        latitude may be supplied as an approximation, but it is not formally
        the coordinate system used to derive the model.

    Returns
    -------
    dict
        ``number_flux`` in ions cm^-2 s^-1 sr^-1, ``energy_flux`` in
        keV cm^-2 s^-1 sr^-1, and ``mean_energy`` in keV.

    Notes
    -----
    The three inputs follow ordinary NumPy broadcasting rules. A scalar Kp can
    therefore be combined directly with two-dimensional MLT and latitude
    grids. Non-finite input locations return NaN in every output.

    Number flux and energy flux were fitted independently by Hardy. The mean
    energy returned here is their ratio, as defined in equation 3 of Hardy et
    al. (1989); it is not an independently fitted characteristic energy.

    The function evaluates finite latitudes outside 50--90 degrees, but those
    values lie outside the spatial range used to construct the statistical
    model and should not be interpreted as a validated extrapolation.
    """

    # 1. Put Kp, MLT, and latitude on one common array shape.
    kp, mlt, mlat = np.broadcast_arrays(
        np.asarray(kp, dtype=float),
        np.asarray(mlt, dtype=float),
        np.asarray(mlat, dtype=float),
    )

    valid = np.isfinite(kp) & np.isfinite(mlt) & np.isfinite(mlat)

    # 2. Locate the two integer Kp models surrounding every requested value.
    # The final source-data group is Kp >= 6-. NaN is replaced temporarily so
    # that it can be converted safely to an integer array index.
    kp_for_index = np.where(np.isfinite(kp), kp, 0)
    kp_for_index = np.clip(kp_for_index, 0, 6)
    lower_kp = np.floor(kp_for_index).astype(int)
    upper_kp = np.ceil(kp_for_index).astype(int)
    fraction = kp_for_index - lower_kp

    mlt = np.mod(mlt, 24)

    # 3. Evaluate complete number- and energy-flux profiles at both Kp levels.
    lower_number = _log_flux_at_kp_level(
        NUMBER_FLUX_COEFFICIENTS, lower_kp, mlt, mlat, "number"
    )
    upper_number = _log_flux_at_kp_level(
        NUMBER_FLUX_COEFFICIENTS, upper_kp, mlt, mlat, "number"
    )

    lower_energy = _log_flux_at_kp_level(
        ENERGY_FLUX_COEFFICIENTS, lower_kp, mlt, mlat, "energy"
    )
    upper_energy = _log_flux_at_kp_level(
        ENERGY_FLUX_COEFFICIENTS, upper_kp, mlt, mlat, "energy"
    )

    # 4. Interpolate the completed log-flux profiles. Hardy explicitly warns
    # that interpolating the coefficients instead can give unpredictable
    # results.
    log_number_flux = lower_number + fraction * (upper_number - lower_number)
    log_energy_flux = lower_energy + fraction * (upper_energy - lower_energy)

    # 5. Return to physical flux units and derive mean energy from their ratio.
    number_flux = np.power(10.0, log_number_flux)
    energy_flux = np.power(10.0, log_energy_flux)
    mean_energy = energy_flux / number_flux

    number_flux = np.where(valid, number_flux, np.nan)
    energy_flux = np.where(valid, energy_flux, np.nan)
    mean_energy = np.where(valid, mean_energy, np.nan)

    return {
        "number_flux": number_flux,
        "energy_flux": energy_flux,
        "mean_energy": mean_energy,
    }

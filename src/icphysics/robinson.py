"""Robinson et al. (1987) Hall and Pedersen conductance equations.

This is an intentionally direct extraction from icBuilder. Scientific cleanup
and API consolidation can follow after the consuming projects reproduce their
current results.
"""

#%% Imports

import numpy as np


#%% Conductance

def ped(E0, Fe):
    """Return Pedersen conductance in siemens.

    Parameters
    ----------
    E0 : float or array
        Electron average energy [keV].
    Fe : float or array
        Electron energy flux [mW/m2, equivalent to erg/cm2/s].
    """

    return 40 * E0 / (16 + E0**2) * np.sqrt(Fe)


def hall(E0, Fe):
    """Return Hall conductance in siemens."""

    return 18 * E0**1.85 / (16 + E0**2) * np.sqrt(Fe)


#%% Uncertainty

def peduncertainty(E0, Fe, dE0, dFe, varE0Fe):
    """Propagate E0 and Fe uncertainty into Pedersen conductance."""

    if Fe == 0:
        # The derivative is singular at zero flux. Use the same one-sided
        # excursion from Fe=0 to Fe=dFe as the current icBuilder code.
        dP = ped(E0, dFe)
    else:
        denominator = 16 + E0**2
        dP_dE0 = (
            40 / denominator - 80 * (E0 / denominator)**2
        ) * np.sqrt(Fe)
        dP_dFe = 40 * E0 / denominator / (2 * np.sqrt(Fe))
        dP = np.sqrt(
            dP_dE0**2 * dE0**2
            + dP_dFe**2 * dFe**2
            + 2 * dP_dE0 * dP_dFe * varE0Fe
        )

    return dP


def halluncertainty(E0, Fe, dE0, dFe, varE0Fe):
    """Propagate E0 and Fe uncertainty into Hall conductance."""

    if Fe == 0:
        dH = hall(E0, dFe)
    else:
        denominator = 16 + E0**2
        dH_dE0 = (
            18 * E0**0.85 / denominator
            * (1.85 - 2 * E0**2 / denominator)
            * np.sqrt(Fe)
        )
        dH_dFe = 9 * E0**1.85 / denominator / np.sqrt(Fe)
        dH = np.sqrt(
            dH_dE0**2 * dE0**2
            + dH_dFe**2 * dFe**2
            + 2 * dH_dE0 * dH_dFe * varE0Fe
        )

    return dH


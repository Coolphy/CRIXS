# %%
import numpy as np
from .peak import *
from .sigmoid import *


# %%
def Psd_Voigt_logistic(x, area, center, fwhm, mu, asym, bsym):
    """Psd_Voigt_logistic(x, area, center, fwhm, mu, asym"""

    w = fwhm * (1 + (logistic(x, asym, center, fwhm * bsym) - 0.5 * asym) * 2)
    return Psd_Voigt(x, area, center, w, mu)


# %%

# %%
import numpy as np
import scipy as sp


# %%
def erf_func(x, amplitude, center, sigma):
    """error_func(x, amplitude, center, sigma)"""
    return amplitude / 2 * (1 + sp.special.erf((x - center) / sigma / np.sqrt(2)))


def erf(x, amplitude, center, fwhm):
    """error_fwhm(x, amplitude, center, fwhm):"""

    # fwhm of gaussian
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))

    return erf_func(x, amplitude, center, sigma)


def logistic_func(x, amplitude, center, sigma):
    """logistic_func(x, amplitude, center, sigma)"""
    s = sigma * np.sqrt(3) / np.pi
    return amplitude / 2 * (1 + np.tanh((x - center) / (2 * s)))


def logistic(x, amplitude, center, fwhm):
    """logistic_fwhm(x, amplitude, center, fwhm)"""

    # # calculate fwhm
    # s = fwhm / np.log(3 + 2 * np.sqrt(2))

    # use fwhm in gaussian
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    s = sigma * np.sqrt(3) / np.pi

    return amplitude / 2 * (1 + np.tanh((x - center) / (2 * s)))


def arctan_func(x, amplitude, center, gamma):
    """arctan_func(x, amplitude, center, gamma)"""
    return amplitude / np.pi * np.arctan((x - center) / gamma) + 1 / 2


def arctan(x, amplitude, center, fwhm):
    """arctan_fwhm(x, amplitude, center, fwhm)"""

    # fwhm of lorentz
    gamma = fwhm / 2

    return amplitude / np.pi * np.arctan((x - center) / gamma) + 1 / 2


def heaviside(x, amplitude, center, halfwidth):

    y = np.zeros(len(x))
    for i, x in enumerate(x):
        if x <= center - halfwidth:
            y[i] = 0
        elif (x > center - halfwidth) & (x <= center + halfwidth):
            y[i] = amplitude / halfwidth / 2 * (x - center) + amplitude / 2

    return


# %%
def damped_sigmoid(x, amplitude, center, gamma):
    """ """
    pass

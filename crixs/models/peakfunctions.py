# %%
import numpy as np
from scipy.special import erf


# %%
def gaussian_func(x, amplitude, center, sigma):
    """gaussian_func(x, amplitude, center, sigma)"""
    return amplitude * np.exp(-((x - center) ** 2) / (2 * sigma**2))


def gaussian_area(x, area, center, sigma):
    """gaussian_area(x, area, center, sigma)"""
    amplitude = area / (np.sqrt(2 * np.pi) * sigma)
    return gaussian_func(x, amplitude, center, sigma)


def gaussian_fwhm(x, amplitude, center, fwhm):
    """gaussian_fwhm(x, amplitude, center, fwhm)"""
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return gaussian_func(x, amplitude, center, sigma)


def gaussian(x, area, center, fwhm):
    """gaussian(x, area, center, fwhm)"""
    amplitude = area / (np.sqrt(2 * np.pi) * sigma)
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return gaussian_func(x, amplitude, center, sigma)


def lorentz_func(x, amplitude, center, gamma):
    """lorentz_func(x, amplitude, center, gamma)"""
    return amplitude * gamma**2 / ((x - center) ** 2 + gamma**2)


def lorentz_fwhm(x, amplitude, center, fwhm):
    """lorentz_fwhm(x, amplitude, center, fwhm)"""
    gamma = fwhm
    return lorentz_func(x, amplitude, center, gamma)


def lorentz_area(x, area, center, gamma):
    """lorentz_area(x, area, center, gamma)"""
    amplitude = area / gamma / np.pi
    return lorentz_func(x, amplitude, center, gamma)


def lorentz(x, area, center, fwhm):
    """lorentz(x, area, center, fwhm)"""
    gamma = fwhm / 2
    amplitude = area / gamma / np.pi
    return lorentz_func(x, amplitude, center, gamma)


def Psd_Voigt(x, area, center, fwhm, mu):
    """Psd_Voigt(x, area, center, fwhm, mu)"""
    return area * (
        mu * lorentz(x, area, center, fwhm) + (1 - mu) * gaussian(x, area, center, fwhm)
    )


def Psd_Voigt2(x, area, center, wl, wg, mu):
    """
    Psd_Voigt2(x,area,center,wl,wg,mu)
    """
    return area * (
        mu * lorentz_area(x, area, center, wl)
        + (1 - mu) * gaussian(x, area, center, wg)
    )


# %%

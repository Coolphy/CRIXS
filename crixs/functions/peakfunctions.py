# %%
import numpy as np
from scipy.special import erf


# %%
def gaussian(x, amplitude, center, sigma):
    return amplitude * np.exp(-((x - center) ** 2) / (2 * sigma**2))


def gaussian_area(x, area, center, sigma):
    amplitude = area / (np.sqrt(2 * np.pi) * sigma)
    return gaussian(x, amplitude, center, sigma)


def gaussian_fwhm(x, amplitude, center, fwhm):
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return gaussian(x, amplitude, center, sigma)


def gaussian_area_fwhm(x, area, center, fwhm):
    amplitude = area / (np.sqrt(2 * np.pi) * sigma)
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return gaussian(x, amplitude, center, sigma)


def lorentz(x, amplitude, center, fwhm):
    gamma = fwhm / 2
    return amplitude * gamma**2 / ((x - center) ** 2 + gamma**2)


def lorentz_area(x, area, center, fwhm):
    gamma = fwhm / 2
    amplitude = area / gamma / np.pi
    return lorentz(x, amplitude, center, fwhm)


def Psd_Voigt(x, area, center, fwhm, mu):
    return area * (
        mu * lorentz_area(x, area, center, fwhm)
        + (1 - mu) * gaussian_area_fwhm(x, area, center, fwhm)
    )


def Psd_Voigt2(
    x,
    area,
    center,
    wl,
    wg,
    mu,
):
    return area * (
        mu * lorentz_area(x, area, center, wl)
        + (1 - mu) * gaussian_area_fwhm(x, area, center, wg)
    )


def error_function(x, amplitude, center, sigma):
    return amplitude / 2 * (1 + erf((x - center) / sigma / np.sqrt(2)))


def error_fwhm(x, amplitude, center, fwhm):
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return error_function(x, amplitude, center, sigma)


def sigmoid(x, amplitude, center, sigma):
    return (
        amplitude / 2 * (1 + np.tanh((x - center) / (2 * np.sqrt(3) / np.pi * sigma)))
    )


def arctan_fwhm(x, amplitude, center, fwhm):
    gamma = fwhm / 2
    return amplitude / np.pi * np.arctan((x - center) / gamma) + 1 / 2


# %%

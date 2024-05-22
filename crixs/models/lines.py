import numpy as np
from scipy.special import erf


def erf_func(x, amplitude, center, sigma):
    """error_func(x, amplitude, center, sigma)"""
    return amplitude / 2 * (1 + erf((x - center) / sigma / np.sqrt(2)))


def my_erf(x, amplitude, center, fwhm):
    """error(x, amplitude, center, fwhm):"""

    # fwhm of gaussian
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))

    return erf_func(x, amplitude, center, sigma)


def sigmoid_func(x, amplitude, center, sigma):
    """sigmoid_func(x, amplitude, center, sigma)"""
    s = sigma * np.sqrt(3) / np.pi
    return amplitude / 2 * (1 + np.tanh((x - center) / (2 * s)))


def sigmoid(x, amplitude, center, fwhm):
    """sigmoid_fwhm(x, amplitude, center, fwhm)"""

    # # calculate fwhm
    # s = fwhm / np.log(3 + 2 * np.sqrt(2))

    # use fwhm in gaussian
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    s = sigma * np.sqrt(3) / np.pi

    return amplitude / 2 * (1 + np.tanh((x - center) / (2 * s)))


def arctan_func(x, amplitude, center, gamma):
    """arctan_func(x, amplitude, center, gamma)"""
    return amplitude / np.pi * np.arctan((x - center) / gamma) + 1 / 2


def arctan_fwhm(x, amplitude, center, fwhm):
    """arctan_fwhm(x, amplitude, center, fwhm)"""

    # fwhm of lorentz
    gamma = fwhm / 2

    return amplitude / np.pi * np.arctan((x - center) / gamma) + 1 / 2

# %%
import numpy as np
from scipy import signal


# %%
def resolution_func(x, center, fwhm):
    sigma = fwhm / 2 / np.sqrt(2 * np.log(2))
    return (
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((x - center) ** 2 / 2 / sigma**2))
    )


def bose(x, T):
    """
    Change to '+' to avoid divergency
    """
    kbt = 8.617e-5 * T
    # return 1 - np.exp(-x / kbt)
    return 1 + np.exp(-x / kbt)


# def dho(x, area, omega1, gamma, T):

#     '''
#     center = omega1
#     width = gamma
#     height = a * area / gamma / np.pi

#     physical meaning:
#     undampedenergy omega0 = np.sqrt(omega1**2 + (gamma / 2) ** 2)
#     amplitude = area / np.pi * 2 * omega1
#     dampingratio = gamma / 2 / omega0 # overdamped >1, underdamped <1
#     this function only valid for underdamped
#     '''

#     return (
#         area
#         / (np.pi)
#         / bose(x, T)
#         * (
#             gamma / 2 / ((x - omega1) ** 2 + (gamma / 2) ** 2)
#             - gamma / 2 / ((x + omega1) ** 2 + (gamma / 2) ** 2)
#         )
#     )


def dho_func(x, amplitude, omega0, gamma, T):
    """
    center = np.sqrt(omega0**2 - (gamma / 2) ** 2)
    area = amplitude * np.pi / 2 / center !!!
    width = gamma
    height = a * area / gamma / np.pi

    dampingratio = gamma / 2 / omega0 # overdamped >1, underdamped <1
    """

    return (
        amplitude
        / bose(x, T)
        * (x * gamma)
        / ((x**2 - omega0**2) ** 2 + x**2 * gamma**2)
    )


def dho(x, area, center, width, resolution, T):
    y1 = resolution_func(x, np.mean(x), resolution)
    y2 = dho_func(x, area, center, width)
    y = signal.convolve(y1, y2, "same") * (abs(x[-1] - x[0]) / len(x))
    return y

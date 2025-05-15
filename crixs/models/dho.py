# %%
import numpy as np
from scipy import signal
from scipy import interpolate


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


# def dho_func(x, area, omega1, gamma, T):

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


def dho(x, area, center, width, resolution, T=20):
    """dho(x, area, center, width, resolution, T)"""

    x_int = np.linspace(x[0], x[-1], int(1000 / center))

    y1 = dho_func(x_int, area, center, width, T)
    y2 = resolution(x_int, np.mean(x), resolution)
    y = signal.convolve(y1, y2, "same") * abs(x_int[1] - x_int[0])

    f = interpolate.interp1d(x_int, y)
    y = f(x)

    return y

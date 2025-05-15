import math
import numpy as np
import scipy as sp

__all__ = ["Spectrum", "ADRESS"]


class Spectrum:

    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)


class ADRESS:
    def __init__(self):
        pass

    def add(self, spec1, spec2):
        f = sp.interpolate.interp1d(
            spec2.x, spec2.y, bounds_error=None, fill_value="extrapolate"
        )
        new = f(spec1.x)

        return Spectrum(spec1.x, spec1.y + new)

    def sub(self, spec1, spec2):
        f = sp.interpolate.interp1d(
            spec2.x, spec2.y, bounds_error=None, fill_value="extrapolate"
        )
        new = f(spec1.x)

        return Spectrum(spec1.x, spec1.y - new)

    def multi(self, spec1, factor):

        return Spectrum(spec1.x, spec1.y * factor)

    def chop(self, spec, rang):

        mask = (spec.x > rang[0]) & (spec.x < rang[1])

        return Spectrum(spec.x[mask], spec.y[mask])

    def bining(self, spec, bins=1):

        new_lens = math.floor(len(spec.x) / bins)
        bin_x = np.zeros(new_lens)
        bin_y = np.zeros(new_lens)
        for i in range(new_lens):
            bin_x[i] = np.mean(spec.x[i * bins : (i + 1) * bins])
            bin_y[i] = np.mean(spec.y[i * bins : (i + 1) * bins])

        return Spectrum(bin_x, bin_y)

    def corr_xaxis(self, spec1, spec2):
        refData = spec1.y
        uncorrData = spec2.y
        corr = sp.signal.correlate(refData, uncorrData)  # consider full pattern
        lags = sp.signal.correlation_lags(len(refData), len(uncorrData))
        lag = lags[np.argmax(corr)]

        corrData = np.roll(uncorrData, lag)
        return Spectrum(spec1.x, corrData)

    def mesh(self, x, y, I_RMU, I_TFY, I_TEY):
        if abs(x[1] - x[0]) > 0.0001:
            print("fix y scan")
            x_int = x[1] - x[0]
            x_steps = 1
            for i in range(len(x)):
                if abs(x[i + 1] - x[i]) < abs(x_int * 2):
                    x_steps += 1
                else:
                    break
            y_steps = round(len(x) / x_steps)

            x_center = np.linspace(np.min(x), np.max(x), x_steps)
            y_center = np.linspace(np.min(y), np.max(y), y_steps)

        else:
            print("fix x scan")

            "exchange axis,"
            xt = x
            x = y
            y = xt

            x_int = x[1] - x[0]
            x_steps = 1
            for i in range(len(x)):
                if abs(x[i + 1] - x[i]) < abs(x_int * 2):
                    x_steps += 1
                else:
                    break
            y_steps = round(len(x) / x_steps)

            x_center = np.linspace(np.min(x), np.max(x), x_steps)
            y_center = np.linspace(np.min(y), np.max(y), y_steps)

        if len(I_RMU) < x_steps * y_steps:
            pad_size = x_steps * y_steps - len(I_RMU)
            # You can choose what values to pad with, here we use 0
            I_RMU = np.pad(
                I_RMU, (0, pad_size), mode="constant", constant_values=np.nan
            )
            I_TFY = np.pad(
                I_TFY, (0, pad_size), mode="constant", constant_values=np.nan
            )
            I_TEY = np.pad(
                I_TEY, (0, pad_size), mode="constant", constant_values=np.nan
            )
        elif len(I_RMU) > x_steps * y_steps:
            I_RMU = I_RMU[: x_steps * y_steps]
            I_TEY = I_TEY[: x_steps * y_steps]
            I_TFY = I_TFY[: x_steps * y_steps]
        else:
            print("data complete")

        RMU = I_RMU.reshape(y_steps, x_steps)
        TFY = I_TFY.reshape(y_steps, x_steps)
        TEY = I_TEY.reshape(y_steps, x_steps)

        print(np.shape(x_center), np.shape(y_center))
        print(np.shape(RMU))

        return y_center, x_center, RMU, TFY, TEY

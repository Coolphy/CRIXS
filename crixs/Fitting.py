# %%
import numpy as np
import lmfit as lf

from .Spectrum import Spectrum

from .models import *


# %%
class Fitting:

    def __init__(self):
        """
        Shell of lmfit.Model
        """
        self._spectrum = Spectrum()
        self._model = None
        self._params = None
        self._out = None
        self._result = {}

    def modeling(self, *args, **kwargs):
        """
        model = Model(function,prefix='Name')
        """

        mod = lf.Model(*args, **kwargs)

        if self._model is None:
            self._model = mod
            self._params = mod.make_params()
        else:
            self._model += mod
            self._params += mod.make_params()

        self.init()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if isinstance(model, lf.Model):
            self._model = model
        else:
            raise ValueError("Unacceptable")

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, *params):
        if len(params) == 1 and isinstance(params[0], lf.Parameters):
            self._update(params[0])
        else:
            raise ValueError("Unacceptable")

    @property
    def spectrum(self):
        return self._spectrum

    @spectrum.setter
    def spectrum(self, spectrum):
        if isinstance(spectrum, Spectrum):
            self._spectrum = spectrum
        else:
            raise ValueError("Unacceptable")

    def init(self, *params):
        """
        Initialize with lmfit parameters
        """
        for param in self._params.values():
            param.set(value=1)
        if len(params) == 0:
            pass
        elif len(params) == 1 and isinstance(params[0], lf.Parameters):
            self._update(params[0])
        else:
            raise ValueError("Unacceptable")

    def _update(self, params):
        """
        accept Parameters, dictionaray of parameter
        """
        if isinstance(params, lf.Parameters):
            self._params.update(params)
        elif isinstance(params, dict):
            params_init = lf.Parameters()
            for param_name, param in params.items():
                kwargs = {}
                if "value" in param:
                    kwargs["value"] = param["value"]
                if "vary" in param:
                    kwargs["vary"] = param["vary"]
                if "min" in param:
                    kwargs["min"] = param["min"]
                if "max" in param:
                    kwargs["max"] = param["max"]
                if "expr" in param:
                    kwargs["expr"] = param["expr"]
                if "brute_step" in param:
                    kwargs["brute_step"] = param["brute_step"]

                params_init.add(param_name, **kwargs)
            self._params.update(params_init)
        else:
            raise ValueError("Unknown input")

    def fit(self, *spec):
        """
        fit spectrum with model
        """
        if len(spec) == 0:
            self._out = self._model.fit(
                self._spectrum.y, self._params, x=self._spectrum.x
            )
        elif len(spec) == 1 and isinstance(spec[0], Spectrum):
            self._spectrum = spec[0]
            self._out = self._model.fit(
                self._spectrum.y, self._params, x=self._spectrum.x
            )
        else:
            raise ValueError("Input must be a spectrum")

    def out(self, *name):
        """
        get fitting output line
        out = Fitting.out('Name')
        """
        if len(name) == 0:
            dely = self._out.eval_uncertainty(x=self._spectrum.x, sigma=1)
            return Spectrum(
                x=self._spectrum.x,
                y=self._out.best_fit,
                err=dely,
                mon=self._spectrum.mon,
            )
        elif len(name) == 1:
            comps = self._out.eval_components(x=self._spectrum.x)
            dely = self._out.eval_uncertainty(x=self._spectrum.x, sigma=1)
            return Spectrum(
                x=self._spectrum.x,
                y=comps[name[0]],
                err=self._out.dely_comps[name[0]],
                mon=self._spectrum.mon,
            )
        else:
            raise ValueError("Unknown input!")

    @property
    def result(self):
        """
        put fitting results of parameters into a dictionary
        """
        for name, param in self._out.params.items():
            self._result[name] = {}
            self._result[name]["value"] = param.value
            self._result[name]["stderr"] = param.stderr

        return self._result


# %%
if __name__ == "__main__":

    import numpy as np

    def func(x, a, b):
        return a * x + b

    ft = Fitting()

    ft.modeling(func, prefix="g_")

    Params_init = {
        "gb": {"value": 0},
    }

    ft.init(Params_init)

    x = np.linspace(-1, 1, 100)
    y = np.cos(x)
    ss = Spectrum(x, y)

    ft.fit(ss)

    result = ft.result

    line = ft.out()
# %%

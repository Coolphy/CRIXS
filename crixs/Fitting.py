# %%
import numpy as np
import lmfit as lf

from Spectrum import Spectrum

from models import *


# %%
class Fitting:

    def __init__(self):
        """
        A shell of lmfit model

        ft = Fitting()

        ft.model(function,prefix=name)

        ft.init(Params_init)

        ft.fit(Spectrum)

        fiting result = ft.result()

        fitted spectrum = ft.out(name)

        """
        self._data = Spectrum()
        self._model = None
        self._params = None
        self._out = None
        self._result = {}

    def modeling(self, *args, **kwargs):
        """
        Shell of lmfit.Model

        model = Model(function,prefix='Name')
        """

        mod = lf.Model(*args, **kwargs)

        if self._model is None:
            self._model = mod
            self._params = mod.make_params()
        else:
            self._model += mod
            self._params += mod.make_params()

        for param in self._params.values():
            param.set(value=1)

    @property
    def model(self):
        """
        copy of Parameters in lmfit
        """
        return self._model

    @property
    def params(self):
        """
        copy of Parameters in lmfit
        """
        return self._params

    def init(self, params, *args, **kwargs):
        """
        Initialize with lmfit parameters
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

                params_init.add(param_name, **kwargs)

            self._params.update(params_init)
        else:
            raise ValueError("Unknown input")

    def fit(self, spec):
        """
        fit spectrum with model
        """
        if isinstance(spec, Spectrum):
            self._data = spec
            print(self._data)
            self._out = self._model.fit(self._data.y, self._params, x=self._data.x)
        else:
            raise ValueError("Input must be a spectrum")

    def out(self, *name):
        """
        get fitting output
        out = Fitting.out('Name')
        """
        if len(name) == 0:
            dely = self._out.eval_uncertainty(self._params, x=self._data.x, sigma=1)
            return Spectrum(
                x=self._data.x,
                y=self._out.best_fit,
                err=dely,
                mon=self._data.mon,
            )
        else:
            comps = self._out.eval_components(self._params, x=self._data.x)
            dely = self._out.eval_uncertainty(self._params, x=self._data.x, sigma=1)
            if not hasattr(self._out, "dely_comps"):
                return Spectrum(
                    x=self._data.x,
                    y=self._out.best_fit,
                    err=dely,
                    mon=self._data.mon,
                )
            else:
                return Spectrum(
                    x=self._data.x,
                    y=comps[name[0]],
                    err=self._out.dely_comps[name[0]],
                    mon=self._data.mon,
                )

    @property
    def result(self):
        """
        get fitting results of parameters
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

    # Params_init = {
    #     "gb": {"value": 0},
    # }

    ft.init(Params_init)

    x = np.linspace(-1, 1, 100)
    y = np.cos(x)
    ss = Spectrum(x, y)

    ft.fit(ss)

    result = ft.result

    line = ft.out()
# %%

from .Spectrum import Spectrum
from .Fitting import Fitting


class Spectrum(Spectrum):
    """
    Initialize:
        >>> ss = Spectrum(x, y)
        >>> ss = Spectrum(x=x, y=y, err=err, mon=mon)
    """

    pass


class Fitting(Fitting):
    """
    Initialize:
        >>> ft = Fitting()

    Usage:
        >>> ft.modeling(function,prefix=name)
        >>> ft.init(Params_init)
        >>> ft.fit(Spectrum)

    Output:
        >>> ft.result = ft.result
        >>> ft.output = ft.out(name)
    """

    pass

# %%
import numpy as np
from .backpack import arraymanip


# %%
class Spectrum:
    """
    Args:
        x : x values (1D list/array).
        y : y values (1D list/array).
        err : stderr values (1D list/array).
        mon : monitor values (1D list/array).
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize:

            **Empty**

            >>> s = br.Spectrum()

            **From array**

            y array like
            x,err,mon array like (optional)

            >>> s = br.Spectrum(y)
            >>> s = br.Spectrum(x, y)
            >>> s = br.Spectrum(x, y, err, mon)

            >>> s = br.Spectrum(y=y)
            >>> s = br.Spectrum(x=x, y=y)
            >>> s = br.Spectrum(x=x, y=y, err=err, mon=mon)

            >>> s = br.Spectrum(y, x=x, err=err, mon=mon)
        """

        self._x = np.array([], dtype="float")
        self._y = np.array([], dtype="float")
        self._err = np.array([], dtype="float")
        self._mon = np.array([], dtype="float")

        error_message = "Initialize error"
        if len(args) > 4 or len(args) == 3 or len(kwargs) > 4:
            raise ValueError(error_message)
        if any([item not in ["x", "y", "err", "mon"] for item in kwargs.keys()]):
            raise ValueError(error_message)

        if len(args) == 1:
            self._y = np.array(args[0], dtype="float")
            self._x = np.arange(len(self._y), dtype="float")
            self._err = np.sqrt(np.abs(self._y))
            self._mon = np.ones(len(self._y), dtype="float")

            if "x" in kwargs:

                if len(kwargs["x"]) == len(self._y):
                    self._x = np.array(kwargs["x"], dtype="float")
                else:
                    raise ValueError("x and y not match")

            if "err" in kwargs:

                if len(kwargs["err"]) == len(self._y):
                    self._err = np.array(kwargs["err"], dtype="float")
                else:
                    raise ValueError("y and err not match")

            if "mon" in kwargs:

                if len(kwargs["mon"]) == len(self._y):
                    self._mon = np.array(kwargs["mon"], dtype="float")
                else:
                    raise ValueError("y and mon not match")

            return

        elif len(args) == 2:
            if len(args[0]) == len(args[1]):
                self._x = np.array(args[0], dtype="float")
                self._y = np.array(args[1], dtype="float")
                self._err = np.sqrt(np.abs(self._y))
                self._mon = np.ones(len(self._y), dtype="float")

                if "err" in kwargs:

                    if len(kwargs["err"]) == len(self._y):
                        self._err = np.array(kwargs["err"], dtype="float")
                    else:
                        raise ValueError("y and err not match")

                if "mon" in kwargs:

                    if len(kwargs["mon"]) == len(self._y):
                        self._mon = np.array(kwargs["mon"], dtype="float")
                    else:
                        raise ValueError("y and mon not match")

                return

            else:
                raise ValueError("x and y not match")

        elif len(args) == 4:
            if len(args[0]) == len(args[1]) == len(args[2]) == len(args[3]):
                self._x = np.array(args[0], dtype="float")
                self._y = np.array(args[1], dtype="float")
                self._err = np.array(args[2], dtype="float")
                self._mon = np.array(args[3], dtype="float")
                return

            else:
                raise ValueError("x and y not match")

        elif len(args) == 0 and "y" in kwargs:

            self._y = np.array(kwargs["y"], dtype="float")
            self._x = np.arange(len(self._y), dtype="float")
            self._err = np.sqrt(np.abs(self._y))
            self._mon = np.ones(len(self._y), dtype="float")

            if "x" in kwargs:

                if len(kwargs["x"]) == len(kwargs["y"]):
                    self._x = np.array(kwargs["x"], dtype="float")
                else:
                    raise ValueError("x and y not match")

            if "err" in kwargs:

                if len(kwargs["err"]) == len(kwargs["y"]):
                    self._err = np.array(kwargs["err"], dtype="float")
                else:
                    raise ValueError("y and err not match")

            if "mon" in kwargs:

                if len(kwargs["mon"]) == len(kwargs["y"]):
                    self._mon = np.array(kwargs["mon"], dtype="float")
                else:
                    raise ValueError("y and mon not match")

            self._y = np.array(kwargs["y"], dtype="float")
            return

    @property
    def x(self):
        return self._x + 0

    @x.setter
    def x(self, value):
        if isinstance(value, (float, int)):
            value = [value]
            if len(value) == len(self._x):
                self._x = np.array(value, dtype="float")
            else:
                raise ValueError("Can not change to different length.\n")

    @property
    def y(self):
        return self._y + 0

    @y.setter
    def y(self, value):
        if isinstance(value, (float, int)):
            value = [value]
            if len(value) == len(self._y):
                self._y = np.array(value, dtype="float")
            else:
                raise ValueError("Can not change to different length.\n")

    @property
    def err(self):
        return self._err + 0

    @err.setter
    def err(self, value):
        if isinstance(value, (float, int)):
            value = [value]
            if len(value) == len(self._err):
                self._err = np.array(value, dtype="float")
            else:
                raise ValueError("Can not change to different length.\n")

    @property
    def mon(self):
        return self._mon + 0

    @mon.setter
    def mon(self, value):
        if isinstance(value, (float, int)):
            value = [value]
            if len(value) == len(self._mon):
                self._mon = np.array(value, dtype="float")
            else:
                raise ValueError("Can not change to different length.\n")

    def __len__(self):
        if self._y is None:
            raise ValueError("No spectrum yet.\n")
        else:
            return len(self._y)

    def __add__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                final = Spectrum(
                    x=self._x,
                    y=self._y + object.y,
                    err=np.sqrt(self._err**2 + object.err**2),
                    mon=self._mon + object.mon,
                )
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(
                    x=self._x, y=self._y + object, err=self._err, mon=self._mon
                )
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(
                x=self._x, y=self._y + object, err=self._err, mon=self._mon
            )
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __sub__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(
                self._x, object.x
            ) and arraymanip.check_array_same(self._mon, object.mon):
                final = Spectrum(
                    x=self._x,
                    y=self._y - object.y,
                    err=np.sqrt(self._err**2 + object.err**2),
                    mon=(self._mon + object.mon) / 2,
                )
            else:
                raise ValueError("Spectrum is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(
                    x=self._x, y=self._y - object, err=self._err, mon=self._mon
                )
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(
                x=self._x, y=self._y - object, err=self._err, mon=self._mon
            )
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __mul__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                final = Spectrum(
                    x=self._x,
                    y=self._y * object.y,
                    err=np.sqrt(
                        (np.mean(object.y) * self._err) ** 2
                        + (np.mean(self._y) * object.err) ** 2
                    ),
                    mon=self._mon * object.mon,
                )
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(
                    x=self._x,
                    y=self._y * object,
                    err=self._err * object,
                    mon=self._mon * object,
                )
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(
                x=self._x,
                y=self._y * object,
                err=self._err * object,
                mon=self._mon * object,
            )
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __turediv__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                if 0 in object.y:
                    raise ValueError("ZeroDivisionError.\n")
                else:
                    final = Spectrum(
                        x=self._x,
                        y=self._y / object.y,
                        err=np.sqrt(
                            (self._err / np.mean(object.y)) ** 2
                            + (np.mean(self._y) * object.err / np.mean(object.y) ** 2)
                            ** 2
                        ),
                        mon=self._mon / object.mon,
                    )
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                if 0 in object.y:
                    raise ValueError("ZeroDivisionError.\n")
                else:
                    final = Spectrum(
                        x=self._x,
                        y=self._y / object,
                        err=self._err / object,
                        mon=self._mon / object,
                    )
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(
                x=self._x,
                y=self._y / object,
                err=self._err / object,
                mon=self._mon / object,
            )
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __getitem__(self, item):
        """
        get sliced Spectrum by x axis
        """
        if isinstance(item, slice):
            start = item.start
            stop = item.stop
            step = item.step

            if start is None:
                start = self._x[0]
            if stop is None:
                stop = self._x[-1]
            if step is None:
                step = 1

            indices = [i for i, val in enumerate(self.x) if start <= val < stop]

            x = np.array([self._x[i] for i in indices[::step]])
            y = np.array([self._y[i] for i in indices[::step]])
            err = np.array([self._err[i] for i in indices[::step]])
            mon = np.array([self._mon[i] for i in indices[::step]])

            return Spectrum(x=x, y=y, err=err, mon=mon)

        elif isinstance(item, (int, float)):
            # Single value
            nearest_index = None
            min_diff = float("inf")

            # Calculate x step size
            x_step = abs(self._x[1] - self._x[0])

            for i in range(len(self._x)):
                diff = abs(self._x[i] - item)
                if diff < min_diff:
                    min_diff = diff
                    nearest_index = i

            # Check if the difference is within 1% of x step
            if nearest_index is not None and min_diff <= 0.01 * x_step:
                x = np.array([self._x[nearest_index]])
                y = np.array([self._y[nearest_index]])
                err = np.array([self._err[nearest_index]])
                mon = np.array([self._mon[nearest_index]])

                return Spectrum(x=x, y=y, err=err, mon=mon)

            else:
                raise ValueError("x value not found")

        else:
            raise ValueError(
                "Index must be a slice or a single value, not {}".format(
                    type(item).__name__
                )
            )

    def _append_static(combined_x, combined_y, combined_err, combined_mon, *args):

        for arg in args:
            if isinstance(arg, Spectrum):
                combined_x = np.append(combined_x, arg._x)
                combined_y = np.append(combined_y, arg._y)
                combined_err = np.append(combined_err, arg._err)
                combined_mon = np.append(combined_mon, arg._mon)
            elif isinstance(arg, list):
                for spectrum in arg:
                    if isinstance(spectrum, Spectrum):
                        combined_x = np.append(combined_x, spectrum._x)
                        combined_y = np.append(combined_y, spectrum._y)
                        combined_err = np.append(combined_err, spectrum._err)
                        combined_mon = np.append(combined_mon, spectrum._mon)
                    else:
                        raise ValueError("Can only append Spectrum objects.")
            else:
                raise ValueError("Can only append Spectrum objects.")

        return Spectrum(x=combined_x, y=combined_y, err=combined_err, mon=combined_mon)

    # def append(self, *args):
    #     """
    #     Append multiple Spectrum objects together to the current instance.
    #     """
    #     combined_x = np.copy(self._x)
    #     combined_y = np.copy(self._y)
    #     combined_err = np.copy(self._err)
    #     combined_mon = np.copy(self._mon)

    #     return self._append_static(
    #         combined_x, combined_y, combined_err, combined_mon, *args
    #     )

    @classmethod
    def append(cls, *args):
        """
        Create a new Spectrum instance with the data appended together.
        """
        combined_x = np.array([])
        combined_y = np.array([])
        combined_err = np.array([])
        combined_mon = np.array([])

        return cls._append_static(
            combined_x, combined_y, combined_err, combined_mon, *args
        )

    # def normalize(self):
    #     final = Spectrum(
    #         x=self._x,
    #         y=self._y / self._mon,
    #         err=self._err / self._mon,
    #         mon=self._mon / self._mon,
    #     )
    #     return final

    @classmethod
    def normalize(cls, object):
        if isinstance(object, Spectrum):
            final = Spectrum(
                x=object._x,
                y=object._y / object._mon,
                err=object._err / object._mon,
                mon=object._mon / object._mon,
            )
        return final


# %%
if __name__ == "__main__":
    pass
    ss = Spectrum
    s1 = ss([0, 1])
    s2 = ss([10, 20])
    s3 = ss.append(s1, s2)
    s4 = ss.normalize(s3)
# %%

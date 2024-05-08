# %%
import numpy as np

import Meta
from .backpack import arraymanip


# %%
class Spectrum(metaclass=Meta._Meta):
    """
     Returns a ``Spectrum`` object.

    Args:
        x (list or array, optional): x values (1D list/array).
        y (list or array, optional): y values (1D list/array).

    How to initialize a Spectrum object:
        **Empty**

            >>> s = br.Spectrum()

        **From array**

            >>> s = br.Spectrum(x, y)
            >>> s = br.Spectrum(y)
            >>> s = br.Spectrum(x=x, y=y)
            >>> s = br.Spectrum(y=y)

        where ``x`` and ``y`` are 1D arrays (or list). If only y data is passed, a dummy
        x-array will be set.

    Attributes:
        x (array): vector with x-coordinate values
        y (array): vector with y-coordinate values
        filepath (str or pathlib.Path): filepath associated with data.

    """

    def __init__(self, *args, **kwargs):

        self._x = np.array([], dtype="float")
        self._y = np.array([], dtype="float")

        error_message = "Can not generate spectrum"
        if len(args) > 2 or len(kwargs) > 2:
            raise ValueError(error_message)
        if any([item not in ["x", "y"] for item in kwargs.keys()]):
            raise ValueError(error_message)

        if len(args) == 1:
            self._y = np.array(args[0], dtype="float")
            self._x = np.arange(len(self._y), dtype="float")
            return
        elif len(args) == 2:
            self._x = np.array(args[0], dtype="float")
            self._y = np.array(args[1], dtype="float")
            return

        if "y" in kwargs:
            if "x" in kwargs:
                self._x = np.array(kwargs["x"], dtype="float")
            self._y = np.array(kwargs["y"], dtype="float")
            return

    def __len__(self):
        if self._x is None:
            raise ValueError("No spectrum yet.\n")
        else:
            return len(self._x)

    def __add__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                final = Spectrum(x=self._x, y=self._y + object.y)
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(x=self._x, y=self._y + object)
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(x=self._x, y=self._y + object)
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __sub__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                final = Spectrum(x=self._x, y=self._y - object.y)
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(x=self._x, y=self._y - object)
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(x=self._x, y=self._y - object)
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __mul__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                final = Spectrum(x=self._x, y=self._y * object.y)
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                final = Spectrum(x=self._x, y=self._y * object)
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(x=self._x, y=self._y * object)
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    def __turediv__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self._x, object.x):
                if 0 in object.y:
                    raise ValueError("ZeroDivisionError.\n")
                else:
                    final = Spectrum(x=self._x, y=self._y / object.y)
            else:
                raise ValueError("Spectrum x is different.\n")

        elif isinstance(object, np.floating):
            if len(self._y) == len(object):
                if 0 in object.y:
                    raise ValueError("ZeroDivisionError.\n")
                else:
                    final = Spectrum(x=self._x, y=self._y / object)
            else:
                raise ValueError("Spectrum length is different.\n")

        elif isinstance(object, (float, int)):
            final = Spectrum(x=self._x, y=self._y / object)
        else:
            raise ValueError(f"Cannot operate type {type(object)} with type Spectrum")

        return final

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if len(value) == len(self._x):
            self._x = np.array(value, dtype="float")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if len(value) == len(self._y):
            self._y = np.array(value, dtype="float")

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

            x = [self._x[i] for i in indices[::step]]
            y = [self._y[i] for i in indices[::step]]

            return Spectrum(x=x, y=y)

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
                x = self._x[nearest_index]
                y = self._y[nearest_index]

                s = Spectrum(x=x, y=y)
                return s

            else:
                raise ValueError("x value not found")

        else:
            raise ValueError(
                "Index must be a slice or a single value, not {}".format(
                    type(item).__name__
                )
            )

    def append(self, *args):
        """
        Append multiple Spectrum objects together to the current instance.
        """
        combined_x = np.copy(self._x)
        combined_y = np.copy(self._y)

        for arg in args:
            if isinstance(arg, Spectrum):
                combined_x = np.append(combined_x, arg._x)
                combined_y = np.append(combined_y, arg._y)
            elif isinstance(arg, list):
                for spectrum in arg:
                    if isinstance(spectrum, Spectrum):
                        combined_x = np.append(combined_x, spectrum._x)
                        combined_y = np.append(combined_y, spectrum._y)
                    else:
                        raise ValueError("Can only append Spectrum objects.")
            else:
                raise ValueError("Can only append Spectrum objects.")

        return Spectrum(combined_x, combined_y)

    @classmethod
    def append(cls, *args):
        """
        Create a new Spectrum instance with the data appended together.
        """
        combined_x = np.array([])
        combined_y = np.array([])

        for arg in args:
            if isinstance(arg, Spectrum):
                combined_x = np.append(combined_x, arg._x)
                combined_y = np.append(combined_y, arg._y)
            elif isinstance(arg, list):
                for spectrum in arg:
                    if isinstance(spectrum, Spectrum):
                        combined_x = np.append(combined_x, spectrum._x)
                        combined_y = np.append(combined_y, spectrum._y)
                    else:
                        raise ValueError("Can only append Spectrum objects.")
            else:
                raise ValueError("Can only append Spectrum objects.")

        return cls(combined_x, combined_y)


# %%

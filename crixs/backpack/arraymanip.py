import numpy as np


def check_array_same(array_self, array_new, max_error=None):
    """
    Checks if two arrays are approximately the same within a specified maximum error.

    Parameters:
        array_self (array-like): First array to compare.
        array_new (array-like): Second array to compare.
        max_error (float): Maximum allowable relative error. Defaults to 0.1.

    Returns:
        bool: True if arrays are approximately the same within the maximum error, False otherwise.
    """
    # Set default value for max_error if not provided
    if max_error is None:
        max_error = 0.1

    # Type checking
    if not isinstance(array_self, (list, np.ndarray)) or not isinstance(
        array_new, (list, np.ndarray)
    ):
        raise TypeError("Both arrays must be array-like objects.")

    # Early exit if arrays have different lengths
    if len(array_self) != len(array_new):
        return False

    # Early exit if arrays are empty or have a single element
    if len(array_self) < 2:
        return True

    # Calculate step sizes for each array
    step1 = abs(np.mean(np.diff(array_self)))
    step2 = abs(np.mean(np.diff(array_new)))

    # Check if the difference in step sizes exceeds the maximum error
    if abs(step1 - step2) > max_error * step1:
        return False

    # Check if absolute differences between arrays exceed the maximum error
    abs_diff = np.abs(array_self - array_new)
    if np.any(abs_diff > max_error * step1):
        return False

    return True


def bin_array_binsize(array, bin_size):
    """
    Bins pixel array to the averages of each bin.

    Parameters:
        array (array-like): Input pixel array.
        bin_size (int): Size of each bin.

    Returns:
        numpy.ndarray: Binned pixel array averages.
    """
    # Input validation
    if not isinstance(bin_size, int) or bin_size <= 0:
        raise ValueError("bin_size must be a positive integer.")

    if not isinstance(array, (list, np.ndarray)):
        raise ValueError("array must be an array-like object.")

    if len(array) < bin_size:
        raise ValueError("bin_size cannot be greater than the length of array.")

    remainder = len(array) % bin_size

    # Handle remainder array points by truncating the array
    if remainder > 0:
        array = array[:-remainder]

    # Reshape array into bins
    binned_array = np.array(array).reshape(-1, bin_size)

    # Calculate mean of each bin and apply floor rounding
    bin_averages = np.mean(binned_array, axis=1)

    return bin_averages


def bin_array_binsize_sqrt(array, bin_size):
    """
    Bins the data based on the standard error being the square root of the data.

    Parameters:
        array (array-like): Input data to be binned.
        bin_size (int): Size of each bin.

    Returns:
        numpy.ndarray: Binned data.
    """
    # Input validation
    if not isinstance(bin_size, int) or bin_size <= 0:
        raise ValueError("bin_size must be a positive integer.")

    if not isinstance(array, (list, np.ndarray)):
        raise ValueError("array must be an array-like object.")

    if len(array) < bin_size:
        raise ValueError("bin_size cannot be greater than the length of array.")

    # Calculate remainder when dividing the length of the array by bin_size
    remainder = len(array) % bin_size

    # Handle remainder array points by truncating the array
    if remainder > 0:
        array = array[:-remainder]

    # Reshape array into bins and calculate squared values
    binned_array_squared = np.array(array).reshape(-1, bin_size) ** 2

    # Calculate mean of squared values in each bin and take the square root
    # This represents the standard deviation of the binned data
    bin_stddev = np.sqrt(np.mean(binned_array_squared, axis=1))

    return bin_stddev

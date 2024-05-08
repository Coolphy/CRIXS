import numpy as np

def check_array_same(array_self, array_new, max_error=None):
    if max_error is None:
        max_error = 0.1
    

    # Early exit if arrays have different lengths
    if len(array_self) != len(array_new):
        return False

    # Early exit if arrays are empty or have a single element
    if len(array_self) < 2:
        return True

    step1 = abs(np.mean(np.diff(array_self)))
    step2 = abs(np.mean(np.diff(array_new)))
    if abs(step1 - step2) > max_error * step1:
        return False

    # Check if differences exceed
    abs_diff = np.abs(array_self - array_new)
    if np.any(abs_diff > max_error * step1):
        return False

    return True
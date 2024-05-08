import copy


class _Meta(type):
    """
    Meta is a class type to pass data
    """

    def __init__(self):
        pass

    def __call__(self):
        # Create a deep copy of the current instance
        copy_instance = copy.deepcopy(self)
        # Delete the original instance
        # del self
        # Return the deep copy
        return copy_instance

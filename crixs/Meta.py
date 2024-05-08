import copy

class _Metadata(type):
    '''
    Meta is a class type to pass data
    '''
    def __init__(self):
        pass

    def __call__(self):
        # Create a deep copy of the current instance
        copy_instance = copy.deepcopy(self)
        # Delete the original instance
        # del self
        # Return the deep copy
        return copy_instance
    
class _Metaclass(type):
    """Metaclass to facilitate creation of read-only and non-removable attributes."""
    def __new__(self, class_name, bases, attrs):

        ###################
        # read only attrs #
        ###################
        def lazy_read_only(_attr):
            variable = '_' + _attr
            if not hasattr(self, variable):
                def getter(self):
                    return getattr(self, variable)
                def setter(self, value):
                    raise AttributeError('Attribute is "read only". Cannot set attribute.')
                def deleter(self):
                    raise AttributeError('Attribute is "read only". Cannot delete object.')
            return getter, setter, deleter#, 'read only attribute'

        #######################
        # non removable attrs #
        #######################
        def lazy_non_removable(_attr):
            variable = '_' + _attr
            if not hasattr(self, variable):
                def getter(self):
                    return getattr(self, variable)
                def setter(self, value):
                    return setattr(self, variable, value)
                def deleter(self):
                    raise AttributeError('Attribute cannot be deleted.')
            return getter, setter, deleter#, 'non-removable attribute'

        #################
        # reserved word #
        #################
        def lazy_reserved(_attr):
            variable = '_' + _attr
            if not hasattr(self, variable):
                def getter(self):
                    raise AttributeError(f'Cannot get attribute. `{_attr}` is a reserved word.')
                def setter(self, value):
                    raise AttributeError(f'Cannot set attribute. `{_attr}` is a reserved word.')
                def deleter(self):
                    raise AttributeError('Attribute cannot be deleted.')
            return getter, setter, deleter

        ################
        # create attrs #
        ################
        new_attrs = {}

        # if '_reserved' in attrs:
        #     print('reserved')
        #     for attr in attrs['_reserved']:
        #         print(attr)
        #         _property = property(*lazy_reserved(attr))
        #         new_attrs[attr] = _property
        if '_non_removable' in attrs:
            for attr in attrs['_non_removable']:
                _property = property(*lazy_non_removable(attr))
                new_attrs[attr] = _property
        if '_read_only' in attrs:
            for attr in attrs['_read_only']:
                _property = property(*lazy_read_only(attr))
                new_attrs[attr] = _property
        for name, value in attrs.items():
            if name not in ('_non_removable', '_read_only', '_reserved'):
                new_attrs[name] = value

        return type(class_name, bases, new_attrs)

# %%
import numpy as np

from Meta import _Metadata
from .backpack import arraymanip

# %%
class Spectrum(metaclass = _Metadata):
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

        self.x = None
        self.y = None

        error_message = "Can not generate spectrum"
        if len(args) > 2 or len(kwargs) > 2:
            raise ValueError(error_message)
        if any([item not in ['x', 'y'] for item in kwargs.keys()]):
            raise ValueError(error_message)
        
        if len(args) == 1:
            self.y = np.asarray(args[0])
            self.x = np.arange(len(self.y))
            return
        elif len(args) == 2:
            self.x = np.asarray(args[0])
            self.y = np.asarray(args[1])
            return

        if 'y' in kwargs:
            if 'x' in kwargs:
                self.x =  np.asarray(kwargs['x'])
            self.y = np.asarray(kwargs['y'])
            return
        

    def __len__(self):
        if self.x is None:
            raise ValueError('No spectrum yet.\n')         
        else:
            return len(self.x)

    def __add__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self.x, object.x):
                final = Spectrum(x=self.x, y=self.y + object.y)
            else:
                raise ValueError('Spectrum x is different.\n')   
            
        elif isinstance(object, np.floating): 
            if len(self.y) == len(object):
                final = Spectrum(x=self.x, y=self.y + object)
            else:
                raise ValueError('Spectrum length is different.\n')   
                
        elif isinstance(object, (float, int)):
            final = Spectrum(x=self.x, y=self.y + object)
        else:
            raise ValueError(f'Cannot operate type {type(object)} with type Spectrum')

        return final

    def __sub__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self.x, object.x):
                final = Spectrum(x=self.x, y=self.y - object.y)
            else:
                raise ValueError('Spectrum x is different.\n')   
            
        elif isinstance(object, np.floating): 
            if len(self.y) == len(object):
                final = Spectrum(x=self.x, y=self.y - object)
            else:
                raise ValueError('Spectrum length is different.\n')   
                
        elif isinstance(object, (float, int)):
            final = Spectrum(x=self.x, y=self.y - object)
        else:
            raise ValueError(f'Cannot operate type {type(object)} with type Spectrum')

        return final
    
    def __mul__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self.x, object.x):
                final = Spectrum(x=self.x, y=self.y * object.y)
            else:
                raise ValueError('Spectrum x is different.\n')   
            
        elif isinstance(object, np.floating): 
            if len(self.y) == len(object):
                final = Spectrum(x=self.x, y=self.y * object)
            else:
                raise ValueError('Spectrum length is different.\n')   
                
        elif isinstance(object, (float, int)):
            final = Spectrum(x=self.x, y=self.y * object)
        else:
            raise ValueError(f'Cannot operate type {type(object)} with type Spectrum')

        return final
    
    def __turediv__(self, object):
        if isinstance(object, Spectrum):
            if arraymanip.check_array_same(self.x, object.x):
                if 0 in object.y:
                    raise ValueError('ZeroDivisionError.\n')
                else:
                    final = Spectrum(x=self.x, y=self.y / object.y)
            else:
                raise ValueError('Spectrum x is different.\n')  
             

        elif isinstance(object, np.floating): 
            if len(self.y) == len(object):
                if 0 in object.y:
                    raise ValueError('ZeroDivisionError.\n')
                else:
                    final = Spectrum(x=self.x, y=self.y / object)
            else:
                raise ValueError('Spectrum length is different.\n')   
                
        elif isinstance(object, (float, int)):
            final = Spectrum(x=self.x, y=self.y / object)
        else:
            raise ValueError(f'Cannot operate type {type(object)} with type Spectrum')

        return final
            
    
# %%


from functools import wraps, partial
from typing import Callable

Class = type[object]

class MultiMethod(object):
    """Manage call signature map to actual functions.
    
    Based on Guido van Rossum's `Five-minute Multimethods in Python <https://www.artima.com/weblogs/viewpost.jsp?thread=101605>`_
    """
    name: str
    typemap: dict

    def __init__(self, name):
        self.name = name
        self.typemap = {}

    def __call__(self, *args):
        """Finds and calls the function which matches the given signature, returning the result."""
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)

    def register(self, types, function):
        """Register function signature."""
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function



class MultiMethodRegistry(object):
    """Registry to map function names to MuultiMethod instnaces"""

    _registry = {}   # class attribute

    @classmethod
    def register(cls, types:list[Class], function: Callable) -> MultiMethod:
        """Register a function as mutimethod."""
        name = function.__name__
        registry = cls._registry
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        mm = wraps(function)(mm)
        return mm



def multimethod(*types):
    """Decorator to register a multimethod signature
    
    You can specify function to be mapped to call signature.
    For example:

    We can define one implementation for the scenario when the
    function receives an ``int`` argument.

    We can also define another implementation for the scenario when
    the function receives a ``str`` argument:


    .. testsetup::

        from pygems.core.functools import multimethod

        @multimethod(int)
        def myfunc(a:int):
            print(a)

        @multimethod(str)
        def myfunc(name:str):
            print(f'Hello, {name}')

    .. code-block:: pycon
    
        >>> @multimethod(int)
        ... def myfunc(a:int):
        ...     print(a)
        >>> @multimethod(str)
        ... def myfunc(name: str):
        ...     print(f'Hello, {name}')

    Trying to register duplicate signature results in TypeError error:

    >>> @multimethod(str)
    ... def myfunc(s:str):
    ...     print(s)
    Traceback (most recent call last):
    ...
    TypeError: duplicate registration

    Calling ``myfunc`` with ``int`` argument:

    >>> myfunc(12)
    12

    Calling ``myfunc`` with ``str`` argument:

    >>> myfunc('Ivan')
    Hello, Ivan

    Trying to call with unregistered signature results in error:
    >>> myfunc([])
    Traceback (most recent call last):
    ...
    TypeError: no match
    """
    def register(function):
        return MultiMethodRegistry.register(types, function)
    return register

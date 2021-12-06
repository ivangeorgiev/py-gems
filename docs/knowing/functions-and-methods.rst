Functions and Methods
=====================

Decorators
----------

Basic Decorator
~~~~~~~~~~~~~~~

Let's define a basic decorator.

.. code-block:: python

    import functools

    class AuthorizationError(Exception):
        pass

    def is_authenticated(f):
        """Require that user is authenticated"""
        @functools.wraps(f)
        def _authenticated(request, *args, **kwargs):
            if 'user' in request:
                return f(request, *args, **kwargs)
            else:
                raise AuthorizationError('You need to be logged in')
        return _authenticated

And decorate a function:

.. code-block:: python

    @is_authenticated
    def get_balance(request):
        return 12345

.. testsetup:: wrapper-1

    import functools

    class AuthorizationError(Exception):
        pass

    def is_authenticated(f):
        @functools.wraps(f)
        def _authenticated(request, *args, **kwargs):
            if 'user' in request:
                return f(request, *args, **kwargs)
            else:
                raise AuthorizationError('You need to be logged in')
        return _authenticated

    @is_authenticated
    def get_balance(request):
        return 12345

Calling the function without being authenticated results in error:

.. doctest:: wrapper-1

    >>> request = {'year': 2021}
    >>> get_balance(request)
    Traceback (most recent call last):
    ...
    AuthorizationError: You need to be logged in

If there is a user authenticated, function returns result:

.. doctest:: wrapper-1

    >>> request = { 'user': 'John', 'year': 2021}
    >>> get_balance(request)
    12345

Parameterized Decorator
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import functools
    import inspect

    def not_user(username):
        def not_user_decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                func_args = inspect.getcallargs(f, *args, **kwargs)
                if func_args.get('username') == username:
                    raise AuthorizationError('User is not authorized')
                else:
                    return f(*args, **kwargs)
            return wrapper
        return not_user_decorator

.. code-block:: python

    @not_user("admin")
    def get_food(username, food):
        return food

You can think of this scenario as calling a factory function which creates a decorator which is
than applied to the function.

.. code-block:: python

    def get_food(username, food):
        return food

    get_food = not_user("admin")(get_food)

.. testsetup:: wrapper-2

    import functools
    import inspect

    class AuthorizationError(Exception):
        pass

    def not_user(username):
        def not_user_decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                func_args = inspect.getcallargs(f, *args, **kwargs)
                if func_args.get('username') == username:
                    raise AuthorizationError('User is not authorized')
                else:
                    return f(*args, **kwargs)
            return wrapper
        return not_user_decorator

    @not_user("admin")
    def get_food(username, food):
        return food

Now the ``get_food`` function gives food if the user is not 'admin'.

.. doctest:: wrapper-2

    >>> get_food(username="john", food="apple")
    'apple'

And raises an error in case of user is 'admin'. Thanks to the ``inspect.getcallargs()`` function.

.. doctest:: wrapper-2

    >>> get_food("admin", "orange")
    Traceback (most recent call last):
    ...
    AuthorizationError: User is not authorized

Supports also positional arguments:

.. doctest:: wrapper-2

    >>> get_food(username="admin", food="orange")
    Traceback (most recent call last):
    ...
    AuthorizationError: User is not authorized


Decorator with optional arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def repeat(_func=None, *, num_times=2):
        def decorator_repeat(func):
            @functools.wraps(func)
            def wrapper_repeat(*args, **kwargs):
                for _ in range(num_times):
                    value = func(*args, **kwargs)
                return value
            return wrapper_repeat

        if _func is None:
            return decorator_repeat
        else:
            return decorator_repeat(_func)

This solution uses the keyword-only arguments (:pep:`3102`). If positional argument is 
passed, it should be the decorated function. All decorator arguments are passed as keyword
arguments.

.. code-block:: python

    @repeat()
    def say_whee():
        print("Whee!")

    @repeat(num_times=3)
    def greet(name):
        print(f"Hello {name}")

.. code-block:: python

    >>> say_whee()
    Whee!
    Whee!

    >>> greet('John')
    Hello John
    Hello John
    Hello John


Similar solution using partial function:

.. code-block:: python

    from functools import partial

    def repeat(_func=None, *, num_times=2):
        @functools.wraps(_func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = _func(*args, **kwargs)
            return value

        if _func is None:
            return partial(repeat, num_times=num_times)
        else:
            return wrapper_repeat


Applying Multiple Decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can think of decorators as being applied to what follows:

.. code-block:: python

    @not_user("admin")
    @not_user("abcd")
    @is_authenticated
    def get_food(username, food):
        return food

``@not_user("admin")`` is being applied to the result from the ``@not_user("abcd")`` decorator which 
in turn is applied to the result from the ``@is_authenticated`` decorator which is applied to the 
``get_food()`` function.

Thus you can also remember that decorators are applied from bottom to top. First is applied the 
decorator at the bottom, next the decorator before it etc. until the top decorator.

Further Reading
~~~~~~~~~~~~~~~
- `Python Cookbook <https://github.com/dabeaz/python-cookbook/blob/master/src/9/defining_a_decorator_that_takes_an_optional_argument/example.py>`_
- `Primer on Python Decorators <https://realpython.com/primer-on-python-decorators/>`_ at Real Python
- :pep:`318` -- Decorators for Functions and Methods
- `Decorators <https://book.pythontips.com/en/latest/decorators.html#>`_  at PythonTips


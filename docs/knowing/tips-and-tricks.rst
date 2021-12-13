Tips and Tricks
================

Get nested attribute with dot notation
--------------------------------------

Interesting application for the ``reduce`` function is to access attribute of 
nested objects:

.. literalinclude:: scripts/get_attribute_deep_using_dot_notation_01.py

.. literalinclude:: scripts/get_attribute_deep_using_dot_notation_02.py

Now if we want to access the city of the user, we acually need to access the
``address`` of the user and than the ``city`` of the address. Expressed in dot notation we 
want to access ``address.city`` :

.. code-block:: pycon

    >>> address = Address('Sofia')
    >>> user = User('john', address)
    >>> print(get_attr(user, 'address.city'))
    Sofia

Trying to access missing attribute results in ``AttributeError`` error:

.. code-block:: pycon

    >>> address = Address('Sofia')
    >>> user = User('john', address)
    >>> print(get_attr(user, 'floor'))
    Traceback (most recent call last):
    ...
    AttributeError: 'Address' object has no attribute 'floor'

This function has been included in ``pygems.core.shortcuts`` module.


Capture function execution time
-------------------------------

The :class:`pygems.core.timer.Timer` class implements the decorator protocol.
You can capture the execution time of a function using the :class:`pygems.core.timer.Timer` class as decorator.

.. code-block:: python

    from pygems.core.timer import Timer

    @Timer(stop_func=lambda t: print(f'{t.elapsed}s'))
    def slow_function():
        # do your work here
        pass

Each time the ``slow_functoin()`` is called, the elapsed time for
the function execution is printed to the console.

.. code-block:: pycon

    >> slow_function()
    3.1e-06s

The :class:`pygems.core.timer.Timer` calls the passed ``stop_func`` function
when the function has finished its execution. 

In the above example we pass a lambda function which simply prints the elapsed seconds.

You could make the timer to log a message:

.. code-block:: pycon

    import logging
    from pygems.core.timer import Timer

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def stop_func(t:Timer, *args):
        logger.info(f'{t.name}: elapsed {t.elapsed}s')


    @Timer(name='slow_function', stop_func=stop_func)
    def slow_function():
        # do your work here
        pass

Now when the ``slow_function`` is called a message is added to the log which includes
the name of the timer and the elapsed time.

.. code-block:: pycon

    >> slow_function()
    INFO:__main__:slow_function: elapsed 6.499999983589078e-06s


Capture the execution time of Python block
------------------------------------------

:class:`pygems.core.timer.Timer` implements the context manager protocol.
This can be used to capture the time required to execute a block of code in Python.

You can pass any function as ``stop_func`` argument to the Timer class.
The function will be called at the end of the block with the timer instance as
first argument.

.. code-block:: pycon

    >>> from pygems.core.timer import Timer
    >>> with Timer(name='slow-block', stop_func=lambda t: print(f'{t.name}: {t.elapsed}s')):
    >>>     # run your code here
    >>>     pass
    slow-block: 3.999999989900971e-06s

Similarly the execution time of the block could be logged using Python's logging module:

.. code-block:: pycon

    >>> import logging
    >>> from pygems.core.timer import Timer
    >>> logging.basicConfig(level=logging.INFO)
    >>> with Timer(name='slow-block', stop_func=lambda t: logging.info(f'{t.name}: {t.elapsed}s')):
    >>>     # run your code here
    >>>     pass
    INFO:root:slow-block: 1.5699999948992627e-05s


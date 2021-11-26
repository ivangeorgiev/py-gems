import timeit
from typing import Callable

class StringMessageCallback:
    """Simple string message callback for timer stop()

    Example 1:

    >>> timer = Timer(name='MyTimer', stop_func=StringMessageCallback())
    >>> timer.stop('loaded')          # doctest: +SKIP
    MyTimer: 2.7700000000019376e-05s loaded
    >>> timer.stop('transferred')     # doctest: +SKIP
    MyTimer: 5.060000000001175e-05s transferred

    Example 2: Custom template could be used:

    >>> timer = Timer(name='MyTimer', stop_func=StringMessageCallback(message_template='{args[0]} at {timer.elapsed}s'))
    >>> timer.stop('Loaded')          # doctest: +SKIP
    Loaded at 2.7700000000019376e-05s
    >>> timer.stop('Transfered')      # doctest: +SKIP
    Transfered at 5.060000000001175e-05s
    """
    message_template: str
    message_func: Callable

    def __init__(self, message_template=None, message_func=None):
        self.message_template = message_template or '{timer.name}: {timer.elapsed}s {args_str}'
        self.message_func = message_func or print

    def __call__(self, timer, *args):
        message = self.message_template.format(timer=timer, args=args, 
                args_str=" ".join(args))
        self.message_func(message)

class Timer:
    """Generic Timer class.

    Useful for profiling.

    Example:
    --------

    In this example we will create a timer which each time the stop() method is called will
    print the elapsed time since the timer was created:

    We will use partial function to simulate current time callback:
    >>> from functools import partial

    Our function returns the elements of a pre-defined list in sequence:
    >>> time_func = partial([1, 9.1234, 30.789].pop, 0)

    Also we want to pass a stop callback which prints some pretty message:
    >>> stop_func = lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s')

    Let's create our timer:
    >>> timer = Timer(name='MyTimer', time_func=time_func, stop_func=stop_func)

    Call the stop() method passing a message which will be used by the stop_func:
    >>> timer.stop('load finished at')
    MyTimer: load finished at 8.1234s

    >>> timer.stop('parse finished at')
    MyTimer: parse finished at 29.789s
    """
    name: str
    started_at: float
    stopped_at: float
    _time_func: Callable
    stop_func: Callable

    def __init__(self, name=None, time_func=None, stop_func=None):
        """Creates, initializes and starts Timer instance.

        name argument is set to name attribute:
        >>> timer = Timer(name='My Timer')
        >>> timer.name
        'My Timer'

        When time_func argument is specified it is set to _time_func attribute:
        >>> time_func = lambda : 20
        >>> timer = Timer(time_func=time_func)
        >>> time_func == timer._time_func
        True

        When time_func argument is not specified, timeit.default_timer is used
        >>> timer = Timer()
        >>> timer._time_func == timeit.default_timer
        True

        Attempt to use time_func which is not callable raises AssertionError:
        >>> timer = Timer(time_func=5)
        Traceback (most recent call last):
           ...
        AssertionError: Expecting time_func argument to be callable

        Newly created object is started
        >>> timer = Timer(time_func=[1].pop)
        >>> timer.started_at
        1

        stop_func is set to passed argument
        >>> timer = Timer(stop_func=print)
        >>> timer.stop_func is print
        True

        Attempt to use stop_func which is not callable raises AssertionError:
        >>> timer = Timer(stop_func=5)
        Traceback (most recent call last):
           ...
        AssertionError: Expecting stop_func argument to be callable

        """
        self.name = name
        if time_func:
            assert callable(time_func), 'Expecting time_func argument to be callable'
        self._time_func = time_func or timeit.default_timer
        if stop_func:
            assert callable(stop_func), 'Expecting stop_func argument to be callable'
        self.stop_func = stop_func
        self.start()

    @property
    def time(self):
        """Returns the current time as presented by the _time_func callback
        
        >>> timer = Timer(time_func=lambda : 5)
        >>> timer.time
        5
        """
        return self._time_func()

    @property
    def elapsed(self) -> float:
        """Returns elapsed time between sarted and stopped or started and current time.

        If timer is not stopped, elapsed returns current - started time:
        >>> from functools import partial
        >>> timer = Timer(time_func=partial([1,5].pop, 0))
        >>> timer.elapsed
        4

        If timer is stopped, elapsed returns stopped time - started time:
        >>> timer = Timer(time_func=partial([1,3,5].pop, 0))
        >>> timer.stop()
        >>> timer.stopped_at
        3
        >>> timer.elapsed
        2

        """
        if self.stopped_at:
            return self.stopped_at - self.started_at
        return self.time - self.started_at

    def start(self):
        """Starts the timer by setting the started_at to current time and stopped_at to None.
        
        >>> from functools import partial
        >>> timer = Timer(time_func=partial([10,20,30].pop, 0))
        
        started_at is set during intialization

        >>> timer.started_at
        10

        When we stop the timer, stopped_at is set:

        >>> timer.stop()
        >>> timer.stopped_at
        20

        Starting a stopped timer sets started_at to current time and stopped_at to None:

        >>> timer.start()
        >>> timer.started_at
        30
        >>> timer.stopped_at is None
        True

        """
        self.started_at = self.time
        self.stopped_at = None

    def stop(self, *args):
        """Stop the timer by setting the stopped_at attribute to current time
        
        >>> from functools import partial
        >>> timer = Timer(time_func=partial([1,9, 50].pop, 0))

        When timer is not stopped, stopped time stopped_at is None

        >>> timer.stopped_at is None
        True

        After we call the stop() method, the stopped_at time is set to current time
        
        >>> timer.stop()
        >>> timer.stopped_at
        9

        Calling stop() method multipe times is safe. Each call remembers current time when
        stop() was called.

        >>> timer.stop()
        >>> timer.stopped_at
        50

        When stop_func attribute is set, it is called when timer stop() metod is called with timer
        passed as first artument:
        >>> timer = Timer(name='MyTimer', time_func=partial([1,9.1234,30.789].pop, 0), 
        ...               stop_func=lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s'))
        >>> timer.stop('load finished at')
        MyTimer: load finished at 8.1234s
        >>> timer.stop('parse finished at')
        MyTimer: parse finished at 29.789s
        """
        self.stopped_at = self.time
        if hasattr(self, 'stop_func') and self.stop_func:
            self.stop_func(self, *args)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

import timeit
from typing import Callable

class Timer:
    name: str
    started_at: float
    stopped_at: float
    _time_func: Callable
    _stop_callback: Callable

    def __init__(self, name=None, time_func=None, stop_callback=None):
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

        _stop_callback is set to passed argument
        >>> timer = Timer(stop_callback=print)
        >>> timer._stop_callback is print
        True

        Attempt to use stop_callback which is not callable raises AssertionError:
        >>> timer = Timer(stop_callback=5)
        Traceback (most recent call last):
           ...
        AssertionError: Expecting stop_callback argument to be callable

        """
        self.name = name
        if time_func:
            assert callable(time_func), 'Expecting time_func argument to be callable'
        self._time_func = time_func or timeit.default_timer
        if stop_callback:
            assert callable(stop_callback), 'Expecting stop_callback argument to be callable'
        self._stop_callback = stop_callback
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

        When stop_callback attribute is set, it is called when timer stop() metod is called with timer
        passed as first artument:
        >>> timer = Timer(name='MyTimer', time_func=partial([1,9.1234,30.789].pop, 0), 
        ...               stop_callback=lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s'))
        >>> timer.stop('load finished at')
        MyTimer: load finished at 8.1234s
        >>> timer.stop('parse finished at')
        MyTimer: parse finished at 29.789s
        """
        self.stopped_at = self.time
        if hasattr(self, '_stop_callback') and self._stop_callback:
            self._stop_callback(self, *args)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

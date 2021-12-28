"""A library of context-related tools."""
import contextlib
from typing import Any

class on_exit(contextlib.AbstractContextManager):
    """Context to automatically call closing method at the end of a block.

    Arguments:
        obj (Any): Name of the driver to use.
        on_exit (str): Method name to call at the end of the block. Default: 'close'

    Example::

        with closing(webdriver.Chrome(), "quit") as driver:
            driver.get("http://igeorgiev.eu")
    """

    def __init__(self, thing: Any, on_exit: str = "close"):
        self.thing = thing
        self.on_exit = getattr(thing, on_exit, None)
        if self.on_exit is None or not callable(self.on_exit):
            raise AttributeError(f"Object has no '{on_exit} method.")

    def __enter__(self):
        return self.thing

    def __exit__(self, *exc_info):
        self.on_exit()

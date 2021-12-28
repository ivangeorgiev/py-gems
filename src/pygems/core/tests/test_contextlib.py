import pytest
from pygems.core.contextlib import on_exit

class Exitable:
    exited: False

    def exit(self):
        self.exited = True

class TestOnExit:
    def test_returns_given_object(self):
        obj = Exitable()
        with on_exit(obj, "exit") as actual:
            assert obj is actual

    def test_calls_the_method(self):
        obj = Exitable()
        with on_exit(obj, "exit"):
            pass
        assert obj.exited

    def test_raises_attributeerror_if_method_not_found(self):
        with pytest.raises(AttributeError):
            with on_exit(object(), "some_exit_work"):
                pass

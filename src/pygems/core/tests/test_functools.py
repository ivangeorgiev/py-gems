import pytest
from unittest import mock
from pygems.core.functools import multimethod

@pytest.fixture(scope="session")   # We cannot use the same function signature multiple times in the same session
def given_int_version():
    @multimethod(int)
    def myfunc(a:int):
        return int
    return myfunc

@pytest.fixture(scope="session")
def given_str_version():
    @multimethod(str)
    def myfunc(a:str):
        return str
    return myfunc

def test_calling_same_function_with_different_signatures_calls_correct_version(
    given_int_version,
    given_str_version
):
    assert given_int_version(1) is int
    assert given_str_version('test') is str

def test_trying_to_register_same_function_with_same_signature_twice_results_in_type_error():
    @multimethod()
    def repeated_function():
        pass

    with pytest.raises(TypeError):
        @multimethod()
        def repeated_function():
            pass


def test_calling_multimethod_with_unregistered_signature_results_in_type_error():
    @multimethod()
    def empty_signature_only():
        pass

    with pytest.raises(TypeError):
        empty_signature_only(22)

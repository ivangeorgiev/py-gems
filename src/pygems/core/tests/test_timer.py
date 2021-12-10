from unittest import mock
from functools import partial
import pytest
import timeit
from pygems.core import timer

@pytest.fixture(scope='function')
def time_func():
    time_func = mock.Mock()
    time_func.side_effect = [1, 5, 9.5, 20.5]
    return time_func

@pytest.fixture(scope='function')
def stop_func():
    return mock.Mock()

@pytest.fixture(scope='function')
def timer_with_func(time_func, stop_func):
    t = timer.Timer('TheTimer', time_func=time_func, stop_func=stop_func)
    return t

class TestTimer:
    def test_time_attribute_returns_timer_func(self):
        time_func = mock.Mock
        t = timer.Timer(time_func=time_func)
        assert time_func is t.time_func

    def test_timer_sets_attribute(self):
        time_func = mock.Mock()
        stop_func = mock.Mock()
        t = timer.Timer('mytimer', time_func, stop_func)
        assert t.name == 'mytimer'
        assert t.time_func is time_func
        assert t.stop_func is stop_func

    def test_create_timer_default_arguments(self):
        t = timer.Timer('thetimer')
        assert t.time_func is timeit.default_timer
        assert t.stop_func is None

    def test_stopped_at_not_set_when_not_stopped(self):
        t = timer.Timer()
        assert t.stopped_at is None
    
    def test_after_call_to_stop_stopped_at_is_set(self, timer_with_func):
        timer_with_func.stop()
        assert timer_with_func.stopped_at == 5

    def test_create_timer_sets_started_at(self, timer_with_func):
        assert timer_with_func.started_at == 1

    def test_elapsed_returns_until_now_when_not_stopped(self, timer_with_func: timer.Timer):
        assert timer_with_func.elapsed == 4
        assert timer_with_func.elapsed == 8.5, 'second call reads current time'

    def test_elapsed_returns_until_stopped_at_when_stopped(self, timer_with_func: timer.Timer):
        timer_with_func.stop()
        assert timer_with_func.elapsed == 4
        assert timer_with_func.elapsed == 4, 'second call returns same time'

    def test_stop_calls_stop_func_passing_args(self, timer_with_func: timer.Timer, stop_func: mock.Mock):
        timer_with_func.stop('arg1', 'arg2')
        stop_func.assert_called_once_with(timer_with_func, 'arg1', 'arg2')

    def test_stop_sets_stopped_at_each_time_called(self, timer_with_func: timer.Timer):
        timer_with_func.stop()
        stopped_at = [timer_with_func.stopped_at]
        timer_with_func.stop()
        stopped_at.append(timer_with_func.stopped_at)
        assert stopped_at == [5, 9.5]

class TestStringMessageCallback:

    def test_create_sets_attributes(self):
        cb = timer.StringMessageCallback('template', 'func', 'separator')
        result = {'tpl': cb.message_template, 'f': cb.message_func, 'sep': cb.arg_separator}
        assert result == {'tpl': 'template', 'f': 'func', 'sep': 'separator'}

    def test_call_calls_message_func_with_formatted_message(self):
        f = mock.Mock()
        cb = timer.StringMessageCallback('{timer}: {args_str} or {args[0]}, {args[1]}',
                message_func=f,
                arg_separator='+')
        expected = 'MyTimer: arg1+arg2 or arg1, arg2'
        cb('MyTimer', 'arg1', 'arg2')
        f.assert_called_with(expected)
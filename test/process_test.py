#!/usr/bin/python

from process_timeout import *
import time
from nose import run

def test1():
    ''' timeout is not stopping quick function
    '''
    @process_timeout(2)
    def func(delay):
        time.sleep(delay)

    func(1)


def test1_call():
    ''' call: timeout is not stopping quick function
    '''
    def func(delay):
        time.sleep(delay)

    process_timeout_call(func, 2, args=(1,))


def test2():
    ''' ExecTimeout
    '''
    @process_timeout(1)
    def func(delay):
        time.sleep(delay)

    try:
        func(3)
        raise Exception("Test2 failed: timeout does not work")
    except ExecTimeout as e:
        pass


def test2_call():
    ''' call: ExecTimeout
    '''
    def func(delay):
        time.sleep(delay)

    try:
        process_timeout_call(func, 1, args=(3,))
        raise Exception("call: Test2 failed: timeout does not work")
    except ExecTimeout as e:
        pass


def test3():
    ''' function returns result
    '''
    @process_timeout(1)
    def func(x):
        return x

    assert func('OK') == 'OK'


def test3_call():
    ''' call: function returns result
    '''
    def func(x):
        return x

    assert process_timeout_call(func, 1, args=('OK',)) == 'OK'


def test5():
    ''' NotKillExecTimeout
    '''
    @process_timeout(1, kill=False)
    def looong_and_unkillable():
            time.sleep(2)
    try:
        looong_and_unkillable()
        raise Exception('NotKillExecTimeout was expected')
    except NotKillExecTimeout as e:
        print("Test5 OK, got expected exception %s" % repr(e))


def test5_call():
    ''' call: NotKillExecTimeout
    '''
    def looong_and_unkillable():
            time.sleep(2)
    try:
        process_timeout_call(looong_and_unkillable, 1, kill=False)
        raise Exception('call: NotKillExecTimeout was expected')
    except NotKillExecTimeout as e:
        print("call: Test5 OK, got expected exception %s" % repr(e))


def test6():
    '''KilledExecTimeout
    '''
    @process_timeout(1)
    def killme():
        for a in range(0, 200):
            time.sleep(0.01)
        raise Exception("Not killed!")

    try:
        killme()
    except KilledExecTimeout:
        pass


def test6_call():
    '''call: KilledExecTimeout
    '''
    def killme():
        for a in range(0, 200):
            time.sleep(0.01)
        raise Exception("call: Not killed!")

    try:
        process_timeout_call(killme, 1)
    except KilledExecTimeout:
        pass


def test7():
    ''' decorator is not changing python's into inspection
    '''
    from inspect import getargspec

    def func(x, y=1, *args, **kwargs):
        return vars()

    func_with_timeout = process_timeout(1)(func)
    assert getargspec(func) == getargspec(func_with_timeout)


def test8():
    ''' Class methods
    '''
    class Class(object):

        @process_timeout(1)
        def short(self, x):
            return x

        @process_timeout(1)
        def looong(self, x):
            for x in range(0, 300):
                time.sleep(0.01)
            return x

    obj = Class()
    res = obj.short("OK")
    assert res == 'OK'
    try:
        res = obj.looong('KO')
    except KilledExecTimeout:
        pass


def test8_call():
    ''' call: Class methods
    '''
    class Class(object):

        def short(self, x):
            return x

        def looong(self, x):
            for x in range(0, 300):
                time.sleep(0.01)
            return x

    obj = Class()
    res = process_timeout_call(obj.short, 1, args=('OK',))
    assert res == 'OK'
    try:
        res = process_timeout_call(obj.looong, 1, args=('OK',))
    except KilledExecTimeout:
        pass


def test10():
    '''Check if decorator stacking works (inner first)
    '''
    @process_timeout(2)
    def outer():
        @process_timeout(1)
        def inner():
            for x in range(0, 500):
                time.sleep(0.01)
        inner()

    begin = time.time()
    try:
        outer()
    except ExecTimeout as e:
        pass
    assert 1 < time.time() - begin < 2


def test10_call():
    '''call: Check if decorator stacking works (inner first)
    '''
    def outer():
        def inner():
            for x in range(0, 500):
                time.sleep(0.01)
        process_timeout_call(inner, 1)

    begin = time.time()
    try:
        process_timeout_call(outer, 2)
    except ExecTimeout as e:
        pass
    assert 1 < time.time() - begin < 2


def test11():
    '''Check if decorator stacking works (outer first)
    '''
    @process_timeout(1)
    def outer():
        @process_timeout(2)
        def inner():
            for x in range(0, 500):
                time.sleep(0.01)
        inner()

    begin = time.time()
    try:
        outer()
    except ExecTimeout:
        pass
    assert 1 < time.time() - begin < 2


def test11_call():
    '''call: Check if decorator stacking works (outer first)
    '''
    def outer():
        def inner():
            for x in range(0, 500):
                time.sleep(0.01)
        process_timeout_call(inner, 2)

    begin = time.time()
    try:
        process_timeout_call(outer, 1)
    except ExecTimeout:
        pass
    assert 1 < time.time() - begin < 2


def test12():
    '''Check if decorator waits before kill'''
    @process_timeout(3)
    def outer():
        @process_timeout(3)
        def inner():
            for x in range(0, 100):
                time.sleep(0.01)
        inner()

    begin = time.time()
    outer()
    assert 1 < time.time() - begin < 3


def test12_call():
    '''call: Check if decorator waits before kill'''
    def outer():
        def inner():
            for x in range(0, 100):
                time.sleep(0.01)
        process_timeout_call(inner, 3)

    begin = time.time()
    process_timeout_call(outer, 3)
    assert 1 < time.time() - begin < 3


def test13():
    '''check if we can instance methods with one kwarg (real bug case)'''
    class Foo:
        @process_timeout(1)
        def bar(self, arg=1):
            pass

    foo = Foo()
    foo.bar(arg=0)


def test13_call():
    '''call: check if we can instance methods with one kwarg (real bug case)'''
    class Foo:
        def bar(self, arg=1):
            pass

    foo = Foo()
    process_timeout_call(foo.bar, 1, kwargs=dict(arg=0))


if __name__ == "__main__":
    print("Running tests")

    run(argv=[
        '', __file__,
        '-v'
    ])

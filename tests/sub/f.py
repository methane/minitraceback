import sys


def f1():
    return f2()


def f2():
    return f3()


def f3():
    return sys._getframe(0)

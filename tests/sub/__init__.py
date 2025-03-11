import sys


class HogeError(Exception):
    pass


def f1() -> BaseException:
    try:
        f2()
    except BaseException as e:
        if sys.version_info[:2] >= (3, 11):
            e.add_note("this is note")
        return e
    raise RuntimeError("unreachable")


def f2():
    f3()


def f3():
    raise HogeError("foobar")

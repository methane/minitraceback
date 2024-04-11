class HogeError(Exception):
    pass


def f1() -> BaseException:
    try:
        f2()
    except BaseException as e:
        e.add_note("this is note")
        return e
    raise RuntimeError("unreachable")


def f2():
    f3()


def f3():
    raise HogeError("foobar")

import minitraceback
import sub


def test_extract_tb():
    e = sub.f1()
    tbs = minitraceback.extract_tb(e.__traceback__)

    assert tbs[0] == ("sub/__init__.py", 19, "f3")
    assert tbs[1] == ("sub/__init__.py", 15, "f2")
    assert tbs[2] == ("sub/__init__.py", 7, "f1")
    assert len(tbs) == 3


def test_format_miti_tb():
    e = sub.f1()
    tbs = minitraceback.extract_tb(e.__traceback__)
    lines = minitraceback.format_miti_tb(tbs)

    assert lines[0] == "Traceback (most recent call first):"
    assert lines[1] == "  sub/__init__.py:19 f3"
    assert lines[2] == "  sub/__init__.py:15 f2"
    assert lines[3] == "  sub/__init__.py:7 f1"
    assert len(lines) == 4


def test_format_exception():
    e = sub.f1()
    s = minitraceback.format_exception(e)
    assert s[0] == "sub.HogeError: foobar"
    assert s[1] == "  this is note"
    assert len(s) == 2

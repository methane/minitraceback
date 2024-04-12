import minitraceback
import sub.f


def test_extract_tb():
    e = sub.f1()
    tbs = minitraceback.extract_tb(e.__traceback__)
    assert tbs[0] == ("sub/__init__.py", 19, "f3")
    assert tbs[1] == ("sub/__init__.py", 15, "f2")
    assert tbs[2] == ("sub/__init__.py", 7, "f1")
    assert len(tbs) == 3

    tbs = minitraceback.extract_tb(e.__traceback__, limit=2)
    assert tbs[0] == ("sub/__init__.py", 19, "f3")
    assert tbs[1] == ("sub/__init__.py", 15, "f2")
    assert len(tbs) == 2


def test_format_frames():
    e = sub.f1()
    fs = minitraceback.extract_tb(e.__traceback__)
    lines = minitraceback.format_frames(fs)

    assert lines[0] == "sub/__init__.py:19 f3"
    assert lines[1] == "sub/__init__.py:15 f2"
    assert lines[2] == "sub/__init__.py:7 f1"
    assert len(lines) == 3


def test_extract_stack():
    f = sub.f.f1()
    fs = minitraceback.extract_stack(f)
    assert fs[0] == ("sub/f.py", 12, "f3")
    assert fs[1] == ("sub/f.py", 8, "f2")
    assert fs[2] == ("sub/f.py", 4, "f1")
    assert fs[3].filename == "test_minitraceback.py"
    assert fs[3].funcname == "test_extract_stack"

    fs = minitraceback.extract_stack(f, limit=2)
    assert fs[0] == ("sub/f.py", 12, "f3")
    assert fs[1] == ("sub/f.py", 8, "f2")
    assert len(fs) == 2


def test_format_exception_only():
    e = sub.f1()
    s = minitraceback.format_exception_only(e)
    assert s[0] == "sub.HogeError: foobar"
    assert s[1] == "  this is note"
    assert len(s) == 2

import io
from io import StringIO

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
    lines = minitraceback.format_list(fs)

    assert lines[0] == "sub/__init__.py:19 f3"
    assert lines[1] == "sub/__init__.py:15 f2"
    assert lines[2] == "sub/__init__.py:7 f1"
    assert len(lines) == 3


def test_extract_stack():
    f = sub.f.f1()
    fs = minitraceback.extract_stack(f)
    assert fs[0] == ("sub/f.py", 13, "f3")
    assert fs[1] == ("sub/f.py", 9, "f2")
    assert fs[2] == ("sub/f.py", 5, "f1")
    assert fs[3].filename == "test_minitraceback.py"
    assert fs[3].funcname == "test_extract_stack"

    fs = minitraceback.extract_stack(f, limit=2)
    assert fs[0] == ("sub/f.py", 13, "f3")
    assert fs[1] == ("sub/f.py", 9, "f2")
    assert len(fs) == 2


def test_format_exception_only():
    e = sub.f1()
    s = minitraceback.format_exception_only(e)
    assert s[0] == "sub.HogeError: foobar"
    assert s[1] == "  this is note"
    assert len(s) == 2


def test_format_tb():
    tb = sub.f1().__traceback__
    formatted_tb = minitraceback.format_tb(tb)
    assert formatted_tb[0] == "  sub/__init__.py:19 f3"
    assert formatted_tb[1] == "  sub/__init__.py:15 f2"
    assert formatted_tb[2] == "  sub/__init__.py:7 f1"

    formatted_tb = minitraceback.format_tb(tb, limit=2)
    assert formatted_tb[0] == "  sub/__init__.py:19 f3"
    assert formatted_tb[1] == "  sub/__init__.py:15 f2"
    assert len(formatted_tb) == 2


def test_print_tb():
    tb = sub.f1().__traceback__

    # Test with default arguments
    expected_output = f"{minitraceback.TRACEBACK_HEADER}\n"
    expected_output += "  sub/__init__.py:19 f3\n"
    expected_output += "  sub/__init__.py:15 f2\n"
    expected_output += "  sub/__init__.py:7 f1\n"

    output = io.StringIO()
    minitraceback.print_tb(tb, file=output)
    assert output.getvalue() == expected_output


def test_format_stack():
    stack = minitraceback.format_stack()
    assert stack[0] == minitraceback.TRACEBACK_HEADER
    assert stack[1].startswith("  test_minitraceback.py:")
    assert stack[1].endswith(" test_format_stack")

    f = sub.f.f1()
    stack = minitraceback.format_stack(f, limit=2)
    assert stack[0] == minitraceback.TRACEBACK_HEADER
    assert stack[1] == "  sub/f.py:13 f3"
    assert stack[2] == "  sub/f.py:9 f2"
    assert len(stack) == 3


def test_print_stack():
    output = StringIO()

    f = sub.f.f1()
    minitraceback.print_stack(f, limit=2, file=output)
    printed_output = output.getvalue()
    expected_output = """\
Traceback (most recent call first):
  sub/f.py:13 f3
  sub/f.py:9 f2
"""
    assert printed_output == expected_output


def test_print_exception():
    e = sub.f1()

    output = io.StringIO()
    minitraceback.print_exception(e, file=output)
    output_value = output.getvalue()
    expected_value = """\
sub.HogeError: foobar
  this is note
Traceback (most recent call first):
  sub/__init__.py:19 f3
  sub/__init__.py:15 f2
  sub/__init__.py:7 f1
"""
    assert output_value == expected_value

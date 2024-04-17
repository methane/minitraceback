from __future__ import annotations

import itertools
import os
import sys
import traceback
from typing import NamedTuple

TRACEBACK_HEADER = "Traceback (most recent call first):"


class FrameInfo(NamedTuple):
    filename: str
    lineno: int
    funcname: str


def _extract_from(gen) -> list[FrameInfo]:
    paths = [os.path.abspath(p) + "/" for p in sys.path]
    paths.sort(key=len, reverse=True)

    result: list[FrameInfo] = []
    for f, lineno in gen:
        c = f.f_code
        filename: str = c.co_filename
        if not filename:
            filename = "?"
        elif not filename.startswith("<"):
            for p in paths:
                if filename.startswith(p):
                    filename = filename.removeprefix(p)
                    break
        result.append(FrameInfo(filename, lineno, c.co_name))

    return result


def extract_tb(tb, /, *, limit: int | None = None) -> list[FrameInfo]:
    """Extract a traceback from a traceback object."""
    tbs = list(traceback.walk_tb(tb))
    if limit is not None:
        tbs = tbs[: -limit - 1 : -1]
    else:
        tbs.reverse()
    return _extract_from(tbs)


def extract_stack(f, /, *, limit: int | None = None) -> list[FrameInfo]:
    """Extract a traceback from a frame object."""
    frames = itertools.islice(traceback.walk_stack(f), limit)
    return _extract_from(frames)


def format_list(frames: list[FrameInfo], *, indent=0) -> list[str]:
    """Format a list of FrameInfo into a list of strings.

    Format is 'filename:lineno funcname'.
    """
    sindent = " " * indent
    return [f"{sindent}{f}:{lineno} {name}" for f, lineno, name in frames]


def format_tb(tb, /, *, limit=None) -> list[str]:
    """Format a traceback from a traceback object."""
    return format_list(extract_tb(tb, limit=limit), indent=2)


def print_tb(tb, /, *, limit=None, file=None):
    """Print a traceback from a traceback object."""
    if file is None:
        file = sys.stderr
    print(TRACEBACK_HEADER, file=file)
    for line in format_tb(tb, limit=limit):
        print(line, file=file)


def format_stack(f=None, /, *, limit=None) -> list[str]:
    """Format a stack trace from a frame object."""
    if f is None:
        f = sys._getframe().f_back
    lines = [TRACEBACK_HEADER] + format_list(extract_stack(f, limit=limit), indent=2)
    return lines


def print_stack(f=None, /, *, limit=None, file=None):
    """Print a stack trace from a frame object."""
    if f is None:
        f = sys._getframe().f_back
    if file is None:
        file = sys.stderr
    print(TRACEBACK_HEADER, file=file)
    for line in format_list(extract_stack(f, limit=limit), indent=2):
        print(line, file=file)


def format_exception_only(exc: BaseException) -> list[str]:
    """Format an exception without a traceback."""
    exc_type = type(exc)
    exc_type_qualname = exc_type.__qualname__
    exc_type_module = exc_type.__module__
    if exc_type_module == "builtins":
        stype = exc_type_qualname
    else:
        stype = f"{exc_type_module}.{exc_type_qualname}"
    res = [f"{stype}: {exc}"]

    for n in getattr(exc, "__notes__", ()):
        res.append(f"  {n}")

    return res


def format_exception(exc, /, *, limit=None) -> list[str]:
    """Format an exception and its traceback."""
    tb = exc.__traceback__
    tbs = extract_tb(tb, limit=limit)
    return [
        *format_exception_only(exc),
        TRACEBACK_HEADER,
        *format_list(tbs, indent=2),
    ]


def print_exception(exc, /, *, limit=None, file=None):
    """Print an exception and its traceback."""
    if file is None:
        file = sys.stderr
    print("\n".join(format_exception(exc, limit=limit)), file=file)

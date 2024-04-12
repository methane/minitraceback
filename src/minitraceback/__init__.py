from __future__ import annotations

import itertools
import os
import pathlib
import sys
import traceback
from typing import NamedTuple

TRACEBACK_HEADER = "Traceback (most recent call first):"


class FrameInfo(NamedTuple):
    filename: str
    lineno: int
    funcname: str


def _extract_from(gen) -> list[FrameInfo]:
    paths = [os.path.abspath(p) for p in sys.path]
    paths.sort(key=len, reverse=True)

    result: list[FrameInfo] = []
    for f, lineno in gen:
        c = f.f_code
        filename: str = c.co_filename
        if not filename:
            filename = "?"
        elif not filename.startswith("<"):
            fp = pathlib.Path(filename)
            for p in paths:
                try:
                    filename = str(fp.relative_to(p, walk_up=False))
                    break
                except ValueError:
                    continue
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


def format_frames(frames: list[FrameInfo], *, indent=0) -> list[str]:
    """Format a list of FrameInfo into a list of strings.

    Format is 'filename:lineno funcname'.
    """
    sindent = " " * indent
    return [f"{sindent}{f}:{lineno} {name}" for f, lineno, name in frames]


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
        *format_frames(tbs, indent=2),
    ]

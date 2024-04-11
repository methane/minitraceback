from __future__ import annotations

import os
import pathlib
import sys
import traceback


def extract_tb(tb, *, limit=None) -> list[tuple[str, int, str]]:
    paths = [(p or os.getcwd()) for p in sys.path]

    tbs = [*traceback.walk_tb(tb)]
    tbs.reverse()
    if limit is not None:
        del tbs[limit:]

    result = []
    for f, lineno in tbs:
        c = f.f_code
        filename = pathlib.Path(c.co_filename)
        for p in paths:
            try:
                filename = filename.relative_to(p, walk_up=False)
                break
            except ValueError:
                continue
        result.append((str(filename), lineno, c.co_name))

    return result


def format_miti_tb(tbs: list[tuple[str, int, str]], *, header=True, indent=2) -> list[str]:
    sindent = " " * indent
    if header:
        res = ["Traceback (most recent call first):"]
    else:
        res = []
    for f, lineno, name in tbs:
        res.append(f"{sindent}{f}:{lineno} {name}")
    return res


def format_exception(exc: BaseException, *, indent=2) -> list[str]:
    exc_type = type(exc)
    exc_type_qualname = exc_type.__qualname__
    exc_type_module = exc_type.__module__
    if exc_type_module == "builtins":
        stype = exc_type_qualname
    else:
        stype = f"{exc_type_module}.{exc_type_qualname}"
    res = [f"{stype}: {exc}"]

    sindent = " " * indent
    for n in getattr(exc, "__notes__", ()):
        res.append(f"{sindent}{n}")

    return res

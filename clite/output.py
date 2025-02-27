import sys
from typing import TextIO


def _make_file_stdout() -> TextIO:
    return sys.stdout


def _make_file_stderr() -> TextIO:
    return sys.stderr


def echo(message: str, is_err: bool = False, is_new_line: bool = True) -> None:
    file = None
    if is_err:
        file = _make_file_stderr()
    else:
        file = _make_file_stdout()
    if is_new_line:
        message += "\n"
    message = message.strip()
    file.write(message)
    file.flush()

import sys

from typing import IO, Any


def echo(
    message: str,
    file: IO[Any] | None = None,
    is_err: bool = False,
    is_new_line: bool = True,
) -> None:
    if file is None:
        if is_err:
            file = sys.stderr
        else:
            file = sys.stdout
    if is_new_line:
        message += "\n"
    print("test echo")
    file.write(message)
    file.flush()

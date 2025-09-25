import sys
from typing import TextIO


def echo(message: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    :param message: message to print
    :param file: file to print(default: stdout)
    :return: None
    """
    file.write(f"{message}\n")
    file.flush()

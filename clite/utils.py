import sys
from typing import TextIO

from clite._types import Any, Mapping
from clite.parser.function import ParameterInfo


def echo(message: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    :param message: message to print
    :param file: file to print(default: stdout)
    :return: None
    """
    file.write(f"{message}\n")
    file.flush()


def split_args_kwargs(
    params: Mapping[str, ParameterInfo],
) -> tuple[tuple[Any], Mapping[str, Any]]:
    """Split parameter arguments into args and kwargs.

    Separates required positional arguments from optional keyword arguments
    based on parameter definitions.

    :param params: mapping of parameter info
    :returns: (args, kwargs) tuple where args is a tuple of required values,
               kwargs is a dict of optional values
    """
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    for _, p in params.items():
        if p.is_optional:
            kwargs[p.name] = p.value
        else:
            args.append(p.value)
    return tuple(args), kwargs

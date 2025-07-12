import inspect
import sys
from collections import deque
from functools import partial
from typing import Callable, get_args, get_origin, get_type_hints

from clite import echo
from clite.parser import parse_command_line


class MissingArgumentError(Exception):
    pass


def hello(name: str, age: int, is_show: bool = False) -> None:
    """Print Hello from playground."""
    if is_show:
        echo(f"Hello from playground, {name} {age}!")
    else:
        echo(f"Hello {name} {age}")


def process_signature(func: Callable) -> inspect.Signature:
    params = []
    signature = inspect.signature(func)

    for param in signature.parameters.values():
        if param.default is inspect.Parameter.empty:
            params.append(
                param.replace(
                    name=param.name,
                    kind=inspect.Parameter.POSITIONAL_ONLY,
                    default=inspect.Parameter.empty,
                )
            )
        else:
            params.append(
                param.replace(
                    name=param.name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    default=param.default,
                )
            )

    signature = signature.replace(parameters=params, return_annotation=signature.return_annotation)

    return signature


def main(argv: list[str]) -> None:
    signature = process_signature(hello)
    args, options = parse_command_line(argv)
    argsd = deque(args)
    print(args, options)
    for param in signature.parameters.values():
        if param.kind is inspect.Parameter.POSITIONAL_ONLY:
            if argsd:
                echo(argsd.popleft())
            else:
                raise MissingArgumentError(f"Missing argument: {param.name}")
        elif param.kind is inspect.Parameter.KEYWORD_ONLY:
            print(param.name, options)
            if param.name in options:
                echo(options.pop(param.name))
            else:
                import difflib

                matches = difflib.get_close_matches(param.name, options.keys(), n=1, cutoff=0.6)
                print(matches, "a")
                if matches:
                    echo(matches[0])
                    raise MissingArgumentError(f"Wrong argument: {matches[0]}, maybe {param.name}?")

    bound_arguments = signature.bind(*args, **options)
    bound_arguments.apply_defaults()
    hello(*bound_arguments.args, **bound_arguments.kwargs)


if __name__ == "__main__":
    main(argv=sys.argv[1:])

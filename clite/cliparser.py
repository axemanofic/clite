import inspect
from collections import deque
from typing import TYPE_CHECKING, Annotated, Any, Callable, TypeVar, get_args, get_origin, get_type_hints

from ._typing import ParamSpec, TypeAlias
from .errors import CommandNotFoundError, RootCommandNotFoundError
from .params_types import ParamType, covert_type

if TYPE_CHECKING:
    from clite import Clite
    from clite.main import Command


Args: TypeAlias = tuple[str, ...]
Options: TypeAlias = dict[str, str]

P = ParamSpec("P")
T = TypeVar("T")


def get_command(clite_instance: "Clite", argv: list[str]) -> tuple["Command", list[str]]:
    """Get the command from the dictionary of commands.

    :param clite_instance: clite instance
    :param argv: list of arguments
    :return: command and list of arguments
    """
    cmd_key = f"{clite_instance}:{argv[0]}"

    cmd = clite_instance.commands.get(cmd_key)

    if argv[0] == "root" and cmd is None:
        raise RootCommandNotFoundError(argv[0])

    if cmd:
        return cmd, argv[1:]
    raise CommandNotFoundError(argv[0])


def parse_multiple_values(argv: list[str]) -> tuple[str, ...]:
    """Parse multiple values."""
    values: list[str] = []
    for _, arg in enumerate(argv):
        if arg.startswith("-"):
            break
        if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
            arg = arg[1:-1]
        values.append(arg)
    return tuple(values)


def parse_command_line(argv: list[str]) -> tuple[Args, Options]:
    """Parse the command line.

    :param argv: list of arguments
    :return: tuple of arguments and options
    """
    arguments: list[str] = []
    options = {}

    for idx, arg in enumerate(argv):
        if arg in ("-h", "--help"):
            options["help"] = ""
            break
        if arg.startswith("--"):
            try:
                option, value = arg[2:].split("=", maxsplit=1)
            except ValueError:
                option = arg[2:]
                value = argv[idx + 1]
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            options[option] = value
        elif arg.startswith("-"):
            option = arg[1:]
            options[option] = ""
        else:
            arguments.append(arg)
    args = tuple(arguments)
    return args, options


def analyse_signature(
    func: Callable[P, T],
) -> tuple[ParamType, ...]:
    """Analyse the signature of the function.

    :param func: function to be analysed
    :param arguments: list of arguments
    :param options: dictionary of options
    :return: tuple of arguments and options
    """
    signature = inspect.signature(func)

    bound_arguments: list[ParamType] = []

    for param_name, value in signature.parameters.items():
        annotation = signature.parameters[param_name].annotation
        origin = get_origin(annotation)
        if origin is Annotated:
            annotation = get_args(annotation)[0]

        value_type = None
        if value.default is inspect.Parameter.empty:
            value_type = covert_type(
                param_name=param_name,
                value="",
                is_optional=False,
                annotation=annotation,
            )
        else:
            value_type = covert_type(
                param_name=param_name,
                value=str(value.default),
                is_optional=True,
                annotation=annotation,
            )
        bound_arguments.append(value_type)

    return tuple(bound_arguments)


class ArgMeta:
    def __init__(self, *, name: str | None, value: str) -> None:
        self.name = name
        self.value = value


def parse_command_line2(argv: list[str]) -> deque[ArgMeta]:
    """Parse the command line.

    :param argv: list of arguments
    :return: tuple of arguments and options
    """

    args = []

    for idx, arg in enumerate(argv):
        if arg in ("-h", "--help"):
            args.append(ArgMeta(name="help", value=""))
            break
        if arg.startswith("--"):
            try:
                option, value = arg[2:].split("=", maxsplit=1)
            except ValueError:
                option = arg[2:]
                value = argv[idx + 1]
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            args.append(ArgMeta(name=option, value=value))
        elif arg.startswith("-"):
            option = arg[1:]
            args.append(ArgMeta(name=option, value=value))
        else:
            args.append(ArgMeta(name=None, value=arg))
    return deque(args)

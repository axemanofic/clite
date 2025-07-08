import inspect
from typing import TYPE_CHECKING, Annotated, Callable, TypeVar, get_args, get_origin

from ._typing import ParamSpec, TypeAlias
from .errors import CommandNotFoundError
from .params_types import covert_type

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
    if cmd := clite_instance.commands.get(cmd_key):
        return cmd, argv[1:]
    raise CommandNotFoundError.format_message(argv[0])


def parse_multiple_values(
    argv: list[str],
) -> tuple[str, ...]:
    values: list[str] = []
    for idx, arg in enumerate(argv):
        if arg.startswith("-"):
            break
        if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]
        elif arg.startswith("'") and arg.endswith("'"):
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
            options[arg[2:]] = ""
            break
        if arg.startswith("--"):
            try:
                option, value = arg[2:].split("=", maxsplit=1)
            except ValueError:
                option = arg[2:]
                value = argv[idx + 1]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
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
    arguments: tuple[str, ...],
    options: dict[str, str],
) -> tuple[tuple[str, ...], dict[str, str]]:
    """Analyse the signature of the function.

    :param func: function to be analysed
    :param arguments: list of arguments
    :param options: dictionary of options
    :return: tuple of arguments and options
    """
    signature = inspect.signature(func)

    bound_arguments = signature.bind(*arguments, **options)
    bound_arguments.apply_defaults()

    for param_name, value in bound_arguments.arguments.items():
        annotation = signature.parameters[param_name].annotation
        origin = get_origin(annotation)
        if origin is Annotated:
            annotation = get_args(annotation)[0]
        value = covert_type(param_name=param_name, value=value, annotation=annotation).covert()
        bound_arguments.arguments[param_name] = value

    for param_name, value in bound_arguments.kwargs.items():
        annotation = signature.parameters[param_name].annotation
        origin = get_origin(annotation)
        if origin is Annotated:
            annotation = get_args(annotation)[0]
        value = covert_type(param_name=param_name, value=value, annotation=annotation).covert()
        bound_arguments.kwargs[param_name] = value

    return bound_arguments.args, bound_arguments.kwargs

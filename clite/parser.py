# noqa: A005
import inspect
from typing import TYPE_CHECKING, Callable, TypeVar

from typing_extensions import ParamSpec, TypeAlias

from clite.errors import CommandNotFoundError
from clite.params_types import covert_type

if TYPE_CHECKING:
    from clite import Clite
    from clite.main import Command


Args: TypeAlias = tuple[str, ...]
Flags: TypeAlias = dict[str, str]

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
    raise CommandNotFoundError.fomat_message(argv[0])


def parse_command_line(argv: list[str]) -> tuple[Args, Flags]:
    """Parse the command line.

    :param argv: list of arguments
    :return: tuple of arguments and flags
    """
    arguments: list[str] = []
    flags = {}

    for arg in argv:
        if arg.startswith("--"):
            try:
                flag, value = arg[2:].split("=")
            except ValueError:
                flag = arg[2:]
                value = ""
            flags[flag] = value
        elif arg.startswith("-"):
            flag = arg[1:]
            flags[flag] = ""
        else:
            arguments.append(arg)
    args = tuple(arguments)
    return args, flags


def analyse_signature(
    func: Callable[P, T],
    arguments: tuple[str, ...],
    flags: dict[str, str],
) -> tuple[tuple[str, ...], dict[str, str]]:
    """Analyse the signature of the function.

    :param func: function to be analysed
    :param arguments: list of arguments
    :param flags: dictionary of flags
    :return: tuple of arguments and flags
    """
    signature = inspect.signature(func)

    bound_arguments = signature.bind(*arguments, **flags)
    bound_arguments.apply_defaults()

    for param_name, value in bound_arguments.arguments.items():
        annotation = signature.parameters[param_name].annotation
        value = covert_type(param_name=param_name, value=value, annotation=annotation).covert()
        bound_arguments.arguments[param_name] = value

    for param_name, value in bound_arguments.kwargs.items():
        annotation = signature.parameters[param_name].annotation
        value = covert_type(param_name=param_name, value=value, annotation=annotation).covert()
        bound_arguments.kwargs[param_name] = value

    return bound_arguments.args, bound_arguments.kwargs

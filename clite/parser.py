import inspect
from typing import TYPE_CHECKING, Callable, Dict, Tuple, TypeVar

from typing_extensions import ParamSpec, TypeAlias

from clite.errors import BadParameter
from clite.params_types import covert_type

if TYPE_CHECKING:
    from clite import Clite
    from clite.main import Command


Args: TypeAlias = Tuple[str]
Flags: TypeAlias = Dict[str, str]

P = ParamSpec("P")
T = TypeVar("T")


def get_command(
    clite_instance: "Clite", argv: list[str]
) -> tuple["Command", list[str]]:
    cmd_key = f"{clite_instance}:{argv[0]}"
    if cmd := clite_instance.commands.get(cmd_key):
        return cmd, argv[1:]
    else:
        raise Exception("Command not found")


def parse_command_line(argv: list[str]) -> tuple[Args, Flags]:
    arguments = []
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
    args = tuple(i for i in arguments)
    return args, flags


def analyse_signature(func: Callable[P, T], *args, **kwargs) -> tuple[Args, Flags]:  # type: ignore
    signature = inspect.signature(func)

    bound_arguments = signature.bind(*args, **kwargs)
    bound_arguments.apply_defaults()

    for param_name, value in bound_arguments.arguments.items():
        annotation = signature.parameters[param_name].annotation
        value = covert_type(
            param_name=param_name, value=value, annotation=annotation
        ).covert()
        bound_arguments.arguments[param_name] = value

    for param_name, value in bound_arguments.kwargs.items():
        annotation = signature.parameters[param_name].annotation
        value = covert_type(
            param_name=param_name, value=value, annotation=annotation
        ).covert()
        bound_arguments.kwargs[param_name] = value

    return bound_arguments.args, bound_arguments.kwargs

from typing import TYPE_CHECKING, Callable, TypeVar, get_type_hints

from ._typing import ParamSpec
from .params_types import covert_type
from .utils import echo

if TYPE_CHECKING:
    from .main import Clite, Command

P = ParamSpec("P")
T = TypeVar("T")


class Helper:
    def create_help_message(self, func: Callable[P, T]) -> None:
        echo(func)

    def create_help_command(self, cmd: "Command") -> None:
        echo(f"{cmd.name} - {cmd.description}")
        echo(f"Usage: {cmd.name} [OPTIONS]")
        annotations = get_type_hints(cmd.func)
        for param in annotations:
            if param == "return":
                continue
            _param = covert_type(param_name=param, value="", annotation=annotations[param])
            echo(f"{param.upper()} [{_param.param_type}]")
        # for param in cmd.func.__annotations__:
        #     echo(f"{param} - {cmd.func.__annotations__[param]}")

    def create_help_clite(self, instance: "Clite") -> None:
        echo(f"{instance.name} - {instance.description}\n")
        echo(f"Usage: {instance.name} [OPTIONS] <COMMAND>\n")
        echo("Commands:")
        for cmd in instance.commands.values():
            echo(f"{cmd.name} - {cmd.description}")

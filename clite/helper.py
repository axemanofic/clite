from typing import TYPE_CHECKING, get_type_hints

from .params_types import covert_type
from .utils import echo

if TYPE_CHECKING:
    from .main import Clite, Command


class Helper:
    """Helper class."""

    def create_help_command(self, cmd: "Command") -> None:
        """Create help for command.

        :param cmd: command
        :return: None
        """
        echo(f"{cmd.name} - {cmd.description}")
        echo(f"Usage: {cmd.name} [OPTIONS]")
        annotations = get_type_hints(cmd.func)
        for param in annotations:
            if param == "return":
                continue
            _param = covert_type(param_name=param, value="", annotation=annotations[param])
            echo(f"{param} [{_param}]")

    def create_help_clite(self, instance: "Clite") -> None:
        """Create help for clite.

        :param instance: clite instance
        :return: None
        """
        echo(f"{instance.name} - {instance.description}\n")
        echo(f"Usage: {instance.name} [OPTIONS] <COMMAND>\n")
        echo("Commands:")
        for cmd in instance.commands.values():
            if cmd.is_root:
                continue
            echo(f"{cmd.name} - {cmd.description}")

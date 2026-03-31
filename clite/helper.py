from typing import TYPE_CHECKING

from clite.utils import echo

if TYPE_CHECKING:
    from clite._types import Mapping
    from clite.main import Clite
    from clite.parser.commands import Command
    from clite.parser.function import ParameterInfo


class Helper:
    """Helper class."""

    def create_help_command(
        self,
        cmd: "Command",
        params: "Mapping[str, ParameterInfo]",
    ) -> None:
        """Create help for command.

        :param cmd: command
        :return: None
        """
        echo(f"{cmd.name} - {cmd.description}")
        echo(f"Usage: {cmd.name} [OPTIONS]")
        for _, param in params.items():
            if param.is_optional:
                if param.short_name:
                    echo(f"{param.name}/{param.short_name} - {param.annotation} - {param.name}")
                else:
                    echo(f"{param.name} - {param.annotation} - {param.name}")

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

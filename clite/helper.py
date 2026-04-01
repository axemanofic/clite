from typing import TYPE_CHECKING

from rich.console import Console
from rich.containers import Lines
from rich.text import Text

from clite.rich_utils import _to_ansi
from clite.utils import echo

if TYPE_CHECKING:
    from clite._types import Mapping, Sequence
    from clite.main import Clite
    from clite.parser.arguments import ArgumentMeta
    from clite.parser.commands import Command
    from clite.parser.function import ParameterInfo


class Helper:
    """Helper class."""

    def is_show_help_message(self, args: "Sequence[ArgumentMeta]") -> bool:
        """Return tag show help message.

        :param args: list args
        :return: Boolean
        """
        for arg in args:
            if arg.is_optional and arg.name in ("h", "help"):
                return True
            if arg.name == "help":
                return True
        return False

    def create_help_command(
        self,
        instance: "Clite",
        cmd: "Command",
        params: "Mapping[str, ParameterInfo]",
    ) -> None:
        """Create help for command.

        :param cmd: command
        :return: None
        """
        echo(f"{cmd.name} - {cmd.description}\n")
        echo(f"Usage: {instance.name} {cmd.name} [OPTIONS]\n")
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
            echo(f"{cmd.name} - {cmd.description}")


class RichHelper(Helper):
    def __init__(self) -> None:
        self.console = Console(color_system="auto", force_terminal=True, markup=True)
        super().__init__()

    def create_help_command(
        self,
        instance: "Clite",
        cmd: "Command",
        params: "Mapping[str, ParameterInfo]",
    ) -> None:
        """Create help for command.

        :param instance: clite instance
        :param cmd: command
        :return: None
        """
        text = Lines()
        text.append(Text.from_markup(f"[bold]{cmd.name}[/bold] - {cmd.description}\n"))
        text.append(Text.from_markup(f"[bold]Usage[/]: {instance.name} {cmd.name} [OPTIONS]\n"))

        from rich.table import Table

        grid = Table.grid(padding=(0, 3, 0, 0))

        for _, param in params.items():
            if param.is_optional:
                grid.add_row(
                    f"{param.name}/{param.short_name}",
                    f"{param.annotation}",
                    f"{param.name} - \\[default: {param.value}]",
                )
                # text.append(
                #     Text.from_markup(
                #         f"{param.name}/{param.short_name} - {param.annotation} - {param.name} - \\[default: {param.value}]",
                #     ),
                # )
            else:
                grid.add_row(
                    f"{param.name}",
                    f"{param.annotation}",
                    f"{param.name}",
                )
                # text.append(
                #     Text.from_markup(f"{param.name} - {param.annotation} - {param.name}"),
                # )
        _ansi_text = _to_ansi(self.console, text)
        echo(_ansi_text.rstrip("\n"))
        echo(_to_ansi(self.console, grid))

    def create_help_clite(self, instance: "Clite") -> None:
        """Create help for clite.

        :param instance: clite instance
        :return: None
        """
        echo(f"{instance.name} - {instance.description}\n")
        echo(f"Usage: {instance.name} [OPTIONS] <COMMAND>\n")
        echo("Commands:")
        for cmd in instance.commands.values():
            echo(f"{cmd.name} - {cmd.description}")

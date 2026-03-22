from typing import TYPE_CHECKING

from clite._types import Sequence
from clite.errors import CommandNotFoundError, RootCommandNotFoundError

if TYPE_CHECKING:
    from clite.main import Clite, Command


def get_command(
    clite_instance: "Clite",
    argv: Sequence[str],
) -> tuple["Command", Sequence[str]]:
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

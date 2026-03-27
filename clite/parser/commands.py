from collections import deque
from typing import TYPE_CHECKING

from clite._types import Callable, ParamSpec, Sequence, TypeVar
from clite.errors import CommandNotFoundError
from clite.parser.arguments import ArgumentMeta

if TYPE_CHECKING:
    from clite.main import Clite


P = ParamSpec("P")
T = TypeVar("T")


class Command:
    """Command class.

    Class describing the command to be executed
    """

    def __init__(
        self,
        name: str | None,
        description: str | None,
        func: Callable[..., T],
        *,
        is_root: bool = False,
    ) -> None:
        self.name: str = func.__name__ if name is None else name
        self.description = description
        self.func = func
        self.is_root = is_root

    def __repr__(self) -> str:
        """Return the name of the command.

        :return: name of the command
        """
        return self.name.lower()


def parse_command_argv(
    clite_instance: "Clite",
    cmds: deque[ArgumentMeta],
) -> tuple[Command | None, deque[ArgumentMeta]]:
    """Parse the command line arguments.

    :param clite_instance: clite instance
    :param cmds: list of arguments
    :return: command and list of arguments
    """
    cmd: Command | None = None

    orig_cmds = cmds.copy()
    while len(orig_cmds) > 0:
        cmd_key = f"{clite_instance}:{'.'.join([c.value for c in orig_cmds])}"
        cmd = clite_instance.commands.get(cmd_key)

        if cmd is not None:
            break

        orig_cmds.pop()

    return cmd, orig_cmds


def get_command(
    clite_instance: "Clite",
    argv: Sequence[ArgumentMeta],
) -> tuple[Command, deque[ArgumentMeta]]:
    """Get the command from the dictionary of commands.

    :param clite_instance: clite instance
    :param argv: list of arguments
    :return: command and list of arguments
    """
    cmds: deque[ArgumentMeta] = deque()

    for arg in argv:
        if arg.is_optional:
            break
        if arg.name in ("help", "h"):
            break
        cmds.append(arg)

    cmd, args = parse_command_argv(clite_instance, cmds)

    if cmd is None:
        cmd_key = f"{clite_instance}"
        cmd = clite_instance.commands.get(cmd_key)

    if cmd is None:
        raise CommandNotFoundError(" ".join([c.value for c in cmds]))

    argv = deque(filter(lambda x: x not in args, argv))

    return cmd, argv

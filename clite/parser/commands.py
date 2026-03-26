from collections import deque
from typing import TYPE_CHECKING

from clite._types import Callable, Deque, ParamSpec, Sequence, TypeVar
from clite.errors import CommandNotFoundError, RootCommandNotFoundError
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


def get_command(
    clite_instance: "Clite",
    argv: Sequence[ArgumentMeta],
) -> tuple[Command | None, Deque[ArgumentMeta]]:
    """Get the command from the dictionary of commands.

    :param clite_instance: clite instance
    :param argv: list of arguments
    :return: command and list of arguments
    """

    cmd: Command | None = None

    cmds: deque[ArgumentMeta] = deque([])

    for arg in argv:
        if arg.is_optional:
            continue
        if arg.name in ("help"):
            break
        cmds.append(arg)

    print(f"cmds: {cmds}")

    while len(cmds) > 0:
        cmd_key = f"{clite_instance}:{'.'.join([c.value for c in cmds])}"
        cmd = clite_instance.commands.get(cmd_key)

        if cmd is not None:
            break

        cmds.pop()

    print(f"cmds: {cmds}")

    if len(cmds) == 0:
        cmd_key = f"{clite_instance}"
        cmd = clite_instance.commands.get(cmd_key)

    if len(cmds) == 0 and cmd is None:
        raise RootCommandNotFoundError

    if cmd is None:
        raise CommandNotFoundError(" ".join(cmds))

    if len(cmds) > 0:
        idx = argv.index(cmds[-1])
        idx = idx + 1
    else:
        idx = 0

    result = (cmd, deque(argv[idx:]))
    print(f"result: {result}")
    return result

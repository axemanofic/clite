import sys
from typing import Any, Callable, Optional, TypeVar

from ._typing import ParamSpec
from .errors import CliteError
from .helper import Helper
from .parser import analyse_signature, get_command, parse_command_line
from .utils import echo

P = ParamSpec("P")
T = TypeVar("T")


class Command:
    """Command class.

    Class describing the command to be executed
    """

    def __init__(
        self,
        name: Optional[str],
        description: Optional[str],
        func: Callable[..., T],
    ) -> None:
        self.name: str = func.__name__ if name is None else name
        self.description = description
        self.func = func

    def __repr__(self) -> str:
        """Return the name of the command.

        :return: name of the command
        """
        return self.name.lower()


class Clite:
    """Clite class.

    Class containing all the commands
    """

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        description: Optional[str] = None,
    ) -> None:
        self.name = "clite" if name is None else name.lower()
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(
        self,
        name: Optional[str] = None,
        *,
        description: Optional[str] = None,
    ) -> Callable[[Callable[P, T]], Callable[P, None]]:
        """Return wrapper function.

        :param name: name of the command
        :param description: description of the command.
        :return: wrapped function
        """

        def wrapper(func: Callable[P, T]) -> Callable[..., Any]:
            """Return wrapped function.

            Adds the command to the dictionary of commands

            :param func: function to be wrapped
            :return: wrapped function
            """
            cmd = Command(name, description, func)
            self.commands[f"{self}:{cmd}"] = cmd
            return func

        return wrapper

    def _run(self, argv: list[str]) -> None:
        """Run the command.

        ALl magic happens here

        :param argv: list of arguments
        :return: exit code
        """
        if argv:
            if argv[0] in ("--help", "-h"):
                h = Helper()
                h.create_help_clite(self)
                return
            cmd, argv = get_command(self, argv)
            if argv[-1] in ("--help", "-h"):
                h = Helper()
                h.create_help_command(cmd)
                return
            arguments, flags = parse_command_line(argv)
            arguments, flags = analyse_signature(cmd.func, arguments, flags)
            cmd.func(*arguments, **flags)

    def __repr__(self) -> str:
        """Return the name of the app.

        :return: name of the app
        """
        return self.name

    def __call__(self) -> int:
        """Call app intsance for run the command.

        :return: exit code
        """
        try:
            self._run(sys.argv[1:])
        except CliteError as err:
            echo(err, file=sys.stderr)
            return 1
        else:
            return 0

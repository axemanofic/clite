import sys
from collections.abc import Callable
from typing import Any, TypeVar

from ._types import Sequence
from ._typing import ParamSpec
from .converter import convert_params_value
from .errors import CliteError, RootCommandNotFoundError
from .helper import Helper
from .mapping import mapping_param_and_meta
from .parser.arguments import parse_argv
from .parser.commands import get_command
from .parser.function import analyse_signature
from .utils import echo

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


class Clite:
    """Clite class.

    Class containing all the commands
    """

    def __init__(
        self,
        name: str | None = None,
        *,
        description: str | None = None,
    ) -> None:
        self.name = "clite" if name is None else name.lower()
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(
        self,
        name: str | None = None,
        *,
        description: str | None = None,
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

    def root(
        self,
        name: str | None = None,
        *,
        description: str | None = None,
    ) -> Callable[[Callable[P, T]], Callable[P, None]]:
        """Return wrapper function.

        :param name: name of the command
        :param description: description of the command.
        :return: wrapped function
        """

        def wrapper(func: Callable[P, T]) -> Callable[..., Any]:
            """Return wrapped function.

            Adds the root command to the dictionary of commands

            :param func: function to be wrapped
            :return: wrapped function
            """
            cmd = Command(name, description, func, is_root=True)
            self.commands[f"{self}:{cmd}"] = cmd
            return func

        return wrapper

    def _run(self, argv: Sequence[str]) -> None:
        """Run the command.

        ALl magic happens here

        :param argv: list of arguments
        :return: exit code
        """
        if not argv:
            argv = ["root"]

        try:
            cmd, argv = get_command(self, argv)
        except RootCommandNotFoundError:
            h = Helper()
            h.create_help_clite(self)
            return

        arguments = parse_argv(argv)

        for arg in arguments:
            if arg.name == "help":
                h = Helper()
                h.create_help_command(cmd)
                return

        params = analyse_signature(cmd.func)

        params = mapping_param_and_meta(params, arguments)
        params = convert_params_value(params)

        args: list[Any] = []
        kwargs: dict[str, Any] = {}
        for _, p in params.items():
            if p.is_optional:
                kwargs[p.name] = p.value
            else:
                args.append(p.value)

        cmd.func(*args, **kwargs)

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
            echo(err.__str__(), file=sys.stderr)
            return err.exit_code
        else:
            return 0

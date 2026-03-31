import sys
from collections.abc import Callable
from typing import Any, TypeVar

from clite._types import Sequence
from clite._typing import ParamSpec
from clite.converter import convert_params_value
from clite.errors import CliteError
from clite.helper import Helper
from clite.mapping import mapping_param_and_meta
from clite.parser.arguments import parse_argv
from clite.parser.commands import Command, get_command
from clite.parser.function import analyse_signature
from clite.utils import echo, split_args_kwargs

P = ParamSpec("P")
T = TypeVar("T")


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
        self.helper: Helper = Helper()

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
            self.commands[f"{self}"] = cmd
            return func

        return wrapper

    def _run(self, argv: Sequence[str]) -> None:
        """Run the command.

        ALl magic happens here

        :param argv: list of arguments
        :return: exit code
        """
        arguments = parse_argv(argv)

        cmd, arguments = get_command(self, arguments)
        params = analyse_signature(cmd.func)

        self.helper.create_help_command(cmd, params)
        return

        params = mapping_param_and_meta(params, arguments)
        params = convert_params_value(params)
        args, kwargs = split_args_kwargs(params)

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

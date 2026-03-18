import sys
from typing import Any, Callable, Optional, TypeVar

from ._typing import ParamSpec
from .cliparser import analyse_signature, get_command, parse_command_line, parse_command_line2
from .errors import CliteError, MissingRequiredParameterError, RootCommandNotFoundError
from .helper import Helper
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

    def __init__(self, name: Optional[str] = None, *, description: Optional[str] = None) -> None:
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

    def root(
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

            Adds the root command to the dictionary of commands

            :param func: function to be wrapped
            :return: wrapped function
            """
            cmd = Command(name, description, func, is_root=True)
            self.commands[f"{self}:{cmd}"] = cmd
            return func

        return wrapper

    def _run(self, argv: list[str]) -> None:
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

        params = analyse_signature(cmd.func)

        arguments = parse_command_line2(argv)

        print(params, arguments)

        args: list[Any, ...] = []
        kwargs: dict[str, Any] = {}

        for p in params:
            while len(arguments) > 0:
                a = arguments.popleft()
                p.value = a.value
                v = p.covert()
                if p.is_optional:
                    kwargs[p.param_name] = v
                else:
                    args.append(v)
                break
            if p.value == "":
                raise MissingRequiredParameterError(p.param_name)
            if p.is_optional:
                kwargs[p.param_name] = p.covert()
        # if "help" in flags:
        #     h = Helper()
        #     h.create_help_command(cmd)
        #     return

        print(args, kwargs)

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

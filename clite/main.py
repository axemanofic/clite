from collections.abc import Callable
from typing import Any, Optional

from clite.types import Argv


class Command:
    def __init__(
        self,
        name: Optional[None],
        description: Optional[None],
        func: Callable,
    ):
        self.name = func.__name__ if name is None else name
        self.description = description
        self.func = func


class Clite:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(
        self,
        name: Optional[None] = None,
        description: Optional[None] = None,
    ):
        def wrapper(func: Callable):
            cmd = Command(name, description, func)
            self.commands[cmd.name] = cmd
            return func

        return wrapper

    def run(
        self,
        argv: Argv,
    ) -> None:
        if argv is None:
            argv = []
        try:
            self.commands[argv[0]].func()
        except Exception as e:
            print(e)
        finally:
            import sys

            sys.stdout.flush()
            stdout = sys.stdout

        for line in stdout:
            print(f"line={line}")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise Exception("Not implemented")
        self.commands["test"].func(*args, **kwds)

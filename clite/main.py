from collections.abc import Callable
from typing import Any


class Command:
    def __init__(self, name: str | None, description: str | None, func: Callable):
        self.name = func.__name__ if name is None else name
        self.description = description
        self.func = func


class Clite:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(self, name: str | None = None, description: str | None = None):
        def wrapper(func: Callable):
            cmd = Command(name, description, func)
            self.commands[cmd.name] = cmd
            return func

        return wrapper

    def run(
        self,
        argv: list[str] | None = None,
    ) -> None:
        if argv is None:
            argv = []
        self.commands[argv[0]].func()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise Exception("Not implemented")
        self.commands["test"].func(*args, **kwds)

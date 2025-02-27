from collections.abc import Callable
from typing import Any, Optional

from clite.types import Argv


class Command:
    def __init__(self, name: Optional[str], description: Optional[str], func: Callable):
        self.name = func.__name__ if name is None else name
        self.description = description
        self.func = func

    def __repr__(self):
        return self.name.lower()


class Clite:
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = "clite" if name is None else name.lower()
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(self, name: Optional[str] = None, description: Optional[str] = None):
        def wrapper(func: Callable):
            cmd = Command(name, description, func)
            self.commands[f"{self}:{cmd}"] = cmd
            return func

        return wrapper

    def run(self, argv: Argv) -> Any:
        print(argv)
        if argv is None:
            argv = []
        return self.commands[f"{self}:{argv[0]}"].func()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print(args, kwds)
        self.commands[f"{self}:test"].func(*args, **kwds)

    def __repr__(self):
        if self.name is None:
            return "clite"
        return self.name.lower()

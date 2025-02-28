from collections.abc import Callable
from typing import Any, Optional

from clite.parser import get_command, parse_command_line
from clite.types import Argv


class Result:
    def __init__(self, code: int = 0):
        self.code = code

    def __repr__(self) -> str:
        return str(self.code)


class Command:
    def __init__(self, name: Optional[str], description: Optional[str], func: Callable):
        self.name: str = func.__name__ if name is None else name
        self.description = description
        self.func = func

    def __repr__(self) -> str:
        return self.name.lower()


class Clite:
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = "clite" if name is None else name.lower()
        self.description = description
        self.commands: dict[str, Command] = {}

    def command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        def wrapper(func: Callable) -> Callable:
            cmd = Command(name, description, func)
            self.commands[f"{self}:{cmd}"] = cmd
            return func

        return wrapper

    def _run(self, *args: Any, **kwds: Any) -> Result:
        try:
            cmd, argv = get_command(self, args[0])
            args, flags = parse_command_line(argv)
            cmd.func(*args, **flags)
        except Exception:
            return Result(1)
        else:
            return Result(0)

    def __call__(self, *args: Any, **kwds: Any) -> Result:
        return self._run(*args, **kwds)

    def __repr__(self) -> str:
        return self.name

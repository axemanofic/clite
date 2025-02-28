from typing import TYPE_CHECKING, Dict, Tuple

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from clite import Clite
    from clite.main import Command


Args: TypeAlias = Tuple[str]
Flags: TypeAlias = Dict[str, str]


def get_command(
    clite_instance: "Clite", argv: list[str]
) -> tuple["Command", list[str]]:
    cmd_key = f"{clite_instance}:{argv[0]}"
    if cmd := clite_instance.commands.get(cmd_key):
        return cmd, argv[1:]
    else:
        raise Exception("Command not found")


def parse_command_line(argv: list[str]) -> tuple[Args, Flags]:
    arguments = []
    flags = {}

    for arg in argv:
        if arg.startswith("--"):
            try:
                flag, value = arg[2:].split("=")
            except ValueError:
                flag = arg[2:]
                value = ""
            flags[flag] = value
        elif arg.startswith("-"):
            flag = arg[1:]
            flags[flag] = ""
        else:
            arguments.append(arg)
    args = tuple(i for i in arguments)
    return args, flags

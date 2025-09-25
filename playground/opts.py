import inspect
from collections import deque
from typing import Annotated

from clite.parser import Args, Options

FLAG_MARKS = ("--", "-")

HELP_MARKS = ("--help", "-h")


class Option:
    nargs = -1


class Argument:
    nargs = -1


def demo(
    ips: Annotated[list[str], Argument()],
    data: Annotated[list[int], Option()],
    is_show: bool = False,
) -> None:
    pass


def is_opt(arg: str):
    if arg.startswith(FLAG_MARKS):
        return True
    return False


def is_opt_arg(arg: str):
    return (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'"))


def parse_opts(argv: list[str], params: dict[str, str]) -> tuple[Args, Options]:
    """Do Some docs."""
    print(argv)
    signature = inspect.signature(demo)
    params = signature.parameters
    print(params)

    c = list(set(argv) & set(HELP_MARKS))

    args, options = [], {}

    d = deque(argv)

    if c:
        return (), {"help": ""}
    while True:
        try:
            arg = d.popleft()
        except IndexError:
            break
        if arg.startswith("--"):
            try:
                option, value = arg[2:].split("=", maxsplit=1)
            except ValueError:
                option = arg[2:]
            try:
                value = d.popleft()
            except IndexError:
                value = ""

            if is_opt_arg(arg):
                value = value[1:-1]
            options[option] = value
        elif arg.startswith("-"):
            option = arg[1:]
            options[option] = ""
        else:
            args.append(arg)

    print(args, options)

    return (), {}


# def parse_command_line(argv: list[str]) -> tuple[Args, Options]:
#     """Parse the command line.
#
#     :param argv: list of arguments
#     :return: tuple of arguments and options
#     """
#     arguments: list[str] = []
#     options = {}
#
#     for idx, arg in enumerate(argv):
#         if arg in ("-h", "--help"):
#             options["help"] = ""
#             break
#         if arg.startswith("--"):
#             try:
#                 option, value = arg[2:].split("=", maxsplit=1)
#             except ValueError:
#                 option = arg[2:]
#                 value = argv[idx + 1]
#             if value.startswith('"') and value.endswith('"'):
#                 value = value[1:-1]
#             elif value.startswith("'") and value.endswith("'"):
#                 value = value[1:-1]
#             options[option] = value
#         elif argv[idx - 1].startswith(("--", "-")):
#             continue
#         elif arg.startswith("-"):
#             option = arg[1:]
#             options[option] = ""
#         else:
#             arguments.append(arg)
#     args = tuple(arguments)
#     return args, options


def main(argv: list[str]):
    signature = inspect.signature(demo)
    parse_opts(argv, signature.parameters)


if __name__ == "__main__":
    import sys

    main(argv=sys.argv[1:])

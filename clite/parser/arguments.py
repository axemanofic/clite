from collections import deque

from clite._types import Any, MutableSequence, Sequence


class ArgumentMeta:
    """Meta information about argument cli."""

    def __init__(
        self,
        *,
        name: str,
        value: str | None,
        is_optional: bool = False,
    ) -> None:
        self.name = name
        self.value = value
        self.is_optional = is_optional

    def __repr__(self) -> str:
        """Return the type of the parameter."""
        return f"ArgumentMeta({self.name}={self.value})"


def replace_quotes(value: str) -> str:
    """Replace quotes in the value."""
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    return value


def parse_opt(*, opt: str, is_short: bool = False) -> Sequence[ArgumentMeta]:
    """Parse the command line options."""
    opts = []

    value: Any | None = None

    try:
        name, value = opt.split("=", maxsplit=1)
    except ValueError:
        name = opt
        value = None

    if value is not None:
        value = replace_quotes(value)

    print(name, value, "parse_opt")

    if is_short and len(name) > 1:
        for n in name:
            opts.append(
                ArgumentMeta(
                    name=n,
                    value=value,
                    is_optional=True,
                ),
            )
    else:
        opts.append(
            ArgumentMeta(
                name=name,
                value=value,
                is_optional=True,
            ),
        )
    return opts


def parse_argv(argv: Sequence[str]) -> MutableSequence[ArgumentMeta]:
    """Parse the command line arguments."""
    argvd: deque[str] = deque(argv)

    argv_pipe: MutableSequence[ArgumentMeta] = []

    print(argvd, "argvd")

    while len(argvd) > 0:
        arg = argvd.popleft()
        if arg in ("-h", "--help", "help"):
            argv_pipe.append(
                ArgumentMeta(
                    name="help",
                    value="help",
                    is_optional=True,
                ),
            )
            break
        if arg.startswith("--"):
            opts = parse_opt(opt=arg[2:], is_short=False)
            argv_pipe.extend(opts)
            continue
        if arg.startswith("-"):
            opts = parse_opt(opt=arg[1:], is_short=True)
            argv_pipe.extend(opts)
            continue
        if len(argv_pipe) > 0 and argv_pipe[-1].is_optional and argv_pipe[-1].value is None:
            arg = replace_quotes(arg)
            argv_pipe[-1].value = arg
            continue
        argv_pipe.append(
            ArgumentMeta(
                name="argument",
                value=arg,
                is_optional=False,
            ),
        )

    print(argv_pipe, "argv_pipe")

    return argv_pipe

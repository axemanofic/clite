from collections import deque
from typing import Any

from ._types import Empty, Mapping, MutableSequence, Sequence
from .errors import NoSuchOptionError, UnexpectedExtraArgumentsError
from .parser.arguments import ArgumentMeta
from .parser.function import ParameterInfo


def mapping_param_and_meta(
    params: Mapping[str, ParameterInfo],
    args: Sequence[ArgumentMeta],
) -> Mapping[str, ParameterInfo]:
    """Map the parameters info to the arguments meta."""
    arguments = deque(args)
    extra_args: MutableSequence[Any] = []

    while len(arguments) > 0:
        arg = arguments.popleft()

        for _, p in params.items():
            if p.is_optional and arg.is_optional and arg.name in p.names():
                p.value = arg.value
                continue

            if arg.is_optional and arg.name not in params:
                raise NoSuchOptionError(arg.name)

            if not p.is_optional and not arg.is_optional and p.value == Empty:
                p.value = arg.value
                break

        if not arg.is_optional and p.value != arg.value:
            extra_args.append(arg)
            continue

    if len(extra_args) > 0:
        raise UnexpectedExtraArgumentsError([a.value for a in extra_args])

    return params

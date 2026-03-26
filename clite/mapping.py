from typing import Any

from ._types import Deque, Empty, Mapping, MutableSequence
from .errors import NoSuchOptionError, UnexpectedExtraArgumentsError
from .parser.arguments import ArgumentMeta
from .parser.function import ParameterInfo


def mapping_param_and_meta(
    params: Mapping[str, ParameterInfo],
    arguments: Deque[ArgumentMeta],
) -> Mapping[str, ParameterInfo]:
    """Map the parameters info to the arguments meta."""
    extra_args: MutableSequence[Any] = []

    print(f"arguments: {arguments}")
    while len(arguments) > 0:
        arg = arguments.popleft()

        for _, p in params.items():
            if p.is_optional and arg.is_optional and arg.name in p.names():
                p.value = arg.value
                continue

            if arg.is_optional and arg.name not in params:
                raise NoSuchOptionError(arg.name)

            # print(p.value == Empty, p.value, Empty)
            if not p.is_optional and not arg.is_optional and p.value == Empty:
                # print(p, arg, "ZALUPA")
                p.value = arg.value
                break
            # print(p, arg)

        if len(params.items()) == 0:
            extra_args.append(arg)
            continue
        if not arg.is_optional and p.value != arg.value:
            extra_args.append(arg)
            continue

    # print(params)
    if len(extra_args) > 0:
        raise UnexpectedExtraArgumentsError([a.value for a in extra_args])

    return params

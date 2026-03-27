from collections.abc import Callable as Callable
from collections.abc import Mapping as Mapping
from collections.abc import MutableMapping as MutableMapping
from collections.abc import MutableSequence as MutableSequence
from collections.abc import Sequence as Sequence
from inspect import Parameter as Parameter
from typing import Any as Any
from typing import ParamSpec as ParamSpec
from typing import TypeAlias as TypeAlias
from typing import TypeVar as TypeVar

Empty = Parameter.empty


__all__ = [
    "Any",
    "Callable",
    "Empty",
    "Mapping",
    "MutableMapping",
    "MutableSequence",
    "ParamSpec",
    "Sequence",
    "TypeAlias",
    "TypeVar",
]

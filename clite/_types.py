from collections.abc import Mapping as Mapping
from collections.abc import MutableMapping as MutableMapping
from collections.abc import MutableSequence as MutableSequence
from collections.abc import Sequence as Sequence
from inspect import _empty
from typing import Any as Any

Empty = _empty

__all__ = [
    "Any",
    "Empty",
    "Mapping",
    "MutableMapping",
    "MutableSequence",
    "Sequence",
]

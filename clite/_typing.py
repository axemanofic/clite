import sys

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias
else:
    from typing_extensions import ParamSpec, TypeAlias

__all__ = (
    "ParamSpec",
    "TypeAlias",
)

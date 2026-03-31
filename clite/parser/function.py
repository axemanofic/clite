import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Annotated, TypeVar, get_args, get_origin

from clite._types import Any, Empty, Mapping
from clite._typing import ParamSpec

if TYPE_CHECKING:
    from clite._types import MutableMapping


P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class ParameterInfo:
    """Base class for parameter types."""

    name: str
    value: Any | None
    annotation: Any
    is_optional: bool = False
    short_name: str | None = None

    def names(self) -> tuple[str, ...]:
        """Return the names of the parameter.

        :return: names of the parameter
        """
        if self.short_name is None:
            return (self.name,)
        return (self.name, self.short_name)


class ArgumentInfo(ParameterInfo):
    """Information about argument in the function."""

    def __init__(
        self,
        *,
        name: str,
        value: Any | None,
        annotation: Any,
        is_optional: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            value=value,
            annotation=annotation,
            is_optional=is_optional,
            short_name=None,
        )


class OptionInfo(ParameterInfo):
    """Information about option in the function."""

    def __init__(
        self,
        *,
        name: str,
        value: Any | None,
        annotation: Any,
        is_optional: bool = True,
        short_name: str | None = None,
    ) -> None:
        super().__init__(
            name=name,
            value=value,
            annotation=annotation,
            is_optional=is_optional,
            short_name=short_name,
        )


def analyse_signature(
    func: Callable[P, T],
) -> Mapping[str, ParameterInfo]:
    """Analyse the signature of the function.

    :param func: function to be analysed
    :return: dict of parameters
    """
    signature = inspect.signature(func)

    bound_arguments: MutableMapping[str, ParameterInfo] = {}

    for param_name, value in signature.parameters.items():
        annotation = signature.parameters[param_name].annotation
        if annotation == Empty:
            annotation = str
        origin = get_origin(annotation)
        if origin is Annotated:
            annotation = get_args(annotation)[0]

        if value.default == Empty:
            bound_arguments[param_name] = ArgumentInfo(
                name=param_name,
                value=value.default,
                annotation=annotation,
                is_optional=False,
            )
        else:
            bound_arguments[param_name] = OptionInfo(
                name=param_name,
                value=value.default,
                annotation=annotation,
                is_optional=True,
            )

    return bound_arguments

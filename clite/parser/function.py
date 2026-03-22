import inspect
from collections.abc import MutableMapping
from typing import Annotated, Callable, TypeVar, get_args, get_origin

from clite._types import Any, Empty, Mapping
from clite._typing import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


class ParameterInfo:
    """Base class for parameter types."""

    def __init__(
        self,
        *,
        name: str,
        value: Any | None,
        annotation: Any,
        is_optional: bool = False,
    ) -> None:
        self.name = name
        self.value = value
        self.annotation = annotation
        self.is_optional = is_optional

    def __repr__(self) -> str:
        """Return the type of the parameter.

        :return: type of the parameter
        """
        return f"ParameterInfo(name={self.name}, value={self.value}, annotation={self.annotation})"

    def __str__(self) -> str:
        """Return the type of the parameter.

        :return: type of the parameter
        """
        return self.__repr__()


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
    ) -> None:
        super().__init__(
            name=name,
            value=value,
            annotation=annotation,
            is_optional=is_optional,
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

        if value.default is Empty:
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

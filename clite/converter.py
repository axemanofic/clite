from typing import TYPE_CHECKING

from ._types import Any, Empty, Mapping
from .errors import MissingRequiredArgumentError
from .params_types import BoolType, FloatType, IntegerType, ParamType, StringType

if TYPE_CHECKING:
    from .parser.function import ParameterInfo

_PARAM_TYPES = {
    int: IntegerType,
    bool: BoolType,
    float: FloatType,
    str: StringType,
}


def covert_type(*, param_name: str, value: Any, annotation: type) -> ParamType:
    """Convert the value to the desired type."""
    param: type[ParamType] | None = _PARAM_TYPES.get(annotation)
    if param is None:
        param = StringType
    return param(param_name=param_name, value=value)


def convert_params_value(
    params: Mapping[str, "ParameterInfo"],
) -> Mapping[str, "ParameterInfo"]:
    """Convert the value to the desired type."""
    for _, p in params.items():
        if p.value == Empty:
            raise MissingRequiredArgumentError(p.name)

    for _, p in params.items():
        _type = covert_type(
            param_name=p.name,
            value=p.value,
            annotation=p.annotation,
        )
        p.value = _type.convert()

    return params

from typing import Any

from clite.errors import BadParameter


class ParamType:
    def __init__(self, *, param_name: str, value: str) -> None:
        self.param_name = param_name
        self.value = value

    def __repr__(self) -> str:
        return self.value

    def covert(self) -> Any:
        raise NotADirectoryError


class IntegerType(ParamType):
    def covert(self) -> int:
        try:
            return int(self.value)
        except ValueError:
            raise BadParameter.fomat_message(param_hint=self.param_name, message=self.value)


class StringType(ParamType):
    def covert(self) -> str:
        return self.value


class BoolType(ParamType):
    def covert(self) -> bool:
        value = self.value.lower()
        if value in ("1", "true", "t", "yes", "y", "on"):
            return True
        if value in ("0", "false", "f", "no", "n", "off"):
            return False
        raise BadParameter.fomat_message(param_hint=self.param_name, message=self.value)


class FloatType(ParamType):
    def covert(self) -> float:
        try:
            return float(self.value)
        except ValueError:
            raise BadParameter.fomat_message(param_hint=self.param_name, message=self.value)


def covert_type(*, param_name: str, value: str, annotation: type) -> ParamType:
    if annotation == int:
        return IntegerType(param_name=param_name, value=value)
    if annotation == bool:
        return BoolType(param_name=param_name, value=value)
    if annotation == float:
        return FloatType(param_name=param_name, value=value)
    if annotation == str:
        return StringType(param_name=param_name, value=value)
    return StringType(param_name=param_name, value=value)

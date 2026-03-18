from typing import Any

from .errors import BadParameterError


class ParamType:
    """Base class for parameter types."""

    def __init__(self, *, param_name: str, value: str, is_optional: bool) -> None:
        self.param_name = param_name
        self.value = value
        self.is_optional = is_optional

    def covert(self) -> Any:  # noqa: ANN401
        """Convert the value to the desired type."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Return the type of the parameter.

        :return: type of the parameter
        """
        raise NotImplementedError


class IntegerType(ParamType):
    """Integer parameter type."""

    def __repr__(self) -> str:
        """Return the type of the parameter."""
        return f"INTEGER({self.param_name}:{self.value})"

    def covert(self) -> int:
        """Convert the value to an integer."""
        try:
            return int(self.value)
        except ValueError as exc:
            raise BadParameterError(
                param_hint=self.param_name,
                message=self.value,
            ) from exc


class StringType(ParamType):
    """String parameter type."""

    def __repr__(self) -> str:
        """Return the type of the parameter."""
        return f"STRING({self.param_name}:{self.value})"

    def covert(self) -> str:
        """Convert the value to a string."""
        return self.value


class BoolType(ParamType):
    """Boolean parameter type."""

    def __repr__(self) -> str:
        """Return the type of the parameter."""
        return f"BOOLEAN({self.param_name}:{self.value})"

    def covert(self) -> bool:
        """Convert the value to a boolean."""
        value = self.value.lower()
        if value in ("1", "true", "t", "yes", "y", "on"):
            return True
        if value in ("0", "false", "f", "no", "n", "off"):
            return False
        raise BadParameterError(param_hint=self.param_name, message=self.value)


class FloatType(ParamType):
    """Float parameter type."""

    def __repr__(self) -> str:
        """Return the type of the parameter."""
        return f"FLOAT({self.param_name}:{self.value})"

    def covert(self) -> float:
        """Convert the value to a float."""
        try:
            return float(self.value)
        except ValueError as exc:
            raise BadParameterError(param_hint=self.param_name, message=self.value) from exc


def covert_type(*, param_name: str, value: str, is_optional: bool, annotation: type) -> ParamType:
    """Convert the value to the desired type."""
    if annotation is int:
        return IntegerType(param_name=param_name, value=value, is_optional=is_optional)
    if annotation is bool:
        return BoolType(param_name=param_name, value=value, is_optional=is_optional)
    if annotation is float:
        return FloatType(param_name=param_name, value=value, is_optional=is_optional)
    if annotation is str:
        return StringType(param_name=param_name, value=value, is_optional=is_optional)
    return StringType(param_name=param_name, value=value, is_optional=is_optional)

class BaseType:
    """Base class."""

    def __init__(self, name: str, *, description: str | None = None, nargs: int = 1) -> None:
        self.name = name
        self.description = description
        self.nargs = nargs

    def __repr__(self) -> str:
        """Return the name of the parameter."""
        return self.name


class Argument(BaseType):
    """Argument class."""


class Option(BaseType):
    """Option class."""

    def __init__(self, name: str, *, description: str | None = None, default: str | None = None) -> None:
        super().__init__(name, description=description)
        self.default = default

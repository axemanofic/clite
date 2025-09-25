from typing import Optional


class BaseType:
    def __init__(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        nargs: int = 1,
    ) -> None:
        self.name = name
        self.description = description
        self.nargs = nargs

    def __repr__(self) -> str:
        return self.name


class Argument(BaseType):
    pass


class Option(BaseType):
    def __init__(
        self,
        name: str,
        *,
        description: Optional[str] = None,
        default: Optional[str] = None,
    ) -> None:
        super().__init__(name, description=description)
        self.default = default

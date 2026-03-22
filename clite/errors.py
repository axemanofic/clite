from enum import IntEnum

from ._types import Any


class ExitCode(IntEnum):
    """Description exit codes for shell."""

    GENERAL = 1  # general error
    SHELL = 2  # shell error


class CliteError(Exception):
    """Clite error."""

    exit_code = ExitCode.GENERAL


class RootCommandNotFoundError(CliteError):
    """Command not found error."""

    exit_code = ExitCode.SHELL

    def __init__(self, message: str) -> None:
        super().__init__(f"Root command not found: {message}")


class CommandNotFoundError(CliteError):
    """Command not found error."""

    exit_code = ExitCode.SHELL

    def __init__(self, message: str) -> None:
        super().__init__(f"Command not found: {message}")


class BadParameterError(CliteError):
    """Bad parameter error."""

    exit_code = ExitCode.SHELL

    def __init__(self, param_hint: str, message: Any) -> None:
        super().__init__(f"Invalid value for '{param_hint}': {message}")


class MissingRequiredArgumentError(CliteError):
    """Missing required argument error."""

    exit_code = ExitCode.SHELL

    def __init__(self, param_hint: str) -> None:
        super().__init__(f"Missing required argument: {param_hint}")


class UnexpectedExtraArgumentsError(CliteError):
    """Got unexpected extra arguments error."""

    exit_code = ExitCode.SHELL

    def __init__(self, arguments: list[str]) -> None:
        message = ", ".join(arguments)
        super().__init__(f"Got unexpected extra arguments: ({message})")


class NoSuchOptionError(CliteError):
    """No such option error."""

    exit_code = ExitCode.SHELL

    def __init__(self, option: str) -> None:
        super().__init__(f"No such option: {option}")

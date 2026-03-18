from enum import IntEnum


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

    def __init__(self, param_hint: str, message: str) -> None:
        super().__init__(f"Invalid value for '{param_hint}': {message}")


class MissingRequiredParameterError(CliteError):
    """Missing required parameter error."""

    exit_code = ExitCode.SHELL

    def __init__(self, param_hint: str) -> None:
        super().__init__(f"Missing required parameter: {param_hint}")

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

    @classmethod
    def format_message(cls, message: str) -> "RootCommandNotFoundError":
        """Format error message.

        :return: RootCommandNotFoundError instance with formatted message
        """
        return cls(f"Root command not found: {message}")


class CommandNotFoundError(CliteError):
    """Command not found error."""

    exit_code = ExitCode.SHELL

    @classmethod
    def format_message(cls, message: str) -> "CommandNotFoundError":
        """Format error message.

        :return: CommandNotFoundError instance with formatted message
        """
        return cls(f"Command not found: {message}")


class BadParameterError(CliteError):
    """Bad parameter error."""

    exit_code = ExitCode.SHELL

    @classmethod
    def format_message(cls, param_hint: str, message: str) -> "BadParameterError":
        """Format error message.

        :return: BadParameter instance with formatted message
        """
        return cls(f"Invalid value for {param_hint}: {message}")

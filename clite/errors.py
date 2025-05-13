class CliteError(Exception):
    """Clite error."""


class CommandNotFoundError(CliteError):
    """Command not found error."""

    @classmethod
    def format_message(cls, message: str) -> "CommandNotFoundError":
        """Format error message.

        :return: CommandNotFoundError instance with formatted message
        """
        return cls(f"Command not found: {message}")


class BadParameterError(CliteError):
    """Bad parameter error."""

    @classmethod
    def format_message(cls, param_hint: str, message: str) -> "BadParameterError":
        """Format error message.

        :return: BadParameter instance with formatted message
        """
        return cls(f"Invalid value for {param_hint}: {message}")

from clite import Clite
from clite.errors import CliteError


class Result:
    """Result class for testing."""

    def __init__(self, exit_code: int = 0) -> None:
        self.exit_code = exit_code


class CliRunner:
    """CliRunner class for testing."""

    def invoke(self, clite_instance: Clite, argv: list[str]) -> Result:
        """Invoke the command.

        :param clite_instance: clite instance
        :param argv: list of arguments
        :return: exit code
        """
        try:
            clite_instance._run(argv)  # noqa: SLF001
        except CliteError:
            return Result(exit_code=1)
        return Result(exit_code=0)

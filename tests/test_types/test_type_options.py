from typing import Annotated

from clite.testing import CliRunner
from clite.typing import Option


def test_flags(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(
        flag_int: Annotated[int, Option("--flag_int")] = 3,
        flag_float: Annotated[float, Option("--flag_float")] = 0.3,
        flag_str: Annotated[str, Option("--flag_str")] = "world",
        flag_bool: Annotated[bool, Option("--flag_bool")] = False,
    ) -> None:
        pass

    result = runner.invoke(
        app, ["todo_list", "--flag_int=1", "--flag_float=0.5", "--flag_str=hello1", "--flag_bool=true"]
    )

    assert result.exit_code == 0


def test_flags_error(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(flag_int: Annotated[int, Option("--flag_int")] = 3) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "--flag_int=asdasd"])

    assert result.exit_code == 1

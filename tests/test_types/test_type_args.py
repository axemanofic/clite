from typing import Annotated

import pytest

from clite.clityping import Argument
from clite.testing import CliRunner


@pytest.mark.skip(reason="this test is currently broken")
def test_arguments(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(
        arg_int: Annotated[int, Argument("name arg")],
        arg_float: Annotated[float, Argument("name arg")],
        arg_str: Annotated[str, Argument("name arg")],
        arg_bool: Annotated[bool, Argument("name arg")],
    ) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "1", "0.5", "hello", "true"])

    assert result.exit_code == 0


@pytest.mark.skip(reason="this test is currently broken")
def test_arguments_bad(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(
        arg_int: Annotated[bool, Argument("name arg")],
    ) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "dasd"])

    assert result.exit_code == 2

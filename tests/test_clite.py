from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clite.testing import CliRunner


def test_create_app():
    from clite import Clite

    app = Clite("test_app", "test_descr")

    assert app.name == "test_app"
    assert app.description == "test_descr"


def test_create_command():
    from clite import Clite

    app = Clite("test_app", "test_descr")

    @app.command(name="test_command", description="test_descr")
    def test_command():
        pass

    command_key = f"{app.name}:test_command"

    assert app.commands[command_key].name == "test_command"
    assert app.commands[command_key].description == "test_descr"


def test_run_command(runner: "CliRunner"):
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list() -> None:
        pass

    result = runner.invoke(app, ["todo_list"])
    assert result.code == 0


def test_arguments(runner: "CliRunner"):
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg1: int, arg2: str) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "1", "hello"])
    assert result.code == 0

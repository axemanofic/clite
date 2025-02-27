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
    def test_command():
        return 1 + 1

    result = runner.invoke(app, ["test_command"])
    assert result == 0

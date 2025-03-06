from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from clite.testing import CliRunner


def test_create_app() -> None:
    from clite import Clite

    app = Clite("test_app", "test_descr")

    assert app.name == "test_app"
    assert app.description == "test_descr"


def test_create_command() -> None:
    from clite import Clite

    app = Clite("test_app", "test_descr")

    @app.command(name="test_command", description="test_descr")
    def test_command():
        pass

    command_key = f"{app.name}:test_command"

    assert app.commands[command_key].name == "test_command"
    assert app.commands[command_key].description == "test_descr"


def test_run_command(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list() -> None:
        pass

    result = runner.invoke(app, ["todo_list"])
    assert result.exit_code == 0


def test_arguments(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg_int: int, arg_float: float, arg_str: str, arg_bool: bool) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "1", "0.5", "hello", "true"])

    assert result.exit_code == 0


def test_arguments_error(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg_int: int) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "asdasd"])

    assert result.exit_code == 1

def test_flags(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(flag_int: int = 3, flag_float: float = 0.3, flag_str: str = "world", flag_bool: bool = False) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "--flag_int=1", "--flag_float=0.5", "--flag_str=hello1", "--flag_bool=true"])

    assert result.exit_code == 0


def test_flags_error(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg_int: int = 3) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "--flag_int=asdasd"])

    assert result.exit_code == 1

def test_mixed(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg_int: int, flag_float: float = 0.3) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "1", "--flag_float=0.5"])

    assert result.exit_code == 0

def test_mixed_default(runner: "CliRunner") -> None:
    from clite import Clite

    app = Clite()

    @app.command()
    def todo_list(arg_int: int, flag_float: float = 0.3) -> None:
        pass

    result = runner.invoke(app, ["todo_list", "1"])

    assert result.exit_code == 0

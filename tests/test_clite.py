from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from clite.testing import CliRunner


def test_basic_functionality(runner: "CliRunner"):
    from clite import Clite, echo

    app = Clite("test_app", "test_descr")

    @app.command()
    def test_command():
        echo("test echo")

    result = runner.invoke(app, ["test_command"])

    assert result.output_text == "test echo"

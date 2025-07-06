import pytest

from clite.parser import parse_command_line


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["--option_str='hello world'"], {"option_str": "hello world"}),
        (['--option_str="hello world"'], {"option_str": "hello world"}),
        (["--option_str", "'hello world'"], {"option_str": "hello world"}),
        (["--option_str", '"hello world"'], {"option_str": "hello world"}),
        (["--option_str", "hello", "world"], {"option_str": "hello"}),
    ],
)
def test_parse_options(argv: list[str], expected: dict[str, str]) -> None:
    args, options = parse_command_line(argv)

    assert options == expected

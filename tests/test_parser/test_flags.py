import pytest

from clite.parser import parse_command_line


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["--flag_str", "'hello world'"], {"flag_str": "hello world"}),
        # ("--flag_str", '"hello world"'),
        # ("--flag_str=hello world"),
        # ("--flag_str='hello world'"),
        # ('--flag_str="hello world"'),
        # ("--flag_str", "hello", "world"),
    ],
)
def test_parse_flags(argv: list[str], expected: dict[str, str]) -> None:
    args, flags = parse_command_line(argv)

    assert args == ()
    assert flags == expected

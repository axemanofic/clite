import pytest

from clite.parser import parse_command_line


@pytest.mark.parametrize(
    "argv",
    [
        ("hello", "world"),
        ("hello", "world", "foo", "bar"),
    ],
)
def test_parse_args(argv) -> None:
    args, flags = parse_command_line(argv)

    assert args == argv
    assert flags == {}

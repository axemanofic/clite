import pytest

from clite.parser import parse_command_line


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["hello", "world"], ("hello", "world")),
        (["hello", "world", "foo", "bar"], ("hello", "world", "foo", "bar")),
    ],
)
def test_parse_args(argv: list[str], expected: tuple[str]) -> None:
    args, flags = parse_command_line(argv)

    assert args == expected

import pytest

from clite.parser.arguments import parse_argv


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["hello", "world"], ("hello", "world")),
        (["hello", "world", "foo", "bar"], ("hello", "world", "foo", "bar")),
    ],
)
def test_parse_args(argv: list[str], expected: tuple[str]) -> None:
    arguments = parse_argv(argv)

    result_args = []
    for arg in arguments:
        if arg.is_optional:
            continue
        result_args.append(arg.value)

    assert tuple(result_args) == expected

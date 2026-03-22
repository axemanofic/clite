import pytest

from clite.parser.arguments import parse_argv


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
    arguments = parse_argv(argv)

    for arg in arguments:
        if not arg.is_optional:
            continue
        assert arg.value == expected.get(arg.name)

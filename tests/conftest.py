import pytest

from clite.testing import CliRunner


@pytest.fixture(scope="function")
def runner() -> CliRunner:
    return CliRunner()

import pytest

from clite.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    """CliRunner fixture for tests."""
    return CliRunner()

from typing import TYPE_CHECKING

import nox

if TYPE_CHECKING:
    from nox.sessions import Session

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session: "Session") -> None:
    """Run all tests."""
    session.install("pytest")
    session.run("pytest", "-v", "tests")


@nox.session
def lint(session: "Session") -> None:
    """Run all linters."""
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", ".")

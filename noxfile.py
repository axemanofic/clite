from typing import TYPE_CHECKING

import nox

if TYPE_CHECKING:
    from nox.sessions import Session


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def tests(session: "Session") -> None:
    session.install("pytest")
    session.run("pytest", "-v", "tests")


@nox.session
def lint(session: "Session") -> None:
    session.install("ruff")
    session.run("ruff", "check", "clite")

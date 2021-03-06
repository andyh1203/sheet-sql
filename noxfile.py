"""Nox sessions."""

import os
import tempfile
from typing import Any

import nox
from nox.sessions import Session

PYTHON = ["3.7", "3.8"]
locations = "src", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "lint", "safety", "mypy", "pytype", "tests"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """
    Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
        kwargs: Additional keyword arguments for Session.install.
    """
    req_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    session.run(
        "poetry",
        "export",
        "--dev",
        "--format=requirements.txt",
        f"--output={req_path}",
        external=True,
    )
    session.install(f"--constraint={req_path}", *args, **kwargs)
    os.unlink(req_path)


@nox.session(python=PYTHON)
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov", "mock")
    session.run("pytest", *args)


@nox.session(python=PYTHON)
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-black",
        "flake8-bugbear",
        "flake8-bandit",
        "flake8-docstrings",
        # "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=PYTHON)
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=PYTHON)
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        requirements_filepath = requirements.name
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements_filepath}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run(
            "safety", "check", f"--file={requirements_filepath}", "--full-report"
        )


@nox.session(python=PYTHON)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python="3.7")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.7")
def docs(session: Session) -> None:
    """Build the documentation."""
    install_with_constraints(session, "sphinx")
    session.run("sphinx-build", "docs", "docs/_build")

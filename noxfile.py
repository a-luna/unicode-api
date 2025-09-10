import nox


@nox.session(python=["3.12"], reuse_venv=False, venv_backend="venv")
def test(session):
    """Run the test suite."""
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")
    session.install("pytest")
    session.install(".")
    session.run("pytest")

import nox


def install_flit_dev_deps(session):
    session.install("flit")
    session.run("flit", "install", "--deps", "develop")


@nox.session(python=["3.8"])
def tests(session):
    install_flit_dev_deps(session)
    session.run("pytest", "--cov=reducto", "--cov-report=xml", "tests")


@nox.session
def lint(session):
    install_flit_dev_deps(session)
    session.run("black", "--check", "reducto")
    session.run("mypy", "reducto")
    session.run("make", "documentation")

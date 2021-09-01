import nox


def install_flit_dev_deps(session):
    session.install("flit")
    session.run("flit", "install", "--deps", "all")


@nox.session(python=["3.8"])
def tests(session):
    install_flit_dev_deps(session)
    session.run("pytest", "--cov=reducto", "--cov-report=xml", "tests")


@nox.session
def lint(session):
    install_flit_dev_deps(session)
    session.run("black", "--check", "reducto")
    # session.run("mypy", "--ignore-missing-imports", "--strict", "reducto")
    # session.run('cd ${PWD}/docs && make html')
    # session.run(
    #     "sphinx-build",
    #     "-nW",
    #     "-q",
    #     "-b",
    #     "html",
    #     "-b",
    #     "linkcheck",
    #     "-d",
    #     "docs/_build/doctrees",
    #     "docs",
    #     "docs/_build/html",
    # )

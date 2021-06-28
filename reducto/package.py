"""
Code controlling python package traversal.
"""

from pathlib import Path

import reducto.src as src


class Package:
    """Class controlling a package.

    Entry point for reducto.
    Controls what a python package is and generates the associated source
    files to be then parsed.
    The general content of a package is grabbed from here.

    Attributes
    ----------
    source_files
    lines
    functions
    source_lines
    docstrings
    comments
    blank_lines
    average_function_length

    Methods
    -------

    """
    def __init__(self, path: Path) -> None:
        """
        Parameters
        ----------
        path : Path
            Full path pointing to the package.
        """
        self._path: Path = path

    def __repr__(self) -> str:
        return type(self).__name__ + f'({self.name})'

    @property
    def path(self) -> Path:
        """Returns the full path pointing to the package. """
        return self._path

    @property
    def name(self) -> str:
        """Name of the package.

        Returns
        -------
        name : str
        """
        return self.path.name

    def _walk(self) -> None:
        """Traverses the package structure.

        Walks listing the files on the main dir, and if any subpackage
        is found on the process this is walked recursively, generating
        a subpackage.

        Inspired by trailrunner.Trailrunner.walk.
        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Returns the total number of source files contained.

        Accounts for *.py files under the root self.path.

        Returns
        -------
        length : int
        """
        raise NotImplementedError

    @property
    def source_file(self) -> int:
        raise NotImplementedError

    @property
    def blank_lines(self) -> int:
        raise NotImplementedError

    @property
    def comment_lines(self) -> int:
        raise NotImplementedError

    @property
    def docstrings(self) -> int:
        raise NotImplementedError

    @property
    def source_lines(self) -> int:
        raise NotImplementedError

    @property
    def functions(self) -> int:
        raise NotImplementedError

    @property
    def average_function_length(self) -> int:
        raise NotImplementedError


def is_package(path: Path) -> bool:
    """Checks whether a given folder is a python package or not.

    ├─ packagename
    │  ├─ __init__.py
    │  └─ ...

    Parameters
    ----------
    path

    Returns
    -------

    """
    raise NotImplementedError


def is_src_package(path: Path) -> bool:
    """Checks whether a package is of the form:

    ├─ src
    │  └─ packagename
    │     ├─ __init__.py
    │     └─ ...
    ├─ tests
    │  └─ ...
    └─ setup.py

    Parameters
    ----------
    path

    Returns
    -------

    """
    raise NotImplementedError

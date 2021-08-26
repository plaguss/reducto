"""Module containing code to control python package crawling. """

import statistics
from typing import Iterator, Optional, List
from pathlib import Path

import reducto.src as src
import reducto.items as it
import reducto.reports as rp


class PackageError(Exception):
    """Error raised when a directory is not a valid python package."""

    pass


# File that makes a directory a python package.
PKG_FILE: str = "__init__.py"


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
        self.validate(path)
        self._path: Path = path
        self._source_files: Optional[List[src.SourceFile]] = None
        self._blank_lines: Optional[List[int]] = None
        self._comment_lines: Optional[List[int]] = None
        self._docstrings: Optional[List[int]] = None
        self._functions: Optional[List[List[it.FunctionDef]]] = None
        self._average_function_length: Optional[List[int]] = None

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.name})"

    def __len__(self) -> int:
        """Returns the total number of lines of the package.

        Returns
        -------
        lines : int
        """
        return sum(self.lines)

    @staticmethod
    def validate(path: Path) -> None:
        """Check if the input path is a proper python package.

        If the directory is either a package or an src package, returns
        None, otherwise raises PackageError.

        Parameters
        ----------
        path : Path

        Raises
        ------
        PackageError
            When the directory is not a valid python package.
        """
        if is_package(path):
            return
        elif is_src_package(path):
            return
        else:
            raise PackageError(f'{path} is not a valid python package.')

    @property
    def path(self) -> Path:
        """Returns the full path pointing to the package."""
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

        def walk(path: Path) -> Iterator[Optional[src.SourceFile]]:
            for child in path.iterdir():

                try:
                    yield src.SourceFile(child)
                except src.SourceFileError:
                    pass

                # Maybe regenerate a package to crawl itself
                # if self.validate(child):
                #     yield Package(child)

                if child.is_dir():
                    yield from walk(child)

        self._source_files = list(walk(self.path))

    @property
    def source_files(self) -> List[src.SourceFile]:
        # FIXME: Check when no files are found
        if self._source_files is None:
            self._walk()
        return self._source_files

    @property
    def lines(self) -> List[int]:
        return [len(file) for file in self.source_files]

    @property
    def blank_lines(self) -> List[int]:
        if self._blank_lines is None:
            self._walk()
        return [file.blank_lines for file in self.source_files]

    @property
    def docstrings(self) -> List[int]:
        if self._docstrings is None:
            self._walk()
        return [file.total_docstrings for file in self.source_files]

    @property
    def comment_lines(self) -> List[int]:
        if self._comment_lines is None:
            self._walk()
        return [file.comment_lines for file in self.source_files]

    @property
    def source_lines(self) -> List[int]:
        return [
            sum([func.source_lines for func in file.functions])
            for file in self.source_files
        ]

    @property
    def functions(self) -> List[List[it.FunctionDef]]:
        # FIXME: For the moment returns a list of list of functions
        if self._functions is None:
            self._functions = [file.functions for file in self.source_files]
        return self._functions

    @property
    def number_of_functions(self) -> List[int]:
        return [len(func_list) for func_list in self.functions]

    @property
    def average_function_length(self) -> int:
        source_lines: List[float] = []
        for function_list in self.functions:
            for function in function_list:
                source_lines.append(function.source_lines)

        average: int = (
            round(statistics.mean(source_lines)) if len(source_lines) > 0 else 0
        )

        return average

    @property
    def average_function_lengths(self) -> List[int]:
        averages: List[int] = []
        for function_list in self.functions:
            if len(function_list) == 0:
                avg_func_length = 0
            else:
                avg_func_length: int = round(
                    statistics.mean([f.source_lines for f in function_list])
                )
            averages.append(avg_func_length)

        return averages

    def report(self) -> rp.PackageReport:
        """Obtain the reporter class.

        Returns
        -------
        reporter : rp.PackageReport.
            Reporter object to obtain a proper data structure
            to present the results.

        See Also
        --------
        rp.PackageReport
        """
        report: rp.PackageReport = rp.PackageReport(self)
        return report


def is_package(path: Path) -> bool:
    """Checks whether a given folder is a python package or not.

    ├─ packagename
    │  ├─ __init__.py
    │  └─ ...

    Parameters
    ----------
    path : Path

    Returns
    -------
    check : bool
        Returns True if a path is a directory and contains an __init__.py file
        inside, False otherwise.
    """
    is_init: bool = False
    if path.is_dir():
        is_init = any(f.name == PKG_FILE for f in path.iterdir())
    return is_init


def is_src_package(path: Path) -> bool:
    """Checks whether a package is of the form:

    ├─ src
    │  └─ packagename
    │     ├─ __init__.py
    │     └─ ...
    ├─ tests
    │  └─ ...
    └─ setup.py

    The check for the path will be if its a directory with only one subdirectory
    containing an __init__.py file.

    Parameters
    ----------
    path : Path
        Full path pointing to a dir.

    Returns
    -------
    check : bool
        If the package is an src package, returns True, False otherwise.

    See Also
    --------
    is_package
    """
    check: bool = False
    if path.is_dir():
        maybe_subdirs = list(path.iterdir())
        if len(maybe_subdirs) == 1:
            check = is_package(path / maybe_subdirs[0])
    return check

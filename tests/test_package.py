"""
Contains tests related to reducto/package.py
"""

from typing import List
import pytest
import pathlib
import tempfile

import reducto.package as pkg
import reducto.src as src


def listdir_recursive(folder: pathlib.Path) -> List[pathlib.Path]:
    """

    Parameters
    ----------
    folder

    Returns
    -------

    Examples
    --------
    To see all the contents of a directory
    >>> [print(thing) for thing in listdir_recursive(sample_package)]
    """
    for f in folder.iterdir():
        if f.is_dir():
            yield from listdir_recursive(f)
        yield f


def test_tmp(sample_package):
    # Used only to check some fixtures for the tests
    print('sp ', sample_package)
    print([i for i in listdir_recursive(sample_package)])
    assert sample_package.is_file()


class TestPackage:
    @pytest.fixture(scope='class')
    def package(self, sample_package):
        return pkg.Package(sample_package)

    def test_name(self, package, sample_package):
        assert package.name == sample_package.name

    def test_repr(self, package, sample_package):
        assert repr(package) == f'Package({sample_package.name})'

    def test_package_len(self, package):
        assert len(package) == 6

    def test_source_files(self, package):
        assert isinstance(package.source_files, list)
        assert all(isinstance(f, src.SourceFile) for f in package.source_files)

    def test_package_lines(self, package):
        assert package.lines == 30  # Sum of docstring lines from every SourceFile

    def test_package_docstrings(self, package):
        assert package.docstrings == 30  # Sum of docstring lines from every SourceFile

    def test_package_comments(self, package):
        assert package.comments == 30  # Sum of docstring lines from every SourceFile

    def test_package_blank_lines(self, package):
        assert package.blank_lines == 30  # Sum of docstring lines from every SourceFile

    def test_package_source_lines(self, package):
        assert package.source_lines == 30  # Sum of docstring lines from every SourceFile

    def test_package_number_of_functions(self, package):
        assert package.number_of_functions == 30

    def test_package_average_function_length(self, package):
        assert package.average_function_length == 30

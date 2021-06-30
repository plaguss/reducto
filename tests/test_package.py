"""
Contains tests related to reducto/package.py
"""

from typing import List
import pytest
import pathlib

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


def test_is_package(sample_package):
    assert pkg.is_package(sample_package)


def test_is_src_package(src_sample_package):
    assert pkg.is_src_package(src_sample_package)


class TestPackage:
    @pytest.fixture
    def package(self, sample_package):
        return pkg.Package(sample_package)

    def test_package_validate(self, sample_package):
        with pytest.raises(pkg.PackageError):
            pkg.Package(sample_package / 'data')
        pkg.Package(sample_package)
        pkg.Package(sample_package / 'src')

    def test_name(self, package, sample_package):
        assert package.name == sample_package.name

    def test_repr(self, package, sample_package):
        assert repr(package) == f'Package({sample_package.name})'

    def test_package_len(self, package):

        assert len(package) == 528

    def test_source_files(self, package):
        assert isinstance(package.source_files, list)
        assert all(isinstance(f, src.SourceFile) for f in package.source_files)
        assert len(package.source_files) == 6

    def test_package_lines(self, package):
        assert isinstance(package.lines, list)
        assert all(a == b for a, b in zip(package.lines, [0, 128, 1, 128, 128, 128]))

    def test_package_docstrings(self, package):
        assert package.docstrings == 30  # Sum of docstring lines from every SourceFile

    def test_package_comments(self, package):
        assert isinstance(package.blank_lines, list)
        assert all(a == b for a, b in zip(package.comment_lines, [0, 3, 0, 3, 3, 3]))

    def test_package_blank_lines(self, package):
        assert isinstance(package.blank_lines, list)
        assert all(a == b for a, b in zip(package.blank_lines, [0, 32, 1, 32, 32, 32]))

    def test_package_source_lines(self, package):
        assert package.source_lines == 30  # Sum of docstring lines from every SourceFile

    def test_package_number_of_functions(self, package):
        assert package.functions == 30

    def test_package_average_function_length(self, package):
        assert package.average_function_length == 30

    def test_package_walk(self, package):
        walked = package._walk()
        print(list(walked))
        print([str(f) for f in package._walk()])
        assert 1 == 0

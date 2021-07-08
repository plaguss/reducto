"""
Contains tests related to reducto/package.py
"""

from typing import List
import pytest
import pathlib

import reducto.package as pkg
import reducto.src as src
import reducto.items as it
import reducto.reports as rp


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
        assert len(package) == 514

    def test_source_files(self, package):
        assert isinstance(package.source_files, list)
        assert all(isinstance(f, src.SourceFile) for f in package.source_files)
        assert len(package.source_files) == 7

    def test_package_lines(self, package):
        assert isinstance(package.lines, list)
        print(sorted(package.lines))
        assert all(a == b for a, b in zip(sorted(package.lines), [0, 1, 1, 128, 128, 128, 128]))

    def test_package_docstrings(self, package):
        assert isinstance(package.docstrings, list)
        assert all(a == b for a, b in zip(sorted(package.docstrings), [0, 0, 0, 29, 29, 29, 29]))

    def test_package_comments(self, package):
        assert isinstance(package.blank_lines, list)
        assert all(a == b for a, b in zip(sorted(package.comment_lines), [0, 0, 0, 3, 3, 3, 3]))

    def test_package_blank_lines(self, package):
        assert isinstance(package.blank_lines, list)
        assert all(a == b for a, b in zip(sorted(package.blank_lines), [0, 1, 1, 32, 32, 32, 32]))

    def test_package_source_lines(self, package):
        assert isinstance(package.source_lines, list)
        assert all(a == b for a, b in zip(sorted(package.source_lines), [0, 0, 0, 36, 36, 36, 36]))

    def test_package_functions(self, package):
        assert isinstance(package.functions, list)
        assert all([isinstance(f, it.FunctionDef) or f is None for func_list in package.functions for f in func_list])
        assert sorted(package.number_of_functions) == [0, 0, 0, 11, 11, 11, 11]

    def test_package_number_of_functions(self, package):
        assert isinstance(package.number_of_functions, list)
        assert sorted(package.number_of_functions) == [0, 0, 0, 11, 11, 11, 11]

    def test_package_average_function_length(self, package):
        assert package.average_function_length == 3

    def test_package_average_function_lengths(self, package):
        assert sorted(package.average_function_lengths) == [0, 0, 0, 3, 3, 3, 3]

    def test_package_report(self, package):
        report = package.report()
        assert isinstance(report, rp.PackageReport)

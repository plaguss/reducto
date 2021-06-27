"""
Contains tests related to reducto/package.py
"""

import pytest
import pathlib

import reducto.package as pkg
from .conftest import get_sample_file


def test_this():
    file = pathlib.Path(get_sample_file('example.py'))
    assert file.is_file()


# TODO:
#   Create a package in tempdir
#   copy example.py in different dirs (use shutil)

class TestPackage:
    @pytest.fixture(scope='class')
    def package(self):
        return pkg.Package('INSERT DIR NAME')

    def test_name(self):
        assert 1 == 0

    def test_repr(self):
        assert 1 == 0

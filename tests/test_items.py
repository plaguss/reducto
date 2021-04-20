"""Contains the tests for reducto.items. """

import pytest

import reducto.items as it


class TestItem:

    @pytest.fixture(scope='class')
    def function_def(self) -> it.FunctionDef:
        return it.FunctionDef('name', start=4, end=14)

    def test_instance(self, function_def):
        assert isinstance(function_def, it.FunctionDef)

    def test_repr(self, function_def):
        assert repr(function_def) == 1

    def test_name(self, function_def):
        assert function_def.name == 4

    def test_start(self, function_def):
        assert function_def.start == 4

    def test_end(self, function_def):
        assert function_def.end == 4

    def test_len(self, function_def):
        assert function_def.start == 4


class TestMethodDef:
    pass

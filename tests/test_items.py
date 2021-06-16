"""Contains the tests for reducto.items. """

import pytest
import bisect
import reducto.items as it


class TestItem:

    @pytest.fixture(scope='class')
    def item(self) -> it.Item:
        return it.Item('name', start=4, end=14)

    def test_instance(self, item):
        assert isinstance(item, it.Item)

    def test_repr(self, item):
        assert repr(item) == 'Item(name[4, 14])'

    def test_name(self, item):
        assert item.name == 'name'

    def test_start(self, item):
        assert item.start == 4

    def test_end(self, item):
        assert item.end == 14

    def test_len(self, item):
        assert len(item) == 10

    def test_lower_than(self, item):
        assert (item < it.Item('name2', start=5, end=7)) is True
        assert (item < it.Item('name2', start=4, end=7)) is False
        assert (item < it.Item('name2', start=3, end=7)) is False
        with pytest.raises(TypeError):
            item < "function"

    def test_docstring(self, item):
        assert item.docstrings == 0
        item.docstrings += 2
        assert item.docstrings == 2
        assert item.source_lines == 8
        item.docstrings = 0

    def test_comments(self, item):
        assert item.comments == 0
        item.comments += 2
        assert item.comments == 2
        assert item.source_lines == 8
        item.comments = 0

    def test_blank(self, item):
        assert item.blank == 0
        item.blank += 2
        assert item.blank == 2
        assert item.source_lines == 8
        item.blank = 0

    def test_source_lines(self, item):
        assert item.source_lines == 10
        item.docstrings += 1
        item.comments += 1
        item.blank += 1
        assert item.source_lines == 7


class TestFuncionDef:
    @pytest.fixture(scope='class')
    def function_def(self) -> it.Item:
        return it.FunctionDef('name', start=4, end=14)

    def test_repr(self, function_def):
        assert repr(function_def) == 'FunctionDef(name[4, 14])'


class TestMethodDef:
    @pytest.fixture(scope='class')
    def method_def(self) -> it.Item:
        return it.MethodDef('name', start=4, end=14)

    def test_name(self, method_def):
        assert method_def.name == 'name'


def test_sorting_list_of_function_defs():
    """Check a list of FunctionDef and MethodDef mixed can be sorted.
    checks for different positions and objects can be found using bisect_left.
    """
    func1 = it.FunctionDef('func1', start=0, end=5)
    func2 = it.MethodDef('func2', start=6, end=10)
    func3 = it.FunctionDef('func3', start=11, end=11)
    list_sorted = [func1, func2, func3]
    assert list_sorted == sorted([func2, func3, func1])

    assert bisect.bisect_left(list_sorted, it.FunctionDef('func', start=3, end=9)) == 1
    assert bisect.bisect_left(list_sorted, 0) == 0
    assert bisect.bisect_left(list_sorted, 1) == 1
    assert bisect.bisect_left(list_sorted, 3) == 1
    assert bisect.bisect_left(list_sorted, 5) == 1
    assert bisect.bisect_left(list_sorted, 6) == 1
    assert bisect.bisect_left(list_sorted, 7) == 2
    assert bisect.bisect_left(list_sorted, 10) == 2
    assert bisect.bisect_left(list_sorted, 11) == 2

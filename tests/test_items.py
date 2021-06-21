"""Contains the tests for reducto.items. """
import ast

import pytest
import bisect
import reducto.items as it


def sample_node():
    # Helper function to add a sample node to an item.
    txt = """def foo(x, y=2): return x+y """
    tree = ast.parse(txt, mode='exec')
    return tree.body[0]


class TestItem:

    @pytest.fixture(scope='class')
    def item(self) -> it.Item:
        item = it.Item('name', start=4, end=14)
        return item

    def test_instance(self, item):
        assert isinstance(item, it.Item)

    def test_repr(self, item):
        assert repr(item) == 'Item(name[4, 14])'

    def test_node(self, item):
        assert item.node is None
        item.node = sample_node()
        assert isinstance(item.node, ast.AST)

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

    def test_greater_equal(self, item):
        assert (item >= it.Item('name2', start=1, end=2)) is True
        assert (item >= it.Item('name2', start=4, end=7)) is True
        assert (item >= it.Item('name2', start=14, end=15)) is False
        with pytest.raises(TypeError):
            item >= "function"

    def test_contains(self, item):
        assert 6 in item
        assert 89 not in item

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
        assert item.blank_lines == 0
        item.blank_lines += 2
        assert item.blank_lines == 2
        assert item.source_lines == 8
        item.blank_lines = 0

    def test_source_lines(self, item):
        assert item.source_lines == 10
        item.docstrings += 1
        item.comments += 1
        item.blank_lines += 1
        assert item.source_lines == 7


class TestFuncionDef:
    @pytest.fixture(scope='class')
    def function_def(self) -> it.FunctionDef:
        return it.FunctionDef('name', start=4, end=14)

    def test_repr(self, function_def):
        assert repr(function_def) == 'FunctionDef(name[4, 14])'

    def test_get_docstring(self, function_def):
        function_def.node = sample_node()
        assert function_def.get_docstrings() == 0


class TestMethodDef:
    @pytest.fixture(scope='class')
    def method_def(self) -> it.MethodDef:
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


def test_get_docstring_lines():

    func_0 = r"""
def foo(x, y=2):
    return x+y 
    """

    func_1 = r'''
def foo(x, y=2):
    """docs """
    return x+y 
    '''

    func_2 = r'''
def foo(x, y=2):
    """docs
    """
    return x+y 
    '''

    func_3 = r'''
def foo(x, y=2):
    """

    docs"""
    return x+y 
    '''

    func_4 = r'''
def foo(x, y=2):
    """
    docs
    """
    return x+y 
    '''

    func_5 = r'''
def foo(x, y=2):
    """

    three lines 2"""
    return x+y 
    '''

    func_6 = r'''
def foo(x, y=2):
    """docs


    """
    return x+y 
    '''

    numpy_docstring_function = r'''
def fun(x):
    """sample doc

    Parameters
    ----------
    x : int

    Returns
    -------
    x : int
    """
    return x
    '''

    def function_ast(txt):
        tree = ast.parse(txt, mode='exec')
        return tree.body[0]

    assert it.get_docstring_lines(function_ast(func_0)) == 0
    assert it.get_docstring_lines(function_ast(func_1)) == 1
    assert it.get_docstring_lines(function_ast(func_2)) == 2
    assert it.get_docstring_lines(function_ast(func_3)) == 1
    assert it.get_docstring_lines(function_ast(func_4)) == 1
    assert it.get_docstring_lines(function_ast(func_5)) == 1
    assert it.get_docstring_lines(function_ast(func_6)) == 4
    assert it.get_docstring_lines(function_ast(numpy_docstring_function)) == 9
"""Tests defined for reducto.parser.
"""

import os
import pytest
import ast

import reducto.api as rd


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


def test_load_source_file():
    tree = rd.source_to_ast(get_sample_file('example.py'))
    assert isinstance(tree, ast.Module)


class TestSourceVisitor:
    @pytest.fixture(scope='class')
    def visitor(self):
        visitor = rd.SourceVisitor()
        visitor.visit(rd.source_to_ast(get_sample_file('example.py')))
        return visitor

    # def test_visitor_instance(self):

    def test_len_items(self, visitor):
        print(visitor.items)
        assert len(visitor.items) == 11

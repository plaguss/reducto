"""Tests defined for reducto.parser.
"""

import os
import pathlib

import pytest
import ast
import tokenize

import reducto.src as rd


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


def ast_parsed() -> ast.Module:
    # Simplify parsing the file as there is no
    # external function for it.
    path = pathlib.Path(get_sample_file('example.py'))
    src = rd.SourceFile(path)
    return src.ast


class TestSourceVisitor:
    @pytest.fixture(scope='class')
    def visitor(self):
        visitor = rd.SourceVisitor()
        visitor.visit(ast_parsed())
        return visitor

    # def test_visitor_instance(self):

    def test_len_items(self, visitor):
        print(visitor.items)
        assert len(visitor.items) == 11


class TestSourceFile:
    @pytest.fixture(scope='class')
    def src(self):
        return rd.SourceFile(get_sample_file('example.py'))

    def test_src_instance(self, src):
        assert isinstance(src, rd.SourceFile)

    def test_src_instance_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            rd.SourceFile('wrong_file.py')

    def test_src_repr(self, src):
        assert f"SourceFile(example.py)" == repr(src)

    def test_lines_are_read(self, src):
        assert isinstance(src.lines, list)
        assert isinstance(src.lines[0], str)

    def test_ast(self, src):
        assert isinstance(src.ast, ast.Module)

    def test_tokens(self, src):
        tokens = src.tokens
        assert isinstance(tokens, list)
        assert isinstance(tokens[0], tokenize.TokenInfo)

    def test_len(self, src):
        assert len(src) == 128

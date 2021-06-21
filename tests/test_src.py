"""Tests defined for reducto.parser.
"""

import os
import pathlib

import pytest
import ast
import tokenize

import reducto.src as src
import reducto.items as it


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


def ast_parsed() -> ast.Module:
    # Simplify parsing the file as there is no
    # external function for it.
    path = pathlib.Path(get_sample_file('example.py'))
    source = src.SourceFile(path)
    return source.ast


def test_constants():
    assert src.NL_CHAR == '\n'
    assert src.COMMENT_CHAR == '#'


class TestSourceVisitor:

    # TODO
    #   Insert test for source file without content.

    @pytest.fixture(scope='class')
    def visitor(self):
        visitor = src.SourceVisitor()
        visitor.visit(ast_parsed())
        return visitor

    def test_len_items(self, visitor):
        print(visitor.items)
        assert len(visitor.items) == 11

    def test_visit_FunctionDef(self, visitor):
        ast_tree = ast_parsed()
        # an ast.FunctionDef is passed from the example file.
        node = visitor.visit_FunctionDef(ast_tree.body[6])
        assert isinstance(node, ast.FunctionDef)

    def test_visit_ClassDef(self, visitor):
        ast_tree = ast_parsed()
        # an ast.FunctionDef is passed from the example file.
        node = visitor.visit_ClassDef(ast_tree.body[9])
        assert isinstance(node, ast.ClassDef)

    def test_items(self, visitor):
        assert all((isinstance(item, it.Item) for item in visitor.items))

    def test_functions(self, visitor):
        assert all((isinstance(item, it.FunctionDef) for item in visitor.functions))

    def test_register_elements(self, visitor):
        content = {'comments': [1, 4, 5, 6, 22], 'blank_lines': [12, 46]}

        visitor._register_elements(content['comments'], 'comments')
        assert visitor.functions[0].docstrings == 1

    def test_register_functions(self, visitor):
        content = {'comments': [1, 4, 5, 6, 22], 'blank_lines': [12, 46]}
        visitor.register_functions(content)
        assert visitor.functions[0].docstrings == 1


def test_token_is_comment_line():
    comment_line = tokenize.TokenInfo(
        type=tokenize.COMMENT,
        string='# Use some imports.\n',
        start=(6, 0),
        end=(6, 19),
        line='# Use some imports.\n'
    )
    assert src.token_is_comment_line(comment_line)

    comment_line_on_variable = tokenize.TokenInfo(
        type=tokenize.COMMENT,
        string='# Attribute set outside init.',
        start=(44, 16),
        end=(44, 45),
        line='    attrib = 1  # Attribute set outside init.\n'
    )
    assert not src.token_is_comment_line(comment_line_on_variable)
    comment_line_on_variable = tokenize.TokenInfo(
        type=tokenize.NEWLINE,
        string='\n',
        start=(44, 16),
        end=(44, 45),
        line='    attrib = 1  # Attribute set outside init.\n'
    )
    assert not src.token_is_comment_line(comment_line_on_variable)


def test_token_is_blank_line():
    blank_line = tokenize.TokenInfo(
        type=tokenize.NL,
        string='\n',
        start=(43, 0),
        end=(43, 1),
        line='\n'
    )
    assert src.token_is_blank_line(blank_line)

    blank_line_and_space = tokenize.TokenInfo(
        type=tokenize.NL,
        string='  \n',
        start=(43, 0),
        end=(43, 1),
        line='  \n'
    )
    assert not src.token_is_blank_line(blank_line_and_space)

    comment_line_on_variable = tokenize.TokenInfo(
        type=tokenize.NEWLINE,
        string='\n',
        start=(44, 16),
        end=(44, 45),
        line='    attrib = 1  # Attribute set outside init.\n'
    )
    assert not src.token_is_blank_line(comment_line_on_variable)


class TestSourceFile:
    @pytest.fixture(scope='class')
    def src_(self):
        return src.SourceFile(get_sample_file('example.py'))

    def test_src_instance(self, src_):
        assert isinstance(src_, src.SourceFile)

    def test_src_instance_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            src.SourceFile('wrong_file.py')

    def test_src_repr(self, src_):
        assert f"SourceFile(example.py)" == repr(src_)

    def test_lines_are_read(self, src_):
        assert isinstance(src_.lines, list)
        assert isinstance(src_.lines[0], str)

    def test_ast(self, src_):
        assert isinstance(src_.ast, ast.Module)

    def test_tokens(self, src_):
        tokens = src_.tokens
        assert isinstance(tokens, list)
        assert isinstance(tokens[0], tokenize.TokenInfo)

    def test_len(self, src_):
        assert len(src_) == 128

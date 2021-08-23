"""Tests defined for reducto.parser.
"""

import os
import pathlib

import pytest
import ast
import tokenize

import reducto.src as src
import reducto.items as it
import reducto.reports as rp

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

    @pytest.fixture(scope='class')
    def visitor(self):
        visitor = src.SourceVisitor()
        visitor.visit(ast_parsed())
        return visitor

    def test_repr(self, visitor):
        assert repr(visitor) == 'SourceVisitor'

    def test_len_items(self, visitor):
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
        return src.SourceFile(pathlib.Path(get_sample_file('example.py')))

    def test_src_validate(self, sample_package):
        with pytest.raises(src.SourceFileError):
            src.SourceFile(sample_package / 'extension.cpp')
        print(list(sample_package.iterdir()))
        with pytest.raises(src.SourceFileError):
            src.SourceFile(sample_package / 'data')

        src.SourceFile(sample_package / '__init__.py')

    def test_src_instance(self, src_):
        assert isinstance(src_, src.SourceFile)

    def test_read_file_by_lines(self, src_):
        file = src_._read_file_by_lines()
        assert isinstance(file, list)
        assert all(isinstance(l, str) for l in file)

    def test_src_repr(self, src_):
        assert f"SourceFile(example.py)" == repr(src_)

    def test_str(self, src_):
        assert str(src_) == get_sample_file('example.py')

    def test_lines_are_read(self, src_):
        assert isinstance(src_.lines, list)
        assert isinstance(src_.lines[0], str)

    def test_len(self, src_):
        assert len(src_) == 128

    def test_ast(self, src_):
        assert isinstance(src_.ast, ast.Module)

    def test_tokens(self, src_):
        tokens = src_.tokens
        assert isinstance(tokens, list)
        assert isinstance(tokens[0], tokenize.TokenInfo)
        assert len(tokens) == 399

    def test_comment_lines(self, src_):
        assert src_.comment_lines == 3

    def test_comment_lines_positions(self, src_):
        assert isinstance(src_.comment_lines_positions, list)
        assert all(
            pos == corr for pos, corr in zip(
                src_.comment_lines_positions,
                [6, 20, 36]
            )
        )

    def test_blank_lines(self, src_):
        assert src_.blank_lines == 32

    def test_blank_lines_positions(self, src_):
        correct = [
            5, 12, 13, 17, 18, 21, 25, 26, 29, 32, 34, 35, 37, 38, 43, 45, 48,
            51, 55, 68, 70, 93, 95, 98, 105, 112, 114, 119, 120, 123, 124, 126
        ]

        assert isinstance(src_.blank_lines_positions, list)
        assert all(pos == corr for pos, corr in  zip(src_.blank_lines_positions, correct))

    def test_source_visitor(self, src_):
        assert isinstance(src_.source_visitor, src.SourceVisitor)

    def test_visit_source(self, src_):
        src_visitor = src_._visit_source()
        assert isinstance(src_visitor, src.SourceVisitor)
        # Check the functions are obtained.
        assert all(isinstance(f, it.FunctionDef) for f in src_visitor.functions)
        # Check the functions are registered.
        assert src_visitor.functions[0].docstrings == 1

    def test_functions(self, src_):
        funcs = src_.functions
        assert len(funcs) == 11
        assert all(isinstance(f, it.FunctionDef) for f in funcs)

    def test_module_docstrings(self, src_):
        assert src_.module_docstrings == 3

    def test_total_docstrings(self, src_):
        func_docs = sum([f.docstrings for f in src_.functions])
        assert src_.total_docstrings == src_.module_docstrings + func_docs
        assert src_.total_docstrings == 29

    def test_source_lines(self, src_):
        source_lines = len(src_) - src_.total_docstrings \
                       - src_.comment_lines - src_.blank_lines
        assert src_.source_lines == source_lines

    def test_report_dict(self, src_):
        report = src_.report()
        assert isinstance(report, rp.SourceReport)

    def test_src_no_functions(self, source_file_no_functions):
        # Test when a file contains no functions
        source_file = src.SourceFile(source_file_no_functions)
        assert len(source_file.functions) == 0
        report = source_file.report().report()
        print('rep-->', report['no_functions.py'])
        assert report['no_functions.py']['lines'] == 1
        assert report['no_functions.py']['number_of_functions'] == 0
        assert report['no_functions.py']['average_function_length'] == 0
        assert report['no_functions.py']['docstring_lines'] == 0
        assert report['no_functions.py']['blank_lines'] == 1

    def test_src_one_function(self, source_file_one_function):
        # Test when a file contains only one functions
        source_file = src.SourceFile(source_file_one_function)
        assert len(source_file.functions) == 1
        report = source_file.report().report()
        assert report['one_function.py']['lines'] == 3
        assert report['one_function.py']['number_of_functions'] == 1
        assert report['one_function.py']['average_function_length'] == 1
        assert report['one_function.py']['docstring_lines'] == 0
        assert report['one_function.py']['blank_lines'] == 1

"""Module containing the functionalities to parse a python source file.

Uses `ast` and `tokenize` builtin libraries.

References
----------
https://stackoverflow.com/questions/37514636/good-way-to-count-number-of-functions-of-a-python-file-given-path
https://greentreesnakes.readthedocs.io/en/latest/manipulating.html#inspecting-nodes
https://laptrinhx.com/julien-danjou-finding-definitions-from-a-source-file-and-a-line-number-in-python-468576127/
https://kamneemaran45.medium.com/python-ast-5789a1b60300
"""

import os
import ast
import tokenize


def source_to_ast(filename: str) -> ast.Module:
    """Opens and parses a source file by means of tokenize.open.

    Parameters
    ----------
    filename : str
        Name of the file to be parsed. Must be a source file with .py extension.

    Returns
    -------
    ast_module : ast.Module
        Source file parsed to an ast.

    Raises
    ------
    FileNotFoundError
        If the file is not found.
    """

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"No file found called: {filename}.")

    with tokenize.open(filename) as f:
        return ast.parse(f.read(), filename=filename)


class SourceVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        print('lines', (node.name, node.lineno, node.end_lineno))
        # self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef
    # def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
    #     print('lines', (node.name, node.lineno, node.end_lineno))
    #     # print(NotImplementedError)

    def visit_ClassDef(self, node: ast.ClassDef):
        print('lines', (node.name, node.lineno, node.end_lineno))
        print('Inside class ->')
        self.generic_visit(node)
        # print(NotImplementedError)


if __name__ == '__main__':
    EXAMPLE = r'C:\Users\agustin\git_repository\reducto\tests\data\example.py'
    tree = source_to_ast(EXAMPLE)

    sourcer = SourceVisitor()
    sourcer.visit(tree)

    funcs = [(i, f) for i, f in enumerate(tree.body) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    # get a function

"""Module containing the functionalities to parse a python source file.

Uses `ast` and `tokenize` builtin libraries.

References
----------
https://stackoverflow.com/questions/37514636/good-way-to-count-number-of-functions-of-a-python-file-given-path
https://greentreesnakes.readthedocs.io/en/latest/manipulating.html#inspecting-nodes
https://laptrinhx.com/julien-danjou-finding-definitions-from-a-source-file-and-a-line-number-in-python-468576127/
https://kamneemaran45.medium.com/python-ast-5789a1b60300
"""

import ast
import tokenize

SAY_HELLO = r'C:\Users\agustin\git_repository\reducto\tests\data\say_hello.py'

def parse_file(filename):
    with tokenize.open(filename) as f:
        return ast.parse(f.read(), filename=filename)

tree = parse_file(SAY_HELLO)


class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

FuncLister().visit(tree)


for node in ast.walk(tree):
    print(node)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(node.name)


class SourceVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        print(node)
        print(NotImplementedError)

    def visit_ClassDef(self, node):
        print(node)
        print(NotImplementedError)

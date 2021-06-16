"""Module containing the functionalities to parse a python source file.

Uses `ast` and `tokenize` builtin libraries.

References
----------
https://stackoverflow.com/questions/37514636/good-way-to-count-number-of-functions-of-a-python-file-given-path
https://greentreesnakes.readthedocs.io/en/latest/manipulating.html#inspecting-nodes
https://laptrinhx.com/julien-danjou-finding-definitions-from-a-source-file-and-a-line-number-in-python-468576127/
https://kamneemaran45.medium.com/python-ast-5789a1b60300
"""

from typing import Union, List, Optional, Tuple
import os
import ast
import tokenize
import pathlib

import reducto.items as it


TokenType = Tuple[int, str, Tuple[int, int], Tuple[int, int], str]

NL_CHAR: str = '\n'  # New line character


class SourceFile:
    """Class representing a .py source file.

    Allows to read a file, obtain the tokens and the ast.
    """
    def __init__(self, filename: str) -> None:
        """

        Parameters
        ----------
        filename : str
            Name of the file.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"No file found called: {filename}.")

        self._filename: pathlib.Path = pathlib.Path(filename)
        self._lines: Optional[List[str]] = None
        self._ast: Optional[ast.Module] = None
        self._tokens: Optional[List[tokenize.TokenInfo]] = None
        self._blank_lines: int = 0
        self._source_visitor: Optional[SourceVisitor] = None

    def __repr__(self):
        return type(self).__name__ + f"({self._filename.name})"

    def __len__(self) -> int:
        """Return the total number of lines in the file. """
        return len(self.lines)

    def _read_file_by_lines(self) -> List[str]:
        """Read a file using tokenize.open and return the lines.

        Returns
        -------
        lines : List[str]
            Returns the lines as a list of str.
        """
        with tokenize.open(str(self._filename)) as fd:
            return fd.readlines()

    @property
    def lines(self) -> List[str]:
        """Contains the lines of the file as initially parsed with tokenize module. """
        if self._lines is None:
            self._lines: List[str] = self._read_file_by_lines()
        return self._lines

    @property
    def ast(self) -> ast.Module:
        """Parses and returns the ast of a file from the lines read with tokenize module.

        Returns
        -------
        ast : ast.Module
            Abstract Syntax Tree module object.
        """
        if self._ast is None:
            self._ast = ast.parse("".join(self.lines))
        return self._ast

    @property
    def tokens(self) -> List[tokenize.TokenInfo]:
        """Return the complete set of tokens for a file. """
        if self._tokens is None:
            line_iter = iter(self.lines)
            self._tokens = list(tokenize.generate_tokens(lambda: next(line_iter)))

        return self._tokens

    @property
    def comment_lines(self) -> int:
        """

        Obtained with tokens

        Returns
        -------

        """
        pass

    def comment_lines_positioned(self):
        """
        TODO:
            Obtain the comments, as a list of tuples containing the
            line number and the actual content.
            Maybe differentiate if its a line with only comment?

        Returns
        -------

        """
#        for i, t in enumerate(tokens):
#            if token_is_comment(t):
#                print((i, t))
        pass

    @property
    def blank_lines(self):
        """
        Obtained with tokens.

        TODO:
            Hace falta tener el total de blank lines tanto en número de blank lines
            para el módulo, como la línea en la que está para restarlos de las funciones.

        Returns
        -------

        """
        return self._blank_lines

    def blank_lines_positioned(self):
        """
        TODO:
            Obtain the comments, as a list of tuples containing the
            line number and the actual content.
            Maybe differentiate if its a line with only comment?

        Returns
        -------

        """
        pass

    @property
    def source_visitor(self) -> "SourceVisitor":
        """Returns the SourceVisitor once visited.

        Instantiates and calls the visit method to the SourceVisitor.
        All the necessary info regarding the ast of the source file
        should be contained here.

        Returns
        -------
        source_visitor : SourceVisitor
        """
        if self._source_visitor is None:
            self._source_visitor = self._visit_source()
        return self._source_visitor

    def _visit_source(self) -> "SourceVisitor":
        """
        TODO:
            Se encargará de llamar al SourceVisitor
            Tiene que almacenar los diferentes objetos visitados
            Dejar los diferentes métodos controlados para acceder a las funciones
            y trabajar con ellas de forma sencilla.
            Dejar todo ese contenido dentro de SourceVisitor

        Returns
        -------

        """
        tree: ast.Module = self.ast
        source_visitor = SourceVisitor()
        source_visitor.visit(tree)
        return source_visitor

    @property
    def module_docstrings(self) -> int:
        """Obtains the lines of docstrings at the module level.

        Returns
        -------
        docstrings : int
            Lines of docstrings in the module.
        """
        return it.get_docstring_lines(self.ast)


def token_is_comment(tok: tokenize.TokenInfo) -> bool:
    """Checks whether a given token is a comment.

    TODO: THIS MUST BE CHECKED FOR A LINE, NOT JUST A TOKEN.

    Parameters
    ----------
    tok

    Returns
    -------

    """
    return tok[0] == tokenize.COMMENT


def token_is_blank_line(tok: tokenize.TokenInfo) -> bool:
    r"""Checks if a given line is a blank line or not.

    The check is done for a NL token and a line containing only a
    new line character.

    Parameters
    ----------
    tok : tokenize.TokenInfo
        Token obtained from tokenize.generate_tokens.

    Returns
    -------
    check : bool
        If a token is a blank line returns True, False otherwise.

    Examples
    --------
    >>> tok = tokenize.TokenInfo(type=61, string='\n', start=(123, 0), end=(126, 1), line='\n')
    >>> token_is_blank_line(tok)
    True
    """
    return tok[0] == tokenize.NL and tok.line == NL_CHAR


class SourceVisitor(ast.NodeVisitor):
    """
    TODO:
        - Añadir la distinción entre método y función (método nuevo en lugar
        de generic_visit?)
        - Método len para contar casos
        - docstrings

    Notes
    -----
    For the moment, no distinction is done between functions and definitions,
    so between the items there will be only FunctionDef, no MethodDef items.
    """

    def __init__(self) -> None:
        self._items: List[it.Item] = []
        self._functions: List[it.FunctionDef] = []

    def __repr__(self):
        return type(self).__name__

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visits the FunctionDef nodes.

        Creates and stores the corresponding item, along with the
        name, start and end lines.

        Parameters
        ----------
        node : ast.FunctionDef
            Node automatically filtered when visit method is called.

        Returns
        -------
        node : ast.FunctionDef
            Returns the node itself.
        """
        print('lines', (node.name, node.lineno, node.end_lineno))
        func_def = it.FunctionDef(node.name, start=node.lineno, end=node.end_lineno)
        func_def.node = node  # TODO: This has to be tested! https://stackoverflow.com/questions/48759838/how-to-create-a-function-object-from-an-ast-functiondef-node
        self._items.append(func_def)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        TODO: Review how to distinguish between functions and methods.
        """
        print('lines', (node.name, node.lineno, node.end_lineno))
        print('Inside class ->')
        self.generic_visit(node)
        return node

    @property
    def items(self) -> List[it.Item]:
        """

        May be without any content for some .py files.

        Returns
        -------
        items : List[it.Item]
            Returns all the items found in the ast source.
        """
        return self._items

    @property
    def functions(self) -> List[it.FunctionDef]:
        """Returns the items which are functions from the list of items obtained. """
        if len(self._functions) == 0:
            self._functions = [item for item in self.items if isinstance(item, it.FunctionDef)]
            [func.get_docstrings() for func in self._functions]
        return self._functions

    def private_functions(self) -> List[it.FunctionDef]:
        raise NotImplementedError

    def dunder_methods(self) -> List[it.FunctionDef]:
        raise NotImplementedError


if __name__ == '__main__':
    EXAMPLE = os.path.join(os.getcwd(), 'tests', 'data', 'example.py')

    src = SourceFile(EXAMPLE)
    tree = src.ast
    tokens = src.tokens

    sourcer = SourceVisitor()
    sourcer.visit(tree)
    functions: List[it.FunctionDef] = sourcer.functions
    # Access to the items to see the content.

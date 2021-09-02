"""Module containing the functionalities to parse a python source file.

Uses `ast` and `tokenize` builtin libraries.

References
----------
- https://stackoverflow.com/questions/37514636/good-way-to-count-number-of-functions-of-a-python-file-given-path
- https://greentreesnakes.readthedocs.io/en/latest/manipulating.html#inspecting-nodes
- https://laptrinhx.com/julien-danjou-finding-definitions-from-a-source-file-and-a-line-number-in-python-468576127/
- https://kamneemaran45.medium.com/python-ast-5789a1b60300
"""

from typing import List, Optional, Dict
import ast
import tokenize
import pathlib
from bisect import bisect_left

import reducto.items as it
import reducto.reports as rp

NL_CHAR: str = "\n"  # New line character
COMMENT_CHAR: str = "#"  # Comment character


class SourceFileError(Exception):
    """Error raised when a path is not a valid python path."""

    pass


class SourceFile:
    """Class representing a .py source file.

    Allows to read a file, obtain the tokens and the ast.
    """

    def __init__(self, filename: pathlib.Path) -> None:
        """
        Parameters
        ----------
        filename : pathlib.Path
            Full name of the file.

        Raises
        ------
        FileNotFoundError
            If the file doesn't exists.
        """

        self.validate(filename)

        self._filename: pathlib.Path = filename
        self._lines: Optional[List[str]] = None
        self._ast: Optional[ast.Module] = None
        self._tokens: Optional[List[tokenize.TokenInfo]] = None
        self._blank_lines: int = 0
        self._blank_lines_positions: Optional[List[int]] = None
        self._comment_lines: int = 0
        self._comment_lines_positions: Optional[List[int]] = None
        self._source_visitor: Optional[SourceVisitor] = None

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self._filename.name})"

    def __str__(self) -> str:
        return str(self._filename)

    def __len__(self) -> int:
        """Return the total number of lines in the file."""
        return len(self.lines)

    @staticmethod
    def validate(path: pathlib.Path) -> None:
        """Check if the path is a valid python file.

        Called on instantiation. It must be a file with the extension .py.

        Parameters
        ----------
        path : Path
            Path to validate.

        Returns
        -------
        check : bool
            True if is a valid python file, false otherwise.

        Raises
        ------
        SourceFileError
            When the file is not a valid python file.
        """
        if path.is_file():
            if path.name.endswith(".py"):
                return
        raise SourceFileError(f"{path} is not a valid python file.")

    @property
    def name(self) -> str:
        """Returns the name of the file.

        Returns
        -------
        name : str
        """
        return self._filename.name

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
        """Contains the lines of the file as initially parsed with tokenize module."""
        if self._lines is None:
            self._lines = self._read_file_by_lines()
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
        """Return the complete set of tokens for a file.

        See Also
        --------
        tokenize.generate_tokens
        """
        if self._tokens is None:
            line_iter = iter(self.lines)
            self._tokens = list(tokenize.generate_tokens(lambda: next(line_iter)))

        return self._tokens

    @property
    def comment_lines(self) -> int:
        """Returns the total number of lines which are comments.

        Returns
        -------
        comments : int

        See Also
        --------
        token_is_comment_line
        """
        if self._comment_lines_positions is None:
            self._comment_blank_lines_positions()
        return self._comment_lines

    @property
    def comment_lines_positions(self) -> List[int]:
        """Returns the list of positions of the comment lines.

        This is used to register the functions.

        Returns
        -------
        comments_positions : List[int]
            List with the line position of each comment line.
        """
        if self._comment_lines_positions is None:
            self._comment_blank_lines_positions()
        return self._comment_lines_positions  # type: ignore[return-value]

    @property
    def blank_lines(self) -> int:
        """Returns the total number of lines which are blank lines.

        Returns
        -------
        blank_lines : int

        See Also
        --------
        token_is_blank_line
        """
        if self._blank_lines_positions is None:
            self._comment_blank_lines_positions()  # pragma: no cover, call to a tested method.
        return self._blank_lines

    @property
    def blank_lines_positions(self) -> List[int]:
        """Returns the list of positions of the blank lines.

        This is used to register the functions.

        Returns
        -------
        blank_lines_positions : List[int]
            List with the positions of the blank lines.
        """
        if self._blank_lines_positions is None:
            self._comment_blank_lines_positions()  # pragma: no cover, call to a tested method.
        return self._blank_lines_positions  # type: ignore[return-value]

    def _comment_blank_lines_positions(self) -> None:
        """Grabs the blank lines and comments.

        Traverses the tokens and checks whether any is a comment line
        or a blank line. If they are, the comment_lines and blank_lines
        are grown, and the corresponding positions are registered.

        See Also
        --------
        token_is_comment_line
        token_is_blank_line
        """
        self._comment_lines_positions = []
        self._blank_lines_positions = []
        for tok in self.tokens:
            if token_is_comment_line(tok):
                idx: int = tok.start[0]  # Get the line number.
                self._comment_lines_positions.append(idx)
                self._comment_lines += 1
            if token_is_blank_line(tok):
                idx = tok.start[0]  # Get the line number.
                self._blank_lines_positions.append(idx)
                self._blank_lines += 1

    @property
    def source_visitor(self) -> "SourceVisitor":
        """Returns the SourceVisitor once visited.

        Instantiates and calls the visit method of the SourceVisitor.
        All the necessary info regarding the ast of the source file
        should be contained here.

        Returns
        -------
        source_visitor : SourceVisitor

        See Also
        --------
        SourceVisitor
        """
        if self._source_visitor is None:
            self._source_visitor = self._visit_source()
        return self._source_visitor

    def _visit_source(self) -> "SourceVisitor":
        """Calls the SourceVisitor on the parsed ast.

        Registers the functions with the comments and blank lines obtained
        from the tokens.

        Returns
        -------
        source_visitor : SourceVisitor
        """
        tree: ast.Module = self.ast
        source_visitor = SourceVisitor()
        source_visitor.visit(tree)

        # Register comments and blank lines on the functions.
        content: Dict[str, List[int]] = {
            "comments": self.comment_lines_positions,
            "blank_lines": self.blank_lines_positions,
        }
        source_visitor.register_functions(content)

        return source_visitor

    @property
    def functions(self) -> List[it.FunctionDef]:
        """Returns the list of functions grabbed through the ast.

        Returns
        -------
        functions : List[it.FunctionDef]
            List of FunctionDef objects in the file.

        See Also
        --------
        reducto.items.FunctionDef
        """
        return self.source_visitor.functions

    @property
    def module_docstrings(self) -> int:
        """Obtains the lines of docstrings at the module level.

        Returns
        -------
        docstrings : int
            Lines of docstrings in the module.
        """
        return it.get_docstring_lines(self.ast)

    @property
    def total_docstrings(self) -> int:
        """Get the total number of docstring lines.

        The total number of docstrings are the module level docstrings
        plus the ones recorded from the functions.

        Returns
        -------
        total_docstrings : int
        """
        module_docs: int = self.module_docstrings
        funcs_docs: int = sum([f.docstrings for f in self.functions])
        return module_docs + funcs_docs

    @property
    def source_lines(self) -> int:
        """Computes the total number of source code lines of the file.

        Returns
        -------
        source_lines : int
            Source lines are computed as the total number of lines
            minus the docstrings, minus the comment lines and minus
            the blank lines.
        """
        return len(self) - self.total_docstrings - self.comment_lines - self.blank_lines

    def report(self) -> rp.SourceReport:
        """Obtain the reporter class.

        Returns
        -------
        reporter : rp.SourceReport.

        See Also
        --------
        reducto.reports.SourceReport
        """
        report: rp.SourceReport = rp.SourceReport(self)
        return report


def token_is_comment_line(tok: tokenize.TokenInfo) -> bool:
    """Checks whether a given token line is a comment.

    The check is done for the whole line, not just the token type.
    A line containing a comment after anything which isn't a space
    is not considered a comment line.

    Parameters
    ----------
    tok : tokenize.TokenInfo
        Token as extracted from tokenize.generate_tokens.

    Returns
    -------
    is_comment_line : bool
        Returns True when the line is a comment line only, False otherwise.
    """
    is_comment_line: bool = False

    if tok.type == tokenize.COMMENT:
        is_comment_line = tok.line.lstrip().startswith(COMMENT_CHAR)

    return is_comment_line


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
    return tok.type == tokenize.NL and tok.line == NL_CHAR


class SourceVisitor(ast.NodeVisitor):
    """Class inheriting from ast.NodeVisitor.

    Defines the actions to be taken on the ast being parsed.
    Obtains every FunctionDef in the source file, (included async ones)
    and when a class is found, the corresponding methods are parsed
    just like FunctionDef objects.
    No other object is obtained from the SourceVisitor.
    Instantiates the corresponding items and registers the content, like
    the number of lines and docstrings.

        TODO:
        - Añadir la distinción entre método y función (método nuevo en lugar
        de generic_visit?)

    Notes
    -----
    For the moment, no distinction is done between functions and definitions,
    so between the items there will be only FunctionDef, no MethodDef items.

    See Also
    --------
    ast.NodeVisitor
    """

    def __init__(self) -> None:
        self._items: List[it.Item] = []
        self._functions: List[it.FunctionDef] = []

    def __repr__(self) -> str:
        return type(self).__name__

    def visit_FunctionDef(self, node):
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

        See Also
        --------
        reducto.items.FunctionDef

        Notes
        -----
        Typing the argument raises mypy error.
        """
        func_def = it.FunctionDef(node.name, start=node.lineno, end=node.end_lineno)
        func_def.node = node
        self._items.append(func_def)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef):
        """Calls the general generic_visit method on itself, obtaining
        the FunctionDef objects found.
        """
        self.generic_visit(node)
        return node

    @property
    def items(self) -> List[it.Item]:
        """List of items parsed with the ast.parse.

        Returns
        -------
        items : List[it.Item]
            Returns all the items found in the ast source.

        See Also
        --------
        reducto.items.Item
        """
        return self._items

    @property
    def functions(self) -> List[it.FunctionDef]:
        """Returns the items which are functions from the list of items obtained.

        When the functions are retrieved, the docstrings are obtained registered.

        Returns
        -------
        functions : List[it.FunctionDef]
        """
        if len(self._functions) == 0:
            self._functions = [
                item for item in self.items if isinstance(item, it.FunctionDef)
            ]
            [func.get_docstrings() for func in self._functions]
        return self._functions

    def _register_elements(self, positions: List[int], attribute: str) -> None:
        """Algorithm to insert the comments and blank lines on functions.

        Algorithm to insert items on functions:
            1) get position with bisect_left
            idx = bisect_left(functions, comment_position[0]) - 1
            2) See if the value is contained in the item (may be between functions)
            comment_position[0] in functions[idx]
            3) If found, register
            functions[idx].comments +=1

        Parameters
        ----------
        positions : List[int]
            List of ints representings the positions of the lines.
        attribute : str
            Name of the attribute. May be one of comments or blank_lines.
            Must be an attribute of the corresponding items.

        Examples
        --------
        Per a list of positions of comments in the source code:
        >>> comment_positions = [4, 40, 41, 107]

        Register those lines on the corresponding functions when corresponds:

        >>> visitor._register_elements(comment_positions, 'comments')
        """
        # Only check between the start of the first function
        # and the end of the last function.
        start: int = self.functions[0].start
        end: int = self.functions[-1].end

        for line in positions:
            if start < line < end:  # Exclude exactly first and last.
                idx: int = bisect_left(self.functions, line) - 1
                function = self.functions[idx]
                if line in function:
                    value = getattr(function, attribute) + 1
                    setattr(function, attribute, value)

    def register_functions(self, content: Dict[str, List[int]]) -> None:
        """Register the contents grabbed as tokens outside the ast.

        Inserts the positions of the comments and blank lines.

        Parameters
        ----------
        content : Dict[str, List[int]]
            Contains a dict with the list of the corresponding positions
            to be registered.

        Examples
        --------
        >>> content = {'comments': [1, 4, 5, 6, 22], 'blank_lines': [12, 46]}
        >>> visitor.register_functions(content)
        """
        if len(self.functions) > 0:  # Only run when at least one function was
            for attribute, positions in content.items():
                self._register_elements(positions, attribute)

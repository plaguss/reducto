"""Contains the elements to be extracted from a source file. """

from typing import Optional, Union
import ast


class Item:
    """Base class for the items to be extracted from an ast parsed source file.

    A subclass of this Item corresponds to an ast Node.

    Notes
    -----
    The nodes are inserted as an attribute instead of doing it on the initialization
    to simplify the unit tests.
    """

    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the item.
        start : int
            Line where the item starts in the file.
        end : int
            Line where the item ends in the file.
        """
        self._node: Optional[ast.AST] = None
        self._name = name
        self._start = start
        self._end = end
        self._docstrings: int = 0
        self._get_docstrings_called: bool = False
        self._comments = 0
        self._blank_lines = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}[{self.start}, {self.end}])"

    @property
    def node(self) -> ast.AST:
        """Returns the node itself.

        Returns
        -------
        node : ast.AST
        """
        return self._node  # type: ignore[return-value]

    @node.setter
    def node(self, node_: ast.AST) -> None:
        self._node = node_

    @property
    def name(self) -> str:
        """Name the node.

        Returns
        -------
        name : str
        """
        return self._name

    @property
    def start(self) -> int:
        """Line of the source file where the item starts.

        Returns
        -------
        start : int
        """
        return self._start

    @property
    def end(self) -> int:
        """Line of the source file where the item ends.

        Returns
        -------
        end : int
        """
        return self._end

    def __len__(self) -> int:
        """Computes the total number of lines of the function."""
        return self.end - self.start

    def __lt__(self, other: Union["Item", int]) -> bool:
        """Lower than operator to allow the objects to be sorted in a list.

        Parameters
        ----------
        other : Item
            Item or subclass of it.
        """
        if isinstance(other, Item):
            other_start = other.start
        elif isinstance(other, int):
            other_start = other
        else:
            msg = (
                f"Operator defined only for {self.__class__.__name__}"
                f" instances. You gave: {type(other)}."
            )
            raise TypeError(msg)

        return self.start < other_start

    def __ge__(self, other: Union["Item", int]) -> bool:
        return not self < other

    def __contains__(self, item: int) -> bool:
        """To check if a given line is contained in the item or not.

        Parameters
        ----------
        item : int
            Line position to check.

        Returns
        -------
        contained : bool
            Returns True if the line is between the bounds of the functions.
        """
        return self.start <= item <= self.end

    @property
    def docstrings(self) -> int:
        """Number of lines which are docstring in the item.

        Returns
        -------
        docstrings : int
        """
        return self._docstrings

    @docstrings.setter
    def docstrings(self, docs: int):
        self._docstrings = docs

    @property
    def comments(self) -> int:
        """Number of lines which are comments in the item.

        Returns
        -------
        comments : int
        """
        return self._comments

    @comments.setter
    def comments(self, cmnt: int):
        self._comments = cmnt

    @property
    def blank_lines(self) -> int:
        """Number of lines which are blank lines in the item.

        Returns
        -------
        blank_lines : int
        """
        return self._blank_lines

    @blank_lines.setter
    def blank_lines(self, blnk: int) -> None:
        self._blank_lines = blnk

    @property
    def source_lines(self) -> int:
        """Computes the total number of lines of the item.

        Returns
        -------
        source_lines : int
            The total number of lines is the len of the function minus
            docstrings, comment lines and blank lines.
        """
        return len(self) - self.docstrings - self.comments - self.blank_lines


class FunctionDef(Item):
    """Implementation of an ast.FunctionDef.

    No distinction to an AsyncFunctionDef is made.
    """

    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        super().__init__(name, start=start, end=end)

    def get_docstrings(self) -> int:
        """Obtain the number of lines which are docstring inside the function.

        The method must be called once a node is already registered.

        Returns
        -------
        docs : int

        See Also
        --------
        get_docstring_lines
        """
        if not self._get_docstrings_called:
            self.docstrings = get_docstring_lines(self.node)
        return self.docstrings


class MethodDef(FunctionDef):
    """Equivalent to a FunctionDef.

    Defined in case a distinction between functions and methods is implemented.
    NOT USED.
    """

    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        super().__init__(name, start=start, end=end)


def get_docstring_lines(node: Union[ast.Module, ast.FunctionDef, ast.AST]) -> int:
    r"""Obtains the number of lines which are docstrings.

    Uses ast.get_docstring to extract the docstrings of an ast node.

    Parameters
    ----------
    node : Union[ast.Module, ast.FunctionDef]
        Node which may be a container of docstrings. Only defined for Module and
        FunctionDed.

    Returns
    -------
    docstring_lines : int
        Number of lines in the function or module which are docstrings.

    Notes
    -----
        Reminder:
        -
        '''first '''
        1
        -
        '''second
        '''
        2
        -
        '''

        third'''
        1
        -
        '''
        fourth
        '''
        1
        -
        '''docs


        '''
        4

    """
    docs = ast.get_docstring(node)

    try:
        docstrings = len(docs.split("\n"))  # type: ignore[union-attr]
    except AttributeError:  # When there are no docstrings, returns None.
        docstrings = 0

    return docstrings

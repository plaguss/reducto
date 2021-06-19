"""Contains the the elements to be extracted from a source file.

"""

from typing import Optional, Union
import ast


class Item:
    """Base class for the items to be extracted from an ast parsed source file.

    A subclass of this Item corresponds to an ast Node
    """
    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        self._node: Optional[ast.AST] = None
        self._name = name
        self._start = start
        self._end = end
        self._docstrings: Optional[int] = None  # Initially as None to detect when to run get_docstrings
        self._comments = 0
        self._blank = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}[{self.start}, {self.end}])"

    @property
    def node(self) -> ast.AST:
        """Returns the node itself. """
        return self._node

    @node.setter
    def node(self, node_: ast.AST) -> None:
        self._node = node_

    @property
    def name(self) -> str:
        """Name the node. """
        return self._name

    @property
    def start(self) -> int:
        """Line of the source file where the item starts. """
        return self._start

    @property
    def end(self) -> int:
        """Line of the source file where the item ends. """
        return self._end

    def __len__(self) -> int:
        """Computes the total number of lines of the function. """

        return self.end - self.start

    def __lt__(self, other: 'Item') -> bool:
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
            msg = f"Operator defined only for {self.__class__.__name__}" \
                  f" intances. You gave: {type(other)}."
            raise TypeError(msg)

        return self.start < other_start

    def __ge__(self, other: Union['Item', int]) -> bool:
        return not self < other

    def __contains__(self, item: Union['Item', int]) -> bool:
        """To check if a given line is contained in the item or not.

        Parameters
        ----------
        item

        Returns
        -------

        """
        return self.start <= item <= self.end

    @property
    def docstrings(self) -> int:
        """Number of lines which are docstring in the item. """

        return self._docstrings

    @docstrings.setter
    def docstrings(self, docs: int):
        self._docstrings = docs

    @property
    def comments(self) -> int:
        """Number of lines which are comments in the item. """

        return self._comments

    @comments.setter
    def comments(self, cmnt: int):
        self._comments = cmnt

    @property
    def blank(self) -> int:
        """Number of lines which are blank lines in the item. """

        return self._blank

    @blank.setter
    def blank(self, blnk: int) -> None:
        self._blank = blnk

    @property
    def source_lines(self) -> int:
        """
        Computes the total number of lines of the item, subtracts docstrings, and blank
        lines if found.
        """

        return len(self) - self.docstrings - self.comments - self.blank


def get_docstring_lines(node: Union[ast.Module, ast.FunctionDef]) -> int:
    """Obtains the number of lines which are docstrings.

    TODO: When the docstrings are not multiline, a 1 must be added?

    Parameters
    ----------
    node : Union[ast.Module, ast.FunctionDef]

    Returns
    -------
    docstring_lines : int
    """

    docs: str = ast.get_docstring(node)

    try:
        docstrings: int = len(docs.split('\n'))
    except AttributeError:  # When there are no docstrings, returns None.
        docstrings: int = 0

    return docstrings


class FunctionDef(Item):
    """Corresponds to ast.FunctionDef. No distinction to an AsyncFunctionDef in here.
    """
    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        super().__init__(name, start=start, end=end)

    def get_docstrings(self) -> int:
        """Obtain the number of lines which are docstring inside the function.

        Returns
        -------

        """
        if self.docstrings is None:
            self.docstrings = get_docstring_lines(self.node)
        return self.docstrings


class MethodDef(FunctionDef):
    """Equivalent to a FunctionDef, but obtained from a class.

    The reason to keep it separated from FunctionDef is to add a distinction in the
    name to avoid possible collisions. Always prepends __method__ to the name.
    """
    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        super().__init__(name, start=start, end=end)

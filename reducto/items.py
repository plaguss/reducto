"""Contains the the elements to be extracted from a source file.

"""

import typing as ty


class Item:
    """Base class for the items to be extracted from an ast parsed source file.

    A subclass of this Item corresponds to an ast Node
    """
    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        self._name = name
        self._start = start
        self._end = end
        self._docstrings = 0
        self._comments = 0
        self._blank = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}[{self.start}, {self.end}])"

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

        if not isinstance(other, Item):
            msg = f"Operator defined only for {self.__class__.__name__} intances."
            raise TypeError(msg)

        return self.start < other.start

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
    def blank(self, blnk: int):
        self._blank = blnk

    def source_lines(self) -> int:
        """
        Computes the total number of lines of the item, subtracts docstrings, and blank
        lines if found.
        """

        return len(self) - self.docstrings - self.comments - self.blank


class FunctionDef(Item):
    """Corresponds to ast.FunctionDef. No distinction to an AsyncFunctionDef in here.
    """
    def __init__(self, name: str, start: int = 0, end: int = 0) -> None:
        super().__init__(name)


class MethodDef(Item):
    """Equivalent to a FunctionDef, but obtained from a class.

    The reason to keep it separated from FunctionDef is to add a distinction in the
    name to avoid possible collisions. Always prepends __method__ to the name.
    """
    def __init__(self, name: str) -> None:
        super().__init__("__method__" + name)

"""Module level docstrings.

The following module contains a sample module to be parsed by tests.
"""

# Use some imports.
import os
import sys
import asyncio
import time
import typing as ty


def say_hello() -> str:
    """simple function. """
    return "Hello, World!"


async def print_task() -> None:
    # Function without docstring

    time.sleep(2)
    print("Hey")
    return


def nested_func() -> float:
    import random

    def _inner_func(param):
        return param

    return _inner_func(random.random())


# This line is a simple comment.


class SampleClass:
    """Sample class containing different types of methods.

    """

    attrib = 1  # Attribute set outside init.

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def decorated_method() -> None:
        print("staticmethod")

    def single_arg(self, arg1: str) -> str:
        """Function returning the parameter arg1 as given.

        Parameters
        ----------
        arg1 : str

        Returns
        -------
        arg1 : str
            Expects a string.
        """

        return arg1

    def multi_args(
            self,
            arg1,
            arg2,
            *args,
            kwarg1,
            kwarg2,
            **kwargs
    ) -> None:
        """Function containing multiple positional and keyword arguments accros.

        The arguments are split in different lines.

        Parameters
        ----------
        arg1
        arg2
        args
        kwarg1
        kwarg2
        kwargs
        """

        return

    def multi_return(self) -> ty.Union[int, str]:
        """Multiple return functions. """

        if self.attrib == 1:
            return 1
        elif not isinstance(self.attrib, int):
            return self.attrib
        else:
            return "Other"

    def try_except_method(self, a, b) -> int:
        """Try/except example. """
        try:
            summed = a + b
        except ValueError as err:
            raise err

        return summed

    def yield_func(self):
        """function yielding ints from 1 to 5. """
        for i in range(5):
            yield i


A = 'a'
"""Variable with docstring. """


"""Docstring alone. """

if __name__ == '__main__':
    say_hello()

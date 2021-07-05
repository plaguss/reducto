"""Module containing the application abstraction.

"""

from typing import List
import argparse


class Reducto:
    """Class defining the package application.
    """
    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def add_argument_format(self) -> None:
        """Adds the argument for the type of output format.

        Returns
        -------

        """
        self.parser.add_argument(
            '-f',
            '--format'
        )

    def add_argument_exclude(self):
        pass

    def add_argument_grouped(self):
        pass

    def run(self, arguments: List[str]):
        """

        Parameters
        ----------
        arguments

        Returns
        -------

        """
        pass

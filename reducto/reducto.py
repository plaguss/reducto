"""Module containing the application abstraction.

"""

from typing import List, Optional
import argparse
import pathlib


class Reducto:
    """Class defining the package application.
    """
    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()

    def add_argument_target(self) -> None:
        """Target argument.

        Expects the path pointing to a python package or source file.
        """
        self.parser.add_argument(
            'target',
            type=pathlib.Path,
            default=pathlib.Path.cwd()
        )

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
        """Add argument to exclude paths, files, methods (private or dunder). """
        pass

    def add_argument_grouped(self):
        """Whether to group the package report or not. """
        self.parser.add_argument(
            '-g',
            '--grouped',
            default=False
        )

    def run(self, argv: Optional[List[str]] = None):
        """Execute reducto

        Parameters
        ----------
        argv

        Returns
        -------

        """
        self.parser.parse_args(argv)
        print('hey!')

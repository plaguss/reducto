"""Module containing the application abstraction.

Test the app for development.

From the path containing the pyproject.toml, run:
$ flit install --deps production

Then execute against a package or source file.
"""

from typing import List, Optional
import argparse
import pathlib
import pprint

import reducto.package as pkg
import reducto.src as src
import reducto.reports as rp


class Reducto:
    """Class defining the package application."""

    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self.args: Optional[argparse.Namespace] = None

        # Add arguments
        self.add_argument_target()
        self.add_argument_format()
        self.add_argument_grouped()
        self.add_argument_exclude()
        self.add_argument_output_file()

    def add_argument_target(self) -> None:
        """Target argument.

        Expects the path pointing to a python package or source file.
        """
        self.parser.add_argument(
            "target",
            type=pathlib.Path,
            default=pathlib.Path.cwd(),
            help="Path to execute the program into. "
            "Must be either a python package (REF?) "
            "or a python source file <SRC.py>",
            nargs="?",
        )

    def add_argument_format(self) -> None:
        """Adds the argument for the type of output format.

        The current implementation only allows for raw format (a dict).

        Notes
        -----
        Add redirection to tabulate methods.
        """
        choices: List[str] = [str(rep) for rep in rp.ReportFormat]

        self.parser.add_argument(
            "-f",
            "--format",
            type=rp.ReportFormat,
            default=rp.ReportFormat.RAW,
            choices=list(rp.ReportFormat),
            dest="format",
            help=f"Format for the report type. Options are: {choices}.",
        )

    def add_argument_grouped(self):
        """Whether to group the package report or not.

        Notes
        -----
        The implementation for the boolean argument is taken from:
        https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
        """
        help_: str = (
            "Return the results separated by "
            "source files, or grouped for the "
            "whole package. Only used when the "
            "target path is a package."
        )
        grouped_parser = self.parser.add_mutually_exclusive_group(required=False)
        grouped_parser.add_argument(
            "--grouped", dest="grouped", action="store_true", help=help_
        )
        grouped_parser.add_argument(
            "--ungrouped",
            dest="grouped",
            action="store_false",
            help="Opposite of --grouped.",
        )
        self.parser.set_defaults(grouped=False)

    def add_argument_exclude(self):
        """Add argument to exclude paths, files, methods (private or dunder)."""
        pass

    def add_argument_as_percentage(self) -> None:
        pass

    def add_argument_output_file(self) -> None:
        pass

    def _report_source_file(self, target: pathlib.Path) -> None:
        """

        Parameters
        ----------
        target : pathlib.Path
            Path to the source file.
        """
        src_file: src.SourceFile = src.SourceFile(target)
        reporter: rp.SourceReport = src_file.report()
        pprint.pprint(reporter.report(fmt=self.args.format))

    def _report_package(self, target: pathlib.Path) -> None:
        """

        Parameters
        ----------
        target : pathlib.Path
            Path to the package.
        """
        # TODO: Add extra info for packages, as resume of source files ungrouped
        package: pkg.Package = pkg.Package(target)
        reporter: rp.PackageReport = package.report()
        pprint.pprint(reporter.report(fmt=self.args.format, grouped=self.args.grouped))

    def report(self) -> None:
        """Detects whether the input target is a file or a directory.

        Calls the corresponding method depending on the target.
        """
        target: pathlib.Path = self.args.target
        if target.is_file():
            self._report_source_file(target)
        else:
            self._report_package(target)

    def run(self, argv: Optional[List[str]] = None):
        """Execute reducto.

        Parameters
        ----------
        argv
        """
        self.args: argparse.Namespace = self.parser.parse_args(argv)
        self.report()

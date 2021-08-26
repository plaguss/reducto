"""Module containing the application abstraction.

Test the app for development.

From the path containing the pyproject.toml, run:
$ flit install --deps production

Then execute against a package or source file.
"""

from typing import List, Optional, Dict, Union
import argparse
import pathlib
import json

import reducto.package as pkg
import reducto.src as src
import reducto.reports as rp


# Emoji list: https://unicode.org/emoji/charts/full-emoji-list.html
# MAGIC_WAND: str = "\U0001FA84"
#https://manytools.org/hacker-tools/ascii-banner/
BANNER = """
┬─┐┌─┐┌┬┐┬ ┬┌─┐┌┬┐┌─┐
├┬┘├┤  │││ ││   │ │ │
┴└─└─┘─┴┘└─┘└─┘ ┴ └─┘"""


class Reducto:
    """Class defining the package application."""

    def __init__(self) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self.args: Optional[argparse.Namespace] = None

        # Add arguments
        self._add_argument_target()
        self._add_argument_format()
        self._add_argument_grouped()
        self._add_argument_output_file()

    def _add_argument_target(self) -> None:
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

    def _add_argument_format(self) -> None:
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
            default=rp.ReportFormat.JSON,
            # choices=list(rp.ReportFormat),
            choices="json",
            dest="format",
            help="Format for the report type.",
        )

    def _add_argument_grouped(self):
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
        self.parser.set_defaults(grouped=True)

    def _add_argument_output_file(self) -> None:
        """Argument to insert the output file (if applies).

        Returns
        -------

        """
        default: pathlib.Path = pathlib.Path.cwd() / "reducto_report.json"
        self.parser.add_argument(
            "-o",
            "--output",
            type=pathlib.Path,
            default=default,
            help=f"Full path of the report to be generated. Defaults to {default}",
        )

    def _add_argument_exclude(self):
        """Add argument to exclude paths, files, methods (private or dunder)."""
        raise NotImplementedError

    def _add_argument_as_percentage(self) -> None:
        raise NotImplementedError

    def _report_source_file(self, target: pathlib.Path) -> rp.ReportDict:
        """

        Parameters
        ----------
        target : pathlib.Path
            Path to the source file.
        """
        src_file: src.SourceFile = src.SourceFile(target)
        reporter: rp.SourceReport = src_file.report()
        return reporter.report(fmt=self.args.format)

    def _report_package(self, target: pathlib.Path) -> rp.ReportPackageDict:
        """

        Parameters
        ----------
        target : pathlib.Path
            Path to the package.
        """
        # TODO: Add extra info for packages, as resume of source files ungrouped
        package: pkg.Package = pkg.Package(target)
        reporter: rp.PackageReport = package.report()
        return reporter.report(fmt=self.args.format, grouped=self.args.grouped)

    def report(self) -> Union[rp.ReportDict, rp.ReportPackageDict]:
        """Detects whether the input target is a file or a directory.

        Calls the corresponding method depending on the target.
        """
        target: pathlib.Path = self.args.target
        if target.is_file():
            report = self._report_source_file(target)
        else:
            report = self._report_package(target)

        return report

    def _write_report(self, report: dict) -> None:
        """

        Parameters
        ----------
        filename

        Returns
        -------

        """
        output_file = self.args.output
        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)
        print(f"Report generated: {output_file}")

    def run(self, argv: Optional[List[str]] = None):
        """Execute reducto.

        Parameters
        ----------
        argv
        """
        self.args: argparse.Namespace = self.parser.parse_args(argv)
        print(BANNER)
        report = self.report()
        self._write_report(report)

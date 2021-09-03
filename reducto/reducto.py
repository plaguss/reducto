"""Module containing the application abstraction. """

from typing import List, Optional, Union
import argparse
import pathlib
import json
import pprint

import reducto.package as pkg
import reducto.src as src
import reducto.reports as rp
import reducto as rd


class Reducto:
    """Class defining the package application.

    This class represents the reducto application.
    Its made of an argparse.ArgumentParser.
    The different arguments are defined as private methods to be
    called on initialization.
    """

    def __init__(self) -> None:  # pragma: no cover, redirects methods
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self.args: Optional[argparse.Namespace] = None
        # Add arguments
        self._add_argument_version()
        self._add_argument_target()
        self._add_argument_format()
        self._add_argument_grouped()
        self._add_argument_output_file()
        self._add_argument_as_percentage()

    def _parse_args(self, argv: Optional[List[str]] = None) -> None:  # pragma: no cover
        # proxy function to simplify testing
        self.args = self.parser.parse_args(argv)

    def _add_argument_version(self) -> None:  # pragma: no cover
        """Version argument.

        Returns the current version of the package.
        """
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"reducto {rd.__version__}",
            help="Show the version of the program.",
        )

    def _add_argument_target(self) -> None:  # pragma: no cover
        """Target argument.

        Expects the path pointing to a python package or source file.
        """
        self.parser.add_argument(
            "target",
            type=pathlib.Path,
            default=pathlib.Path.cwd(),
            help="Path to execute the program into. "
            "Must be either a python package (directory containing an __init__.py) "
            "or a python source file {SRC.py}",
            nargs="?",
        )

    def _add_argument_format(self) -> None:  # pragma: no cover
        """Adds the argument for the type of output format.

        The current implementation only allows for raw format (a dict).

        Notes
        -----
        Add redirection to tabulate methods.
        """
        self.parser.add_argument(
            "-f",
            "--format",
            type=rp.ReportFormat,
            default=rp.ReportFormat.JSON,
            choices=list(rp.ReportFormat),
            dest="format",
            help="Format for the report type.",
        )

    def _add_argument_grouped(self) -> None:  # pragma: no cover
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

    def _add_argument_output_file(self) -> None:  # pragma: no cover
        """Argument to insert the output file (if applies)."""
        self.parser.add_argument(
            "-o",
            "--output",
            type=pathlib.Path,
            default=None,
            help="Full path of the report to be generated. If not"
            " given, redirects to stdout.",
        )

    def _add_argument_exclude(self) -> None:  # pragma: no cover
        """Add argument to exclude paths, files, methods (private or dunder)."""
        raise NotImplementedError

    def _add_argument_as_percentage(self) -> None:  # pragma: no cover
        """Add argument to report lines as percentage."""
        self.parser.add_argument(
            "-p",
            "--percentage",
            dest="percentage",
            action="store_true",
            help="Report the number of lines as percentage.",
        )

    def _report_source_file(self, target: pathlib.Path) -> rp.SourceReportType:
        """Create a report of a single source file.

        Parameters
        ----------
        target : pathlib.Path
            Path to the source file.

        Returns
        -------
        report : rp.ReportDict
            Dict containing the report.
        """
        src_file: src.SourceFile = src.SourceFile(target)
        reporter: rp.SourceReport = src_file.report()
        return reporter.report(
            fmt=self.args.format,  # type: ignore[union-attr]
            is_package=True,
            percentage=self.args.percentage,  # type: ignore[union-attr]
        )

    def _report_package(self, target: pathlib.Path) -> rp.PackageReportType:
        """Create a report of a python package.

        Parameters
        ----------
        target : pathlib.Path
            Path to the package.

        Returns
        -------
        report : rp.ReportPackageDict
            Dict containing the report.
        """
        package: pkg.Package = pkg.Package(target)
        reporter: rp.PackageReport = package.report()
        return reporter.report(
            fmt=self.args.format,  # type: ignore[union-attr]
            grouped=self.args.grouped,  # type: ignore[union-attr]
            percentage=self.args.percentage,  # type: ignore[union-attr]
        )

    def report(self) -> Union[rp.SourceReportType, rp.PackageReportType]:
        """Detects whether the input target is a file or a directory.

        Calls the corresponding method depending on the target.

        See Also
        --------
        run
        """
        target: pathlib.Path = self.args.target  # type: ignore[union-attr]
        if target.is_file():
            report: Union[
                rp.SourceReportType, rp.PackageReportType
            ] = self._report_source_file(target)
        else:
            report = self._report_package(target)

        return report

    def _write_report(
        self, report: Union[rp.SourceReportType, rp.PackageReportType]
    ) -> None:  # pragma: no cover, proxy to json dump
        """Writes the report to a json file.

        Parameters
        ----------
        report : Union[rp.ReportDict, rp.ReportPackageDict]
            Contains the resulting report.
        """
        output_file = self.args.output  # type: ignore[union-attr]
        if isinstance(report, dict):
            with open(output_file, "w") as f:
                json.dump(report, f, indent=4)
        else:
            with open(output_file, "w") as f:
                f.write(report)

        print(f"Report generated: {output_file}")

    def run(self, argv: Optional[List[str]] = None) -> None:
        """Execute reducto.

        The only relevant public method.
        Parses the terminal arguments, generates the report
        and writes it to a file.

        Parameters
        ----------
        argv : Optional[List[str]]
            Arguments passed from the terminal.
        """
        self._parse_args(argv)
        report: Union[rp.SourceReportType, rp.PackageReportType] = self.report()
        if self.args.output is not None:  # type: ignore[union-attr]  # pragma: no cover
            # Write file if output is given.
            self._write_report(report)
        elif self.args.format == rp.ReportFormat.JSON:  # type: ignore[union-attr]
            # pretty print dict result
            pprint.pprint(report)
        else:  # tabulate results are expected to be printed with print.
            print(report)

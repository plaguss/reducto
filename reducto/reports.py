"""Module storing the different reports presented by the package. """

from __future__ import annotations

import pathlib
from typing import Dict, Union, List
from enum import Enum
import statistics
from tabulate import tabulate

# This is done to avoid circular imports.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .src import SourceFile  # pragma: no cover, only to avoid circular imports
    from .package import Package  # pragma: no cover, only to avoid circular imports

import os


ReportDict = Dict[str, Dict[str, int]]
ReportPackageDict = Dict[str, ReportDict]

Reporting = Union[ReportDict, ReportPackageDict]


class ReportFormat(Enum):
    """Formats allowed for the reports.

    JSON corresponds to the base dict format, the remaining
    formats correspond to the ones defined in tabulate package.
    """

    JSON = "json"
    # Tabulate formats:
    SIMPLE = "simple"
    PLAIN = "plain"
    GRID = "grid"
    FANCY_GRID = "fancy_grid"
    GITHUB = "github"
    PIPE = "pipe"
    ORGTBL = "orgtbl"
    JIRA = "jira"
    PRESTO = "presto"
    PRETTY = "pretty"
    PSQL = "psql"
    RST = "rst"
    MEDIAWIKI = "mediawiki"
    MOINMOIN = "moinmoin"
    YOUTRACK = "youtrack"
    HTML = "html"
    UNSAFEHTML = "unsafehtml"
    LATEX = "latex"
    LATEX_RAW = "latex_raw"
    LATEX_BOOKTABS = "latex_booktabs"
    LATEX_LONGTABLE = "latex_longtable"
    TSV = "tsv"
    TEXTILE = "textile"

    def __str__(self) -> str:
        return self.value


class ReportFormatError(Exception):
    """Error raised on wrong reporting format."""

    def __init__(self, fmt: ReportFormat) -> None:
        msg = (
            f"Report format not defined: {fmt}. "
            f"Must be one defined in {[str(fmt) for fmt in ReportFormat]}."
        )
        super().__init__(msg)


class SourceReport:
    """Reporting class per a source (.py) file.

    Contains a report method to obtain the proper report format
    from a SourceFile object.

    Methods
    -------
    report

    See Also
    --------
    SourceFile
    """

    def __init__(self, src_file: SourceFile) -> None:
        """
        Parameters
        ----------
        src_file : src.SourceFile
            File to where the data is gathered from to obtain a report.
        """
        self._src_file: SourceFile = src_file

    def __repr__(self) -> str:
        return type(self).__name__

    @property
    def source_file(self) -> SourceFile:
        """Returns the source file.

        Returns
        -------
        src_file : src.SourceFile.
        """
        return self._src_file

    def report(
            self,
            fmt: ReportFormat = ReportFormat.JSON,
            is_package: bool = False
    ) -> ReportDict:
        """Report of a source file.

        Parameters
        ----------
        fmt : ReportFormat
            Must be one of ReportFormats. Defaults to ReportFormats.JSON.
        is_package : bool
            Bool to determine if a SourceFile is the single entry point for an app.
            Defaults to False.
            It is used to

        Returns
        -------
        report : ReportDict

        Raises
        ------
        ReportFormatError
            When the reporting required is not defined in ReportFormat enum.
        """
        report_ = self._as_dict()

        if fmt == ReportFormat.JSON:
            pass
        elif fmt in set(fmt_ for fmt_ in ReportFormat):
            if is_package:
                # raise NotImplementedError('Table method for SourceReport')
                return self._table(report_, fmt=str(fmt))
        else:
            raise ReportFormatError(fmt)

        return report_

    def _as_dict(self) -> ReportDict:
        """Report of a file with a dict format.

        The reporting is a dict with the source file name as a key,
        and an inner key with the following data:
        lines (total lines of the file), number of functions,
        average function length, docstring lines, comment lines,
        blank lines.

        Returns
        -------
        dict_report : ReportDict
        """
        # Check whether any function was found
        if len(self.source_file.functions) == 0:
            avg_func_length = 0
        else:
            avg_func_length: int = statistics.mean(
                [f.source_lines for f in self.source_file.functions]
            )

        data: Dict[str, int] = {
            "lines": len(self.source_file),
            "number_of_functions": len(self.source_file.functions),
            "average_function_length": round(avg_func_length),
            "docstring_lines": self.source_file.total_docstrings,
            "comment_lines": self.source_file.comment_lines,
            "blank_lines": self.source_file.blank_lines,
            "source_lines": self.source_file.source_lines,  # FIXME: Add source lines to src.py
        }

        return {self.source_file.name: data}

    def _table(
        self,
        report: Union[ReportDict, ReportPackageDict],
        fmt: str = "grid"
    ) -> str:  # pragma: no cover, proxy
        """Creates the report from tabulate. Proxy method for tabulate_report
        """
        columns: List[str] = [
            "lines",
            "number_of_functions",
            "source_lines",
            "docstring_lines",
            "comment_lines",
            "blank_lines",
            "average_function_length"
        ]
        return tabulate_report(
            self.source_file.name,
            report,
            columns,
            grouped=True,
            fmt=fmt
        )


class PackageReport:
    """Define report for a package, gets a pkg.Package as input.

    Contains a report method to obtain the proper report format
    from a SourceFile object.

    See Also
    --------
    Package
    """

    def __init__(self, package: Package) -> None:
        """
        Parameters
        ----------
        package : Package
            Package containing the data to be reported
        """
        self._package: Package = package
        self.columns: List[str] = [
            "lines",
            "number_of_functions",
            "source_lines",
            "docstring_lines",
            "comment_lines",
            "blank_lines",
            "average_function_length",
            "source_files",
        ]

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self.package.name})"

    @property
    def package(self) -> Package:
        """Returns the package given as input.

        Returns
        -------
        package : Package
        """
        return self._package

    @property
    def name(self) -> str:
        # Redirect name to simplify testing
        return self.package.name

    def report(
        self, fmt: ReportFormat = ReportFormat.JSON, grouped: bool = False
    ) -> List[List[str | int]] | Dict[str, Dict[str, int]] | Dict[
        str, Dict[str, Dict[str, int]]
    ]:
        """Report method for a package.

        Generates the report for a Package made of Source files.
        Initially gets the info either grouped or ungrouped,
        if the format chosen is json its returned directly.

        Parameters
        ----------
        fmt : ReportFormat
            Format to return the information. Defaults to ReportFormats.JSON.
        grouped : bool
            Whether to return the information by source files, or grouped at
            the package level (resumes the package). Defaults to False, returns
            the information per source file.

        Returns
        -------
        report : ReportPackageDict

        Raises
        ------
        ReportFormatError
            When a report format is not defined
        """
        if grouped:
            report: ReportDict = self._report_grouped()
        else:
            report: ReportPackageDict = self._report_ungrouped()

        if fmt == ReportFormat.JSON:
            pass
        elif fmt in set(fmt_ for fmt_ in ReportFormat):
            return self._table(report, fmt=str(fmt), grouped=grouped)
        else:  # Other formats may modify the report here
            raise ReportFormatError(fmt)

        return report

    def _report_grouped(self) -> ReportDict:
        """Obtain the reporting information grouped for the whole package.

        Returns
        -------
        report : ReportDict
            Dict ordered as: {package_name: {source_file_report}}.
        """
        report_ungrouped: ReportPackageDict = self._report_ungrouped()
        package_lines: int = len(self.package)

        lines: int = 0
        number_of_functions: int = 0
        average_function_length: int = 0
        docstring_lines: int = 0
        comment_lines: int = 0
        blank_lines: int = 0
        source_lines: int = 0

        for reporting in report_ungrouped[self.package.name].values():
            lines += reporting["lines"]
            number_of_functions += reporting["number_of_functions"]
            # Weight for the average function length across the whole package.
            weight: float = reporting["lines"] / package_lines
            average_function_length += reporting["average_function_length"] * weight
            docstring_lines += reporting["docstring_lines"]
            comment_lines += reporting["comment_lines"]
            blank_lines += reporting["blank_lines"]
            source_lines += reporting["source_lines"]

        report_grouped: Dict[str, int] = {
            "lines": lines,
            "number_of_functions": number_of_functions,
            "average_function_length": round(average_function_length),
            "docstring_lines": docstring_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "source_files": len(self.package.source_files),
            "source_lines": source_lines,
        }

        return {self.package.name: report_grouped}

    def _report_ungrouped(self) -> ReportPackageDict:
        """Obtain the reporting information per source file.

        Returns
        -------
        report : ReportPackageDict
            Dict ordered as:
            {package_name:
                {source_file_1:
                    {source_file_report},
                source_file_2:
                    {source_file_report}
                }
            }
        """
        report: ReportDict = {}
        for file in self.package.source_files:
            report[self._get_relname(str(file))] = SourceReport(file).report(
                fmt=ReportFormat.JSON
            )[file.name]

        return {self.package.name: report}

    def _get_relname(self, file: str) -> str:
        """Obtain the relative name of a file in the package.

        Parameters
        ----------
        file : str
            Name of the file.

        Returns
        -------
        relname : str
            Relative path of the file starting on the package.

        Examples
        --------
        For a given __init__.py file at the top of a package
        named my_package:

        >>> package_report._package_relname('__init__.py')
        'my_package/__init__.py'
        """
        relname: str = os.path.relpath(file, start=self.package.path)
        return str(pathlib.Path(self.package.name) / relname)

    def _table(
        self,
        report: Union[ReportDict, ReportPackageDict],
        fmt: str = "grid",
        grouped: bool = True,
    ) -> str:  # pragma: no cover, proxy
        """Creates the report from tabulate. Proxy method for tabulate_report
        """
        return tabulate_report(
            self.name,
            report,
            self.columns,
            grouped=grouped,
            fmt=fmt
        )


def tabulate_report(
        name: str,
        report: Union[ReportDict, ReportPackageDict],
        columns: List[str],
        grouped: bool = True,
        fmt: str = "grid"
) -> str:
    """

    Parameters
    ----------
    name
    report
    columns
    grouped
    fmt

    Returns
    -------

    """
    name: str = name
    headers: List[str] = []
    table: List[List[Union[str, int]]] = []
    inner = report[name]
    if grouped:
        headers.extend(column_split(columns))
        headers.insert(0, "package")
        row = [name]
        row.extend([inner[col] for col in columns])
        table.append(row)

    else:
        columns = columns.copy()
        columns.remove("source_files")
        headers.extend(column_split(columns))
        headers.insert(0, "filename")
        rows: List[List[Union[str, int]]] = []
        for filename in inner:
            row = [filename]
            row.extend([inner[filename][col] for col in columns])
            rows.append(row)
        table.extend(rows)

    return tabulate(table, headers=headers, tablefmt=fmt)


def column_split(columns: List[str]) -> List[str]:
    r"""Splits the columns to avoid longer formats for tabulate.

    Replaces every `_` by `\n`

    Parameters
    ----------
    columns : List[str]

    Returns
    -------
    splitted : List[str]
    """
    return [column.replace('_', '\n') for column in columns]


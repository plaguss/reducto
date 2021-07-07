"""
Module storing the different reports presented by the package.
"""

from __future__ import annotations

from typing import List, Dict, Union
from enum import Enum
import statistics
# from tabulate import tabulate

# This is done to avoid circular imports.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .src import SourceFile  # pragma: no cover, only to avoid circular imports
    from .package import Package  # pragma: no cover, only to avoid circular imports


ReportDict = Dict[str, Dict[str, int]]
ReportPackageDict = Dict[str, ReportDict]

Reporting = Union[ReportDict, ReportPackageDict]


class ReportFormat(Enum):
    """Formats allowed for the reports. """
    RAW = 'raw'

    def __str__(self) -> str:
        return self.value


class ReportFormatError(Exception):
    """Error raised on wrong reporting format. """
    def __init__(self, fmt: ReportFormat) -> None:
        msg = f'Report format not defined: {fmt}. ' \
              f'Must be one defined in {ReportFormat}.'
        super().__init__(msg)


class SourceReport:
    """Reporting class.

    Methods
    -------
    report
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

    def report(self, fmt: ReportFormat = ReportFormat.RAW) -> Reporting:
        """Report of a source file.

        Parameters
        ----------
        fmt : ReportFormat
            Must be one of ReportFormats. Defaults to ReportFormats.RAW.

        Returns
        -------
        report : Reporting
        """
        if fmt == ReportFormat.RAW:
            report_ = self._as_dict()
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
            avg_func_length: int = statistics.mean([f.source_lines for f in self.source_file.functions])

        data: Dict[str, int] = {
            'lines': len(self.source_file),
            'number_of_functions': len(self.source_file.functions),
            'average_function_length': round(avg_func_length),
            'docstring_lines': self.source_file.total_docstrings,
            'comment_lines': self.source_file.comment_lines,
            'blank_lines': self.source_file.blank_lines,
            # 'source_lines': self.source_file  # FIXME: Add source lines to src.py
        }

        return {self.source_file.name: data}


class PackageReport:
    """
    Define report for a package, gets a pkg.Package as input.
    """
    def __init__(self, package: Package) -> None:
        """
        Parameters
        ----------
        package : Package
            Package containing the data to be reported
        """
        self._package: Package = package

    def __repr__(self) -> str:
        return type(self).__name__ + f'({self.package.name})'

    @property
    def package(self) -> Package:
        """Returns the package given as input.

        Returns
        -------
        package : Package
        """
        return self._package

    def report(
            self,
            fmt: ReportFormat = ReportFormat.RAW,
            grouped: bool = False
    ) -> Reporting:
        """

        Parameters
        ----------
        fmt : ReportFormat
            Format to return the information. Defaults to ReportFormats.RAW.
        grouped : bool
            Whether to return the information by source files, or grouped at
            the package level (resumes the package). Defaults to False, returns
            the information per source file.

        Returns
        -------

        """
        # FIXME: Add functionality for different formats
        if grouped:
            report: ReportDict = self._report_grouped()
        else:
            report: ReportPackageDict = self._report_ungrouped()

        if fmt == ReportFormat.RAW:
            pass
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

        for reporting in report_ungrouped[self.package.name].values():
            lines += reporting['lines']
            number_of_functions += reporting['number_of_functions']
            # Weight for the average function length across the whole package.
            weight: float = reporting['lines'] / package_lines
            average_function_length += reporting['average_function_length'] * weight
            docstring_lines += reporting['docstring_lines']
            comment_lines += reporting['comment_lines']
            blank_lines += reporting['blank_lines']

        report_grouped: Dict[str, int] = {
            'lines': lines,
            'number_of_functions': number_of_functions,
            'average_function_length': round(average_function_length),
            'docstring_lines': docstring_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'source_files': len(self.package.source_files)
            # 'source_lines':
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
            report[file.name] = SourceReport(file).report(fmt=ReportFormat.RAW)[file.name]

        return {self.package.name: report}

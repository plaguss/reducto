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


ReportDict = Dict[str, Dict[str, int]]

Reporting = Union[ReportDict]


class ReportFormats(Enum):
    """Formats allowed for the reports. """
    DICT = 0


class ReportFormatError(Exception):
    """Error raised on wrong reporting format. """
    def __init__(self, fmt: ReportFormats) -> None:
        msg = f'Report format not defined: {fmt}. ' \
              f'Must be one defined in {ReportFormats}.'
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

    def report(self, fmt: ReportFormats = ReportFormats.DICT) -> Reporting:
        """Report of a source file.

        Parameters
        ----------
        fmt : ReportFormats
            Must be one of ReportFormats. Defaults to ReportFormats.DICT.

        Returns
        -------
        report : Reporting
        """
        if fmt == ReportFormats.DICT:
            report_ = self._report_dict()
        else:
            raise ReportFormatError(fmt)

        return report_

    def _report_dict(self) -> ReportDict:
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
        avg_func_length: float = statistics.mean([f.source_lines for f in self.source_file.functions])
        data: Dict[str, int] = {
            'lines': len(self.source_file),
            'number_of_functions': len(self.source_file.functions),
            'average_function_length': round(avg_func_length),
            'docstring_lines': self.source_file.total_docstrings,
            'comment_lines': self.source_file.comment_lines,
            'blank_lines': self.source_file.blank_lines
        }

        return {self.source_file.name: data}

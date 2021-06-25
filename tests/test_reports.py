"""
Contains the tests for reports module.
"""
import pytest

import reducto.reports as rp
import reducto.src as src
import os
import pathlib

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def test_err():
    assert isinstance(rp.ReportFormatError('aa'), Exception)


def test_assert_report_formats():
    assert len(rp.ReportFormats.__members__.items()) == 1
    assert rp.ReportFormats.DICT.value == 0


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


class TestModuleReport:
    @pytest.fixture(scope='class')
    def reporter(self):
        src_file = src.SourceFile(pathlib.Path(get_sample_file('example.py')))
        return rp.SourceReport(src_file)

    def test_report_instance(self, reporter):
        assert isinstance(reporter, rp.SourceReport)

    def test_report_repr(self, reporter):
        assert repr(reporter) == 'SourceReport'

    def test_source_file(self, reporter):
        assert isinstance(reporter.source_file, src.SourceFile)

    def test_report_error(self, reporter):
        with pytest.raises(rp.ReportFormatError):
            reporter.report(fmt='wrong')

    def test_report(self, reporter):
        assert reporter.report(fmt=rp.ReportFormats.DICT) == reporter._report_dict()

    def test_report_dict(self, reporter):
        report_dict = reporter._report_dict()
        assert isinstance(report_dict, dict)
        assert isinstance(report_dict['example.py'], dict)
        assert report_dict['example.py']['lines'] == 128
        assert report_dict['example.py']['number_of_functions'] == 11
        assert report_dict['example.py']['average_function_length'] == 3
        assert report_dict['example.py']['docstring_lines'] == 29
        assert report_dict['example.py']['blank_lines'] == 32

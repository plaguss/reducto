"""
Contains the tests for reports module.
"""

import pytest
import os
import pathlib

import reducto.reports as rp
import reducto.src as src
import reducto.package as pkg


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def test_err():
    assert isinstance(rp.ReportFormatError('aa'), Exception)


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
        assert reporter.report(fmt=rp.ReportFormat.RAW) == reporter._as_dict()

    def test_as_dict(self, reporter):
        report_dict = reporter._as_dict()
        assert isinstance(report_dict, dict)
        assert isinstance(report_dict['example.py'], dict)
        assert report_dict['example.py']['lines'] == 128
        assert report_dict['example.py']['number_of_functions'] == 11
        assert report_dict['example.py']['average_function_length'] == 3
        assert report_dict['example.py']['docstring_lines'] == 29
        assert report_dict['example.py']['blank_lines'] == 32
        assert report_dict['example.py']['comment_lines'] == 3
        assert report_dict['example.py']['source_lines'] == 64


class TestPackageReport:
    @pytest.fixture
    def reporter(self, sample_package):
        pack = pkg.Package(sample_package)
        return rp.PackageReport(pack)

    def test_report_repr(self, reporter, sample_package):
        assert repr(reporter) == f'PackageReport({sample_package.name})'

    def test_package(self, reporter):
        assert isinstance(reporter.package, pkg.Package)

    def test_report_error(self, reporter):
        with pytest.raises(rp.ReportFormatError):
            reporter.report(fmt='wrong')

    def test_report(self, reporter):
        assert reporter.report(fmt=rp.ReportFormat.RAW) == reporter._report_ungrouped()
        assert reporter.report(fmt=rp.ReportFormat.RAW, grouped=True) == reporter._report_grouped()

    def test_report_grouped(self, reporter):
        report = reporter.report(grouped=True)
        keys = list(report.keys())
        assert len(keys) == 1
        name = keys[0]
        assert name == reporter.package.name
        info = report[name]
        assert info['lines'] == 514
        assert info['docstring_lines'] == 116
        assert info['comment_lines'] == 12
        assert info['blank_lines'] == 130
        # info['source_lines'] == 513
        assert info['source_files'] == 7
        assert info['source_lines'] == 256
        assert info['number_of_functions'] == 44
        assert info['average_function_length'] == 3

    def test_report_ungrouped(self, reporter):
        report = reporter.report(grouped=False)
        keys = list(report.keys())
        assert len(keys) == 1
        name = keys[0]
        assert name == reporter.package.name
        info = report[name]
        example = info[str(pathlib.Path(name) / 'pyfile.py')]
        # Only tested one source file
        assert example
        assert example['lines'] == 128
        assert example['number_of_functions'] == 11
        assert example['average_function_length'] == 3
        assert example['docstring_lines'] == 29
        assert example['blank_lines'] == 32
        assert example['comment_lines'] == 3
        assert example['source_lines'] == 64

    def test_report_relpaths(self, reporter):
        report = reporter.report(grouped=False)
        name = reporter.package.name
        info = report[name]
        relnames = sorted(info.keys())
        correct_names = sorted([
            str(pathlib.Path(name) / '__init__.py'),
            str(pathlib.Path(name) / 'pyfile.py'),
            str(pathlib.Path(name) / 'subproj' / '__init__.py'),
            str(pathlib.Path(name) / 'subproj' / 'main.py'),
            str(pathlib.Path(name) / 'subproj' / 'help.py'),
            str(pathlib.Path(name) / 'src' / 'ext' / '__init__.py'),
            str(pathlib.Path(name) / 'src' / 'ext' / 'ext.py'),
        ])
        assert all(rel == corr for rel, corr in zip(relnames, correct_names))

    @pytest.mark.skip('NOT IMPLEMENTED')
    def test_report_package_void(self, reporter):
        # Test a package without content
        assert 1 == 0

    @pytest.mark.skip('NOT IMPLEMENTED')
    def test_report_package_percentage(self, reporter):
        # Test a package with results formatted as percentages
        assert 1 == 0

    @pytest.mark.skip('NOT IMPLEMENTED')
    def test_sample(self, reporter):
        print(reporter.table(reporter.report()))
        assert 1 == 0

"""
Contains the tests for reports module.
"""

import pytest
import os
import pathlib
from unittest import mock
from unittest.mock import PropertyMock

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
        assert reporter.report(fmt=rp.ReportFormat.JSON) == reporter._as_dict()

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

    def test_as_dict_percentage(self, reporter):
        report_dict = reporter._as_dict(percentage=True)
        assert isinstance(report_dict, dict)
        assert isinstance(report_dict['example.py'], dict)
        assert report_dict['example.py']['lines'] == 128
        assert report_dict['example.py']['number_of_functions'] == 11
        assert report_dict['example.py']['average_function_length'] == 3
        assert report_dict['example.py']['docstring_lines'] == '23%'
        assert report_dict['example.py']['blank_lines'] == '25%'
        assert report_dict['example.py']['comment_lines'] == '2%'
        assert report_dict['example.py']['source_lines'] == '50%'


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
        assert reporter.report(fmt=rp.ReportFormat.JSON) == reporter._report_ungrouped()
        assert reporter.report(fmt=rp.ReportFormat.JSON, grouped=True) == reporter._report_grouped()

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

    def test_report_grouped_percentage(self, reporter):
        report = reporter.report(grouped=True, percentage=True)
        keys = list(report.keys())
        assert len(keys) == 1
        name = keys[0]
        assert name == reporter.package.name
        info = report[name]
        print(info)
        assert info['lines'] == 514
        assert info['docstring_lines'] == '23%'
        assert info['comment_lines'] == '2%'
        assert info['blank_lines'] == '25%'
        assert info['source_files'] == 7
        assert info['source_lines'] == '50%'
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

    def test_columns(self, reporter):
        assert len(reporter.columns) == 8

    @pytest.mark.skipif(rp.tabulate is None, reason='Tabulate is not installed.')
    def test_table_grouped(self, reporter):
        report = {
            "reducto": {
                "lines": 1609,
                "number_of_functions": 102,
                "average_function_length": 5,
                "docstring_lines": 557,
                "comment_lines": 30,
                "blank_lines": 196,
                "source_files": 7,
                "source_lines": 826
            }
        }
        to_mock = 'reducto.reports.PackageReport.name'
        with mock.patch(to_mock, new_callable=PropertyMock) as mocked:
            mocked.return_value = 'reducto'
            table = reporter._table(report, fmt='grid')
            expected = '\n'.join([
                "+-----------+---------+-------------+----------+-------------+-----------+---------+------------+----------+",
                "| package   |   lines |      number |   source |   docstring |   comment |   blank |    average |   source |",
                "|           |         |          of |    lines |       lines |     lines |   lines |   function |    files |",
                "|           |         |   functions |          |             |           |         |     length |          |",
                "+===========+=========+=============+==========+=============+===========+=========+============+==========+",
                "| reducto   |    1609 |         102 |      826 |         557 |        30 |     196 |          5 |        7 |",
                "+-----------+---------+-------------+----------+-------------+-----------+---------+------------+----------+"
            ])
            assert table == expected

    @pytest.mark.skipif(rp.tabulate is None, reason='Tabulate is not installed.')
    def test_table_ungrouped(self, reporter):
        report = {'reducto': {'reducto/__init__.py': {'average_function_length': 0,
                                     'blank_lines': 2,
                                     'comment_lines': 0,
                                     'docstring_lines': 1,
                                     'lines': 5,
                                     'number_of_functions': 0,
                                     'source_lines': 2},
             'reducto/cli.py': {'average_function_length': 5,
                                'blank_lines': 5,
                                'comment_lines': 0,
                                'docstring_lines': 5,
                                'lines': 20,
                                'number_of_functions': 1,
                                'source_lines': 10},
             'reducto/items.py': {'average_function_length': 3,
                                  'blank_lines': 33,
                                  'comment_lines': 0,
                                  'docstring_lines': 121,
                                  'lines': 272,
                                  'number_of_functions': 22,
                                  'source_lines': 118},
             'reducto/package.py': {'average_function_length': 5,
                                    'blank_lines': 39,
                                    'comment_lines': 6,
                                    'docstring_lines': 157,
                                    'lines': 351,
                                    'number_of_functions': 20,
                                    'source_lines': 149},
             'reducto/reducto.py': {'average_function_length': 7,
                                    'blank_lines': 20,
                                    'comment_lines': 5,
                                    'docstring_lines': 67,
                                    'lines': 212,
                                    'number_of_functions': 13,
                                    'source_lines': 120},
             'reducto/reports.py': {'average_function_length': 8,
                                    'blank_lines': 45,
                                    'comment_lines': 7,
                                    'docstring_lines': 106,
                                    'lines': 378,
                                    'number_of_functions': 16,
                                    'source_lines': 220},
             'reducto/src.py': {'average_function_length': 4,
                                'blank_lines': 53,
                                'comment_lines': 3,
                                'docstring_lines': 279,
                                'lines': 561,
                                'number_of_functions': 32,
                                'source_lines': 226}
            }
        }
        to_mock = 'reducto.reports.PackageReport.name'
        with mock.patch(to_mock, new_callable=PropertyMock) as mocked:
            mocked.return_value = 'reducto'
            table = reporter._table(report, grouped=False, fmt='grid')
            expected = '\n'.join([
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| filename            |   lines |      number |   source |   docstring |   comment |   blank |    average |",
                "|                     |         |          of |    lines |       lines |     lines |   lines |   function |",
                "|                     |         |   functions |          |             |           |         |     length |",
                "+=====================+=========+=============+==========+=============+===========+=========+============+",
                "| reducto/__init__.py |       5 |           0 |        2 |           1 |         0 |       2 |          0 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/cli.py      |      20 |           1 |       10 |           5 |         0 |       5 |          5 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/items.py    |     272 |          22 |      118 |         121 |         0 |      33 |          3 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/package.py  |     351 |          20 |      149 |         157 |         6 |      39 |          5 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/reducto.py  |     212 |          13 |      120 |          67 |         5 |      20 |          7 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/reports.py  |     378 |          16 |      220 |         106 |         7 |      45 |          8 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+",
                "| reducto/src.py      |     561 |          32 |      226 |         279 |         3 |      53 |          4 |",
                "+---------------------+---------+-------------+----------+-------------+-----------+---------+------------+"
            ])
            assert table == expected

    @pytest.mark.skipif(rp.tabulate is None, reason='Tabulate is not installed.')
    def test_report_table(self, reporter):
        # Test in this point is only done for a str and one of the column names in
        # the table.
        table = reporter.report(fmt=rp.ReportFormat.PLAIN, grouped=False)
        assert isinstance(table, str)
        assert 'lines' in table

    @pytest.mark.skip('NOT IMPLEMENTED')
    def test_report_package_void(self, reporter):
        # Test a package without content
        assert 1 == 0

    @pytest.mark.skip('NOT IMPLEMENTED')
    def test_report_package_percentage(self, reporter):
        # Test a package with results formatted as percentages
        assert 1 == 0


def test_column_split():
    columns = [
        "lines",
        "number_of_functions",
        "source_lines",
        "docstring_lines",
        "comment_lines",
        "blank_lines",
        "average_function_length"
    ]
    expected = [
        "lines",
        "number\nof\nfunctions",
        "source\nlines",
        "docstring\nlines",
        "comment\nlines",
        "blank\nlines",
        "average\nfunction\nlength"
    ]
    splitted = rp.column_split(columns)

    assert expected == splitted

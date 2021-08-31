"""Tests for reducto/reducto.py

Includes functional tests for Reducto app.
"""

from unittest import mock

import pytest

import reducto.reducto as rd


class TestReducto:
    @pytest.fixture(scope='class')
    def app(self):
        return rd.Reducto()

    def test_report_source_file_report_json(self, app, source_file_one_function):
        app._parse_args(['--format', 'json'])
        report = app._report_source_file(source_file_one_function)
        assert isinstance(report, dict)

    def test_report_source_file_report_tabulate(self, app, source_file_one_function):
        app._parse_args(['--format', 'plain'])
        report = app._report_source_file(source_file_one_function)
        assert isinstance(report, str)

    def test_report_package_report_json(self, app, sample_package):
        app._parse_args(['--format', 'json'])
        report = app._report_package(sample_package)
        assert isinstance(report, dict)

    def test_report_package_report_tabulate(self, app, sample_package):
        app._parse_args(['--format', 'plain'])
        report = app._report_package(sample_package)
        assert isinstance(report, str)

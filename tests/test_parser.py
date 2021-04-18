"""Tests defined for reducto.parser.
"""

import os
import pytest

import reducto.parser as prs


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


def test_load_source_file():
    assert True is False


def test_line_count():
    pass


if __name__ == '__main__':
    print(SAMPLE_DATA)


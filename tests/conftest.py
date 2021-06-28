"""
Contains functions useful on different testing modules.
"""

import os
import pathlib
import tempfile
import shutil

import pytest

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)


@pytest.fixture()
def sample_package():
    # Creates a sample python package with subdirectories
    try:
        example_src_file = pathlib.Path(get_sample_file('example.py'))

        # Create a temporary directory
        tmp_dir = tempfile.TemporaryDirectory()
        tmp_path = pathlib.Path(tmp_dir.name).resolve()

        (tmp_path / '__init__.py').touch()  # Make the directory a python package

        # Some folder containing internal data
        (tmp_path / 'data').mkdir()
        (tmp_path / 'data' / 'sample_data.csv').write_text("\n")

        # Source Files on the main level
        shutil.copy(example_src_file, tmp_path / 'pyfile.py')
        (tmp_path / 'Makefile').write_text("\n")
        (tmp_path / 'extension.cpp').write_text("\n")

        # Subdir with code
        (tmp_path / 'subproj').mkdir()
        shutil.copy(example_src_file, tmp_path / 'subproj' /'main.py')
        shutil.copy(example_src_file, tmp_path / 'subproj' /'help.py')

        # Nested dir (package) with files
        (tmp_path / 'src').mkdir()
        (tmp_path / 'src' / 'ext').mkdir()
        (tmp_path / 'src' / 'ext' / '__init__.py').write_text("\n")
        (tmp_path / 'src' / 'ext' / 'ext.c').write_text("\n")
        shutil.copy(example_src_file, tmp_path / 'src' / 'ext' / 'ext.py')

        yield tmp_path

    finally:
        tmp_dir.cleanup()  # Remove everything at end.

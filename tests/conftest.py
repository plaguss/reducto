"""
Contains functions useful on different testing modules.
"""

import os

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA = os.path.join(PARENT_DIR, 'data')


def get_sample_file(name: str) -> str:
    return os.path.join(SAMPLE_DATA, name)

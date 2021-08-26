.. reducto documentation master file, created by
   sphinx-quickstart on Wed Aug 25 20:56:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reducto Command Line Interface
==============================

The code is expected to be executed from the terminal, using
*reducto* command. Only the *target* argument is mandatory (otherwise
it will try to execute on the current working directory, and raise
an error if is not a python package).


Arguments and Options
---------------------

.. program:: reducto

.. option:: reducto <TARGET>

   Target path to execute the program. Must be either a python package (a
   directory containing an __init__.py file) or a python source file <SRC.py>.
   If a directory is not a python package or a file is not a python source
   file, a reducto.package.PackageError or reducto.src.SourceFileError
   would be raised respectively.

.. option::  -v, --version

   TBD: Show the version in use.

.. option:: -f, --format <format>

   Format for the reports. Currently only *json* is available.

.. option:: --grouped, --ungrouped

   Whether to report the data for the whole package (--grouped) or splitted
   by source file (--ungrouped). Defaults to --grouped.
   These are mutually exclusive arguments, only one can be chosen.

   An example for the --ungrouped option is as follows:

.. code-block:: json

   {
    "reducto": {
        "reducto/__init__.py": {
            "lines": 5,
            "number_of_functions": 0,
            "average_function_length": 0,
            "docstring_lines": 1,
            "comment_lines": 0,
            "blank_lines": 2,
            "source_lines": 2
        },
        "reducto/reducto.py": {
            "lines": 209,
            ...
        },
        ...
   }


.. option:: -o, --output <OUTPUT_FILE>

   Full path for the report to be written. Defaults to
   the current working directory, and the file named would be named
   reducto_report.json

.. option:: -h, --help

   Show help on the command-line interface.


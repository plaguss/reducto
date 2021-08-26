.. reducto documentation master file, created by
   sphinx-quickstart on Wed Aug 25 20:56:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Developer Guide
===============

Here resides the documentation for the reducto modules.
This may be interesting if you are curious of how it works reducto
under the hoods.

cli
---

Contains a single function which would be generated when running
*flit install* locally, or when pip installing the package.

.. automodule:: reducto.cli

.. autofunction:: reducto.cli.main

reducto
-------

Contains the class representing the application.
When the program is invoked, the code called from main is defined
in this module.

.. automodule:: reducto.reducto

.. autoclass:: reducto.reducto.Reducto
   :members:


reports
-------

This module defines the reporting facilities defined.
There are two classes, SourceReport for single files, and
PackageReport to deal with a whole package.

.. automodule:: reducto.reports

.. autoexception:: reducto.reports.ReportFormatError

.. autoclass:: reducto.reports.SourceReport
   :members:
   :noindex:

.. autoclass:: reducto.reports.PackageReport
   :members:


package
-------

Contains the code which deals with a python package traversal.
Package class parses a directory tree to obtain the python source
files, instantiating the corresponding *SourceFile*s.

.. automodule:: reducto.package

.. autoexception:: reducto.package.PackageError

.. autoclass:: reducto.package.Package
   :members:
   :noindex:

.. autofunction:: reducto.package.is_package

.. autofunction:: reducto.package.is_src_package


src
---

.. automodule:: reducto.src

.. autoexception:: reducto.src.SourceFileError

.. autoclass:: reducto.src.SourceFile
   :members:
   :noindex:

.. autofunction:: reducto.src.token_is_comment_line

.. autofunction:: reducto.src.token_is_blank_line

.. autoclass:: reducto.src.SourceVisitor
   :members:
   :noindex:


items
-----

.. automodule:: reducto.items

.. autoclass:: reducto.items.Item
   :members:
   :noindex:
   :show-inheritance:

.. autoclass:: reducto.items.FunctionDef
   :members:
   :noindex:
   :show-inheritance:

.. autoclass:: reducto.items.MethodDef
   :members:
   :show-inheritance:

.. autofunction:: reducto.items.get_docstring_lines

.. reducto documentation master file, created by
   sphinx-quickstart on Wed Aug 25 20:56:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Developer Guide
===============

Here resides the doc for the reducto modules.


CLI
---

.. automodule:: reducto.cli

.. autofunction:: reducto.cli.main


Reducto
-------

.. automodule:: reducto.reducto

.. autoclass:: reducto.reducto.Reducto
   :members:


Reports
-------

.. automodule:: reducto.reports

.. autoexception:: reducto.reports.ReportFormatError

.. autoclass:: reducto.reports.SourceReport
   :members:
   :noindex:

.. autoclass:: reducto.reports.PackageReport
   :members:


Package
-------

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


Items
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

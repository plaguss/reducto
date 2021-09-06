.. reducto documentation master file, created by
   sphinx-quickstart on Wed Aug 25 20:56:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

reducto - Python source code features in a command
==================================================

.. toctree::
   :titlesonly:

   command_line_interface
   changelog

Quickstart
----------
Hands on example

Installation
------------

To install the package, use pip, preferably inside a virtual
environment.

.. code-block::

   $ pip install reducto

reducto requires version 3.8 at least.

The extras include `tabulate <https://pypi.org/project/tabulate/>`_ to properly parse
the tables.

.. code-block::

   $ pip install reducto[tabulate]


Motivation
----------
I was looking for a toy project and remembered reading `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_
by *Kenneth Reitz & Tanya Schlusser*. In the *Chapter 5: Reading Great Code*,
there is a table titled, Common features in the example projects. A copy
of the table can be seen here:

.. image:: _static/reading_great_code_t5_1.png
   :width: 600
   :alt: reading_great_code_table5_1

I thought a package able to obtain those features and alike would be an
interesting project (at least for me at the moment), and here it is.

=========  =======  ===========  ========  ===========  =========  =======  ==========  ========
package      lines       number  source    docstring    comment    blank       average    source
                             of  lines     lines        lines      lines      function     files
                      functions                                                 length
=========  =======  ===========  ========  ===========  =========  =======  ==========  ========
reducto       1973          108  48%       41%          1%         11%               6         7
=========  =======  ===========  ========  ===========  =========  =======  ==========  ========

Some examples
-------------

The following examples are obtained from executing **reducto** on itself, for the version
1.0.0:

.. code-block::

   $ reducto --version
   reducto 1.0.0

Default behavior

.. code-block::

   $ reducto reducto
   {'reducto': {'average_function_length': 6,
                'blank_lines': 208,
                'comment_lines': 20,
                'docstring_lines': 803,
                'lines': 1973,
                'number_of_functions': 108,
                'source_files': 7,
                'source_lines': 942}}

Redirect the report to a file:

.. code-block::

   $ reducto reducto -o /home/agustin/github_repos/test_reducto/reducto_report.json
   Report generated: /home/agustin/github_repos/test_reducto/reducto_report.json

Assuming *tabulate* is installed, the reporting format accepts the formats defined for that
library, for example:

.. code-block::

   $ reducto reducto -f rst
   =========  =======  ===========  ========  ===========  =========  =======  ==========  ========
   package      lines       number    source    docstring    comment    blank     average    source
                                of     lines        lines      lines    lines    function     files
                         functions                                                 length
   =========  =======  ===========  ========  ===========  =========  =======  ==========  ========
   reducto       1973          108       942          803         20      208           6         7
   =========  =======  ===========  ========  ===========  =========  =======  ==========  ========

The results may also be reported on a *per file* basis (the default behaviour is for the
whole package grouped, --grouped):

.. code-block::

   $ reducto reducto -f rst --ungrouped
   ===================  =======  ===========  ========  ===========  =========  =======  ==========
   filename               lines       number    source    docstring    comment    blank     average
                                          of     lines        lines      lines    lines    function
                                   functions                                                 length
   ===================  =======  ===========  ========  ===========  =========  =======  ==========
   reducto/__init__.py        5            0         2            1          0        2           0
   reducto/reducto.py       239           14       147           68          4       20           8
   reducto/cli.py            20            1        10            5          0        5           5
   reducto/src.py           563           32       224          283          3       53           4
   reducto/package.py       351           20       149          157          6       39           5
   reducto/items.py         272           22       118          121          0       33           3
   reducto/reports.py       523           19       292          168          7       56          10
   ===================  =======  ===========  ========  ===========  =========  =======  ==========

This same reports can be printed in relative terms:

.. code-block::

   $ reducto reducto -f rst --ungrouped --percentage
   ===================  =======  ===========  ========  ===========  =========  =======  ==========
   filename               lines       number  source    docstring    comment    blank       average
                                          of  lines     lines        lines      lines      function
                                   functions                                                 length
   ===================  =======  ===========  ========  ===========  =========  =======  ==========
   reducto/__init__.py        5            0  40%       20%          0%         40%               0
   reducto/reducto.py       239           14  62%       28%          2%         8%                8
   reducto/cli.py            20            1  50%       25%          0%         25%               5
   reducto/src.py           563           32  40%       50%          1%         9%                4
   reducto/package.py       351           20  42%       45%          2%         11%               5
   reducto/items.py         272           22  43%       44%          0%         12%               3
   reducto/reports.py       523           19  56%       32%          1%         11%              10
   ===================  =======  ===========  ========  ===========  =========  =======  ==========

Or just for a single file:

.. code-block::

   $ reducto reducto/items.py -f rst --ungrouped --percentage
   =========  =======  ===========  ========  ===========  =========  =======  ==========
   package      lines       number  source    docstring    comment    blank       average
                                of  lines     lines        lines      lines      function
                         functions                                                 length
   =========  =======  ===========  ========  ===========  =========  =======  ==========
   items.py       272           22  43%       44%          0%         12%               3
   =========  =======  ===========  ========  ===========  =========  =======  ==========

The API Documentation
---------------------

In case you are wondering anything about the source code, watch here.

.. toctree::
   :maxdepth: 2

   developer_guide


About the title
---------------
I'm a Harry Potter fan and the name can be cast as a spell.

Its a simple command line interface that reduces the content
of the python source code to a bunch of simple measures.

It must be a name which didn't exist on PyPI, so... reducto it is.

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

Motivation
----------
I was watching for a toy project and remembered reading `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/>`_
by *Kenneth Reitz & Tanya Schlusser*. In the *Chapter 5: Reading Great Code*,
there is a table titled, Common features in the example projects. A copy
of the table can be seen here:

.. image:: _static/reading_great_code_t5_1.png
   :width: 600
   :alt: reading_great_code_table5_1

I thought a package able to obtain those features and alike would be an
interesting project (at least for me at the moment), and here it is.

=========  =========  ============ ============= ==============  =============  ==============  =================
Package    License      Line count Source Lines   Docstrings     Comments       Blank lines     Average function
                                                  (% of lines)   (% of lines)   (% of lines)    length
=========  =========  ============ ============= ==============  =============  ==============  =================
reducto    MIT                1612           51%            35%             2%             12%                  5
=========  =========  ============ ============= ==============  =============  ==============  =================

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

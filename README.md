# Reducto

**Reducto** is a command line utility to extract statistical features from your 
_python_ source code.

- Count the number of lines in a project (_.py files only_)
- Number of lines.
- Number of functions/methods.
- Average function length.
- Docstring lines.
- Comment lines.
- Blank lines.
- Source files.
- Source lines.

### Development status

![ci workflow](https://github.com/plaguss/reducto/actions/workflows/ci.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/plaguss/reducto/branch/main/graph/badge.svg?token=AVKH6TS7G7)](https://codecov.io/gh/plaguss/reducto)
[![Documentation Status](https://readthedocs.org/projects/reducto/badge/?version=latest)](https://reducto.readthedocs.io/en/latest/?badge=latest)

### Installation

**reducto** is available in [PyPI](https://pypi.org/project/reducto/), run from your terminal:

    $ pip install reducto

Install with extras to print tables via [tabulate](https://pypi.org/project/tabulate/):

    $ pip install reducto[tabulate]

_Currently tested on python 3.8 only_.

### Usage

To start with the default example:

    $ reducto {source_file_or_directory}

The default mode will print the base `json` report to the command line using `pprint.pprint`.

Let's see an example running on the reducto source code (for the current version):

```sh
$ reducto reducto
{'reducto': {'average_function_length': 6,
             'blank_lines': 208,
             'comment_lines': 20,
             'docstring_lines': 803,
             'lines': 1973,
             'number_of_functions': 108,
             'source_files': 7,
             'source_lines': 942}}
```

The formats include `json` as a default, but when installing _tabulate_ dependency,
the formats defined there are available too. For example:

```sh
$ reducto reducto --format="rst"
=========  =======  ===========  ========  ===========  =========  =======  ==========  ========
package      lines       number    source    docstring    comment    blank     average    source
                             of     lines        lines      lines    lines    function     files
                      functions                                                 length
=========  =======  ===========  ========  ===========  =========  =======  ==========  ========
reducto       1973          108       942          803         20      208           6         7
=========  =======  ===========  ========  ===========  =========  =======  ==========  ========
```

Or copying directly the output from executing `reducto reducto/ --format "github" --percentage`
to this README.md:

| package   |   lines |   number_of_functions | source_lines   | docstring_lines   | comment_lines   | blank_lines   |   average_function_length |   source_files |
|-----------|---------|-----------------------|----------------|-------------------|-----------------|---------------|---------------------------|----------------|
| reducto   |    1973 |                   108 | 48%            | 41%               | 1%              | 11%           |                         6 |              7 |

Typing the help command may show the different formats defined currently, but for more
info, the [documentation](#Documentation) may be more helpful.

```sh
$ reducto --help
usage: reducto [-h] [-v]
               [-f {json,simple,plain,grid,fancy_grid,github,pipe,orgtbl,jira,presto,pretty,psql,rst,mediawiki,moinmoin,youtrack,html,unsafehtml,latex,latex_raw,latex_booktabs,latex_longtable,tsv,textile}]
               [--grouped | --ungrouped] [-o OUTPUT] [-p]
               [target]

positional arguments:
  target                Path to execute the program into. Must be either a python package (directory containing an __init__.py) or a python source file {SRC.py}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show the version of the program.
  -f {json,simple,plain,grid,fancy_grid,github,pipe,orgtbl,jira,presto,pretty,psql,rst,mediawiki,moinmoin,youtrack,html,unsafehtml,latex,latex_raw,latex_booktabs,latex_longtable,tsv,textile}, --format {json,simple,plain,grid,fancy_grid,github,pipe,orgtbl,jira,presto,pretty,psql,rst,mediawiki,moinmoin,youtrack,html,unsafehtml,latex,latex_raw,latex_booktabs,latex_longtable,tsv,textile}
                        Format for the report type.
  --grouped             Return the results separated by source files, or grouped for the whole package. Only used when the target path is a package.
  --ungrouped           Opposite of --grouped.
  -o OUTPUT, --output OUTPUT
                        Full path of the report to be generated. If not given, redirects to stdout.
  -p, --percentage      Report the number of lines as percentage.

```

### Documentation

**[Read the documentation on ReadTheDocs!](https://reducto.readthedocs.io/en/latest/)**

### License

[MIT License](https://github.com/plaguss/reducto/blob/main/LICENSE)

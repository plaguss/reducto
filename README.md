# reducto

**reducto** is a command line utility to extract basic features from
your _python_ source code.

### Development status

TODO: Add badges:
- ci
- codecov
- docs

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/plaguss/reducto/branch/main/graph/badge.svg?token=AVKH6TS7G7)](https://codecov.io/gh/plaguss/reducto)


### Installation

To install **reducto**, run from your terminal:

    $ pip install reducto

Keep in mind it is tested on python 3.8.

### Usage

To start watch an example right away:

    $ reducto {source_file_or_directory}

The default mode would write the report in json format to the
current working directory, under the name of *reducto_report.json*.

Let's see an example running on the reducto source code as of the moment
of writing this:

    $ reducto reducto
    ┬─┐┌─┐┌┬┐┬ ┬┌─┐┌┬┐┌─┐
    ├┬┘├┤  │││ ││   │ │ │
    ┴└─└─┘─┴┘└─┘└─┘ ┴ └─┘
    Report generated: {PATH_TO_REDUCTO}/report_json.json

And the resulting report may contain a report like the following:

```json
{
    "reducto": {
        "lines": 1612,
        "number_of_functions": 102,
        "average_function_length": 5,
        "docstring_lines": 557,
        "comment_lines": 31,
        "blank_lines": 197,
        "source_files": 7,
        "source_lines": 827
    }
}
```

### Documentation

Watch the documentation if you are interested on different report 
possibilities or how it works.

TBD

**[Read the documentation on ReadTheDocs!](https://reducto.readthedocs.io/en/stable)**

### License

[MIT License](https://github.com/plaguss/reducto/blob/main/LICENSE)

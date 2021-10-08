"""Script to insert badges for reducto report to README.md present in the repo.

Just run from root level:

$ python readme_badges.py
"""

from typing import Dict, Union, List
import pathlib
import json
import subprocess
from string import Template

BASE_URL = r'https://img.shields.io/badge/<LABEL>-<MESSAGE>-green?logo=python&color=ffd43b'
LABEL = '<LABEL>'
MESSAGE = '<MESSAGE>'

here = pathlib.Path('.').resolve()
target = here / 'reducto'
report_name = here / 'reducto_report.json'


def generate_report(
        target_path: pathlib.Path = target,
        output_path: pathlib.Path = report_name
) -> None:
    """Generate reducto report on the project root. """
    args: List[str] = ["reducto", str(target_path), "-p", "-o", str(output_path)]
    subprocess.check_output(args)


def reducto_report(path: pathlib.Path = report_name) -> Dict[str, Union[str, int]]:
    """Read a reducto report and return the content without the package name.

    Returns
    -------
    report : Dict[str, Union[str, int]]
    """
    with open(str(path), 'r') as f:
        report = json.load(f)

    package_name: str = list(report.keys())[0]
    return report[package_name]


def generate_url(variable: str, report: Dict) -> str:
    r"""Generates the url to be requested to shields.io.

    Parameters
    ----------
    variable : str
        Variable from reducto_report.json.
    report : dict
        Report from json, with package name already filtered.

    Returns
    -------
    url : str
        URL to be requested.

    Examples
    --------
    >>> report = generate_report()
    >>> generate_url('lines', report)
    'https://img.shields.io/badge/lines-1974-green?logo=python&color=ffd43b'
    """
    label = variable
    if '%' in str(report[variable]):
        # Encode the % sign
        message = str(report[variable]) + '25'
    else:  # Left as is
        message = str(report[variable])

    return BASE_URL.replace(LABEL, label).replace(MESSAGE, message)


def get_badges(report: Dict) -> Dict[str, str]:
    """Generates badge url to be written to readme.

    Parameters
    ----------
    report : Dict
        Reducto report.

    Returns
    -------
    badges : Dict[str, str]
        Badges expressed in format to be passed to Template.substitute.

    Examples
    --------
    >>> get_badges(report)
    """
    badges = {}
    variables = [
        "lines", "source_lines", "blank_lines", "comment_lines", "docstring_lines",
        "average_function_length", "number_of_functions", "source_files"
    ]
    for variable in variables:
        url: str = generate_url(variable, report)
        badge_variable = 'badge_' + variable
        badge = rf"![{badge_variable}]({url})"
        badges[badge_variable] = badge
    return badges


def update_readme(name: str = 'READYOU.md') -> None:
    """Generates a readme file from the template in ./templates/readme_template.md.

    Parameters
    ----------
    name : str
        Name of the file.
    """
    def templated(line):
        return line.startswith('$badge_')

    report = reducto_report()
    badges = get_badges(report)

    template_file = here / 'templates' / 'readme_template.md'
    readme = here / name

    new_lines = []
    # Read template and add badges:
    try:
        file = open(template_file, 'r')
        for line in file:
            if templated(line):
                templ = Template(line)
                line = templ.substitute(badges)
            new_lines.append(line)
    except Exception as exc:
        print("Badges couldn't be added to template content.")
        raise exc
    finally:
        file.close()

    with open(str(readme), 'w') as f:
        f.writelines(new_lines)

    print('README.md generated.')


if __name__ == "__main__":

    generate_report()
    update_readme('README.md')

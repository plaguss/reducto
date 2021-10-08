"""Script to insert badges for reducto report to README.md present in the repo.

"""

from typing import Dict, Union, List
import pathlib
import json
import subprocess

here: pathlib.Path = pathlib.Path('.').resolve()
target: pathlib.Path = here / 'reducto'
report_name: pathlib.Path = here / 'reducto_report.json'


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


if __name__ == "__main__":

    generate_report()
    reducto_report()

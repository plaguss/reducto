"""Call the Command Line Interface here. """

import sys
from typing import List
from typing import Optional

from reducto import reducto


def main(argv: Optional[List[str]] = None) -> None:
    """Execute the reducto application."""
    if argv is None:
        argv = sys.argv[1:]

    app = reducto.Reducto()
    app.run(argv)

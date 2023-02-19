"""Merge all of the API spec source files into a single JSON file."""

import argparse
import json
import os
from typing import Any, Dict

import prance  # type: ignore
from prance.util.resolver import RESOLVE_FILES  # type: ignore

# Location of the spec relative to the repository root
_SPEC = 'api/openapi.yml'


def main(output: str = '.') -> None:
    """Main script method."""
    # Load top-level YAML spec
    parser = prance.ResolvingParser(_SPEC, resolve_types=RESOLVE_FILES)
    if not os.path.isdir(output):
        os.makedirs(output)
    spec: Dict[str, Any] = parser.specification  # type: ignore
    # Export as JSON
    with open(os.path.join(output, 'openapi.json'), 'w') as out:
        json.dump(spec, out, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    main(parser.parse_args().output)

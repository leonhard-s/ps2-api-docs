"""Merge all of the API spec source files into a single JSON file."""

import argparse
import json
import os
from typing import Any, Dict

import prance

# Location of the spec relative to the repository root
_SPEC = 'api/openapi.yml'


def main(output: str = '.') -> None:
    """Main script method."""
    # Load top-level YAML spec
    parser = prance.ResolvingParser(_SPEC)
    if not os.path.isdir(output):
        os.makedirs(output)
    # Export as JSON
    with open(os.path.join(output, 'openapi.json'), 'w') as out:
        spec: Dict[str, Any] = parser.specification  # type: ignore
        json.dump(spec, out, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    main(parser.parse_args().output)

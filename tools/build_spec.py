"""Merge all of the API spec source files into a single JSON file."""

import json
from typing import Any, Dict

import prance

# Location of the spec relative to the repository root
_SPEC = 'api/openapi.yml'


def main() -> None:
    """Main script method."""
    # Load top-level YAML spec
    parser = prance.ResolvingParser(_SPEC)
    # Export as JSON
    with open('openapi.json', 'w') as out:
        spec: Dict[str, Any] = parser.specification  # type: ignore
        json.dump(spec, out, indent=4)


if __name__ == '__main__':
    main()

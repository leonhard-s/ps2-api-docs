"""Merge all of the API spec source files into a single JSON file."""

import argparse
import json
import os
from typing import Any, Dict

import prance
from prance.util.resolver import RESOLVE_FILES

# Location of the spec relative to the repository root
_SPEC = 'api/openapi.yml'


def main(output: str = '.') -> None:
    """Main script method."""
    # Load top-level YAML spec
    parser = prance.ResolvingParser(_SPEC, resolve_types=RESOLVE_FILES)
    if not os.path.isdir(output):
        os.makedirs(output)
    spec: Dict[str, Any] = parser.specification  # type: ignore
    # Insert schema example references
    # NOTE: Since a link back to the main openapi.yaml file would result in the
    # reference being resolved as part of the build process, this link must be
    # created after the rest of the specification has been built.
    for data in spec['paths'].values():
        schema_props: Dict[str, Any] = (
            data['get']['responses']['200']['content']
            ['application/json']['schema']['properties'])
        datatype = list(schema_props)[0][:-5]
        schema_props[f'{datatype}_list']['items']['example'] = {
            '$ref': f'#/components/examples/{datatype}'}
    # Export as JSON
    with open(os.path.join(output, 'openapi.json'), 'w') as out:
        json.dump(spec, out, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    main(parser.parse_args().output)

"""Convert a YAML file to JSON format.

Resolves local file references using prance.
"""

import argparse
import json
import os
import prance  # type: ignore


def main(input_: str, output: str) -> None:
    """Main script entrypoint."""
    parser = prance.ResolvingParser(input_)
    spec = parser.specification  # type: ignore
    if os.path.dirname(output):
        os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(spec, file, indent=2)


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--input', default='census.yaml',
                         help='Path to the input YAML file')
    _parser.add_argument('--output', default='generated/openapi.json',
                         help='Path to the output JSON file')
    _args = _parser.parse_args()
    main(_args.input, _args.output)

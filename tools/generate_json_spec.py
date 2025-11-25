import argparse
import json
import pathlib
import prance  # type: ignore


def main(input_: pathlib.Path, output: pathlib.Path) -> None:
    parser = prance.ResolvingParser(input_.as_posix())
    spec = parser.specification  # type: ignore

    # Dump the spec to a JSON-based OpenAPI spec
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(spec, file, indent=2)


if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('input', type=pathlib.Path)
    _parser.add_argument('output', type=pathlib.Path)
    _args = _parser.parse_args()

    _input = _args.input
    _output = _args.output

    if not _input.exists() and _input.is_file():
        raise FileNotFoundError(f'Input file {_input} does not exist')

    # Check whether the given output path is a file based on the extension
    if _output.suffix != '.json':
        _output = _output / 'openapi.json'

    # Check whether the output directory exists
    if not _output.is_file():
        _output.parent.mkdir(parents=True, exist_ok=True)

    main(_input, _output)

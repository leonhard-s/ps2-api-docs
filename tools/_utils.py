"""Utility module for repository tools."""

import io
import re
import os
from typing import Any, Dict, List, Tuple

__all__ = [
    'SERVICE_ID'
]

# The service ID to use for any API interactions. Must be specified for
# utilities to not get rate limited.
SERVICE_ID = os.environ.get('SERVICE_ID', 's:example')

# Pattern used to replace expressions in the template YAML
_PATTERN = re.compile('(\\${{ ?(\\w+?) ?}})')


def process_placeholders(template: List[str],
                         expressions: Dict[str, Any]) -> io.StringIO:
    """Replace YAML placeholders with the given expressions.

    This uses the same expression syntax as GitHub actions. The
    following substrings will be repaced by the corresponding entry in
    the `expressions` mapping:

        ${{expression}}
        ${{ expression }}
    """
    buffer = io.StringIO()
    for line in template:
        expression: Tuple[str, str]
        for expression in _PATTERN.findall(line):
            placeholder, key = expression
            try:
                line = line.replace(placeholder, expressions[key])
            except KeyError:
                pass
        buffer.write(line)
    buffer.seek(0)
    return buffer

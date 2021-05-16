"""Utility module for repository tools."""

import os

__all__ = [
    'SERVICE_ID'
]

# The service ID to use for any API interactions. Must be specified for
# utilities to not get rate limited.
SERVICE_ID = os.environ.get('SERVICE_ID', 's:example')

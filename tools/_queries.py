"""Utility module containing helper methods for navigating the API."""

from typing import List, cast

import auraxium
from auraxium import census
from auraxium.types import CensusData

__all__ = [
    'get_collections',
    'get_fields',
    'guess_fields_required'
]


async def get_collections(game: str, client: auraxium.Client) -> List[str]:
    """Return the list of collections for the given game."""
    query = census.Query(None, game, client.service_id)
    payload = await client.request(query)
    if not payload:
        raise RuntimeError('Collection list is empty')
    results = cast(List[CensusData], payload['datatype_list'])
    return sorted([str(r['name']) for r in results])

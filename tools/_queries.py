"""Utility module containing helper methods for navigating the API."""

from typing import Any, Dict, List, Type, cast

import auraxium
from auraxium import census
from auraxium.types import CensusData

__all__ = [
    'get_collections',
    'get_fields',
    'guess_fields_required'
]

# List of tables for which to hard-code a character ID. This is both to ensure
# the data is interesting, but also so we know it's someone who doesn't care
# about being in the docs.
_REQUIRE_CHARID = [
    'character',
    'character_name',
    'characters_achievement',
    'characters_currency',
    'characters_directive',
    'characters_directive_tier',
    'characters_directive_objective',
    'characters_directive_tree',
    'characters_friend',
    'characters_item',
    'characters_event',
    'characters_event_grouped',
    'characters_leaderboard',
    'characters_online_status',
    'characters_skill',
    'characters_stat',
    'characters_stat_by_faction',
    'characters_stat_history',
    'characters_weapon_stat',
    'characters_weapon_stat_by_faction',
    'characters_world',
    'outfit_member',
    'outfit_member_extended',
    'single_character_by_id'
]


def amend_query(query: census.Query, table: str) -> None:
    """Insert extra keys to make non-standard tables work properly."""
    if table in _REQUIRE_CHARID:
        query.add_term('character_id', 5428072203494645969)
        if table == 'characters_leaderboard':
            query.add_term('name', 'Kills')
            query.add_term('period', 'Forever')
    elif table == 'map':
        query.add_term('world_id', 13)
        query.add_term('zone_ids', 2)
    elif table == 'leaderboard':
        query.add_term('name', 'Score')
        query.add_term('period', 'OneLife')
    elif table == 'event':
        query.add_term('type', 'VEHICLE_DESTROY')


async def get_fields(table: str, game: str, client: auraxium.Client,
                     include_null: bool = False, **kwargs: Any) -> List[str]:
    """Return the list of fields for a given collection.

    Nested objects will be resolved via dot notation, i.e. `name.first`
    or `description.en`. Only a single level of nested keys will be
    considered.

    Check for the existence of a dot character to determine whether a
    given key will return an inner object.
    """
    query = census.Query(table, game, client.service_id, **kwargs)
    amend_query(query, table)
    if include_null:
        query.include_null(True)
    try:
        payload = await client.request(query)
    except auraxium.errors.ServerError:
        print('Unable to fetch field list for collection '
              f'"{game}/{table}": server error')
        return []
    results = cast(List[CensusData], payload[f'{table}_list'])
    if not results:
        print('Unable to fetch field list for collection '
              f'"{game}/{table}": table is empty')
        return []
    first: Dict[str, Any] = results[0]
    fields: List[str] = []
    for key, value in first.items():
        if hasattr(value, 'keys'):
            for inner in value.keys():
                fields.append(f'{key}.{inner}')
        else:
            fields.append(key)
    return fields


async def get_collections(game: str, client: auraxium.Client) -> List[str]:
    """Return the list of collections for the given game."""
    query = census.Query(None, game, client.service_id)
    payload = await client.request(query)
    if not payload:
        raise RuntimeError('Collection list is empty')
    results = cast(List[CensusData], payload['datatype_list'])
    return sorted([str(r['name']) for r in results])


async def guess_fields_required(table: str, game: str,
                                client: auraxium.Client) -> Dict[str, bool]:
    """Guess what fields of a collection are required.

    This compares the number of entries in a collection with the number
    of non-NULL entries for a given field.
    """
    base_query = census.Query(table, game, client.service_id)
    amend_query(base_query, table)
    try:
        payload = await client.request(base_query, verb='count')
    except auraxium.errors.ServerError:
        print('Unable to guess required fields for collection '
              f'"{game}/{table}": server error')
        return {}
    total = int(str(payload['count']))
    field_mapping: Dict[str, bool] = {}
    for field in await get_fields(table, game, client, include_null=True):
        field_query = census.Query.copy(base_query).has(field)
        try:
            payload = await client.request(field_query, verb='count')
        except auraxium.errors.InvalidSearchTermError:
            field_mapping[field] = True
            print('Unable to guess required fields for collection '
                  f'"{game}/{table}": invalid search term, assuming required')
            continue
        filtered = int(str(payload['count']))
        field_mapping[field] = total == filtered
    return field_mapping


async def guess_fields_type(table: str, game: str,
                            client: auraxium.Client) -> Dict[str, str]:
    """Guess the types for a given field.

    This fetches up to 5000 distinct entries as possible before
    checking for the broadest applicable type.
    """
    types: Dict[str, str] = {}
    for field in await get_fields(table, game, client, include_null=True):
        types[field] = 'unknown'
        if '.' in field:
            types[field] = 'object'
            continue
        query = census.Query(table, game, client.service_id)
        amend_query(query, table)
        query.distinct(field)
        query.has(field)
        query.limit(5000)
        try:
            payload = await client.request(query)
        except auraxium.errors.ServerError:
            print(f'Unable to guess type of field "{field}" for collection '
                  f'"{game}/{table}": server error')
            continue
        entries = cast(
            List[Dict[str, List[Any]]], payload[f'{table}_list'])
        if not entries:
            print(f'Unable to guess type of field "{field}" for collection '
                  f'"{game}/{table}": field unused')
            continue
        if table == 'characters_friend':
            # This table returns a non-standard payload and must be processed
            # separately
            print(f'Unable to guess type of field "{field}" for collection '
                  f'"{game}/{table}": blacklisted table')
            continue
        values = entries[0][field]
        # Guess the type of the field
        guesses: Dict[Type[Any], bool] = {
            int: True, float: True, bool: True, str: True}
        for value in values:
            value = str(value)
            if guesses[int]:
                try:
                    _ = int(value)
                except ValueError:
                    guesses[int] = False
            if guesses[float]:
                try:
                    _ = float(value)
                except ValueError:
                    guesses[float] = False
            if guesses[bool]:
                if value.lower() not in ('false', 'true'):
                    guesses[bool] = False
        if guesses[bool]:
            types[field] = 'boolean'
        elif guesses[int]:
            types[field] = 'integer'
        elif guesses[float]:
            types[field] = 'number'
        else:
            types[field] = 'string'
    return types

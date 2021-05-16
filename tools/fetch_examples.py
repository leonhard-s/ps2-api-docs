"""A script for retrieving example payloads for all collections.

This script first checks the PS2 namespace for the list of collections
before retrieving example payloads from each. For non-standard tables,
this will insert required IDs to produce sensible responses.

When run from the repository root, this script will automatically place
all retrieved examples into the `api/components/examples` subfolder as
required by the OpenAPI specification of the repo.
"""

import asyncio
import json
from typing import Any, Coroutine, List, TYPE_CHECKING

import auraxium
from auraxium import census
from auraxium.types import CensusData

# Slightly sketchy double-import to appease Pylance
if TYPE_CHECKING:
    from ._queries import get_collections
    from ._utils import SERVICE_ID
else:
    from _queries import get_collections
    from _utils import SERVICE_ID

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


async def main(game: str) -> None:
    """Main script method."""

    async with auraxium.Client(service_id=SERVICE_ID) as client:
        print('Fetching collections...')
        collections = await get_collections(game, client)
        print(f'Found {len(collections)} tables in namespace {game}\n'
              'Generating requests...')
        tasks: List[Coroutine[Any, Any, List[CensusData]]] = []
        for table in collections:
            query = census.Query(table, game, client.service_id)
            print(query)
            # The following elif chain handles non-standard tables that require
            # a parameter to return real data.
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
            # Create a copy of the query with NULL fields included
            query_null = census.Query.copy(query).include_null(True)

            async def worker(*queries: census.Query) -> List[CensusData]:
                return [await client.request(q) for q in queries]

            tasks.append(worker(query, query_null))
        print(tasks)
        print('Fetching examples...')
        results = await asyncio.gather(*tasks)
        print('Writing examples...')
        for result in results:
            # Retrieve name of collection
            for field in result[0]:
                if field.endswith('_list'):
                    table = field.rsplit('_', maxsplit=1)[0]
                    break
            else:
                raise RuntimeError(
                    f'Unable to determine collection of payload: {result}')
            # Discard the second example if the two are identical
            if result[0] == result[1]:
                result = [result[0]]
            # Write pretty-print JSON to disk
            with open(f'api/components/examples/{table}.json', 'w') as file_:
                json.dump(result, file_, indent=4)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('ps2:v2'))

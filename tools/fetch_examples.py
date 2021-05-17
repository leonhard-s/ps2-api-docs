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
    from ._queries import amend_query, get_collections
    from ._utils import SERVICE_ID
else:
    from _queries import amend_query, get_collections
    from _utils import SERVICE_ID


async def main(game: str) -> None:
    """Main script method."""

    async with auraxium.Client(service_id=SERVICE_ID) as client:
        print('Fetching collections...')
        tables = await get_collections(game, client)
        print(f'Found {len(tables)} tables in namespace {game}\n'
              'Generating requests...')
        tasks: List[Coroutine[Any, Any, List[CensusData]]] = []
        for table in tables:
            query = census.Query(table, game, client.service_id)
            # Feed non-standard tables extra parameters to return real data.
            amend_query(query, table)
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

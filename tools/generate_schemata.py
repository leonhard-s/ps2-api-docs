"""A script for generating payload schemata from a template.

This script fetches a list of all collections before processing each to
determine its required fields and guessing the field type.

A few notes on the guessed types:

- Fields that are unused will be typed as `unknown`
- Nested keys are typed as `object` and require manual introspection
"""

import asyncio
from typing import Dict, List, TYPE_CHECKING

import auraxium

# Slightly sketchy double-import to appease Pylance
if TYPE_CHECKING:
    from ._queries import (get_collections, get_fields, guess_fields_required,
                           guess_fields_type)
    from ._utils import SERVICE_ID, process_placeholders
else:
    from _queries import (get_collections, get_fields, guess_fields_required,
                          guess_fields_type)
    from _utils import SERVICE_ID, process_placeholders


async def main(game: str) -> None:
    """Main script method."""
    async with auraxium.Client(service_id=SERVICE_ID) as client:
        # Mapping of collections to fields to field info
        field_info: Dict[str, Dict[str, Dict[str, str]]] = {}
        for collection in await get_collections(game, client):
            collection_info: Dict[str, Dict[str, str]] = {}
            # Get field data
            fields_required = await guess_fields_required(
                collection, game, client)
            fields_types = await guess_fields_type(collection, game, client)
            # Get list of fields
            for field in await get_fields(
                    collection, game, client, include_null=True):
                collection_info[field] = {
                    'required': 'true' if fields_required[field] else 'false',
                    'type': fields_types[field]}
            field_info[collection] = collection_info
    # Load templates
    with open('templates/schema.yml') as template_file:
        template: List[str] = []
        template_fields: List[str] = []
        scrape_field = False
        for line in template_file:
            if line.strip() == 'properties:':
                scrape_field = True
                template.append(line)
                continue
            if scrape_field:
                template_fields.append(line)
            else:
                template.append(line)
    # Generate schemata
    for collection, fields in field_info.items():
        with open(f'api/components/schemas/{collection}.yml', 'w') as schema:
            schema.writelines(process_placeholders(
                template, {'datatype': collection}))
            for field, info in fields.items():
                schema.writelines(process_placeholders(
                    template_fields, {'field': field, **info}))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('ps2:v2'))

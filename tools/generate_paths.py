"""A script for generating path items from a template."""

import asyncio
from typing import TYPE_CHECKING

import auraxium

# Slightly sketchy double-import to appease Pylance
if TYPE_CHECKING:
    from ._queries import get_collections
    from ._utils import SERVICE_ID, process_placeholders
else:
    from _queries import get_collections
    from _utils import SERVICE_ID, process_placeholders


async def main(game: str) -> None:
    """Main script method."""
    # Get collections
    async with auraxium.Client(service_id=SERVICE_ID) as client:
        expressions = [
            {'datatype': c} for c in await get_collections(game, client)]
    # Load templates
    with open('templates/path.yml') as template_file:
        template = template_file.readlines()
    # Generate path items
    for variables in expressions:
        datatype = variables['datatype']
        # "get" query verb
        with open(f'api/paths/get_{datatype}.yml', 'w') as path_item:
            path_item.writelines(
                process_placeholders(template, variables))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('ps2:v2'))

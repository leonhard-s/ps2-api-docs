# PS2 API Docs

Unofficial OpenAPI specification and documentation provider for the PlanetSide 2 API.

***

This repository maintains a full list of all collections in the [PlanetSide 2 API](https://census.daybreakgames.com/). Currently, only the REST endpoint is documented. A WebSocket API reference may be added in a later version.

## API Preview

An HTML version of this specification is automatically built using [ReDoc](https://github.com/Redocly/redoc) and hosted [at this location](https://ps2-api-docs.readthedocs.io/en/latest/openapi.html).

## Usage

This repository defines the API endpoints according to the [OpenAPI 3.1](https://swagger.io/specification/) speficiation, which manifests itself as a YAML or JSON document defining available server endpoints, paths/routes, schemata and example payloads.

If your use case does not support multi-file OpenAPI documents or you are restricted to a single file, you can use the [single-file JSON version](https://raw.githubusercontent.com/leonhard-s/ps2-api-docs/main/generated/openapi.json). This is also the file used to generate the HTML preview linked above.

> **Note:** Please be aware that the generated spec is not yet stable and may change in the future (see [#9](https://github.com/leonhard-s/ps2-api-docs/issues/9) for details).

### Extensions

> **Note:** Vendor extensions are not yet finalized and may change in the near future. See [#7](https://github.com/leonhard-s/ps2-api-docs/issues/7) for details.

The OpenAPI standard allows the insertion of custom fields into the standard. These fields are prefixed with `x-` and listed below:

- **`x-cast-to`**

  The Census API returns most values as strings. This field defines the type to which the value should be cast. Note that casting to boolean requires special handling of the strings `"0"` and `"NULL"`, which may be interpreted as truthy values in some languages such as Python.

- **`x-reference-to`**

  For ID fields, this field defines the qualified names of a collection that can be joined to this field as an array of strings.

  For example, the property `outfit.leader_character_id` has the value `character.character_id` in its `x-reference-to` list.

  This field may be used to dynamically create or validate joins to related data.

## Contributing

Contributions of any form are always appreciated and vital to the project, be it corrections, more specific examples, edge cases or other improvements.

If you are unfamiliar with the OpenAPI syntax, feel free to just create an issue with your changes and have someone else sort it out.

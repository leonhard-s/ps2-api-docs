# PS2 API Docs

Unofficial OpenAPI specification and documentation provider for the PlanetSide 2 API.

> ## Update Notice
>
> This project is currently being updated for OpenAPI 3.1, including improved documentation of query commands, parameters, and response variants.
>
> The previous version can be found on the [`develop`](https://github.com/leonhard-s/ps2-api-docs/tree/develop) branch.

***

This repository maintains a full list of all collections in the [PlanetSide 2 API](https://census.daybreakgames.com/). Currently, only the REST endpoint is documented. A WebSocket API reference may be added in a later version.

## Usage

This repository defines the API endpoints according to the [OpenAPI 3.1](https://swagger.io/specification/) speficiation, which manifests itself as a JSON document defining available server endpoints, paths/routes, schemata and example payloads.

An HTML version of this specification is automatically built using [ReDoc](https://github.com/Redocly/redoc) and hosted [here](https://ps2-api-docs.readthedocs.io/en/latest/openapi.html).
<!-- 
Alternatively, you can build the latest version of the specification by cloning this repository and running the `tools/build_spec.py` script. This option is recommended for CI/CD setups as it will always use the latest version of the specification. -->

<!-- ## Details

### A note regarding types

According to the OpenAPI standard, a quoted integer (e.g. `"12"`) should be typed as a `string`.
However, due to the PS2 API quoting nearly every value it returns, following this convention would make the type hints meaningless.

Code consuming API payloads should always expect strings in addition to the documented type. If you are using the `c:includeNull` query command, you may also need a special case to parse the string `"NULL"` as your coding environment's NULL type.

### Extensions

The OpenAPI standard allows the insertion of custom fields into the standard. These fields are prefixed with `x-` and listed below:

- **`x-reference-to`**

  For ID-type properties, this field defines the qualified names of collections that can be joined to this field as an array of strings.

  For example, the property `outfit.leader_character_id` has the value `character.character_id` in its `x-reference-to` list.

  This field may be used to dynamically create or validate joins to related data. -->

## Contributing

Contributions of any form are always appreciated and vital to the project, be it corrections, more specific examples, edge cases or other improvements.

If you are unfamiliar with the OpenAPI syntax, feel free to just create an issue with your changes and have someone else sort it out.

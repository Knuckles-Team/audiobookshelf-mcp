---
name: audiobookshelf-library-management
skill_type: skill
description: >-
  Create and maintain libraries, scan them, and read their items, series, authors and
  statistics. Do NOT use for tasks outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf libraries

Use the typed tools of the `audiobookshelf-mcp` connector: one tool per upstream API operation, named `audiobookshelf_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **audiobookshelf-libraries** (`AUDIOBOOKSHELF_URL`): holds Library; read with `audiobookshelf_get_libraries`.
- **audiobookshelf-items** (`AUDIOBOOKSHELF_URL`): holds MediaAsset; read with `audiobookshelf_get_library_items`.
- **audiobookshelf-authors** (`AUDIOBOOKSHELF_URL`): holds Person; read with `audiobookshelf_get_library_authors`.
- **audiobookshelf-episodes** (`AUDIOBOOKSHELF_URL`): holds MediaAsset; read with `audiobookshelf_get_library_recent_episodes`.
- **audiobookshelf-collections** (`AUDIOBOOKSHELF_URL`): holds Collection; read with `audiobookshelf_get_collections`.
- **audiobookshelf-sessions** (`AUDIOBOOKSHELF_URL`): holds ListeningSession; read with `audiobookshelf_get_sessions`.
- **audiobookshelf-users** (`AUDIOBOOKSHELF_URL`): holds Person; read with `audiobookshelf_get_users`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `audiobookshelf-manage-library`

1. `audiobookshelf_get_libraries` (no parameters) - Get libraries.
2. `audiobookshelf_get_library_by_id` (`id`, `include`) - Get library by id.
3. `audiobookshelf_create_library` (`body`) - Create library.
4. `audiobookshelf_order_libraries` (`body`) - Order libraries.
5. `audiobookshelf_update_library_by_id` (`id`, `params_json`) - Update library by id.
6. `audiobookshelf_delete_library_by_id` (`confirm`, `id`) - Delete library by id. (destructive: ask the operator first)
7. `audiobookshelf_delete_library_issues` (`confirm`, `id`) - Delete library issues. (destructive: ask the operator first)

### `audiobookshelf-inspect-library-authors`

1. `audiobookshelf_get_library_authors` (`id`) - Get library authors.

### `audiobookshelf-manage-library-items`

1. `audiobookshelf_get_library_filter_data` (`id`) - Get library filter data.
2. `audiobookshelf_get_library_items` (`id`, `params_json`) - Get library items.
3. `audiobookshelf_get_library_personalized` (`id`, `include`, `limit`) - Get library personalized.
4. `audiobookshelf_search_library` (`id`, `limit`, `q`) - Search library.
5. `audiobookshelf_match_all_library_items` (`id`) - Match all library items.
6. `audiobookshelf_scan_library` (`force`, `id`) - Scan library.
7. `audiobookshelf_remove_library_items_with_issues` (`confirm`, `id`) - Remove library items with issues. (destructive: ask the operator first)

### `audiobookshelf-inspect-library-series`

1. `audiobookshelf_get_library_series` (`id`, `params_json`) - Get library series.
2. `audiobookshelf_get_library_series_by_id` (`id`, `series_id`) - Get library series by id.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

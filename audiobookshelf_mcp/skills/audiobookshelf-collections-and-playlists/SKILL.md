---
name: audiobookshelf-collections-and-playlists
skill_type: skill
description: >-
  Curate collections of books and per-user playlists of items. Do NOT use for tasks
  outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf collections and playlists

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

### `audiobookshelf-manage-collection`

1. `audiobookshelf_get_collection` (`id`) - Get collection.
2. `audiobookshelf_get_collections` (no parameters) - Get collections.
3. `audiobookshelf_get_library_collections` (`filter`, `id`, `limit`, `minified`, `page`, `sort`) - Get library collections.
4. `audiobookshelf_add_book_to_collection` (`body`, `id`) - Add book to collection.
5. `audiobookshelf_batch_add_books_to_collection` (`body`, `id`) - Batch add books to collection.
6. `audiobookshelf_create_collection` (`body`) - Create collection.
7. `audiobookshelf_create_playlist_from_collection` (`collection_id`) - Create playlist from collection.
8. `audiobookshelf_update_collection` (`body`, `id`) - Update collection.
9. `audiobookshelf_batch_remove_books_from_collection` (`body`, `confirm`, `id`) - Batch remove books from collection. (destructive: ask the operator first)
10. `audiobookshelf_delete_collection` (`confirm`, `id`) - Delete collection. (destructive: ask the operator first)
11. `audiobookshelf_remove_book_from_collection` (`book_id`, `confirm`, `id`) - Remove book from collection. (destructive: ask the operator first)

### `audiobookshelf-manage-playlist`

1. `audiobookshelf_get_library_playlists` (`id`, `limit`, `page`) - Get library playlists.
2. `audiobookshelf_get_playlist` (`id`) - Get playlist.
3. `audiobookshelf_get_playlists` (no parameters) - Get playlists.
4. `audiobookshelf_add_item_to_playlist` (`body`, `id`) - Add item to playlist.
5. `audiobookshelf_batch_add_items_to_playlist` (`body`, `id`) - Batch add items to playlist.
6. `audiobookshelf_create_playlist` (`body`) - Create playlist.
7. `audiobookshelf_update_playlist` (`body`, `id`) - Update playlist.
8. `audiobookshelf_batch_remove_items_from_playlist` (`body`, `confirm`, `id`) - Batch remove items from playlist. (destructive: ask the operator first)
9. `audiobookshelf_delete_playlist` (`confirm`, `id`) - Delete playlist. (destructive: ask the operator first)
10. `audiobookshelf_remove_item_from_playlist` (`confirm`, `id`, `library_item_id`) - Remove item from playlist. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

---
name: audiobookshelf-item-catalog
skill_type: skill
description: >-
  Read and edit library items, covers, chapters, metadata and files, and maintain authors,
  series, genres and tags. Do NOT use for tasks outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf items, authors and series

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

### `audiobookshelf-manage-author`

1. `audiobookshelf_get_author_by_id` (`id`, `params_json`) - Get author by id.
2. `audiobookshelf_get_author_image_by_id` (`id`, `params_json`) - Get author image by id.
3. `audiobookshelf_search_authors` (`q`) - Search authors.
4. `audiobookshelf_add_author_image_by_id` (`id`, `params_json`) - Add author image by id.
5. `audiobookshelf_match_author_by_id` (`id`, `params_json`, `q`) - Match author by id.
6. `audiobookshelf_update_author_by_id` (`id`, `params_json`) - Update author by id.
7. `audiobookshelf_update_author_image_by_id` (`id`, `params_json`) - Update author image by id.
8. `audiobookshelf_delete_author_by_id` (`confirm`, `id`) - Delete author by id. (destructive: ask the operator first)
9. `audiobookshelf_delete_author_image_by_id` (`confirm`, `id`) - Delete author image by id. (destructive: ask the operator first)

### `audiobookshelf-manage-item`

1. `audiobookshelf_batch_get_items` (`body`) - Batch get items.
2. `audiobookshelf_get_item` (`episode`, `expanded`, `id`, `include`) - Get item.
3. `audiobookshelf_get_item_cover` (`format`, `height`, `id`, `raw`, `width`) - Get item cover.
4. `audiobookshelf_get_item_ffprobe` (`file_id`, `id`) - Get item ffprobe.
5. `audiobookshelf_get_item_tone_object` (`id`) - Get item tone object.
6. `audiobookshelf_send_ebook_to_device` (`body`) - Send ebook to device.
7. `audiobookshelf_upload_item_cover` (`body`, `id`) - Upload item cover.
8. `audiobookshelf_batch_embed_metadata` (`body`) - Batch embed metadata.
9. `audiobookshelf_batch_quickmatch_items` (`body`) - Batch quickmatch items.
10. `audiobookshelf_batch_scan_items` (`body`) - Batch scan items.
11. `audiobookshelf_batch_update_items` (`body`) - Batch update items.
12. `audiobookshelf_embed_item_metadata` (`backup`, `force_embed_chapters`, `id`) - Embed item metadata.
13. `audiobookshelf_encode_item_m4b` (`bitrate`, `channels`, `codec`, `id`, `token`) - Encode item m4b.
14. `audiobookshelf_match_item` (`body`, `id`) - Match item.
15. `audiobookshelf_scan_item` (`id`) - Scan item.
16. `audiobookshelf_update_item_chapters` (`body`, `id`) - Update item chapters.
17. `audiobookshelf_update_item_cover` (`body`, `id`) - Update item cover.
18. `audiobookshelf_update_item_media` (`body`, `id`) - Update item media.
19. `audiobookshelf_batch_delete_items` (`body`, `confirm`, `hard`) - Batch delete items. (destructive: ask the operator first)
20. `audiobookshelf_cancel_item_m4b_encode` (`confirm`, `id`) - Cancel item m4b encode. (destructive: ask the operator first)
21. `audiobookshelf_delete_item` (`confirm`, `hard`, `id`) - Delete item. (destructive: ask the operator first)
22. `audiobookshelf_delete_item_cover` (`confirm`, `id`) - Delete item cover. (destructive: ask the operator first)
23. `audiobookshelf_delete_item_file` (`confirm`, `file_id`, `id`) - Delete item file. (destructive: ask the operator first)

### `audiobookshelf-manage-metadata`

1. `audiobookshelf_get_genres` (no parameters) - Get genres.
2. `audiobookshelf_get_tags` (no parameters) - Get tags.
3. `audiobookshelf_search_books` (`author`, `isbn`, `provider`, `title`) - Search books.
4. `audiobookshelf_search_chapters` (`asin`, `region`) - Search chapters.
5. `audiobookshelf_search_covers` (`author`, `provider`, `title`) - Search covers.
6. `audiobookshelf_rename_genre` (`body`) - Rename genre.
7. `audiobookshelf_rename_tag` (`body`) - Rename tag.
8. `audiobookshelf_delete_genre` (`confirm`, `genre`) - Delete genre. (destructive: ask the operator first)
9. `audiobookshelf_delete_tag` (`confirm`, `tag`) - Delete tag. (destructive: ask the operator first)

### `audiobookshelf-manage-series`

1. `audiobookshelf_get_series` (`id`, `params_json`) - Get series.
2. `audiobookshelf_update_series` (`id`, `params_json`) - Update series.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

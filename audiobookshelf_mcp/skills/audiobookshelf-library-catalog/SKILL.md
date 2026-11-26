---
name: audiobookshelf-library-catalog
skill_type: skill
description: >-
  Browse and manage Audiobookshelf libraries, audiobook/ebook items and series: list libraries, page items with sort/filter, read a library or series, curate metadata. Use to explore a collection, find books by author or series, or fix item metadata. Do NOT use for podcasts (audiobookshelf-podcast-manager) or KG ingestion (audiobookshelf-kg-ingestion).
license: MIT
tags: [audiobookshelf, library, audiobook, series, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Audiobookshelf Library Catalog

Scope: Browse and manage Audiobookshelf libraries, their audiobook/ebook items and series via the audiobookshelf-mcp MCP server — list libraries, page through library items with sort/filter, read a single library or series, and curate metadata. Use when the agent must explore a collection, find books by author/series, or fix item metadata. Do NOT use for podcasts (audiobookshelf-podcast-manager) or pushing the catalog into the knowledge graph (audiobookshelf-kg-ingestion).

Domain-typed access to Audiobookshelf **libraries**, **library items** (audiobooks /
ebooks) and **series** through the `audiobookshelf-mcp` MCP server. Prefer these
typed tools over raw HTTP — they carry the Audiobookshelf field conventions and
return item-shaped records.

## When to use
- List the configured libraries and inspect one by id.
- Page through the items in a library with limit/page/sort/filter.
- List the series (or authors) inside a library, or read a single series.
- Update item / series metadata.

## When NOT to use
- Podcast items, feeds, or episodes → `audiobookshelf-podcast-manager`.
- Author portrait/image upload or provider match -> `audiobookshelf_add_author_image_by_id`, `audiobookshelf_match_author_by_id`.
- Pushing the catalog into the medulla → `audiobookshelf-kg-ingestion`.
- Email / ereader / notification settings -> the `audiobookshelf_*_email_*` and `audiobookshelf_*_notification*` tools.

## Steps

1. List libraries with `audiobookshelf_get_libraries`.
   Verify the library id and its `mediaType` are as expected.
2. Page items with `audiobookshelf_get_library_items` using `limit`, `page` and `sort`.
   Verify `total` and the page number in the response.
3. Read series or one item with `audiobookshelf_get_library_series_by_id` or `audiobookshelf_get_item`.
   Verify the title and series match the request.
4. Update metadata only when asked with `audiobookshelf_update_series`.
   Verify `audiobookshelf_get_series` shows the change.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| HTTP 401 or connection error | `AUDIOBOOKSHELF_TOKEN` or `AUDIOBOOKSHELF_URL` is missing or wrong | Set both variables to a valid API token and base URL, restart the server, and confirm with `audiobookshelf_get_libraries` |
| Empty items list | The library is a podcast library or the page is past the end | Check `mediaType` from `audiobookshelf_get_libraries` and use page 0 with a small `limit` |
| 404 or empty result | The `id` is wrong or belongs to another object | Call `audiobookshelf_get_libraries` and copy the exact id from its result |

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`audiobookshelf-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `AUDIOBOOKSHELF_URL` | ✅ | Server base URL (default `http://localhost:13378`) |
| `AUDIOBOOKSHELF_TOKEN` | ✅ | Bearer API token (Config → API Keys) |
| `AUDIOBOOKSHELF_SSL_VERIFY` | optional | TLS verification toggle |

## Tools
One typed tool per API operation; pass real arguments, not JSON strings.

| Task | Tool |
|------|------|
| List / read / create / update / delete a library | `audiobookshelf_get_libraries`, `audiobookshelf_get_library_by_id`, `audiobookshelf_create_library`, `audiobookshelf_update_library_by_id`, `audiobookshelf_delete_library_by_id` |
| Browse a library | `audiobookshelf_get_library_items`, `audiobookshelf_get_library_authors`, `audiobookshelf_get_library_series`, `audiobookshelf_get_library_series_by_id`, `audiobookshelf_search_library`, `audiobookshelf_get_library_filter_data`, `audiobookshelf_get_library_stats`, `audiobookshelf_get_library_personalized` |
| Read one item | `audiobookshelf_get_item` (also `audiobookshelf_get_item_cover`) |
| Collections | `audiobookshelf_get_collections`, `audiobookshelf_get_collection`, `audiobookshelf_get_library_collections` |
| Series | `audiobookshelf_get_series`, `audiobookshelf_update_series` |

### Key parameters
- `id` - the library id (or item id for `audiobookshelf_get_item`).
- `series_id` - required for `audiobookshelf_get_library_series_by_id`.
- `audiobookshelf_get_library_items` supports `limit`, `page`, `sort`, `desc`, `filter`, `collapseseries`.

## Recipes
List all libraries: call `audiobookshelf_get_libraries` with no arguments.

Page through a library's items, newest first: `audiobookshelf_get_library_items` with
`id=<library_id>`, `limit=25`, `page=0`, `sort=addedAt`, `desc=1`.

Read one series with its books: `audiobookshelf_get_library_series_by_id` with
`id=<library_id>`, `series_id=<series_id>`.

## Gotchas
- `list` returns `{"libraries":[...]}`; `items` returns `{"results":[...],"total":N,"page":P}` — page is 0-based.
- A library is single-media-type: its `mediaType` is `book` **or** `podcast`; the
  `items` of a podcast library are podcasts, not audiobooks.
- Item metadata lives under `media.metadata` (title, authors[], series[], narratorName);
  the cover is `media.coverPath`.

## Related
- **KG ingestion:** `audiobookshelf-kg-ingestion` pushes these same libraries/items into
  the knowledge graph as typed `:Library` / `:Book` / `:Series` nodes.
- Podcast libraries: `audiobookshelf-podcast-manager`.

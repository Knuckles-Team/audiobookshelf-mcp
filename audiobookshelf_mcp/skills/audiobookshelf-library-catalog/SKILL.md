---
name: audiobookshelf-library-catalog
skill_type: skill
description: >-
  Browse and manage Audiobookshelf libraries, their audiobook/ebook items and series
  via the audiobookshelf-mcp MCP server — list libraries, page through library items
  with sort/filter, read a single library or series, and curate metadata. Use when the
  agent must explore a collection, find books by author/series, or fix item metadata.
  Do NOT use for podcasts (audiobookshelf-podcast-manager) or pushing the catalog into
  the knowledge graph (audiobookshelf-kg-ingestion).
license: MIT
tags: [audiobookshelf, library, audiobook, series, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Audiobookshelf Library Catalog

Domain-typed access to Audiobookshelf **libraries**, **library items** (audiobooks /
ebooks) and **series** through the `audiobookshelf-mcp` MCP server. Prefer these
condensed tools over raw HTTP — they carry the Audiobookshelf field conventions and
return item-shaped records.

## When to use
- List the configured libraries and inspect one by id.
- Page through the items in a library with limit/page/sort/filter.
- List the series (or authors) inside a library, or read a single series.
- Update item / series metadata.

## When NOT to use
- Podcast items, feeds, or episodes → `audiobookshelf-podcast-manager`.
- Author portrait/image upload or provider match → the raw `author_operations` tool.
- Pushing the catalog into the epistemic-graph → `audiobookshelf-kg-ingestion`.
- Email / ereader / notification settings → the raw `email_operations` /
  `notification_operations` tools.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`audiobookshelf-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `AUDIOBOOKSHELF_URL` | ✅ | Server base URL (default `http://localhost:13378`) |
| `AUDIOBOOKSHELF_TOKEN` | ✅ | Bearer API token (Config → API Keys) |
| `AUDIOBOOKSHELF_SSL_VERIFY` | optional | TLS verification toggle |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (used
below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `library_operations` | `list`, `get`, `create`, `update`, `delete`, `authors`, `items`, `series`, `series_by_id`, `delete_issues` |
| `series_operations` | `get`, `update` |

### Key parameters
- `id` — the library id (required for `get`/`items`/`series`/`authors`) or series id.
- `series_id` — required for `series_by_id`.
- `items` supports `limit`, `page`, `sort`, `desc`, `filter`, `collapseseries`.

## Recipes (`params_json`)
List all libraries:
```json
{}
```
Page through a library's items, newest first:
```json
{"id":"<library_id>","limit":25,"page":0,"sort":"addedAt","desc":1}
```
Get the series inside a library:
```json
{"id":"<library_id>"}
```
Read one series with its books:
```json
{"id":"<library_id>","series_id":"<series_id>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `list` returns `{"libraries":[...]}`; `items` returns `{"results":[...],"total":N,"page":P}` — page is 0-based.
- A library is single-media-type: its `mediaType` is `book` **or** `podcast`; the
  `items` of a podcast library are podcasts, not audiobooks.
- Item metadata lives under `media.metadata` (title, authors[], series[], narratorName);
  the cover is `media.coverPath`.

## Related
- **KG ingestion:** `audiobookshelf-kg-ingestion` pushes these same libraries/items into
  the knowledge graph as typed `:Library` / `:Book` / `:Series` nodes.
- Podcast libraries: `audiobookshelf-podcast-manager`.

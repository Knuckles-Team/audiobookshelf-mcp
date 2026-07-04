---
name: audiobookshelf-podcast-manager
description: >-
  Create and manage Audiobookshelf podcasts, their RSS feeds and episodes via the
  audiobookshelf-mcp MCP server — add a podcast from a feed URL, bulk-import from OPML,
  check for and download new episodes, manage the download queue, and read/update/remove
  episodes. Use when the agent must onboard or maintain podcasts. Do NOT use for
  audiobook/ebook libraries (audiobookshelf-library-catalog) or KG ingestion
  (audiobookshelf-kg-ingestion).
license: MIT
tags: [audiobookshelf, podcast, rss, opml, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Audiobookshelf Podcast Manager

Domain-typed access to Audiobookshelf **podcasts** and **episodes** through the
`audiobookshelf-mcp` MCP server. Prefer the condensed `podcast_operations` tool over raw
HTTP — it carries the feed/episode field conventions.

## When to use
- Add a podcast from an RSS feed URL, or bulk-create from an OPML feed / text.
- Preview a feed's episodes before adding it.
- Check for new episodes and queue them for download; inspect or clear the queue.
- Read, update, or remove an individual episode; quick-match episodes against a feed.

## When NOT to use
- Audiobook / ebook libraries and series → `audiobookshelf-library-catalog`.
- Author portrait/provider-match curation → the raw `author_operations` tool.
- Pushing podcasts into the epistemic-graph → `audiobookshelf-kg-ingestion`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`audiobookshelf-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `AUDIOBOOKSHELF_URL` | ✅ | Server base URL (default `http://localhost:13378`) |
| `AUDIOBOOKSHELF_TOKEN` | ✅ | Bearer API token (Config → API Keys) |
| `AUDIOBOOKSHELF_SSL_VERIFY` | optional | TLS verification toggle |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface vs. the
one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `podcast_operations` | `create`, `feed`, `opml_create`, `opml_parse`, `check_new`, `clear_queue`, `download_episodes`, `downloads`, `get_episode`, `update_episode`, `remove_episode`, `match_episodes`, `find_episode` |

### Key parameters
- `id` — the podcast library-item id (required for episode/queue actions).
- `episode_id` — required for `get_episode` / `update_episode` / `remove_episode`.
- `create` takes a podcast body (folder/library ids + `media.metadata.feedUrl`).
- `feed` / `opml_parse` take the feed `rssFeed` URL or `opmlText` body.

## Recipes (`params_json`)
Preview a feed before adding:
```json
{"rssFeed":"https://example.com/podcast.rss"}
```
Check for new episodes of a podcast:
```json
{"id":"<podcast_item_id>"}
```
Queue specific new episodes for download:
```json
{"id":"<podcast_item_id>","episodes":[{"episodeId":"<ep_id>"}]}
```
Read one episode:
```json
{"id":"<podcast_item_id>","episode_id":"<ep_id>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `check_new` / `clear_queue` / `downloads` are GET-style: they only need `id`.
- Downloading episodes is asynchronous — poll `downloads` to watch the queue drain.
- A podcast lives in a `mediaType: podcast` library; you cannot add one to a book library.

## Related
- **KG ingestion:** `audiobookshelf-kg-ingestion` maps podcasts to `:Podcast` /
  `:PodcastEpisode` nodes.
- Book libraries: `audiobookshelf-library-catalog`.

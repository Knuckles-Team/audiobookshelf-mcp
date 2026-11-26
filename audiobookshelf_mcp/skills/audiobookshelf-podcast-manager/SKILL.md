---
name: audiobookshelf-podcast-manager
skill_type: skill
description: >-
  Create and manage Audiobookshelf podcasts, RSS feeds and episodes: add a podcast from a feed URL, import OPML, check and download new episodes, manage the download queue, update or remove episodes. Use to onboard or maintain podcasts. Do NOT use for audiobook/ebook libraries (audiobookshelf-library-catalog) or KG ingestion (audiobookshelf-kg-ingestion).
license: MIT
tags: [audiobookshelf, podcast, rss, opml, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Audiobookshelf Podcast Manager

Scope: Create and manage Audiobookshelf podcasts, their RSS feeds and episodes via the audiobookshelf-mcp MCP server — add a podcast from a feed URL, bulk-import from OPML, check for and download new episodes, manage the download queue, and read/update/remove episodes. Use when the agent must onboard or maintain podcasts. Do NOT use for audiobook/ebook libraries (audiobookshelf-library-catalog) or KG ingestion (audiobookshelf-kg-ingestion).

Domain-typed access to Audiobookshelf **podcasts** and **episodes** through the
`audiobookshelf-mcp` MCP server. Prefer the typed podcast tools over raw
HTTP — it carries the feed/episode field conventions.

## When to use
- Add a podcast from an RSS feed URL, or bulk-create from an OPML feed / text.
- Preview a feed's episodes before adding it.
- Check for new episodes and queue them for download; inspect or clear the queue.
- Read, update, or remove an individual episode; quick-match episodes against a feed.

## When NOT to use
- Audiobook / ebook libraries and series → `audiobookshelf-library-catalog`.
- Author portrait/provider-match curation -> `audiobookshelf_match_author_by_id` and the author image tools.
- Pushing podcasts into the medulla → `audiobookshelf-kg-ingestion`.

## Steps

1. Preview the feed with `audiobookshelf_get_podcast_feed` (`body` carries `rssFeed`).
   Verify the episode titles match the intended podcast.
2. Add the podcast with `audiobookshelf_create_podcast`, or import many with `audiobookshelf_bulk_create_podcasts_from_opml_feed`.
   Verify the response returns library item ids.
3. Check for new episodes with `audiobookshelf_check_new_episodes` and queue with `audiobookshelf_download_episodes`.
   Verify `audiobookshelf_get_episode_downloads` shows the queue draining.
4. Update or remove an episode only when asked with `audiobookshelf_update_episode` or `audiobookshelf_remove_episode`.
   Verify `audiobookshelf_get_episode` reflects the change.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| HTTP 401 or connection error | `AUDIOBOOKSHELF_TOKEN` or `AUDIOBOOKSHELF_URL` is missing or wrong | Set both variables to a valid API token and base URL, restart the server, and confirm with `audiobookshelf_get_library_recent_episodes` |
| Podcast cannot be added | The target library is a book library | Choose a library whose `mediaType` is podcast in the `audiobookshelf_create_podcast` body |
| Feed preview fails | The RSS URL is wrong or unreachable | Correct the `rssFeed` value and call `audiobookshelf_get_podcast_feed` with the corrected URL |

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`audiobookshelf-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `AUDIOBOOKSHELF_URL` | ✅ | Server base URL (default `http://localhost:13378`) |
| `AUDIOBOOKSHELF_TOKEN` | ✅ | Bearer API token (Config → API Keys) |
| `AUDIOBOOKSHELF_SSL_VERIFY` | optional | TLS verification toggle |

## Tools
One typed tool per operation.

| Task | Tool |
|------|------|
| Create / preview | `audiobookshelf_create_podcast`, `audiobookshelf_get_podcast_feed` |
| OPML | `audiobookshelf_bulk_create_podcasts_from_opml_feed`, `audiobookshelf_get_feeds_from_opml_text` |
| Episodes | `audiobookshelf_check_new_episodes`, `audiobookshelf_download_episodes`, `audiobookshelf_get_episode_downloads`, `audiobookshelf_clear_episode_download_queue`, `audiobookshelf_get_episode`, `audiobookshelf_update_episode`, `audiobookshelf_remove_episode`, `audiobookshelf_quick_match_episodes`, `audiobookshelf_find_episode` |
| Library views | `audiobookshelf_get_library_recent_episodes`, `audiobookshelf_get_library_episode_downloads` |

### Key parameters
- `id` - the podcast library-item id (required for episode/queue tools).
- `episode_id` - required for `audiobookshelf_get_episode`, `audiobookshelf_update_episode`, `audiobookshelf_remove_episode`.
- `audiobookshelf_create_podcast` takes a podcast body (folder/library ids + `media.metadata.feedUrl`).
- `audiobookshelf_get_podcast_feed` takes the `rssFeed` URL in `body`; `audiobookshelf_get_feeds_from_opml_text` takes `opmlText` in `body`.

## Recipes
Preview a feed before adding: `audiobookshelf_get_podcast_feed` with `body={"rssFeed":"https://example.com/podcast.rss"}`.

Check for new episodes: `audiobookshelf_check_new_episodes` with `id=<podcast_item_id>`.

Queue specific episodes: `audiobookshelf_download_episodes` with `id=<podcast_item_id>` and the episodes list.

## Gotchas
- `check_new` / `clear_queue` / `downloads` are GET-style: they only need `id`.
- Downloading episodes is asynchronous — poll `downloads` to watch the queue drain.
- A podcast lives in a `mediaType: podcast` library; you cannot add one to a book library.

## Related
- **KG ingestion:** `audiobookshelf-kg-ingestion` maps podcasts to `:Podcast` /
  `:PodcastEpisode` nodes.
- Book libraries: `audiobookshelf-library-catalog`.

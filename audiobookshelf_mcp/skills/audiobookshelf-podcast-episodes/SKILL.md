---
name: audiobookshelf-podcast-episodes
skill_type: skill
description: >-
  Create podcasts, search and import feeds, and manage episodes and the episode download
  queue. Do NOT use for tasks outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf podcasts

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

### `audiobookshelf-manage-podcast`

1. `audiobookshelf_get_feeds_from_opml_text` (`body`) - Get feeds from opml text.
2. `audiobookshelf_get_library_opml` (`id`) - Get library opml.
3. `audiobookshelf_get_podcast_feed` (`body`) - Get podcast feed.
4. `audiobookshelf_search_podcasts` (`term`) - Search podcasts.
5. `audiobookshelf_bulk_create_podcasts_from_opml_feed` (`body`) - Bulk create podcasts from opml feed.
6. `audiobookshelf_create_podcast` (`body`) - Create podcast.

### `audiobookshelf-manage-episode`

1. `audiobookshelf_check_new_episodes` (`id`) - Check new episodes.
2. `audiobookshelf_find_episode` (`id`, `params_json`) - Find episode.
3. `audiobookshelf_get_episode` (`episode_id`, `id`) - Get episode.
4. `audiobookshelf_get_library_recent_episodes` (`id`, `limit`, `page`) - Get library recent episodes.
5. `audiobookshelf_quick_match_episodes` (`id`, `params_json`) - Quick match episodes.
6. `audiobookshelf_update_episode` (`episode_id`, `id`, `params_json`) - Update episode.
7. `audiobookshelf_remove_episode` (`confirm`, `episode_id`, `id`) - Remove episode. (destructive: ask the operator first)

### `audiobookshelf-manage-download`

1. `audiobookshelf_get_episode_downloads` (`id`) - Get episode downloads.
2. `audiobookshelf_get_library_episode_downloads` (`id`, `limit`) - Get library episode downloads.
3. `audiobookshelf_download_episodes` (`id`, `params_json`) - Download episodes.
4. `audiobookshelf_clear_episode_download_queue` (`id`) - Clear episode download queue. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

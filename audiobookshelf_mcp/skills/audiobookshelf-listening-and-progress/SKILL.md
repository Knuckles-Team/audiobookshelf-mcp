---
name: audiobookshelf-listening-and-progress
skill_type: skill
description: >-
  Read and change listening sessions, progress, bookmarks, playback and listening
  statistics. Do NOT use for tasks outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf listening and progress

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

### `audiobookshelf-manage-session`

1. `audiobookshelf_get_my_listening_sessions` (`items_per_page`, `page`) - Get my listening sessions.
2. `audiobookshelf_get_open_sessions` (no parameters) - Get open sessions.
3. `audiobookshelf_get_session` (`id`) - Get session.
4. `audiobookshelf_get_sessions` (`desc`, `items_per_page`, `page`, `sort`, `user`) - Get sessions.
5. `audiobookshelf_get_user_listening_sessions` (`id`, `items_per_page`, `page`) - Get user listening sessions.
6. `audiobookshelf_sync_session` (`body`, `id`) - Sync session.
7. `audiobookshelf_batch_delete_sessions` (`body`, `confirm`) - Batch delete sessions. (destructive: ask the operator first)
8. `audiobookshelf_close_session` (`body`, `id`) - Close session. (destructive: ask the operator first)
9. `audiobookshelf_delete_session` (`confirm`, `id`) - Delete session. (destructive: ask the operator first)

### `audiobookshelf-manage-progress`

1. `audiobookshelf_get_my_items_in_progress` (`limit`) - Get my items in progress.
2. `audiobookshelf_batch_update_my_progress` (`body`) - Batch update my progress.
3. `audiobookshelf_sync_local_progress` (`body`) - Sync local progress.
4. `audiobookshelf_update_my_episode_progress` (`body`, `episode_id`, `library_item_id`) - Update my episode progress.
5. `audiobookshelf_update_my_progress` (`body`, `library_item_id`) - Update my progress.
6. `audiobookshelf_delete_my_progress` (`confirm`, `progress_id`) - Delete my progress. (destructive: ask the operator first)

### `audiobookshelf-manage-bookmark`

1. `audiobookshelf_create_my_bookmark` (`body`, `library_item_id`) - Create my bookmark.
2. `audiobookshelf_update_my_bookmark` (`body`, `library_item_id`) - Update my bookmark.
3. `audiobookshelf_delete_my_bookmark` (`confirm`, `library_item_id`, `time`) - Delete my bookmark. (destructive: ask the operator first)

### `audiobookshelf-inspect-stats`

1. `audiobookshelf_get_library_stats` (`id`) - Get library stats.
2. `audiobookshelf_get_my_listening_stats` (no parameters) - Get my listening stats.
3. `audiobookshelf_get_my_year_stats` (`year`) - Get my year stats.
4. `audiobookshelf_get_online_users` (no parameters) - Get online users.
5. `audiobookshelf_get_server_stats_year` (`year`) - Get server stats year.
6. `audiobookshelf_get_user_listening_stats` (`id`) - Get user listening stats.

### `audiobookshelf-manage-playback`

1. `audiobookshelf_play_item` (`body`, `id`) - Play item.
2. `audiobookshelf_play_item_episode` (`body`, `episode_id`, `id`) - Play item episode.
3. `audiobookshelf_remove_item_from_continue_listening` (`confirm`, `progress_id`) - Remove item from continue listening. (destructive: ask the operator first)
4. `audiobookshelf_remove_series_from_continue_listening` (`confirm`, `series_id`) - Remove series from continue listening. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

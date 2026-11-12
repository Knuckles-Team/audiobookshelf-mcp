---
name: audiobookshelf-server-administration
skill_type: skill
description: >-
  Administer the server: status, settings, backups, notifications, email and e-reader
  devices, cache and filesystem. Do NOT use for tasks outside the audiobookshelf-mcp
  connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf server administration

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

### `audiobookshelf-manage-backup`

1. `audiobookshelf_get_backups` (no parameters) - Get backups.
2. `audiobookshelf_create_backup` (no parameters) - Create backup.
3. `audiobookshelf_update_backup_path` (`body`) - Update backup path.
4. `audiobookshelf_apply_backup` (`id`) - Apply backup. (destructive: ask the operator first)
5. `audiobookshelf_delete_backup` (`confirm`, `id`) - Delete backup. (destructive: ask the operator first)

### `audiobookshelf-manage-maintenance`

1. `audiobookshelf_check_path_exists` (`body`) - Check path exists.
2. `audiobookshelf_get_filesystem_paths` (`level`) - Get filesystem paths.
3. `audiobookshelf_purge_cache` (`confirm`) - Purge cache. (destructive: ask the operator first)
4. `audiobookshelf_purge_items_cache` (`confirm`) - Purge items cache. (destructive: ask the operator first)

### `audiobookshelf-manage-notification`

1. `audiobookshelf_get_notification_event_data` (no parameters) - Get notification event data.
2. `audiobookshelf_get_notifications` (no parameters) - Get notifications.
3. `audiobookshelf_configure_notification_settings` (`body`) - Configure notification settings.
4. `audiobookshelf_create_notification` (`body`) - Create notification.
5. `audiobookshelf_send_default_test_notification` (no parameters) - Send default test notification.
6. `audiobookshelf_send_test_notification` (`id`) - Send test notification.
7. `audiobookshelf_update_notification` (`id`, `params_json`) - Update notification.
8. `audiobookshelf_delete_notification` (`confirm`, `id`) - Delete notification. (destructive: ask the operator first)

### `audiobookshelf-manage-email`

1. `audiobookshelf_get_email_settings` (no parameters) - Get email settings.
2. `audiobookshelf_send_test_email` (`body`) - Send test email.
3. `audiobookshelf_update_email_settings` (`body`) - Update email settings.
4. `audiobookshelf_update_ereader_devices` (`body`) - Update ereader devices.

### `audiobookshelf-inspect-status`

1. `audiobookshelf_get_server_logs` (no parameters) - Get server logs.
2. `audiobookshelf_get_server_status` (no parameters) - Get server status.
3. `audiobookshelf_healthcheck_server` (no parameters) - Healthcheck server.
4. `audiobookshelf_ping_server` (no parameters) - Ping server.

### `audiobookshelf-manage-settings`

1. `audiobookshelf_update_server_settings` (`body`) - Update server settings.
2. `audiobookshelf_update_sorting_prefixes` (`body`) - Update sorting prefixes.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

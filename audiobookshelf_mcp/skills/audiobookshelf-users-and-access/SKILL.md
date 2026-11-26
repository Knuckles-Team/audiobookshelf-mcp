---
name: audiobookshelf-users-and-access
skill_type: skill
description: >-
  Manage Audiobookshelf accounts, API keys and authentication settings. Do NOT use for
  tasks outside the audiobookshelf-mcp connector.
license: MIT
tags: [audiobookshelf, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Audiobookshelf users and access

Use the typed tools of the `audiobookshelf-mcp` connector: one tool per upstream API operation, named `audiobookshelf_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Steps

1. Confirm the acting account with `audiobookshelf_get_me`.
   Verify it has the admin type needed.
2. List accounts with `audiobookshelf_get_users` or keys with `audiobookshelf_get_api_keys`.
   Verify the target id is present before changing it.
3. Create or change with `audiobookshelf_create_user`, `audiobookshelf_update_user` or `audiobookshelf_create_api_key`.
   Verify the response shows the submitted fields without echoing secrets.
4. Delete only when approved with `audiobookshelf_delete_user` or `audiobookshelf_delete_api_key`.
   Verify the id no longer appears in the list tool.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| HTTP 401 or connection error | `AUDIOBOOKSHELF_TOKEN` or `AUDIOBOOKSHELF_URL` is missing or wrong | Set both variables to a valid API token and base URL, restart the server, and confirm with `audiobookshelf_get_me` |
| Destructive call refused | `confirm` was not passed or the operator has not approved | Ask the operator, then pass `confirm` set to true on `audiobookshelf_delete_user` |
| 404 or empty result | The `id` is wrong or belongs to another object | Call `audiobookshelf_get_users` and copy the exact id from its result |

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

### `audiobookshelf-manage-auth`

1. `audiobookshelf_authorize` (no parameters) - Authorize.
2. `audiobookshelf_get_auth_settings` (no parameters) - Get auth settings.
3. `audiobookshelf_update_auth_settings` (`body`) - Update auth settings.

### `audiobookshelf-manage-user`

1. `audiobookshelf_get_me` (`include`) - Get me.
2. `audiobookshelf_get_user` (`id`, `include`) - Get user.
3. `audiobookshelf_get_users` (`include`) - Get users.
4. `audiobookshelf_create_user` (`body`) - Create user.
5. `audiobookshelf_change_my_password` (`body`) - Run change my password.
6. `audiobookshelf_update_user` (`body`, `id`) - Update user.
7. `audiobookshelf_delete_user` (`confirm`, `id`) - Delete user. (destructive: ask the operator first)

### `audiobookshelf-manage-api-key`

1. `audiobookshelf_get_api_keys` (no parameters) - Get api keys.
2. `audiobookshelf_create_api_key` (`body`) - Create api key.
3. `audiobookshelf_update_api_key` (`body`, `id`) - Update api key.
4. `audiobookshelf_delete_api_key` (`confirm`, `id`) - Delete api key. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the API token or other users' credentials.
- Identify media by library item id; confirm the item exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.

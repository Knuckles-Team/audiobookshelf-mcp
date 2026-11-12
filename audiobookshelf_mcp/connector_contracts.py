"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "audiobookshelf-manage-auth",
        (
            ToolStep(
                "audiobookshelf_authorize",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_auth_settings",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_auth_settings",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-user",
        (
            ToolStep(
                "audiobookshelf_get_me",
                params=(
                    "include",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_user",
                params=(
                    "id",
                    "include",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_users",
                params=(
                    "include",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_user",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_change_my_password",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_user",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_user",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-api-key",
        (
            ToolStep(
                "audiobookshelf_get_api_keys",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_api_key",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_api_key",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_api_key",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-session",
        (
            ToolStep(
                "audiobookshelf_get_my_listening_sessions",
                params=(
                    "items_per_page",
                    "page",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_open_sessions",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_session",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_sessions",
                params=(
                    "desc",
                    "items_per_page",
                    "page",
                    "sort",
                    "user",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_user_listening_sessions",
                params=(
                    "id",
                    "items_per_page",
                    "page",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_sync_session",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_delete_sessions",
                params=(
                    "body",
                    "confirm",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_close_session",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_session",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-progress",
        (
            ToolStep(
                "audiobookshelf_get_my_items_in_progress",
                params=(
                    "limit",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_update_my_progress",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_sync_local_progress",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_my_episode_progress",
                params=(
                    "body",
                    "episode_id",
                    "library_item_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_my_progress",
                params=(
                    "body",
                    "library_item_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_my_progress",
                params=(
                    "confirm",
                    "progress_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-bookmark",
        (
            ToolStep(
                "audiobookshelf_create_my_bookmark",
                params=(
                    "body",
                    "library_item_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_my_bookmark",
                params=(
                    "body",
                    "library_item_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_my_bookmark",
                params=(
                    "confirm",
                    "library_item_id",
                    "time",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-inspect-stats",
        (
            ToolStep(
                "audiobookshelf_get_library_stats",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_my_listening_stats",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_my_year_stats",
                params=(
                    "year",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_online_users",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_server_stats_year",
                params=(
                    "year",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_user_listening_stats",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-playback",
        (
            ToolStep(
                "audiobookshelf_play_item",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_play_item_episode",
                params=(
                    "body",
                    "episode_id",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_item_from_continue_listening",
                params=(
                    "confirm",
                    "progress_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_series_from_continue_listening",
                params=(
                    "confirm",
                    "series_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-podcast",
        (
            ToolStep(
                "audiobookshelf_get_feeds_from_opml_text",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_opml",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_podcast_feed",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_podcasts",
                params=(
                    "term",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_bulk_create_podcasts_from_opml_feed",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_podcast",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-episode",
        (
            ToolStep(
                "audiobookshelf_check_new_episodes",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_find_episode",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_episode",
                params=(
                    "episode_id",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_recent_episodes",
                params=(
                    "id",
                    "limit",
                    "page",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_quick_match_episodes",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_episode",
                params=(
                    "episode_id",
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_episode",
                params=(
                    "confirm",
                    "episode_id",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-download",
        (
            ToolStep(
                "audiobookshelf_get_episode_downloads",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_episode_downloads",
                params=(
                    "id",
                    "limit",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_download_episodes",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_clear_episode_download_queue",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-collection",
        (
            ToolStep(
                "audiobookshelf_get_collection",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_collections",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_collections",
                params=(
                    "filter",
                    "id",
                    "limit",
                    "minified",
                    "page",
                    "sort",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_add_book_to_collection",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_add_books_to_collection",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_collection",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_playlist_from_collection",
                params=(
                    "collection_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_collection",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_remove_books_from_collection",
                params=(
                    "body",
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_collection",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_book_from_collection",
                params=(
                    "book_id",
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-playlist",
        (
            ToolStep(
                "audiobookshelf_get_library_playlists",
                params=(
                    "id",
                    "limit",
                    "page",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_playlist",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_playlists",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_add_item_to_playlist",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_add_items_to_playlist",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_playlist",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_playlist",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_remove_items_from_playlist",
                params=(
                    "body",
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_playlist",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_item_from_playlist",
                params=(
                    "confirm",
                    "id",
                    "library_item_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-backup",
        (
            ToolStep(
                "audiobookshelf_get_backups",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_backup",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_backup_path",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_apply_backup",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_backup",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-maintenance",
        (
            ToolStep(
                "audiobookshelf_check_path_exists",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_filesystem_paths",
                params=(
                    "level",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_purge_cache",
                params=(
                    "confirm",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_purge_items_cache",
                params=(
                    "confirm",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-notification",
        (
            ToolStep(
                "audiobookshelf_get_notification_event_data",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_notifications",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_configure_notification_settings",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_notification",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_send_default_test_notification",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_send_test_notification",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_notification",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_notification",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-email",
        (
            ToolStep(
                "audiobookshelf_get_email_settings",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_send_test_email",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_email_settings",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_ereader_devices",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-inspect-status",
        (
            ToolStep(
                "audiobookshelf_get_server_logs",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_server_status",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_healthcheck_server",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_ping_server",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-settings",
        (
            ToolStep(
                "audiobookshelf_update_server_settings",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_sorting_prefixes",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-library",
        (
            ToolStep(
                "audiobookshelf_get_libraries",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_by_id",
                params=(
                    "id",
                    "include",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_create_library",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_order_libraries",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_library_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_library_by_id",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_library_issues",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-inspect-library-authors",
        (
            ToolStep(
                "audiobookshelf_get_library_authors",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-library-items",
        (
            ToolStep(
                "audiobookshelf_get_library_filter_data",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_items",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_personalized",
                params=(
                    "id",
                    "include",
                    "limit",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_library",
                params=(
                    "id",
                    "limit",
                    "q",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_match_all_library_items",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_scan_library",
                params=(
                    "force",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_remove_library_items_with_issues",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-inspect-library-series",
        (
            ToolStep(
                "audiobookshelf_get_library_series",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_library_series_by_id",
                params=(
                    "id",
                    "series_id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-author",
        (
            ToolStep(
                "audiobookshelf_get_author_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_author_image_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_authors",
                params=(
                    "q",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_add_author_image_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_match_author_by_id",
                params=(
                    "id",
                    "params_json",
                    "q",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_author_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_author_image_by_id",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_author_by_id",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_author_image_by_id",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-item",
        (
            ToolStep(
                "audiobookshelf_batch_get_items",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_item",
                params=(
                    "episode",
                    "expanded",
                    "id",
                    "include",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_item_cover",
                params=(
                    "format",
                    "height",
                    "id",
                    "raw",
                    "width",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_item_ffprobe",
                params=(
                    "file_id",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_item_tone_object",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_send_ebook_to_device",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_upload_item_cover",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_embed_metadata",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_quickmatch_items",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_scan_items",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_update_items",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_embed_item_metadata",
                params=(
                    "backup",
                    "force_embed_chapters",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_encode_item_m4b",
                params=(
                    "bitrate",
                    "channels",
                    "codec",
                    "id",
                    "token",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_match_item",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_scan_item",
                params=(
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_item_chapters",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_item_cover",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_item_media",
                params=(
                    "body",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_batch_delete_items",
                params=(
                    "body",
                    "confirm",
                    "hard",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_cancel_item_m4b_encode",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_item",
                params=(
                    "confirm",
                    "hard",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_item_cover",
                params=(
                    "confirm",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_item_file",
                params=(
                    "confirm",
                    "file_id",
                    "id",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-metadata",
        (
            ToolStep(
                "audiobookshelf_get_genres",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_get_tags",
                params=(),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_books",
                params=(
                    "author",
                    "isbn",
                    "provider",
                    "title",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_chapters",
                params=(
                    "asin",
                    "region",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_search_covers",
                params=(
                    "author",
                    "provider",
                    "title",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_rename_genre",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_rename_tag",
                params=(
                    "body",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_genre",
                params=(
                    "confirm",
                    "genre",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
            ToolStep(
                "audiobookshelf_delete_tag",
                params=(
                    "confirm",
                    "tag",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                    Refusal("CONFIRMATION_REQUIRED", "the caller has not confirmed the destructive call"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "audiobookshelf-manage-series",
        (
            ToolStep(
                "audiobookshelf_get_series",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "audiobookshelf_update_series",
                params=(
                    "id",
                    "params_json",
                ),
                result=(
                    "result",
                ),
                refusals=(
                    Refusal("ACCESS_DENIED", "the credential lacks access to the operation"),
                    Refusal("INVALID_ARGUMENT", "the upstream system rejects the input"),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "audiobookshelf-manage-auth",
        tools=(
            "audiobookshelf_authorize",
            "audiobookshelf_get_auth_settings",
            "audiobookshelf_update_auth_settings",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-users-and-access",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-user",
        tools=(
            "audiobookshelf_change_my_password",
            "audiobookshelf_create_user",
            "audiobookshelf_delete_user",
            "audiobookshelf_get_me",
            "audiobookshelf_get_user",
            "audiobookshelf_get_users",
            "audiobookshelf_update_user",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-users-and-access",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-api-key",
        tools=(
            "audiobookshelf_create_api_key",
            "audiobookshelf_delete_api_key",
            "audiobookshelf_get_api_keys",
            "audiobookshelf_update_api_key",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-users-and-access",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-session",
        tools=(
            "audiobookshelf_batch_delete_sessions",
            "audiobookshelf_close_session",
            "audiobookshelf_delete_session",
            "audiobookshelf_get_my_listening_sessions",
            "audiobookshelf_get_open_sessions",
            "audiobookshelf_get_session",
            "audiobookshelf_get_sessions",
            "audiobookshelf_get_user_listening_sessions",
            "audiobookshelf_sync_session",
        ),
        prompts=(
            "audiobookshelf-listener-support",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-listening-and-progress",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-progress",
        tools=(
            "audiobookshelf_batch_update_my_progress",
            "audiobookshelf_delete_my_progress",
            "audiobookshelf_get_my_items_in_progress",
            "audiobookshelf_sync_local_progress",
            "audiobookshelf_update_my_episode_progress",
            "audiobookshelf_update_my_progress",
        ),
        prompts=(
            "audiobookshelf-listener-support",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-listening-and-progress",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-bookmark",
        tools=(
            "audiobookshelf_create_my_bookmark",
            "audiobookshelf_delete_my_bookmark",
            "audiobookshelf_update_my_bookmark",
        ),
        prompts=(
            "audiobookshelf-listener-support",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-listening-and-progress",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-inspect-stats",
        tools=(
            "audiobookshelf_get_library_stats",
            "audiobookshelf_get_my_listening_stats",
            "audiobookshelf_get_my_year_stats",
            "audiobookshelf_get_online_users",
            "audiobookshelf_get_server_stats_year",
            "audiobookshelf_get_user_listening_stats",
        ),
        prompts=(
            "audiobookshelf-listener-support",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-listening-and-progress",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-playback",
        tools=(
            "audiobookshelf_play_item",
            "audiobookshelf_play_item_episode",
            "audiobookshelf_remove_item_from_continue_listening",
            "audiobookshelf_remove_series_from_continue_listening",
        ),
        prompts=(
            "audiobookshelf-listener-support",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-listening-and-progress",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-podcast",
        tools=(
            "audiobookshelf_bulk_create_podcasts_from_opml_feed",
            "audiobookshelf_create_podcast",
            "audiobookshelf_get_feeds_from_opml_text",
            "audiobookshelf_get_library_opml",
            "audiobookshelf_get_podcast_feed",
            "audiobookshelf_search_podcasts",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-podcast-manager",
        ),
        skills=(
            "audiobookshelf-podcast-episodes",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-episode",
        tools=(
            "audiobookshelf_check_new_episodes",
            "audiobookshelf_find_episode",
            "audiobookshelf_get_episode",
            "audiobookshelf_get_library_recent_episodes",
            "audiobookshelf_quick_match_episodes",
            "audiobookshelf_remove_episode",
            "audiobookshelf_update_episode",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-podcast-manager",
        ),
        skills=(
            "audiobookshelf-podcast-episodes",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-download",
        tools=(
            "audiobookshelf_clear_episode_download_queue",
            "audiobookshelf_download_episodes",
            "audiobookshelf_get_episode_downloads",
            "audiobookshelf_get_library_episode_downloads",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-podcast-manager",
        ),
        skills=(
            "audiobookshelf-podcast-episodes",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-collection",
        tools=(
            "audiobookshelf_add_book_to_collection",
            "audiobookshelf_batch_add_books_to_collection",
            "audiobookshelf_batch_remove_books_from_collection",
            "audiobookshelf_create_collection",
            "audiobookshelf_create_playlist_from_collection",
            "audiobookshelf_delete_collection",
            "audiobookshelf_get_collection",
            "audiobookshelf_get_collections",
            "audiobookshelf_get_library_collections",
            "audiobookshelf_remove_book_from_collection",
            "audiobookshelf_update_collection",
        ),
        prompts=(
            "audiobookshelf-collection-curator",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-collections-and-playlists",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-playlist",
        tools=(
            "audiobookshelf_add_item_to_playlist",
            "audiobookshelf_batch_add_items_to_playlist",
            "audiobookshelf_batch_remove_items_from_playlist",
            "audiobookshelf_create_playlist",
            "audiobookshelf_delete_playlist",
            "audiobookshelf_get_library_playlists",
            "audiobookshelf_get_playlist",
            "audiobookshelf_get_playlists",
            "audiobookshelf_remove_item_from_playlist",
            "audiobookshelf_update_playlist",
        ),
        prompts=(
            "audiobookshelf-collection-curator",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-collections-and-playlists",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-backup",
        tools=(
            "audiobookshelf_apply_backup",
            "audiobookshelf_create_backup",
            "audiobookshelf_delete_backup",
            "audiobookshelf_get_backups",
            "audiobookshelf_update_backup_path",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-maintenance",
        tools=(
            "audiobookshelf_check_path_exists",
            "audiobookshelf_get_filesystem_paths",
            "audiobookshelf_purge_cache",
            "audiobookshelf_purge_items_cache",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-notification",
        tools=(
            "audiobookshelf_configure_notification_settings",
            "audiobookshelf_create_notification",
            "audiobookshelf_delete_notification",
            "audiobookshelf_get_notification_event_data",
            "audiobookshelf_get_notifications",
            "audiobookshelf_send_default_test_notification",
            "audiobookshelf_send_test_notification",
            "audiobookshelf_update_notification",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-email",
        tools=(
            "audiobookshelf_get_email_settings",
            "audiobookshelf_send_test_email",
            "audiobookshelf_update_email_settings",
            "audiobookshelf_update_ereader_devices",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-inspect-status",
        tools=(
            "audiobookshelf_get_server_logs",
            "audiobookshelf_get_server_status",
            "audiobookshelf_healthcheck_server",
            "audiobookshelf_ping_server",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-settings",
        tools=(
            "audiobookshelf_update_server_settings",
            "audiobookshelf_update_sorting_prefixes",
        ),
        prompts=(
            "audiobookshelf-operator",
            "audiobookshelf-server-administrator",
        ),
        skills=(
            "audiobookshelf-server-administration",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-library",
        tools=(
            "audiobookshelf_create_library",
            "audiobookshelf_delete_library_by_id",
            "audiobookshelf_delete_library_issues",
            "audiobookshelf_get_libraries",
            "audiobookshelf_get_library_by_id",
            "audiobookshelf_order_libraries",
            "audiobookshelf_update_library_by_id",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-library-management",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-inspect-library-authors",
        tools=(
            "audiobookshelf_get_library_authors",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-library-management",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-library-items",
        tools=(
            "audiobookshelf_get_library_filter_data",
            "audiobookshelf_get_library_items",
            "audiobookshelf_get_library_personalized",
            "audiobookshelf_match_all_library_items",
            "audiobookshelf_remove_library_items_with_issues",
            "audiobookshelf_scan_library",
            "audiobookshelf_search_library",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-library-management",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-inspect-library-series",
        tools=(
            "audiobookshelf_get_library_series",
            "audiobookshelf_get_library_series_by_id",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-library-management",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-author",
        tools=(
            "audiobookshelf_add_author_image_by_id",
            "audiobookshelf_delete_author_by_id",
            "audiobookshelf_delete_author_image_by_id",
            "audiobookshelf_get_author_by_id",
            "audiobookshelf_get_author_image_by_id",
            "audiobookshelf_match_author_by_id",
            "audiobookshelf_search_authors",
            "audiobookshelf_update_author_by_id",
            "audiobookshelf_update_author_image_by_id",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-item-catalog",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-item",
        tools=(
            "audiobookshelf_batch_delete_items",
            "audiobookshelf_batch_embed_metadata",
            "audiobookshelf_batch_get_items",
            "audiobookshelf_batch_quickmatch_items",
            "audiobookshelf_batch_scan_items",
            "audiobookshelf_batch_update_items",
            "audiobookshelf_cancel_item_m4b_encode",
            "audiobookshelf_delete_item",
            "audiobookshelf_delete_item_cover",
            "audiobookshelf_delete_item_file",
            "audiobookshelf_embed_item_metadata",
            "audiobookshelf_encode_item_m4b",
            "audiobookshelf_get_item",
            "audiobookshelf_get_item_cover",
            "audiobookshelf_get_item_ffprobe",
            "audiobookshelf_get_item_tone_object",
            "audiobookshelf_match_item",
            "audiobookshelf_scan_item",
            "audiobookshelf_send_ebook_to_device",
            "audiobookshelf_update_item_chapters",
            "audiobookshelf_update_item_cover",
            "audiobookshelf_update_item_media",
            "audiobookshelf_upload_item_cover",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-item-catalog",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-metadata",
        tools=(
            "audiobookshelf_delete_genre",
            "audiobookshelf_delete_tag",
            "audiobookshelf_get_genres",
            "audiobookshelf_get_tags",
            "audiobookshelf_rename_genre",
            "audiobookshelf_rename_tag",
            "audiobookshelf_search_books",
            "audiobookshelf_search_chapters",
            "audiobookshelf_search_covers",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-item-catalog",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-manage-series",
        tools=(
            "audiobookshelf_get_series",
            "audiobookshelf_update_series",
        ),
        prompts=(
            "audiobookshelf-librarian",
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-item-catalog",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-kg-ingestion",
        tools=(
            "audiobookshelf_get_item_cover",
            "audiobookshelf_get_libraries",
            "audiobookshelf_get_library_authors",
            "audiobookshelf_get_library_items",
        ),
        prompts=(
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-kg-ingestion",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-library-catalog",
        tools=(
            "audiobookshelf_add_author_image_by_id",
            "audiobookshelf_create_library",
            "audiobookshelf_delete_library_by_id",
            "audiobookshelf_get_collection",
            "audiobookshelf_get_collections",
            "audiobookshelf_get_item",
            "audiobookshelf_get_item_cover",
            "audiobookshelf_get_libraries",
            "audiobookshelf_get_library_authors",
            "audiobookshelf_get_library_by_id",
            "audiobookshelf_get_library_collections",
            "audiobookshelf_get_library_filter_data",
            "audiobookshelf_get_library_items",
            "audiobookshelf_get_library_personalized",
            "audiobookshelf_get_library_series",
            "audiobookshelf_get_library_series_by_id",
            "audiobookshelf_get_library_stats",
            "audiobookshelf_get_series",
            "audiobookshelf_match_author_by_id",
            "audiobookshelf_search_library",
            "audiobookshelf_update_library_by_id",
            "audiobookshelf_update_series",
        ),
        prompts=(
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-library-catalog",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-media-operations",
        tools=(
            "audiobookshelf_get_item",
            "audiobookshelf_get_libraries",
            "audiobookshelf_get_library_items",
        ),
        prompts=(
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-media-operations",
        ),
    ),
    SurfaceLink(
        "audiobookshelf-podcast-manager",
        tools=(
            "audiobookshelf_bulk_create_podcasts_from_opml_feed",
            "audiobookshelf_check_new_episodes",
            "audiobookshelf_clear_episode_download_queue",
            "audiobookshelf_create_podcast",
            "audiobookshelf_download_episodes",
            "audiobookshelf_find_episode",
            "audiobookshelf_get_episode",
            "audiobookshelf_get_episode_downloads",
            "audiobookshelf_get_feeds_from_opml_text",
            "audiobookshelf_get_library_episode_downloads",
            "audiobookshelf_get_library_recent_episodes",
            "audiobookshelf_get_podcast_feed",
            "audiobookshelf_match_author_by_id",
            "audiobookshelf_quick_match_episodes",
            "audiobookshelf_remove_episode",
            "audiobookshelf_update_episode",
        ),
        prompts=(
            "audiobookshelf-operator",
        ),
        skills=(
            "audiobookshelf-podcast-manager",
        ),
    ),
)

LOCATIONS = (
    DataLocation(
        "audiobookshelf-libraries",
        (
            "Library",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_libraries",
    ),
    DataLocation(
        "audiobookshelf-items",
        (
            "MediaAsset",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_library_items",
    ),
    DataLocation(
        "audiobookshelf-authors",
        (
            "Person",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_library_authors",
    ),
    DataLocation(
        "audiobookshelf-episodes",
        (
            "MediaAsset",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_library_recent_episodes",
    ),
    DataLocation(
        "audiobookshelf-collections",
        (
            "Collection",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_collections",
    ),
    DataLocation(
        "audiobookshelf-sessions",
        (
            "ListeningSession",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_sessions",
    ),
    DataLocation(
        "audiobookshelf-users",
        (
            "Person",
        ),
        "AUDIOBOOKSHELF_URL",
        "audiobookshelf_get_users",
    ),
)

ROLES = (
    BusinessRole(
        "librarian",
        tasks=(
            "audiobookshelf-inspect-library-authors",
            "audiobookshelf-inspect-library-series",
            "audiobookshelf-manage-author",
            "audiobookshelf-manage-item",
            "audiobookshelf-manage-library",
            "audiobookshelf-manage-library-items",
            "audiobookshelf-manage-metadata",
            "audiobookshelf-manage-series",
        ),
    ),
    BusinessRole(
        "podcast manager",
        tasks=(
            "audiobookshelf-manage-download",
            "audiobookshelf-manage-episode",
            "audiobookshelf-manage-podcast",
        ),
    ),
    BusinessRole(
        "collection curator",
        tasks=(
            "audiobookshelf-manage-collection",
            "audiobookshelf-manage-playlist",
        ),
    ),
    BusinessRole(
        "listener support",
        tasks=(
            "audiobookshelf-inspect-stats",
            "audiobookshelf-manage-bookmark",
            "audiobookshelf-manage-playback",
            "audiobookshelf-manage-progress",
            "audiobookshelf-manage-session",
        ),
    ),
    BusinessRole(
        "server administrator",
        tasks=(
            "audiobookshelf-inspect-status",
            "audiobookshelf-manage-api-key",
            "audiobookshelf-manage-auth",
            "audiobookshelf-manage-backup",
            "audiobookshelf-manage-email",
            "audiobookshelf-manage-maintenance",
            "audiobookshelf-manage-notification",
            "audiobookshelf-manage-settings",
            "audiobookshelf-manage-user",
        ),
    ),
)

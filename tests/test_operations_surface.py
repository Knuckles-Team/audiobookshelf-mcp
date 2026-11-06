"""The connector serves one typed tool per operation, with no action-routed tools."""

import inspect

from audiobookshelf_mcp.api import ApiClientSystem


def _public_methods():
    return {
        name: fn
        for name, fn in inspect.getmembers(ApiClientSystem, inspect.isfunction)
        if not name.startswith("_") and name not in {"request", "close"}
    }


def test_media_progress_tools_are_served():
    methods = _public_methods()
    for name in (
        "get_users",
        "get_user_listening_stats",
        "get_user_listening_sessions",
        "get_my_items_in_progress",
        "update_my_progress",
    ):
        assert name in methods


def test_no_operation_takes_an_action_or_params_json():
    for name, fn in _public_methods().items():
        params = inspect.signature(fn).parameters
        assert "action" not in params, name
        assert "params_json" not in params, name


def test_every_route_covers_the_core_domains():
    methods = _public_methods()
    for name in (
        "get_item",
        "get_collections",
        "get_playlists",
        "get_backups",
        "get_sessions",
        "search_books",
        "get_server_status",
    ):
        assert name in methods

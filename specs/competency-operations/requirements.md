# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` | The connector must serve typed tools that return media progress per user and item: `audiobookshelf_get_users`, `audiobookshelf_get_user_listening_stats`, `audiobookshelf_get_user_listening_sessions`, `audiobookshelf_get_my_items_in_progress`. Proving test: `tests/test_operations_surface.py`. Caller chain: the `audiobookshelf-mcp = scion_sdk.cli:serve` console script -> entry point `audiobookshelf_mcp:connector` -> `ApiClientSystem` (`audiobookshelf_mcp/api/__init__.py`) -> `ApiClientUsers` (`api_client_users.py`) and `ApiClientMe` (`api_client_me.py`). Shape: one client method per upstream route; the SDK serves each as one typed tool. | The operation returns the documented fields. Test: `tests/test_operations_surface.py::test_media_progress_tools_are_served`. |

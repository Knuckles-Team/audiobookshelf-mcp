# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` | The connector must serve a `library_operations` or `users` action that returns media progress per user and item. Proving test: `tests/test_media_progress.py`. Caller chain: (planned) the `library_operations` tool (`audiobookshelf_mcp/mcp/mcp_libraries.py:72`, registered by `register_libraries_tools` at line 68) -> a new action handler beside `_libraries_items` (line 43) -> a new method on the client in `audiobookshelf_mcp/api/api_client_libraries.py`. Shape: (planned) add one `_libraries_*` async handler in `mcp_libraries.py` and one client method in `api_client_libraries.py` that reads per-user media progress; reuse the existing action table pattern; no `users` client module exists today. | The operation returns the documented fields. Planned test: `tests/test_media_progress.py::test_media_progress_per_user_and_item`. |

# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` | The connector must serve a `library_operations` or `users` action that returns media progress per user and item. Proving test: `tests/test_media_progress.py`. | The operation returns the documented fields. |

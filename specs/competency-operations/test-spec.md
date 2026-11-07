# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` | `tests/test_media_progress.py` | The operation returns the documented fields. |

## Adoption of scion-sdk 0.10.0 (`CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R002`)

| Requirement | Test | Observation |
|---|---|---|
| `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R002` | `tests/test_scion_sdk_0_10_imports.py::test_every_scion_sdk_import_resolves_on_the_pinned_release` | Every `scion_sdk` import resolves on the pinned release; a removed path fails the test. |

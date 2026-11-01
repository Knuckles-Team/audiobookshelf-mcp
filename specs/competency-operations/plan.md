# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

The operation is one tool per API operation, served through the connector's MCP server and mapped by the connector's virtual mapping. It returns only the fields named in the requirement.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 1 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
audiobookshelf_mcp/api/api_client_libraries.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

The rows are delivered in place; the design is the caller chain below.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001`: (planned) the `library_operations` tool (`audiobookshelf_mcp/mcp/mcp_libraries.py:72`, registered by `register_libraries_tools` at line 68) -> a new action handler beside `_libraries_items` (line 43) -> a new method on the client in `audiobookshelf_mcp/api/api_client_libraries.py`.

## Cross-repo seams

none

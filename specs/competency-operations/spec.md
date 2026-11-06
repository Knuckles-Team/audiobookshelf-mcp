# CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS — User listening progress

Owner: audiobookshelf-mcp. Cross-repo IDs: MEDULLA-MEDIA-VOCAB-R022.

## Purpose and user stories

Medulla answers a connector competency question over this connector's virtual graph. The question needs the operation below, which the connector does not serve today. Until it lands, Medulla answers with a typed abstention that names this operation.

## Why a new spec

No local spec owns connector operations that competency questions need. This spec owns them. It moved here from Medulla (MEDULLA-MEDIA-VOCAB-R022), where the rows described this connector's behaviour.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - User listening progress (Priority: P1)

Medulla answers a connector competency question over this connector's virtual graph. The question needs the operation below, which the connector does not serve today. Until it lands, Medulla answers with a typed abstention that names this operation.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` (the connector must serve typed tools that return media progress per user and item) is exercised, **Then** the operation returns the documented fields.

### Edge Cases

- If `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` is not met, its proving test fails: the connector must serve typed tools that return media progress per user and item.

## Requirements

- **FR-001**: The connector must serve typed tools that return media progress per user and item. Rows: `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001`.

## Success Criteria

- **SC-001**: The operation returns the documented fields. Rows: `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-AUDIOBOOKSHELF-MCP-COMPETENCY-OPERATIONS-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |

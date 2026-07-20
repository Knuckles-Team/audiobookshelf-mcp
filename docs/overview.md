# audiobookshelf-mcp — Concept Overview

> **Category**: Integration | **Ecosystem Role**: MCP Server + A2A Agent
> Built on [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) — the unified AGI Harness.

## Description

Audiobookshelf API + MCP Server + A2A Server

## Architecture

This project follows the standardized agent-package pattern:

- **Modular Design**: split into `api/` (client mixins) and `mcp/` (action-routed
  tool modules) for cleaner organization.
- **Dynamic Tool Registration**: action-routed dynamic tool tags, strictly
  lowercase, each togglable with a `*TOOL` environment flag.
- **A2A Agent Server**: a Pydantic-AI graph agent (console script `audiobookshelf-agent`)
  that calls the MCP tool surface and exposes an AG-UI web interface.
- **Verified transport profiles**: every outbound request uses the shared AgentConfig
  TLS resolver; verification is not a connector-level toggle.
- **Governed capability inputs**: one human-reviewed skill, ontology, source preset,
  prompts, and package entry points are discoverable without storing an instance
  schema or URL. The provider has no direct graph writer.

## Capability boundary

The ontology models the standard Audiobookshelf library, book, podcast, episode,
author, and series concepts used by the public tool surface. The source preset maps
the neutral `library_operations` list result. Environment-specific records, custom
fields, tenant mappings, endpoints, credentials, live records, and generated signatures
are discovered or supplied at runtime and are not part of this repository.

## Concept Registry

This project implements or inherits the following ecosystem concepts:

| Concept ID | Description | Source |
|:-----------|:------------|:-------|
| ECO-4.1 | MCP & Universal Skills | `agent-utilities` (inherited) |
| AU-ECO.toolkit.journey-map-narrative | A2A Network & Consensus | `agent-utilities` (inherited) |

> 📖 **Full Registry**: See [`agent-utilities/docs/overview.md`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/overview.md) for the complete 5-Pillar concept index.

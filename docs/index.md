# audiobookshelf-mcp

Audiobookshelf MCP **API + MCP Server + A2A Agent** for the agent-utilities ecosystem — a
typed, action-routed connector.

!!! info "Official documentation"
    This site is the canonical reference for `audiobookshelf-mcp`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/audiobookshelf-mcp)](https://pypi.org/project/audiobookshelf-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/audiobookshelf-mcp)](https://github.com/Knuckles-Team/audiobookshelf-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/audiobookshelf-mcp)

## Overview

`audiobookshelf-mcp` wraps the target service with typed, deterministic MCP tools and an
optional Pydantic-AI agent server.

The connector remains inactive until a runtime endpoint alias and either a fixed token
or delegated identity are available.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — package extras, source, and local container builds.
- :material-shield-lock: **[Configuration](configuration.md)** — AgentConfig, external secrets, verified TLS, and privacy.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers with neutral runtime inputs.
- :material-console: **[Usage](usage.md)** — the MCP tools, the Python client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — target-service requirements and ownership boundary.
- :material-sitemap: **[Overview](overview.md)** — the action-routed tool surface and architecture.
- :material-graph: **[Concepts](concepts.md)** — the CONCEPT ID registry.

</div>

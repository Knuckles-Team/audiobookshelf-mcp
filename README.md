# Audiobookshelf MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/audiobookshelf-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/audiobookshelf-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/audiobookshelf-mcp)
![PyPI - License](https://img.shields.io/pypi/l/audiobookshelf-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/audiobookshelf-mcp)

*Version: 0.1.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing platform are maintained in the
> [official documentation](https://knuckles-team.github.io/audiobookshelf-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Available MCP Tools](#available-mcp-tools)
- [Installation](#installation)
- [Usage](#usage)
- [MCP](#mcp)
- [Documentation](#documentation)

---

## Overview

**Audiobookshelf MCP MCP Server + A2A Agent**

Audiobookshelf API + MCP Server + A2A Server

This repository is actively maintained - Contributions are welcome!

## Key Features

- **Action-routed MCP tools** — each domain is exposed as a single MCP tool that routes
  to many underlying operations via an `action` argument, keeping the tool surface small.
- **Three interfaces, one package** — use it as a Python **API client**, an **MCP server**
  (`stdio` / `streamable-http` / `sse`), or a Pydantic-AI **A2A agent**.
- **`agent-utilities` native** — built on the shared framework (auth, action router,
  telemetry, governance) for fleet consistency.
- **Per-tool toggles** — enable or disable each tool domain with environment switches.
- **Enterprise-ready** — OTEL/Langfuse telemetry and optional Eunomia access governance.

## Available MCP Tools

Each tool is **action-routed**: pass an `action` and a JSON `params_json` payload. Tool
domains can be toggled on or off with the listed environment variable. The table below is
**auto-generated from the live server** by the `mcp-readme-table` pre-commit hook
(`python -m agent_utilities.mcp.readme_tools`) — do not edit it by hand.

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `author_operations` | `AUTHORSTOOL` | Manage Audiobookshelf authors. CONCEPT:ABS-002 |
| `email_operations` | `EMAILTOOL` | Manage Audiobookshelf email settings and e-reader delivery. CONCEPT:ABS-005 |
| `library_operations` | `LIBRARIESTOOL` | Manage Audiobookshelf libraries. CONCEPT:ABS-001 |
| `notification_operations` | `NOTIFICATIONTOOL` | Manage Audiobookshelf notifications. CONCEPT:ABS-006 |
| `podcast_operations` | `PODCASTSTOOL` | Manage Audiobookshelf podcasts and episodes. CONCEPT:ABS-004 |
| `series_operations` | `SERIESTOOL` | Manage Audiobookshelf series. CONCEPT:ABS-003 |

_6 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

### Install with `uvx` (no install — run on demand)

```bash
uvx --from audiobookshelf-mcp audiobookshelf-mcp      # MCP server
uvx --from audiobookshelf-mcp audiobookshelf-agent    # A2A agent server
```

### Install with `pip`

```bash
python -m pip install audiobookshelf-mcp            # core (API client)
python -m pip install "audiobookshelf-mcp[all]"     # + MCP server + A2A agent + telemetry
```

### Console scripts

After installation the following entry points are available on your `PATH`:

| Command | Description |
|---------|-------------|
| `audiobookshelf-mcp` | Launch the MCP server |
| `audiobookshelf-agent` | Launch the A2A agent server |

## Usage

### As a Python API client

```python
from audiobookshelf_mcp.auth import get_client

client = get_client()
status = client.get_system_status()
print(status)
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
audiobookshelf-mcp

# Networked streamable-http
audiobookshelf-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "system_operations",
  "arguments": {
    "action": "status",
    "params_json": "{}"
  }
}
```

## MCP

### Using as an MCP Server

The MCP Server can be run in `stdio` (local), `streamable-http` (networked), or
`sse` mode.

#### Environment Variables

*   `AUDIOBOOKSHELF_URL`: The URL of the target service.
*   `AUDIOBOOKSHELF_TOKEN`: The API token or access token.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "command": "uvx",
      "args": ["--from", "audiobookshelf-mcp", "audiobookshelf-mcp"],
      "env": {
        "AUDIOBOOKSHELF_URL": "https://service.example.com",
        "AUDIOBOOKSHELF_TOKEN": "your_token"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "command": "uvx",
      "args": ["--from", "audiobookshelf-mcp", "audiobookshelf-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "AUDIOBOOKSHELF_URL": "https://service.example.com",
        "AUDIOBOOKSHELF_TOKEN": "your_token"
      }
    }
  }
}
```

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`audiobookshelf-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/audiobookshelf-mcp/deployment/) has full,
copy-paste `mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://audiobookshelf-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Install Python Package

```bash
python -m pip install audiobookshelf-mcp
```

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/audiobookshelf-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)

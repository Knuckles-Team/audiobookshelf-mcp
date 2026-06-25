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
uvx --from "audiobookshelf-mcp[mcp]" audiobookshelf-mcp      # MCP server (slim)
uvx --from "audiobookshelf-mcp[agent]" audiobookshelf-agent  # A2A agent server (full)
```

### Install with `pip` / `uv`

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `audiobookshelf-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `audiobookshelf-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `audiobookshelf-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "audiobookshelf-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "audiobookshelf-mcp[agent]"

# Everything (development)
uv pip install "audiobookshelf-mcp[all]"      # or: python -m pip install "audiobookshelf-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/audiobookshelf-mcp:mcp` | `--target mcp` | `audiobookshelf-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `audiobookshelf-mcp` |
| `knucklessg1/audiobookshelf-mcp:latest` | `--target agent` (default) | `audiobookshelf-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `audiobookshelf-agent` |

```bash
docker build --target mcp   -t knucklessg1/audiobookshelf-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/audiobookshelf-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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

> **Install the slim `[mcp]` extra.** The MCP examples below install
> `audiobookshelf-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

### Using as an MCP Server

The MCP Server can be run in `stdio` (local), `streamable-http` (networked), or
`sse` mode.

#### Environment Variables

See the full [Environment Variables](#environment-variables) reference below. The minimum
to connect is `AUDIOBOOKSHELF_URL` (target service URL) and `AUDIOBOOKSHELF_TOKEN`
(API/access token).

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "command": "uvx",
      "args": ["--from", "audiobookshelf-mcp[mcp]", "audiobookshelf-mcp"],
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
      "args": ["--from", "audiobookshelf-mcp[mcp]", "audiobookshelf-mcp", "--transport", "streamable-http", "--port", "8000"],
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

## Environment Variables

Every variable the server reads, grouped by concern.

### Connection & Credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIOBOOKSHELF_URL` | Base URL of the Audiobookshelf instance | `http://localhost:13378` |
| `AUDIOBOOKSHELF_TOKEN` | API token / access token | — |
| `AUDIOBOOKSHELF_SSL_VERIFY` | TLS certificate verification | `True` |

### Authentication mode (OIDC delegation)
| Variable | Description |
|----------|-------------|
| `ENABLE_DELEGATION` | Set `true` to flow the caller's IdP token (RFC 8693 token exchange) to Audiobookshelf |
| `OIDC_CONFIG_URL` / `OIDC_CLIENT_ID` / `OIDC_CLIENT_SECRET` | OIDC delegation IdP config (required when delegation is enabled) |
| `AUDIENCE` | OIDC delegation token audience |
| `DELEGATED_SCOPES` | OIDC delegation scopes |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `DEBUG` | Verbose logging | `False` |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`):
`LIBRARIESTOOL`, `AUTHORSTOOL`, `SERIESTOOL`, `PODCASTSTOOL`, `EMAILTOOL`, `NOTIFICATIONTOOL`
(see the [Available MCP Tools](#available-mcp-tools) table above).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

See [`.env.example`](.env.example) for a copy-paste starting point.

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/audiobookshelf-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)

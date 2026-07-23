# Audiobookshelf MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/audiobookshelf-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/audiobookshelf-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/audiobookshelf-mcp)
![PyPI - License](https://img.shields.io/pypi/l/audiobookshelf-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/audiobookshelf-mcp)

*Version: 2.0.0*

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

**Audiobookshelf API client + MCP Server + A2A Agent**

The package exposes an operator-selected Audiobookshelf service through typed,
action-routed tools without storing an endpoint, credential, or instance profile.

This repository is actively maintained - Contributions are welcome!

## Key Features

- **Action-routed MCP tools** — each domain is exposed as a single MCP tool that routes
  to many underlying operations via an `action` argument, keeping the tool surface small.
- **Three interfaces, one package** — use it as a Python **API client**, an **MCP server**
  (`stdio` / `streamable-http` / `sse`), or a Pydantic-AI **A2A agent**.
- **`agent-utilities` native** — built on the shared framework (auth, action router,
  telemetry, governance) for fleet consistency.
- **Verified transport profiles** — outbound HTTP uses AgentConfig-backed TLS trust;
  peer and hostname verification cannot be disabled by this connector.
- **Governed graph capability inputs** — ships one comprehensive skill, a public-model
  ontology, and a neutral source preset, but no direct graph-write or raw-media tool.
- **Per-tool toggles** — enable or disable each tool domain with environment switches.
- **Enterprise-ready** — OTEL/Langfuse telemetry and optional Eunomia access governance.

## Available MCP Tools

Each tool is **action-routed**: pass an `action` and a JSON `params_json` payload. Tool
domains can be toggled on or off with the listed environment variable. The table below is
**auto-generated from the live server** by the `mcp-readme-table` pre-commit hook
(`python -m agent_utilities.mcp.readme_tools`) — do not edit it by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `author_operations` | `AUTHORSTOOL` | Manage Audiobookshelf authors. CONCEPT:AS-OS.identity.abs-2 |
| `email_operations` | `EMAILTOOL` | Manage Audiobookshelf email settings and e-reader delivery. CONCEPT:AS-OS.governance.abs-3 |
| `library_operations` | `LIBRARIESTOOL` | Manage Audiobookshelf libraries. CONCEPT:AS-OS.identity.abs |
| `notification_operations` | `NOTIFICATIONTOOL` | Manage Audiobookshelf notifications. CONCEPT:AS-OS.governance.abs-4 |
| `podcast_operations` | `PODCASTSTOOL` | Manage Audiobookshelf podcasts and episodes. CONCEPT:AS-OS.governance.abs-2 |
| `series_operations` | `SERIESTOOL` | Manage Audiobookshelf series. CONCEPT:AS-OS.governance.abs |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>46 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `audiobookshelf_add_author_image_by_id` | `AUTHORSTOOL` | Upload/add an author's image by id. |
| `audiobookshelf_bulk_create_podcasts_from_opml_feed` | `PODCASTSTOOL` | Bulk create podcasts from an OPML feed. |
| `audiobookshelf_check_new_episodes` | `PODCASTSTOOL` | Check for new episodes for a podcast by id. |
| `audiobookshelf_clear_episode_download_queue` | `PODCASTSTOOL` | Clear the episode download queue for a podcast by id. |
| `audiobookshelf_configure_notification_settings` | `NOTIFICATIONTOOL` | Update the global notification settings. |
| `audiobookshelf_create_library` | `LIBRARIESTOOL` | Create a new library. |
| `audiobookshelf_create_notification` | `NOTIFICATIONTOOL` | Create a new notification. |
| `audiobookshelf_create_podcast` | `PODCASTSTOOL` | Create a new podcast library item. |
| `audiobookshelf_delete_author_by_id` | `AUTHORSTOOL` | Delete an author by id. |
| `audiobookshelf_delete_author_image_by_id` | `AUTHORSTOOL` | Remove an author's image by id. |
| `audiobookshelf_delete_library_by_id` | `LIBRARIESTOOL` | Delete a library by id. |
| `audiobookshelf_delete_library_issues` | `LIBRARIESTOOL` | Remove all library items that have issues from a library. |
| `audiobookshelf_delete_notification` | `NOTIFICATIONTOOL` | Delete a notification by id. |
| `audiobookshelf_download_episodes` | `PODCASTSTOOL` | Queue episodes for download for a podcast by id. |
| `audiobookshelf_find_episode` | `PODCASTSTOOL` | Search for a podcast episode by id. |
| `audiobookshelf_get_author_by_id` | `AUTHORSTOOL` | Get a single author by id (supports include/library params). |
| `audiobookshelf_get_author_image_by_id` | `AUTHORSTOOL` | Get an author's image by id. |
| `audiobookshelf_get_email_settings` | `EMAILTOOL` | Get the server email settings. |
| `audiobookshelf_get_episode` | `PODCASTSTOOL` | Get a single podcast episode by id. |
| `audiobookshelf_get_episode_downloads` | `PODCASTSTOOL` | Get the current episode download queue for a podcast by id. |
| `audiobookshelf_get_feeds_from_opml_text` | `PODCASTSTOOL` | Parse feeds from raw OPML text. |
| `audiobookshelf_get_libraries` | `LIBRARIESTOOL` | List all libraries. |
| `audiobookshelf_get_library_authors` | `LIBRARIESTOOL` | Get the authors within a library. |
| `audiobookshelf_get_library_by_id` | `LIBRARIESTOOL` | Get a single library by id. |
| `audiobookshelf_get_library_items` | `LIBRARIESTOOL` | Get the items within a library (supports limit/page/sort/filter params). |
| `audiobookshelf_get_library_series` | `LIBRARIESTOOL` | Get the series within a library. |
| `audiobookshelf_get_library_series_by_id` | `LIBRARIESTOOL` | Get a single series within a library by id. |
| `audiobookshelf_get_notification_event_data` | `NOTIFICATIONTOOL` | Get the available notification event data. |
| `audiobookshelf_get_notifications` | `NOTIFICATIONTOOL` | Get the configured notification settings and notifications. |
| `audiobookshelf_get_podcast_feed` | `PODCASTSTOOL` | Fetch a podcast RSS feed by URL. |
| `audiobookshelf_get_series` | `SERIESTOOL` | Get a single series by id (supports include params). |
| `audiobookshelf_match_author_by_id` | `AUTHORSTOOL` | Match an author against a metadata provider by id. |
| `audiobookshelf_quick_match_episodes` | `PODCASTSTOOL` | Quick-match a podcast's episodes against a feed by id. |
| `audiobookshelf_remove_episode` | `PODCASTSTOOL` | Remove a podcast episode by id. |
| `audiobookshelf_send_default_test_notification` | `NOTIFICATIONTOOL` | Send a default test notification. |
| `audiobookshelf_send_ebook_to_device` | `EMAILTOOL` | Send an ebook to a configured e-reader device. |
| `audiobookshelf_send_test_email` | `EMAILTOOL` | Send a test email using the configured settings. |
| `audiobookshelf_send_test_notification` | `NOTIFICATIONTOOL` | Send a test notification for a specific notification by id. |
| `audiobookshelf_update_author_by_id` | `AUTHORSTOOL` | Update an author by id. |
| `audiobookshelf_update_author_image_by_id` | `AUTHORSTOOL` | Update an author's image by id. |
| `audiobookshelf_update_email_settings` | `EMAILTOOL` | Update the server email settings. |
| `audiobookshelf_update_episode` | `PODCASTSTOOL` | Update a podcast episode by id. |
| `audiobookshelf_update_ereader_devices` | `EMAILTOOL` | Update the configured e-reader devices. |
| `audiobookshelf_update_library_by_id` | `LIBRARIESTOOL` | Update a library by id. |
| `audiobookshelf_update_notification` | `NOTIFICATIONTOOL` | Update a notification by id. |
| `audiobookshelf_update_series` | `SERIESTOOL` | Update a series by id. |

</details>

_6 action-routed tool(s) · 46 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

### Install with `uvx` (no install — run on demand)

```bash
uvx --from "audiobookshelf-mcp[mcp]" audiobookshelf-mcp      # MCP server
uvx --from "audiobookshelf-mcp[agent]" audiobookshelf-agent  # A2A agent server (full)
```

### Install with `pip` / `uv`

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `audiobookshelf-mcp[mcp]` | MCP server (`agent-utilities[mcp]`) plus the mandatory full epistemic-graph base runtime | You run the **MCP server** without the agent UI/runtime |
| `audiobookshelf-mcp[agent]` | Current agent runtime (`agent-utilities[agent-runtime,logfire]`) | You run the **integrated agent** |
| `audiobookshelf-mcp[all]` | MCP + agent runtime + Logfire | Development or both surfaces |

```bash
# MCP server only (recommended for tool hosting)
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
| `audiobookshelf-mcp:mcp` | `--target mcp` | MCP server plus the mandatory full epistemic-graph base dependency | `audiobookshelf-mcp` |
| `audiobookshelf-mcp@sha256:<digest>` | `--target agent` (default) | MCP dependencies plus the current Pydantic-AI agent runtime | `audiobookshelf-agent` |

```bash
docker build --target mcp -t audiobookshelf-mcp:mcp -f docker/Dockerfile .
docker build --target agent -t audiobookshelf-mcp:agent-local -f docker/Dockerfile .
```

`docker/mcp.compose.yml` runs the MCP-only `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Every install receives `epistemic-graph[full]` through the current Agent Utilities base
dependency. The connector does not open an insecure engine listener or silently select a
machine-specific engine. Deployment topology and identity are resolved by AgentConfig. For a
shared production authority, follow the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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
try:
    print(client.get_libraries())
finally:
    client.close()
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
audiobookshelf-mcp

# Networked streamable-http
audiobookshelf-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "library_operations",
  "arguments": {
    "action": "list",
    "params_json": "{}"
  }
}
```

## MCP

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `audiobookshelf-mcp[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "audiobookshelf-mcp[mcp]",
        "audiobookshelf-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "AUDIOBOOKSHELF_TOKEN": "env://AUDIOBOOKSHELF_TOKEN",
        "AUDIOBOOKSHELF_URL": "env://AUDIOBOOKSHELF_URL",
        "AUTHORSTOOL": "True",
        "EMAILTOOL": "True",
        "LIBRARIESTOOL": "True",
        "NOTIFICATIONTOOL": "True",
        "PODCASTSTOOL": "True",
        "SERIESTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "audiobookshelf-mcp[mcp]",
        "audiobookshelf-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "AUDIOBOOKSHELF_TOKEN": "env://AUDIOBOOKSHELF_TOKEN",
        "AUDIOBOOKSHELF_URL": "env://AUDIOBOOKSHELF_URL",
        "AUTHORSTOOL": "True",
        "EMAILTOOL": "True",
        "LIBRARIESTOOL": "True",
        "NOTIFICATIONTOOL": "True",
        "PODCASTSTOOL": "True",
        "SERIESTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "audiobookshelf-mcp": {
      "url": "http://localhost:8000/audiobookshelf-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e AUDIOBOOKSHELF_TOKEN \
  -e AUDIOBOOKSHELF_URL \
  -e AUTHORSTOOL=True \
  -e EMAILTOOL=True \
  -e LIBRARIESTOOL=True \
  -e NOTIFICATIONTOOL=True \
  -e PODCASTSTOOL=True \
  -e SERIESTOOL=True \
  registry.example.invalid/audiobookshelf-mcp@sha256:<digest> audiobookshelf-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`audiobookshelf-mcp` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/audiobookshelf-mcp/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `MCP_TOOL_MODE` | `intent` | options: intent, condensed, verbose, both |
| `ENABLE_OTEL` | `False` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `env://OTEL_EXPORTER_OTLP_ENDPOINT` | runtime endpoint |
| `OTEL_EXPORTER_OTLP_HEADERS_REF` | `secret://telemetry/headers` | runtime header reference |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | OTLP transport protocol |
| `LANGFUSE_CAPTURE_CONTENT` | `false` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | — |  |
| `EUNOMIA_REMOTE_URL` | `env://EUNOMIA_REMOTE_URL` | runtime policy endpoint |
| `AUDIOBOOKSHELF_URL` | `env://AUDIOBOOKSHELF_URL` | resolved by the fleet launcher |
| `AUDIOBOOKSHELF_TOKEN` | `env://AUDIOBOOKSHELF_TOKEN` | secret provider or delegation |
| `LIBRARIESTOOL` | `True` |  |
| `AUTHORSTOOL` | `True` |  |
| `SERIESTOOL` | `True` |  |
| `PODCASTSTOOL` | `True` |  |
| `EMAILTOOL` | `True` |  |
| `NOTIFICATIONTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_20 package + 15 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->

The generated table is the authoritative process-variable catalog. Endpoint and
credential examples are unresolved references, not deployment values. AgentConfig owns
TLS selection, OIDC delegation, runtime secret resolution, and observability policy; see
[Configuration, trust, and privacy](docs/configuration.md) for those typed profiles.

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/audiobookshelf-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Configuration, Trust, and Privacy](docs/configuration.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `audiobookshelf-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "audiobookshelf-mcp[mcp]"`, then run `audiobookshelf-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `audiobookshelf-mcp` |
| Immutable container | deploy `registry.example.invalid/audiobookshelf-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package owns the complete release-generated schema-v2 capability bundle:
`connector_manifest.yml`, the exact local MCP schema fingerprint, the Audiobookshelf
ontology, SHACL shapes, the neutral source mapping and fixture, the migration ledger,
and an offline source attestation. Release tooling derives and signs these artifacts
from the current tool and ontology sources; they are not hand-authored and do not claim
external-live certification.

Runtime endpoints, credentials, certificate trust, identity, tenant/ACL policy,
retention, and observability destinations are deployment inputs and are never packaged
values. See [Configuration, trust, and privacy](docs/configuration.md) before enabling
a network transport, GraphOS delegation, governed source synchronization, or trace
export.
<!-- GOVERNED-CAPABILITY:END -->

# Usage — API / CLI / MCP

`audiobookshelf-mcp` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** you import, and as a **CLI**.

## As an MCP server

Once [deployed](deployment.md), the server registers consolidated, action-routed
tool modules. Each module is independently togglable with a `*TOOL` environment
flag.

## As a Python API

```python
from audiobookshelf_mcp.auth import get_client

api = get_client()  # resolves AgentConfig/runtime connection and verified TLS trust
try:
    libraries = api.get_libraries()
finally:
    api.close()
```

## As a CLI

```bash
# AUDIOBOOKSHELF_URL and AUDIOBOOKSHELF_TOKEN are injected by the runtime.
audiobookshelf-mcp --transport stdio
```

The condensed surface exposes `library_operations`, `author_operations`,
`series_operations`, `podcast_operations`, `email_operations`, and
`notification_operations`. Each call takes an `action` and a JSON-encoded
`params_json` string. Enable only the domains authorized for the connector identity.

When catalog metadata must enter epistemic-graph, request centrally governed GraphOS
source synchronization. The provider exposes no direct graph-write or raw-cover
ingestion action. See [Configuration, trust, and privacy](configuration.md).

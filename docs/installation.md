# Installation

`audiobookshelf-mcp` is a standard Python package with separate MCP and agent runtime
extras. Connection and secret values are configured after installation.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable target service instance and access token.

## Run on demand with uvx

```bash
uvx --from "audiobookshelf-mcp[mcp]" audiobookshelf-mcp
```

Pydantic-AI server and the full epistemic-graph runtime are required.

## Install from PyPI

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "audiobookshelf-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-connector-sdk`) |
| `all` | `pip install "audiobookshelf-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/audiobookshelf-mcp.git
cd audiobookshelf-mcp
pip install -e ".[all]"
```

## Build a local container image

```bash
docker build --target mcp -t audiobookshelf-mcp:mcp -f docker/Dockerfile .
```

The Compose files accept `AUDIOBOOKSHELF_MCP_IMAGE` and
`AUDIOBOOKSHELF_AGENT_IMAGE` when an operator-approved registry is used. No personal
registry namespace is embedded in this repository.

Proceed to [Configuration, trust, and privacy](configuration.md) before the first
connection attempt.

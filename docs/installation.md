# Installation

`audiobookshelf-mcp` is a standard Python package and a prebuilt container image.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable target service instance and access token.

## From PyPI (recommended)

```bash
pip install audiobookshelf-mcp
```

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "audiobookshelf-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "audiobookshelf-mcp[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "audiobookshelf-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/audiobookshelf-mcp.git
cd audiobookshelf-mcp
pip install -e ".[all]"
```

## Docker

```bash
docker pull knucklessg1/audiobookshelf-mcp:latest
```

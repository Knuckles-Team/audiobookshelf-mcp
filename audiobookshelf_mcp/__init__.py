"""Public Audiobookshelf client package.

MCP and agent runtimes remain explicit console entry points; importing this package
does not probe optional server dependencies.
"""

from audiobookshelf_mcp.api import ApiClientBase, ApiClientSystem

__all__ = ["ApiClientBase", "ApiClientSystem"]

from agent_connector_sdk.connector import Connector

from audiobookshelf_mcp.auth import get_client

connector = Connector(
    api=ApiClientSystem,
    get_client=get_client,
    tools="audiobookshelf_mcp.mcp",
    instructions="Audiobookshelf library and podcast operations. Media records and account configuration are sensitive; use the governed current tool surface.",
)

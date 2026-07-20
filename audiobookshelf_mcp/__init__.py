"""Public Audiobookshelf client package.

MCP and agent runtimes remain explicit console entry points; importing this package
does not probe optional server dependencies.
"""

from audiobookshelf_mcp.api import ApiClientBase, ApiClientSystem

__all__ = ["ApiClientBase", "ApiClientSystem"]

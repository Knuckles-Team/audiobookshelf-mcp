import importlib

import pytest


@pytest.mark.concept("AS-OS.identity.abs")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:AS-OS.identity.abs"""
    assert importlib.import_module("audiobookshelf_mcp.mcp_server") is not None

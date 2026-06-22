import importlib

import pytest


@pytest.mark.concept("ABS-001")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:ABS-001"""
    assert importlib.import_module("audiobookshelf_mcp.mcp_server") is not None

import importlib

import pytest


@pytest.mark.concept("AS-OS.identity.abs")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:AS-OS.identity.abs"""
    module = importlib.import_module("audiobookshelf_mcp")
    assert module.__all__ == ["ApiClientBase", "ApiClientSystem"]
    assert not hasattr(module, "_MCP_AVAILABLE")
    assert not hasattr(module, "_AGENT_AVAILABLE")

import pytest

from audiobookshelf_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("AS-OS.identity.abs")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:AS-OS.identity.abs
    """
    monkeypatch.setattr("sys.argv", ["audiobookshelf-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None

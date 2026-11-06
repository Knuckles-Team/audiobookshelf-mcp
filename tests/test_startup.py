import importlib

import pytest


@pytest.mark.concept("AS-OS.identity.abs")
def test_connector_declaration_importable():
    """The connector declaration imports cleanly at startup. CONCEPT:AS-OS.identity.abs"""
    module = importlib.import_module("audiobookshelf_mcp")
    assert module.connector is not None

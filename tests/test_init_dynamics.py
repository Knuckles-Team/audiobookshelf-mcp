import importlib

import pytest


@pytest.mark.concept("AS-OS.identity.abs")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:AS-OS.identity.abs"""
    module = importlib.import_module("audiobookshelf_mcp")
    assert hasattr(module, "__all__")

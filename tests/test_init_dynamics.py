import importlib

import pytest


@pytest.mark.concept("ABS-001")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:ABS-001"""
    module = importlib.import_module("audiobookshelf_mcp")
    assert hasattr(module, "__all__")

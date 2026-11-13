"""The connector ontology must not declare :Author in the shared namespace."""

from __future__ import annotations

import re
from importlib import resources

import pytest


def _text() -> str:
    return (
        resources.files("audiobookshelf_mcp.ontology")
        .joinpath("audiobookshelf.ttl")
        .read_text(encoding="utf-8")
    )


@pytest.mark.spec("CONN-AUDIOBOOKSHELF-MCP-CONNECTOR-CONTENT-R002")
def test_author_is_not_declared_in_the_shared_namespace() -> None:
    text = _text()
    assert not re.search(r"^:Author\s+a\s+owl:Class", text, re.M)
    assert "core:Author" not in text
    block = re.search(r"^:writtenBy\s.*?\.\s*$", text, re.M | re.S)
    assert block is not None
    assert "rdfs:subPropertyOf mv:contributor" in block.group(0)
    assert "rdfs:range core:Person" in block.group(0)

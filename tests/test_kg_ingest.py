"""Epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_libraries`` / ``ingest_library_items``
/ ``ingest_authors`` seam against a fake transport one level below the SDK's own
``SourceIngest`` request builder, asserting the committed nodes/edges and the
Audiobookshelf record -> :Library / :Book / :Author / :Series mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake fakes the **transport boundary**, not the SDK's own request-building/
validation contract (``agent_connector_sdk.ingest``), per the fleet SDK migration
recipe. Like gramps-mcp, ``audiobookshelf_mcp.kg_ingest`` is a **best-effort** surface
(its MCP tools must never raise when the KG stack is down), so it converts
``IngestError``/``IngestUnavailableError`` into ``None`` rather than propagating it --
those semantics are exercised explicitly below.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from audiobookshelf_mcp.kg_ingest import (
    ingest_authors,
    ingest_entities,
    ingest_libraries,
    ingest_library_items,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's node/document ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _node(transport: _FakeTransport, node_id: str) -> dict[str, Any]:
    for request in transport.requests:
        for record in request.records:
            if record.record_id == node_id:
                return dict(record.payload)
    raise AssertionError(f"no committed record {node_id!r}")


def _edges(transport: _FakeTransport) -> set[tuple[str, str, str]]:
    edges: set[tuple[str, str, str]] = set()
    for request in transport.requests:
        for rel in request.relationships:
            relationship_name = rel.relation_reference.rsplit("/relations/", 1)[-1]
            edges.add((rel.source.record_id, rel.target.record_id, relationship_name))
    return edges


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Book", "title": "T"},
            {"id": "b", "node_type": "Library"},
        ],
        [{"source": "a", "target": "b", "relationship": "inLibrary"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    record_ids = {record.record_id for record in transport.requests[0].records}
    assert record_ids == {"a", "b"}


@pytest.mark.asyncio
async def test_ingest_libraries_maps_library_nodes(ingest):
    service, transport = ingest
    res = await ingest_libraries(
        {"libraries": [{"id": "lib-1", "name": "Audiobooks", "mediaType": "book"}]},
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    node = _node(transport, "audiobookshelf:library:lib-1")
    assert node["name"] == "Audiobooks"
    assert node["mediaType"] == "book"
    assert node["externalToolId"] == "lib-1"


@pytest.mark.asyncio
async def test_ingest_library_items_maps_book_author_series_links(ingest):
    service, transport = ingest
    res = await ingest_library_items(
        {
            "results": [
                {
                    "id": "item-9",
                    "mediaType": "book",
                    "libraryId": "lib-1",
                    "media": {
                        "duration": 3600,
                        "numTracks": 12,
                        "coverPath": "/covers/9.jpg",
                        "metadata": {
                            "title": "The Hobbit",
                            "authors": [{"id": "au-1", "name": "Tolkien"}],
                            "series": [{"id": "se-1", "name": "Middle-earth"}],
                            "narratorName": "Serkis",
                            "isbn": "12345",
                        },
                    },
                }
            ]
        },
        ingest=service,
    )
    # 1 book + 1 author + 1 series
    assert res == {"nodes": 3, "edges": 3}
    book = _node(transport, "audiobookshelf:book:item-9")
    assert book["title"] == "The Hobbit"
    assert book["narrator"] == "Serkis"
    assert book["duration"] == 3600
    assert _node(transport, "audiobookshelf:author:au-1")["name"] == "Tolkien"
    assert _node(transport, "audiobookshelf:series:se-1")["name"] == "Middle-earth"
    edges = _edges(transport)
    assert ("audiobookshelf:book:item-9", "audiobookshelf:author:au-1", "writtenBy") in edges
    assert (
        "audiobookshelf:book:item-9",
        "audiobookshelf:series:se-1",
        "partOfSeries",
    ) in edges
    assert (
        "audiobookshelf:book:item-9",
        "audiobookshelf:library:lib-1",
        "inLibrary",
    ) in edges


@pytest.mark.asyncio
async def test_ingest_library_items_maps_podcast(ingest):
    service, transport = ingest
    res = await ingest_library_items(
        [
            {
                "id": "pod-1",
                "mediaType": "podcast",
                "media": {"metadata": {"title": "Daily", "feedUrl": "http://f"}},
            }
        ],
        library_id="lib-2",
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    pod = _node(transport, "audiobookshelf:podcast:pod-1")
    assert pod["feedUrl"] == "http://f"


@pytest.mark.asyncio
async def test_ingest_authors_maps_author_nodes_and_library_link(ingest):
    service, transport = ingest
    res = await ingest_authors(
        {"authors": [{"id": "au-2", "name": "Le Guin", "numBooks": 20}]},
        library_id="lib-1",
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    assert _node(transport, "audiobookshelf:author:au-2")["numBooks"] == 20
    assert _edges(transport) == {
        (
            "audiobookshelf:author:au-2",
            "audiobookshelf:library:lib-1",
            "inLibrary",
        )
    }


@pytest.mark.asyncio
async def test_ingest_noops_without_engine():
    # No injected ingest + no configured engine -> clean no-op (best-effort surface).
    assert await ingest_entities([{"id": "a", "node_type": "Book"}]) is None


@pytest.mark.asyncio
async def test_ingest_rejects_retired_structural_alias_as_noop(ingest):
    # audiobookshelf_mcp's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating an ingest error.
    service, transport = ingest
    assert await ingest_entities([{"id": "a", "type": "Book"}], ingest=service) is None
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_empty_is_noop(ingest):
    service, _transport = ingest
    assert await ingest_entities([], ingest=service) is None
    assert await ingest_libraries({"libraries": []}, ingest=service) is None
    assert await ingest_library_items([], ingest=service) is None
    assert await ingest_authors([], ingest=service) is None

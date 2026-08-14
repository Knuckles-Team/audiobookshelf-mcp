"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_libraries`` / ``ingest_library_items``
/ ``ingest_authors`` seam with a fake ChangeEnvelope-capable engine client (no engine
required), asserting the committed nodes/edges and the Audiobookshelf record -> :Library
/ :Book / :Author / :Series mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake client mirrors agent-utilities' own sanctioned test double
(``agent-utilities/tests/knowledge_graph/test_native_ingest.py``) — the ``txn``-only
fake is retired; ``native_ingest`` now hard-requires an injected client exposing
``.changes``/``.nodes``/``.rdf``/``.supports()``. Like gramps-mcp,
``audiobookshelf_mcp.kg_ingest`` is a **best-effort** surface (its MCP tools must never
raise when the KG stack is down), so it converts ``NativeIngestError`` into ``None``
rather than propagating it — those semantics are exercised explicitly below.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from audiobookshelf_mcp.kg_ingest import (
    ingest_authors,
    ingest_entities,
    ingest_libraries,
    ingest_library_items,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Book", "title": "T"},
            {"id": "b", "node_type": "Library"},
        ],
        [{"source": "a", "target": "b", "relationship": "inLibrary"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "audiobookshelf-mcp"
    assert c.nodes.values["a"]["domain"] == "audiobookshelf"
    assert c.changes.edges == [("a", "b", {"relationship": "inLibrary"})]


def test_ingest_libraries_maps_library_nodes():
    c = _FakeClient()
    res = ingest_libraries(
        {"libraries": [{"id": "lib-1", "name": "Audiobooks", "mediaType": "book"}]},
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert len(c.changes.applied) == 1
    node = c.nodes.values["audiobookshelf:library:lib-1"]
    assert node["node_type"] == "Library"
    assert node["name"] == "Audiobooks"
    assert node["mediaType"] == "book"
    assert node["externalToolId"] == "lib-1"


def test_ingest_library_items_maps_book_author_series_links():
    c = _FakeClient()
    res = ingest_library_items(
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
        client=c,
    )
    # 1 book + 1 author + 1 series
    assert res == {"nodes": 3, "edges": 3}
    assert len(c.changes.applied) == 1
    book = c.nodes.values["audiobookshelf:book:item-9"]
    assert book["node_type"] == "Book"
    assert book["title"] == "The Hobbit"
    assert book["narrator"] == "Serkis"
    assert book["duration"] == 3600
    assert c.nodes.values["audiobookshelf:author:au-1"]["node_type"] == "Author"
    assert c.nodes.values["audiobookshelf:series:se-1"]["node_type"] == "Series"
    edge_types = {(s, t, p["relationship"]) for s, t, p in c.changes.edges}
    assert (
        "audiobookshelf:book:item-9",
        "audiobookshelf:author:au-1",
        "writtenBy",
    ) in edge_types
    assert (
        "audiobookshelf:book:item-9",
        "audiobookshelf:series:se-1",
        "partOfSeries",
    ) in edge_types
    assert (
        "audiobookshelf:book:item-9",
        "audiobookshelf:library:lib-1",
        "inLibrary",
    ) in edge_types


def test_ingest_library_items_maps_podcast():
    c = _FakeClient()
    res = ingest_library_items(
        [
            {
                "id": "pod-1",
                "mediaType": "podcast",
                "media": {"metadata": {"title": "Daily", "feedUrl": "http://f"}},
            }
        ],
        library_id="lib-2",
        client=c,
    )
    assert res == {"nodes": 1, "edges": 1}
    assert len(c.changes.applied) == 1
    pod = c.nodes.values["audiobookshelf:podcast:pod-1"]
    assert pod["node_type"] == "Podcast"
    assert pod["feedUrl"] == "http://f"


def test_ingest_authors_maps_author_nodes_and_library_link():
    c = _FakeClient()
    res = ingest_authors(
        {"authors": [{"id": "au-2", "name": "Le Guin", "numBooks": 20}]},
        library_id="lib-1",
        client=c,
    )
    assert res == {"nodes": 1, "edges": 1}
    assert len(c.changes.applied) == 1
    assert c.nodes.values["audiobookshelf:author:au-2"]["numBooks"] == 20
    assert c.changes.edges == [
        (
            "audiobookshelf:author:au-2",
            "audiobookshelf:library:lib-1",
            {"relationship": "inLibrary"},
        )
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op (best-effort surface).
    assert ingest_entities([{"id": "a", "node_type": "Book"}]) is None


def test_ingest_rejects_retired_structural_alias_as_noop():
    # audiobookshelf_mcp's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating NativeIngestError.
    c = _FakeClient()
    assert ingest_entities([{"id": "a", "type": "Book"}], client=c) is None
    assert c.changes.applied == []


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_libraries({"libraries": []}, client=_FakeClient()) is None
    assert ingest_library_items([], client=_FakeClient()) is None
    assert ingest_authors([], client=_FakeClient()) is None

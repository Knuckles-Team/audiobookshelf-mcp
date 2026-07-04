"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_libraries`` / ``ingest_library_items``
/ ``ingest_authors`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the Audiobookshelf record → :Library / :Book /
:Author / :Series mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from audiobookshelf_mcp.kg_ingest import (
    ingest_authors,
    ingest_entities,
    ingest_libraries,
    ingest_library_items,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Book", "title": "T"},
            {"id": "b", "type": "Library"},
        ],
        [{"source": "a", "target": "b", "type": "inLibrary"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "audiobookshelf-mcp"
    assert c.txn.nodes["a"]["domain"] == "audiobookshelf"
    assert c.edges.edges == [("a", "b", {"type": "inLibrary"})]


def test_ingest_libraries_maps_library_nodes():
    c = _FakeClient()
    res = ingest_libraries(
        {"libraries": [{"id": "lib-1", "name": "Audiobooks", "mediaType": "book"}]},
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["audiobookshelf:library:lib-1"]
    assert node["type"] == "Library"
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
        graph="__commons__",
    )
    # 1 book + 1 author + 1 series
    assert res == {"nodes": 3, "edges": 3}
    book = c.txn.nodes["audiobookshelf:book:item-9"]
    assert book["type"] == "Book"
    assert book["title"] == "The Hobbit"
    assert book["narrator"] == "Serkis"
    assert book["duration"] == 3600
    assert c.txn.nodes["audiobookshelf:author:au-1"]["type"] == "Author"
    assert c.txn.nodes["audiobookshelf:series:se-1"]["type"] == "Series"
    edge_types = {(s, t, p["type"]) for s, t, p in c.edges.edges}
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 1}
    pod = c.txn.nodes["audiobookshelf:podcast:pod-1"]
    assert pod["type"] == "Podcast"
    assert pod["feedUrl"] == "http://f"


def test_ingest_authors_maps_author_nodes_and_library_link():
    c = _FakeClient()
    res = ingest_authors(
        {"authors": [{"id": "au-2", "name": "Le Guin", "numBooks": 20}]},
        library_id="lib-1",
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 1}
    assert c.txn.nodes["audiobookshelf:author:au-2"]["numBooks"] == 20
    assert c.edges.edges == [
        (
            "audiobookshelf:author:au-2",
            "audiobookshelf:library:lib-1",
            {"type": "inLibrary"},
        )
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Book"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_libraries({"libraries": []}, client=_FakeClient()) is None
    assert ingest_library_items([], client=_FakeClient()) is None
    assert ingest_authors([], client=_FakeClient()) is None

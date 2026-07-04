"""Native epistemic-graph blob ingestion — Wire-First cover-art coverage.

Exercises the real ``store_cover`` / ``fetch_and_store_item_cover`` seam with a fake
``MediaStore`` and a fake authenticated session (no engine required).
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from audiobookshelf_mcp.kg_media import fetch_and_store_item_cover, store_cover


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="media:cover1", digest="cover1")


def test_store_cover_stores_bytes_and_metadata():
    store = _FakeMediaStore()
    res = store_cover(
        b"\xff\xd8jpegbytes",
        owner_id="audiobookshelf:book:item-9",
        name="The Hobbit",
        mime_type="image/jpeg",
        store=store,
        extra={"abs_item_id": "item-9"},
    )
    assert res is not None
    assert res["asset_id"] == "media:cover1"
    assert res["media_type"] == "image"
    assert res["size_bytes"] == len(b"\xff\xd8jpegbytes")

    assert len(store.calls) == 1
    data, kw = store.calls[0]
    assert data == b"\xff\xd8jpegbytes"
    assert kw["media_type"] == "image"
    assert kw["mime_type"] == "image/jpeg"
    assert kw["source"] == "audiobookshelf-mcp"
    assert kw["name"] == "The Hobbit"
    assert kw["extra"]["owner_id"] == "audiobookshelf:book:item-9"
    assert kw["extra"]["abs_item_id"] == "item-9"


def test_store_cover_noop_without_bytes():
    assert store_cover(b"", owner_id="x", store=_FakeMediaStore()) is None


def test_store_cover_noops_without_engine():
    # No injected store + no reachable engine -> clean no-op.
    assert store_cover(b"bytes", owner_id="x") is None


class _FakeResponse:
    def __init__(self, content, content_type="image/png"):
        self.content = content
        self.headers = {"Content-Type": content_type}

    def raise_for_status(self):
        return None


class _FakeSession:
    def __init__(self, response):
        self._response = response
        self.requested = []

    def get(self, url, **kw):
        self.requested.append(url)
        return self._response


class _FakeClient:
    def __init__(self, response):
        self.session = _FakeSession(response)
        self.base_url = "http://abs.test"
        self.verify = True


def test_fetch_and_store_item_cover_pulls_and_stores():
    store = _FakeMediaStore()
    client = _FakeClient(_FakeResponse(b"pngbytes", "image/png"))
    res = fetch_and_store_item_cover(client, "item-9", name="The Hobbit", store=store)

    assert res is not None
    assert res["media_type"] == "image"
    assert client.session.requested == ["http://abs.test/api/items/item-9/cover"]
    _, kw = store.calls[0]
    assert kw["mime_type"] == "image/png"
    assert kw["extra"]["owner_id"] == "audiobookshelf:book:item-9"
    assert kw["extra"]["abs_item_id"] == "item-9"


def test_fetch_cover_noops_without_session():
    class _NoSession:
        session = None
        base_url = ""

    assert fetch_and_store_item_cover(_NoSession(), "item-9") is None

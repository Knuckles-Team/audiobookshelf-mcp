"""Native epistemic-graph blob ingestion for Audiobookshelf cover art.

CONCEPT:AU-KG.ingest.list-durable-media. Audiobookshelf items carry cover images (and
audio tracks); this seam captures those raw bytes as content-addressed **blobs** with a
``:MediaAsset`` node in one cross-modal ACID commit via the shared ``MediaStore`` (obtained
through :func:`audiobookshelf_mcp.kg_ingest.media_store`). This makes the raw cover/audio
bytes — not just a server path — durable, deduped and queryable inside the knowledge graph,
and links them back to the owning ``:Book`` / ``:Podcast`` / ``:Author`` via ``:hasCover``.

Entirely best-effort and engine-guarded: with no live engine every entry point **no-ops**
(returns ``None``), so the connector runs with zero KG infrastructure. Never raises.
"""

from __future__ import annotations

import logging
from typing import Any

from .kg_ingest import media_store

logger = logging.getLogger("audiobookshelf_mcp.kg_media")

_SOURCE = "audiobookshelf-mcp"


def store_cover(
    data: bytes | None,
    *,
    owner_id: str,
    name: str | None = None,
    mime_type: str = "image/jpeg",
    source: str = _SOURCE,
    extra: dict[str, Any] | None = None,
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Store cover/portrait bytes as an ``image`` blob + ``:MediaAsset``.

    ``owner_id`` is the node id of the owning ``:Book`` / ``:Podcast`` / ``:Author``
    (carried onto the asset's ``extra`` as ``owner_id`` so a ``:hasCover`` link can be
    resolved hub-side). Returns ``{asset_id, digest, size_bytes, media_type}`` on
    success, or ``None`` (no engine / no bytes / store failed). ``store`` may be
    injected for tests.
    """
    if not data:
        return None
    st = store if store is not None else media_store()
    if st is None:
        return None

    meta = {"owner_id": owner_id}
    if extra:
        meta.update({k: v for k, v in extra.items() if v is not None})

    try:
        stored = st.store_media(
            data,
            media_type="image",
            mime_type=mime_type,
            source=source,
            name=name or owner_id,
            extra=meta,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("KG media ingest: store_media failed: %s", e)
        return None
    if stored is None:
        return None

    logger.info(
        "KG media ingest: stored cover for %s (%d bytes) as asset %s",
        owner_id,
        len(data),
        getattr(stored, "asset_id", "?"),
    )
    return {
        "asset_id": getattr(stored, "asset_id", None),
        "digest": getattr(stored, "digest", None),
        "size_bytes": len(data),
        "media_type": "image",
    }


def fetch_and_store_item_cover(
    client: Any,
    item_id: str,
    *,
    name: str | None = None,
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Fetch a library item's cover via the client session and store it as a blob.

    Uses the Audiobookshelf ``GET /api/items/{id}/cover`` endpoint on the client's
    authenticated ``requests`` session. Best-effort: any transport error → ``None``.
    """
    session = getattr(client, "session", None)
    base_url = getattr(client, "base_url", None)
    if session is None or not base_url:
        return None
    try:
        resp = session.get(
            f"{base_url}/api/items/{item_id}/cover",
            verify=getattr(client, "verify", True),
        )
        resp.raise_for_status()
        data = resp.content
        mime = resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
    except Exception as e:  # noqa: BLE001 — cover fetch is best-effort
        logger.debug("KG media ingest: cover fetch failed for %s: %s", item_id, e)
        return None
    return store_cover(
        data,
        owner_id=f"audiobookshelf:book:{item_id}",
        name=name,
        mime_type=mime or "image/jpeg",
        store=store,
        extra={"abs_item_id": item_id},
    )

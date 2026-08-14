"""Native epistemic-graph ingestion for Audiobookshelf records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (``:Library``,
``:Book``, ``:Podcast``, ``:Author``, ``:Series``) + links, matching the classes federated
by ``audiobookshelf_mcp.ontology``.

The txn write path itself is the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` — this module is only the thin
**mapper** (Audiobookshelf records → entity / document dicts); there is no self-contained
fallback transaction here.

The MCP tool surface (``audiobookshelf_mcp.mcp.mcp_ingest``) exposes these as best-effort
tools that must never raise on an unreachable/misconfigured KG stack, so
``ingest_entities`` / ``ingest_documents`` stay **best-effort**: they return ``None``
(never raise) for empty input or when the shared primitive reports
:class:`NativeIngestError` (no reachable engine, or a malformed record). Node ids follow
``audiobookshelf:<class>:<externalId>`` and each ``node_type`` matches a class the
package's ontology federates.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    NativeIngestError,
    ingest_documents as _native_ingest_documents,
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("audiobookshelf_mcp.kg")

_SOURCE = "audiobookshelf-mcp"
_DOMAIN = "audiobookshelf"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into the engine. Best-effort, never raises.

    ``entities``: ``[{"id":..., "node_type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "relationship":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (empty input / no reachable engine /
    malformed record). ``client``/``graph`` may be injected (tests); otherwise the
    process-owned governed authority is resolved on demand.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    try:
        return _native_ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder). Best-effort.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``. Never raises.
    """
    if not documents:
        return None
    try:
        return _native_ingest_documents(
            documents, source=source, domain=domain, client=client, graph=graph
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def media_store() -> Any | None:
    """Return a shared :class:`MediaStore` over a live engine (raw-blob ingestion), or ``None``."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest.media_store()
    except Exception as e:  # noqa: BLE001 — shared primitive not present yet
        logger.debug("KG ingest: shared media_store unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — no reachable engine
        logger.debug("KG media ingest: engine unreachable: %s", e)
        return None


# --------------------------------------------------------------------------- #
# Domain mappers — Audiobookshelf records → typed entity / document dicts.     #
# --------------------------------------------------------------------------- #
def _unwrap(resp: Any, *keys: str) -> list[dict[str, Any]]:
    """Coerce an API response into a list of record dicts.

    Accepts a bare list, a single dict record, or a dict wrapping the records under
    one of ``keys`` (e.g. ``libraries``, ``results``, ``authors``).
    """
    if resp is None:
        return []
    if hasattr(resp, "model_dump"):
        resp = resp.model_dump()
    if isinstance(resp, list):
        return [r for r in resp if isinstance(r, dict)]
    if isinstance(resp, dict):
        for key in keys:
            val = resp.get(key)
            if isinstance(val, list):
                return [r for r in val if isinstance(r, dict)]
        # a single record dict that looks like one of our entities
        if resp.get("id") is not None:
            return [resp]
    return []


def ingest_libraries(
    libraries: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Audiobookshelf library records → ``:Library`` nodes and ingest."""
    entities: list[dict[str, Any]] = []
    for lib in _unwrap(libraries, "libraries", "results"):
        lid = lib.get("id")
        if lid is None:
            continue
        entities.append(
            {
                "id": f"audiobookshelf:library:{lid}",
                "node_type": "Library",
                "name": lib.get("name"),
                "mediaType": lib.get("mediaType"),
                "provider": lib.get("provider"),
                "externalToolId": str(lid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def _book_metadata(item: dict[str, Any]) -> dict[str, Any]:
    media = item.get("media") or {}
    return media.get("metadata") or {}


def ingest_library_items(
    items: Any,
    *,
    library_id: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map library items → ``:Book`` / ``:Podcast`` nodes with author/series/library links.

    Handles both book and podcast media types. Books gain ``:writtenBy`` (Author),
    ``:partOfSeries`` (Series) and ``:inLibrary`` (Library) edges; every item gains
    ``:inLibrary`` when a library id is known.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    seen: set[str] = set()

    def _add(ent: dict[str, Any]) -> None:
        if ent["id"] not in seen:
            seen.add(ent["id"])
            entities.append(ent)

    for item in _unwrap(items, "results", "libraryItems", "items"):
        iid = item.get("id")
        if iid is None:
            continue
        media_type = item.get("mediaType") or "book"
        meta = _book_metadata(item)
        media = item.get("media") or {}
        lib_id = library_id or item.get("libraryId")

        if media_type == "podcast":
            node_id = f"audiobookshelf:podcast:{iid}"
            _add(
                {
                    "id": node_id,
                    "node_type": "Podcast",
                    "title": meta.get("title"),
                    "mediaType": "podcast",
                    "feedUrl": meta.get("feedUrl"),
                    "publishedYear": meta.get("releaseDate"),
                    "coverPath": media.get("coverPath") or item.get("coverPath"),
                    "externalToolId": str(iid),
                }
            )
        else:
            node_id = f"audiobookshelf:book:{iid}"
            _add(
                {
                    "id": node_id,
                    "node_type": "Book",
                    "title": meta.get("title"),
                    "subtitle": meta.get("subtitle"),
                    "mediaType": "book",
                    "publishedYear": meta.get("publishedYear"),
                    "isbn": meta.get("isbn"),
                    "asin": meta.get("asin"),
                    "narrator": meta.get("narratorName"),
                    "duration": media.get("duration"),
                    "numTracks": media.get("numTracks"),
                    "coverPath": media.get("coverPath") or item.get("coverPath"),
                    "externalToolId": str(iid),
                }
            )
            # authors -> :Author + :writtenBy
            for author in meta.get("authors") or []:
                aid = author.get("id") if isinstance(author, dict) else None
                aname = author.get("name") if isinstance(author, dict) else author
                if not aid and not aname:
                    continue
                akey = aid or aname
                author_id = f"audiobookshelf:author:{akey}"
                _add(
                    {
                        "id": author_id,
                        "node_type": "Author",
                        "name": aname,
                        "externalToolId": str(akey),
                    }
                )
                relationships.append(
                    {
                        "source": node_id,
                        "target": author_id,
                        "relationship": "writtenBy",
                    }
                )
            # narrator (Person) — fall back to :narratedBy on the book props only
            # series -> :Series + :partOfSeries
            for series in meta.get("series") or []:
                sid = series.get("id") if isinstance(series, dict) else None
                sname = series.get("name") if isinstance(series, dict) else series
                if not sid and not sname:
                    continue
                skey = sid or sname
                series_id = f"audiobookshelf:series:{skey}"
                _add(
                    {
                        "id": series_id,
                        "node_type": "Series",
                        "name": sname,
                        "externalToolId": str(skey),
                    }
                )
                relationships.append(
                    {
                        "source": node_id,
                        "target": series_id,
                        "relationship": "partOfSeries",
                    }
                )

        if lib_id is not None:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"audiobookshelf:library:{lib_id}",
                    "relationship": "inLibrary",
                }
            )

    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_authors(
    authors: Any,
    *,
    library_id: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map author records → ``:Author`` nodes (+ ``:inLibrary`` when a library is known)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for author in _unwrap(authors, "authors", "results"):
        aid = author.get("id")
        if aid is None:
            continue
        author_id = f"audiobookshelf:author:{aid}"
        entities.append(
            {
                "id": author_id,
                "node_type": "Author",
                "name": author.get("name"),
                "description": author.get("description"),
                "numBooks": author.get("numBooks"),
                "imagePath": author.get("imagePath"),
                "externalToolId": str(aid),
            }
        )
        if library_id is not None:
            relationships.append(
                {
                    "source": author_id,
                    "target": f"audiobookshelf:library:{library_id}",
                    "relationship": "inLibrary",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)

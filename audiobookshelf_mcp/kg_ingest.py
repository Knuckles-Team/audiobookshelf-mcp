"""Native epistemic-graph ingestion for Audiobookshelf records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (``:Library``,
``:Book``, ``:Podcast``, ``:Author``, ``:Series``) + links, matching the classes federated
by ``audiobookshelf_mcp.ontology``.

The txn write path itself is the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` — this module is only the thin
**mapper** (Audiobookshelf records → entity / document dicts). The primitive import is
guarded: if the shared helper (or a live engine) is unavailable, a self-contained txn
fallback over the lightweight ``GraphComputeEngine`` client is used, and if even that is
absent every entry point **no-ops** (returns ``None``), so the connector runs with zero KG
infrastructure. Node ids follow ``audiobookshelf:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("audiobookshelf_mcp.kg")

_SOURCE = "audiobookshelf-mcp"
_DOMAIN = "audiobookshelf"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------- #
# Write path — prefer the shared primitive, fall back to a self-contained txn. #
# --------------------------------------------------------------------------- #
def _native_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write_nodes(
    client: Any,
    graph: str,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    source: str,
    domain: str,
) -> dict[str, int] | None:
    """Self-contained txn write, used when the shared primitive is not importable."""
    nodes = [n for n in nodes if n.get("id")]
    if not nodes:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest[%s]: wrote %d nodes, %d edges", domain, len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into the engine.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None``. ``client``/``graph`` may be
    injected (tests); otherwise resolved on demand. Never raises.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    # Prefer the shared fleet primitive when it is installed AND we are not under an
    # injected client (tests inject a fake client to exercise the txn path directly).
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_entities as _shared_ingest,
            )

            return _shared_ingest(
                entities,
                relationships,
                source=source,
                domain=domain,
                graph=graph,
            )
        except Exception as e:  # noqa: BLE001 — shared primitive not present yet
            logger.debug("KG ingest: shared primitive unavailable: %s", e)
        client, graph = _native_client()
    if client is None:
        return None
    return _fallback_write_nodes(
        client,
        graph or _DEFAULT_GRAPH,
        entities,
        relationships,
        source=source,
        domain=domain,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``. Never raises.
    """
    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_documents as _shared_docs,
            )

            return _shared_docs(documents, source=source, domain=domain, graph=graph)
        except Exception as e:  # noqa: BLE001 — shared primitive not present yet
            logger.debug("KG ingest: shared doc primitive unavailable: %s", e)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    nodes: list[dict[str, Any]] = []
    for doc in documents or []:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        node.setdefault("created_at", now)
        nodes.append(node)
    if not nodes:
        return None
    if client is None:
        client, graph = _native_client()
    if client is None:
        return None
    return _fallback_write_nodes(
        client, graph or _DEFAULT_GRAPH, nodes, None, source=source, domain=domain
    )


def media_store() -> Any | None:
    """Return a shared :class:`MediaStore` over a live engine (raw-blob ingestion), or ``None``."""
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            media_store as _shared_media_store,
        )

        return _shared_media_store()
    except Exception as e:  # noqa: BLE001 — shared primitive not present yet
        logger.debug("KG ingest: shared media_store unavailable: %s", e)
    client, _ = _native_client()
    if client is None:
        return None
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore

        return MediaStore(GraphComputeEngine())
    except Exception as e:  # noqa: BLE001
        logger.debug("KG ingest: media_store build failed: %s", e)
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
                "type": "Library",
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
                    "type": "Podcast",
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
                    "type": "Book",
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
                        "type": "Author",
                        "name": aname,
                        "externalToolId": str(akey),
                    }
                )
                relationships.append(
                    {"source": node_id, "target": author_id, "type": "writtenBy"}
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
                        "type": "Series",
                        "name": sname,
                        "externalToolId": str(skey),
                    }
                )
                relationships.append(
                    {"source": node_id, "target": series_id, "type": "partOfSeries"}
                )

        if lib_id is not None:
            relationships.append(
                {
                    "source": node_id,
                    "target": f"audiobookshelf:library:{lib_id}",
                    "type": "inLibrary",
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
                "type": "Author",
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
                    "type": "inLibrary",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)

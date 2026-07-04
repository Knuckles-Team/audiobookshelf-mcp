import json

from agent_utilities.mcp_utilities import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_ingest_tools(mcp: FastMCP):
    """Register native knowledge-graph ingestion tools. CONCEPT:AU-KG.ingest.enterprise-source-extractor"""

    @mcp.tool(tags={"ingest", "kg"})
    async def audiobookshelf_ingest_libraries(
        params_json: str = Field(
            default="{}",
            description=(
                'JSON string of options: {"library_id": optional id to scope to one '
                'library, "include_items": bool (default true) to also ingest books/'
                'podcasts, "include_authors": bool (default true), "include_covers": '
                "bool (default false) to also capture item cover art as blobs, "
                '"item_params": object of extra get_library_items filters}.'
            ),
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Natively ingest Audiobookshelf libraries into epistemic-graph as typed nodes.

        Lists libraries via the Audiobookshelf API and pushes them as ``:Library`` nodes;
        for each library it optionally lists items (``:Book`` / ``:Podcast`` with
        ``:writtenBy`` / ``:partOfSeries`` / ``:inLibrary`` links) and authors
        (``:Author``), and optionally captures item cover art as ``:MediaAsset`` blobs.
        Best-effort: returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from ..kg_ingest import (
            ingest_authors,
            ingest_libraries,
            ingest_library_items,
        )
        from ..kg_media import fetch_and_store_item_cover

        try:
            opts = json.loads(params_json) if params_json else {}
        except Exception as e:  # noqa: BLE001
            return {"error": f"Invalid params_json: {e}"}

        library_id = opts.get("library_id")
        include_items = opts.get("include_items", True)
        include_authors = opts.get("include_authors", True)
        include_covers = opts.get("include_covers", False)
        item_params = opts.get("item_params") or {}

        if ctx:
            await ctx.info(
                "Ingesting Audiobookshelf libraries into the knowledge graph..."
            )

        if library_id:
            lib_resp = await run_blocking(client.get_library_by_id, id=library_id)
            libraries = [lib_resp] if lib_resp else []
        else:
            lib_resp = await run_blocking(client.get_libraries)
            libraries = (
                lib_resp.get("libraries", [])
                if isinstance(lib_resp, dict)
                else (lib_resp or [])
            )

        summary: dict = {"libraries": ingest_libraries(libraries)}
        items_res: list = []
        authors_res: list = []
        covers = 0

        for lib in libraries:
            lid = lib.get("id") if isinstance(lib, dict) else None
            if lid is None:
                continue
            if include_items:
                items_resp = await run_blocking(
                    client.get_library_items, id=lid, **item_params
                )
                items_res.append(ingest_library_items(items_resp, library_id=lid))
                if include_covers:
                    results = (
                        items_resp.get("results", [])
                        if isinstance(items_resp, dict)
                        else (items_resp or [])
                    )
                    for it in results:
                        iid = it.get("id") if isinstance(it, dict) else None
                        if not iid:
                            continue
                        stored = fetch_and_store_item_cover(client, iid)
                        if stored:
                            covers += 1
            if include_authors:
                authors_resp = await run_blocking(client.get_library_authors, id=lid)
                authors_res.append(ingest_authors(authors_resp, library_id=lid))

        summary["items"] = items_res
        summary["authors"] = authors_res
        summary["covers_stored"] = covers
        return {"listed_libraries": len(libraries), "ingested": summary}

    return None

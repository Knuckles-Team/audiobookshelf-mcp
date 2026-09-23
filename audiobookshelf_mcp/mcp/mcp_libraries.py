from typing import Literal

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


# One tiny extracted handler per action -- each preserves the exact
# client-method call and kwargs passthrough the if/elif chain used to
# perform inline. Kept module-level (not nested) so each has CCN 1 and
# is independently addressable/testable.
async def _libraries_list(client, **kwargs):
    return await run_blocking(client.get_libraries, **kwargs)


async def _libraries_create(client, **kwargs):
    return await run_blocking(client.create_library, **kwargs)


async def _libraries_get(client, **kwargs):
    return await run_blocking(client.get_library_by_id, **kwargs)


async def _libraries_update(client, **kwargs):
    return await run_blocking(client.update_library_by_id, **kwargs)


async def _libraries_delete(client, **kwargs):
    return await run_blocking(client.delete_library_by_id, **kwargs)


async def _libraries_authors(client, **kwargs):
    return await run_blocking(client.get_library_authors, **kwargs)


async def _libraries_delete_issues(client, **kwargs):
    return await run_blocking(client.delete_library_issues, **kwargs)


async def _libraries_items(client, **kwargs):
    return await run_blocking(client.get_library_items, **kwargs)


async def _libraries_series(client, **kwargs):
    return await run_blocking(client.get_library_series, **kwargs)


async def _libraries_series_by_id(client, **kwargs):
    return await run_blocking(client.get_library_series_by_id, **kwargs)


_LIBRARIES_ACTION_HANDLERS = {
    "list": _libraries_list,
    "create": _libraries_create,
    "get": _libraries_get,
    "update": _libraries_update,
    "delete": _libraries_delete,
    "authors": _libraries_authors,
    "delete_issues": _libraries_delete_issues,
    "items": _libraries_items,
    "series": _libraries_series,
}


def register_libraries_tools(mcp: FastMCP):
    """Register library-management dynamic tools. CONCEPT:AS-OS.identity.abs"""

    @mcp.tool(
        tags={"libraries"},
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": True,
        },
        meta={
            "eg.annotations": {"modalities_in": ["text"], "modalities_out": ["text"]}
        },
    )
    async def library_operations(
        action: Literal[
            "authors",
            "create",
            "delete",
            "delete_issues",
            "get",
            "items",
            "list",
            "series",
            "series_by_id",
            "update",
        ] = Field(
            description=(
                "Action to perform. One of: 'list', 'create', 'get', 'update', "
                "'delete', 'authors', 'delete_issues', 'items', 'series', "
                "'series_by_id'."
            )
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters for the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage Audiobookshelf libraries. CONCEPT:AS-OS.identity.abs"""
        if ctx:
            await ctx.info("Executing Audiobookshelf library operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

        resolved = resolve_action(
            action,
            {
                "list",
                "create",
                "get",
                "update",
                "delete",
                "authors",
                "delete_issues",
                "items",
                "series",
                "series_by_id",
            },
            service="audiobookshelf-mcp",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _LIBRARIES_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        return await _libraries_series_by_id(client, **kwargs)

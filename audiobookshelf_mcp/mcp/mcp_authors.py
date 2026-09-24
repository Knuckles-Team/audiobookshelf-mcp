from agent_connector_sdk.mcp.action_dispatch import resolve_action
from agent_connector_sdk.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


# One tiny extracted handler per action -- each preserves the exact
# client-method call and kwargs passthrough the if/elif chain used to
# perform inline. Kept module-level (not nested) so each has CCN 1 and
# is independently addressable/testable.
async def _authors_get(client, **kwargs):
    return await run_blocking(client.get_author_by_id, **kwargs)


async def _authors_update(client, **kwargs):
    return await run_blocking(client.update_author_by_id, **kwargs)


async def _authors_delete(client, **kwargs):
    return await run_blocking(client.delete_author_by_id, **kwargs)


async def _authors_get_image(client, **kwargs):
    return await run_blocking(client.get_author_image_by_id, **kwargs)


async def _authors_add_image(client, **kwargs):
    return await run_blocking(client.add_author_image_by_id, **kwargs)


async def _authors_update_image(client, **kwargs):
    return await run_blocking(client.update_author_image_by_id, **kwargs)


async def _authors_delete_image(client, **kwargs):
    return await run_blocking(client.delete_author_image_by_id, **kwargs)


async def _authors_match(client, **kwargs):
    return await run_blocking(client.match_author_by_id, **kwargs)


_AUTHORS_ACTION_HANDLERS = {
    "get": _authors_get,
    "update": _authors_update,
    "delete": _authors_delete,
    "get_image": _authors_get_image,
    "add_image": _authors_add_image,
    "update_image": _authors_update_image,
    "delete_image": _authors_delete_image,
}


def register_authors_tools(mcp: FastMCP):
    """Register author dynamic tools. CONCEPT:AS-OS.identity.abs-2"""

    @mcp.tool(tags={"authors"})
    async def author_operations(
        action: str = Field(
            description=(
                "Action to perform. One of: 'get', 'update', 'delete', 'get_image', "
                "'add_image', 'update_image', 'delete_image', 'match'."
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
        """Manage Audiobookshelf authors. CONCEPT:AS-OS.identity.abs-2"""
        if ctx:
            await ctx.info("Executing Audiobookshelf author operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

        resolved = resolve_action(
            action,
            {
                "get",
                "update",
                "delete",
                "get_image",
                "add_image",
                "update_image",
                "delete_image",
                "match",
            },
            service="audiobookshelf-mcp",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _AUTHORS_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        return await _authors_match(client, **kwargs)

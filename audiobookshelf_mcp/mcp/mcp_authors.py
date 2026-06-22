import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_authors_tools(mcp: FastMCP):
    """Register author dynamic tools. CONCEPT:ABS-002"""

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
        """Manage Audiobookshelf authors. CONCEPT:ABS-002"""
        if ctx:
            await ctx.info("Executing author tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

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

        if action == "get":
            return await run_blocking(client.get_author_by_id, **kwargs)
        if action == "update":
            return await run_blocking(client.update_author_by_id, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_author_by_id, **kwargs)
        if action == "get_image":
            return await run_blocking(client.get_author_image_by_id, **kwargs)
        if action == "add_image":
            return await run_blocking(client.add_author_image_by_id, **kwargs)
        if action == "update_image":
            return await run_blocking(client.update_author_image_by_id, **kwargs)
        if action == "delete_image":
            return await run_blocking(client.delete_author_image_by_id, **kwargs)
        return await run_blocking(client.match_author_by_id, **kwargs)

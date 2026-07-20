from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


def register_libraries_tools(mcp: FastMCP):
    """Register library-management dynamic tools. CONCEPT:AS-OS.identity.abs"""

    @mcp.tool(tags={"libraries"})
    async def library_operations(
        action: str = Field(
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

        if action == "list":
            return await run_blocking(client.get_libraries, **kwargs)
        if action == "create":
            return await run_blocking(client.create_library, **kwargs)
        if action == "get":
            return await run_blocking(client.get_library_by_id, **kwargs)
        if action == "update":
            return await run_blocking(client.update_library_by_id, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_library_by_id, **kwargs)
        if action == "authors":
            return await run_blocking(client.get_library_authors, **kwargs)
        if action == "delete_issues":
            return await run_blocking(client.delete_library_issues, **kwargs)
        if action == "items":
            return await run_blocking(client.get_library_items, **kwargs)
        if action == "series":
            return await run_blocking(client.get_library_series, **kwargs)
        return await run_blocking(client.get_library_series_by_id, **kwargs)

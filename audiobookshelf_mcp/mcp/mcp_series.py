from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


def register_series_tools(mcp: FastMCP):
    """Register series dynamic tools. CONCEPT:AS-OS.governance.abs"""

    @mcp.tool(tags={"series"})
    async def series_operations(
        action: str = Field(description="Action to perform. One of: 'get', 'update'."),
        params_json: str = Field(
            default="{}", description="JSON string of parameters for the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage Audiobookshelf series. CONCEPT:AS-OS.governance.abs"""
        if ctx:
            await ctx.info("Executing Audiobookshelf series operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

        resolved = resolve_action(
            action, {"get", "update"}, service="audiobookshelf-mcp"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_series, **kwargs)
        return await run_blocking(client.update_series, **kwargs)

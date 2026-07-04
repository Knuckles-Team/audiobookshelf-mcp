import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


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
            await ctx.info("Executing series tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "update"}, service="audiobookshelf-mcp"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_series, **kwargs)
        return await run_blocking(client.update_series, **kwargs)

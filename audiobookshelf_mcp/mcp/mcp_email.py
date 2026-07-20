from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


def register_email_tools(mcp: FastMCP):
    """Register email/e-reader dynamic tools. CONCEPT:AS-OS.governance.abs-3"""

    @mcp.tool(tags={"email"})
    async def email_operations(
        action: str = Field(
            description=(
                "Action to perform. One of: 'get_settings', 'update_settings', "
                "'update_ereader_devices', 'send_ebook', 'test'."
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
        """Manage Audiobookshelf email settings and e-reader delivery. CONCEPT:AS-OS.governance.abs-3"""
        if ctx:
            await ctx.info("Executing Audiobookshelf email operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

        resolved = resolve_action(
            action,
            {
                "get_settings",
                "update_settings",
                "update_ereader_devices",
                "send_ebook",
                "test",
            },
            service="audiobookshelf-mcp",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_settings":
            return await run_blocking(client.get_email_settings, **kwargs)
        if action == "update_settings":
            return await run_blocking(client.update_email_settings, **kwargs)
        if action == "update_ereader_devices":
            return await run_blocking(client.update_ereader_devices, **kwargs)
        if action == "send_ebook":
            return await run_blocking(client.send_ebook_to_device, **kwargs)
        return await run_blocking(client.send_test_email, **kwargs)

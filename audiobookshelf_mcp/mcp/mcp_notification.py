import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_notification_tools(mcp: FastMCP):
    """Register notification dynamic tools. CONCEPT:AS-OS.governance.abs-4"""

    @mcp.tool(tags={"notification"})
    async def notification_operations(
        action: str = Field(
            description=(
                "Action to perform. One of: 'event_data', 'list', 'configure', "
                "'create', 'test', 'delete', 'update', 'test_one'."
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
        """Manage Audiobookshelf notifications. CONCEPT:AS-OS.governance.abs-4"""
        if ctx:
            await ctx.info("Executing notification tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "event_data",
                "list",
                "configure",
                "create",
                "test",
                "delete",
                "update",
                "test_one",
            },
            service="audiobookshelf-mcp",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "event_data":
            return await run_blocking(client.get_notification_event_data, **kwargs)
        if action == "list":
            return await run_blocking(client.get_notifications, **kwargs)
        if action == "configure":
            return await run_blocking(client.configure_notification_settings, **kwargs)
        if action == "create":
            return await run_blocking(client.create_notification, **kwargs)
        if action == "test":
            return await run_blocking(client.send_default_test_notification, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_notification, **kwargs)
        if action == "update":
            return await run_blocking(client.update_notification, **kwargs)
        return await run_blocking(client.send_test_notification, **kwargs)

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
async def _notification_event_data(client, **kwargs):
    return await run_blocking(client.get_notification_event_data, **kwargs)


async def _notification_list(client, **kwargs):
    return await run_blocking(client.get_notifications, **kwargs)


async def _notification_configure(client, **kwargs):
    return await run_blocking(client.configure_notification_settings, **kwargs)


async def _notification_create(client, **kwargs):
    return await run_blocking(client.create_notification, **kwargs)


async def _notification_test(client, **kwargs):
    return await run_blocking(client.send_default_test_notification, **kwargs)


async def _notification_delete(client, **kwargs):
    return await run_blocking(client.delete_notification, **kwargs)


async def _notification_update(client, **kwargs):
    return await run_blocking(client.update_notification, **kwargs)


async def _notification_test_one(client, **kwargs):
    return await run_blocking(client.send_test_notification, **kwargs)


_NOTIFICATION_ACTION_HANDLERS = {
    "event_data": _notification_event_data,
    "list": _notification_list,
    "configure": _notification_configure,
    "create": _notification_create,
    "test": _notification_test,
    "delete": _notification_delete,
    "update": _notification_update,
}


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
            await ctx.info("Executing Audiobookshelf notification operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

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

        handler = _NOTIFICATION_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        return await _notification_test_one(client, **kwargs)

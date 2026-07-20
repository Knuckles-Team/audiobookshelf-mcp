from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client
from ._params import parse_params_json


def register_podcasts_tools(mcp: FastMCP):
    """Register podcast dynamic tools. CONCEPT:AS-OS.governance.abs-2"""

    @mcp.tool(tags={"podcasts"})
    async def podcast_operations(
        action: str = Field(
            description=(
                "Action to perform. One of: 'create', 'feed', 'opml_create', "
                "'opml_parse', 'check_new', 'clear_queue', 'download_episodes', "
                "'downloads', 'get_episode', 'update_episode', 'remove_episode', "
                "'match_episodes', 'find_episode'."
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
        """Manage Audiobookshelf podcasts and episodes. CONCEPT:AS-OS.governance.abs-2"""
        if ctx:
            await ctx.info("Executing Audiobookshelf podcast operation")
        kwargs, error = parse_params_json(params_json)
        if error:
            return error
        assert kwargs is not None

        resolved = resolve_action(
            action,
            {
                "create",
                "feed",
                "opml_create",
                "opml_parse",
                "check_new",
                "clear_queue",
                "download_episodes",
                "downloads",
                "get_episode",
                "update_episode",
                "remove_episode",
                "match_episodes",
                "find_episode",
            },
            service="audiobookshelf-mcp",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "create":
            return await run_blocking(client.create_podcast, **kwargs)
        if action == "feed":
            return await run_blocking(client.get_podcast_feed, **kwargs)
        if action == "opml_create":
            return await run_blocking(
                client.bulk_create_podcasts_from_opml_feed, **kwargs
            )
        if action == "opml_parse":
            return await run_blocking(client.get_feeds_from_opml_text, **kwargs)
        if action == "check_new":
            return await run_blocking(client.check_new_episodes, **kwargs)
        if action == "clear_queue":
            return await run_blocking(client.clear_episode_download_queue, **kwargs)
        if action == "download_episodes":
            return await run_blocking(client.download_episodes, **kwargs)
        if action == "downloads":
            return await run_blocking(client.get_episode_downloads, **kwargs)
        if action == "get_episode":
            return await run_blocking(client.get_episode, **kwargs)
        if action == "update_episode":
            return await run_blocking(client.update_episode, **kwargs)
        if action == "remove_episode":
            return await run_blocking(client.remove_episode, **kwargs)
        if action == "match_episodes":
            return await run_blocking(client.quick_match_episodes, **kwargs)
        return await run_blocking(client.find_episode, **kwargs)

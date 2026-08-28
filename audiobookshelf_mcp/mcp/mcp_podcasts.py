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
async def _podcasts_create(client, **kwargs):
    return await run_blocking(client.create_podcast, **kwargs)


async def _podcasts_feed(client, **kwargs):
    return await run_blocking(client.get_podcast_feed, **kwargs)


async def _podcasts_opml_create(client, **kwargs):
    return await run_blocking(client.bulk_create_podcasts_from_opml_feed, **kwargs)


async def _podcasts_opml_parse(client, **kwargs):
    return await run_blocking(client.get_feeds_from_opml_text, **kwargs)


async def _podcasts_check_new(client, **kwargs):
    return await run_blocking(client.check_new_episodes, **kwargs)


async def _podcasts_clear_queue(client, **kwargs):
    return await run_blocking(client.clear_episode_download_queue, **kwargs)


async def _podcasts_download_episodes(client, **kwargs):
    return await run_blocking(client.download_episodes, **kwargs)


async def _podcasts_downloads(client, **kwargs):
    return await run_blocking(client.get_episode_downloads, **kwargs)


async def _podcasts_get_episode(client, **kwargs):
    return await run_blocking(client.get_episode, **kwargs)


async def _podcasts_update_episode(client, **kwargs):
    return await run_blocking(client.update_episode, **kwargs)


async def _podcasts_remove_episode(client, **kwargs):
    return await run_blocking(client.remove_episode, **kwargs)


async def _podcasts_match_episodes(client, **kwargs):
    return await run_blocking(client.quick_match_episodes, **kwargs)


async def _podcasts_find_episode(client, **kwargs):
    return await run_blocking(client.find_episode, **kwargs)


_PODCASTS_ACTION_HANDLERS = {
    "create": _podcasts_create,
    "feed": _podcasts_feed,
    "opml_create": _podcasts_opml_create,
    "opml_parse": _podcasts_opml_parse,
    "check_new": _podcasts_check_new,
    "clear_queue": _podcasts_clear_queue,
    "download_episodes": _podcasts_download_episodes,
    "downloads": _podcasts_downloads,
    "get_episode": _podcasts_get_episode,
    "update_episode": _podcasts_update_episode,
    "remove_episode": _podcasts_remove_episode,
    "match_episodes": _podcasts_match_episodes,
}


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

        handler = _PODCASTS_ACTION_HANDLERS.get(action)
        if handler is not None:
            return await handler(client, **kwargs)
        return await _podcasts_find_episode(client, **kwargs)

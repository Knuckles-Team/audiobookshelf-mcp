from .api_client_authors import ApiClientAuthors
from .api_client_base import ApiClientBase
from .api_client_email import ApiClientEmail
from .api_client_libraries import ApiClientLibraries
from .api_client_notification import ApiClientNotification
from .api_client_podcasts import ApiClientPodcasts
from .api_client_series import ApiClientSeries


class ApiClientSystem(
    ApiClientLibraries,
    ApiClientAuthors,
    ApiClientSeries,
    ApiClientPodcasts,
    ApiClientEmail,
    ApiClientNotification,
):
    """Combined Audiobookshelf API client.

    Aggregates every domain mixin into one client so the shared
    ``register_tool_surface`` helper can build the verbose 1:1 tool surface from a
    single ``client_cls`` while the condensed action-routed tools dispatch per domain.
    """


__all__ = [
    "ApiClientBase",
    "ApiClientSystem",
    "ApiClientLibraries",
    "ApiClientAuthors",
    "ApiClientSeries",
    "ApiClientPodcasts",
    "ApiClientEmail",
    "ApiClientNotification",
]

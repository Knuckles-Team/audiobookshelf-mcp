from .api_client_authors import ApiClientAuthors
from .api_client_backups import ApiClientBackups
from .api_client_base import ApiClientBase
from .api_client_collections import ApiClientCollections
from .api_client_email import ApiClientEmail
from .api_client_filesystem import ApiClientFilesystem
from .api_client_items import ApiClientItems
from .api_client_libraries import ApiClientLibraries
from .api_client_libraries_extra import ApiClientLibrariesExtra
from .api_client_me import ApiClientMe
from .api_client_metadata import ApiClientMetadata
from .api_client_notification import ApiClientNotification
from .api_client_playlists import ApiClientPlaylists
from .api_client_podcasts import ApiClientPodcasts
from .api_client_search import ApiClientSearch
from .api_client_series import ApiClientSeries
from .api_client_server import ApiClientServer
from .api_client_sessions import ApiClientSessions
from .api_client_tools import ApiClientTools
from .api_client_users import ApiClientUsers


class ApiClientSystem(
    ApiClientLibraries,
    ApiClientLibrariesExtra,
    ApiClientItems,
    ApiClientMe,
    ApiClientUsers,
    ApiClientSessions,
    ApiClientCollections,
    ApiClientPlaylists,
    ApiClientBackups,
    ApiClientFilesystem,
    ApiClientSearch,
    ApiClientTools,
    ApiClientServer,
    ApiClientMetadata,
    ApiClientAuthors,
    ApiClientSeries,
    ApiClientPodcasts,
    ApiClientEmail,
    ApiClientNotification,
):
    """Combined Audiobookshelf API client.

    Aggregates every domain mixin into one client so the shared
    ``register_tool_surface`` helper can build one typed tool per operation from a
    single ``client_cls``.
    """


__all__ = [
    "ApiClientBase",
    "ApiClientSystem",
    "ApiClientLibraries",
    "ApiClientLibrariesExtra",
    "ApiClientItems",
    "ApiClientMe",
    "ApiClientUsers",
    "ApiClientSessions",
    "ApiClientCollections",
    "ApiClientPlaylists",
    "ApiClientBackups",
    "ApiClientFilesystem",
    "ApiClientSearch",
    "ApiClientTools",
    "ApiClientServer",
    "ApiClientMetadata",
    "ApiClientAuthors",
    "ApiClientSeries",
    "ApiClientPodcasts",
    "ApiClientEmail",
    "ApiClientNotification",
]

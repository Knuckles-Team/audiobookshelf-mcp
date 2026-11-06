from typing import Any

from .api_client_base import ApiClientBase


class ApiClientLibrariesExtra(ApiClientBase):
    """Audiobookshelf libraries operations."""

    def get_library_filter_data(
        self,
        id: str,
    ) -> Any:
        """Get a library's filter data (genres, tags, authors, series, languages)."""
        return self.request("GET", self._path("api", "libraries", id, "filterdata"))

    def get_library_stats(
        self,
        id: str,
    ) -> Any:
        """Get a library's statistics."""
        return self.request("GET", self._path("api", "libraries", id, "stats"))

    def get_library_personalized(
        self,
        id: str,
        limit: str | int | bool | None = None,
        include: str | int | bool | None = None,
    ) -> Any:
        """Get a library's personalized shelves."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "personalized"),
            params={
                k: v
                for k, v in {"limit": limit, "include": include}.items()
                if v is not None
            }
            or None,
        )

    def search_library(
        self,
        id: str,
        q: str | int | bool | None = None,
        limit: str | int | bool | None = None,
    ) -> Any:
        """Search a library for books, series, authors, tags and narrators."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "search"),
            params={k: v for k, v in {"q": q, "limit": limit}.items() if v is not None}
            or None,
        )

    def get_library_collections(
        self,
        id: str,
        limit: str | int | bool | None = None,
        page: str | int | bool | None = None,
        sort: str | int | bool | None = None,
        filter: str | int | bool | None = None,
        minified: str | int | bool | None = None,
    ) -> Any:
        """Get the collections of a library."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "collections"),
            params={
                k: v
                for k, v in {
                    "limit": limit,
                    "page": page,
                    "sort": sort,
                    "filter": filter,
                    "minified": minified,
                }.items()
                if v is not None
            }
            or None,
        )

    def get_library_playlists(
        self,
        id: str,
        limit: str | int | bool | None = None,
        page: str | int | bool | None = None,
    ) -> Any:
        """Get the current user's playlists of a library."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "playlists"),
            params={
                k: v for k, v in {"limit": limit, "page": page}.items() if v is not None
            }
            or None,
        )

    def scan_library(
        self,
        id: str,
        force: str | int | bool | None = None,
    ) -> Any:
        """Scan a library for new, changed and removed items."""
        return self.request(
            "POST",
            self._path("api", "libraries", id, "scan"),
            params={k: v for k, v in {"force": force}.items() if v is not None} or None,
        )

    def match_all_library_items(
        self,
        id: str,
    ) -> Any:
        """Quick match every item of a library."""
        return self.request("GET", self._path("api", "libraries", id, "matchall"))

    def order_libraries(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Set the display order of the libraries."""
        return self.request(
            "POST", self._path("api", "libraries", "order"), json=body or {}
        )

    def get_library_recent_episodes(
        self,
        id: str,
        limit: str | int | bool | None = None,
        page: str | int | bool | None = None,
    ) -> Any:
        """Get the most recent podcast episodes of a library."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "recent-episodes"),
            params={
                k: v for k, v in {"limit": limit, "page": page}.items() if v is not None
            }
            or None,
        )

    def get_library_episode_downloads(
        self,
        id: str,
        limit: str | int | bool | None = None,
    ) -> Any:
        """Get a podcast library's episode download queue."""
        return self.request(
            "GET",
            self._path("api", "libraries", id, "episode-downloads"),
            params={k: v for k, v in {"limit": limit}.items() if v is not None} or None,
        )

    def get_library_opml(
        self,
        id: str,
    ) -> Any:
        """Export a podcast library as OPML."""
        return self.request("GET", self._path("api", "libraries", id, "opml"))

    def remove_library_items_with_issues(
        self,
        id: str,
    ) -> Any:
        """Remove every item with issues from a library."""
        return self.request("DELETE", self._path("api", "libraries", id, "issues"))

from typing import Any

from .api_client_base import ApiClientBase


class ApiClientSessions(ApiClientBase):
    """Audiobookshelf sessions operations."""

    def get_sessions(
        self,
        items_per_page: str | int | bool | None = None,
        page: str | int | bool | None = None,
        user: str | int | bool | None = None,
        sort: str | int | bool | None = None,
        desc: str | int | bool | None = None,
    ) -> Any:
        """List listening sessions."""
        return self.request(
            "GET",
            self._path("api", "sessions"),
            params={
                k: v
                for k, v in {
                    "itemsPerPage": items_per_page,
                    "page": page,
                    "user": user,
                    "sort": sort,
                    "desc": desc,
                }.items()
                if v is not None
            }
            or None,
        )

    def get_open_sessions(
        self,
    ) -> Any:
        """List the currently open playback sessions."""
        return self.request("GET", self._path("api", "sessions", "open"))

    def get_session(
        self,
        id: str,
    ) -> Any:
        """Get a playback session."""
        return self.request("GET", self._path("api", "session", id))

    def sync_session(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Sync a playback session's progress."""
        return self.request(
            "POST", self._path("api", "session", id, "sync"), json=body or {}
        )

    def close_session(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Close a playback session."""
        return self.request(
            "POST", self._path("api", "session", id, "close"), json=body or {}
        )

    def delete_session(
        self,
        id: str,
    ) -> Any:
        """Delete a listening session."""
        return self.request("DELETE", self._path("api", "sessions", id))

    def batch_delete_sessions(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Delete several listening sessions."""
        return self.request(
            "POST", self._path("api", "sessions", "batch", "delete"), json=body or {}
        )

from typing import Any

from .api_client_base import ApiClientBase


class ApiClientMe(ApiClientBase):
    """Audiobookshelf me operations."""

    def get_me(
        self,
        include: str | int | bool | None = None,
    ) -> Any:
        """Get the authenticated user."""
        return self.request(
            "GET",
            self._path("api", "me"),
            params={k: v for k, v in {"include": include}.items() if v is not None}
            or None,
        )

    def get_my_listening_sessions(
        self,
        items_per_page: str | int | bool | None = None,
        page: str | int | bool | None = None,
    ) -> Any:
        """Get the authenticated user's listening sessions."""
        return self.request(
            "GET",
            self._path("api", "me", "listening-sessions"),
            params={
                k: v
                for k, v in {"itemsPerPage": items_per_page, "page": page}.items()
                if v is not None
            }
            or None,
        )

    def get_my_listening_stats(
        self,
    ) -> Any:
        """Get the authenticated user's listening statistics."""
        return self.request("GET", self._path("api", "me", "listening-stats"))

    def get_my_items_in_progress(
        self,
        limit: str | int | bool | None = None,
    ) -> Any:
        """Get the items the authenticated user is part way through."""
        return self.request(
            "GET",
            self._path("api", "me", "items-in-progress"),
            params={k: v for k, v in {"limit": limit}.items() if v is not None} or None,
        )

    def get_my_year_stats(
        self,
        year: str,
    ) -> Any:
        """Get the authenticated user's stats for a year."""
        return self.request("GET", self._path("api", "me", "stats", "year", year))

    def update_my_progress(
        self,
        library_item_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create or update the authenticated user's progress on an item."""
        return self.request(
            "PATCH",
            self._path("api", "me", "progress", library_item_id),
            json=body or {},
        )

    def update_my_episode_progress(
        self,
        library_item_id: str,
        episode_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create or update the authenticated user's progress on a podcast episode."""
        return self.request(
            "PATCH",
            self._path("api", "me", "progress", library_item_id, episode_id),
            json=body or {},
        )

    def delete_my_progress(
        self,
        progress_id: str,
    ) -> Any:
        """Remove a media progress entry."""
        return self.request("DELETE", self._path("api", "me", "progress", progress_id))

    def batch_update_my_progress(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update several media progress entries."""
        return self.request(
            "PATCH",
            self._path("api", "me", "progress", "batch", "update"),
            json=body or {},
        )

    def create_my_bookmark(
        self,
        library_item_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create a bookmark on a library item."""
        return self.request(
            "POST",
            self._path("api", "me", "item", library_item_id, "bookmark"),
            json=body or {},
        )

    def update_my_bookmark(
        self,
        library_item_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update a bookmark on a library item."""
        return self.request(
            "PATCH",
            self._path("api", "me", "item", library_item_id, "bookmark"),
            json=body or {},
        )

    def delete_my_bookmark(
        self,
        library_item_id: str,
        time: str,
    ) -> Any:
        """Delete a bookmark from a library item."""
        return self.request(
            "DELETE", self._path("api", "me", "item", library_item_id, "bookmark", time)
        )

    def change_my_password(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Change the authenticated user's password."""
        return self.request(
            "PATCH", self._path("api", "me", "password"), json=body or {}
        )

    def remove_item_from_continue_listening(
        self,
        progress_id: str,
    ) -> Any:
        """Hide a progress entry from continue listening."""
        return self.request(
            "GET",
            self._path(
                "api", "me", "progress", progress_id, "remove-from-continue-listening"
            ),
        )

    def remove_series_from_continue_listening(
        self,
        series_id: str,
    ) -> Any:
        """Hide a series from continue listening."""
        return self.request(
            "GET",
            self._path(
                "api", "me", "series", series_id, "remove-from-continue-listening"
            ),
        )

    def sync_local_progress(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Sync progress recorded by a local mobile client."""
        return self.request(
            "POST", self._path("api", "me", "sync-local-progress"), json=body or {}
        )

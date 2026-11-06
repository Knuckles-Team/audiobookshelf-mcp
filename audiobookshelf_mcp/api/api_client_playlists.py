from typing import Any

from .api_client_base import ApiClientBase


class ApiClientPlaylists(ApiClientBase):
    """Audiobookshelf playlists operations."""

    def get_playlists(
        self,
    ) -> Any:
        """List the current user's playlists."""
        return self.request("GET", self._path("api", "playlists"))

    def create_playlist(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create a playlist."""
        return self.request("POST", self._path("api", "playlists"), json=body or {})

    def get_playlist(
        self,
        id: str,
    ) -> Any:
        """Get a playlist."""
        return self.request("GET", self._path("api", "playlists", id))

    def update_playlist(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update a playlist."""
        return self.request(
            "PATCH", self._path("api", "playlists", id), json=body or {}
        )

    def delete_playlist(
        self,
        id: str,
    ) -> Any:
        """Delete a playlist."""
        return self.request("DELETE", self._path("api", "playlists", id))

    def add_item_to_playlist(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Add an item to a playlist."""
        return self.request(
            "POST", self._path("api", "playlists", id, "item"), json=body or {}
        )

    def remove_item_from_playlist(
        self,
        id: str,
        library_item_id: str,
    ) -> Any:
        """Remove an item from a playlist."""
        return self.request(
            "DELETE", self._path("api", "playlists", id, "item", library_item_id)
        )

    def batch_add_items_to_playlist(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Add several items to a playlist."""
        return self.request(
            "POST", self._path("api", "playlists", id, "batch", "add"), json=body or {}
        )

    def batch_remove_items_from_playlist(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Remove several items from a playlist."""
        return self.request(
            "POST",
            self._path("api", "playlists", id, "batch", "remove"),
            json=body or {},
        )

    def create_playlist_from_collection(
        self,
        collection_id: str,
    ) -> Any:
        """Create a playlist from a collection."""
        return self.request(
            "POST", self._path("api", "playlists", "collection", collection_id)
        )

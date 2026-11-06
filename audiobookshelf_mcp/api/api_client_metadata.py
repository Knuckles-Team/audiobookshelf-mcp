from typing import Any

from .api_client_base import ApiClientBase


class ApiClientMetadata(ApiClientBase):
    """Audiobookshelf metadata operations."""

    def get_tags(
        self,
    ) -> Any:
        """List every tag in use."""
        return self.request("GET", self._path("api", "tags"))

    def rename_tag(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Rename a tag across all items."""
        return self.request(
            "POST", self._path("api", "tags", "rename"), json=body or {}
        )

    def delete_tag(
        self,
        tag: str,
    ) -> Any:
        """Delete a tag from all items."""
        return self.request("DELETE", self._path("api", "tags", tag))

    def get_genres(
        self,
    ) -> Any:
        """List every genre in use."""
        return self.request("GET", self._path("api", "genres"))

    def rename_genre(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Rename a genre across all items."""
        return self.request(
            "POST", self._path("api", "genres", "rename"), json=body or {}
        )

    def delete_genre(
        self,
        genre: str,
    ) -> Any:
        """Delete a genre from all items."""
        return self.request("DELETE", self._path("api", "genres", genre))

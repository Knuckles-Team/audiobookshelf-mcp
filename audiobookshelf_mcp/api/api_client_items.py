from typing import Any

from .api_client_base import ApiClientBase


class ApiClientItems(ApiClientBase):
    """Audiobookshelf items operations."""

    def get_item(
        self,
        id: str,
        expanded: str | int | bool | None = None,
        include: str | int | bool | None = None,
        episode: str | int | bool | None = None,
    ) -> Any:
        """Get a library item by id."""
        return self.request(
            "GET",
            self._path("api", "items", id),
            params={
                k: v
                for k, v in {
                    "expanded": expanded,
                    "include": include,
                    "episode": episode,
                }.items()
                if v is not None
            }
            or None,
        )

    def delete_item(
        self,
        id: str,
        hard: str | int | bool | None = None,
    ) -> Any:
        """Remove a library item from the library (hard=1 also deletes files; use only on zz-validation items)."""
        return self.request(
            "DELETE",
            self._path("api", "items", id),
            params={k: v for k, v in {"hard": hard}.items() if v is not None} or None,
        )

    def update_item_media(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update a library item's media metadata and tags."""
        return self.request(
            "PATCH", self._path("api", "items", id, "media"), json=body or {}
        )

    def get_item_cover(
        self,
        id: str,
        width: str | int | bool | None = None,
        height: str | int | bool | None = None,
        format: str | int | bool | None = None,
        raw: str | int | bool | None = None,
    ) -> Any:
        """Get a library item's cover image."""
        return self.request(
            "GET",
            self._path("api", "items", id, "cover"),
            params={
                k: v
                for k, v in {
                    "width": width,
                    "height": height,
                    "format": format,
                    "raw": raw,
                }.items()
                if v is not None
            }
            or None,
        )

    def upload_item_cover(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Upload a cover for a library item from a url."""
        return self.request(
            "POST", self._path("api", "items", id, "cover"), json=body or {}
        )

    def update_item_cover(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Set a library item's cover to an existing path."""
        return self.request(
            "PATCH", self._path("api", "items", id, "cover"), json=body or {}
        )

    def delete_item_cover(
        self,
        id: str,
    ) -> Any:
        """Remove a library item's cover."""
        return self.request("DELETE", self._path("api", "items", id, "cover"))

    def match_item(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Quick match a library item against a metadata provider."""
        return self.request(
            "POST", self._path("api", "items", id, "match"), json=body or {}
        )

    def scan_item(
        self,
        id: str,
    ) -> Any:
        """Rescan a library item's files."""
        return self.request("POST", self._path("api", "items", id, "scan"))

    def play_item(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Start a playback session for a library item."""
        return self.request(
            "POST", self._path("api", "items", id, "play"), json=body or {}
        )

    def play_item_episode(
        self,
        id: str,
        episode_id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Start a playback session for a podcast episode."""
        return self.request(
            "POST", self._path("api", "items", id, "play", episode_id), json=body or {}
        )

    def get_item_ffprobe(
        self,
        id: str,
        file_id: str,
    ) -> Any:
        """Get the ffprobe data of a library item file."""
        return self.request("GET", self._path("api", "items", id, "ffprobe", file_id))

    def delete_item_file(
        self,
        id: str,
        file_id: str,
    ) -> Any:
        """Delete one file of a library item."""
        return self.request("DELETE", self._path("api", "items", id, "file", file_id))

    def update_item_chapters(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Replace a library item's chapters."""
        return self.request(
            "POST", self._path("api", "items", id, "chapters"), json=body or {}
        )

    def get_item_tone_object(
        self,
        id: str,
    ) -> Any:
        """Get the tone metadata object of a library item."""
        return self.request("GET", self._path("api", "items", id, "tone-object"))

    def batch_delete_items(
        self,
        hard: str | int | bool | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Remove several library items by id."""
        return self.request(
            "POST",
            self._path("api", "items", "batch", "delete"),
            params={k: v for k, v in {"hard": hard}.items() if v is not None} or None,
            json=body or {},
        )

    def batch_update_items(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update several library items."""
        return self.request(
            "POST", self._path("api", "items", "batch", "update"), json=body or {}
        )

    def batch_get_items(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Get several library items by id."""
        return self.request(
            "POST", self._path("api", "items", "batch", "get"), json=body or {}
        )

    def batch_quickmatch_items(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Quick match several library items."""
        return self.request(
            "POST", self._path("api", "items", "batch", "quickmatch"), json=body or {}
        )

    def batch_scan_items(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Rescan several library items."""
        return self.request(
            "POST", self._path("api", "items", "batch", "scan"), json=body or {}
        )

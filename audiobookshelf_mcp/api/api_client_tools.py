from typing import Any

from .api_client_base import ApiClientBase


class ApiClientTools(ApiClientBase):
    """Audiobookshelf tools operations."""

    def encode_item_m4b(
        self,
        id: str,
        token: str | int | bool | None = None,
        codec: str | int | bool | None = None,
        bitrate: str | int | bool | None = None,
        channels: str | int | bool | None = None,
    ) -> Any:
        """Encode a library item's audio files to a single m4b."""
        return self.request(
            "POST",
            self._path("api", "tools", "item", id, "encode-m4b"),
            params={
                k: v
                for k, v in {
                    "token": token,
                    "codec": codec,
                    "bitrate": bitrate,
                    "channels": channels,
                }.items()
                if v is not None
            }
            or None,
        )

    def cancel_item_m4b_encode(
        self,
        id: str,
    ) -> Any:
        """Cancel an m4b encode task."""
        return self.request(
            "DELETE", self._path("api", "tools", "item", id, "encode-m4b")
        )

    def embed_item_metadata(
        self,
        id: str,
        force_embed_chapters: str | int | bool | None = None,
        backup: str | int | bool | None = None,
    ) -> Any:
        """Embed a library item's metadata into its audio files."""
        return self.request(
            "POST",
            self._path("api", "tools", "item", id, "embed-metadata"),
            params={
                k: v
                for k, v in {
                    "forceEmbedChapters": force_embed_chapters,
                    "backup": backup,
                }.items()
                if v is not None
            }
            or None,
        )

    def batch_embed_metadata(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Embed metadata into several library items."""
        return self.request(
            "POST",
            self._path("api", "tools", "batch", "embed-metadata"),
            json=body or {},
        )

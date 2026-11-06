from typing import Any

from .api_client_base import ApiClientBase


class ApiClientFilesystem(ApiClientBase):
    """Audiobookshelf filesystem operations."""

    def get_filesystem_paths(
        self,
        level: str | int | bool | None = None,
    ) -> Any:
        """List the server's directories for choosing a library folder."""
        return self.request(
            "GET",
            self._path("api", "filesystem"),
            params={k: v for k, v in {"level": level}.items() if v is not None} or None,
        )

    def check_path_exists(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Check whether a path exists on the server."""
        return self.request(
            "POST", self._path("api", "filesystem", "pathexists"), json=body or {}
        )

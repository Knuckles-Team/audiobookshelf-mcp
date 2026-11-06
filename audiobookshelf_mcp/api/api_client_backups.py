from typing import Any

from .api_client_base import ApiClientBase


class ApiClientBackups(ApiClientBase):
    """Audiobookshelf backups operations."""

    def get_backups(
        self,
    ) -> Any:
        """List the server backups."""
        return self.request("GET", self._path("api", "backups"))

    def create_backup(
        self,
    ) -> Any:
        """Create a server backup."""
        return self.request("POST", self._path("api", "backups"))

    def delete_backup(
        self,
        id: str,
    ) -> Any:
        """Delete a server backup."""
        return self.request("DELETE", self._path("api", "backups", id))

    def apply_backup(
        self,
        id: str,
    ) -> Any:
        """Restore a server backup (replaces server data)."""
        return self.request("GET", self._path("api", "backups", id, "apply"))

    def update_backup_path(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Set the backup directory."""
        return self.request(
            "PATCH", self._path("api", "backups", "path"), json=body or {}
        )

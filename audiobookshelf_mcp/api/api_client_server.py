from typing import Any

from .api_client_base import ApiClientBase


class ApiClientServer(ApiClientBase):
    """Audiobookshelf server operations."""

    def get_server_status(
        self,
    ) -> Any:
        """Get the server status and initialisation state."""
        return self.request("GET", self._path("status"))

    def ping_server(
        self,
    ) -> Any:
        """Ping the server."""
        return self.request("GET", self._path("ping"))

    def healthcheck_server(
        self,
    ) -> Any:
        """Check the server health."""
        return self.request("GET", self._path("healthcheck"))

    def authorize(
        self,
    ) -> Any:
        """Return the authenticated user and server settings for the token."""
        return self.request("POST", self._path("api", "authorize"))

    def update_server_settings(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update the server settings."""
        return self.request("PATCH", self._path("api", "settings"), json=body or {})

    def update_sorting_prefixes(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update the sorting prefixes."""
        return self.request(
            "PATCH", self._path("api", "sorting-prefixes"), json=body or {}
        )

    def get_server_stats_year(
        self,
        year: str,
    ) -> Any:
        """Get server-wide stats for a year."""
        return self.request("GET", self._path("api", "stats", "year", year))

    def get_server_logs(
        self,
    ) -> Any:
        """Get recent server log entries."""
        return self.request("GET", self._path("api", "logger-data"))

    def purge_cache(
        self,
    ) -> Any:
        """Purge the server cache."""
        return self.request("POST", self._path("api", "cache", "purge"))

    def purge_items_cache(
        self,
    ) -> Any:
        """Purge the items cache."""
        return self.request("POST", self._path("api", "cache", "items", "purge"))

    def get_auth_settings(
        self,
    ) -> Any:
        """Get the authentication settings."""
        return self.request("GET", self._path("api", "auth-settings"))

    def update_auth_settings(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update the authentication settings."""
        return self.request(
            "PATCH", self._path("api", "auth-settings"), json=body or {}
        )

    def get_api_keys(
        self,
    ) -> Any:
        """List the API keys."""
        return self.request("GET", self._path("api", "api-keys"))

    def create_api_key(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create an API key."""
        return self.request("POST", self._path("api", "api-keys"), json=body or {})

    def update_api_key(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update an API key."""
        return self.request("PATCH", self._path("api", "api-keys", id), json=body or {})

    def delete_api_key(
        self,
        id: str,
    ) -> Any:
        """Delete an API key."""
        return self.request("DELETE", self._path("api", "api-keys", id))

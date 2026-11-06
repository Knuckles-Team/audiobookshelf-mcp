from typing import Any

from .api_client_base import ApiClientBase


class ApiClientUsers(ApiClientBase):
    """Audiobookshelf users operations."""

    def get_users(
        self,
        include: str | int | bool | None = None,
    ) -> Any:
        """List the server's users."""
        return self.request(
            "GET",
            self._path("api", "users"),
            params={k: v for k, v in {"include": include}.items() if v is not None}
            or None,
        )

    def create_user(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create a user."""
        return self.request("POST", self._path("api", "users"), json=body or {})

    def get_user(
        self,
        id: str,
        include: str | int | bool | None = None,
    ) -> Any:
        """Get a user by id."""
        return self.request(
            "GET",
            self._path("api", "users", id),
            params={k: v for k, v in {"include": include}.items() if v is not None}
            or None,
        )

    def update_user(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update a user."""
        return self.request("PATCH", self._path("api", "users", id), json=body or {})

    def delete_user(
        self,
        id: str,
    ) -> Any:
        """Delete a user."""
        return self.request("DELETE", self._path("api", "users", id))

    def get_user_listening_sessions(
        self,
        id: str,
        items_per_page: str | int | bool | None = None,
        page: str | int | bool | None = None,
    ) -> Any:
        """Get a user's listening sessions."""
        return self.request(
            "GET",
            self._path("api", "users", id, "listening-sessions"),
            params={
                k: v
                for k, v in {"itemsPerPage": items_per_page, "page": page}.items()
                if v is not None
            }
            or None,
        )

    def get_user_listening_stats(
        self,
        id: str,
    ) -> Any:
        """Get a user's listening statistics."""
        return self.request("GET", self._path("api", "users", id, "listening-stats"))

    def get_online_users(
        self,
    ) -> Any:
        """List the users currently online."""
        return self.request("GET", self._path("api", "users", "online"))

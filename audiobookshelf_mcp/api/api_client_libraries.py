from typing import Any

from .api_client_base import ApiClientBase


class ApiClientLibraries(ApiClientBase):
    """Library management operations (Audiobookshelf ``Libraries`` tag)."""

    def get_libraries(self) -> dict[str, Any]:
        """List all libraries."""
        return self.request("GET", "/api/libraries")

    def create_library(self, **body: Any) -> dict[str, Any]:
        """Create a new library."""
        return self.request("POST", "/api/libraries", json=body)

    def get_library_by_id(self, id: str, include: str | None = None) -> dict[str, Any]:
        """Get a single library by id."""
        params = {"include": include} if include else None
        return self.request("GET", f"/api/libraries/{id}", params=params)

    def update_library_by_id(self, id: str, **body: Any) -> dict[str, Any]:
        """Update a library by id."""
        return self.request("PATCH", f"/api/libraries/{id}", json=body)

    def delete_library_by_id(self, id: str) -> dict[str, Any]:
        """Delete a library by id."""
        return self.request("DELETE", f"/api/libraries/{id}")

    def get_library_authors(self, id: str) -> dict[str, Any]:
        """Get the authors within a library."""
        return self.request("GET", f"/api/libraries/{id}/authors")

    def delete_library_issues(self, id: str) -> dict[str, Any]:
        """Remove all library items that have issues from a library."""
        return self.request("DELETE", f"/api/libraries/{id}/issues")

    def get_library_items(self, id: str, **params: Any) -> dict[str, Any]:
        """Get the items within a library (supports limit/page/sort/filter params)."""
        return self.request("GET", f"/api/libraries/{id}/items", params=params or None)

    def get_library_series(self, id: str, **params: Any) -> dict[str, Any]:
        """Get the series within a library."""
        return self.request("GET", f"/api/libraries/{id}/series", params=params or None)

    def get_library_series_by_id(self, id: str, series_id: str) -> dict[str, Any]:
        """Get a single series within a library by id."""
        return self.request("GET", f"/api/libraries/{id}/series/{series_id}")

from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAuthors(ApiClientBase):
    """Author operations (Audiobookshelf ``Authors`` tag)."""

    def get_author_by_id(self, id: str, **params: Any) -> dict[str, Any]:
        """Get a single author by id (supports include/library params)."""
        return self.request("GET", f"/api/authors/{id}", params=params or None)

    def update_author_by_id(self, id: str, **body: Any) -> dict[str, Any]:
        """Update an author by id."""
        return self.request("PATCH", f"/api/authors/{id}", json=body)

    def delete_author_by_id(self, id: str) -> dict[str, Any]:
        """Delete an author by id."""
        return self.request("DELETE", f"/api/authors/{id}")

    def get_author_image_by_id(self, id: str, **params: Any) -> dict[str, Any]:
        """Get an author's image by id."""
        return self.request("GET", f"/api/authors/{id}/image", params=params or None)

    def add_author_image_by_id(self, id: str, **body: Any) -> dict[str, Any]:
        """Upload/add an author's image by id."""
        return self.request("POST", f"/api/authors/{id}/image", json=body)

    def update_author_image_by_id(self, id: str, **body: Any) -> dict[str, Any]:
        """Update an author's image by id."""
        return self.request("PATCH", f"/api/authors/{id}/image", json=body)

    def delete_author_image_by_id(self, id: str) -> dict[str, Any]:
        """Remove an author's image by id."""
        return self.request("DELETE", f"/api/authors/{id}/image")

    def match_author_by_id(
        self, id: str, q: str | None = None, **body: Any
    ) -> dict[str, Any]:
        """Match an author against a metadata provider by id."""
        if q is not None:
            body["q"] = q
        return self.request("POST", f"/api/authors/{id}/match", json=body)

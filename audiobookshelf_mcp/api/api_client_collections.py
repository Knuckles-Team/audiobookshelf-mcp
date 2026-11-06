from typing import Any

from .api_client_base import ApiClientBase


class ApiClientCollections(ApiClientBase):
    """Audiobookshelf collections operations."""

    def get_collections(
        self,
    ) -> Any:
        """List collections."""
        return self.request("GET", self._path("api", "collections"))

    def create_collection(
        self,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Create a collection."""
        return self.request("POST", self._path("api", "collections"), json=body or {})

    def get_collection(
        self,
        id: str,
    ) -> Any:
        """Get a collection."""
        return self.request("GET", self._path("api", "collections", id))

    def update_collection(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Update a collection."""
        return self.request(
            "PATCH", self._path("api", "collections", id), json=body or {}
        )

    def delete_collection(
        self,
        id: str,
    ) -> Any:
        """Delete a collection."""
        return self.request("DELETE", self._path("api", "collections", id))

    def add_book_to_collection(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Add a book to a collection."""
        return self.request(
            "POST", self._path("api", "collections", id, "book"), json=body or {}
        )

    def remove_book_from_collection(
        self,
        id: str,
        book_id: str,
    ) -> Any:
        """Remove a book from a collection."""
        return self.request(
            "DELETE", self._path("api", "collections", id, "book", book_id)
        )

    def batch_add_books_to_collection(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Add several books to a collection."""
        return self.request(
            "POST",
            self._path("api", "collections", id, "batch", "add"),
            json=body or {},
        )

    def batch_remove_books_from_collection(
        self,
        id: str,
        body: dict[str, Any] | None = None,
    ) -> Any:
        """Remove several books from a collection."""
        return self.request(
            "POST",
            self._path("api", "collections", id, "batch", "remove"),
            json=body or {},
        )

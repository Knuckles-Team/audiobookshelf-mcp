from typing import Any

from .api_client_base import ApiClientBase


class ApiClientSearch(ApiClientBase):
    """Audiobookshelf search operations."""

    def search_covers(
        self,
        title: str | int | bool | None = None,
        author: str | int | bool | None = None,
        provider: str | int | bool | None = None,
    ) -> Any:
        """Search metadata providers for covers."""
        return self.request(
            "GET",
            self._path("api", "search", "covers"),
            params={
                k: v
                for k, v in {
                    "title": title,
                    "author": author,
                    "provider": provider,
                }.items()
                if v is not None
            }
            or None,
        )

    def search_books(
        self,
        title: str | int | bool | None = None,
        author: str | int | bool | None = None,
        provider: str | int | bool | None = None,
        isbn: str | int | bool | None = None,
    ) -> Any:
        """Search metadata providers for books."""
        return self.request(
            "GET",
            self._path("api", "search", "books"),
            params={
                k: v
                for k, v in {
                    "title": title,
                    "author": author,
                    "provider": provider,
                    "isbn": isbn,
                }.items()
                if v is not None
            }
            or None,
        )

    def search_podcasts(
        self,
        term: str | int | bool | None = None,
    ) -> Any:
        """Search for podcasts."""
        return self.request(
            "GET",
            self._path("api", "search", "podcast"),
            params={k: v for k, v in {"term": term}.items() if v is not None} or None,
        )

    def search_authors(
        self,
        q: str | int | bool | None = None,
    ) -> Any:
        """Search for an author by name."""
        return self.request(
            "GET",
            self._path("api", "search", "authors"),
            params={k: v for k, v in {"q": q}.items() if v is not None} or None,
        )

    def search_chapters(
        self,
        asin: str | int | bool | None = None,
        region: str | int | bool | None = None,
    ) -> Any:
        """Search for chapters by ASIN."""
        return self.request(
            "GET",
            self._path("api", "search", "chapters"),
            params={
                k: v
                for k, v in {"asin": asin, "region": region}.items()
                if v is not None
            }
            or None,
        )
